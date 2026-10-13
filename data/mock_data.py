from datetime import datetime, timedelta


def _date_days_ago(days):
	return (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")


CUSTOMERS = [
	{
		"id": 1,
		"first_name": "Aarav",
		"last_name": "Sharma",
		"email": "aarav.sharma@example.com",
		"billing": {"phone": "+91 98765 43210", "city": "Mumbai"},
	},
	{
		"id": 2,
		"first_name": "Ananya",
		"last_name": "Patel",
		"email": "ananya.patel@example.com",
		"billing": {"phone": "+91 98765 43211", "city": "Ahmedabad"},
	},
	{
		"id": 3,
		"first_name": "Vihaan",
		"last_name": "Reddy",
		"email": "vihaan.reddy@example.com",
		"billing": {"phone": "+91 98765 43212", "city": "Hyderabad"},
	},
	{
		"id": 4,
		"first_name": "Diya",
		"last_name": "Iyer",
		"email": "diya.iyer@example.com",
		"billing": {"phone": "+91 98765 43213", "city": "Chennai"},
	},
	{
		"id": 5,
		"first_name": "Kabir",
		"last_name": "Singh",
		"email": "kabir.singh@example.com",
		"billing": {"phone": "+91 98765 43214", "city": "New Delhi"},
	},
	{
		"id": 6,
		"first_name": "Meera",
		"last_name": "Nair",
		"email": "meera.nair@example.com",
		"billing": {"phone": "+91 98765 43215", "city": "Kochi"},
	},
	{
		"id": 7,
		"first_name": "Arjun",
		"last_name": "Desai",
		"email": "arjun.desai@example.com",
		"billing": {"phone": "+91 98765 43216", "city": "Pune"},
	},
	{
		"id": 8,
		"first_name": "Ishita",
		"last_name": "Mukherjee",
		"email": "ishita.mukherjee@example.com",
		"billing": {"phone": "+91 98765 43217", "city": "Kolkata"},
	},
	{
		"id": 9,
		"first_name": "Rohan",
		"last_name": "Kulkarni",
		"email": "rohan.kulkarni@example.com",
		"billing": {"phone": "+91 98765 43218", "city": "Bengaluru"},
	},
	{
		"id": 10,
		"first_name": "Sana",
		"last_name": "Khan",
		"email": "sana.khan@example.com",
		"billing": {"phone": "+91 98765 43219", "city": "Jaipur"},
	},
	{
		"id": 11,
		"first_name": "Aditya",
		"last_name": "Joshi",
		"email": "aditya.joshi@example.com",
		"billing": {"phone": "+91 98765 43220", "city": "Nagpur"},
	},
	{
		"id": 12,
		"first_name": "Priya",
		"last_name": "Menon",
		"email": "priya.menon@example.com",
		"billing": {"phone": "+91 98765 43221", "city": "Thiruvananthapuram"},
	},
]


ORDERS = [
	{"id": 1001, "customer_id": 1, "status": "completed", "total": "6999.00", "date_created": _date_days_ago(120), "date_modified": _date_days_ago(119)},
	{"id": 1002, "customer_id": 1, "status": "processing", "total": "3499.00", "date_created": _date_days_ago(90), "date_modified": _date_days_ago(89)},
	{"id": 1003, "customer_id": 1, "status": "completed", "total": "1299.00", "date_created": _date_days_ago(65), "date_modified": _date_days_ago(64)},
	{"id": 1004, "customer_id": 1, "status": "on-hold", "total": "5999.00", "date_created": _date_days_ago(40), "date_modified": _date_days_ago(39)},
	{"id": 1005, "customer_id": 1, "status": "completed", "total": "2499.00", "date_created": _date_days_ago(25), "date_modified": _date_days_ago(24)},
	{"id": 1006, "customer_id": 1, "status": "processing", "total": "899.00", "date_created": _date_days_ago(12), "date_modified": _date_days_ago(11)},
	{"id": 1007, "customer_id": 1, "status": "completed", "total": "4999.00", "date_created": _date_days_ago(3), "date_modified": _date_days_ago(2)},
	{"id": 1008, "customer_id": 2, "status": "completed", "total": "8499.00", "date_created": _date_days_ago(150), "date_modified": _date_days_ago(149)},
	{"id": 1009, "customer_id": 2, "status": "processing", "total": "1999.00", "date_created": _date_days_ago(110), "date_modified": _date_days_ago(109)},
	{"id": 1010, "customer_id": 2, "status": "completed", "total": "4299.00", "date_created": _date_days_ago(75), "date_modified": _date_days_ago(74)},
	{"id": 1011, "customer_id": 2, "status": "on-hold", "total": "9999.00", "date_created": _date_days_ago(50), "date_modified": _date_days_ago(49)},
	{"id": 1012, "customer_id": 2, "status": "completed", "total": "1599.00", "date_created": _date_days_ago(30), "date_modified": _date_days_ago(29)},
	{"id": 1013, "customer_id": 2, "status": "cancelled", "total": "699.00", "date_created": _date_days_ago(18), "date_modified": _date_days_ago(17)},
	{"id": 1014, "customer_id": 2, "status": "processing", "total": "2499.00", "date_created": _date_days_ago(8), "date_modified": _date_days_ago(7)},
	{"id": 1015, "customer_id": 2, "status": "completed", "total": "5999.00", "date_created": _date_days_ago(1), "date_modified": _date_days_ago(0)},
	{"id": 1016, "customer_id": 3, "status": "completed", "total": "2499.00", "date_created": _date_days_ago(50), "date_modified": _date_days_ago(49)},
	{"id": 1017, "customer_id": 3, "status": "processing", "total": "899.00", "date_created": _date_days_ago(25), "date_modified": _date_days_ago(24)},
	{"id": 1018, "customer_id": 3, "status": "completed", "total": "1799.00", "date_created": _date_days_ago(5), "date_modified": _date_days_ago(4)},
	{"id": 1019, "customer_id": 4, "status": "on-hold", "total": "3499.00", "date_created": _date_days_ago(45), "date_modified": _date_days_ago(44)},
	{"id": 1020, "customer_id": 4, "status": "completed", "total": "1299.00", "date_created": _date_days_ago(20), "date_modified": _date_days_ago(19)},
	{"id": 1021, "customer_id": 4, "status": "refunded", "total": "799.00", "date_created": _date_days_ago(4), "date_modified": _date_days_ago(3)},
	{"id": 1022, "customer_id": 5, "status": "pending", "total": "1999.00", "date_created": _date_days_ago(35), "date_modified": _date_days_ago(34)},
	{"id": 1023, "customer_id": 5, "status": "processing", "total": "4499.00", "date_created": _date_days_ago(15), "date_modified": _date_days_ago(14)},
	{"id": 1024, "customer_id": 5, "status": "completed", "total": "999.00", "date_created": _date_days_ago(2), "date_modified": _date_days_ago(1)},
	{"id": 1025, "customer_id": 6, "status": "completed", "total": "1799.00", "date_created": _date_days_ago(75), "date_modified": _date_days_ago(74)},
	{"id": 1026, "customer_id": 7, "status": "on-hold", "total": "2499.00", "date_created": _date_days_ago(95), "date_modified": _date_days_ago(94)},
	{"id": 1027, "customer_id": 8, "status": "refunded", "total": "899.00", "date_created": _date_days_ago(120), "date_modified": _date_days_ago(119)},
	{"id": 1028, "customer_id": 9, "status": "processing", "total": "1499.00", "date_created": _date_days_ago(6), "date_modified": _date_days_ago(5)},
	{"id": 1029, "customer_id": 10, "status": "pending", "total": "3299.00", "date_created": _date_days_ago(2), "date_modified": _date_days_ago(1)},
	{"id": 1030, "customer_id": 11, "status": "completed", "total": "599.00", "date_created": _date_days_ago(0), "date_modified": _date_days_ago(0)},
]
