"""
ReAct Agent state definition for LangGraph.
Implements the Reasoning-Action-Observation loop pattern.
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from datetime import datetime

from config.settings import settings


class ToolCall(BaseModel):
    """Record of a single tool call in the ReAct loop."""
    tool_name: str
    tool_input: Dict[str, Any]
    result: Optional[str] = None
    error: Optional[str] = None
    timestamp: str = ""

    def __init__(self, **data):
        if "timestamp" not in data or not data["timestamp"]:
            data["timestamp"] = datetime.now().isoformat()
        super().__init__(**data)


class ReActState(TypedDict):
    """State object for ReAct agent graph."""

    # Messages (required for LangGraph)
    messages: Annotated[list, add_messages]

    # User context
    user_id: str
    is_authenticated: bool

    # Original query
    query: str

    # ReAct loop control
    current_iteration: int
    max_iterations: int
    should_stop: bool

    # Current reasoning step
    current_thought: Optional[str]
    current_action: Optional[str]
    current_action_input: Optional[Dict[str, Any]]
    current_observation: Optional[str]

    # Reasoning trace (accumulated history)
    reasoning_trace: List[Dict[str, Any]]

    # Tool call history
    tool_calls: List[Dict[str, Any]]

    # Final output
    final_response: Optional[str]

    # Metadata
    ical_url: Optional[str]

    # Conversation history (for memory)
    conversation_history: Optional[List[Dict[str, str]]]

    # Planning (optional)
    plan: Optional[str]           # High-level strategy
    plan_reasoning: Optional[str] # Why this approach


def create_initial_state(
    query: str,
    user_id: str = "",
    ical_url: Optional[str] = None,
    max_iterations: Optional[int] = None,
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> ReActState:
    """Create initial state for ReAct agent.

    Args:
        query: User's query message
        user_id: User/session identifier
        ical_url: Optional iCal URL for timetable queries
        max_iterations: Maximum reasoning loops (defaults to settings.max_agent_iterations)
        conversation_history: Optional list of previous messages

    Returns:
        Initialized ReActState
    """
    return ReActState(
        messages=[],
        user_id=user_id,
        is_authenticated=False,
        query=query,
        current_iteration=0,
        max_iterations=max_iterations if max_iterations is not None else settings.max_agent_iterations,
        should_stop=False,
        current_thought=None,
        current_action=None,
        current_action_input=None,
        current_observation=None,
        reasoning_trace=[],
        tool_calls=[],
        final_response=None,
        ical_url=ical_url,
        conversation_history=conversation_history,
        plan=None,
        plan_reasoning=None
    )
