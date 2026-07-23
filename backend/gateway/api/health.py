from fastapi import APIRouter, HTTPException

from core.settings import get_settings
from core.startup import check_runtime_readiness


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ready")
def readiness_check():
    try:
        return check_runtime_readiness(get_settings())
    except Exception as error:
        raise HTTPException(status_code=503, detail="Application is not ready.") from error
