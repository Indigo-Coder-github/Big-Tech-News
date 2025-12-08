"""
Microsoft AI News scraper
Scrapes AI-related articles from Microsoft's news portal
"""

from typing import List, Dict
from .html_scraper import HTMLScraper
from bs4 import BeautifulSoup
import re


class MicrosoftAIScraper(HTMLScraper):
    """Scraper for Microsoft AI News"""

    def __init__(self, source_name: str, url: str, user_agent: str, delay: float = 1.5):
        super().__init__(source_name, url, user_agent, delay)

    def fetch(self) -> List[Dict]:
        """Fetch articles from Microsoft AI News"""
        soup = self.fetch_page()
        if not soup:
            return []

        articles = []

        # Find all article links
        # Microsoft News uses various article card formats with different URL patterns
        # Pattern includes: /source/features/ai/, /features/ai/, /canada/features/ai/, etc.
        article_links = soup.find_all('a', href=re.compile(r'/features/ai/'))

        seen_urls = set()

        for link in article_links:
            try:
                url = link.get('href', '')

                # Skip if we've already processed this URL
                if url in seen_urls or not url:
                    continue

                # Make absolute URL
                if url.startswith('/'):
                    url = f"https://news.microsoft.com{url}"

                seen_urls.add(url)

                # Try to find title - could be in the link text or nearby heading
                title = ''

                # Look for heading elements within or near the link
                heading = link.find(['h2', 'h3', 'h4'])
                if heading:
                    title = heading.get_text(strip=True)
                else:
                    # Try getting text from the link itself
                    title = link.get_text(strip=True)

                # Skip if title is empty or too short (likely not an article)
                if not title or len(title) < 10:
                    continue

                # Try to find image for summary
                img = link.find('img')
                summary = ''
                if img:
                    summary = img.get('alt', '')

                # Try to extract date - Microsoft uses various date formats
                date = ''
                # Look for date in parent container
                parent = link.find_parent(['article', 'div'])
                if parent:
                    date_elem = parent.find('time')
                    if date_elem:
                        date = date_elem.get('datetime', '')
                        if not date:
                            date = date_elem.get_text(strip=True)

                # Normalize date format
                if date:
                    date = self._normalize_date(date)

                article = {
                    'title': title,
                    'url': url,
                    'date': date,
                    'summary': summary,
                    'author': '',
                    'categories': ['AI']
                }

                articles.append(article)

            except Exception as e:
                self.logger.warning(f"Failed to parse article: {e}")
                continue

        return [self.normalize_article(article) for article in articles]

    def _normalize_date(self, date_str: str) -> str:
        """Normalize various date formats to YYYY-MM-DD"""
        try:
            from dateutil import parser
            # Parse date string
            dt = parser.parse(date_str)
            return dt.strftime('%Y-%m-%d')
        except Exception:
            # If parsing fails, return original or empty
            return date_str if re.match(r'\d{4}-\d{2}-\d{2}', date_str) else ''
