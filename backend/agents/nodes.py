"""
Agent graph node implementations.
"""

from typing import Dict, Any
from agents.state import AgentState
from tools.tool_registry import tool_registry
from services.llm_service import llm_service
from utils.formatters import format_search_results, format_timetable_events, format_tiktok_results
from utils.logger import setup_logger
import re

logger = setup_logger(__name__)


def router_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyze query and determine required tools.

    Args:
        state: Current agent state

    Returns:
        Updated state with tool flags
    """
    logger.info(f"Router analyzing query: {state['query']}")

    query = state["query"].lower()
    original_query = state["query"]

    # Determine query type and required tools - expand timetable keywords
    timetable_keywords = [
        "timetable", "schedule", "class", "lecture", "lesson",
        "when is my", "what do i have", "show me my",
        "tomorrow", "tmr", "today", "this week", "next week",
        "professor", "teacher", "instructor", "module", "course"
    ]

    # TikTok keywords for detection
    tiktok_keywords = [
        "tiktok", "fyp", "for you page",
        "viral", "trending", "influencer", "creator", "social media",
        "video", "clips", "content"
    ]

    needs_timetable = any(keyword in query for keyword in timetable_keywords)

    # Check for TikTok triggers: keywords or #hashtag/@username patterns
    hashtag_pattern = re.compile(r'#(\w+)')
    profile_pattern = re.compile(r'@(\w+)')

    hashtags_found = hashtag_pattern.findall(original_query)
    profiles_found = profile_pattern.findall(original_query)

    needs_tiktok = (
        any(keyword in query for keyword in tiktok_keywords) or
        bool(hashtags_found) or
        bool(profiles_found)
    )

    # Extract TikTok query parameters
    tiktok_hashtags = hashtags_found if hashtags_found else None
    tiktok_profiles = profiles_found if profiles_found else None

    # Build search query from remaining text (remove hashtags and mentions)
    remaining_query = re.sub(r'[#@]\w+', '', original_query).strip()
    tiktok_queries = [remaining_query] if remaining_query and needs_tiktok else None

    # Only search if it's not a pure timetable query and not a TikTok query
    needs_search = not needs_timetable and not needs_tiktok

    needs_scraping = needs_search  # Scrape top result if we search

    return {
        "query_type": "tiktok" if needs_tiktok else ("timetable" if needs_timetable else "general"),
        "needs_search": needs_search,
        "needs_scraping": needs_scraping and needs_search,
        "needs_timetable": needs_timetable,
        "needs_tiktok": needs_tiktok,
        "search_results": None,
        "scraped_content": None,
        "timetable_events": None,
        "tiktok_results": None,
        "tiktok_hashtags": tiktok_hashtags,
        "tiktok_profiles": tiktok_profiles,
        "tiktok_queries": tiktok_queries
    }


def search_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute web search if needed.

    Args:
        state: Current agent state

    Returns:
        Updated state with search results
    """
    if not state.get("needs_search", False):
        logger.info("Skipping search - not needed")
        return {"search_results": None}

    logger.info("Executing search")
    search_tool = tool_registry.get_tool("search")
    results = search_tool.execute(query=state["query"], num_results=5)

    return {"search_results": results}


def scraper_node(state: AgentState) -> Dict[str, Any]:
    """
    Scrape top search result if needed.

    Args:
        state: Current agent state

    Returns:
        Updated state with scraped content
    """
    if not state.get("needs_scraping", False):
        logger.info("Skipping scraper - not needed")
        return {"scraped_content": None}

    search_results = state.get("search_results", [])
    if not search_results:
        logger.info("No search results to scrape")
        return {"scraped_content": None}

    # Scrape first result
    top_result = search_results[0]
    url = top_result.get("link")

    if not url:
        return {"scraped_content": None}

    logger.info(f"Scraping top result: {url}")
    scraper_tool = tool_registry.get_tool("scraper")
    content = scraper_tool.execute(url=url)

    return {"scraped_content": content}


