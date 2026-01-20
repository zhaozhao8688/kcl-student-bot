"""Session API endpoints."""

from fastapi import APIRouter, HTTPException
from models.session import SessionResponse, SessionStatus
from core.session import session_manager
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/create", response_model=SessionResponse)
async def create_session():
    """
    Create a new session.

    Returns:
        SessionResponse with new session_id
    """
    try:
        session_id = session_manager.create_session()
        logger.info(f"Created new session: {session_id}")

        return SessionResponse(session_id=session_id)

    except Exception as e:
        logger.error(f"Error creating session: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create session: {str(e)}"
        )


@router.get("/status/{session_id}", response_model=SessionStatus)
async def get_session_status(session_id: str):
    """
    Get the status of a session.

    Args:
        session_id: Session identifier

    Returns:
        SessionStatus with session details
    """
    try:
        session = session_manager.get_session(session_id)

        if not session:
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found"
            )

        return SessionStatus(
            session_id=session.session_id,
            has_ical_url=session.ical_url is not None,
            message_count=session.message_count,
            created_at=session.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get session status: {str(e)}"
        )


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session.

    Args:
        session_id: Session identifier

    Returns:
        Success response
    """
    try:
        if not session_manager.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found"
            )

        session_manager.delete_session(session_id)
        logger.info(f"Deleted session: {session_id}")

        return {
            "success": True,
            "message": f"Session {session_id} deleted"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete session: {str(e)}"
        )
