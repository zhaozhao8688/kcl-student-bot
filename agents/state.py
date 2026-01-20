"""
Agent state definition for LangGraph.
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State object that flows through the agent graph."""

    # Messages (required for LangGraph)
    messages: Annotated[list, add_messages]

    # User context
    user_id: str
    is_authenticated: bool

    # Query analysis
    query: str
    query_type: str  # general, timetable, university_info, etc.

    # Tool execution flags
    needs_search: bool
    needs_scraping: bool
    needs_timetable: bool

    # Tool results
    search_results: Optional[List[Dict[str, Any]]]
    scraped_content: Optional[str]
    timetable_events: Optional[List[Dict[str, Any]]]

    # Response
    final_response: Optional[str]

    # Metadata
    ical_url: Optional[str]  # For timetable access
