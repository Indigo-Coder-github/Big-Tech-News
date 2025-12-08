"""
Meta AI Blog Scraper
"""
from typing import List, Dict
import re
from datetime import datetime
from .html_scraper import HTMLScraper, logger


class MetaScraper(HTMLScraper):
    """Scraper for Meta AI blog"""

    # Month name to number mapping
    MONTHS = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    def fetch(self) -> List[Dict]:
        """Fetch articles from Meta AI blog"""
        try:
            logger.info(f"Fetching blog posts from {self.source_name}...")

            soup = self.fetch_page()
            if not soup:
                return []

            articles = []
            seen_urls = set()

            # Date pattern: "Month DD, YYYY"
            date_pattern = re.compile(
                r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'
            )

            # Find all date elements and extract articles from their containers
            for date_elem in soup.find_all(string=date_pattern):
                try:
                    date_text = date_elem.strip()
                    article = self._extract_article_from_date(date_elem, date_text, date_pattern)

                    if article and article['url'] and article['url'] not in seen_urls:
                        if article['title'] and len(article['title']) > 15:
                            seen_urls.add(article['url'])
                            articles.append(self.normalize_article(article))
                except Exception:
                    continue

            # Remove duplicates by URL while preserving order
            unique_articles = []
            seen = set()
            for article in articles:
                if article['url'] not in seen:
                    seen.add(article['url'])
                    unique_articles.append(article)

            logger.info(f"Found {len(unique_articles)} articles from {self.source_name}")
            self.wait()

            return unique_articles[:30]  # Limit to 30 most recent

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []

    def _extract_article_from_date(self, date_elem, date_text: str, date_pattern) -> Dict:
        """Extract article info by traversing up from a date element"""
        article = {
            'title': '',
            'url': '',
            'date': self._parse_date(date_text),
            'summary': '',
            'categories': [],
            'author': ''
        }

        # Traverse up to find container with blog link
        container = date_elem.parent
        for _ in range(10):
            if container is None or container.name == 'body':
                break
            container = container.parent
            if container:
                # Look for blog link
                link = container.find('a', href=re.compile(r'/blog/[a-z0-9-]+/?$'))
                if link:
                    url = link.get('href', '')
                    if url and not url.startswith('http'):
                        url = f"https://ai.meta.com{url}"
                    article['url'] = url

                    # Extract title from container text
                    all_text = container.get_text(separator='|', strip=True)
                    parts = [
                        p.strip() for p in all_text.split('|')
                        if len(p.strip()) > 20
                        and 'FEATURED' not in p.upper()
                        and not date_pattern.search(p)
                        and not p.startswith('더 알아보기')
                        and '→' not in p
                    ]
                    if parts:
                        article['title'] = parts[0]
                    break

        return article

    def _parse_date(self, date_text: str) -> str:
        """Parse 'Month DD, YYYY' format to 'YYYY-MM-DD'"""
        try:
            match = re.match(
                r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})',
                date_text
            )
            if match:
                month = self.MONTHS[match.group(1)]
                day = match.group(2).zfill(2)
                year = match.group(3)
                return f"{year}-{month}-{day}"
        except Exception:
            pass
        return ''
