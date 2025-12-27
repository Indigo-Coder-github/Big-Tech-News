"""
Baidu Research Blog Scraper
"""
from typing import List, Dict
import re
from datetime import datetime
from urllib.parse import urljoin
from .html_scraper import HTMLScraper, logger


class BaiduResearchScraper(HTMLScraper):
    """Scraper for Baidu Research blog"""

    # Month abbreviations to full names
    MONTHS = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    def fetch(self) -> List[Dict]:
        """Fetch articles from Baidu Research blog"""
        try:
            logger.info(f"Fetching blog posts from {self.source_name}...")

            soup = self.fetch_page()
            if not soup:
                return []

            articles = []
            seen_urls = set()

            # Find all blog article links
            # Pattern: <a href="/Blog/index-view?id=NUMBER">
            blog_links = soup.find_all('a', href=re.compile(r'/Blog/index-view\?id=\d+'))

            for link in blog_links:
                try:
                    # Extract URL
                    relative_url = link.get('href', '')
                    if not relative_url:
                        continue

                    url = urljoin(self.url, relative_url)

                    # Skip duplicates
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)

                    # Extract title from div with class="blog-title"
                    title_elem = link.find('div', class_='blog-title')
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)

                    # Extract summary from div with class="blog-introduce"
                    summary_elem = link.find('div', class_='blog-introduce')
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''

                    # Extract date from div with class="blog-date"
                    # Format: "Oct 28th，2024" (note: uses Chinese comma)
                    date_elem = link.find('div', class_='blog-date')
                    date_str = ''
                    if date_elem:
                        date_text = date_elem.get_text(strip=True)
                        date_str = self._parse_date(date_text)

                    # Only add if we have at least title and URL
                    if title and url:
                        article = {
                            'title': title,
                            'url': url,
                            'date': date_str,
                            'summary': summary,
                            'author': '',
                            'categories': []
                        }
                        articles.append(self.normalize_article(article))

                except Exception as e:
                    logger.debug(f"Error parsing article: {e}")
                    continue

            logger.info(f"Found {len(articles)} articles from {self.source_name}")
            self.wait()

            return articles

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []

    def _parse_date(self, date_text: str) -> str:
        """
        Parse date in format 'Oct 28th，2024' to 'YYYY-MM-DD'
        Note: Uses Chinese comma (，) instead of Western comma
        Handles ordinal suffixes: st, nd, rd, th
        """
        try:
            # Replace Chinese comma with space for easier parsing
            date_text = date_text.replace('，', ' ').replace(',', ' ')

            # Pattern: Month Day(st/nd/rd/th) Year
            # Example: "Oct 28th 2024"
            match = re.search(
                r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})',
                date_text
            )

            if match:
                month_abbr = match.group(1)
                day = match.group(2).zfill(2)
                year = match.group(3)
                month = self.MONTHS.get(month_abbr, '01')
                return f"{year}-{month}-{day}"

            # Fallback: try to parse with datetime
            # Try common formats
            for fmt in ['%b %d %Y', '%B %d %Y', '%Y-%m-%d']:
                try:
                    # Remove ordinal suffixes
                    clean_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_text)
                    dt = datetime.strptime(clean_date.strip(), fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue

        except Exception as e:
            logger.debug(f"Error parsing date '{date_text}': {e}")

        return ''
