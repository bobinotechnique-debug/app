"""Placeholder service for skeleton wiring."""

from __future__ import annotations


class PlaceholderService:
    """Orchestrates placeholder flows without business rules."""

    def placeholder_response(self) -> dict[str, str]:
        """Return a static response indicating the route is not implemented."""

        return {"detail": "not implemented"}
