"""
Base scraper class with common functionality
"""
from abc import ABC, abstractmethod
from typing import List, Dict
import time
import logging
import re
import html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def strip_html(text: str) -> str:
    """Remove HTML tags and clean up text"""
    if not text:
        return ''
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode all HTML entities using Python's html library
    text = html.unescape(text)
    # Remove common RSS feed artifacts
    text = re.sub(r'\s*Read Article\s*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*Read More\s*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*Continue Reading\s*$', '', text, flags=re.IGNORECASE)
    # Remove "The post ... appeared first on ..." pattern
    text = re.sub(r'The post .* appeared first on .*\.?$', '', text, flags=re.IGNORECASE)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


class BaseScraper(ABC):
    """Base class for all scrapers"""

    def __init__(self, source_name: str, url: str, user_agent: str, delay: float = 1.5):
        self.source_name = source_name
        self.url = url
        self.user_agent = user_agent
        self.delay = delay
        self.headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    @abstractmethod
    def fetch(self) -> List[Dict]:
        """Fetch and parse articles from the source"""
        pass

    def wait(self):
        """Apply rate limiting"""
        time.sleep(self.delay)

    def normalize_article(self, article: Dict) -> Dict:
        """Normalize article data to standard format"""
        # Clean summary by stripping HTML tags
        summary = strip_html(article.get('summary', ''))
        # Limit summary length to 500 characters
        if len(summary) > 500:
            summary = summary[:497] + '...'

        return {
            'source': self.source_name,
            'title': article.get('title', ''),
            'url': article.get('url', ''),
            'date': article.get('date', ''),
            'summary': summary,
            'author': article.get('author', ''),
            'categories': article.get('categories', []),
            'collected_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
