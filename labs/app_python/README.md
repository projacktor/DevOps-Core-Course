# DevOps Info Service

![Python CI](https://github.com/projacktor/DevOps-Core-Course/workflows/Python%20CI/badge.svg)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-projacktor%2Fpython--info--service-blue)](https://hub.docker.com/r/projacktor/python-info-service)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)

A Python web service that provides comprehensive system and runtime information, designed for DevOps monitoring and introspection.

## Overview

This service exposes endpoints to retrieve detailed information about the application itself, the system it's running on, and runtime metrics. Built with FastAPI, it serves as a foundation for DevOps tooling and monitoring systems.

## Prerequisites

- Python 3.12 or higher
- pip package manager
- Virtual environment (recommended)

## Quick Start

### Development Setup

1. Clone the repository and navigate to the project directory:

```bash
cd labs/app_python
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (for testing, linting)
pip install -r requirements-dev.txt
```

4. Run the application:

```bash
python app.py
```

### Using Docker (Recommended)

```bash
# Pull and run from Docker Hub
docker run -d -p 8080:8080 -e HOST=0.0.0.0 --name python-info-app projacktor/python-info-service:latest

# Access the service
curl http://localhost:8080/
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

## Testing

The project uses pytest for automated testing with comprehensive coverage.

### Running Tests

```bash
# Run all tests
pytest -v

# Run tests with coverage
pytest --cov=. --cov-report=term --cov-report=html

# Run specific test file
pytest tests/test_endpoints.py -v
```

### Test Coverage

Current test coverage includes:

- ✅ All API endpoints (`/`, `/health`)
- ✅ Response structure validation
- ✅ HTTP status codes
- ✅ Error handling scenarios
- ✅ System information gathering

View detailed coverage report: `htmlcov/index.html` (generated after running tests with coverage)

## CI/CD Pipeline

This project includes a fully automated CI/CD pipeline using GitHub Actions:

### Continuous Integration

- ✅ **Automated Testing**: pytest runs on every push/PR
- ✅ **Code Linting**: flake8 ensures code quality
- ✅ **Security Scanning**: Snyk vulnerability scanning
- ✅ **Dependency Caching**: Optimized build times

### Continuous Deployment

- ✅ **Docker Build**: Automatic image building
- ✅ **Multi-tag Strategy**: `latest`, branch name, and date-SHA tags
- ✅ **Docker Hub Push**: Automated publishing to Docker registry
- ✅ **Docker Layer Caching**: Optimized container builds

### Pipeline Status

[![Python CI](https://github.com/projacktor/DevOps-Core-Course/actions/workflows/python-ci.yaml/badge.svg)](https://github.com/projacktor/DevOps-Core-Course/actions/workflows/python-ci.yaml)

The pipeline runs on:

- Push to `main` or `lab*` branches
- Pull requests to any branch
- Git tags matching `v*` pattern

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

## Docker

### Available Images

```bash
# Latest stable version
docker pull projacktor/python-info-service:latest

# Specific versions (CalVer: YYYYMMDD-SHA)
docker pull projacktor/python-info-service:20260210-a1b2c3d

# Branch-specific builds
docker pull projacktor/python-info-service:lab3
```

### Running the Container

```bash
# Run in background with port mapping
docker run -d -p 8080:8080 -e HOST=0.0.0.0 --name python-info-app python-info-service

# Run interactively for debugging
docker run -it -p 8080:8080 -e HOST=0.0.0.0 python-info-service

# Run with custom environment variables
docker run -d -p 3000:3000 -e HOST=0.0.0.0 -e PORT=3000 -e DEBUG=true --name python-info-app python-info-service
```

### Pulling from Docker Hub

```bash
# Pull the latest image
docker pull projacktor/python-info-service:latest

# Pull specific version
docker pull projacktor/python-info-service:v1.0.0

# Run from Docker Hub image
docker run -d -p 8080:8080 -e HOST=0.0.0.0 --name python-info-app projacktor/python-info-service:latest
```

### Container Management

```bash
# Check running containers
docker ps

# View container logs
docker logs python-info-app

# Stop and remove container
docker stop python-info-app && docker rm python-info-app
```

**Important:** Always use `-e HOST=0.0.0.0` when running the container to make the application accessible from outside the container.

## Development

## Development

### Development Workflow

1. **Make changes** to the code
2. **Run tests locally**: `pytest -v`
3. **Check linting**: `flake8 .`
4. **Commit changes** with conventional commits
5. **Push to branch** - CI pipeline automatically runs
6. **Create PR** - Additional CI checks on PR

### Code Quality Tools

The project maintains high code quality using:

- **pytest**: Test framework with fixtures and parametrized tests
- **flake8**: Code linting for PEP 8 compliance
- **Snyk**: Security vulnerability scanning
- **GitHub Actions**: Automated CI/CD pipeline

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and add tests
4. Ensure all tests pass: `pytest -v`
5. Check linting: `flake8 .`
6. Commit with conventional commits: `git commit -m "feat: add new feature"`
7. Push and create a Pull Request

## Security

### Vulnerability Scanning

This project uses Snyk for continuous security monitoring:

- **Automated scanning** on every CI run
- **Severity threshold**: High and Critical vulnerabilities fail the build
- **Dependency monitoring**: All Python packages are scanned
- **Security advisories**: Automated alerts for new vulnerabilities

### Secure Deployment

- Container runs as non-root user
- Minimal base image (python:3.12-slim)
- No sensitive data in environment variables
- Security headers in HTTP responses

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
