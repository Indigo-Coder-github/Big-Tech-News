"""
Playwright-based Dynamic Scraper base class
JavaScript rendering support for dynamic websites
"""
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, logger

# Playwright is optional - only import when needed
try:
    from playwright.sync_api import sync_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. Dynamic scraping will be disabled.")


class PlaywrightScraper(BaseScraper):
    """Base class for scrapers that need JavaScript rendering"""

    def __init__(self, source_name: str, url: str, user_agent: str, delay: float = 1.5):
        super().__init__(source_name, url, user_agent, delay)
        self.browser: Optional[Browser] = None
        self.playwright = None
        self._wait_for_selector: Optional[str] = None  # CSS selector to wait for
        self._wait_timeout: int = 30000  # milliseconds

    def _ensure_playwright(self) -> bool:
        """Check if Playwright is available"""
        if not PLAYWRIGHT_AVAILABLE:
            logger.error(
                f"Playwright not installed. Install with: "
                f"pip install playwright && playwright install chromium"
            )
            return False
        return True

    def fetch_page_dynamic(
        self,
        url: Optional[str] = None,
        wait_for: Optional[str] = None,
        wait_timeout: Optional[int] = None
    ) -> Optional[BeautifulSoup]:
        """
        Fetch page with JavaScript rendering using Playwright

        Args:
            url: URL to fetch (defaults to self.url)
            wait_for: CSS selector to wait for before parsing
            wait_timeout: Timeout in milliseconds

        Returns:
            BeautifulSoup object or None on error
        """
        if not self._ensure_playwright():
            return None

        target_url = url or self.url
        selector = wait_for or self._wait_for_selector
        timeout = wait_timeout or self._wait_timeout

        try:
            with sync_playwright() as p:
                # Launch headless browser
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.user_agent,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = context.new_page()

                logger.info(f"Fetching {target_url} with Playwright...")

                # Navigate to page
                page.goto(target_url, wait_until='networkidle', timeout=timeout)

                # Wait for specific selector if provided
                if selector:
                    try:
                        page.wait_for_selector(selector, timeout=timeout)
                    except Exception as e:
                        logger.warning(f"Selector '{selector}' not found: {e}")

                # Get rendered HTML
                html_content = page.content()

                # Clean up
                browser.close()

                return BeautifulSoup(html_content, 'html.parser')

        except Exception as e:
            logger.error(f"Error fetching {target_url} with Playwright: {e}")
            return None

    def fetch_with_scroll(
        self,
        url: Optional[str] = None,
        scroll_count: int = 3,
        scroll_delay: int = 1000
    ) -> Optional[BeautifulSoup]:
        """
        Fetch page with scrolling for infinite scroll pages

        Args:
            url: URL to fetch
            scroll_count: Number of scroll actions
            scroll_delay: Delay between scrolls in milliseconds

        Returns:
            BeautifulSoup object or None on error
        """
        if not self._ensure_playwright():
            return None

        target_url = url or self.url

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.user_agent,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = context.new_page()

                logger.info(f"Fetching {target_url} with scroll support...")

                page.goto(target_url, wait_until='networkidle', timeout=self._wait_timeout)

                # Scroll down multiple times
                for i in range(scroll_count):
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    page.wait_for_timeout(scroll_delay)
                    logger.debug(f"Scroll {i + 1}/{scroll_count}")

                # Wait for any lazy-loaded content
                page.wait_for_timeout(1000)

                html_content = page.content()
                browser.close()

                return BeautifulSoup(html_content, 'html.parser')

        except Exception as e:
            logger.error(f"Error fetching {target_url} with scroll: {e}")
            return None

    def fetch(self) -> List[Dict]:
        """Override this method in subclasses"""
        raise NotImplementedError("Subclasses must implement fetch()")
