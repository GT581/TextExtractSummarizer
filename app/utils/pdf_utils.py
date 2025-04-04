import re
from typing import List, Tuple

from app.core.logging import get_logger

logger = get_logger(__name__)


def extract_possible_headers(text: str) -> List[str]:
    """
    Extract possible section headers from text.
    
    Args:
        text (str): The input text
        
    Returns:
        List[str]: List of possible headers
    """
    # Patterns for common section header formats
    patterns = [
        r"^(?:CHAPTER|Chapter|SECTION|Section)\s+\d+[.:]\s*(.+)$",
        r"^\d+\.\d+\s+(.+)$",  # 1.1 Header
        r"^\d+\.\s+(.+)$",     # 1. Header
        r"^[A-Z][A-Z\s]+[A-Z]$",  # ALL CAPS HEADERS
        r"^[IVX]+\.\s+(.+)$",    # Roman numerals: IV. Header
    ]
    
    headers = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # Checking if line matches any header patterns
        for pattern in patterns:
            if re.match(pattern, line):
                headers.append(line)
                break
                
    return headers


def identify_section_boundaries(text: str) -> List[Tuple[int, int, str]]:
    """
    Identify section boundaries in the text.
    
    Args:
        text (str): The input text
        
    Returns:
        List[Tuple[int, int, str]]: List of (start_index, end_index, header) tuples
    """
    lines = text.split("\n")
    possible_headers = extract_possible_headers(text)
    
    # Find indices of all possible section headers
    section_starts = []
    for i, line in enumerate(lines):
        if line.strip() in possible_headers:
            section_starts.append((i, line.strip()))
    
    # Create section boundaries
    sections = []
    for i in range(len(section_starts)):
        start_idx, header = section_starts[i]
        
        if i < len(section_starts) - 1:
            end_idx = section_starts[i + 1][0] - 1
        else:
            end_idx = len(lines) - 1
            
        sections.append((start_idx, end_idx, header))
    
    # If no sections are found, then have the entire text as one section
    if not sections:
        sections = [(0, len(lines) - 1, "")]
        
    return sections