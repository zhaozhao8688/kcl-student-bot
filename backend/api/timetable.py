"""Timetable API endpoints."""

from fastapi import APIRouter, HTTPException
from models.session import TimetableUrlRequest, TimetableUrlResponse
from core.session import session_manager
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/set-url")
async def set_timetable_url(request: TimetableUrlRequest):
    """
    Set the iCal URL for a session's timetable.

    Args:
        request: Request containing session_id and ical_url

    Returns:
        Success response
    """
    try:
        logger.info(f"Setting timetable URL for session {request.session_id}")

        # Validate session exists or create it
        if not session_manager.session_exists(request.session_id):
            logger.info(f"Session {request.session_id} does not exist, creating it")

        # Set the iCal URL
        session_manager.set_ical_url(request.session_id, request.ical_url)

        logger.info(f"Successfully set timetable URL for session {request.session_id}")

        return {
            "success": True,
            "message": "Timetable URL set successfully"
        }

    except Exception as e:
        logger.error(f"Error setting timetable URL: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set timetable URL: {str(e)}"
        )


@router.get("/get-url/{session_id}", response_model=TimetableUrlResponse)
async def get_timetable_url(session_id: str):
    """
    Get the iCal URL for a session's timetable.

    Args:
        session_id: Session identifier

    Returns:
        TimetableUrlResponse with ical_url and has_timetable flag
    """
    try:
        ical_url = session_manager.get_ical_url(session_id)

        return TimetableUrlResponse(
            ical_url=ical_url,
            has_timetable=ical_url is not None
        )

    except Exception as e:
        logger.error(f"Error getting timetable URL: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get timetable URL: {str(e)}"
        )
