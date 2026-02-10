"""
Tests for FastAPI endpoints
"""

from fastapi.testclient import TestClient
from app import app
from datetime import datetime

# Create a test client
client = TestClient(app)


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_returns_200(self):
        """Test that root endpoint returns 200 status code"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_json(self):
        """Test that root endpoint returns JSON"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"

    def test_root_response_structure(self):
        """Test that root endpoint returns required structure"""
        response = client.get("/")
        data = response.json()

        # Check main sections
        assert "service" in data
        assert "system" in data
        assert "runtime" in data
        assert "request" in data
        assert "endpoints" in data

    def test_root_service_info(self):
        """Test service information in response"""
        response = client.get("/")
        service = response.json()["service"]

        assert service["name"] == "devops-info-service"
        assert service["version"] == "1.0.0"
        assert service["framework"] == "FastAPI"

    def test_root_system_info(self):
        """Test system information is present"""
        response = client.get("/")
        system = response.json()["system"]

        assert "hostname" in system
        assert "platform" in system
        assert "architecture" in system
        assert "cpu_count" in system
        assert "python_version" in system

    def test_root_runtime_info(self):
        """Test runtime information"""
        response = client.get("/")
        runtime = response.json()["runtime"]

        assert "uptime_seconds" in runtime
        assert "uptime_human" in runtime
        assert "current_time" in runtime
        assert isinstance(runtime["uptime_seconds"], int)
        assert runtime["uptime_seconds"] >= 0

    def test_root_request_info(self):
        """Test request information in response"""
        response = client.get("/")
        request_info = response.json()["request"]

        assert "client_ip" in request_info
        assert "method" in request_info
        assert request_info["method"] == "GET"
        assert "path" in request_info
        assert request_info["path"] == "/"

    def test_root_endpoints_list(self):
        """Test that endpoints list is present"""
        response = client.get("/")
        endpoints = response.json()["endpoints"]

        assert isinstance(endpoints, list)
        assert len(endpoints) > 0

        # Check structure of first endpoint
        endpoint = endpoints[0]
        assert "path" in endpoint
        assert "method" in endpoint
        assert "description" in endpoint


class TestHealthEndpoint:
    """Tests for GET /health endpoint"""

    def test_health_returns_200(self):
        """Test that health endpoint returns 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self):
        """Test that health endpoint returns JSON"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_response_structure(self):
        """Test health response structure"""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "timestamp" in data
        assert "uptime_seconds" in data

    def test_health_status_healthy(self):
        """Test that health status is 'healthy'"""
        response = client.get("/health")
        assert response.json()["status"] == "healthy"

    def test_health_uptime_is_integer(self):
        """Test that uptime_seconds is an integer"""
        response = client.get("/health")
        uptime = response.json()["uptime_seconds"]

        assert isinstance(uptime, int)
        assert uptime >= 0

    def test_health_timestamp_format(self):
        """Test that timestamp is in ISO format"""
        response = client.get("/health")
        timestamp = response.json()["timestamp"]

        # Try to parse ISO format
        try:
            datetime.fromisoformat(timestamp)
            valid = True
        except ValueError:
            valid = False

        assert valid, f"Timestamp '{timestamp}' is not in ISO format"


class TestFaviconEndpoint:
    """Tests for GET /favicon.ico endpoint"""

    def test_favicon_returns_204(self):
        """Test that favicon endpoint returns 204 (No Content)"""
        response = client.get("/favicon.ico")
        assert response.status_code == 204

    def test_favicon_no_content(self):
        """Test that favicon endpoint returns no content"""
        response = client.get("/favicon.ico")
        assert len(response.content) == 0


class TestErrorHandling:
    """Tests for error handling"""

    def test_nonexistent_endpoint_returns_404(self):
        """Test that non-existent endpoint returns 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_404_response_structure(self):
        """Test 404 error response structure"""
        response = client.get("/nonexistent")
        data = response.json()

        assert "error" in data
        assert data["error"] == "not_found"
        assert "message" in data

    def test_unsupported_method_returns_405(self):
        """Test that unsupported HTTP method returns 405"""
        response = client.post("/")
        assert response.status_code == 405


class TestEndpointIntegration:
    """Integration tests for multiple endpoints"""

    def test_multiple_calls_increase_uptime(self):
        """Test that uptime increases with repeated calls"""
        from time import sleep

        response1 = client.get("/health")
        uptime1 = response1.json()["uptime_seconds"]

        sleep(1)  # Wait 1 second

        response2 = client.get("/health")
        uptime2 = response2.json()["uptime_seconds"]

        # Second uptime should be greater or equal
        assert uptime2 >= uptime1

    def test_endpoints_consistency(self):
        """Test that endpoints return consistent uptime"""
        response_root = client.get("/")
        response_health = client.get("/health")

        uptime_root = response_root.json()["runtime"]["uptime_seconds"]
        uptime_health = response_health.json()["uptime_seconds"]

        # Should be approximately equal (within 1 second)
        assert abs(uptime_root - uptime_health) <= 1
