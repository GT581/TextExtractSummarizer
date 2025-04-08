import os
from typing import Optional

from fastapi import APIRouter, UploadFile, HTTPException, File, Form

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.summarization import SummarizationRequest, SummarizationResponse
from app.models.text import ContentSourceType
from app.services.summarization import SummarizationService
from app.services.llm_provider import LLMProviderFactory
from app.utils.file_utils import handle_file_upload, clean_temp_file


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


@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_content(
    file: Optional[UploadFile] = File(None),
    max_length: Optional[int] = Form(None),
    include_metadata: bool = Form(True),
    source_type: ContentSourceType = Form(ContentSourceType.PDF),
    text: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
):
    """
    Summarize content from different sources (PDF, text, or URL).
    
    Args:
        file (Optional[UploadFile]): The file to summarize (for PDF source types)
        max_length (Optional[int]): Maximum length of the summary in words
        include_metadata (bool): Whether to include document metadata in the response
        source_type (ContentSourceType): Type of content source
        text (Optional[str]): Raw text to summarize (for TEXT source type)
        url (Optional[str]): URL to scrape and summarize (for URL source type)
        
    Returns:
        SummarizationResponse: The generated summary
    """
    temp_file_path = None
    
    try:
        # Validate request
        if source_type == ContentSourceType.URL and not url:
            raise HTTPException(status_code=400, detail="URL is required for URL source type")
        
        if source_type == ContentSourceType.TEXT and not text:
            raise HTTPException(status_code=400, detail="Text is required for TEXT source type")
        
        if source_type == ContentSourceType.PDF and not file:
            raise HTTPException(status_code=400, detail="File is required for PDF source type")
        
        # Initialize LLM / Summary services
        llm_provider = LLMProviderFactory.get_provider()
        summarization_service = SummarizationService(llm_provider=llm_provider)

        # Handle PDF
        if source_type == ContentSourceType.PDF:
            if not file:
                raise HTTPException(status_code=400, detail=f"File is required for {source_type.value} source type")
            
            # Handle file upload
            temp_file_path = handle_file_upload(file)
            
            request = SummarizationRequest(
                source_type=source_type,
                max_length=max_length,
                file_path=temp_file_path,
                include_metadata=include_metadata
            )
            
            response = await summarization_service.summarize_from_request(request)
            
        else:
            # Handle TEXT and URL direct input source types
            request = SummarizationRequest(
                source_type=source_type,
                max_length=max_length,
                text=text,
                url=url,
                include_metadata=include_metadata
            )
            
            response = await summarization_service.summarize_from_request(request)
            
        return response
            
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error processing content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")
    
    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            clean_temp_file(temp_file_path)