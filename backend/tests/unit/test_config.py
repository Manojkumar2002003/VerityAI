"""Unit tests for application configuration, defaults, and overrides."""

import pytest
from pydantic import ValidationError

from app.core.config import Settings

pytestmark = pytest.mark.unit


def test_config_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that default settings instantiate with expected values when no env overrides exist."""
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("API_VERSION", raising=False)
    monkeypatch.delenv("API_V1_PREFIX", raising=False)
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    settings = Settings(_env_file=None)
    assert settings.app_name == "VerityAI API"
    assert settings.api_version == "0.1.0"
    assert settings.environment == "development"
    assert settings.api_v1_prefix == "/api/v1"
    assert "http://localhost:5173" in settings.cors_origins
    assert settings.log_level == "INFO"
    assert "sqlite" in settings.database_url


def test_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that environment variables properly override default settings."""
    monkeypatch.setenv("APP_NAME", "VerityAI Custom Service")
    monkeypatch.setenv("API_VERSION", "1.2.3")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("API_V1_PREFIX", "/api/v2")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setenv("CORS_ORIGINS", "https://app.verity.ai")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./prod.db")

    settings = Settings(_env_file=None)
    assert settings.app_name == "VerityAI Custom Service"
    assert settings.api_version == "1.2.3"
    assert settings.environment == "production"
    assert settings.api_v1_prefix == "/api/v2"
    assert settings.log_level == "WARNING"
    assert settings.cors_origins == ["https://app.verity.ai"]
    assert settings.database_url == "sqlite:///./prod.db"


def test_cors_origins_parsing_from_string() -> None:
    """Verify that comma-separated and JSON string formats for cors_origins parse properly."""
    settings_csv = Settings(cors_origins="https://example.com, https://app.verity.ai")
    assert settings_csv.cors_origins == ["https://example.com", "https://app.verity.ai"]

    settings_json = Settings(cors_origins='["https://client1.com", "https://client2.com"]')
    assert settings_json.cors_origins == ["https://client1.com", "https://client2.com"]


def test_invalid_log_level_raises_validation_error() -> None:
    """Verify that an unrecognized log_level raises a validation error."""
    with pytest.raises(ValidationError):
        Settings(log_level="SUPER_VERBOSE")


def test_invalid_environment_raises_validation_error() -> None:
    """Verify that an invalid environment raises a validation error."""
    with pytest.raises(ValidationError):
        Settings(environment="staging")


def test_api_v1_prefix_validation() -> None:
    """Verify that malformed API prefixes fail validation with clear messages."""
    # Must start with forward slash
    with pytest.raises(ValidationError) as exc_info:
        Settings(api_v1_prefix="api/v1")
    assert "must start with a forward slash" in str(exc_info.value)

    # Must not end with trailing slash (except if prefix is root "/")
    with pytest.raises(ValidationError) as exc_info:
        Settings(api_v1_prefix="/api/v1/")
    assert "must not end with a trailing slash" in str(exc_info.value)

    # Valid prefix succeeds
    settings = Settings(api_v1_prefix="/api/v1")
    assert settings.api_v1_prefix == "/api/v1"
