"""
TikTok scraping tool using Apify's TikTok Scraper.
"""

from typing import List, Dict, Any, Optional
from apify_client import ApifyClient
from tools.base import BaseTool
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TikTokTool(BaseTool):
    """Tool for searching and scraping TikTok videos."""

    def __init__(self):
        """Initialize TikTok tool."""
        super().__init__(
            name="tiktok",
            description="Search and scrape TikTok videos by hashtag, profile, or search query"
        )
        self.api_key = settings.apify_api_key

    def execute(
        self,
        hashtags: Optional[List[str]] = None,
        profiles: Optional[List[str]] = None,
        search_queries: Optional[List[str]] = None,
        results_per_page: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Execute TikTok scraping.

        Args:
            hashtags: List of hashtags to search (without #)
            profiles: List of profile usernames to search (without @)
            search_queries: List of search query strings
            results_per_page: Number of results to return (max 50)

        Returns:
            List of video data dictionaries
        """
        logger.info(f"TikTok search - hashtags: {hashtags}, profiles: {profiles}, queries: {search_queries}")

        try:
            client = ApifyClient(self.api_key)
            run_input = {"resultsPerPage": min(results_per_page, 50)}

            if hashtags:
                run_input["hashtags"] = [h.lstrip('#') for h in hashtags]
            if profiles:
                run_input["profiles"] = [p.lstrip('@') for p in profiles]
            if search_queries:
                run_input["searchQueries"] = search_queries

            # Run the Apify TikTok Scraper actor
            run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)

            results = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(self._parse_video_data(item))

            logger.info(f"TikTok scraper returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"TikTok scraping error: {str(e)}")
            return []

    def _parse_video_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw video data into standardized format.

        Args:
            item: Raw video data from Apify

        Returns:
            Parsed video data dictionary
        """
        return {
            "id": item.get("id", ""),
            "description": item.get("text", ""),
            "author": {
                "username": item.get("authorMeta", {}).get("name", ""),
                "nickname": item.get("authorMeta", {}).get("nickName", ""),
                "verified": item.get("authorMeta", {}).get("verified", False),
            },
            "stats": {
                "views": item.get("playCount", 0),
                "likes": item.get("diggCount", 0),
                "comments": item.get("commentCount", 0),
                "shares": item.get("shareCount", 0),
            },
            "hashtags": [tag.get("name", "") for tag in item.get("hashtags", [])],
            "music": {
                "title": item.get("musicMeta", {}).get("musicName", ""),
                "author": item.get("musicMeta", {}).get("musicAuthor", ""),
            },
            "url": item.get("webVideoUrl", ""),
            "created_at": item.get("createTimeISO", ""),
        }
