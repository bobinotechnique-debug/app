"""Application settings for the backend skeleton."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized settings loader aligned to architecture lock."""

    model_config = SettingsConfigDict(env_prefix="SAMU_", env_file=".env", extra="ignore")

    app_name: str = Field(default="Planning Backend")
    environment: str = Field(default="development")
    database_url: str | None = Field(default=None)
    redis_url: str | None = Field(default=None)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()
