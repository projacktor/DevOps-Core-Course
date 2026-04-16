"""
DevOps Info Service
Main application module
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

import logging
import json
import time
import platform
import socket
from datetime import datetime, timezone
import os

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    cache_items.set(0)
    db_pool_size.set(0)
    yield
    # shutdown (optional)

app = FastAPI(lifespan=lifespan)

# Structured JSON logging


class JSONFormatter(logging.Formatter):
    def format(self, record):
        record_time = datetime.fromtimestamp(record.created, timezone.utc).isoformat()
        obj = {
            "timestamp": record_time,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # include extra fields attached to the record
        for k, v in record.__dict__.items():
            if k in (
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "pathname",
                "filename",
                "module",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
            ):
                continue
            try:
                json.dumps({k: v})
                obj[k] = v
            except Exception:
                obj[k] = str(v)
        if record.exc_info:
            obj["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(obj)


handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.handlers = [handler]

logger = logging.getLogger(__name__)

# Config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# System Information
def get_system_info():
    """Collect system information."""
    with system_info_duration.time():
        return {
            "hostname": socket.gethostname(),
            "platform_name": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "cpu_count": os.cpu_count(),
        }


# Uptime Tracking
START_TIME = datetime.now()


def get_uptime():
    """Calculate service uptime."""
    delta = datetime.now() - START_TIME
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return {"seconds": seconds, "human": f"{hours} hours, {minutes} minutes"}


def count_visit(client_ip):
    visit = datetime.now()
    with open("data/visits.json", "r") as file:
        data = json.load(file)
    data["visits"].append({"datetime": visit, "IP": client_ip})
    data["total"] += 1
    with open("data/visits.json", "w") as file:
        json.dump(data, file)


# Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # don't log a traceback for expected 404s
        logger.warning(
            "HTTP 404 on path=%s client=%s",
            request.url.path,
            request.client.host if request.client else "unknown",
        )
        return JSONResponse(
            status_code=404,
            content={
                "error": "not_found",
                "message": "Endpoint does not exist",
            },
        )
    logger.error("HTTP %s on path=%s", exc.status_code, request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "http_error", "message": exc.detail},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception while processing request",
        extra={"path": request.url.path if request.url else None},
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred.",
        },
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    client_ip = request.client.host if request.client else None

    # low-cardinality endpoint label
    route = request.scope.get("route")
    endpoint = getattr(route, "path", None) or "unmatched"

    http_requests_in_progress.inc()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        logger.exception(
            "request_error",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_ip": client_ip,
            },
        )
        raise
    finally:
        # Business metric: endpoint usage
        endpoint_calls.labels(endpoint=endpoint).inc()

        duration = time.time() - start
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)

        http_requests_total.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(status_code)
        ).inc()

        http_requests_in_progress.dec()

    duration_ms = int((time.time() - start) * 1000)
    logger.info(
        "request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "client_ip": client_ip,
            "user_agent": request.headers.get("user-agent"),
        },
    )
    return response


# Endpoints
@app.get("/")
async def root(request: Request):
    """Main endpoint - service and system information."""
    client_ip = request.client.host if request.client else "unknown"
    count_visit(client_ip)
    logger.info(
        "endpoint",
        extra={
            "endpoint": "root",
            "method": request.method,
            "path": request.url.path,
            "client": client_ip,
            "user_agent": request.headers.get("user-agent"),
            "uptime_seconds": get_uptime()["seconds"],
        },
    )
    info = get_system_info()
    return {
        "service": {
            "name": "devops-info-service",
            "version": "1.0.0",
            "description": "DevOps course info service",
            "framework": "FastAPI",
        },
        "system": {
            "hostname": info["hostname"],
            "platform": info["platform_name"],
            "platform_version": info["platform_version"],
            "architecture": info["architecture"],
            "cpu_count": info["cpu_count"],
            "python_version": info["python_version"],
        },
        "runtime": {
            "uptime_seconds": get_uptime()["seconds"],
            "uptime_human": get_uptime()["human"],
            "current_time": datetime.now().isoformat(),
            "timezone": datetime.now().astimezone().tzname(),
        },
        "request": {
            "client_ip": client_ip,
            "user_agent": request.headers.get("user-agent"),
            "method": request.method,
            "path": request.url.path,
        },
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Service information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
        ],
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.info(
        "endpoint",
        extra={
            "endpoint": "health",
            "status": "healthy",
            "uptime_seconds": get_uptime()["seconds"],
            "timestamp": datetime.now().isoformat(),
        },
    )
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": get_uptime()["seconds"],
    }


@app.get("/favicon.ico")
async def favicon():
    """Favicon handler to avoid repeated 404s from browsers"""
    return Response(status_code=204)


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/visit")
async def visit():
    with open("data/visits.json", "r") as f:
        visits = json.load(f)
        return {"total": visits["total"], "all": visits["visits"]}


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

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )
