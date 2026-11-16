"""Main FastAPI application initialization, middleware, routes, and error handlers."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import get_current_request_id, setup_logging
from app.core.middleware import RequestLoggingMiddleware
from app.schemas.common import RootResponse

logger = logging.getLogger("verityai")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown events."""
    settings = get_settings()
    setup_logging(settings.log_level)
    logger.info("Starting %s v%s in %s environment", settings.app_name, settings.api_version, settings.environment)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    setup_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.api_version,
        description="VerityAI — English-language AI-generated text detection platform backend API.",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
        lifespan=lifespan,
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # Configure request logging and correlation ID middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Root identification endpoint
    @app.get(
        "/",
        response_model=RootResponse,
        summary="API Root",
        description="Provide basic service identification and operational status.",
        tags=["System"],
    )
    async def root() -> RootResponse:
        return RootResponse(
            app_name=settings.app_name,
            version=settings.api_version,
            message="VerityAI API is running.",
        )

    # Mount versioned API router
    app.include_router(api_router, prefix=settings.api_v1_prefix, tags=["v1"])

    # Global Exception Handlers for consistent structured errors
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Handle standard HTTP exceptions consistently with correlation ID header."""
        headers = {}
        request_id = get_current_request_id()
        if request_id:
            headers["X-Request-ID"] = request_id

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle request validation errors without exposing internal paths or details."""
        headers = {}
        request_id = get_current_request_id()
        if request_id:
            headers["X-Request-ID"] = request_id

        sanitized_errors = []
        for err in exc.errors():
            loc = [str(x) for x in err.get("loc", []) if x != "body"]
            sanitized_errors.append(
                {
                    "field": ".".join(loc) if loc else "body",
                    "message": err.get("msg", "Validation error"),
                    "type": err.get("type", "value_error"),
                }
            )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": sanitized_errors},
            headers=headers,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch unhandled exceptions, log details with correlation ID, and return safe 500 response."""
        logger.error(
            "Unhandled exception processing %s %s: %s",
            request.method,
            request.url.path,
            str(exc),
            exc_info=True,
        )
        headers = {}
        request_id = get_current_request_id()
        if request_id:
            headers["X-Request-ID"] = request_id

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
            headers=headers,
        )

    return app


app = create_app()
