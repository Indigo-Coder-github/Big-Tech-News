"""
Google AI Scraper
"""
from typing import List, Dict
import re
from .html_scraper import HTMLScraper, logger


class GoogleAIScraper(HTMLScraper):
    """Scraper for Google AI site"""

    def fetch(self) -> List[Dict]:
        """Fetch articles from Google AI"""
        try:
            logger.info(f"Fetching updates from {self.source_name}...")

            soup = self.fetch_page()
            if not soup:
                return []

            articles = []

            # Look for research links
            research_links = soup.find_all('a', href=re.compile(r'/research/'))

            # Look for any announcement or update sections
            for link in research_links[:30]:
                try:
                    title = link.get_text(strip=True)
                    url = link.get('href', '')

                    if not url.startswith('http'):
                        url = f"https://ai.google{url}"

                    if title and len(title) >= 10 and url not in [a['url'] for a in articles]:
                        articles.append({
                            'title': title,
                            'url': url,
                            'date': '',
                            'summary': '',
                            'categories': ['Research'],
                            'author': ''
                        })
                except Exception:
                    continue

            # Also check for blog-style updates
            headings = soup.find_all(['h2', 'h3'], string=re.compile(r'(Latest|New|Recent|Updates)', re.I))
            for heading in headings:
                parent = heading.find_parent(['section', 'div'])
                if parent:
                    links = parent.find_all('a', href=True)
                    for link in links[:10]:
                        try:
                            title = link.get_text(strip=True)
                            url = link.get('href', '')

                            if not url.startswith('http'):
                                url = f"https://ai.google{url}"

                            if title and len(title) >= 10 and url not in [a['url'] for a in articles]:
                                articles.append({
                                    'title': title,
                                    'url': url,
                                    'date': '',
                                    'summary': '',
                                    'categories': [],
                                    'author': ''
                                })
                        except Exception:
                            continue

            normalized = [self.normalize_article(a) for a in articles]
            logger.info(f"Found {len(normalized)} articles from {self.source_name}")
            self.wait()

            return normalized

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []
