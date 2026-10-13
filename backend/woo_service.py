"""WooCommerce API access with a local mock-data fallback.

Mock mode is used when WC_URL is unset. To switch to live mode, add WC_URL,
WC_KEY, and WC_SECRET to the project .env file using WooCommerce REST API v3
credentials, then restart the backend.
"""

import os
import sys

import requests
from dotenv import load_dotenv


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

from data.mock_data import CUSTOMERS, ORDERS


WC_URL = os.getenv("WC_URL")
WC_KEY = os.getenv("WC_KEY")
WC_SECRET = os.getenv("WC_SECRET")


def is_live():
	"""Return whether live WooCommerce API access is configured."""
	return bool(WC_URL)


def _fetch_resource(resource):
	"""Fetch all pages for a WooCommerce REST API resource."""
	results = []
	page = 1
	url = f"{WC_URL.rstrip('/')}/wp-json/wc/v3/{resource}"

	while True:
		response = requests.get(
			url,
			auth=(WC_KEY, WC_SECRET),
			params={"per_page": 100, "page": page},
			timeout=20,
		)
		response.raise_for_status()
		items = response.json()
		results.extend(items)

		if len(items) < 100:
			return results

		page += 1


def fetch_customers():
	"""Return WooCommerce customers or the local mock customers."""
	if not is_live():
		return CUSTOMERS
	return _fetch_resource("customers")


def fetch_orders():
	"""Return WooCommerce orders or the local mock orders."""
	if not is_live():
		return ORDERS
	return _fetch_resource("orders")
