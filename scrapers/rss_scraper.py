"""
RSS Feed Scraper
"""
import feedparser
from typing import List, Dict
from datetime import datetime
from .base import BaseScraper, logger


class RSScraper(BaseScraper):
    """Scraper for RSS feeds"""

    def fetch(self) -> List[Dict]:
        """Fetch articles from RSS feed"""
        try:
            logger.info(f"Fetching RSS feed from {self.source_name}...")

            # Parse the feed
            feed = feedparser.parse(self.url, agent=self.user_agent)

            if feed.bozo:
                logger.warning(f"Feed parsing warning for {self.source_name}: {feed.bozo_exception}")

            articles = []
            for entry in feed.entries:
                article = self._parse_entry(entry)
                if article:
                    articles.append(self.normalize_article(article))

            logger.info(f"Found {len(articles)} articles from {self.source_name}")
            self.wait()

            return articles

        except Exception as e:
            logger.error(f"Error fetching RSS from {self.source_name}: {e}")
            return []

    def _parse_entry(self, entry) -> Dict:
        """Parse a single RSS entry"""
        try:
            # Extract date
            date_str = ''
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                date_str = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                date_str = datetime(*entry.updated_parsed[:6]).strftime('%Y-%m-%d')

            # Extract categories
            categories = []
            if hasattr(entry, 'tags'):
                categories = [tag.term for tag in entry.tags]

            # Extract author
            author = ''
            if hasattr(entry, 'author'):
                author = entry.author
            elif hasattr(entry, 'authors') and entry.authors:
                author = ', '.join([a.get('name', '') for a in entry.authors])

            return {
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'date': date_str,
                'summary': entry.get('summary', ''),
                'author': author,
                'categories': categories
            }
        except Exception as e:
            logger.error(f"Error parsing entry: {e}")
            return None
