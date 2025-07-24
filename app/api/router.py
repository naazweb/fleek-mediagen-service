from fastapi import APIRouter
from app.api.media_gen import router as media_gen_router

api_router = APIRouter()

api_router.include_router(media_gen_router, prefix="", tags=["media"])