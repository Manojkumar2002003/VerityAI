"""Integration tests for the root service identification endpoint."""

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_root_endpoint_returns_200(client: TestClient) -> None:
    """Verify that GET / returns HTTP 200 with service identification."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["app_name"] == "VerityAI API"
    assert data["version"] == "0.1.0"
    assert "running" in data["message"].lower()


def test_root_endpoint_does_not_leak_internals(client: TestClient) -> None:
    """Verify that root endpoint does not expose environment secrets or paths."""
    response = client.get("/")
    data = response.json()
    assert "env" not in data
    assert "path" not in data
    assert "secret" not in data
