"""Application bootstrap for the FastAPI backend."""

from __future__ import annotations

import os
from typing import Callable

from fastapi import FastAPI

from .api.routes import get_api_router
from .health import HealthCheckHook, create_health_router
from .infra.database import DatabaseSessionManager
from .settings import Settings, get_settings


def default_dependency_check() -> None:
    """Placeholder dependency check hook for readiness."""

    return None


def create_app(
    dependency_check: Callable[[], None] | None = None,
    *,
    testing: bool | None = None,
    settings: Settings | None = None,
) -> FastAPI:
    """Create the FastAPI application with health routes and placeholder APIs wired."""

    resolved_settings = settings or get_settings()

    app = FastAPI(title=resolved_settings.app_name)
    app.state.testing = bool(testing) if testing is not None else os.getenv("TESTING", "").lower() == "true"
    app.state.settings = resolved_settings
    app.state.db_session_manager = DatabaseSessionManager(resolved_settings.database_url)

    health_router = create_health_router(app, dependency_check or default_dependency_check)
    app.include_router(health_router)
    app.include_router(get_api_router())

    return app


app = create_app()

