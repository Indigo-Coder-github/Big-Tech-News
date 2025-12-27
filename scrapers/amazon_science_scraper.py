"""
Amazon Science RSS Scraper
"""
import html
from typing import List, Dict
from .rss_scraper import RSScraper, logger


class AmazonScienceScraper(RSScraper):
    """
    Scraper for Amazon Science blog

    Uses the RSS feed at https://www.amazon.science/index.rss

    Note: Amazon Science's robots.txt requires a 10-second crawl delay.
    This is handled by setting a higher delay in config.yaml for this source.
    """

    def normalize_article(self, article: Dict) -> Dict:
        """
        Normalize article data with HTML entity decoding for titles

        Amazon Science RSS feed contains HTML entities in titles that need decoding.
        """
        # Use parent class normalization
        normalized = super().normalize_article(article)

        # Decode HTML entities in title (e.g., &quot; -> ", &#8221; -> ")
        if normalized.get('title'):
            normalized['title'] = html.unescape(normalized['title'])

        return normalized

    def fetch(self) -> List[Dict]:
        """
        Fetch articles from Amazon Science RSS feed

        The base RSScraper class handles all the parsing logic.
        This implementation uses the default behavior which extracts:
        - title (with HTML entity decoding)
        - url (link)
        - date (published_parsed or updated_parsed)
        - summary (description)
        - author
        - categories (tags)

        Returns:
            List[Dict]: List of normalized article dictionaries
        """
        try:
            logger.info(f"Fetching Amazon Science articles from RSS feed...")

            # Use parent class's fetch method
            # It handles feedparser, date normalization, and error handling
            articles = super().fetch()

            logger.info(f"Successfully fetched {len(articles)} articles from Amazon Science")
            return articles

        except Exception as e:
            logger.error(f"Error fetching Amazon Science articles: {e}")
            return []
