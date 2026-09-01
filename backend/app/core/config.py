"""
B2 - Application Settings & Environment Variable Configuration
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 1 (Foundation)

Loads and validates all environment variables at startup using Pydantic v2
BaseSettings. Any missing or malformed required variable raises a clear
ValidationError immediately, rather than failing silently at runtime.

Usage:
    # Option 1 – cached singleton (recommended for production code)
    from app.core.config import get_settings
    settings = get_settings()

    # Option 2 – direct module-level import (for bootstrap code)
    from app.core.config import settings
"""

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Type-safe application settings loaded from environment variables
    (or the .env file at project root).

    All fields are validated by Pydantic v2 at startup, so misconfigured
    environments are caught immediately rather than at runtime.
    """

    # ------------------------------------------------------------------
    # Application metadata
    # ------------------------------------------------------------------
    PROJECT_NAME: str = "AdoptAI App Knowledge Base"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Centralized knowledge base API for AdoptAI applications"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # ------------------------------------------------------------------
    # CORS – accepted as a comma-separated string from the env file and
    # parsed into a list of strings by the validator below.
    # ------------------------------------------------------------------
    ALLOWED_ORIGINS: str | List[str] = ["http://localhost:3000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: Any) -> List[str]:
        """Accept either a Python list OR a comma-separated string from .env."""
        if isinstance(value, str):
            if value.startswith("[") and value.endswith("]"):
                import json
                try:
                    return json.loads(value)
                except Exception:
                    pass
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(v).strip() for v in value]
        return ["http://localhost:3000"]

    # ------------------------------------------------------------------
    # Database – SQLAlchemy / PostgreSQL
    # ------------------------------------------------------------------
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/postgres"

    # ------------------------------------------------------------------
    # Database – Prisma Client Python
    # Used by `prisma generate` and the Prisma async client.
    # ------------------------------------------------------------------
    PRISMA_DATABASE_URL: str = ""

    # ------------------------------------------------------------------
    # Security (reserved for future auth stages – not used in Stage 1)
    # ------------------------------------------------------------------
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ------------------------------------------------------------------
    # Pydantic-Settings configuration
    # ------------------------------------------------------------------
    model_config = SettingsConfigDict(
        # Looks for `.env` relative to wherever the process is started.
        env_file=".env",
        env_file_encoding="utf-8",
        # Ignore extra keys that may exist in the .env file.
        extra="ignore",
        # Environment variables are case-insensitive.
        case_sensitive=False,
    )

    # ------------------------------------------------------------------
    # Derived helpers (not env vars — computed from other fields)
    # ------------------------------------------------------------------
    @property
    def app_name(self) -> str:
        """Shorthand alias kept for backward-compat with code using APP_NAME."""
        return self.PROJECT_NAME


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached singleton of the Settings object.

    Using @lru_cache means the .env file is parsed exactly once per
    process lifetime, which is both efficient and safe for production.

    Typical FastAPI DI usage:
        from app.core.config import get_settings
        from fastapi import Depends

        def some_route(cfg: Settings = Depends(get_settings)):
            ...
    """
    return Settings()


# Convenience module-level instance for direct imports where
# FastAPI DI is not required (e.g., database.py, main.py bootstrap).
settings: Settings = get_settings()
