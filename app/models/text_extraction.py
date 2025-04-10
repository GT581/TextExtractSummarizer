from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any


class ContentSourceType(str, Enum):
    """
    Type of source / input content.
    """
    PDF = "pdf"
    URL = "url"
    TEXT = "text"


class ExtractionType(str, Enum):
    """
    Enum for extraction types.
    """
    KEY_POINTS = "key_points"
    ENTITIES = "entities"
    CUSTOM = "custom"


class ExtractionRequest(BaseModel):
    """
    Model for a text extraction request.
    
    Attributes:
        source_type (ContentSourceType): Type of content source
        extraction_type (ExtractionType): Type of extraction to perform
        url (Optional[str]): URL to scrape (for URL source type)
        text (Optional[str]): Raw text (for TEXT source type)
        file_path (Optional[str]): Path to the uploaded PDF file (for PDF source type)
        custom_instructions (Optional[str]): Custom extraction instructions
        include_context (bool): Whether to include context in the response
    """
    source_type: ContentSourceType
    extraction_type: ExtractionType
    url: Optional[str] = None
    text: Optional[str] = None
    file_path: Optional[str] = None
    custom_instructions: Optional[str] = None
    include_context: bool = False


class KeyValuePair(BaseModel):
    """
    Model for a key-value pair.
    
    Attributes:
        key (str): The key or label
        value (str): The extracted value
    """
    key: str
    value: str


class Entity(BaseModel):
    """
    Model for an extracted entity.
    
    Attributes:
        name (str): Entity name
        type (str): Entity type (e.g., person, organization, location)
        mentions (List[str]): Mentions of the entity in the text
    """
    name: str
    type: str
    mentions: List[str] = Field(default_factory=list)


class ExtractionResponse(BaseModel):
    """
    Model for a text extraction response.
    
    Attributes:
        success (bool): Whether the extraction was successful
        extraction_type (ExtractionType): Type of extraction performed
        source_type (ContentSourceType): Type of content source
        data (Dict[str, Any]): Extracted data
        key_value_pairs (List[KeyValuePair]): List of key-value pairs
        entities (List[Entity]): List of extracted entities
        context (Optional[str]): Context for the extraction
    """
    success: bool
    extraction_type: ExtractionType
    source_type: ContentSourceType
    data: Dict[str, Any] = Field(default_factory=dict)
    key_value_pairs: List[KeyValuePair] = Field(default_factory=list)
    entities: List[Entity] = Field(default_factory=list)
    context: Optional[str] = None