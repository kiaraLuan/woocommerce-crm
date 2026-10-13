import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crm.db")


def get_conn():
	"""Open a CRM database connection that returns rows by column name."""
	connection = sqlite3.connect(DB_PATH)
	connection.row_factory = sqlite3.Row
	return connection


def init_db():
	"""Create the CRM tables when they do not already exist."""
	connection = get_conn()
	try:
		connection.executescript(
			"""
			-- Stores WooCommerce customer profiles and CRM summaries.
			CREATE TABLE IF NOT EXISTS customers (
				id INTEGER PRIMARY KEY,
				woo_id INTEGER UNIQUE,
				name TEXT,
				email TEXT,
				phone TEXT,
				city TEXT,
				total_spent REAL DEFAULT 0,
				orders_count INTEGER DEFAULT 0,
				last_order_at TEXT,
				segment TEXT DEFAULT 'New'
			);

			-- Tracks WooCommerce orders linked to their customers.
			CREATE TABLE IF NOT EXISTS orders (
				id INTEGER PRIMARY KEY,
				woo_id INTEGER UNIQUE,
				customer_woo_id INTEGER,
				status TEXT,
				total REAL,
				created_at TEXT,
				updated_at TEXT
			);

			-- Records each status change for an order over time.
			CREATE TABLE IF NOT EXISTS order_events (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				order_woo_id INTEGER,
				status TEXT,
				ts TEXT
			);

			-- Keeps a history of automated or manual customer messages.
			CREATE TABLE IF NOT EXISTS messages (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				customer_woo_id INTEGER,
				order_woo_id INTEGER,
				template TEXT,
				body TEXT,
				sent_at TEXT
			);
			"""
		)
	finally:
		connection.close()
