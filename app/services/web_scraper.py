import requests
from typing import Dict, Any
from bs4 import BeautifulSoup
from fastapi import HTTPException

from app.core.logging import get_logger
from app.utils.text_utils import clean_html_text

logger = get_logger(__name__)


class WebScraper:
    """
    Utility for scraping and parsing text content from websites.
    Extracts and cleans text content for LLM processing.
    """
    
    def __init__(self):
        """
        Initialize the web scraper with standard headers.
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

    def scrape_url(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Scrape, clean, and return content from a URL with metadata.
        
        Args:
            url (str): The URL to scrape
            timeout (int): Request timeout in seconds
            
        Returns:
            Dict[str, Any]: Dictionary with content, title, URL, and word count
            
        Raises:
            HTTPException(408): When the request times out
            HTTPException(400): When the URL is invalid or returns a client error
            HTTPException(500): When the URL returns a server error
        """
        try:
            logger.info(f"Scraping URL: {url}")
            
            # Make request to URL
            response = requests.get(url, timeout=timeout, headers=self.headers)
            response.raise_for_status()  # Trigger the requests exception
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else url
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.extract()
            
            # Remove common noise elements
            for element in soup.select('nav, header, footer, aside, .ads, .comments, .navigation, .menu'):
                element.extract()
            
            # Get text content
            content = soup.get_text(separator=' ', strip=True)
            
            # Clean the text
            cleaned_content = clean_html_text(content)
            
            # Calculate word count
            word_count = len(cleaned_content.split())
            
            logger.info(f"Successfully scraped URL: {url}")
            
            # Return formatted response
            return {
                "content": cleaned_content,
                "title": title,
                "url": url,
                "word_count": word_count
            }
            
        except requests.Timeout:
            logger.error(f"Timeout error fetching URL: {url}")
            raise HTTPException(status_code=408, detail=f"Request timeout while fetching URL")
        
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error parsing content from URL {url}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")


# Optional wrapper function for direct scraper usage
def scrape_url(url: str) -> Dict[str, Any]:
    """
    Scrape content from a URL and return as a dictionary with metadata.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        Dict[str, Any]: Dictionary with content, title, URL, and word count
    """
    scraper = WebScraper()

    return scraper.scrape_url(url)