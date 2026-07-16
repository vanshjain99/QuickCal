import logging
import datetime
from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.schemas import TimetableEvent, DayOfWeek

# Configure logger
logger = logging.getLogger("quickcal.calendar_service")

# Map DayOfWeek enum to Google Calendar 2-letter RRULE codes
DAY_TO_RRULE_CODE = {
    DayOfWeek.MONDAY: "MO",
    DayOfWeek.TUESDAY: "TU",
    DayOfWeek.WEDNESDAY: "WE",
    DayOfWeek.THURSDAY: "TH",
    DayOfWeek.FRIDAY: "FR",
    DayOfWeek.SATURDAY: "SA",
    DayOfWeek.SUNDAY: "SU"
}

def get_next_occurrence_date(day: DayOfWeek) -> datetime.date:
    """
    Calculates the date of the next occurrence of a weekday starting from today.
    If today is that weekday, returns today's date.
    """
    weekday_index_map = {
        DayOfWeek.MONDAY: 0,
        DayOfWeek.TUESDAY: 1,
        DayOfWeek.WEDNESDAY: 2,
        DayOfWeek.THURSDAY: 3,
        DayOfWeek.FRIDAY: 4,
        DayOfWeek.SATURDAY: 5,
        DayOfWeek.SUNDAY: 6
    }
    
    target_idx = weekday_index_map[day]
    today = datetime.date.today()
    current_idx = today.weekday() # Monday = 0, Sunday = 6
    
    days_ahead = target_idx - current_idx
    if days_ahead < 0:
        days_ahead += 7 # Target day is in the next week
        
    return today + datetime.timedelta(days=days_ahead)

def sync_events_to_calendar(access_token: str, events: List[TimetableEvent], timezone: str, calendar_name: str) -> int:
    """
    Authenticates with Google Calendar API using the provided OAuth2 access token,
    creates a dedicated secondary calendar with the specified name, and
    inserts the list of TimetableEvent models with weekly recurrence rules and color-coding.
    
    Returns the count of successfully created events.
    """
    logger.info(f"Starting calendar sync for {len(events)} events with timezone '{timezone}' and calendar name '{calendar_name}'.")
    
    # 1. Instantiate OAuth2 Credentials with the access token
    creds = Credentials(token=access_token)
    
    # 2. Build the Google Calendar API Service client
    service = build('calendar', 'v3', credentials=creds)
    
    # 3. Create a secondary calendar with the custom name
    try:
        logger.info(f"Creating secondary calendar: '{calendar_name}'")
        calendar_meta = {
            'summary': calendar_name,
            'timeZone': timezone
        }
        created_calendar = service.calendars().insert(body=calendar_meta).execute()
        calendar_id = created_calendar['id']
        logger.info(f"Successfully created secondary calendar with ID: {calendar_id}")
    except Exception as e:
        logger.error(f"Failed to create secondary calendar: {str(e)}", exc_info=True)
        raise e
        
    success_count = 0
    
    for event in events:
        try:
            # Determine the start date (the next upcoming occurrence of the primary day_of_week)
            start_date = get_next_occurrence_date(event.day_of_week)
            
            # Parse times (expecting HH:MM format)
            shour, sminute = map(int, event.start_time.split(':'))
            ehour, eminute = map(int, event.end_time.split(':'))
            
            # Combine date and times
            start_datetime = datetime.datetime.combine(start_date, datetime.time(shour, sminute))
            end_datetime = datetime.datetime.combine(start_date, datetime.time(ehour, eminute))
            
            # Map weekly repeat days to Google Calendar RRULE codes
            rrule_days = []
            for repeat_day in event.weekly_days:
                if repeat_day in DAY_TO_RRULE_CODE:
                    rrule_days.append(DAY_TO_RRULE_CODE[repeat_day])
            
            # Fallback to primary day_of_week if weekly_days is empty
            if not rrule_days:
                rrule_days.append(DAY_TO_RRULE_CODE[event.day_of_week])
                
            byday_str = ",".join(rrule_days)
            recurrence_rule = f"RRULE:FREQ=WEEKLY;BYDAY={byday_str}"
            
            # Get event color_id (use event's color_id if valid, fallback to Graphite '8')
            color_id = event.color_id if event.color_id and event.color_id.isdigit() else "8"
            
            # Construct Google Calendar Event Resource JSON
            gcal_event: Dict[str, Any] = {
                'summary': event.title,
                'location': event.location or '',
                'description': 'Synced automatically via Schedule to Calendar AI Utility.',
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': timezone,
                },
                'recurrence': [
                    recurrence_rule
                ],
                'colorId': color_id,
                'reminders': {
                    'useDefault': True,
                }
            }
            
            # Insert the event into user's secondary calendar
            logger.info(f"Inserting event: '{event.title}' on {event.day_of_week} ({event.start_time} - {event.end_time}) repeating on {byday_str} in calendar {calendar_id}")
            service.events().insert(calendarId=calendar_id, body=gcal_event).execute()
            
            success_count += 1
            
        except Exception as e:
            logger.error(f"Failed to sync event '{event.title}': {str(e)}", exc_info=True)
            raise e
            
    return success_count
