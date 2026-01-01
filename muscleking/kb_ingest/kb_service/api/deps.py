from __future__ import annotations

from functools import lru_cache

from kb_service.core.config import Config, load_config


@lru_cache
def get_config() -> Config:
    """为 FastAPI 路由提供配置对象且仅加载一次"""
    return load_config()
