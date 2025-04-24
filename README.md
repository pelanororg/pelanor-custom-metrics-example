# Pelanor Custom Metric Uploads

This repo includes scripts to push business metrics into Pelanor’s **Unit Cost Analysis** via the API.

## Requirements

- Python 3.8+
- `pip install python-dotenv requests`
- Create a `.env` file in the project root:

`PELANOR_API_TOKEN=<your-token>`

---

## 1. Upload Daily Active Users

**Script:** `upload_dau_metric.py`  
**Metric type:** Basic (plain)  
**CSV:** `dau_timeseries.csv`

Example format:

`timestamp,value 2025-04-01,1020 2025-04-02,985`


Run:

`python upload_dau_metric.py`


---

## 2. Upload Tenants & Environment Metrics

**Script:** `upload_tenant_env_metrics.py`  
**Metric type:** Dimensional  
**CSV:** `tenant_env_usage.csv`

Example format:

`tenant,environment,timestamp,value_mb Alpha,Production,2025-04-01,32450.0`


Creates:

- `tenant_usage` with dimension `Tenants`
- `environment_usage` with dimension `Environment`

Run:

`python upload_tenant_env_metrics.py`


---

## After Upload

- Go to the **Unit Cost** section in Pelanor
- Select your metric
- Set cost filters, aggregation, and date range
- View trends and breakdowns in the dashboard or Explore tab
s
