"""Session-related Pydantic models."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SessionCreate(BaseModel):
    """Request model for creating a new session."""
    pass


class SessionResponse(BaseModel):
    """Response model for session creation."""
    session_id: str = Field(..., description="Unique session identifier")


class SessionStatus(BaseModel):
    """Model representing session status information."""
    session_id: str = Field(..., description="Session identifier")
    has_ical_url: bool = Field(..., description="Whether session has timetable URL configured")
    message_count: int = Field(default=0, description="Number of messages in session")
    created_at: Optional[datetime] = Field(None, description="Session creation timestamp")


class TimetableUrlRequest(BaseModel):
    """Request model for setting timetable URL."""
    session_id: str = Field(..., description="Session identifier")
    ical_url: str = Field(..., min_length=1, description="iCal URL for timetable")


class TimetableUrlResponse(BaseModel):
    """Response model for timetable URL."""
    ical_url: Optional[str] = Field(None, description="iCal URL if set")
    has_timetable: bool = Field(..., description="Whether timetable is configured")
