from fastapi import APIRouter
from .endpoints import items, demo

router = APIRouter(prefix="/api/v1")
router.include_router(items.router)
router.include_router(demo.router)
