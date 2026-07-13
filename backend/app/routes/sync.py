import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.schemas import TimetableEvent
from app.services.calendar import sync_events_to_calendar

logger = logging.getLogger("schedule_to_calendar.sync")

router = APIRouter(prefix="/api/v1", tags=["Synchronization"])

class CalendarSyncRequest(BaseModel):
    """
    Request model containing the OAuth2 access token and events list to sync.
    """
    access_token: str = Field(
        ...,
        description="Google OAuth2 access token provided by the frontend authentication flow."
    )
    events: List[TimetableEvent] = Field(
        ...,
        description="List of parsed schedule events to sync to the user's Google Calendar."
    )
    timezone: Optional[str] = Field(
        "Asia/Kolkata",
        description="Standard IANA timezone string for the synced calendar events (e.g. 'Asia/Kolkata', 'America/New_York')."
    )

@router.post("/sync")
async def sync_timetable(request: CalendarSyncRequest):
    """
    Synchronizes the list of timetable events directly to the user's primary Google Calendar.
    """
    try:
        synced_count = sync_events_to_calendar(
            access_token=request.access_token,
            events=request.events,
            timezone=request.timezone or "Asia/Kolkata"
        )
        return {
            "status": "success",
            "message": f"Successfully synchronized {synced_count} event(s) to Google Calendar.",
            "synced_count": synced_count
        }
    except Exception as e:
        logger.error(f"Error during Google Calendar sync endpoint call: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to synchronize events to Google Calendar: {str(e)}"
        )
