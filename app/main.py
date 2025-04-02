from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.core.config import get_settings


def create_application() -> FastAPI:
    """
    Create and configure our FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    settings = get_settings()
    
    # Create our FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        redoc_url=None,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )
    
    # Configure basic CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount API router using settings prefix
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    return app


app = create_application()