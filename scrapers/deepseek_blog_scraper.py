"""
DeepSeek Blog Scraper
Scrapes blog posts from https://deepseek.ai/blog using sitemap
"""

from typing import List, Dict
import xml.etree.ElementTree as ET
from datetime import datetime
from .html_scraper import HTMLScraper, logger


class DeepSeekBlogScraper(HTMLScraper):
    """Scraper for DeepSeek Blog using sitemap.xml"""

    def fetch(self) -> List[Dict]:
        """Fetch blog posts from DeepSeek sitemap"""
        try:
            logger.info(f"Fetching blog posts from {self.source_name}...")

            # Fetch sitemap
            import requests
            response = requests.get(
                'https://deepseek.ai/sitemap.xml',
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()

            # Parse XML (handle BOM and leading whitespace)
            content = response.content
            if content.startswith(b'\xef\xbb\xbf'):
                content = content[3:]  # Remove UTF-8 BOM

            # Remove leading whitespace (newlines, spaces, etc.)
            content = content.lstrip()

            root = ET.fromstring(content)

            # Define namespace
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            articles = []
            seen_urls = set()

            # Find all blog URLs
            for url_elem in root.findall('sm:url', ns):
                try:
                    loc_elem = url_elem.find('sm:loc', ns)
                    lastmod_elem = url_elem.find('sm:lastmod', ns)

                    if loc_elem is None:
                        continue

                    url = loc_elem.text.strip()

                    # Only process blog post URLs (skip /blog itself and other pages)
                    if '/blog/' not in url or url in seen_urls:
                        continue

                    seen_urls.add(url)

                    # Extract date from lastmod
                    date_str = ''
                    if lastmod_elem is not None and lastmod_elem.text:
                        date_str = lastmod_elem.text.strip()

                    # Extract title from URL slug
                    # e.g., https://deepseek.ai/blog/deepseek-v31 -> DeepSeek V31
                    slug = url.split('/blog/')[-1]
                    title = self._slug_to_title(slug)

                    article = {
                        'title': title,
                        'url': url,
                        'date': date_str,
                        'summary': '',
                        'categories': ['Blog'],
                        'author': ''
                    }

                    articles.append(self.normalize_article(article))

                except Exception as e:
                    logger.warning(f"Error parsing sitemap entry: {e}")
                    continue

            logger.info(f"Found {len(articles)} blog posts from {self.source_name}")
            self.wait()

            return articles

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []

    def _slug_to_title(self, slug: str) -> str:
        """
        Convert URL slug to readable title
        e.g., 'deepseek-v31' -> 'DeepSeek V31'
        """
        # Replace hyphens with spaces
        title = slug.replace('-', ' ')

        # Capitalize words, but keep certain patterns
        words = title.split()
        capitalized = []

        for word in words:
            # Keep version numbers and special patterns
            if word.lower() in ['v31', 'v3', 'r1', 'r2', 'ai', 'vs', 'llama']:
                capitalized.append(word.upper())
            # Keep years as-is
            elif word.isdigit() and len(word) == 4:
                capitalized.append(word)
            # Special case for DeepSeek
            elif word.lower() == 'deepseek':
                capitalized.append('DeepSeek')
            else:
                capitalized.append(word.capitalize())

        return ' '.join(capitalized)
