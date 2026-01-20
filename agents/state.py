"""
Agent state definition for LangGraph.
"""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """State object that flows through the agent graph."""

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
