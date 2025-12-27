"""
IBM Research Blog Scraper
Uses RSS feed from https://research.ibm.com/rss
"""
from typing import List, Dict
from .rss_scraper import RSScraper, logger


class IBMResearchScraper(RSScraper):
    """Scraper for IBM Research blog via RSS feed"""

    def fetch(self) -> List[Dict]:
        """
        Fetch articles from IBM Research RSS feed.

        The RSS feed includes:
        - title: Article title
        - link: Full article URL
        - pubDate: Publication date
        - description: Article summary
        - category: Multiple topic tags (e.g., AI, Quantum, News, Research)

        Returns:
            List[Dict]: List of normalized article dictionaries
        """
        try:
            logger.info(f"Fetching news from {self.source_name}...")

            # Parse RSS feed using parent class method
            articles = super().fetch()

            # IBM Research RSS is well-structured, so no additional processing needed
            # The parent RSScraper class handles all standard RSS fields

            logger.info(f"Found {len(articles)} articles from {self.source_name}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []
