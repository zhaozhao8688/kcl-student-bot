"""
Web scraping tool using Firecrawl.
"""

from typing import Optional
from tools.base import BaseTool
from config.settings import settings
from utils.logger import setup_logger
import requests

logger = setup_logger(__name__)


class ScraperTool(BaseTool):
    """Scrape web pages using Firecrawl."""

    def __init__(self):
        """Initialize scraper tool."""
        super().__init__(
            name="scraper",
            description="Scrape and extract content from web pages"
        )
        self.api_key = settings.firecrawl_api_key
        self.base_url = "https://api.firecrawl.dev/v0"

    def execute(self, url: str) -> Optional[str]:
        """
        Scrape content from a URL.

        Args:
            url: URL to scrape

        Returns:
            Scraped content in markdown format or None if error
        """
        try:
            logger.info(f"Scraping URL: {url}")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "url": url,
                "formats": ["markdown"]
            }

            response = requests.post(
                f"{self.base_url}/scrape",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get("data", {}).get("markdown", "")
                logger.info(f"Successfully scraped {len(content)} characters")
                return content
            else:
                logger.error(f"Scraping failed with status: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error scraping URL: {str(e)}")
            return None

    def requires_auth(self) -> bool:
        """Scraper tool does not require authentication."""
        return False
