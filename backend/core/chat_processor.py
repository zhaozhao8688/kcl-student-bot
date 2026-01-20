"""Chat processing logic using the agent graph.

Handles chat message processing through the LangGraph agent workflow.
"""

from typing import Optional
from agents.graph import agent_graph
from agents.state import AgentState
from services.supabase_service import supabase_service
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def process_chat(
    query: str,
    session_id: str,
    ical_url: Optional[str] = None
) -> str:
    """
    Process a chat message through the agent graph.

    Args:
        query: User's query message
        session_id: Session identifier
        ical_url: Optional iCal URL for timetable queries

    Returns:
        str: AI assistant's response

    Raises:
        Exception: If processing fails
    """
    try:
        logger.info(f"Processing query for session {session_id}: {query}")

        # Prepare initial state
        initial_state: AgentState = {
            "messages": [],
            "user_id": session_id,  # Use session_id as user_id
            "is_authenticated": False,
            "query": query,
            "query_type": "",
            "needs_search": False,
            "needs_scraping": False,
            "needs_timetable": False,
            "search_results": None,
            "scraped_content": None,
            "timetable_events": None,
            "final_response": None,
            "ical_url": ical_url
        }

        # Run through agent graph
        result = agent_graph.invoke(initial_state)

        # Extract response
        response = result.get(
            "final_response",
            "I couldn't generate a response. Please try again."
        )

        logger.info(f"Successfully generated response for session {session_id}")

        # Save messages to database
        try:
            save_messages_to_db(session_id, query, response)
        except Exception as db_error:
            logger.error(f"Error saving to database: {str(db_error)}")
            # Don't fail the request if DB save fails

        return response

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
            user_id=session_id,
            limit=limit
        )
        return messages

    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return []
