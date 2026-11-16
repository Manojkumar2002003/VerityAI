"""Unit tests for backend Pydantic response models and schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.common import (
    ErrorDetail,
    HealthResponse,
    ModelInfoResponse,
    ReadinessChecks,
    ReadinessResponse,
    RootResponse,
)

pytestmark = pytest.mark.unit


def test_root_response_valid() -> None:
    """Verify RootResponse validates expected fields and types."""
    data = {
        "app_name": "VerityAI API",
        "version": "0.1.0",
        "message": "VerityAI backend service is running.",
    }
    response = RootResponse(**data)
    assert response.app_name == "VerityAI API"
    assert response.version == "0.1.0"
    assert response.message == "VerityAI backend service is running."


def test_root_response_missing_fields_raises_validation_error() -> None:
    """Verify RootResponse rejects missing required attributes."""
    with pytest.raises(ValidationError):
        RootResponse(app_name="VerityAI API")  # type: ignore[call-arg]


def test_health_response_valid() -> None:
    """Verify HealthResponse model serialization."""
    health = HealthResponse(status="ok", app_name="VerityAI API", version="0.1.0")
    assert health.status == "ok"
    assert health.app_name == "VerityAI API"
    assert health.version == "0.1.0"


def test_readiness_response_valid() -> None:
    """Verify ReadinessResponse with database checks."""
    checks = ReadinessChecks(database="ok")
    ready = ReadinessResponse(status="ready", checks=checks)
    assert ready.status == "ready"
    assert ready.checks.database == "ok"

    unready = ReadinessResponse(status="not_ready", checks=ReadinessChecks(database="unavailable"))
    assert unready.status == "not_ready"
    assert unready.checks.database == "unavailable"


def test_model_info_response_defaults_and_values() -> None:
    """Verify ModelInfoResponse structure and contract attributes."""
    info = ModelInfoResponse(
        status="not_configured",
        supported_language="en",
        detection_available=False,
        model_candidate="microsoft/deberta-v3-base (planned)",
    )
    assert info.status == "not_configured"
    assert info.supported_language == "en"
    assert info.detection_available is False
    assert "deberta" in info.model_candidate


def test_error_detail_structure() -> None:
    """Verify ErrorDetail validation with string or list payloads."""
    str_err = ErrorDetail(detail="Resource not found")
    assert str_err.detail == "Resource not found"

    list_err = ErrorDetail(detail=[{"field": "count", "message": "Invalid integer"}])
    assert isinstance(list_err.detail, list)
    assert len(list_err.detail) == 1
