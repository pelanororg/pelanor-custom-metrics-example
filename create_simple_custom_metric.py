#!/usr/bin/env python3
"""
Upload Daily Active Users from dau_timeseries.csv as a plain custom metric.
"""

import csv
import os
import requests
from dotenv import load_dotenv

CSV_FILE = "dau_timeseries.csv"
BASE_URL = "https://api.pelanor.io/v1"
CUSTOM_METRIC_URL = f"{BASE_URL}/custom-metrics"


def read_points(path: str):
    """
    Reads timestamp/value pairs from the CSV file.
    Returns a list of dicts compatible with the Pelanor API.
    """
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return [
            {"timestamp": row["timestamp"], "value": int(row["value"])}
            for row in reader
        ]


def main():
    """
    Loads environment variables, reads data from CSV, and uploads it to Pelanor.
    """
    load_dotenv()
    token = os.getenv("PELANOR_API_TOKEN")
    if not token:
        raise RuntimeError("PELANOR_API_TOKEN missing; set it in .env or env vars")

    points = read_points(CSV_FILE)

    payload = {
        "metric_name": "Daily Active Users",
        "metric_data": {
            "Plain": {
                "data": points
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    resp = requests.post(CUSTOM_METRIC_URL, json=payload, headers=headers, timeout=30)
    if resp.status_code in (200, 201):
        print("Metric created successfully – id =", resp.json().get("id"))
    else:
        print("Metric creation failed –", resp.status_code, resp.text)


if __name__ == "__main__":
    main()
