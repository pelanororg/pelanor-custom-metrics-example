#!/usr/bin/env python3

import csv
import os
from collections import defaultdict
import requests
from dotenv import load_dotenv

CSV_FILE = "tenant_env_usage.csv"
BASE_URL = "https://api.pelanor.io/v1"
POST_URL = f"{BASE_URL}/custom-metrics"
TIMEOUT = 30


def build_series(csv_path: str, column: str):
    """
    Reads CSV and groups values into time series by a given dimension column.
    Returns a list of Pelanor-compatible property_value blocks.
    """
    bucket = defaultdict(list)
    with open(csv_path, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            key = row[column]
            bucket[key].append({
                "timestamp": row["timestamp"],
                "value": float(row["value_mb"])
            })
    return [{"property_value": k, "timeseries_point": v} for k, v in bucket.items()]


def post_metric(metric_name: str, dimension_name: str, series):
    """
    Sends a dimensional custom metric to the Pelanor API.
    """
    payload = {
        "metric_name": metric_name,
        "metric_data": {
            "Dimensional": {
                "data": series,
                "property_kind": {"Dimension": dimension_name}
            }
        }
    }

    resp = requests.post(
        POST_URL,
        json=payload,
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json",
        },
        timeout=TIMEOUT,
    )

    if resp.status_code in (200, 201):
        print(f"{metric_name} ({dimension_name}) created – id {resp.json().get('id')}")
    else:
        print(f"{metric_name} failed – {resp.status_code} {resp.text}")


def main():
    """
    Builds and uploads two dimensional metrics: one for Tenants, one for Environment.
    """
    tenant_series = build_series(CSV_FILE, "tenant")
    env_series = build_series(CSV_FILE, "environment")

    post_metric("tenant_usage", "Tenants", tenant_series)
    post_metric("environment_usage", "Environment", env_series)


if __name__ == "__main__":
    load_dotenv()
    API_TOKEN = os.getenv("PELANOR_API_TOKEN")
    if not API_TOKEN:
        raise RuntimeError("PELANOR_API_TOKEN missing")

    main()
