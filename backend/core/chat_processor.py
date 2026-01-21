"""Chat processing logic using the ReAct agent graph.

Handles chat message processing through the LangGraph ReAct workflow.
"""

from typing import Optional, Dict, Any, Tuple
from agents.react_graph import react_agent_graph
from agents.react_state import create_initial_state
from services.supabase_service import supabase_service
from utils.logger import setup_logger

logger = setup_logger(__name__)


def _extract_debug_info(result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract debug information from the agent result."""
    iterations = result.get("current_iteration", 0)
    tool_calls = result.get("tool_calls", [])
    reasoning_trace = result.get("reasoning_trace", [])

    # Get list of tools used
    tools_used = list(set(tc.get("tool_name", "") for tc in tool_calls if tc.get("tool_name")))

    # Build step details
    steps = []
    for i, trace in enumerate(reasoning_trace):
        step = {
            "iteration": trace.get("iteration", i + 1),
            "thought": trace.get("thought"),
            "action": trace.get("action"),
            "action_input": trace.get("action_input"),
            "timestamp": trace.get("timestamp")
        }

        # Add observation from corresponding tool call if available
        if i < len(tool_calls):
            tc = tool_calls[i]
            if tc.get("error"):
                step["observation"] = f"Error: {tc.get('error')}"
            else:
                # Truncate long observations for readability
                obs = tc.get("result", "")
                if obs and len(str(obs)) > 500:
                    step["observation"] = str(obs)[:500] + "... (truncated)"
                else:
                    step["observation"] = obs

        steps.append(step)

    return {
        "total_iterations": iterations,
        "tool_calls_count": len(tool_calls),
        "tools_used": tools_used,
        "steps": steps
    }


async def process_chat(
    query: str,
    session_id: str,
    ical_url: Optional[str] = None,
    include_steps: bool = False,
    conversation_history: Optional[list] = None
) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Process a chat message through the agent graph.

    Args:
        query: User's query message
        session_id: Session identifier
        ical_url: Optional iCal URL for timetable queries
        include_steps: Whether to include debug/step information
        conversation_history: Optional list of previous messages in the conversation

    Returns:
        Tuple of (response string, debug info dict or None)

    Raises:
        Exception: If processing fails
    """
    try:
        logger.info(f"Processing query for session {session_id}: {query}")

        # Prepare initial state for ReAct agent (max_iterations defaults to settings)
        initial_state = create_initial_state(
            query=query,
            user_id=session_id,
            ical_url=ical_url,
            conversation_history=conversation_history
        )

        # Run through ReAct agent graph
        result = react_agent_graph.invoke(initial_state)

        # Extract response (with fallback for empty/None)
        response = result.get("final_response")
        if not response:
            logger.warning("No final_response from agent, using fallback")
            response = "I couldn't generate a response. Please try again."

        # Log iteration count for monitoring
        iterations = result.get("current_iteration", 0)
        tool_calls = result.get("tool_calls", [])
        reasoning_trace = result.get("reasoning_trace", [])

        # Log detailed steps
        logger.info(f"ReAct completed in {iterations} iterations with {len(tool_calls)} tool calls")
        for i, trace in enumerate(reasoning_trace):
            logger.info(f"  Step {trace.get('iteration', i+1)}: {trace.get('action', 'unknown')} - {trace.get('thought', '')[:100]}...")

        logger.info(f"Successfully generated response for session {session_id}")

        # Extract debug info if requested
        debug_info = _extract_debug_info(result) if include_steps else None

        # Save messages to database
        try:
            save_messages_to_db(session_id, query, response)
        except Exception as db_error:
            logger.error(f"Error saving to database: {str(db_error)}")
            # Don't fail the request if DB save fails

        return response, debug_info

    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}", exc_info=True)
        raise Exception(f"Failed to process chat: {str(e)}")


def save_messages_to_db(
    session_id: str,
    user_message: str,
    assistant_message: str
) -> None:
    """
    Save chat messages to Supabase database.

    Args:
        session_id: Session identifier
        user_message: User's message
        assistant_message: Assistant's response
    """
    try:
        # Save user message
        supabase_service.save_chat_message(
            user_id=session_id,
            role="user",
            content=user_message,
            session_id=session_id
        )

        # Save assistant message
        supabase_service.save_chat_message(
            user_id=session_id,
            role="assistant",
            content=assistant_message,
            session_id=session_id
        )

        logger.info(f"Messages saved to database for session {session_id}")

    except Exception as e:
        logger.error(f"Error saving messages to database: {str(e)}")
        raise


async def get_chat_history(session_id: str, limit: int = 50) -> list:
    """
    Retrieve chat history for a session.

    Args:
        session_id: Session identifier
        limit: Maximum number of messages to retrieve

    Returns:
        list: List of message dictionaries
    """
    try:
        messages = supabase_service.get_chat_history(
            session_id=session_id,
            limit=limit
        )
        return messages

    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return []
