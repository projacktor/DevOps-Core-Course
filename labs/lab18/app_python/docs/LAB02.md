# Lab 2 — Docker Containerization Documentation

## 1. Docker Best Practices Applied

### 1.1 Non-root User Implementation
**Practice:** Creating and running as a non-root user (`app`)

```dockerfile
RUN groupadd -r app && useradd -r -g app app
USER app
```

**Why:** Running containers as root poses significant security risks. If an attacker gains access to the container, they have root privileges. By using a non-root user, we limit potential damage through the principle of least privilege. This practice is essential for production deployments and is required by many security policies.

### 1.2 Proper Layer Ordering for Caching
**Practice:** Dependencies installed before application code

```dockerfile
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

**Why:** Docker builds images in layers and caches each layer. Since Python dependencies change less frequently than application code, copying `requirements.txt` first allows Docker to reuse the dependency installation layer when only code changes. This dramatically speeds up build times during development.

### 1.3 Minimal Base Image Selection
**Practice:** I used `python:3.13-slim` instead of full Python image

```dockerfile
FROM python:3.13-slim
```

**Why:** Since the slim variant excludes unnecessary packages, reducing image size from ~900MB to ~150MB base. This means faster pulls, less storage usage, smaller attack surface, and reduced bandwidth costs. For production apps, smaller images are more secure and deploy faster.

### 1.4 [.dockerignore](../.dockerignore) Implementation
**Practice:** Excluding unnecessary files from build context

```.dockerignore
# VCS
.git

# Python env
.venv
venv
__pycache__

# Documentation
docs
*.md

# Tests unneeded in production
tests
```

**Why:** Prevents sending large or sensitive files to Docker daemon, reducing build context size and improving build speed. Also prevents accidentally including development files, credentials, or large assets in the final image.

### 1.5 No-cache pip Installation
**Practice:** Using `--no-cache-dir` flag for pip

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

**Why:** Prevents pip from storing cache in the image layer, reducing final image size by 10-50MB. The cache serves no purpose in a container since each build starts fresh, so removing it is pure optimization.

### 1.6 Proper File Ownership
**Practice:** Changing ownership before switching to non-root user

```dockerfile
COPY . .
RUN chown -R app:app /app
USER app
```

**Why:** Files copied as root remain owned by root. The non-root user needs to be able to read and potentially modify these files. Proper ownership ensures the application can access its own files while maintaining security boundaries.

## 2. Image Information & Decisions

### 2.1 Base Image Choice: python:3.13-slim
**Chosen:** `python:3.13-slim`
**Alternatives considered:** `python:3.13-alpine`, `python:3.13`

**Justification:**
- **Size efficiency:** 150MB vs 900MB for full Python image
- **Compatibility:** Debian-based, ensuring compatibility with most Python packages
- **Security updates:** Regular security updates from Debian team
- **Community support:** Well-maintained, widely used base image

**Why not Alpine?** While Alpine is smaller (~50MB), it uses musl libc instead of glibc, which can cause compatibility issues with some Python packages that have C extensions.

### 2.2 Final Image Size Analysis
```
REPOSITORY                SIZE
python-info-service       284MB
```

**Size breakdown:**
- Base python:3.13-slim: ~150MB
- Python dependencies (FastAPI, uvicorn, etc.): ~84.5MB  
- Application code: ~33KB
- Metadata and layers: ~49MB

**Assessment:** The size is reasonable for a FastAPI application. The majority comes from the base image and dependencies, which are necessary. The application code itself is minimal at 33KB.

### 2.3 Layer Structure Analysis

Our Dockerfile creates optimized layers:

1. **User creation** (41KB) - Only done once, cached well
2. **Working directory** (8.19KB) - Metadata only
3. **Requirements copy** (12.3KB) - Triggers rebuild when dependencies change
4. **Dependencies installation** (84.5MB) - Largest layer, well cached
5. **Application copy** (28.7KB) - Changes most frequently, minimal impact
6. **Ownership change** (32.8KB) - Necessary for security

**Optimization choices:**
- Dependencies before code for better caching
- Single RUN command for user creation (fewer layers)
- Minimal COPY operations to reduce layer count

### 2.4 Security Considerations
- **Non-root execution:** Runs as user `app` (UID > 999)
- **Minimal attack surface:** Slim base image with fewer packages
- **No secrets in layers:** .dockerignore prevents accidental inclusion
- **Explicit port exposure:** EXPOSE 8080 documents intended usage

## 3. Build & Run Process

### 3.1 Build Process Output
```bash
$ docker build -t python-info-service .
[+] Building 1.2s (12/12) FINISHED         docker:default
 => [internal] load build definition from Dockerfile  0.0s
 => => transferring dockerfile: 280B                 0.0s
 => [internal] load metadata for docker.io/library/  1.1s
 => [internal] load .dockerignore                    0.0s
 => => transferring context: 153B                    0.0s
 => [1/7] FROM docker.io/library/python:3.13-slim@sha256:... 0.0s
 => => resolve docker.io/library/python:3.13-slim@sha256:... 0.0s
 => [internal] load build context                    0.0s
 => => transferring context: 155B                    0.0s
 => CACHED [2/7] RUN groupadd -r app && useradd -r -g app app 0.0s
 => CACHED [3/7] WORKDIR /app                        0.0s
 => CACHED [4/7] COPY requirements.txt ./            0.0s
 => CACHED [5/7] RUN pip install --no-cache-dir -r requirements.txt 0.0s
 => CACHED [6/7] COPY . .                            0.0s
 => CACHED [7/7] RUN chown -R app:app /app           0.0s
 => exporting to image                               0.0s
 => => exporting layers                              0.0s
 => => exporting manifest sha256:49d8b52584570df711  0.0s
 => => exporting config sha256:37d1615c185c515d918d  0.0s
 => => exporting attestation manifest sha256:177a7a  0.0s
 => => exporting manifest list sha256:8e664a0fce812  0.0s
 => => naming to docker.io/library/python-info-service  0.0s
 => => unpacking to docker.io/library/python-info-service  0.0s
