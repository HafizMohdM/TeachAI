from fastapi import APIRouter
from . import story

api_router = APIRouter()

api_router.include_router(story.router, prefix="/ai", tags=["AI"])
