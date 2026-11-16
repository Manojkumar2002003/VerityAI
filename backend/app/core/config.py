"""Application settings and environment configuration."""

import json
from functools import lru_cache
from typing import List, Literal, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(
        default="VerityAI API",
        description="Public title and service identifier",
    )
    api_version: str = Field(
        default="0.1.0",
        description="Semantic version of the API",
    )
    environment: Literal["development", "test", "production"] = Field(
        default="development",
        description="Runtime environment name",
    )
    api_v1_prefix: str = Field(
        default="/api/v1",
        description="Prefix path for version 1 API endpoints",
    )
    cors_origins: Union[List[str], str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"],
        description="Permitted cross-origin resource sharing (CORS) origins",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging verbosity level",
    )
    database_url: str = Field(
        default="sqlite:///./data/verityai.db",
        description="Database connection URL (defaults to local dedicated data directory)",
    )

    @field_validator("api_v1_prefix")
    @classmethod
    def validate_api_v1_prefix(cls, v: str) -> str:
        """Validate that API prefix starts with a leading slash and does not have a trailing slash."""
        prefix = v.strip()
        if not prefix.startswith("/"):
            raise ValueError("api_v1_prefix must start with a forward slash '/'")
        if prefix != "/" and prefix.endswith("/"):
            raise ValueError("api_v1_prefix must not end with a trailing slash '/'")
        return prefix

    @field_validator("cors_origins", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins whether provided as a JSON array or comma-separated string."""
        if isinstance(v, str):
            v_stripped = v.strip()
            if v_stripped.startswith("[") and v_stripped.endswith("]"):
                try:
                    parsed = json.loads(v_stripped)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except Exception:
                    pass
            return [origin.strip() for origin in v_stripped.split(",") if origin.strip()]
        elif isinstance(v, list):
            return [str(item).strip() for item in v if str(item).strip()]
        raise ValueError("Invalid cors_origins format. Must be a list or comma-separated string.")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level string against standard logging levels."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper_v = v.strip().upper()
        if upper_v not in valid_levels:
            raise ValueError(f"Invalid log_level: '{v}'. Must be one of {valid_levels}")
        return upper_v


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
