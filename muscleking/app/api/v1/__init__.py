"""
聚合v1版本的所有路由
"""

from fastapi import APIRouter
from muscleking.app.api.v1 import chat


api_v1_router = APIRouter()

api_v1_router.include_router(chat.router, prefix="/chat", tags=["Unified Chat"])
# api_v1_router.include_router(sessions.router, prefix="/sessions", tags=["Chat Sessions"])
# api_v1_router.include_router(upload.router, prefix="/upload", tags=["File Upload"])