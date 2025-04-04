import re

from app.core.logging import get_logger

logger = get_logger(__name__)


def estimate_word_count(text: str) -> int:
    """
    Estimate the word count in a text input.
    
    Args:
        text (str): The input text
        
    Returns:
        int: Estimated word count
    """
    # Remove extra whitespace and split by whitespace
    words = re.sub(r'\s+', ' ', text).strip().split()
    
    return len(words)


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text (str): The input text
        
    Returns:
        str: Cleaned text
    """
    # Replace multiple newlines with single newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove form feed characters
    text = text.replace('\f', '\n')
    
    # Standardize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()