"""
Anthropic News Scraper
"""
from typing import List, Dict
import re
from datetime import datetime
from .html_scraper import HTMLScraper, logger


class AnthropicScraper(HTMLScraper):
    """Scraper for Anthropic news page"""

    # Month abbreviation to number mapping
    MONTHS = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    def fetch(self) -> List[Dict]:
        """Fetch articles from Anthropic news page"""
        try:
            logger.info(f"Fetching news from {self.source_name}...")

            soup = self.fetch_page()
            if not soup:
                return []

            articles = []
            seen_urls = set()

            # Date pattern: "Mon DD, YYYY" (e.g., "Nov 24, 2025")
            date_pattern = re.compile(
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}'
            )

            # Find all news article links
            news_links = soup.find_all('a', href=re.compile(r'^/news/[a-z0-9-]+$'))

            for link in news_links:
                try:
                    url = link.get('href', '')
                    if not url or url in seen_urls:
                        continue

                    # Parse text parts from link content
                    text = link.get_text(separator='|', strip=True)
                    parts = [p.strip() for p in text.split('|') if p.strip()]

                    if not parts:
                        continue

                    # Extract date
                    date_str = ''
                    for part in parts:
                        if date_pattern.search(part):
                            date_str = self._parse_date(part)
                            break

                    # Extract title and category
                    title = ''
                    category = ''
                    summary = ''

                    # Filter out date parts
                    non_date_parts = [p for p in parts if not date_pattern.search(p)]

                    # Known category names
                    known_categories = [
                        'Announcements', 'Product', 'Policy', 'Research',
                        'Company', 'Safety', 'Economic Research', 'Core Views'
                    ]

                    if len(non_date_parts) >= 2:
                        # Determine which part is category vs title
                        first_is_category = (
                            non_date_parts[0] in known_categories or
                            (len(non_date_parts[0]) < 25 and non_date_parts[0][0].isupper() and
                             not non_date_parts[0].startswith('Introducing') and
                             not non_date_parts[0].startswith('Anthropic'))
                        )

                        if first_is_category:
                            category = non_date_parts[0]
                            title = non_date_parts[1]
                            if len(non_date_parts) > 2:
                                summary = non_date_parts[2]
                        else:
                            title = non_date_parts[0]
                            # Check if second part is category
                            if non_date_parts[1] in known_categories:
                                category = non_date_parts[1]
                                if len(non_date_parts) > 2:
                                    summary = non_date_parts[2]
                            else:
                                summary = non_date_parts[1]
                    elif len(non_date_parts) == 1:
                        title = non_date_parts[0]

                    if not title or len(title) < 10:
                        continue

                    seen_urls.add(url)
                    full_url = f"https://www.anthropic.com{url}"

                    articles.append(self.normalize_article({
                        'title': title,
                        'url': full_url,
                        'date': date_str,
                        'summary': summary[:300] if summary else '',
                        'categories': [category] if category else [],
                        'author': ''
                    }))

                except Exception as e:
                    logger.warning(f"Error parsing Anthropic link: {e}")
                    continue

            logger.info(f"Found {len(articles)} articles from {self.source_name}")
            self.wait()

            return articles[:30]  # Limit to 30 most recent

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []

    def _parse_date(self, date_text: str) -> str:
        """Parse 'Mon DD, YYYY' format to 'YYYY-MM-DD'"""
        try:
            match = re.search(
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+(\d{4})',
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
