from datetime import datetime, timedelta, timezone


def compute_segment(
	total_spent: float, orders_count: int, last_order_at: str | None
) -> str:
	"""Assign VIP, At-risk, Repeat, or New based on spending and order history.

	VIP takes priority for high spend or frequent orders. Otherwise, customers
	with an order more than 60 days ago are At-risk, customers with multiple
	orders are Repeat, and everyone else is New. Missing or invalid dates do
	not trigger the At-risk segment.
	"""
	if total_spent >= 20000 or orders_count >= 5:
		return "VIP"

	if orders_count > 0 and last_order_at:
		date_string = last_order_at
		if date_string.endswith("Z"):
			date_string = date_string[:-1] + "+00:00"

		try:
			last_order_date = datetime.fromisoformat(date_string)
		except ValueError:
			last_order_date = None

		if last_order_date is not None:
			now = datetime.now(last_order_date.tzinfo)
			if (now - last_order_date).days > 60:
				return "At-risk"

	if orders_count >= 2:
		return "Repeat"

	return "New"


if __name__ == "__main__":
	old_order_date = (
		datetime.now(timezone.utc) - timedelta(days=61)
	).isoformat().replace("+00:00", "Z")
	print(compute_segment(25000, 1, None))
	print(compute_segment(500, 1, old_order_date))
	print(compute_segment(1000, 3, None))
	print(compute_segment(0, 0, None))
