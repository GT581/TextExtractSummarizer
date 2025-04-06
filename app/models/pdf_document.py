from typing import List, Optional
from pydantic import BaseModel, Field


class PDFSection(BaseModel):
    """
    Model representing a section within a PDF document. 
    Sections will be used to create logical chunks, maintaining the document's flow and work with larger documents.
    
    Attributes:
        title (Optional[str]): Section title or heading
        content (str): The text content of the section
        page_number (int): The page number where the section is located
    
    """
    title: Optional[str] = None
    content: str
    page_number: int


class PDFMetadata(BaseModel):
    """
    Model representing metadata specific to PDF documents.

    Attributes:
        title (Optional[str]): Document title
        author (Optional[str]): Document author
        subject (Optional[str]): Document subject
        keywords (List[str]): Keywords associated with the document
        creation_date (Optional[str]): Document creation date
        modification_date (Optional[str]): Document last modification date
        page_count (int): Total number of pages
        word_count (int): Approximate word count
    """
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    page_count: int = 0
    word_count: int = 0


class PDFDocument(BaseModel):
    """
    Model representing a PDF document with additional PDF-specific fields.

    Attributes:
        filename (str): Original filename of the document
        metadata (PDFMetadata): Document metadata
        sections (List[PDFSection]): List of identified sections
        raw_text (str): Raw extracted text from the document
    """
    filename: str
    metadata: PDFMetadata
    sections: List[PDFSection] = Field(default_factory=list)
    raw_text: str
