"""
Agent module exports.
"""

# ReAct agent components (primary)
from agents.react_graph import react_agent_graph, create_react_agent_graph
from agents.react_state import ReActState, ToolCall, create_initial_state
from agents.react_nodes import (
    reasoning_node,
    tool_execution_node,
    observation_node,
    should_continue
)
from agents.prompts import get_react_system_prompt, format_tool_history

# Legacy components (deprecated, kept for rollback)
# from agents.graph_legacy import agent_graph, create_agent_graph
# from agents.state_legacy import AgentState
# from agents.nodes_legacy import router_node, search_node, scraper_node, timetable_node, tiktok_node, response_node

__all__ = [
    # ReAct exports
    "react_agent_graph",
    "create_react_agent_graph",
    "ReActState",
    "ToolCall",
    "create_initial_state",
    "reasoning_node",
    "tool_execution_node",
    "observation_node",
    "should_continue",
    "get_react_system_prompt",
    "format_tool_history",
]
