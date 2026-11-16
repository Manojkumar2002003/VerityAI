"""Integration tests for liveness, readiness, and model-info endpoints."""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

pytestmark = pytest.mark.integration


def test_health_liveness_returns_200_and_ok(client: TestClient) -> None:
    """Verify that GET /api/v1/health returns HTTP 200 with ok status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["app_name"] == "VerityAI API"
    assert data["version"] == "0.1.0"
    assert "X-Request-ID" in response.headers

    # Ensure liveness does not report unverified dependencies
    assert "checks" not in data


def test_readiness_returns_200_when_database_is_healthy(client: TestClient) -> None:
    """Verify that GET /api/v1/health/ready returns HTTP 200 and ready status when DB check succeeds."""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ready"
    assert data["checks"]["database"] == "ok"
    assert "X-Request-ID" in response.headers

    # Ensure connection string and absolute file paths are not exposed
    assert "sqlite" not in response.text.lower()
    assert "verityai.db" not in response.text.lower()


def test_readiness_returns_503_when_database_check_fails(client: TestClient) -> None:
    """Verify that GET /api/v1/health/ready returns HTTP 503 when DB connectivity raises an error."""
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = OperationalError("connection refused", {}, None)

    with patch("app.api.v1.router.get_engine", return_value=mock_engine):
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 503

        data = response.json()
        assert data["status"] == "not_ready"
        assert data["checks"]["database"] == "unavailable"
        assert "X-Request-ID" in response.headers

        # Ensure no raw exception details or paths leaked
        assert "traceback" not in response.text.lower()
        assert "connection refused" not in response.text.lower()


def test_model_info_reports_unconfigured_state(client: TestClient) -> None:
    """Verify that GET /api/v1/model-info accurately reports that the model is unconfigured."""
    response = client.get("/api/v1/model-info")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "not_configured"
    assert data["supported_language"] == "en"
    assert data["detection_available"] is False
    assert "deberta" in data["model_candidate"].lower()
    assert "X-Request-ID" in response.headers
