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

app = FastAPI()

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
    try:
        response = await call_next(request)
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
    duration_ms = int((time.time() - start) * 1000)
    logger.info(
        "request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
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
    logger.info(
        "endpoint",
        extra={
            "endpoint": "root",
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else "unknown",
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
            "client_ip": request.client.host,
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


if __name__ == "__main__":
    logger.info("Application starting...")

    uvicorn.run("app:app", host=HOST, port=PORT, reload=DEBUG)
