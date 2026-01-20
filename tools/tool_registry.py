"""
Central tool registry and factory.
"""

from typing import List, Dict
from tools.base import BaseTool
from tools.search_tool import SearchTool
from tools.scraper_tool import ScraperTool
from tools.timetable_tool import TimetableTool
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ToolRegistry:
    """Registry for all available tools."""

    def __init__(self):
        """Initialize tool registry."""
        self._tools: Dict[str, BaseTool] = {}
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all available tools."""
        tools = [
            SearchTool(),
            ScraperTool(),
            TimetableTool()
        ]

        for tool in tools:
            self._tools[tool.get_name()] = tool
            logger.info(f"Registered tool: {tool.get_name()}")

    def get_tool(self, name: str) -> BaseTool:
        """
        Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance

        Raises:
            KeyError: If tool not found
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name]

    def get_all_tools(self) -> List[BaseTool]:
        """
        Get all registered tools.

        Returns:
            List of all tools
        """
        return list(self._tools.values())

    def get_public_tools(self) -> List[BaseTool]:
        """
        Get tools that don't require authentication.

        Returns:
            List of public tools
        """
        return [tool for tool in self._tools.values() if not tool.requires_auth()]

    def get_authenticated_tools(self) -> List[BaseTool]:
        """
        Get all tools including those requiring authentication.

        Returns:
            List of all tools
        """
        return self.get_all_tools()

    def get_tools_for_user(self, is_authenticated: bool) -> List[BaseTool]:
        """
        Get available tools based on authentication status.

        Args:
            is_authenticated: Whether user is authenticated

        Returns:
            List of available tools
        """
        if is_authenticated:
            return self.get_authenticated_tools()
        else:
            return self.get_public_tools()


# Singleton instance
tool_registry = ToolRegistry()
