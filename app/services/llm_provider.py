from abc import ABC, abstractmethod
from typing import Dict, List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers, if further developed to not use just Gemini.
    
    This class defines the interface that all LLM providers must implement,
    allowing for easy switching between different LLM services in the future.
    """
    
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text based on a prompt.
        
        Args:
            prompt (str): The input prompt
            **kwargs: Additional parameters for the model
            
        Returns:
            str: Generated text
        """
        pass
    
    @abstractmethod
    async def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate a response based on a conversation history.
        
        Args:
            messages (List[Dict[str, str]]): List of messages in the conversation
            **kwargs: Additional parameters for the model
            
        Returns:
            str: Generated response
        """
        pass


class GoogleGeminiProvider(LLMProvider):
    """
    Google Gemini LLM provider implementation. Inherits the LLMProvider abstract class and uses settings from the core config.
    """
    
    def __init__(self):
        """
        Initialize the Google Gemini provider.
        """
        settings = get_settings()
        
        # Initialize LangChain Gemini client
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GOOGLE_MODEL_NAME,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            top_p=settings.LLM_TOP_P,
            max_output_tokens=settings.LLM_MAX_TOKENS,
        )
    
    async def generate_text(self, prompt: str) -> str:
        """
        Generate text using Google Gemini.
        
        Args:
            prompt (str): The input prompt
            
        Returns:
            str: Generated text
        """
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating text with Google Gemini: {str(e)}")
            return f"Error generating text: {str(e)}"
    
    async def generate_chat_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response using Google Gemini chat mode.
        
        Args:
            messages (List[Dict[str, str]]): List of messages
                Each message should have 'role' (system, user) and 'content' fields
            
        Returns:
            str: Generated response
        """
        try:
            # Convert the messages to LangChain format
            langchain_messages = []
            for message in messages:
                if message["role"] == "system":
                    langchain_messages.append(SystemMessage(content=message["content"]))
                elif message["role"] in ["user", "human"]:
                    langchain_messages.append(HumanMessage(content=message["content"]))
            
            response = self.llm.invoke(langchain_messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating chat response with Google Gemini: {str(e)}")
            return f"Error generating response: {str(e)}"


class LLMProviderFactory:
    """
    Factory class for creating LLM provider instances.
    
    This class provides a centralized way to create instances of different
    LLM providers based on configuration settings.
    """
    
    @staticmethod
    def get_provider(provider_name: str = None) -> LLMProvider:
        """
        Get an instance of an LLM provider.
        
        Args:
            provider_name (str, optional): Name of the provider to use.
                If None, the default provider from settings will be used.
                
        Returns:
            LLMProvider: An instance of the specified LLM provider
            
        Raises:
            ValueError: If the specified provider is not supported
        """
        settings = get_settings()
        
        # If no provider name is specified, use the default from settings
        if provider_name is None:
            provider_name = settings.DEFAULT_LLM_PROVIDER
        
        # Create the appropriate provider based on the name
        if provider_name.lower() in ["gemini", "google", "google_gemini"]:
            return GoogleGeminiProvider()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")