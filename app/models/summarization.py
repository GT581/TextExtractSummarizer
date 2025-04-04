from pydantic import BaseModel
from typing import Optional
from .text import ContentSourceType


class SummarizationRequest(BaseModel):
    """
    Model for a summarization request.
    
    Attributes:
        source_type (ContentSourceType): Type of content source
        max_length (Optional[int]): Maximum length of the summary in words
        text (Optional[str]): Raw text (for TEXT source type)
        url (Optional[HttpUrl]): URL to scrape (for URL source type)
    """
    source_type: ContentSourceType
    max_length: Optional[int] = None
    text: Optional[str] = None
    url: Optional[str] = None


class SummarizationResponse(BaseModel):
    """
    Model for a summarization response.
    
    Attributes:
        summary (str): The generated summary text
        word_count (int): Number of words in the summary
        title (Optional[str]): Title of the original content
    """
    summary: str
    word_count: Optional[int] = None
    title: Optional[str] = None