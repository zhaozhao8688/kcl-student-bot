"""
KCL Student Bot - Main Streamlit Application
"""

import streamlit as st
from auth.session_manager import SessionManager
from ui.components import render_header, render_sidebar
from ui.auth_button import render_auth_button
from ui.chat_interface import render_chat_interface, render_settings_panel
from utils.logger import setup_logger

logger = setup_logger(__name__)


# Page configuration
st.set_page_config(
    page_title="KCL Student Bot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 2rem;
    }

    /* Header styling */
    h1 {
        color: #0072CE;
    }

    /* Chat messages */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 0.5rem;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    logger.info("Starting KCL Student Bot")

    # Initialize session
    SessionManager.initialize()

    # Render header
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title("🎓 KCL Student Bot")
        st.caption("Your AI Assistant for King's College London")

    with col2:
        render_auth_button()

    st.divider()

    # Render sidebar
    render_sidebar()

    # Render settings panel if authenticated
    render_settings_panel()

    # Render main chat interface
    render_chat_interface()

    # Footer
    st.divider()
    st.caption("KCL Student Bot v1.0.0 | Powered by OpenRouter, LangGraph & Streamlit")


if __name__ == "__main__":
    main()
