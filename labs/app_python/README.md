# DevOps Info Service

A Python web service that provides comprehensive system and runtime information, designed for DevOps monitoring and introspection.

## Overview

This service exposes endpoints to retrieve detailed information about the application itself, the system it's running on, and runtime metrics. Built with FastAPI, it serves as a foundation for DevOps tooling and monitoring systems.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

## Installation

1. Clone the repository and navigate to the project directory:

```bash
cd app_python
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Default Configuration

```bash
python app.py
```

This starts the service on `127.0.0.1:8080`

### Custom Configuration

```bash
# Custom port
PORT=8080 python app.py

# Custom host and port
HOST=0.0.0.0 PORT=3000 python app.py

# Enable debug mode
DEBUG=true python app.py
```

### Using uvicorn directly

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

## API Endpoints

### GET /

**Description:** Returns comprehensive service and system information

**Response (example):**

```json
{
  "service": {
    "name": "devops-info-service",
    "version": "1.0.0",
    "description": "DevOps course info service",
    "framework": "FastAPI"
  },
  "system": {
    "hostname": "my-laptop",
    "platform": "Linux",
    "platform_version": "Ubuntu 24.04",
    "architecture": "x86_64",
    "cpu_count": 8,
    "python_version": "3.13.1"
  },
  "runtime": {
    "uptime_seconds": 3600,
    "uptime_human": "1 hour, 0 minutes",
    "current_time": "2026-01-28T14:30:00.000Z",
    "timezone": "UTC"
  },
  "request": {
    "client_ip": "127.0.0.1",
    "user_agent": "curl/7.81.0",
    "method": "GET",
    "path": "/"
  },
  "endpoints": [
    { "path": "/", "method": "GET", "description": "Service information" },
    { "path": "/health", "method": "GET", "description": "Health check" }
  ]
}
```

### GET /health

**Description:** Health check endpoint for monitoring and load balancers

**Response (example):**

```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T14:30:00.000Z",
  "uptime_seconds": 3600
}
```

## Configuration

The application supports configuration via environment variables:

| Variable | Default     | Description                       |
| -------- | ----------- | --------------------------------- |
| `HOST`   | `127.0.0.1` | Server host address               |
| `PORT`   | `8080`      | Server port number                |
| `DEBUG`  | `false`     | Enable debug mode and auto-reload |

## Testing the API

### Using curl

```bash
# Main endpoint
curl http://localhost:8080/

# Health check
curl http://localhost:8080/health

# Pretty-printed JSON
curl http://localhost:8080/ | jq .
```

### Using HTTPie

```bash
# Main endpoint
http localhost:8080

# Health check
http localhost:8080/health
```

## Features

- **System Information**: Hardware, OS, and Python runtime details
- **Request Tracking**: Client IP, user agent, and request metadata
- **Uptime Monitoring**: Service runtime tracking in seconds and human-readable format
- **Health Checks**: Simple endpoint for monitoring systems
- **Structured Logging**: Comprehensive request and error logging
- **Error Handling**: Proper HTTP error responses with JSON format
- **Configuration**: Environment variable support for deployment flexibility

## Architecture

The application follows a simple but robust architecture:

- **FastAPI Framework**: Modern, async-capable web framework
- **Structured Responses**: Consistent JSON format across endpoints
- **Exception Handling**: Global exception handlers for proper error responses
- **Logging**: Structured logging for observability
- **Configuration**: Environment-based configuration for different deployment scenarios

## Development

### Code Style

The project follows PEP 8 Python style guidelines and includes:

- Type hints where appropriate
- Docstrings for functions and modules
- Proper import organization
- Consistent naming conventions

### Error Handling

The application includes comprehensive error handling:

- HTTP 404 responses for unknown endpoints
- HTTP 500 responses for server errors
- Structured JSON error responses
- Proper logging of errors and warnings