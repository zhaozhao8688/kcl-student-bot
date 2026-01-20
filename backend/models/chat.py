"""Chat-related Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for sending a chat message."""
    query: str = Field(..., min_length=1, description="User's query message")
    session_id: Optional[str] = Field(None, description="Session ID for continuing conversation")
    ical_url: Optional[str] = Field(None, description="iCal URL for timetable access")


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    response: str = Field(..., description="AI assistant's response")
    session_id: str = Field(..., description="Session ID for the conversation")


class Message(BaseModel):
    """Model representing a single chat message."""
    id: str = Field(..., description="Unique message identifier")
    role: str = Field(..., description="Message role: 'user' or 'ai'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")


class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    messages: list[Message] = Field(default_factory=list, description="List of messages")
    session_id: str = Field(..., description="Session ID")
