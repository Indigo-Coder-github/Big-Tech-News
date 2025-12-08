"""
LG AI Research Blog Scraper
Uses the internal API for reliable data extraction
"""
from typing import List, Dict
import re
import requests
from datetime import datetime
from .base import BaseScraper, logger


class LGResearchScraper(BaseScraper):
    """Scraper for LG AI Research blog using internal API"""

    API_URL = "https://www.lgresearch.ai/api/board/blog/list"

    def __init__(self, source_name: str, url: str, user_agent: str, delay: float = 1.5):
        super().__init__(source_name, url, user_agent, delay)
        self.headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def fetch(self) -> List[Dict]:
        """Fetch articles from LG AI Research blog API"""
        try:
            logger.info(f"Fetching blog posts from {self.source_name} (API)...")

            articles = []
            seen_seqs = set()

            # Fetch English articles
            en_articles = self._fetch_language('EN')
            for seq, article in en_articles:
                if seq not in seen_seqs:
                    seen_seqs.add(seq)
                    articles.append(article)

            # Fetch Korean articles (some may be different)
            kr_articles = self._fetch_language('KR')
            for seq, article in kr_articles:
                if seq not in seen_seqs:
                    seen_seqs.add(seq)
                    articles.append(article)

            # Sort by date descending
            articles.sort(key=lambda x: x.get('date', '1900-01-01'), reverse=True)

            logger.info(f"Found {len(articles)} articles from {self.source_name}")
            self.wait()

            return articles[:30]

        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            return []

    def _fetch_language(self, lang: str) -> List[Dict]:
        """Fetch articles for a specific language"""
        articles = []

        try:
            today = datetime.now().strftime('%Y%m%d')
            params = {
                'pg': 1,
                'pgSz': 30,
                'schExpsYn': 'Y',
                'schLangTp': lang,
                'schExpsYmd': today
            }

            response = requests.get(
                self.API_URL,
                params=params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if data.get('status') != 200:
                logger.warning(f"API returned status {data.get('status')} for {lang}")
                return []

            items = data.get('data', {}).get('list', [])
            logger.info(f"Found {len(items)} {lang} articles from API")

            for item in items:
                try:
                    result = self._parse_item(item, lang)
                    if result:
                        articles.append(result)  # (seq, article) tuple
                except Exception as e:
                    logger.debug(f"Error parsing item: {e}")
                    continue

        except Exception as e:
            logger.warning(f"Error fetching {lang} articles: {e}")

        return articles

    def _parse_item(self, item: Dict, lang: str):
        """Parse a single API item into article format

        Returns:
            Tuple of (seq, normalized_article) or None
        """
        seq = item.get('seq')
        title = item.get('ttl', '').strip()

        if not title or not seq:
            return None

        # Parse date from expsYmd (YYYYMMDD format)
        date_str = ''
        exps_ymd = item.get('expsYmd', '')
        if exps_ymd and len(exps_ymd) == 8:
            try:
                date_str = f"{exps_ymd[:4]}-{exps_ymd[4:6]}-{exps_ymd[6:8]}"
            except Exception:
                pass

        # Fallback to rgstYmd
        if not date_str:
            rgst_ymd = item.get('rgstYmd', '')
            if rgst_ymd and len(rgst_ymd) == 8:
                try:
                    date_str = f"{rgst_ymd[:4]}-{rgst_ymd[4:6]}-{rgst_ymd[6:8]}"
                except Exception:
                    pass

        # Build URL - blog detail page with query parameter
        url = f"https://www.lgresearch.ai/blog/view?seq={seq}"

        # Extract tags/categories
        categories = []
        blog_tags = item.get('blogTags', [])
        if blog_tags:
            for tag in blog_tags:
                tag_name = tag.get('tag', '')
                if tag_name and tag_name not in categories:
                    categories.append(tag_name)

        # Category from catgCd
        catg_cd = item.get('catgCd', '')
        catg_mapping = {
            'BAAACC': 'Research',
            'BAAADD': 'News'
        }
        if catg_cd in catg_mapping and catg_mapping[catg_cd] not in categories:
            categories.insert(0, catg_mapping[catg_cd])

        # Extract summary from content (first paragraph, strip HTML)
        summary = ''
        cont = item.get('cont', '')
        if cont:
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', cont)
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            if text:
                summary = text[:300]

        # Add language indicator if Korean
        if lang == 'KR':
            categories.append('Korean')

        article = self.normalize_article({
            'title': title,
            'url': url,
            'date': date_str,
            'summary': summary,
            'categories': categories[:5],  # Limit categories
            'author': ''
        })

        return (seq, article)
