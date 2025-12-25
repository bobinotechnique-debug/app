"""Hardening smoke tests for application startup wiring."""

from __future__ import annotations

import asyncio

from backend.app.infra.database import DatabaseSessionManager
from backend.app.main import create_app


def test_app_registers_health_and_api_routes() -> None:
    app = create_app(testing=True)

    registered_paths = {route.path for route in app.router.routes}

    assert "/health/live" in registered_paths
    assert "/health/ready" in registered_paths
    assert "/api/placeholder" in registered_paths


def test_shutdown_hook_disposes_database_manager(monkeypatch) -> None:
    app = create_app(testing=True)
    manager: DatabaseSessionManager = app.state.db_session_manager
    disposed = {"called": False}

    def _mark_disposed() -> None:
        disposed["called"] = True

    monkeypatch.setattr(manager, "dispose", _mark_disposed)

    async def _run_shutdown() -> None:
        for handler in app.router.on_shutdown:
            await handler()

    asyncio.run(_run_shutdown())

    assert disposed["called"] is True
