"""
Main LangGraph workflow definition.
"""

from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes import (
    router_node,
    search_node,
    scraper_node,
    timetable_node,
    response_node
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_agent_graph():
    """
    Create and compile the agent workflow graph.

    Returns:
        Compiled graph
    """
    logger.info("Creating agent graph")

    # Create graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("search", search_node)
    workflow.add_node("scraper", scraper_node)
    workflow.add_node("timetable", timetable_node)
    workflow.add_node("response", response_node)

    # Define flow
    workflow.set_entry_point("router")

    # Router -> Search
    workflow.add_edge("router", "search")

    # Search -> Scraper
    workflow.add_edge("search", "scraper")

    # Scraper -> Timetable
    workflow.add_edge("scraper", "timetable")

    # Timetable -> Response
    workflow.add_edge("timetable", "response")

    # Response -> END
    workflow.add_edge("response", END)

    # Compile
    graph = workflow.compile()

    logger.info("Agent graph compiled successfully")
    return graph


# Singleton graph instance
agent_graph = create_agent_graph()
