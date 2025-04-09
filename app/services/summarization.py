from typing import Optional, Dict, Any
import os

from app.models.summarization import SummarizationRequest, SummarizationResponse
from app.models.text_extraction import ContentSourceType
from app.services.llm_provider import LLMProvider, LLMProviderFactory
from app.services.pdf_parser import PDFParser
from app.services.text_processor import TextProcessor
from app.services.web_scraper import WebScraper
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class SummarizationService:
    """
    Service for using LLMs to generate summaries of text extracted from various sources.
    """
    
    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        """
        Initialize the summarization service with dependencies.
        
        Args:
            llm_provider (Optional[LLMProvider]): LLM provider instance (if None, default will be used)
        """
        self.settings = get_settings()
        self.llm_provider = llm_provider or LLMProviderFactory.get_provider()
        self.pdf_parser = PDFParser()
        self.text_processor = TextProcessor()
        self.web_scraper = WebScraper()

    def create_prompt(self, content: str, metadata: Dict[str, Any], max_length: int) -> str:
        """
        Create a summarization prompt for the LLM.
        
        Args:
            content (str): The content to summarize
            metadata (Dict[str, Any]): Content metadata
            max_length (int): Target summary length in words
            
        Returns:
            str: The prompt for the LLM
        """
        # Extract title and content type
        title = metadata.get("title", "")
        source_type = metadata.get("source_type", "content")
        
        # Create prompt header
        header = f"Please summarize the following {source_type} content"
        if title:
            header += f" titled '{title}'"
        header += f" in approximately {max_length} words.\n\n"
        
        # Add metadata context
        context = "Content Information:\n"
        for key, value in metadata.items():
            if value and key not in ["raw_text", "content", "text"]:
                context += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        # Add summarization guidelines
        guidelines = """
        Please provide a summary that:
        1. Captures the main ideas and key points
        2. Preserves important details and facts
        3. Maintains a logical flow
        4. Uses objective language
        5. Is concise but comprehensive
        """
        
        # Combine all parts for final prompt
        prompt = f"{header}{context}\n{guidelines}\n\nContent to summarize:\n{content}"

        return prompt
    
    async def summarize_text(self, text: str, max_length: Optional[int] = None, include_metadata: bool = True) -> SummarizationResponse:
        """
        Summarize plain text content.
        
        Args:
            text (str): The text to summarize
            max_length (Optional[int]): Target summary length in words
            include_metadata (bool): Whether to include metadata in the response
            
        Returns:
            SummarizationResponse: The summarization response
        """
        try:
            max_length = max_length or self.settings.DEFAULT_MAX_SUMMARY_LENGTH
            
            # Process the text using the text processor
            processed = self.text_processor.process_text(text)
            content = processed["raw_text"]
            
            # Create metadata dictionary
            metadata = processed["metadata"]
            metadata["source_type"] = ContentSourceType.TEXT.value
            
            # Create prompt and generate summary
            prompt = self.create_prompt(content, metadata, max_length)
            summary = await self.llm_provider.generate_text(prompt)
            
            # Create response
            return SummarizationResponse(
                summary=summary,
                word_count=len(summary.split()),
                title=metadata.get("title"),
                metadata=metadata if include_metadata else None
            )
            
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            raise

    async def summarize_url(self, url: str, max_length: Optional[int] = None, include_metadata: bool = True) -> SummarizationResponse:
        """
        Summarize content from a URL.
        
        Args:
            url (str): The URL to summarize
            max_length (Optional[int]): Target summary length in words
            include_metadata (bool): Whether to include metadata in the response
            
        Returns:
            SummarizationResponse: The summarization response
        """
        try:
            max_length = max_length or self.settings.DEFAULT_MAX_SUMMARY_LENGTH
            
            # Scrape content from the URL
            web_content = await self.web_scraper.scrape_url(url)
            
            # Create metadata dictionary
            metadata = {
                "title": web_content["title"],
                "url": url,
                "source_type": ContentSourceType.URL.value,
                "word_count": web_content["word_count"]
            }
            
            # Create prompt and generate summary
            prompt = self.create_prompt(web_content["content"], metadata, max_length)
            summary = await self.llm_provider.generate_text(prompt)
            
            # Create response
            return SummarizationResponse(
                summary=summary,
                word_count=len(summary.split()),
                title=web_content["title"],
                metadata=metadata if include_metadata else None
            )
            
        except Exception as e:
            logger.error(f"Error summarizing URL: {str(e)}")
            raise

    async def summarize_pdf(self, pdf_path: str, filename: str, max_length: Optional[int] = None, include_metadata: bool = True) -> SummarizationResponse:
        """
        Summarize content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            filename (str): Original filename
            max_length (Optional[int]): Target summary length in words
            include_metadata (bool): Whether to include metadata in the response
            
        Returns:
            SummarizationResponse: The summarization response
        """
        try:
            max_length = max_length or self.settings.DEFAULT_MAX_SUMMARY_LENGTH
            
            # Parse PDF document
            document = self.pdf_parser.parse_pdf(pdf_path, filename)
            
            # Create metadata dictionary
            metadata = {
                "title": document.metadata.title,
                "author": document.metadata.author,
                "page_count": document.metadata.page_count,
                "word_count": document.metadata.word_count
            }
            
            # Add section info if available
            if document.sections:
                section_titles = [s.title for s in document.sections if s.title]
                if section_titles:
                    metadata["sections"] = ", ".join(section_titles)
            
            # Create prompt and generate summary
            prompt = self.create_prompt(document.raw_text, metadata, max_length)
            summary = await self.llm_provider.generate_text(prompt)
            
            # Create response
            return SummarizationResponse(
                summary=summary,
                word_count=len(summary.split()),
                title=document.metadata.title,
                metadata=metadata if include_metadata else None
            )
            
        except Exception as e:
            logger.error(f"Error summarizing PDF: {str(e)}")
            raise

    async def summarize_from_request(self, request: SummarizationRequest) -> SummarizationResponse:
        """
        Generate summary based on a SummarizationRequest.
        This method routes to the appropriate specialized method based on source type.
        
        Args:
            request (SummarizationRequest): The summarization request
            
        Returns:
            SummarizationResponse: The summarization response
        """
        source_type = request.source_type
        max_length = request.max_length
        include_metadata = request.include_metadata
        
        try:
            if source_type == ContentSourceType.TEXT:
                if not request.text:
                    raise ValueError("Text is required for TEXT source type")
                
                return await self.summarize_text(request.text, max_length, include_metadata)
                
            elif source_type == ContentSourceType.URL:
                if not request.url:
                    raise ValueError("URL is required for URL source type")
                
                return await self.summarize_url(str(request.url), max_length, include_metadata)
                
            elif source_type == ContentSourceType.PDF:
                if not request.file_path:
                    raise ValueError("File path is required for PDF source type")
                
                # Extract filename from the file path
                filename = os.path.basename(request.file_path)
                
                return await self.summarize_pdf(request.file_path, filename, max_length, include_metadata)
                
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
                
        except Exception as e:
            logger.error(f"Error processing summarization request: {str(e)}")
            raise