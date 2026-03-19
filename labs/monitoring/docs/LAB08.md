# Prometheus Setup Documentation

## Task 1

Configure app with prometheus client

1) `/metrics` endpoint:

![alt text](image-9.png)

2) [Code](../../app_python/app.py) showing metrics def-s:

```python
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently being processed'
)

# Business / domain metrics (Beyond HTTP)
# Track endpoint usage (separate from http_requests_total)
endpoint_calls = Counter(
    "devops_info_endpoint_calls",
    "Endpoint calls",
    ["endpoint"],
)

# Track system info collection time
system_info_duration = Histogram(
    "devops_info_system_collection_seconds",
    "System info collection time",
)

# Examples for typical business metrics (wire them when you add the real integrations)
external_service_calls = Counter(
    "devops_info_external_service_calls_total",
    "API calls to external services",
    ["service", "result"],  # keep low-cardinality (e.g., result: ok|error|timeout)
)

cache_items = Gauge(
    "devops_info_cache_items",
    "Items in cache",
)

db_pool_size = Gauge(
    "devops_info_db_pool_size",
    "Current DB pool size",
)
```

## Task 2

Prometheus server setup and demostration

1) Screenshot of `/targets` page showing all targets UP
![alt text](image-11.png)

2) Screenshot of a successful PromQL query:
![alt text](image-10.png)

3) [Configuration file](../prometheus/config.yaml)

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["prometheus:9090"]

  - job_name: app-python
    metrics_path: /metrics
    static_configs:
      - targets: ["app-python:8080"]
```

## Task 3

Grafana dashboards for Prometheus setup

Setup Prometheus as a data source and start boards:
![alt text](image-12.png)

1) Screenshot of your custom application dashboard with live data
![alt text](image-14.png)

Shows avg time of `get_system_info()` function.

```promql
sum(rate(devops_info_system_collection_seconds_sum[5m])) / sum(rate(devops_info_system_collection_seconds_count[5m]))
```

2) All 6+ panels working
![alt text](image-13.png)   

Import of `3662` dashboard

![alt text](image-15.png)

3) JSON exported dashboard here: [../prometheus/dashboard-my.json](../prometheus/dashboard-my.json)

## Task 4

1) `docker compose ps` healthy
```bash
docker compose ps
NAME            IMAGE                                   COMMAND                  SERVICE      CREATED          STATUS                      PORTS
devops-python   projacktor/python-info-service:latest   "python app.py"          app-python   38 minutes ago   Up 38 minutes               0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
grafana         grafana/grafana:12.3.1                  "/run.sh"                grafana      38 minutes ago   Up 38 minutes (healthy)     0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp
loki            grafana/loki:3.0.0                      "/usr/bin/loki -conf…"   loki         38 minutes ago   Up 38 minutes (unhealthy)   0.0.0.0:3100->3100/tcp, [::]:3100->3100/tcp
prometheus      prom/prometheus:v3.9.0                  "/bin/prometheus --c…"   prometheus   38 minutes ago   Up 38 minutes               0.0.0.0:9000->9090/tcp, [::]:9000->9090/tcp
promtail        grafana/promtail:3.0.0                  "/usr/bin/promtail -…"   promtail     38 minutes ago   Up 38 minutes               0.0.0.0:9080->9080/tcp, [::]:9080->9080/tcp
```

2) Documentation of retention policies

#### Prometheus retention policy
Prometheus retention is configured via startup arguments in `compose.yaml`:

- `--storage.tsdb.retention.time=15d`
- `--storage.tsdb.retention.size=10GB`

This means:
- metrics are stored for a maximum of **15 days**;
- or deleted earlier if the TSDB size exceeds **10GB**;
- whichever limit is reached first (time or size) is triggered.

Purpose of this setting:
- control disk usage;
- maintain a sufficient history window for analyzing trends and incidents;
- avoid performance degradation due to uncontrolled TSDB growth.

#### Persistence
Prometheus data is stored in the volume:
- `prometheus-data:/prometheus`

Therefore, after `docker compose down` / `up -d`, data is not lost (unless the volume is deleted with the `-v` command).

#### Other stack components
- **Loki** and **Grafana** also use persistent volumes (`loki-data`, `grafana-data`), which ensures data/dashboards persist across restarts.
- In this lab, the primary retention policy is explicitly set for Prometheus.

3) I checked that data is still alive since I have dashboards after `compose down` from previous lab
![alt text](image-16.png)
![alt text](image-17.png)