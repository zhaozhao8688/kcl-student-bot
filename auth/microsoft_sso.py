"""
Microsoft SSO authentication using MSAL.
"""

from msal import ConfidentialClientApplication
from typing import Optional, Dict, Any
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MicrosoftSSO:
    """Handle Microsoft SSO authentication."""

    def __init__(self):
        """Initialize MSAL Confidential Client Application."""
        self.client_id = settings.microsoft_client_id
        self.client_secret = settings.microsoft_client_secret
        self.authority = settings.microsoft_authority
        self.redirect_uri = settings.microsoft_redirect_uri
        self.scopes = settings.microsoft_scopes

        self.app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority
        )
        logger.info("Microsoft SSO initialized")

    def get_auth_url(self, state: Optional[str] = None) -> str:
        """
        Get the authorization URL for user login.

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            Authorization URL
        """
        auth_url = self.app.get_authorization_request_url(
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
            state=state
        )
        logger.info("Generated auth URL")
        return auth_url

    def acquire_token(self, auth_code: str) -> Optional[Dict[str, Any]]:
        """
        Acquire access token using authorization code.

        Args:
            auth_code: Authorization code from callback

        Returns:
            Token response dictionary or None if error
        """
        try:
            result = self.app.acquire_token_by_authorization_code(
                code=auth_code,
                scopes=self.scopes,
                redirect_uri=self.redirect_uri
            )

            if "access_token" in result:
                logger.info("Successfully acquired access token")
                return result
            else:
                error = result.get("error", "Unknown error")
                logger.error(f"Failed to acquire token: {error}")
                return None

        except Exception as e:
            logger.error(f"Error acquiring token: {str(e)}")
            return None

    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from Microsoft Graph API.

        Args:
            access_token: Valid access token

        Returns:
            User info dictionary or None if error
        """
        try:
            import requests

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=headers
            )

            if response.status_code == 200:
                user_info = response.json()
                logger.info(f"Retrieved user info for: {user_info.get('userPrincipalName')}")
                return user_info
            else:
                logger.error(f"Failed to get user info: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            return None

    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Refresh an expired access token.

        Args:
            refresh_token: Refresh token

        Returns:
            New token response or None if error
        """
        try:
            result = self.app.acquire_token_by_refresh_token(
                refresh_token=refresh_token,
                scopes=self.scopes
            )

            if "access_token" in result:
                logger.info("Successfully refreshed token")
                return result
            else:
                logger.error("Failed to refresh token")
                return None

        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return None


# Singleton instance
microsoft_sso = MicrosoftSSO()
