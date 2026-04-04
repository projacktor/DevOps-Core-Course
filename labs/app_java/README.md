# DevOps Info Service (Java)

A Java Spring Boot web service that provides comprehensive system and runtime information, designed for DevOps monitoring and introspection.

## Overview

This service exposes REST endpoints to retrieve detailed information about the application itself, the system it's running on, and runtime metrics. Built with Spring Boot, it serves as a foundation for DevOps tooling and monitoring systems.

## Prerequisites

- Java 17 or higher
- Maven 3.6+ or included Maven wrapper
- Internet connection (for dependency download)

## Installation

1. Clone the repository and navigate to the project directory:

```bash
cd app_java
```

2. Build the project using Maven:

```bash
# Using system Maven
mvn clean package

# Or using Maven wrapper (if available)
./mvnw clean package
```

## Running the Application

### Development Mode

```bash
# Using Maven
mvn spring-boot:run

# Or using Maven wrapper
./mvnw spring-boot:run
```

### Production Mode (JAR)

```bash
# Build the JAR
mvn clean package

# Run the JAR
java -jar target/info-service-1.0.0.jar
```

### Custom Configuration

```bash
# Custom port
PORT=9000 java -jar target/info-service-1.0.0.jar

# Custom host and port
HOST=0.0.0.0 PORT=3000 java -jar target/info-service-1.0.0.jar

# Using system properties
java -Dserver.port=9000 -Dserver.address=0.0.0.0 -jar target/info-service-1.0.0.jar
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
    "framework": "Spring Boot"
  },
  "system": {
    "hostname": "my-laptop",
    "platform": "Linux",
    "platformVersion": "6.2.0-39-generic",
    "architecture": "amd64",
    "cpuCount": 8,
    "javaVersion": "17.0.8"
  },
  "runtime": {
    "uptimeSeconds": 3600,
    "uptimeHuman": "1 hours, 0 minutes",
    "currentTime": "2026-01-28T14:30:00.000Z",
    "timezone": "Europe/Moscow"
  },
  "request": {
    "clientIp": "127.0.0.1",
    "userAgent": "curl/7.81.0",
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
  "uptimeSeconds": 3600
}
```

## Configuration

The application supports configuration via environment variables and system properties:

| Environment Variable | System Property  | Default     | Description         |
| -------------------- | ---------------- | ----------- | ------------------- |
| `HOST`               | `server.address` | `127.0.0.1` | Server host address |
| `PORT`               | `server.port`    | `8080`      | Server port number  |

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

## Build Information

### JAR Size Comparison

After building the project:

```bash
ls -lh target/info-service-1.0.0.jar
```

Typical JAR sizes:

- **Fat JAR (with dependencies)**: ~20-25MB
- **Thin JAR (without dependencies)**: ~50KB

### Build Performance

```bash
# Clean build time
time mvn clean package

# Typical build times:
# - Clean build: 10-30 seconds (depending on network for dependencies)
# - Incremental build: 2-5 seconds
```

## Features

- **System Information**: Hardware, OS, and Java runtime details
- **Request Tracking**: Client IP, user agent, and request metadata
- **Uptime Monitoring**: Service runtime tracking in seconds and human-readable format
- **Health Checks**: Simple endpoint for monitoring systems
- **Structured Logging**: Comprehensive request and error logging
- **Configuration**: Environment variable and system property support
- **Production Ready**: Executable JAR with embedded Tomcat server
- **Cross-Platform**: Runs on any system with Java 17+

## Architecture

The application follows Spring Boot best practices:

- **Layered Architecture**: Controller → Service → Model separation
- **Dependency Injection**: Spring IoC container manages components
- **Auto Configuration**: Spring Boot's auto-configuration for web server
- **JSON Serialization**: Jackson for consistent JSON responses
- **Embedded Server**: Tomcat embedded for standalone deployment
- **Actuator Integration**: Health checks and metrics endpoints

## Development

### Project Structure

```
src/
├── main/
│   ├── java/com/devops/infoservice/
│   │   ├── InfoServiceApplication.java      # Main application class
│   │   ├── controller/
│   │   │   └── InfoController.java          # REST endpoints
│   │   ├── service/
│   │   │   └── InfoService.java             # Business logic
│   │   └── model/                           # Data models
│   │       ├── ServiceResponse.java
│   │       ├── HealthResponse.java
│   │       └── [other models...]
│   └── resources/
│       └── application.properties           # Configuration
├── pom.xml                                  # Maven dependencies
└── target/                                  # Build output
```

### Code Quality

The project follows Java best practices:

- **Package Structure**: Clear separation of concerns
- **Dependency Injection**: Spring annotations for component management
- **Exception Handling**: Proper error handling with appropriate HTTP status codes
- **Logging**: SLF4J with structured logging format
- **Documentation**: Comprehensive JavaDoc comments
- **Type Safety**: Strong typing throughout the application

## Performance

### Memory Usage

- **Heap**: ~50-100MB typical usage
- **Startup Time**: ~2-5 seconds
- **Response Time**: <50ms typical

### Optimization Features

- **Lazy Initialization**: Spring Boot optimizations
- **Connection Pooling**: Embedded Tomcat optimizations
- **JSON Caching**: Jackson object mapper reuse
- **Efficient Collections**: Minimal object allocation
