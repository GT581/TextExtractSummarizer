from abc import ABC, abstractmethod
from typing import Dict, List

from app.core.logging import get_logger

logger = get_logger(__name__)


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers, if further developed to not use just Gemini.
    
    This class defines the interface that all LLM providers must implement,
    allowing for easy switching between different LLM services in the future.
    """
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
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
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Generate a response based on a conversation history.
        
        Args:
            messages (List[Dict[str, str]]): List of messages in the conversation
            **kwargs: Additional parameters for the model
            
        Returns:
            str: Generated response
        """
        pass
