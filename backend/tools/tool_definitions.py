"""
Tool definitions with JSON schemas for ReAct agent.
These schemas are used by the LLM to understand available tools and their parameters.
"""

from typing import Dict, Any, List, Optional


TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "name": "search",
        "description": "Search the web for information about King's College London. Use this when you need to find current information, news, policies, or general facts about KCL.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query. Will automatically be enhanced with 'King's College London' context."
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of search results to return (1-10).",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "scraper",
        "description": "Scrape and extract content from a specific web page URL. Use this when you have a URL and need to read its full content in detail.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the web page to scrape."
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "timetable",
        "description": "Access the student's KCL timetable from their iCal subscription. Use this when the user asks about their schedule, classes, lectures, or upcoming events. Requires the user to have set up their iCal URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "days_ahead": {
                    "type": "integer",
                    "description": "Number of days ahead to fetch events (1-30).",
                    "default": 7
                }
            },
            "required": []
        }
    },
    {
        "name": "tiktok",
        "description": "Search TikTok for videos by hashtag, profile, or search query. Use this when the user wants to find TikTok content related to KCL or university life.",
        "parameters": {
            "type": "object",
            "properties": {
                "hashtags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of hashtags to search (without the # symbol). Example: ['kcl', 'kingscollege']"
                },
                "profiles": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of TikTok usernames to search (without the @ symbol)."
                },
                "search_queries": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of text search queries."
                },
                "results_per_page": {
                    "type": "integer",
                    "description": "Number of results to return (max 50).",
                    "default": 10
                }
            },
            "required": []
        }
    },
    {
        "name": "instagram",
        "description": "Search Instagram for posts by profile, hashtag, or search query. Use this when the user wants to find Instagram content related to KCL, university life, or specific accounts.",
        "parameters": {
            "type": "object",
            "properties": {
                "profiles": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of Instagram usernames to scrape (without the @ symbol). Example: ['kingscollege', 'kclsu']"
                },
                "hashtags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of hashtags to search (without the # symbol). Example: ['kcl', 'kingscollege']"
                },
                "search_query": {
                    "type": "string",
                    "description": "Search query to find posts, users, or places."
                },
                "search_type": {
                    "type": "string",
                    "enum": ["hashtag", "user", "place"],
                    "description": "Type of search when using search_query. Options: 'hashtag', 'user', 'place'.",
                    "default": "hashtag"
                },
                "results_limit": {
                    "type": "integer",
                    "description": "Number of results to return (max 100).",
                    "default": 10
                }
            },
            "required": []
        }
    }
]


def get_tool_definitions() -> List[Dict[str, Any]]:
    """Get all tool definitions."""
    return TOOL_DEFINITIONS


def get_tool_definitions_text() -> str:
    """
    Get tool definitions formatted as text for inclusion in prompts.
    """
    lines = ["Available Tools:", ""]

    for tool in TOOL_DEFINITIONS:
        lines.append(f"**{tool['name']}**")
        lines.append(f"Description: {tool['description']}")
        lines.append("Parameters:")

        props = tool["parameters"].get("properties", {})
        required = tool["parameters"].get("required", [])

        for param_name, param_info in props.items():
            req_marker = "(required)" if param_name in required else "(optional)"
            default = f", default: {param_info.get('default')}" if "default" in param_info else ""
            param_type = param_info.get("type", "any")
            lines.append(f"  - {param_name} ({param_type}) {req_marker}: {param_info.get('description', '')}{default}")

        if not props:
            lines.append("  - No parameters required")

        lines.append("")

    return "\n".join(lines)


def get_tool_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Get a specific tool definition by name."""
    for tool in TOOL_DEFINITIONS:
        if tool["name"] == name:
            return tool
    return None
