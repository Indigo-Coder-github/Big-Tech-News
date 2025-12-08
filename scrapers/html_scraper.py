"""
HTML Scraper base class
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from .base import BaseScraper, logger


class HTMLScraper(BaseScraper):
    """Base HTML scraper with common functionality"""

    def fetch_page(self, url: Optional[str] = None) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML page"""
        target_url = url or self.url
        try:
            response = requests.get(target_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {target_url}: {e}")
            return None

    def fetch(self) -> List[Dict]:
        """Override this method in subclasses"""
        raise NotImplementedError("Subclasses must implement fetch()")
