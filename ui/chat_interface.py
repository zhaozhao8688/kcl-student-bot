"""
Chat interface logic.
"""

import streamlit as st
from typing import Optional
from agents.graph import agent_graph
from agents.state import AgentState
from auth.session_manager import SessionManager
from services.supabase_service import supabase_service
from utils.logger import setup_logger

logger = setup_logger(__name__)


def process_user_input(user_input: str) -> str:
    """
    Process user input through the agent graph.

    Args:
        user_input: User's query

    Returns:
        Agent's response
    """
    try:
        logger.info(f"Processing query: {user_input}")

        # Get iCal URL from session
        ical_url = SessionManager.get_ical_url()

        # Prepare initial state
        initial_state: AgentState = {
            "messages": [],
            "user_id": SessionManager.get_user_id(),
            "is_authenticated": False,  # Not using authentication anymore
            "query": user_input,
            "query_type": "",
            "needs_search": False,
            "needs_scraping": False,
            "needs_timetable": False,
            "search_results": None,
            "scraped_content": None,
            "timetable_events": None,
            "final_response": None,
            "ical_url": ical_url if ical_url else None
        }

        # Run through graph
        result = agent_graph.invoke(initial_state)

        # Extract response
        response = result.get("final_response", "I couldn't generate a response. Please try again.")

        logger.info("Successfully generated response")
        return response

    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        return "I encountered an error processing your request. Please try again."


def save_messages_to_db(user_message: str, assistant_message: str) -> None:
    """
    Save chat messages to database.

    Args:
        user_message: User's message
        assistant_message: Assistant's response
    """
    try:
        user_id = SessionManager.get_user_id()
        session_id = SessionManager.get_session_id()

        # Save user message
        supabase_service.save_chat_message(
            user_id=user_id,
            role="user",
            content=user_message,
            session_id=session_id
        )

        # Save assistant message
        supabase_service.save_chat_message(
            user_id=user_id,
            role="assistant",
            content=assistant_message,
            session_id=session_id
        )

        logger.info("Messages saved to database")

    except Exception as e:
        logger.error(f"Error saving messages: {str(e)}")


def render_chat_interface() -> None:
    """Render the main chat interface."""

    # Display chat history
    from ui.components import render_chat_history
    chat_history = SessionManager.get_chat_history()
    render_chat_history(chat_history)

    # Chat input
    user_input = st.chat_input("Ask me anything about KCL...")

    if user_input:
        # Add user message to history and display
        SessionManager.add_message("user", user_input)
        from ui.components import render_message
        render_message("user", user_input)

        # Process input
        with st.spinner("Thinking..."):
            response = process_user_input(user_input)

        # Add assistant message to history and display
        SessionManager.add_message("assistant", response)
        render_message("assistant", response)

        # Save to database
        save_messages_to_db(user_input, response)

        # Rerun to update UI
        st.rerun()


# Settings panel removed - now integrated into main sidebar
