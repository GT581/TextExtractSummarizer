from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ContentSourceType(str, Enum):
    """
    Type of source / input content.
    """
    PDF = "pdf"
    URL = "url"
    TEXT = "text"


class BaseText(BaseModel):
    """
    Base model for all text content.
    """
    content: str
    source_type: ContentSourceType
    title: Optional[str] = None
    word_count: Optional[int] = None