```

**Analysis:** Build completed in 1.2s with all layers cached (CACHED status), demonstrating excellent layer caching strategy. Fast builds are crucial for development productivity.

### 3.2 Container Startup Output
```bash
$ docker run -d -p 8080:8080 -e HOST=0.0.0.0 --name python-info-app python-info-service
880fba723e25e2bcb95520ce954b6402fff8f6543ccd42a64082ea557f38191a

$ docker logs python-info-app
2026-02-03 21:10:40,429 - __main__ - INFO - Application starting...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

**Analysis:** Container started successfully with PID 1, listening on all interfaces (0.0.0.0:8080). The logs show clean startup with proper logging configuration.

### 3.3 Application Testing Output
```bash
$ curl http://localhost:8080/
{"service":{"name":"devops-info-service","version":"1.0.0","description":"DevOps course info service","framework":"FastAPI"},"system":{"hostname":"880fba723e25","platform":"Linux","platform_version":"#37~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 20 10:25:38 UTC 2","architecture":"x86_64","cpu_count":16,"python_version":"3.13.11"},"runtime":{"uptime_seconds":23,"uptime_human":"0 hours, 0 minutes","current_time":"2026-02-03T21:11:03.733544","timezone":"UTC"},"request":{"client_ip":"172.17.0.1","user_agent":"curl/8.5.0","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}

$ curl http://localhost:8080/health
{"status":"healthy","timestamp":"2026-02-03T21:11:10.855826","uptime_seconds":30}
```

**Analysis:** Both endpoints working correctly, showing system information including containerized environment details. The hostname shows Docker container ID, confirming proper containerization.

