"""
Microsoft AI News RSS Scraper with AI Content Filtering
Scrapes AI-related articles from Microsoft's news RSS feed
"""
from typing import List, Dict
from .rss_scraper import RSScraper, logger


class MicrosoftAINewsScraper(RSScraper):
    """
    RSS scraper for Microsoft AI News with AI content filtering

    Uses the RSS feed at https://news.microsoft.com/source/feed/
    and filters for AI-related content based on categories and keywords.

    Robots.txt status: Allowed (10-second crawl-delay recommended)
    URL redirect: blogs.microsoft.com/ai/ -> news.microsoft.com/source/topics/ai/
    """

    # AI-related keywords for filtering
    AI_KEYWORDS = [
        'ai', 'artificial intelligence', 'machine learning', 'ml',
        'deep learning', 'neural network', 'copilot', 'chatgpt',
        'large language model', 'llm', 'generative ai', 'gen ai',
        'computer vision', 'natural language', 'nlp', 'gpt',
        'azure ai', 'cognitive services', 'openai', 'agi'
    ]

    def fetch(self) -> List[Dict]:
        """
        Fetch and filter AI-related articles from Microsoft News RSS feed

        The base RSScraper class handles RSS parsing. This implementation
        adds filtering logic to keep only AI-related content.

        Returns:
            List[Dict]: List of normalized AI-related article dictionaries
        """
        try:
            logger.info(f"Fetching RSS feed from {self.source_name}...")

            # Use parent class's fetch method to get all articles
            all_articles = super().fetch()

            # Filter for AI-related content
            ai_articles = []
            for article in all_articles:
                if self._is_ai_related(article):
                    ai_articles.append(article)

            logger.info(f"Found {len(ai_articles)} AI-related articles from {self.source_name} "
                       f"(filtered from {len(all_articles)} total)")

            return ai_articles

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []

    def _is_ai_related(self, article: Dict) -> bool:
        """
        Check if an article is AI-related based on categories, title, and summary

        Args:
            article: Normalized article dictionary

        Returns:
            bool: True if article is AI-related, False otherwise
        """
        # Check categories first (most reliable)
        categories = article.get('categories', [])
        if categories:
            # Convert categories to lowercase for comparison
            categories_lower = [cat.lower() for cat in categories]

            # Check if 'AI' is explicitly in categories
            if 'ai' in categories_lower or 'artificial intelligence' in categories_lower:
                return True

        # Check title and summary for AI keywords
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        combined_text = f"{title} {summary}"

        # Check if any AI keyword appears in title or summary
        for keyword in self.AI_KEYWORDS:
            if keyword in combined_text:
                return True

        return False
