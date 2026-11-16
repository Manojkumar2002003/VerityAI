"""Version 1 API routes for VerityAI."""

import logging
from typing import Optional
from fastapi import APIRouter, Response, status
from sqlalchemy import Engine, text

from app.core.config import get_settings
from app.db.session import get_engine
from app.schemas.common import (
    HealthResponse,
    ModelInfoResponse,
    ReadinessChecks,
    ReadinessResponse,
)

logger = logging.getLogger("verityai.health")
api_router = APIRouter()


def check_database_connectivity(engine: Optional[Engine] = None) -> str:
    """Execute a lightweight, bounded query to verify database connectivity.

    Returns 'ok' on success or 'unavailable' on error without exposing raw exception
    messages or credentials to external callers.
    """
    target_engine = engine or get_engine()
    try:
        with target_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "ok"
    except Exception as exc:
        logger.error("Database connectivity check failed: %s", str(exc), exc_info=True)
        return "unavailable"


@api_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness check",
    description="Verify that the backend process is running and responsive. Does not probe external dependencies.",
)
async def get_health() -> HealthResponse:
    """Return process operational health/liveness status."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.api_version,
    )


@api_router.get(
    "/health/ready",
    response_model=ReadinessResponse,
    summary="Readiness check",
    description="Verify that the application and its database are ready to process operations.",
    responses={
        status.HTTP_200_OK: {"model": ReadinessResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ReadinessResponse},
    },
)
async def get_readiness(response: Response) -> ReadinessResponse:
    """Verify database readiness. Returns HTTP 503 if database connectivity fails."""
    db_status = check_database_connectivity()
    if db_status == "ok":
        return ReadinessResponse(
            status="ready",
            checks=ReadinessChecks(database="ok"),
        )

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadinessResponse(
        status="not_ready",
        checks=ReadinessChecks(database="unavailable"),
    )


@api_router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    summary="Model metadata contract",
    description="Report machine-learning model readiness and language capabilities.",
)
async def get_model_info() -> ModelInfoResponse:
    """Return model status indicating detection engine is currently unconfigured."""
    return ModelInfoResponse(
        status="not_configured",
        supported_language="en",
        detection_available=False,
        model_candidate="microsoft/deberta-v3-base (planned)",
    )
