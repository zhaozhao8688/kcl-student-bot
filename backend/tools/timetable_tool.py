"""
Timetable tool using iCal subscription.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from icalendar import Calendar
import requests
from tools.base import BaseTool
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TimetableTool(BaseTool):
    """Access KCL timetable via iCal subscription."""

    def __init__(self):
        """Initialize timetable tool."""
        super().__init__(
            name="timetable",
            description="Access and parse KCL student timetable from iCal subscription"
        )

    def execute(
        self,
        ical_url: str,
        days_ahead: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Fetch and parse timetable events.

        Args:
            ical_url: iCal subscription URL
            days_ahead: Number of days ahead to fetch events

        Returns:
            List of event dictionaries
        """
        try:
            logger.info(f"Fetching timetable from iCal URL (length: {len(ical_url)})")

            # Fetch iCal data with timeout
            response = requests.get(ical_url, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to fetch iCal: HTTP {response.status_code}")
                return []

            logger.info(f"Successfully fetched iCal data ({len(response.content)} bytes)")

            # Parse calendar
            cal = Calendar.from_ical(response.content)

            # Filter events
            now = datetime.now()
            end_date = now + timedelta(days=days_ahead)
            events = []
            total_events = 0

            for component in cal.walk():
                if component.name == "VEVENT":
                    total_events += 1
                    try:
                        dtstart = component.get("dtstart")
                        if not dtstart:
                            continue

                        dt = dtstart.dt

                        # Convert to datetime if date only
                        if isinstance(dt, datetime):
                            event_date = dt
                            # Make timezone-naive for comparison
                            if event_date.tzinfo is not None:
                                event_date = event_date.replace(tzinfo=None)
                        else:
                            event_date = datetime.combine(dt, datetime.min.time())

                        # Filter by date range
                        if now <= event_date <= end_date:
                            events.append({
                                "summary": str(component.get("summary", "Untitled")),
                                "start": event_date,
                                "location": str(component.get("location", "")),
                                "description": str(component.get("description", ""))
                            })
                    except Exception as event_error:
                        logger.warning(f"Error parsing event: {event_error}")
                        continue

            # Sort by start time
            events.sort(key=lambda x: x["start"])

            logger.info(f"Found {len(events)} upcoming events out of {total_events} total events")
            return events

        except requests.exceptions.Timeout:
            logger.error("Timeout fetching iCal URL")
            return []
        except requests.exceptions.RequestException as req_error:
            logger.error(f"Network error fetching timetable: {str(req_error)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching timetable: {str(e)}", exc_info=True)
            return []

    def requires_auth(self) -> bool:
        """Timetable tool does not require authentication - only needs iCal URL."""
        return False