### 3.4 Docker Hub Publication
**Repository URL:** [https://hub.docker.com/r/projacktor/python-info-service](https://hub.docker.com/r/projacktor/python-info-service)

```bash
$ docker tag python-info-service projacktor/python-info-service:latest
$ docker tag python-info-service projacktor/python-info-service:v1.0.0
$ docker push projacktor/python-info-service:v1.0.0
...
$ docker push projacktor/python-info-service:latest
...
```

**Tagging strategy:**
- `latest` - Always points to most recent stable build
- `v1.0.0` - Semantic versioning for specific releases

## 4. Technical analysis

### 4.1 Why this Dockerfile works

**Layer Optimization:** The instruction order maximizes Docker's layer caching. Dependencies are installed before copying application code, so code changes don't invalidate the expensive dependency installation layer.

**Security Architecture:** The non-root user prevents privilege escalation attacks. Even if the application is compromised, the attacker cannot gain root access to the host system.

**Resource Efficiency:** The slim base image provides Python runtime without unnecessary development tools, reducing size and attack surface while maintaining compatibility.

### 4.2 Impact of Layer Order Changes

If we moved `COPY . .` before `RUN pip install`, every code change would invalidate the pip cache, causing:
- **Slow builds:** Dependencies would reinstall on every change
- **Higher bandwidth usage:** Larger layers transferred more frequently  
- **Poor developer experience:** 2-3 minute builds instead of 10-second builds

### 4.3 Security Analysis

**Implemented measures:**
- **Principle of least privilege:** Non-root execution
- **Minimal attack surface:** Slim base image
- **No sensitive data:** .dockerignore prevents credential leaks
- **Explicit networking:** EXPOSE documents intended usage

**Additional production considerations:**
- Could use distroless images for even smaller attack surface
- Could implement USER with explicit UID for Kubernetes compatibility
- Could add health checks for better monitoring integration

### 4.4 .dockerignore Benefits

**Build performance:** Excluding `.git` (potentially MB of history), `__pycache__` (compiled Python bytecode), and development files reduces context size from ~50MB to ~15MB.

**Security:** Prevents accidentally including:
- Environment files with credentials
- Development databases or logs
- SSH keys or other sensitive development tools

**Reproducibility:** Ensures only necessary files are included, making builds more predictable across different development environments.

## 5. Challenges & Solutions

### 5.1 Application Not Accessible from Host

**Problem:** Container started successfully but `curl localhost:8080` failed with connection refused.

**Root Cause Analysis:** 
```bash
$ docker logs python-info-app
INFO: Uvicorn running on http://127.0.0.1:8080
```
The application was binding to `127.0.0.1` (localhost only), which is not accessible from outside the container.

**Solution:** Added environment variable override:
```bash
docker run -e HOST=0.0.0.0 -p 8080:8080 python-info-service
```

**Learning:** Container networking requires binding to `0.0.0.0` to accept connections from the host. This is a common containerization gotcha.

### 5.2 Understanding Docker Tag Syntax

**Problem:** Initial attempt `docker run .` failed with "invalid reference format".

**Root Cause:** The `.` in `docker run .` refers to a build context, not a runnable image. Confused Docker build syntax with run syntax.

**Solution:** 
1. Build with explicit tag: `docker build -t python-info-service .`
2. Run with image name: `docker run python-info-service`

**Learning:** Docker commands have different context meanings - `.` for build context vs image names for run context.

### 5.3 Layer Caching Understanding

**Problem:** Initially wrote Dockerfile with application code before dependencies, causing slow rebuilds.

**Investigation Process:**
1. Noticed builds taking 2+ minutes on small code changes
2. Researched Docker layer caching mechanism
3. Analyzed layer sizes with `docker history`
4. Reorganized Dockerfile for optimal caching

**Solution:** Reordered instructions to copy dependencies first, then application code.

**Learning:** Understanding Docker's layering system is crucial for development efficiency. The most expensive operations should be cached at stable layers.

### 5.4 Security and Functionality Balance

**Problem:** Creating non-root user while maintaining application functionality.

**Research Process:**
1. Understood why root containers are dangerous
2. Learned proper user creation syntax for Debian base images
3. Discovered file ownership requirements
4. Implemented proper permission management

**Solution:** Created dedicated `app` user and changed file ownership before switching users.

**Learning:** Container security requires careful consideration of file permissions and user contexts, but the patterns are well-established and repeatable.

## Conclusion

This Docker implementation successfully containerizes the Python Info Service following production-ready practices. The optimized layer structure, security measures, and comprehensive documentation provide a solid foundation for deployment in development, staging, and production environments.