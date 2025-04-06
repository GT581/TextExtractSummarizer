from pydantic import BaseModel
from typing import Optional, Dict, Any
from .text import ContentSourceType


class SummarizationRequest(BaseModel):
    """
    Model for a summarization request.
    
    Attributes:
        source_type (ContentSourceType): Type of content source (PDF, TEXT, or URL)
        max_length (Optional[int]): Targeted length of the summary in words
        text (Optional[str]): Raw text (for TEXT source type)
        url (Optional[str]): URL to scrape (for URL source type)
        file_path (Optional[str]): Path to the uploaded PDF file (for PDF source type)
        include_metadata (bool): Whether to include metadata in the response
    """
    source_type: ContentSourceType
    max_length: Optional[int] = None
    text: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = None
    include_metadata: bool = True


class SummarizationResponse(BaseModel):
    """
    Model for a summarization response.
    
    Attributes:
        summary (str): The generated summary text
        word_count (int): Number of words in the summary
        title (Optional[str]): Title of the original content
        metadata (Optional[Dict[str, Any]]): Additional metadata about the content
    """
    summary: str
    word_count: int
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None