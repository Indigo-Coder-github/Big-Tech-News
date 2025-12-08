"""
Google DeepMind Publications Scraper
"""
from typing import List, Dict
import re
from .html_scraper import HTMLScraper, logger


class DeepMindScraper(HTMLScraper):
    """Scraper for Google DeepMind publications"""

    # Month name to number mapping
    MONTHS = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    def fetch(self) -> List[Dict]:
        """Fetch publications from DeepMind research page"""
        try:
            logger.info(f"Fetching publications from {self.source_name}...")

            soup = self.fetch_page()
            if not soup:
                return []

            articles = []
            seen_urls = set()

            # Date pattern: "DD Month YYYY" (e.g., "30 October 2025")
            date_pattern = re.compile(
                r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})'
            )

            # Find publication links - now using slug-based URLs
            pub_links = soup.find_all('a', href=re.compile(r'/research/publications/[a-z0-9-]+/?$'))

            for link in pub_links[:50]:
                try:
                    url = link.get('href', '')

                    # Skip generic links
                    if not url or url in seen_urls:
                        continue
                    if url.endswith('/publications/') or url.endswith('/publications'):
                        continue
                    if 'learn more' in link.get_text(strip=True).lower():
                        continue

                    # Get full text which includes date and title
                    text = link.get_text(strip=True)

                    # Skip short or non-article text
                    if not text or len(text) < 15:
                        continue

                    # Extract date from text
                    date_str = ''
                    date_match = date_pattern.search(text)
                    if date_match:
                        day = date_match.group(1).zfill(2)
                        month = self.MONTHS[date_match.group(2)]
                        year = date_match.group(3)
                        date_str = f"{year}-{month}-{day}"

                        # Remove date from text to get title
                        title = date_pattern.sub('', text).strip()
                    else:
                        title = text

                    if not title or len(title) < 10:
                        continue

                    seen_urls.add(url)

                    # Normalize URL
                    if not url.startswith('http'):
                        url = f"https://deepmind.google{url}"

                    articles.append(self.normalize_article({
                        'title': title,
                        'url': url,
                        'date': date_str,
                        'summary': '',
                        'categories': ['Research'],
                        'author': ''
                    }))

                except Exception as e:
                    logger.warning(f"Error parsing DeepMind publication: {e}")
                    continue

            logger.info(f"Found {len(articles)} articles from {self.source_name}")
            self.wait()

            return articles[:30]

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []
