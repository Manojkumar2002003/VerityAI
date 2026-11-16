"""Unit tests for centralized logging configuration and correlation ID sanitization."""

import logging
import pytest

from app.core.logging import (
    CorrelationIdFilter,
    generate_request_id,
    request_id_ctx_var,
    sanitize_request_id,
    setup_logging,
)

pytestmark = pytest.mark.unit


def test_request_id_generation_and_sanitization() -> None:
    """Verify that request ID generator produces valid hex strings and sanitizes inputs."""
    gen_id = generate_request_id()
    assert isinstance(gen_id, str)
    assert len(gen_id) == 32

    # Safe client-supplied IDs are preserved
    assert sanitize_request_id("valid-request-123_abc") == "valid-request-123_abc"

    # None or empty strings result in a generated ID
    empty_sanitized = sanitize_request_id(None)
    assert len(empty_sanitized) == 32

    # Unsafe IDs with newlines, spaces, or excessive length are replaced with a safe new ID
    with_newline = sanitize_request_id("id_with\nnewline")
    assert with_newline != "id_with\nnewline"
    assert len(with_newline) == 32

    with_injection = sanitize_request_id("<script>alert(1)</script>")
    assert "<" not in with_injection

    too_long = sanitize_request_id("a" * 100)
    assert len(too_long) == 32


def test_correlation_id_filter_injects_request_id() -> None:
    """Verify that CorrelationIdFilter injects request_id from contextvar into LogRecord."""
    flt = CorrelationIdFilter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None,
    )

    # When no request_id in context, defaults to '-'
    flt.filter(record)
    assert getattr(record, "request_id", None) == "-"

    # When request_id set in context, record receives the value
    token = request_id_ctx_var.set("test-corr-id-999")
    try:
        flt.filter(record)
        assert getattr(record, "request_id", None) == "test-corr-id-999"
    finally:
        request_id_ctx_var.reset(token)


def test_setup_logging_is_idempotent() -> None:
    """Verify that calling setup_logging repeatedly does not accumulate duplicate handlers."""
    setup_logging("DEBUG")
    setup_logging("INFO")
    setup_logging("WARNING")

    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 1
    assert root_logger.level == logging.WARNING
