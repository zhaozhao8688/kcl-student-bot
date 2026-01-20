"""Session management for the KCL Student Bot.

Handles session creation, storage, and retrieval. Currently uses in-memory storage
but can be easily extended to use Redis or Supabase for production.
"""

import uuid
from typing import Optional, Dict
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Session:
    """Represents a user session."""
    session_id: str
    ical_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    message_count: int = 0


class SessionManager:
    """Manages user sessions in memory.

    For production, this should be replaced with Redis or Supabase storage.
    """

    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    def create_session(self) -> str:
        """Create a new session and return its ID."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = Session(session_id=session_id)
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve a session by ID."""
        return self._sessions.get(session_id)

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self._sessions

    def set_ical_url(self, session_id: str, ical_url: str) -> None:
        """Set the iCal URL for a session."""
        session = self.get_session(session_id)
        if session:
            session.ical_url = ical_url
        else:
            # Create session if it doesn't exist
            self._sessions[session_id] = Session(
                session_id=session_id,
                ical_url=ical_url
            )

    def get_ical_url(self, session_id: str) -> Optional[str]:
        """Get the iCal URL for a session."""
        session = self.get_session(session_id)
        return session.ical_url if session else None

    def increment_message_count(self, session_id: str) -> None:
        """Increment the message count for a session."""
        session = self.get_session(session_id)
        if session:
            session.message_count += 1

    def delete_session(self, session_id: str) -> None:
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """Clean up sessions older than max_age_hours.

        Returns the number of sessions deleted.
        """
        from datetime import timedelta

        now = datetime.now()
        cutoff = now - timedelta(hours=max_age_hours)

        old_sessions = [
            sid for sid, session in self._sessions.items()
            if session.created_at < cutoff
        ]

        for sid in old_sessions:
            del self._sessions[sid]

        return len(old_sessions)


# Global session manager instance
session_manager = SessionManager()
