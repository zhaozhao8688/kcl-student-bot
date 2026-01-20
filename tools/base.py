"""
Base tool class for all agent tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseTool(ABC):
    """Abstract base class for all tools."""

    def __init__(self, name: str, description: str):
        """
        Initialize base tool.

        Args:
            name: Tool name
            description: Tool description
        """
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        Execute the tool with given parameters.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            Tool execution result
        """
        pass

    def requires_auth(self) -> bool:
        """
        Check if tool requires authentication.

        Returns:
            True if authentication required, False otherwise
        """
        return False

    def get_description(self) -> str:
        """
        Get tool description.

        Returns:
            Tool description
        """
        return self.description

    def get_name(self) -> str:
        """
        Get tool name.

        Returns:
            Tool name
        """
        return self.name

    def __str__(self) -> str:
        """String representation of tool."""
        return f"{self.name}: {self.description}"
