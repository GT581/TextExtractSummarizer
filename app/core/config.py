import os
from typing import List
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    
    Attributes:
        PROJECT_NAME (str): The name of the project
        PROJECT_DESCRIPTION (str): Description of the project
        PROJECT_VERSION (str): Version of the project
        API_PREFIX (str): Prefix for all API endpoints
        CORS_ORIGINS (List[str]): List of allowed CORS origins
        GOOGLE_API_KEY (str): Google API key for Gemini
        DEFAULT_MAX_SUMMARY_LENGTH (int): Default maximum length for summaries
        UPLOAD_DIR (str): Directory to store uploaded files
    """
    PROJECT_NAME: str = "Text Extract & Summarizer API"
    PROJECT_DESCRIPTION: str = "An API that summarizes content from multiple sources and extracts specific information from text"
    PROJECT_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = ["*"]
    
    # LLM Config - API Key loaded from .env
    GOOGLE_API_KEY: str
    GOOGLE_MODEL_NAME: str = "gemini-1.5-flash"

    LLM_TEMPERATURE: float = 0.1
    LLM_TOP_P: float = 0.95
    LLM_MAX_TOKENS: int = 1024
    
    # App Defaults
    DEFAULT_MAX_SUMMARY_LENGTH: int = 1000
    UPLOAD_DIR: str = "uploads"
    DEFAULT_LLM_PROVIDER: str = 'google'

    # Cls arg for pydantic validator
    @field_validator("UPLOAD_DIR", mode="before")
    def create_upload_dir(cls, v):
        """
        Ensures the upload directory exists.
        
        Args:
            v (str): The upload directory path
            
        Returns:
            str: The validated upload directory path
        """
        os.makedirs(v, exist_ok=True)
        return v
    
    # Load API Key from .env file
    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings with caching.
    
    Returns:
        Settings: Application settings
    """
    return Settings() 