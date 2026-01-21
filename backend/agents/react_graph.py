"""
ReAct Agent LangGraph workflow definition.
Implements a Reasoning-Action-Observation loop with conditional edges.
"""

from langgraph.graph import StateGraph, END
from agents.react_state import ReActState
from agents.react_nodes import (
    reasoning_node,
    tool_execution_node,
    observation_node,
    should_continue
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_react_agent_graph():
    """
    Create and compile the ReAct agent workflow graph.

    The graph implements a loop:
        reasoning_node -> [tool_execution | END]
               ^              |
               └── observation_node

    Returns:
        Compiled LangGraph graph
    """
    logger.info("Creating ReAct agent graph")

    # Create graph with ReAct state
    workflow = StateGraph(ReActState)

    # Add nodes
    workflow.add_node("reasoning", reasoning_node)
    workflow.add_node("tool_execution", tool_execution_node)
    workflow.add_node("observation", observation_node)

    # Set entry point
    workflow.set_entry_point("reasoning")

    # Add conditional edges from reasoning node
    # If should_stop=True or action=final_answer -> END
    # Otherwise -> tool_execution
    workflow.add_conditional_edges(
        "reasoning",
        should_continue,
        {
            "tool": "tool_execution",
            "end": END
        }
    )

    # Tool execution -> Observation
    workflow.add_edge("tool_execution", "observation")

    # Observation -> Back to reasoning (loop)
    workflow.add_edge("observation", "reasoning")

    # Compile the graph
    graph = workflow.compile()

    logger.info("ReAct agent graph compiled successfully")
    return graph


# Singleton graph instance
react_agent_graph = create_react_agent_graph()
