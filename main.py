"""
BigTech AI News Aggregator
Main script to collect news from various sources
"""
import json
import yaml
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from scrapers.rss_scraper import RSScraper
from scrapers.anthropic_scraper import AnthropicScraper
from scrapers.meta_scraper import MetaScraper
from scrapers.deepmind_scraper import DeepMindScraper
from scrapers.google_ai_scraper import GoogleAIScraper
from scrapers.lg_research_scraper import LGResearchScraper
from scrapers.microsoft_ai_scraper import MicrosoftAIScraper
from scrapers.deepseek_scraper import DeepSeekScraper
from scrapers.deepseek_blog_scraper import DeepSeekBlogScraper
from data_manager import DataManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsAggregator:
    """Main aggregator class"""

    def __init__(self, config_path: str = 'config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.settings = self.config['settings']
        self.sources = self.config['sources']

        # Map scraper types
        self.scraper_map = {
            'anthropic': AnthropicScraper,
            'meta': MetaScraper,
            'deepmind': DeepMindScraper,
            'google_ai': GoogleAIScraper,
            'lg_research': LGResearchScraper,
            'microsoft_ai': MicrosoftAIScraper,
            'deepseek': DeepSeekScraper,
            'deepseek_blog': DeepSeekBlogScraper,
        }

    def collect_all(self) -> List[Dict]:
        """Collect articles from all enabled sources"""
        all_articles = []

        for source in self.sources:
            if not source.get('enabled', True):
                logger.info(f"Skipping disabled source: {source['name']}")
                continue

            try:
                articles = self._collect_from_source(source)
                all_articles.extend(articles)
                logger.info(f"Collected {len(articles)} articles from {source['name']}")
            except Exception as e:
                logger.error(f"Error collecting from {source['name']}: {e}")
                continue

        return all_articles

    def _collect_from_source(self, source: Dict) -> List[Dict]:
        """Collect articles from a single source"""
        source_type = source['type']
        source_name = source['name']
        url = source['url']

        if source_type == 'rss':
            scraper = RSScraper(
                source_name=source_name,
                url=url,
                user_agent=self.settings['user_agent'],
                delay=self.settings['request_delay']
            )
            return scraper.fetch()

        elif source_type == 'html':
            scraper_class = self.scraper_map.get(source.get('scraper'))
            if not scraper_class:
                logger.warning(f"Unknown scraper type: {source.get('scraper')}")
                return []

            scraper = scraper_class(
                source_name=source_name,
                url=url,
                user_agent=self.settings['user_agent'],
                delay=self.settings['request_delay']
            )
            return scraper.fetch()

        else:
            logger.warning(f"Unknown source type: {source_type}")
            return []

    def remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on URL"""
        seen_urls = set()
        unique_articles = []

        for article in articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)

        return unique_articles

    def sort_articles(self, articles: List[Dict]) -> List[Dict]:
        """Sort articles by date (newest first)"""
        def get_sort_key(article):
            date_str = article.get('date', '')
            if date_str:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    pass
            # If no date, use collected_at timestamp
            return datetime.strptime(article.get('collected_at', '1970-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S')

        return sorted(articles, key=get_sort_key, reverse=True)

    def save_to_json(self, articles: List[Dict], output_path: str = None):
        """Save articles using new data structure (sources + index)"""
        # Use DataManager for new structure
        dm = DataManager()
        dm.save_articles(articles)
        logger.info(f"Saved {len(articles)} articles to new data structure")

        # Also save old format for backward compatibility (optional)
        if output_path or self.settings.get('output_file'):
            old_output_path = output_path or self.settings['output_file']
            Path(old_output_path).parent.mkdir(parents=True, exist_ok=True)

            data = {
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_articles': len(articles),
                'articles': articles
            }

            with open(old_output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Also saved legacy format to {old_output_path}")

        # Copy data folder to docs/data/ for GitHub Pages
        docs_data_path = Path('docs/data')
        docs_data_path.mkdir(parents=True, exist_ok=True)

        # Copy index.json
        shutil.copy2('data/index.json', docs_data_path / 'index.json')

        # Copy sources folder
        docs_sources_path = docs_data_path / 'sources'
        if docs_sources_path.exists():
            shutil.rmtree(docs_sources_path)
        shutil.copytree('data/sources', docs_sources_path)

        logger.info(f"Copied new data structure to {docs_data_path}")

        # Copy assets folder to docs/assets/ if it exists
        assets_src = Path('assets')
        assets_dest = Path('docs/assets')
        if assets_src.exists():
            assets_dest.mkdir(parents=True, exist_ok=True)
            for file in assets_src.glob('*.svg'):
                shutil.copy2(file, assets_dest / file.name)
            logger.info(f"Copied assets to {assets_dest}")

    def run(self):
        """Main execution method"""
        logger.info("Starting BigTech AI News Aggregator...")

        # Collect articles
        articles = self.collect_all()
        logger.info(f"Total articles collected: {len(articles)}")

        # Remove duplicates
        articles = self.remove_duplicates(articles)
        logger.info(f"After removing duplicates: {len(articles)}")

        # Sort by date
        articles = self.sort_articles(articles)

        # Limit per source if configured
        max_articles = self.settings.get('max_articles_per_source')
        if max_articles:
            # Group by source and limit
            source_articles = {}
            for article in articles:
                source = article['source']
                if source not in source_articles:
                    source_articles[source] = []
                if len(source_articles[source]) < max_articles:
                    source_articles[source].append(article)

            # Flatten back to list
            articles = []
            for source_list in source_articles.values():
                articles.extend(source_list)

            # Re-sort
            articles = self.sort_articles(articles)
            logger.info(f"After limiting per source: {len(articles)}")

        # Save to JSON
        self.save_to_json(articles)

        logger.info("Done!")


def main():
    aggregator = NewsAggregator()
    aggregator.run()


if __name__ == '__main__':
    main()
