import sys
from loguru import logger
from app.core.config import settings

def setup_logging():
    """Configure loguru logging for the application"""
    logger.remove()  # Remove default handler
    
    # Console logging
    logger.add(
        sys.stdout,
        level="INFO" if not settings.DEBUG else "DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    return logger