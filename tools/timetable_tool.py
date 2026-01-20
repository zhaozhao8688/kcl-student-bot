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
            logger.info(f"Fetching timetable from iCal URL")

            # Fetch iCal data
            response = requests.get(ical_url)
            if response.status_code != 200:
                logger.error(f"Failed to fetch iCal: {response.status_code}")
                return []

            # Parse calendar
            cal = Calendar.from_ical(response.content)

            # Filter events
            now = datetime.now()
            end_date = now + timedelta(days=days_ahead)
            events = []

            for component in cal.walk():
                if component.name == "VEVENT":
                    dtstart = component.get("dtstart").dt

                    # Convert to datetime if date only
                    if isinstance(dtstart, datetime):
                        event_date = dtstart
                    else:
                        event_date = datetime.combine(dtstart, datetime.min.time())

                    # Filter by date range
                    if now <= event_date <= end_date:
                        events.append({
                            "summary": str(component.get("summary", "Untitled")),
                            "start": event_date,
                            "location": str(component.get("location", "")),
                            "description": str(component.get("description", ""))
                        })

            # Sort by start time
            events.sort(key=lambda x: x["start"])

            logger.info(f"Found {len(events)} upcoming events")
            return events

        except Exception as e:
            logger.error(f"Error fetching timetable: {str(e)}")
            return []

    def requires_auth(self) -> bool:
        """Timetable tool requires authentication."""
        return True
