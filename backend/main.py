import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import database
import segmentation
import woo_service
import workflows


app = FastAPI(title="WooCommerce CRM")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

FRONTEND_PATH = os.path.join(
	os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "index.html"
)


class StatusUpdate(BaseModel):
	order_id: int
	status: str


@app.on_event("startup")
def initialize_database():
	"""Create the CRM tables when the API starts."""
	database.init_db()


@app.get("/", response_class=FileResponse)
def dashboard():
	"""Serve the single-file CRM dashboard."""
	return FileResponse(FRONTEND_PATH)


@app.post("/sync")
def sync_data():
	"""Import WooCommerce data and refresh CRM customer summaries."""
	customers = woo_service.fetch_customers()
	orders = woo_service.fetch_orders()

	with database.get_conn() as conn:
		messages_before = conn.execute(
			"SELECT COUNT(*) AS count FROM messages"
		).fetchone()["count"]

		for customer in customers:
			billing = customer.get("billing") or {}
			name = " ".join(
				part
				for part in (customer.get("first_name"), customer.get("last_name"))
				if part
			).strip()
			conn.execute(
				"""
				INSERT INTO customers (
					woo_id, name, email, phone, city, total_spent,
					orders_count, last_order_at, segment
				) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
				ON CONFLICT(woo_id) DO UPDATE SET
					name = excluded.name,
					email = excluded.email,
					phone = excluded.phone,
					city = excluded.city,
					total_spent = excluded.total_spent,
					orders_count = excluded.orders_count,
					last_order_at = excluded.last_order_at,
					segment = excluded.segment
				""",
				(
					customer["id"],
					name or customer.get("email") or "Customer",
					customer.get("email"),
					billing.get("phone"),
					billing.get("city"),
					float(customer.get("total_spent") or 0),
					int(customer.get("orders_count") or 0),
					customer.get("last_order_at"),
					"New",
				),
			)

		for order in orders:
			previous = conn.execute(
				"SELECT status FROM orders WHERE woo_id = ?", (order["id"],)
			).fetchone()
			conn.execute(
				"""
				INSERT INTO orders (
					woo_id, customer_woo_id, status, total, created_at, updated_at
				) VALUES (?, ?, ?, ?, ?, ?)
				ON CONFLICT(woo_id) DO UPDATE SET
					customer_woo_id = excluded.customer_woo_id,
					status = excluded.status,
					total = excluded.total,
					created_at = excluded.created_at,
					updated_at = excluded.updated_at
				""",
				(
					order["id"],
					order.get("customer_id"),
					order.get("status"),
					float(order.get("total") or 0),
					order.get("date_created"),
					order.get("date_modified"),
				),
			)
			if previous is None or previous["status"] != order.get("status"):
				workflows.on_status_change(conn, order["id"], order.get("status"))

		for customer in conn.execute("SELECT woo_id FROM customers").fetchall():
			summary = conn.execute(
				"""
				SELECT
					COALESCE(SUM(total), 0) AS total_spent,
					COUNT(*) AS orders_count,
					MAX(created_at) AS last_order_at
				FROM orders
				WHERE customer_woo_id = ? AND status != 'cancelled'
				""",
				(customer["woo_id"],),
			).fetchone()
			segment = segmentation.compute_segment(
				float(summary["total_spent"] or 0),
				int(summary["orders_count"] or 0),
				summary["last_order_at"],
			)
			conn.execute(
				"""
				UPDATE customers
				SET total_spent = ?, orders_count = ?, last_order_at = ?, segment = ?
				WHERE woo_id = ?
				""",
				(
					float(summary["total_spent"] or 0),
					int(summary["orders_count"] or 0),
					summary["last_order_at"],
					segment,
					customer["woo_id"],
				),
			)

		messages_after = conn.execute(
			"SELECT COUNT(*) AS count FROM messages"
		).fetchone()["count"]
		conn.commit()

	return {
		"customers": len(customers),
		"orders": len(orders),
		"new_messages": messages_after - messages_before,
	}


@app.get("/customers")
def list_customers(segment: str | None = None):
	"""List CRM customers, optionally filtered by segment."""
	with database.get_conn() as conn:
		if segment:
			rows = conn.execute(
				"SELECT * FROM customers WHERE segment = ? ORDER BY name", (segment,)
			).fetchall()
		else:
			rows = conn.execute("SELECT * FROM customers ORDER BY name").fetchall()
	return [dict(row) for row in rows]


