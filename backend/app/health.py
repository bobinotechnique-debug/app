"""Health check routes for service monitoring."""

from __future__ import annotations

from typing import Callable

from fastapi import APIRouter, FastAPI

HealthCheckHook = Callable[[], None]


def create_health_router(app: FastAPI, dependency_check: HealthCheckHook | None) -> APIRouter:
    """Create health endpoints with optional dependency check hook."""

    router = APIRouter()

    @router.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/health/ready")
    def ready() -> dict[str, str]:
        if getattr(app.state, "testing", False):
            return {"status": "ok"}

        if dependency_check is not None:
            dependency_check()

        return {"status": "ok"}

    return router

