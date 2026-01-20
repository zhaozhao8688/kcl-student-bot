"""
Authentication button component.
"""

import streamlit as st
from auth.session_manager import SessionManager
from auth.microsoft_sso import microsoft_sso
from utils.logger import setup_logger

logger = setup_logger(__name__)


def render_auth_button() -> None:
    """Render login/logout button based on authentication status."""

    if SessionManager.is_authenticated():
        # Show user info and logout button
        user_info = st.session_state.get("user_info", {})
        user_name = user_info.get("displayName", "User")

        with st.container():
            st.write(f"👤 {user_name}")
            if st.button("🚪 Logout", use_container_width=True):
                SessionManager.logout()
                st.success("Logged out successfully!")
                st.rerun()
    else:
        # Show login button
        if st.button("🔐 Login with Microsoft", use_container_width=True, type="primary"):
            # Generate auth URL
            auth_url = microsoft_sso.get_auth_url()

            # Display info and link
            st.info("Please click the link below to login with your KCL Microsoft account:")
            st.markdown(f"[**Login Here**]({auth_url})")

            st.warning("""
            **Note:** After logging in with Microsoft, you'll be redirected.
            Copy the URL you're redirected to and use the 'Handle Redirect' section below.
            """)

        # Handle OAuth redirect
        with st.expander("🔄 Handle Redirect After Login"):
            redirect_url = st.text_input(
                "Paste the redirect URL here:",
                placeholder="http://localhost:8501?code=..."
            )

            if st.button("Process Login"):
                if redirect_url and "code=" in redirect_url:
                    try:
                        # Extract authorization code
                        code = redirect_url.split("code=")[1].split("&")[0]

                        # Acquire token
                        token_response = microsoft_sso.acquire_token(code)

                        if token_response and "access_token" in token_response:
                            access_token = token_response["access_token"]

                            # Get user info
                            user_info = microsoft_sso.get_user_info(access_token)

                            if user_info:
                                # Login
                                SessionManager.login(user_info, access_token)
                                st.success(f"Welcome, {user_info.get('displayName', 'User')}!")
                                st.rerun()
                            else:
                                st.error("Failed to retrieve user information.")
                        else:
                            st.error("Failed to acquire access token.")
                    except Exception as e:
                        logger.error(f"Login error: {str(e)}")
                        st.error("Login failed. Please try again.")
                else:
                    st.warning("Please paste a valid redirect URL containing the authorization code.")
