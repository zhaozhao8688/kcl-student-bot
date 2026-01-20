"""
Reusable UI components for Streamlit.
"""

import streamlit as st
from typing import List, Dict


def render_message(role: str, content: str) -> None:
    """
    Render a single chat message.

    Args:
        role: Message role (user/assistant)
        content: Message content
    """
    with st.chat_message(role):
        st.markdown(content)


def render_chat_history(messages: List[Dict[str, str]]) -> None:
    """
    Render entire chat history.

    Args:
        messages: List of message dictionaries
    """
    for message in messages:
        render_message(message["role"], message["content"])


def render_sidebar() -> None:
    """Render sidebar with app information and settings."""
    with st.sidebar:
        st.header("📚 KCL Student Bot")

        st.markdown("""
        ### About
        Your AI-powered assistant for King's College London.

        **Features:**
        - 🔍 Search KCL information
        - 📅 Access your timetable (login required)
        - 💡 Get personalized help

        ### How to Use
        1. Type your question in the chat
        2. For timetable access, login with KCL account
        3. Ask anything about KCL!
        """)

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            from auth.session_manager import SessionManager
            SessionManager.clear_chat_history()
            st.rerun()

        st.divider()
        st.caption("Powered by OpenRouter & LangGraph")


def render_header() -> None:
    """Render page header."""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title("🎓 KCL Student Bot")
        st.caption("Your AI Assistant for King's College London")

    # Auth button will be rendered in col2 by auth_button.py
