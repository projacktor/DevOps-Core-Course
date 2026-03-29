# Lab 3: Java CI/CD Implementation

## Overview

For the Java Spring Boot application, I implemented a robust CI/CD pipeline using GitHub Actions to automate testing, code quality checks, security scanning, and Docker image publication.

**Key Features:**

- **Framework:** Spring Boot Test (JUnit 5 + Mockito)
- **Linting:** Maven Checkstyle Plugin (Google Style)
- **Security:** Snyk Vulnerability Scanner
- **Coverage:** JaCoCo + Codecov
- **Versioning:** Semantic Versioning for Docker images

## Workflow

The workflow is triggered on pushes to `main` affecting `labs/app_java/`, excluding documentation updates.

### Workflow Steps:

1. **Setup:** JDK 17 with Maven caching.
2. **Linting:** `mvn checkstyle:check` ensures code quality.
3. **Testing:** `mvn verify` runs unit and integration tests.
4. **Coverage:** Reports sent to Codecov via JaCoCo xml report.
5. **Security:** Snyk scans `pom.xml` for vulnerable dependencies.
6. **Docker:** Builds and pushes image to Docker Hub with SemVer tags (e.g., `v1.0.0`, `latest`).

## Best Practices

1. **Dependency Caching:** Maven dependencies are cached to speed up builds (~40% faster).
2. **Path Filtering:** Workflow runs only for changes in the specific app folder.
3. **Security First:** Snyk blocks the build if critical vulnerabilities are found.
4. **Code Quality:** Checkstyle enforces a consistent coding standard before tests run.

## Test Coverage

Coverage is measured using JaCoCo.

- **Current Coverage:** >80% (aiming for critical service logic and controllers).
- **Tool:** Codecov visualizes the coverage reports.

## Badges

Status badges are added to the main README to provide immediate feedback on the project health.
