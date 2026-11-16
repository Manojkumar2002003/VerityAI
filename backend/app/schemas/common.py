"""Reusable Pydantic schemas for core and system endpoints."""

from typing import Any, List, Union
from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """Response model for root service identification endpoint."""

    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="API semantic version")
    message: str = Field(..., description="Operational status message")


class HealthResponse(BaseModel):
    """Response model for system health/liveness check endpoint."""

    status: str = Field(..., description="Overall service status (e.g. ok)")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="API semantic version")


class ReadinessChecks(BaseModel):
    """Component-level readiness verification results."""

    database: str = Field(
        ...,
        description="Database connectivity status ('ok' or 'unavailable')",
        examples=["ok"],
    )


class ReadinessResponse(BaseModel):
    """Response model for system readiness check endpoint."""

    status: str = Field(
        ...,
        description="Overall service readiness status ('ready' or 'not_ready')",
        examples=["ready"],
    )
    checks: ReadinessChecks = Field(
        ...,
        description="Detailed component health verification results",
    )


class ModelInfoResponse(BaseModel):
    """Response model for ML model metadata and readiness contract."""

    status: str = Field(
        ...,
        description="Configuration and readiness status of the ML model",
        examples=["not_configured"],
    )
    supported_language: str = Field(
        ...,
        description="Primary language code supported by the model",
        examples=["en"],
    )
    detection_available: bool = Field(
        ...,
        description="Whether active ML detection inference is available",
        examples=[False],
    )
    model_candidate: str = Field(
        ...,
        description="Planned primary model architecture candidate",
        examples=["microsoft/deberta-v3-base (planned)"],
    )


class ErrorDetail(BaseModel):
    """Standardized error response payload."""

    detail: Union[str, List[Any]] = Field(
        ...,
        description="Error description or list of validation issues",
    )
