"""Centralized logging configuration with request correlation ID tracking."""

import logging
import re
import sys
import uuid
from contextvars import ContextVar
from typing import Optional

from app.core.config import get_settings

# Context variable holding the correlation ID for the active request context
request_id_ctx_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)

# Regular expression to validate incoming client-supplied request correlation IDs
_SAFE_REQUEST_ID_REGEX = re.compile(r"^[a-zA-Z0-9_\-]{1,64}$")


def generate_request_id() -> str:
    """Generate a clean UUID4 hex string for request correlation."""
    return uuid.uuid4().hex


def sanitize_request_id(incoming_id: Optional[str]) -> str:
    """Validate and sanitize an incoming request ID or generate a new safe one."""
    if incoming_id and _SAFE_REQUEST_ID_REGEX.match(incoming_id.strip()):
        return incoming_id.strip()
    return generate_request_id()


def get_current_request_id() -> Optional[str]:
    """Retrieve the current request correlation ID from context."""
    return request_id_ctx_var.get()


class CorrelationIdFilter(logging.Filter):
    """Logging filter that injects the active request correlation ID into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx_var.get() or "-"
        return True


def setup_logging(log_level: Optional[str] = None) -> None:
    """Configure centralized application logging with correlation ID formatting.

    Idempotent: removes existing handlers before attaching the formatted handler to
    prevent duplicate log entries during test execution or multiple app initializations.
    """
    settings = get_settings()
    level_name = (log_level or settings.log_level).upper()
    numeric_level = getattr(logging, level_name, logging.INFO)

    log_format = "%(asctime)s [%(levelname)s] [%(name)s] [req_id=%(request_id)s] %(message)s"
    formatter = logging.Formatter(log_format)

    correlation_filter = CorrelationIdFilter()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Clear existing handlers to maintain idempotency
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(correlation_filter)
    root_logger.addHandler(console_handler)

    # Configure dedicated verityai logger
    app_logger = logging.getLogger("verityai")
    app_logger.setLevel(numeric_level)
    # Ensure app logger propagates to root handler
    app_logger.propagate = True
