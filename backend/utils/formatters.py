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


def format_tiktok_results(results: List[Dict[str, Any]]) -> str:
    """
    Format TikTok video results into readable markdown.

    Args:
        results: List of TikTok video dictionaries

    Returns:
        Formatted markdown string
    """
    if not results:
        return "No TikTok videos found."

    formatted = "### TikTok Videos\n\n"
    for idx, video in enumerate(results, 1):
        author = video.get("author", {})
        username = author.get("username", "unknown")
        verified = " ✓" if author.get("verified", False) else ""

        description = video.get("description", "No description")
        # Truncate description to 200 chars
        if len(description) > 200:
            description = description[:197] + "..."

        stats = video.get("stats", {})
        views = _format_number(stats.get("views", 0))
        likes = _format_number(stats.get("likes", 0))
        comments = _format_number(stats.get("comments", 0))
        shares = _format_number(stats.get("shares", 0))

        hashtags = video.get("hashtags", [])
        hashtags_str = " ".join([f"#{tag}" for tag in hashtags[:5]]) if hashtags else ""

        music = video.get("music", {})
        music_title = music.get("title", "")
        music_author = music.get("author", "")
        music_str = f"🎵 {music_title} - {music_author}" if music_title else ""

        url = video.get("url", "")

        formatted += f"**{idx}. @{username}{verified}**\n"
        formatted += f"{description}\n"
        formatted += f"👁 {views} | ❤️ {likes} | 💬 {comments} | 🔄 {shares}\n"
        if hashtags_str:
            formatted += f"{hashtags_str}\n"
        if music_str:
            formatted += f"{music_str}\n"
        if url:
            formatted += f"[Watch Video]({url})\n"
        formatted += "\n"

    return formatted


def _format_number(num: int) -> str:
    """
    Format large numbers with K/M suffixes.

    Args:
        num: Number to format

    Returns:
        Formatted string
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)


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
