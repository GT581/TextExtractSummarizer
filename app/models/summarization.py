from pydantic import BaseModel
from typing import Optional
from .text import ContentSourceType


class SummarizationRequest(BaseModel):
    source_type: ContentSourceType
    max_length: Optional[int] = None
    text: Optional[str] = None
    url: Optional[str] = None


class SummarizationResponse(BaseModel):
    summary: str
    word_count: Optional[int] = None
    title: Optional[str] = None