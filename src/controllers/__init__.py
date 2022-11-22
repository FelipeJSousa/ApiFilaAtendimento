from fastapi import APIRouter

from src.controllers.fila.fila import fila_router

router = APIRouter()
router.include_router(fila_router, prefix="/api", tags=["Fila"])


__all__ = ["router"]
