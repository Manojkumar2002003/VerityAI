"""Integration tests for HTTP request logging middleware and correlation ID header handling."""

import logging
import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_response_includes_request_id_header(client: TestClient) -> None:
    """Verify that all responses include an X-Request-ID header."""
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) >= 16


def test_client_supplied_request_id_preserved_when_safe(client: TestClient) -> None:
    """Verify that a safe, valid client-supplied X-Request-ID is preserved in the response."""
    safe_id = "client-trace-id-12345"
    response = client.get("/", headers={"X-Request-ID": safe_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == safe_id


def test_client_supplied_unsafe_request_id_replaced(client: TestClient) -> None:
    """Verify that an unsafe client-supplied request ID with newlines or special chars is sanitized."""
    unsafe_id = "bad\nid\rwith\ninjection"
    response = client.get("/", headers={"X-Request-ID": unsafe_id})
    assert response.status_code == 200
    returned_id = response.headers.get("X-Request-ID")
    assert returned_id is not None
    assert returned_id != unsafe_id
    assert "\n" not in returned_id
    assert "\r" not in returned_id


def test_request_logging_records_lifecycle(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    """Verify that requests produce structured logs with method, path, status code, and duration."""
    with caplog.at_level(logging.INFO, logger="verityai.http"):
        response = client.get("/")
        assert response.status_code == 200

    log_messages = [record.message for record in caplog.records if record.name == "verityai.http"]
    assert len(log_messages) >= 1
    msg = log_messages[-1]
    assert "GET" in msg
    assert "/" in msg
    assert "200" in msg
    assert "ms" in msg


def test_sensitive_data_not_logged(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    """Verify that query parameters, authorization headers, and bodies are not printed in request logs."""
    secret_token = "Bearer secret_jwt_token_12345"
    with caplog.at_level(logging.INFO, logger="verityai.http"):
        response = client.get(
            "/?api_key=secret_key_12345",
            headers={"Authorization": secret_token},
        )
        assert response.status_code == 200

    log_messages = " ".join([record.message for record in caplog.records if record.name == "verityai.http"])
    assert "secret_jwt_token_12345" not in log_messages
    assert "secret_key_12345" not in log_messages
