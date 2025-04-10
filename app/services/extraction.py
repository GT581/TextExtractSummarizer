import json
import os
from typing import Dict, Optional, Any

from app.models.text_extraction import (
    ExtractionType, 
    ContentSourceType,
    ExtractionRequest, 
    ExtractionResponse,
    KeyValuePair,
    Entity
)
from app.services.llm_provider import LLMProvider, LLMProviderFactory
from app.services.pdf_parser import PDFParser
from app.services.text_processor import TextProcessor
from app.services.web_scraper import WebScraper
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class TextExtractionService:
    """
    Service for extracting structured information from text.
    
    This service can extract various types of information from text sources,
    including key points, entities, and custom inputs or questions.
    """
    
    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        """
        Initialize the text extraction service.
        
        Args:
            llm_provider (Optional[LLMProvider]): LLM provider to use for extraction
        """
        self.settings = get_settings()
        self.llm_provider = llm_provider or LLMProviderFactory.get_provider()
        self.pdf_parser = PDFParser()
        self.web_scraper = WebScraper()
        self.text_processor = TextProcessor()
    
    async def extract_from_request(self, request: ExtractionRequest) -> ExtractionResponse:
        """
        Extract information based on an ExtractionRequest.
        This method routes to the appropriate specialized method based on source type.
        
        Args:
            request (ExtractionRequest): The extraction request
            
        Returns:
            ExtractionResponse: The extraction response
        """
        source_type = request.source_type
        include_context = request.include_context
        
        try:
            if source_type == ContentSourceType.TEXT:
                if not request.text:
                    raise ValueError("Text is required for TEXT source type")
                return await self.extract_from_text(
                    text=request.text, 
                    extraction_type=request.extraction_type,
                    custom_instructions=request.custom_instructions,
                    include_context=include_context
                )
                
            elif source_type == ContentSourceType.URL:
                if not request.url:
                    raise ValueError("URL is required for URL source type")
                return await self.extract_from_url(
                    url=str(request.url), 
                    extraction_type=request.extraction_type,
                    custom_instructions=request.custom_instructions,
                    include_context=include_context
                )
                
            elif source_type == ContentSourceType.PDF:
                if not request.file_path:
                    raise ValueError("File path is required for PDF source type")
                
                # Extract filename from the file path
                filename = os.path.basename(request.file_path)
                
                return await self.extract_from_pdf(
                    pdf_path=request.file_path, 
                    filename=filename,
                    extraction_type=request.extraction_type,
                    custom_instructions=request.custom_instructions,
                    include_context=include_context
                )
                
        except Exception as e:
            logger.error(f"Error processing extraction request: {str(e)}")
            raise
    
    async def extract_from_text(
        self, 
        text: str, 
        extraction_type: ExtractionType,
        custom_instructions: Optional[str] = None,
        include_context: bool = False
    ) -> ExtractionResponse:
        """
        Extract information from raw text.
        
        Args:
            text (str): The text to extract from
            extraction_type (ExtractionType): Type of extraction to perform
            custom_instructions (Optional[str]): Custom instructions for custom extraction
            include_context (bool): Whether to include context in the response
            
        Returns:
            ExtractionResponse: The extraction response
        """
        try:
            # Process text
            processed = self.text_processor.process_text(text)
            content = processed["raw_text"]
            
            # Create text context
            metadata = processed["metadata"]
            context = f"Text document, Words: {metadata.get('word_count', 'unknown')}"
            if metadata.get("title"):
                context += f", Title: {metadata['title']}"
            
            if extraction_type == ExtractionType.KEY_POINTS:
                return await self._extract_key_points(
                    content, 
                    extraction_type, 
                    ContentSourceType.TEXT, 
                    context, 
                    include_context
                )
            elif extraction_type == ExtractionType.ENTITIES:
                return await self._extract_entities(
                    content, 
                    extraction_type, 
                    ContentSourceType.TEXT, 
                    context, 
                    include_context
                )
            elif extraction_type == ExtractionType.CUSTOM:
                if not custom_instructions:
                    raise ValueError("Custom instructions are required for custom extraction")
                return await self._extract_custom(
                    content, 
                    extraction_type, 
                    ContentSourceType.TEXT, 
                    custom_instructions, 
                    context, 
                    include_context
                )
                
        except Exception as e:
            logger.error(f"Error extracting from text: {str(e)}")
            raise
    
    async def extract_from_url(
        self, 
        url: str, 
        extraction_type: ExtractionType,
        custom_instructions: Optional[str] = None,
        include_context: bool = False
    ) -> ExtractionResponse:
        """
        Extract information from a URL.
        
        Args:
            url (str): The URL to extract from
            extraction_type (ExtractionType): Type of extraction to perform
            custom_instructions (Optional[str]): Custom instructions for custom extraction
            include_context (bool): Whether to include context in the response
            
        Returns:
            ExtractionResponse: The extraction response
        """
        try:
            # Scrape content from the URL
            web_content = await self.web_scraper.scrape_url(url)
            content = web_content["content"]
            
            # Create URL context
            context = f"Scraped from URL: {url}"
            if web_content.get("title"):
                context += f", Title: {web_content['title']}"
            
            if extraction_type == ExtractionType.KEY_POINTS:
                return await self._extract_key_points(
                    content, 
                    extraction_type, 
                    ContentSourceType.URL, 
                    context, 
                    include_context
                )
            elif extraction_type == ExtractionType.ENTITIES:
                return await self._extract_entities(
                    content, 
                    extraction_type, 
                    ContentSourceType.URL, 
                    context, 
                    include_context
                )
            elif extraction_type == ExtractionType.CUSTOM:
                if not custom_instructions:
                    raise ValueError("Custom instructions are required for custom extraction")
                return await self._extract_custom(
                    content, 
                    extraction_type, 
                    ContentSourceType.URL, 
                    custom_instructions, 
                    context, 
                    include_context
                )
                
        except Exception as e:
            logger.error(f"Error extracting from URL: {str(e)}")
            raise
    
    async def extract_from_pdf(
        self, 
        pdf_path: str, 
        filename: str,
        extraction_type: ExtractionType,
        custom_instructions: Optional[str] = None,
        include_context: bool = False
    ) -> ExtractionResponse:
        """
        Extract information from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            filename (str): Original filename
            extraction_type (ExtractionType): Type of extraction to perform
            custom_instructions (Optional[str]): Custom instructions for custom extraction
            include_context (bool): Whether to include context in the response
            
        Returns:
            ExtractionResponse: The extraction response
        """
        try:
            # Parse PDF document
            document = self.pdf_parser.parse_pdf(pdf_path, filename)
            content = document.raw_text
            
            # Create PDF context
            context = f"PDF Document: {filename}, Pages: {document.metadata.page_count}"
            if document.metadata.title:
                context += f", Title: {document.metadata.title}"
            
            if extraction_type == ExtractionType.KEY_POINTS:
                return await self._extract_key_points(
                    content, 
                    extraction_type, 
                    ContentSourceType.PDF, 
                    context, 
                    include_context
                )
            elif extraction_type == ExtractionType.ENTITIES:
                return await self._extract_entities(
                    content, 
                    extraction_type, 
                    ContentSourceType.PDF, 
                    context, 
                    include_context
                )
            elif extraction_type == ExtractionType.CUSTOM:
                if not custom_instructions:
                    raise ValueError("Custom instructions are required for custom extraction")
                return await self._extract_custom(
                    content, 
                    extraction_type, 
                    ContentSourceType.PDF, 
                    custom_instructions, 
                    context, 
                    include_context
                )
                
        except Exception as e:
            logger.error(f"Error extracting from PDF: {str(e)}")
            raise

    def _parse_json_response(self, response_text: str, default_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse LLM response as JSON.
        
        Args:
            response_text (str): Response text from LLM
            default_structure (Dict[str, Any]): Default structure to return if parsing fails
            
        Returns:
            Dict[str, Any]: Parsed JSON data
        """
        try:

            return json.loads(response_text)
        
        except json.JSONDecodeError:                    
            logger.warning("No valid JSON structure found in response")

            return default_structure

    def _create_key_points_prompt(self, text: str) -> str:
        """
        Create a prompt for extracting key points.
        
        Args:
            text (str): The source text
            
        Returns:
            str: The prompt
        """
        max_tokens = self.settings.LLM_MAX_TOKENS
        return f"""
        Extract the most important key points from the following text.
        Format your response as a JSON array of key-value pairs, where the key is the point name or category, 
        and the value is the specific information.

        For each key point:
        1. Identify the category or type of information
        2. Extract the specific detail, fact, or statistic
        3. Ensure accuracy and preserve the original meaning

        IMPORTANT: Your response must be a valid JSON object only, with NO explanatory text before or after.
        Do NOT include markdown code block syntax (```json) or any other formatting.  THIS IS IMPORTANT.
        Do NOT use newlines or pretty-printing in your JSON - format it as a compact, single-line JSON object.
        Just return the raw JSON object without any whitespace between properties.

        TOKEN LIMIT: Your response MUST be under {max_tokens} tokens. If you have too many key points, 
        prioritize the most important ones and limit the total to stay under this token limit.

        Format your response like this (but without any newlines):
        {{"key_points":[{{"key":"Market Share","value":"Increased from 24% to 28% year-over-year"}}]}}

        The text to analyze:
        {text}
        """
    
    def _create_entities_prompt(self, text: str) -> str:
        """
        Create a prompt for extracting entities.
        
        Args:
            text (str): The source text
            
        Returns:
            str: The prompt
        """
        max_tokens = self.settings.LLM_MAX_TOKENS
        return f"""
        Extract named entities from the following text.
        Format your response as a JSON array of entities, where each entity has a name, type, and list of mentions.

        Entity types to identify:
        - Person (individuals mentioned by name)
        - Organization (companies, agencies, institutions)
        - Location (countries, cities, geographic locations)
        - Product (products, services, brands)
        - Event (specific events or occurrences)
        - Date (specific dates or time periods)

        IMPORTANT: Your response must be a valid JSON object only, with NO explanatory text before or after.
        Do NOT include markdown code block syntax (```json) or any other formatting. THIS IS IMPORTANT.
        Do NOT use newlines or pretty-printing in your JSON - format it as a compact, single-line JSON object.
        Just return the raw JSON object without any whitespace between properties.

        TOKEN LIMIT: Your response MUST be under {max_tokens} tokens. If you have too many entities, 
        prioritize the most important ones and limit the total to stay under this token limit.

        Format your response like this (but without any newlines):
        {{"entities":[{{"name":"Microsoft","type":"Organization","mentions":["Microsoft","MSFT","the company"]}}]}}

        The text to analyze:
        {text}
        """
    
    def _create_custom_prompt(self, text: str, custom_instructions: str) -> str:
        """
        Create a custom extraction prompt.
        
        Args:
            text (str): The source text
            custom_instructions (str): Custom extraction instructions
            
        Returns:
            str: The prompt
        """
        max_tokens = self.settings.LLM_MAX_TOKENS
        return f"""
        You are an expert AI trained to extract specific information from text based on custom instructions.
        Your task is to extract information according to the following instructions:

        {custom_instructions}

        IMPORTANT: Your response must be a valid JSON object only, with NO explanatory text before or after.
        Do NOT include markdown code block syntax (```json) or any other formatting. THIS IS IMPORTANT.
        Do NOT use newlines or pretty-printing in your JSON - format it as a compact, single-line JSON object.
        Just return the raw JSON object without any whitespace between properties.

        TOKEN LIMIT: Your response MUST be under {max_tokens} tokens. If you have too much information, 
        prioritize what is most important relative to the instructions and limit the total to stay under this token limit.

        Example of correct format (but with your extracted content):
        {{"data":{{"key1":"value1","key2":"value2","items":[{{"id":1,"name":"Item 1"}},{{"id":2,"name":"Item 2"}}]}}}}

        Ensure all extracted information is accurate and directly supported by the text.

        The text to analyze:
        {text}
        """
    
    async def _extract_key_points(
        self, 
        text: str, 
        extraction_type: ExtractionType,
        source_type: ContentSourceType,
        context: Optional[str],
        include_context: bool
    ) -> ExtractionResponse:
        """
        Extract key points from text.
        
        Args:
            text (str): The source text
            extraction_type (ExtractionType): Type of extraction
            source_type (ContentSourceType): Type of source
            context (Optional[str]): Context information
            include_context (bool): Whether to include context in the response
            
        Returns:
            ExtractionResponse: The extraction response
        """
        try:
            prompt = self._create_key_points_prompt(text)
            
            response_text = await self.llm_provider.generate_text(prompt)
            
            default_structure = {"key_points": []}
            response_data = self._parse_json_response(response_text, default_structure)

            # Create key-value pairs
            key_value_pairs = []
            for point in response_data.get("key_points", []):
                pair = KeyValuePair(
                    key=point.get("key", ""),
                    value=point.get("value", "")
                )
                key_value_pairs.append(pair)
            
            return ExtractionResponse(
                success=True,
                extraction_type=extraction_type,
                source_type=source_type,
                key_value_pairs=key_value_pairs,
                #data=response_data,
                context=context if include_context else None
            )
        except Exception as e:
            logger.error(f"Error extracting key points: {str(e)}")
            return ExtractionResponse(
                success=False,
                extraction_type=extraction_type,
                source_type=source_type,
                context=f"Error extracting key points: {str(e)}"
            )
    
    async def _extract_entities(
        self, 
        text: str, 
        extraction_type: ExtractionType,
        source_type: ContentSourceType,
        context: Optional[str],
        include_context: bool
    ) -> ExtractionResponse:
        """
        Extract entities from text.
        
        Args:
            text (str): The source text
            extraction_type (ExtractionType): Type of extraction
            source_type (ContentSourceType): Type of source
            context (Optional[str]): Context information
            include_context (bool): Whether to include context in the response
            
        Returns:
            ExtractionResponse: The extraction response
        """
        try:
            prompt = self._create_entities_prompt(text)
            
            response_text = await self.llm_provider.generate_text(prompt)
            
            default_structure = {"entities": []}
            response_data = self._parse_json_response(response_text, default_structure)

            # Create entities
            entities = []
            for entity_data in response_data.get("entities", []):
                entity = Entity(
                    name=entity_data.get("name", ""),
                    type=entity_data.get("type", ""),
                    mentions=entity_data.get("mentions", []) #TODO: Improve mentioned context
                )
                entities.append(entity)
            
            return ExtractionResponse(
                success=True,
                extraction_type=extraction_type,
                source_type=source_type,
                entities=entities,
                #data=response_data,
                context=context if include_context else None
            )
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return ExtractionResponse(
                success=False,
                extraction_type=extraction_type,
                source_type=source_type,
                context=f"Error extracting entities: {str(e)}"
            )
    
    async def _extract_custom(
        self, 
        text: str, 
        extraction_type: ExtractionType,
        source_type: ContentSourceType,
        custom_instructions: str,
        context: Optional[str],
        include_context: bool
    ) -> ExtractionResponse:
        """
        Perform custom extraction based on instructions.
        
        Args:
            text (str): The source text
            extraction_type (ExtractionType): Type of extraction
            source_type (ContentSourceType): Type of source
            custom_instructions (str): Custom extraction instructions
            context (Optional[str]): Context information
            include_context (bool): Whether to include context in the response
            
        Returns:
            ExtractionResponse: The extraction response
        """
        try:
            prompt = self._create_custom_prompt(text, custom_instructions)
            
            response_text = await self.llm_provider.generate_text(prompt)
            
            default_structure = {"data": response_text}
            response_data = self._parse_json_response(response_text, default_structure)

            return ExtractionResponse(
                success=True,
                extraction_type=extraction_type,
                source_type=source_type,
                data=response_data,
                context=context if include_context else None
            )
        except Exception as e:
            logger.error(f"Error performing custom extraction: {str(e)}")
            return ExtractionResponse(
                success=False,
                extraction_type=extraction_type,
                source_type=source_type,
                context=f"Error performing custom extraction: {str(e)}"
            ) 