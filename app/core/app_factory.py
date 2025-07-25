from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    setup_logging()
    logger.info("Starting Media Generation API")
    
    app = FastAPI(
        title="Media Generation API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Register routers
    app.include_router(api_router)

    # Register ORM
    register_tortoise(
        app,
        config=settings.tortoise_config,
        generate_schemas=False,
        add_exception_handlers=True,
    )

    return app
