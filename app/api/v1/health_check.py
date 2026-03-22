import structlog
from fastapi import Depends, APIRouter

from app.core.settings import get_settings, Settings

router = APIRouter(prefix="/health", tags=["Health Check"])
logger = structlog.get_logger()


@router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)):
    return {
        "env": settings.ENV,
        "debug": settings.DEBUG,
    }
