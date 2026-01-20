"""
Session state management for Streamlit.
"""

import streamlit as st
import uuid
from typing import Optional, Dict, Any, List
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SessionManager:
    """Manage Streamlit session state."""

    @staticmethod
    def initialize() -> None:
        """Initialize session state variables if not already set."""
        if "initialized" not in st.session_state:
            st.session_state.initialized = True
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.chat_history = []
            st.session_state.ical_url = ""
            logger.info(f"Initialized new session: {st.session_state.session_id}")

    @staticmethod
    def set_ical_url(url: str) -> None:
        """
        Set the iCal URL for timetable access.

        Args:
            url: iCal subscription URL
        """
        st.session_state.ical_url = url
        logger.info("iCal URL updated")

    @staticmethod
    def get_ical_url() -> str:
        """
        Get the stored iCal URL.

        Returns:
            iCal URL or empty string
        """
        return st.session_state.get("ical_url", "")

    @staticmethod
    def get_user_id() -> str:
        """
        Get user identifier (session-based).

        Returns:
            Session ID
        """
        return st.session_state.get("session_id", "anonymous")

    @staticmethod
    def get_session_id() -> str:
        """
        Get current session ID.

        Returns:
            Session identifier
        """
        return st.session_state.get("session_id", "unknown")

    @staticmethod
    def add_message(role: str, content: str) -> None:
        """
        Add a message to chat history.

        Args:
            role: Message role (user/assistant)
            content: Message content
        """
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        st.session_state.chat_history.append({
            "role": role,
            "content": content
        })
        logger.debug(f"Added {role} message to chat history")

    @staticmethod
    def get_chat_history() -> List[Dict[str, str]]:
        """
        Get chat history.

        Returns:
            List of message dictionaries
        """
        return st.session_state.get("chat_history", [])

    @staticmethod
    def clear_chat_history() -> None:
        """Clear all chat history."""
        st.session_state.chat_history = []
        logger.info("Chat history cleared")

    @staticmethod
    def has_ical_url() -> bool:
        """
        Check if iCal URL is configured.

        Returns:
            True if URL is set, False otherwise
        """
        url = st.session_state.get("ical_url", "")
        return bool(url and url.strip())


# Initialize on import
SessionManager.initialize()
