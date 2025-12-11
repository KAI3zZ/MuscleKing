"""
agents 相关的数据模型
"""
from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any

class AdditionalGuardrailsOutput(BaseModel):
    """
    格式化输出"end" 或 "proceed"，用于判断用户的问题是否与图谱内容相关
    """
    decision: Literal["end", "proceed"] = Field(
        description="Decision on whether the question is related to the graph contents."
    )

class Router(BaseModel):
    """路由类型数据模型，用于分类解决用户问题的路径"""
    # logic是不同路由类型的判断逻辑
    logic: str = ""
    type: Literal[
        "general-query",
        # "additional-query",
        "kb-query",
        "lightrag-query",
        # "image-query",
        # "file-query",
        # "text2sql-query",
    ] = "kb-query"
    question: str = ""
    decision: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None

    class Config:
        extra = "allow" # 允许额外的字段

    def __getattr__(self, key: str) -> Any:
        """字典风格访问兼容旧逻辑。"""
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        """字典风格访问兼容旧逻辑。"""
        return getattr(self, key, self.__dict__.get(key, default))