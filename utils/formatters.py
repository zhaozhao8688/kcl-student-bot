"""
Response formatting utilities.
"""

from typing import List, Dict, Any
from datetime import datetime


def format_search_results(results: List[Dict[str, Any]]) -> str:
    """
    Format search results into readable markdown.

    Args:
        results: List of search result dictionaries

    Returns:
        Formatted markdown string
    """
    if not results:
        return "No search results found."

    formatted = "### Search Results\n\n"
    for idx, result in enumerate(results, 1):
        title = result.get("title", "No title")
        link = result.get("link", "#")
        snippet = result.get("snippet", "No description available")

        formatted += f"{idx}. **[{title}]({link})**\n"
        formatted += f"   {snippet}\n\n"

    return formatted


def format_timetable_events(events: List[Dict[str, Any]]) -> str:
    """
    Format timetable events into readable markdown.

    Args:
        events: List of calendar event dictionaries

    Returns:
        Formatted markdown string
    """
    if not events:
        return "No upcoming events found in your timetable."

    formatted = "### Your Timetable\n\n"
    for event in events:
        summary = event.get("summary", "Untitled Event")
        start = event.get("start")
        location = event.get("location", "Location TBD")
        description = event.get("description", "")

        # Format datetime
        if isinstance(start, datetime):
            start_str = start.strftime("%A, %B %d at %I:%M %p")
        else:
            start_str = str(start)

        formatted += f"**{summary}**\n"
        formatted += f"📅 {start_str}\n"
        formatted += f"📍 {location}\n"
        if description:
            formatted += f"ℹ️ {description}\n"
        formatted += "\n"

    return formatted


def format_error_message(error: str, user_friendly: bool = True) -> str:
    """
    Format error messages for display.

    Args:
        error: Error message
        user_friendly: Whether to make the message user-friendly

    Returns:
        Formatted error message
    """
    if user_friendly:
        return f"⚠️ **Error**: {error}\n\nPlease try again or rephrase your question."
    else:
        return f"Error: {error}"
