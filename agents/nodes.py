"""
Agent graph node implementations.
"""

from typing import Dict, Any
from agents.state import AgentState
from tools.tool_registry import tool_registry
from services.llm_service import llm_service
from utils.formatters import format_search_results, format_timetable_events
from utils.logger import setup_logger

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

    # Determine query type and required tools
    needs_timetable = any(keyword in query for keyword in [
        "timetable", "schedule", "class", "lecture", "when is my"
    ])

    needs_search = not needs_timetable or any(keyword in query for keyword in [
        "what", "where", "who", "how", "when", "why", "information", "about"
    ])

    needs_scraping = needs_search  # Scrape top result if we search

    return {
        "query_type": "timetable" if needs_timetable else "general",
        "needs_search": needs_search,
        "needs_scraping": needs_scraping and needs_search,
        "needs_timetable": needs_timetable,
        "search_results": None,
        "scraped_content": None,
        "timetable_events": None
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
        logger.info("No iCal URL provided")
        return {
            "timetable_events": None,
            "final_response": "To access your timetable, please add your iCal subscription URL in the sidebar.\n\n**How to get your iCal URL:**\n1. Go to your KCL timetable (Scientia)\n2. Click 'Subscribe' button\n3. Copy the URL from 'Manual subscription' section\n4. Paste it in the sidebar"
        }

    logger.info("Fetching timetable")
    timetable_tool = tool_registry.get_tool("timetable")
    events = timetable_tool.execute(ical_url=ical_url, days_ahead=7)

    return {"timetable_events": events}


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

    context = "\n\n".join(context_parts) if context_parts else "No additional context available."

    # Build messages for LLM
    system_message = """You are a helpful AI assistant for King's College London (KCL) students.
Your role is to provide accurate, helpful information about KCL using the context provided.

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
