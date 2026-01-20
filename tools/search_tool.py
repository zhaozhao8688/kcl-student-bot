"""
Web search tool using SerpAPI.
"""

from serpapi import GoogleSearch
from typing import List, Dict, Any
from tools.base import BaseTool
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SearchTool(BaseTool):
    """Search the web using SerpAPI."""

    def __init__(self):
        """Initialize search tool."""
        super().__init__(
            name="search",
            description="Search the web for information about King's College London"
        )
        self.api_key = settings.serpapi_api_key

    def execute(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Execute web search.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search result dictionaries
        """
        try:
            # Enhance query with KCL context
            enhanced_query = f"{query} King's College London"

            logger.info(f"Searching for: {enhanced_query}")

            search = GoogleSearch({
                "q": enhanced_query,
                "api_key": self.api_key,
                "num": num_results
            })

            results = search.get_dict()
            organic_results = results.get("organic_results", [])

            formatted_results = []
            for result in organic_results[:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })

            logger.info(f"Found {len(formatted_results)} search results")
            return formatted_results

        except Exception as e:
            logger.error(f"Error executing search: {str(e)}")
            return []

    def requires_auth(self) -> bool:
        """Search tool does not require authentication."""
        return False
