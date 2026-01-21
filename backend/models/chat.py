"""Chat-related Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for sending a chat message."""
    query: str = Field(..., min_length=1, description="User's query message")
    session_id: Optional[str] = Field(None, description="Session ID for continuing conversation")
    ical_url: Optional[str] = Field(None, description="iCal URL for timetable access")
    include_steps: Optional[bool] = Field(False, description="Include agent step details in response")
    conversation_history: Optional[List[Dict[str, str]]] = Field(None, description="Previous messages in the conversation")


class AgentStep(BaseModel):
    """Model representing a single agent reasoning step."""
    iteration: int = Field(..., description="Step number in the reasoning loop")
    thought: Optional[str] = Field(None, description="Agent's reasoning/thought process")
    action: Optional[str] = Field(None, description="Action taken (tool name or final_answer)")
    action_input: Optional[Dict[str, Any]] = Field(None, description="Input provided to the action")
    observation: Optional[str] = Field(None, description="Result/observation from the action")
    timestamp: Optional[str] = Field(None, description="When this step occurred")


class AgentDebugInfo(BaseModel):
    """Debug information about the agent's execution."""
    total_iterations: int = Field(..., description="Total number of reasoning iterations")
    tool_calls_count: int = Field(..., description="Number of tools called")
    tools_used: List[str] = Field(default_factory=list, description="List of tools that were used")
    steps: List[AgentStep] = Field(default_factory=list, description="Detailed steps of agent reasoning")


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    response: str = Field(..., description="AI assistant's response")
    session_id: str = Field(..., description="Session ID for the conversation")
    debug: Optional[AgentDebugInfo] = Field(None, description="Agent debug info (if requested)")


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
