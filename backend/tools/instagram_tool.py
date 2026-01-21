"""
Instagram scraping tool using Apify's Instagram Scraper.
"""

from typing import List, Dict, Any, Optional
from apify_client import ApifyClient
from tools.base import BaseTool
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class InstagramTool(BaseTool):
    """Tool for searching and scraping Instagram posts."""

    def __init__(self):
        """Initialize Instagram tool."""
        super().__init__(
            name="instagram",
            description="Search and scrape Instagram posts by profile, hashtag, or search query"
        )
        self.api_key = settings.apify_api_key

    def execute(
        self,
        profiles: Optional[List[str]] = None,
        hashtags: Optional[List[str]] = None,
        search_query: Optional[str] = None,
        search_type: str = "hashtag",
        results_limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Execute Instagram scraping.

        Args:
            profiles: List of Instagram usernames to scrape (without @)
            hashtags: List of hashtags to search (without #)
            search_query: Search query to find posts, users, or places
            search_type: Type of search ('hashtag', 'user', 'place')
            results_limit: Number of results to return (max 100)

        Returns:
            List of post data dictionaries
        """
        logger.info(f"Instagram search - profiles: {profiles}, hashtags: {hashtags}, query: {search_query}")

        try:
            client = ApifyClient(self.api_key)

            # Build direct URLs from profiles and hashtags
            direct_urls = []
            if profiles:
                for profile in profiles:
                    username = profile.lstrip('@')
                    direct_urls.append(f"https://www.instagram.com/{username}/")
            if hashtags:
                for hashtag in hashtags:
                    tag = hashtag.lstrip('#')
                    direct_urls.append(f"https://www.instagram.com/explore/tags/{tag}/")

            run_input = {
                "resultsLimit": min(results_limit, 100),
                "resultsType": "posts"
            }

            if direct_urls:
                run_input["directUrls"] = direct_urls
            if search_query:
                run_input["search"] = search_query
                run_input["searchType"] = search_type
                run_input["searchLimit"] = 20

            # Run the Apify Instagram Scraper actor
            run = client.actor("apify/instagram-scraper").call(run_input=run_input)

            results = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(self._parse_post_data(item))

            logger.info(f"Instagram scraper returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Instagram scraping error: {str(e)}")
            return []

    def _parse_post_data(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw post data into standardized format.

        Args:
            item: Raw post data from Apify

        Returns:
            Parsed post data dictionary
        """
        return {
            "id": item.get("id", ""),
            "shortcode": item.get("shortCode", ""),
            "caption": item.get("caption", ""),
            "author": {
                "username": item.get("ownerUsername", ""),
                "full_name": item.get("ownerFullName", ""),
                "verified": item.get("isVerified", False),
            },
            "stats": {
                "likes": item.get("likesCount", 0),
                "comments": item.get("commentsCount", 0),
            },
            "hashtags": item.get("hashtags", []),
            "mentions": item.get("mentions", []),
            "media_type": item.get("type", ""),
            "url": item.get("url", ""),
            "display_url": item.get("displayUrl", ""),
            "video_url": item.get("videoUrl", ""),
            "created_at": item.get("timestamp", ""),
            "location": item.get("locationName", ""),
        }
