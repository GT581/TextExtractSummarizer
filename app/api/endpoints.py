from fastapi import APIRouter

from app.core.config import get_settings
from app.core.logging import get_logger


# Create API router
router = APIRouter()

# Create Endpoint logger
logger = get_logger(__name__)


@router.get("/")
async def root():
    """
    Root endpoint that returns a simple welcome message and lets the user know docs are available at the default /docs endpoint.
    
    Returns:
        dict: Welcome message
    """
    return {
        "message": "Welcome to Text Extract & Summarizer API",
        "docs": "/docs",  # Default FastAPI doc link
    }


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health check information
    """
    settings = get_settings()
    
    return {
        "status": "ok",
        "version": settings.PROJECT_VERSION,
    }