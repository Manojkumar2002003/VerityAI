"""HTTP request logging and correlation ID middleware."""

import http
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.logging import request_id_ctx_var, sanitize_request_id

logger = logging.getLogger("verityai.http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to inject correlation IDs, track requests, and log structured metrics."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Extract and sanitize client-provided correlation ID or generate a fresh UUID4
        client_request_id = request.headers.get("X-Request-ID")
        request_id = sanitize_request_id(client_request_id)

        # Store in both context variable (for log record filter) and request.state
        request.state.request_id = request_id
        token = request_id_ctx_var.set(request_id)
        start_time = time.perf_counter()

        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as exc:
            # Handle unhandled route exceptions cleanly and return sanitized 500
            logging.getLogger("verityai").error(
                "Unhandled exception processing %s %s: %s",
                request.method,
                request.url.path,
                str(exc),
                exc_info=True,
            )
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )
            status_code = 500
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Attach X-Request-ID header to response
            response.headers["X-Request-ID"] = request_id

            # Determine appropriate log level based on response status
            status_phrase = (
                http.HTTPStatus(status_code).phrase
                if status_code in http.HTTPStatus._value2member_map_
                else "Unknown"
            )
            log_message = (
                f"{request.method} {request.url.path} - {status_code} {status_phrase} ({duration_ms:.2f}ms)"
            )

            if status_code >= 500:
                logger.error(log_message)
            elif status_code >= 400:
                logger.warning(log_message)
            else:
                logger.info(log_message)

            request_id_ctx_var.reset(token)

        return response