@app.get("/customers/{woo_id}")
def get_customer(woo_id: int):
	"""Return a customer's profile, orders, and message history."""
	with database.get_conn() as conn:
		profile = conn.execute(
			"SELECT * FROM customers WHERE woo_id = ?", (woo_id,)
		).fetchone()
		if profile is None:
			raise HTTPException(status_code=404, detail="Customer not found")
		orders = conn.execute(
			"SELECT * FROM orders WHERE customer_woo_id = ? ORDER BY created_at DESC",
			(woo_id,),
		).fetchall()
		messages = conn.execute(
			"SELECT * FROM messages WHERE customer_woo_id = ? ORDER BY sent_at DESC",
			(woo_id,),
		).fetchall()
	return {
		"profile": dict(profile),
		"orders": [dict(row) for row in orders],
		"messages": [dict(row) for row in messages],
	}


@app.get("/orders")
def list_orders(status: str | None = None):
	"""List CRM orders, optionally filtered by status."""
	with database.get_conn() as conn:
		if status:
			rows = conn.execute(
				"SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC",
				(status,),
			).fetchall()
		else:
			rows = conn.execute(
				"SELECT * FROM orders ORDER BY created_at DESC"
			).fetchall()
	return [dict(row) for row in rows]


@app.get("/orders/{woo_id}/timeline")
def get_order_timeline(woo_id: int):
	"""Return an order's status events in chronological order."""
	with database.get_conn() as conn:
		rows = conn.execute(
			"SELECT * FROM order_events WHERE order_woo_id = ? ORDER BY ts, id",
			(woo_id,),
		).fetchall()
	return [dict(row) for row in rows]


@app.get("/messages")
def list_messages():
	"""List saved messages from newest to oldest."""
	with database.get_conn() as conn:
		rows = conn.execute(
			"SELECT * FROM messages ORDER BY sent_at DESC, id DESC"
		).fetchall()
	return [dict(row) for row in rows]


@app.get("/stats")
def get_stats():
	"""Return CRM totals, revenue, segment/status counts, and data mode."""
	with database.get_conn() as conn:
		totals = conn.execute(
			"""
			SELECT
				(SELECT COUNT(*) FROM customers) AS total_customers,
				(SELECT COUNT(*) FROM orders) AS total_orders,
				(SELECT COALESCE(SUM(total), 0) FROM orders
				 WHERE status NOT IN ('cancelled', 'refunded')) AS total_revenue
			"""
		).fetchone()
		segment_rows = conn.execute(
			"SELECT segment, COUNT(*) AS count FROM customers GROUP BY segment"
		).fetchall()
		status_rows = conn.execute(
			"SELECT status, COUNT(*) AS count FROM orders GROUP BY status"
		).fetchall()
	return {
		"total_customers": totals["total_customers"],
		"total_orders": totals["total_orders"],
		"total_revenue": totals["total_revenue"],
		"counts_per_segment": {row["segment"]: row["count"] for row in segment_rows},
		"counts_per_order_status": {row["status"]: row["count"] for row in status_rows},
		"mode": "live" if woo_service.is_live() else "mock",
	}


@app.post("/simulate/status")
def simulate_status_change(update: StatusUpdate):
	"""Update an order status and run its status-change workflow."""
	with database.get_conn() as conn:
		order = conn.execute(
			"SELECT woo_id FROM orders WHERE woo_id = ?", (update.order_id,)
		).fetchone()
		if order is None:
			raise HTTPException(status_code=404, detail="Order not found")
		conn.execute(
			"UPDATE orders SET status = ?, updated_at = ? WHERE woo_id = ?",
			(update.status, datetime.now().isoformat(), update.order_id),
		)
		workflows.on_status_change(conn, update.order_id, update.status)
	return {"order_id": update.order_id, "status": update.status}


@app.post("/workflows/winback")
def start_winback():
	"""Send winback messages to at-risk customers and return the count."""
	with database.get_conn() as conn:
		count = workflows.run_winback(conn)
	return {"count": count}
