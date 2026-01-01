from __future__ import annotations

import logging

from fastapi import FastAPI

from kb_service.api.routes import router as api_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Knowledge Ingestion Service",
        version="0.1.0",
        description="Rewrite tabular data with LLMs, embed via pgvector, and expose retrieval APIs.",
    )
    # 同时暴露旧的 /api 接口，以及期望中的 /api/v1/knowledge 接口路径
    app.include_router(api_router, prefix="/api")
    app.include_router(api_router, prefix="/api/v1/knowledge")

    @app.get("/health", tags=["system"])
    def health_check():
        return {"status": "ok"}

    logger.info("FastAPI application initialised")
    return app


app = create_app()
