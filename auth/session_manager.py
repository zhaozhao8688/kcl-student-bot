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
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.access_token = None
            st.session_state.chat_history = []
            logger.info(f"Initialized new session: {st.session_state.session_id}")

    @staticmethod
    def login(user_info: Dict[str, Any], access_token: str) -> None:
        """
        Mark user as authenticated and store user info.

        Args:
            user_info: User information from Microsoft
            access_token: Access token for API calls
        """
        st.session_state.authenticated = True
        st.session_state.user_info = user_info
        st.session_state.access_token = access_token
        logger.info(f"User logged in: {user_info.get('userPrincipalName', 'unknown')}")

    @staticmethod
    def logout() -> None:
        """Clear authentication and reset session."""
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.session_state.access_token = None
        st.session_state.chat_history = []
        logger.info("User logged out")

    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if user is authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        return st.session_state.get("authenticated", False)

    @staticmethod
    def get_user_id() -> str:
        """
        Get user identifier.

        Returns:
            User ID (email) if authenticated, session ID otherwise
        """
        if SessionManager.is_authenticated():
            user_info = st.session_state.get("user_info", {})
            return user_info.get("userPrincipalName", st.session_state.session_id)
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
    def get_access_token() -> Optional[str]:
        """
        Get access token if authenticated.

        Returns:
            Access token or None
        """
        return st.session_state.get("access_token")


# Initialize on import
SessionManager.initialize()
