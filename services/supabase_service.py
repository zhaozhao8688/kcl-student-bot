"""
Supabase database service for chat history and user sessions.
"""

from supabase import create_client, Client
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SupabaseService:
    """Service for interacting with Supabase database."""

    def __init__(self):
        """Initialize Supabase client."""
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        logger.info("Supabase service initialized")

    def save_chat_message(
        self,
        user_id: str,
        role: str,
        content: str,
        session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Save a chat message to the database.

        Args:
            user_id: User identifier
            role: Message role (user/assistant)
            content: Message content
            session_id: Session identifier

        Returns:
            Saved message data or None if error
        """
        try:
            data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "role": role,
                "content": content,
                "session_id": session_id,
                "created_at": datetime.utcnow().isoformat()
            }

            result = self.client.table("chat_messages").insert(data).execute()
            logger.info(f"Saved chat message for user: {user_id}")
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"Error saving chat message: {str(e)}")
            return None

    def get_chat_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Retrieve chat history for a session.

        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries
        """
        try:
            result = self.client.table("chat_messages") \
                .select("*") \
                .eq("session_id", session_id) \
                .order("created_at", desc=False) \
                .limit(limit) \
                .execute()

            logger.info(f"Retrieved {len(result.data)} messages for session: {session_id}")
            return result.data

        except Exception as e:
            logger.error(f"Error retrieving chat history: {str(e)}")
            return []

    def save_user_session(
        self,
        user_id: str,
        session_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Save or update user session data.

        Args:
            user_id: User identifier
            session_data: Session data to save

        Returns:
            Saved session data or None if error
        """
        try:
            data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "session_data": session_data,
                "last_active": datetime.utcnow().isoformat(),
                "created_at": datetime.utcnow().isoformat()
            }

            result = self.client.table("user_sessions").upsert(data).execute()
            logger.info(f"Saved session for user: {user_id}")
            return result.data[0] if result.data else None

        except Exception as e:
            logger.error(f"Error saving user session: {str(e)}")
            return None

    def get_user_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user session data.

        Args:
            user_id: User identifier

        Returns:
            Session data or None if not found
        """
        try:
            result = self.client.table("user_sessions") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("last_active", desc=True) \
                .limit(1) \
                .execute()

            if result.data:
                logger.info(f"Retrieved session for user: {user_id}")
                return result.data[0]
            return None

        except Exception as e:
            logger.error(f"Error retrieving user session: {str(e)}")
            return None


# Singleton instance
supabase_service = SupabaseService()
