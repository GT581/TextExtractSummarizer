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
    Clean and normalize plain text for LLM processing.
    Optimized for text from regular sources like plain text files or user input.
    
    Args:
        text (str): The input text
        
    Returns:
        str: Cleaned text optimized for LLM processing
    """
    # Normalize line breaks (preserve paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove extra spaces/tabs
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Clean up spaces at line boundaries
    text = re.sub(r'\n[ \t]+', '\n', text)
    text = re.sub(r'[ \t]+\n', '\n', text)
    
    # Remove leading/trailing whitespace
    return text.strip()


def clean_pdf_text(text: str) -> str:
    """
    Clean and normalize text extracted from PDF files.
    Optimized for handling PDF-specific artifacts while preserving structure.
    
    Args:
        text (str): The text extracted from PDF
        
    Returns:
        str: Cleaned text optimized for LLM processing
    """
    # Replace form feed characters (page breaks)
    text = text.replace('\f', '\n\n')
    
    # Fix hyphenated words split across lines
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # Normalize line breaks (preserve paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Normalize multiple spaces but preserve initial indents
    lines = []
    for line in text.split('\n'):
        # Preserve indentation (up to 4 spaces)
        match = re.match(r'^( {1,4})', line)
        if match:
            indent = match.group(1)
            rest = re.sub(r'[ \t]+', ' ', line[len(indent):])
            lines.append(indent + rest)
        else:
            lines.append(re.sub(r'[ \t]+', ' ', line))
    
    # Rejoin with preserved newlines
    text = '\n'.join(lines)
    
    # Remove leading/trailing whitespace
    return text.strip()


def clean_html_text(text: str) -> str:
    """
    Clean and normalize text extracted from HTML/web sources.
    Optimized for handling HTML-specific artifacts.
    
    Args:
        text (str): The text extracted from HTML/web
        
    Returns:
        str: Cleaned text optimized for LLM processing
    """
    # Normalize excessive newlines (HTML often has many)
    text = re.sub(r'\n{2,}', '\n', text)
    
    # Normalize spaces (HTML often has inconsistent spacing)
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Clean up spaces at line boundaries
    text = re.sub(r'\n[ \t]+', '\n', text)
    text = re.sub(r'[ \t]+\n', '\n', text)
    
    # Fix common HTML artifacts
    text = re.sub(r'•', '- ', text)  # Convert bullets to dashes
    text = re.sub(r'&nbsp;', ' ', text)  # Fix any remaining HTML entities
    text = re.sub(r'[ \t]*-[ \t]*', ' - ', text)  # Normalize dash spacing
    
    # Remove leading/trailing whitespace
    return text.strip()