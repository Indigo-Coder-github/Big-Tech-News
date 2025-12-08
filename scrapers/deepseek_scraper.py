"""
DeepSeek News Scraper
Scrapes news from https://api-docs.deepseek.com
"""

from typing import List, Dict
import re
from datetime import datetime
from .html_scraper import HTMLScraper, logger


class DeepSeekScraper(HTMLScraper):
    """Scraper for DeepSeek API Docs news"""

    def fetch(self) -> List[Dict]:
        """Fetch news from DeepSeek API documentation"""
        try:
            logger.info(f"Fetching news from {self.source_name}...")

            soup = self.fetch_page()
            if not soup:
                return []

            articles = []

            # Find all news links (format: /news/newsYYMMDD or /news/newsYYYYMMDD)
            news_links = soup.find_all('a', href=re.compile(r'/news/news\d+'))

            seen_urls = set()
            for link in news_links[:30]:  # Limit to 30
                try:
                    href = link.get('href', '')
                    if not href or href in seen_urls:
                        continue

                    seen_urls.add(href)

                    # Build full URL
                    url = f"https://api-docs.deepseek.com{href}"

                    # Extract title
                    title = link.get_text(strip=True)

                    # Skip generic "News" links
                    if title == "News" or len(title) < 5:
                        continue

                    # Extract date from URL pattern
                    # Pattern: /news/newsYYMMDD or /news/newsYYYYMMDD
                    date_str = ''
                    date_match = re.search(r'/news/news(\d+)', href)
                    if date_match:
                        date_code = date_match.group(1)
                        date_str = self._parse_date_from_code(date_code)

                    article = {
                        'title': title,
                        'url': url,
                        'date': date_str,
                        'summary': '',
                        'categories': ['News'],
                        'author': ''
                    }

                    articles.append(self.normalize_article(article))

                except Exception as e:
                    logger.warning(f"Error parsing DeepSeek news item: {e}")
                    continue

            logger.info(f"Found {len(articles)} articles from {self.source_name}")
            self.wait()

            return articles

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []

    def _parse_date_from_code(self, date_code: str) -> str:
        """
        Parse date from DeepSeek URL code
        Formats:
        - YYMMDD: 250929 -> 2025-09-29
        - YYYYMMDD: 20241226 -> 2024-12-26
        """
        try:
            # Try 8-digit format first (YYYYMMDD)
            if len(date_code) == 8:
                year = date_code[:4]
                month = date_code[4:6]
                day = date_code[6:8]
                return f"{year}-{month}-{day}"

            # Try 6-digit format (YYMMDD)
            elif len(date_code) == 6:
                year_short = date_code[:2]
                month = date_code[2:4]
                day = date_code[4:6]

                # Assume 20xx for years
                year = f"20{year_short}"
                return f"{year}-{month}-{day}"

            # Try 4-digit format (MMDD from 2024)
            elif len(date_code) == 4:
                month = date_code[:2]
                day = date_code[2:4]
                # Default to 2024 for short formats
                return f"2024-{month}-{day}"

        except Exception as e:
            logger.warning(f"Error parsing date code {date_code}: {e}")
            pass

        return ''
