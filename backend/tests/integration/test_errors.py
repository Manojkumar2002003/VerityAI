"""Integration tests for error handling, unknown routes, and failure modes."""

import pytest
from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.main import create_app

pytestmark = pytest.mark.integration


def test_unknown_route_returns_404(client: TestClient) -> None:
    """Verify that requesting an unregistered path returns structured HTTP 404 with correlation ID."""
    response = client.get("/api/v1/non-existent-route")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "Not Found" in str(data["detail"])
    assert "X-Request-ID" in response.headers


def test_internal_exception_returns_safe_500_without_stack_trace() -> None:
    """Verify that unhandled exceptions produce a sanitized 500 response without traceback leak."""
    test_app = create_app()
    faulty_router = APIRouter()

    @faulty_router.get("/trigger-crash")
    def trigger_crash() -> None:
        raise RuntimeError("Sensitive internal database connection failed at /var/secrets/key.pem")

    test_app.include_router(faulty_router)

    with TestClient(test_app, raise_server_exceptions=False) as faulty_client:
        response = faulty_client.get("/trigger-crash")
        assert response.status_code == 500

        data = response.json()
        assert data["detail"] == "Internal server error"
        assert "X-Request-ID" in response.headers

        # Ensure sensitive words/paths from exception message are NOT in the response
        assert "Sensitive" not in response.text
        assert "key.pem" not in response.text
        assert "Traceback" not in response.text


def test_validation_error_returns_422_with_sanitized_structure() -> None:
    """Verify that request validation errors return structured 422 responses with correlation ID."""
    test_app = create_app()
    val_router = APIRouter()

    @val_router.get("/test-validation")
    def test_val_endpoint(count: int) -> dict[str, int]:
        return {"count": count}

    test_app.include_router(val_router)

    with TestClient(test_app) as val_client:
        response = val_client.get("/test-validation?count=invalid_number")
        assert response.status_code == 422

        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], list)
        assert "count" in data["detail"][0]["field"]
        assert "X-Request-ID" in response.headers
