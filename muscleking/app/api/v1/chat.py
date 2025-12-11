"""
具有智能体聊天功能的API
"""
from fastapi import APIRouter, HTTPException
from muscleking.app.models.model_chat import ChatRequest, ChatResponse
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from muscleking.app.services.service_chat import get_or_create_session, save_message

router = APIRouter()

@router.post("/",response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db : Session = None  # 假设有一个数据库会话依赖
) -> ChatResponse:
    """
    具有Agent智能体聊天功能的API端点
    """
    # 获取或创建会话
    session_id = get_or_create_session(db, request.session_id, request.user_id)

    # 存储用户消息
    await save_message(db, session_id, request.message, is_user=True)

    response = ChatResponse(
        message="这是一个示例回复。",
        session_id=request.session_id or "new_session",
        message_id="msg_12345"
    )
    return response