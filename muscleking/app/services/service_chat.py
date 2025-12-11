"""
聊天服务模块
"""
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from muscleking.app.models.model_chat import SessionInfo



async def get_or_create_session(db, session_id: Optional[str] = None, user_id: str = "default_user") -> str:
    """获取或创建聊天会话"""
    if session_id:
        pass  # 查询数据库是否存在该会话
    else:
        # 创建新会话
        new_session_id = str(uuid.uuid4())
        pass    # 创建Session信息对象并保存到数据库
    return new_session_id