from typing import Dict, Any

from app.core.logging import get_logger
from app.utils.text_utils import clean_text, estimate_word_count

logger = get_logger(__name__)


class TextProcessor:
    """
    Service for processing plain text content.
    
    This class provides methods to clean text and extract basic metadata.
    """
    
    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """
        Extract metadata from text content.
        
        Args:
            text (str): The text content
            
        Returns:
            Dict[str, Any]: Extracted metadata
        """
        cleaned_text = clean_text(text)
        
        # Extract potential / default title (first non-empty line)
        lines = cleaned_text.split('\n')
        title = None
        
        for line in lines:
            line = line.strip()
            if line and len(line) < 50:  # Reasonable length for a title
                title = line
                break
        
        word_count = estimate_word_count(cleaned_text)
        
        return {
            "title": title,
            "word_count": word_count
        }
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process text content and extract basic metadata.
        
        Args:
            text (str): The text content
            
        Returns:
            Dict[str, Any]: Processed text with metadata
        """
        cleaned_text = clean_text(text)
        metadata = self.extract_metadata(cleaned_text)
        
        return {
            "raw_text": cleaned_text,
            "metadata": metadata
        } 