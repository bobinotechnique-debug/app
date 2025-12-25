"""Application bootstrap for the FastAPI backend."""

from __future__ import annotations

import os
from typing import Callable

from fastapi import FastAPI

from .health import HealthCheckHook, create_health_router


def default_dependency_check() -> None:
    """Placeholder dependency check hook for readiness."""

    return None


def create_app(
    dependency_check: Callable[[], None] | None = None,
    *,
    testing: bool | None = None,
) -> FastAPI:
    """Create the FastAPI application with health routes wired."""

    app = FastAPI(title="Planning Backend")
    app.state.testing = bool(testing) if testing is not None else os.getenv("TESTING", "").lower() == "true"

    health_router = create_health_router(app, dependency_check or default_dependency_check)
    app.include_router(health_router)

    return app


app = create_app()

