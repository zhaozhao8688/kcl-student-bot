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
        - 📅 Access your timetable
        - 💡 Get personalized help

        ### How to Use
        1. Type your question in the chat
        2. For timetable access, paste your iCal URL below
        3. Ask anything about KCL!
        """)

        st.divider()

        # Timetable iCal URL input
        st.subheader("📅 Timetable Setup")
        st.markdown("Paste your Scientia timetable iCal URL:")

        from auth.session_manager import SessionManager

        current_url = SessionManager.get_ical_url()
        ical_url = st.text_area(
            "iCal Subscription URL",
            value=current_url,
            height=150,
            placeholder="https://scientia-eu-v4-api-d4-02.azurewebsites.net/api/ical/ca05f91a-6c36-45db-9b40-6d011398ed58/3cdaebfe-203e-72d4-7a79-...",
            help="Get this from your KCL timetable → Subscribe → Manual subscription"
        )

        if st.button("💾 Save Timetable URL", use_container_width=True, type="primary"):
            if ical_url and ical_url.strip():
                url = ical_url.strip()
                # Basic validation
                if url.startswith("http") and "ical" in url.lower():
                    SessionManager.set_ical_url(url)
                    st.success("✅ Timetable URL saved!")
                    st.rerun()
                else:
                    st.error("⚠️ This doesn't look like a valid iCal URL. Please check and try again.")
            else:
                st.warning("Please enter a valid URL")

        if SessionManager.has_ical_url():
            st.success("✅ Timetable connected")
            # Show part of the URL for confirmation
            saved_url = SessionManager.get_ical_url()
            st.caption(f"URL: {saved_url[:60]}..." if len(saved_url) > 60 else saved_url)
            if st.button("🗑️ Remove Timetable", use_container_width=True):
                SessionManager.set_ical_url("")
                st.rerun()

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
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
