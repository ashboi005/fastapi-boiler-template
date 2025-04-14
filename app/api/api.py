from fastapi import APIRouter
from app.api.routers import any_router

api_router = APIRouter()

api_router.include_router(any_router.router, prefix="/router", tags=["router"])