def timetable_node(state: AgentState) -> Dict[str, Any]:
    """
    Access timetable if iCal URL is provided and needed.

    Args:
        state: Current agent state

    Returns:
        Updated state with timetable events
    """
    if not state.get("needs_timetable", False):
        logger.info("Skipping timetable - not needed")
        return {"timetable_events": None}

    ical_url = state.get("ical_url")
    if not ical_url:
        logger.warning("No iCal URL provided for timetable query")
        return {
            "timetable_events": None,
            "final_response": "To access your timetable, please add your iCal subscription URL in the sidebar.\n\n**How to get your iCal URL:**\n1. Go to your KCL timetable (Scientia)\n2. Click 'Subscribe' button\n3. Copy the URL from 'Manual subscription' section\n4. Paste it in the sidebar"
        }

    logger.info(f"Fetching timetable from URL: {ical_url[:50]}...")
    timetable_tool = tool_registry.get_tool("timetable")
    events = timetable_tool.execute(ical_url=ical_url, days_ahead=7)

    if not events:
        logger.warning("No events returned from timetable")
        return {
            "timetable_events": None,
            "final_response": "I couldn't retrieve your timetable. Please check:\n1. Your iCal URL is complete and correct\n2. The URL hasn't expired\n3. You have an active internet connection\n\nTry getting a fresh iCal URL from your KCL timetable."
        }

    logger.info(f"Successfully retrieved {len(events)} timetable events")
    return {"timetable_events": events}


def tiktok_node(state: AgentState) -> Dict[str, Any]:
    """
    Fetch TikTok videos if needed.

    Args:
        state: Current agent state

    Returns:
        Updated state with TikTok results
    """
    if not state.get("needs_tiktok", False):
        logger.info("Skipping TikTok - not needed")
        return {"tiktok_results": None}

    logger.info("Executing TikTok search")
    tiktok_tool = tool_registry.get_tool("tiktok")

    results = tiktok_tool.execute(
        hashtags=state.get("tiktok_hashtags"),
        profiles=state.get("tiktok_profiles"),
        search_queries=state.get("tiktok_queries"),
        results_per_page=10
    )

    if not results:
        logger.warning("No TikTok results returned")
        return {"tiktok_results": None}

    logger.info(f"Successfully retrieved {len(results)} TikTok videos")
    return {"tiktok_results": results}


def response_node(state: AgentState) -> Dict[str, Any]:
    """
    Generate final response using LLM.

    Args:
        state: Current agent state

    Returns:
        Updated state with final response
    """
    # If we already have a response (e.g., auth error), return it
    if state.get("final_response"):
        logger.info("Using pre-generated response")
        return {}

    logger.info("Generating final response")

    # Compile context from tool results
    context_parts = []

    if state.get("search_results"):
        context_parts.append("Search Results:\n" + format_search_results(state["search_results"]))

    if state.get("scraped_content"):
        # Limit scraped content to avoid token limits
        content = state["scraped_content"][:3000]
        context_parts.append(f"Detailed Information:\n{content}")

    if state.get("timetable_events"):
        context_parts.append("Timetable:\n" + format_timetable_events(state["timetable_events"]))

    if state.get("tiktok_results"):
        context_parts.append("TikTok Videos:\n" + format_tiktok_results(state["tiktok_results"]))

    context = "\n\n".join(context_parts) if context_parts else "No additional context available."

    # Build messages for LLM
    system_message = """You are a helpful AI assistant for King's College London (KCL) students.
Your role is to provide helpful information about KCL using the tools and context provided.

Guidelines:
- Be friendly and supportive
- Provide specific, actionable information
- If you don't have enough information, say so
- Include relevant links when available
- For timetable queries, present information clearly
"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Question: {state['query']}\n\nContext:\n{context}\n\nProvide a helpful response based on the context above."}
    ]

    # Generate response
    try:
        response = llm_service.generate(messages=messages, temperature=0.7, max_tokens=1000)
        return {"final_response": response}
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return {"final_response": "I encountered an error processing your request. Please try again."}
