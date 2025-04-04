from .text import BaseText, ContentSourceType
from typing import List, Optional
from pydantic import BaseModel, Field


class PDFSection(BaseModel):
    """
    Model representing a section within a PDF document. 
    Sections will be used to create logical chunks, maintaining the document's flow and to work with larger documents.
    """
    title: Optional[str] = None
    content: str
    page_number: int


class PDFMetadata(BaseModel):
    """
    Model representing metadata specific to PDF documents.
    """
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    page_count: int = 0


class PDFDocument(BaseText):
    """
    Model representing a PDF document with additional PDF-specific fields.
    """
    metadata: PDFMetadata
    sections: List[PDFSection] = Field(default_factory=list)
    raw_text: str

    def __init__(self, **data):
        super().__init__(**data)
        self.source_type = ContentSourceType.PDF