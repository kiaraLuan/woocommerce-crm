from datetime import datetime


TEMPLATES = {
	"processing": (
		"Hi {name}, your order #{oid} for ₹{total} is being prepared. "
		"We will keep you updated! 📦"
	),
	"on-hold": (
		"Hi {name}, order #{oid} for ₹{total} is currently on hold. "
		"Please contact us if you need help. 💬"
	),
	"completed": (
		"Hi {name}, order #{oid} is complete. Thank you for shopping with us "
		"for ₹{total}! 🎉"
	),
	"cancelled": (
		"Hi {name}, order #{oid} for ₹{total} was cancelled. "
		"Get in touch if you have any questions. ℹ️"
	),
	"refunded": (
		"Hi {name}, your refund of ₹{total} for order #{oid} has been processed. "
		"Thank you for your patience. 💸"
	),
	"winback": (
		"Hi {name}, we miss you! Enjoy 10% off your next order with us. "
		"We hope to see you again soon. 🎁"
	),
}


def send_message(conn, customer_row, order_id, template_key, total):
	"""Format a template, save the message, and print the email preview."""
	total_amount = f"{float(total):.2f}" if total is not None else "0.00"
	body = TEMPLATES[template_key].format(
		name=customer_row["name"] or "there",
		oid=order_id if order_id is not None else "",
		total=total_amount,
	)
	conn.execute(
		"""
		INSERT INTO messages (
			customer_woo_id, order_woo_id, template, body, sent_at
		) VALUES (?, ?, ?, ?, ?)
		""",
		(
			customer_row["woo_id"],
			order_id,
			template_key,
			body,
			datetime.now().isoformat(),
		),
	)
	conn.commit()
	print(f"[EMAIL to {customer_row['email']}] {body}")

	# Mailtrap example for sending instead of printing:
	# import os
	# import smtplib
	# from email.message import EmailMessage
	# mail = EmailMessage()
	# mail["Subject"] = f"Order update #{order_id}"
	# mail["From"] = os.getenv("MAIL_FROM")
	# mail["To"] = customer_row["email"]
	# mail.set_content(body)
	# with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as smtp:
	#     smtp.starttls()
	#     smtp.login(os.getenv("MAILTRAP_USERNAME"), os.getenv("MAILTRAP_PASSWORD"))
	#     smtp.send_message(mail)


def on_status_change(conn, order_id, new_status):
	"""Record an order status event and send its matching customer message."""
	conn.execute(
		"INSERT INTO order_events (order_woo_id, status, ts) VALUES (?, ?, ?)",
		(order_id, new_status, datetime.now().isoformat()),
	)
	order = conn.execute(
		"SELECT * FROM orders WHERE woo_id = ?", (order_id,)
	).fetchone()
	if order is None:
		conn.commit()
		return

	customer = conn.execute(
		"SELECT * FROM customers WHERE woo_id = ?", (order["customer_woo_id"],)
	).fetchone()
	if customer is None:
		conn.commit()
		return

	if new_status in TEMPLATES:
		send_message(conn, customer, order_id, new_status, order["total"])
	else:
		conn.commit()


def run_winback(conn):
	"""Send a 10% winback offer to every customer in the At-risk segment."""
	customers = conn.execute(
		"SELECT * FROM customers WHERE segment = ?", ("At-risk",)
	).fetchall()
	for customer in customers:
		send_message(conn, customer, None, "winback", None)
	return len(customers)
