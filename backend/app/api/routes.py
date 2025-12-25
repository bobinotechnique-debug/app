"""Router registry for API placeholders."""

from fastapi import APIRouter, status

from ..services.placeholder_service import PlaceholderService


def get_api_router() -> APIRouter:
    """Return the aggregated API router."""

    router = APIRouter(prefix="/api")
    service = PlaceholderService()

    @router.get("/placeholder", status_code=status.HTTP_501_NOT_IMPLEMENTED)
    def placeholder() -> dict[str, str]:
        """Static placeholder endpoint to validate wiring."""

        return service.placeholder_response()

    return router
