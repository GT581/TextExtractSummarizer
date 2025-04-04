from typing import List, Tuple, Dict
import fitz
import re

from app.models.pdf_document import PDFDocument, PDFMetadata, PDFSection
from app.utils.text_utils import clean_text, estimate_word_count
from app.core.logging import get_logger

logger = get_logger(__name__)


class PDFParser:
    """
    Service for parsing and extracting content from PDF documents.
    
    This class provides methods to extract text, identify document structure,
    and prepare content for summarization and extraction.
    """
    
    def extract_text_pages(self, file_path: str) -> Tuple[str, Dict[int, int]]:
        """
        Extract text from a PDF file while tracking page numbers.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            Tuple[str, Dict[int, int]]: Tuple containing (extracted_text, line_to_page_map)
        """
        full_text = ""
        line_to_page_map = {}
        line_index = 0
        
        try:
            doc = fitz.open(file_path)
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_text = page.get_text()
                
                # Count the lines in this page's text
                page_lines = page_text.split('\n')
                
                # Map each line in this page to its page number
                for i in range(len(page_lines)):
                    line_to_page_map[line_index + i] = page_num
                
                # Update line index for the next page
                line_index += len(page_lines)
                
                # Add the page text to the full document text
                full_text += page_text
                
            doc.close()

        except Exception as e:
            logger.error(f"Error extracting text with page tracking: {str(e)}")
            
        return full_text, line_to_page_map
    
    def extract_metadata(self, file_path: str) -> PDFMetadata:
        """
        Extract metadata from a PDF file.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            PDFMetadata: Extracted metadata
        """
        metadata = PDFMetadata()
        
        try:
            doc = fitz.open(file_path)
            metadata.page_count = doc.page_count
            
            # Extract standard metadata
            meta = doc.metadata
            if meta:
                metadata.title = meta.get("title", None)
                metadata.author = meta.get("author", None)
                metadata.subject = meta.get("subject", None)
                metadata.keywords = meta.get("keywords", "").split(",") if meta.get("keywords") else []
                metadata.creation_date = meta.get("creationDate", None)
                metadata.modification_date = meta.get("modDate", None)
            
            # Extract all text to estimate word count
            full_text = ""
            for page in doc:
                full_text += page.get_text()
                
            metadata.word_count = estimate_word_count(full_text)
            doc.close()
            
        except Exception as e:
            logger.error(f"Error extracting metadata with PyMuPDF: {str(e)}")
                
        return metadata
    
    def extract_possible_headers(self, text: str) -> List[str]:
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
    
    def identify_section_boundaries(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Identify section boundaries in the text.
        
        Args:
            text (str): The input text
            
        Returns:
            List[Tuple[int, int, str]]: List of (start_index, end_index, header) tuples
        """
        lines = text.split("\n")
        possible_headers = self.extract_possible_headers(text)
        
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

    def identify_sections(self, text: str, line_to_page_map: Dict[int, int]) -> List[PDFSection]:
        """
        Identify and extract sections from the text with page numbers.
        
        Args:
            text (str): The text extracted from the PDF
            line_to_page_map (Dict[int, int]): Mapping from line indices to page numbers
            
        Returns:
            List[PDFSection]: List of identified sections with accurate page numbers
        """
        sections = []
        lines = text.split("\n")
        
        # Use existing function to identify section boundaries
        boundaries = self.identify_section_boundaries(text)
        
        # Create section objects with accurate page numbers
        for i, (start_idx, end_idx, header) in enumerate(boundaries):
            # Extract section content
            section_lines = lines[start_idx:end_idx+1]
            section_content = "\n".join(section_lines)
            
            # Get the page number for this section from our mapping
            page_number = line_to_page_map.get(start_idx, 0)
            
            # Determine header level - simple approach based on header existence
            # Could be expanded in the future to use more sophisticated detection
            level = 0 if not header else 1
            
            # Create section object
            section = PDFSection(
                title=header if header else f"Section {i+1}",
                content=clean_text(section_content),
                level=level,
                page_number=page_number
            )
            
            sections.append(section)
        
        return sections
    
    def parse_pdf(self, file_path: str, filename: str) -> PDFDocument:
        """
        Parse a PDF file and extract text, metadata, and structure with page tracking.
        
        Args:
            file_path (str): Path to the PDF file
            filename (str): Original filename
            
        Returns:
            PDFDocument: Processed PDF document
        """
        # Extract text with page tracking
        text, line_to_page_map = self.extract_text_pages(file_path)
        
        # Clean the extracted text (but keep a copy of the original for section identification)
        cleaned_text = clean_text(text)
        
        # Extract metadata
        metadata = self.extract_metadata(file_path)
        
        # Identify sections with page information
        sections = self.identify_sections(text, line_to_page_map)
        
        # Create document object
        document = PDFDocument(
            filename=filename,
            metadata=metadata,
            sections=sections,
            raw_text=cleaned_text
        )
        
        return document