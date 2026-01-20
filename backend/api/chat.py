"""Chat API endpoints."""

from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest, ChatResponse, ChatHistoryResponse, Message
from core.chat_processor import process_chat, get_chat_history
from core.session import session_manager
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Process a chat message and return the AI response.

    Args:
        request: Chat request containing query, session_id, and optional ical_url

    Returns:
        ChatResponse with AI response and session_id
    """
    try:
        # Create or validate session
        if not request.session_id:
            session_id = session_manager.create_session()
            logger.info(f"Created new session: {session_id}")
        else:
            session_id = request.session_id
            if not session_manager.session_exists(session_id):
                # Create session if it doesn't exist
                session_manager._sessions[session_id] = session_manager._sessions.get(
                    session_id,
                    type('Session', (), {
                        'session_id': session_id,
                        'ical_url': None,
                        'message_count': 0
                    })()
                )
                logger.info(f"Session {session_id} did not exist, created it")

        # Get iCal URL from request or session
        ical_url = request.ical_url
        if not ical_url:
            ical_url = session_manager.get_ical_url(session_id)

        # Process the chat message
        response = await process_chat(
            query=request.query,
            session_id=session_id,
            ical_url=ical_url
        )

        # Increment message count
        session_manager.increment_message_count(session_id)

        return ChatResponse(
            response=response,
            session_id=session_id
        )

    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_history(session_id: str, limit: int = 50):
    """
    Retrieve chat history for a session.

    Args:
        session_id: Session identifier
        limit: Maximum number of messages to retrieve (default: 50)

    Returns:
        ChatHistoryResponse with list of messages
    """
    try:
        if not session_manager.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found"
            )

        messages = await get_chat_history(session_id, limit)

        # Convert to Message models
        message_models = [
            Message(
                id=str(msg.get('id', '')),
                role=msg.get('role', 'ai'),
                content=msg.get('content', ''),
                timestamp=msg.get('created_at')
            )
            for msg in messages
        ]

        return ChatHistoryResponse(
            messages=message_models,
            session_id=session_id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve history: {str(e)}"
        )
