from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class TimetableEvent(BaseModel):
    """
    Represents a single class/lecture event extracted from a timetable.
    """
    title: str = Field(
        ..., 
        description="Name of the class, lecture, seminar, or event."
    )
    day_of_week: DayOfWeek = Field(
        ..., 
        description="Day of the week the event occurs on. Must strictly be one of the uppercase weekdays (e.g., MONDAY)."
    )
    start_time: str = Field(
        ..., 
        description="Start time of the event in 24-hour HH:MM format, zero-padded (e.g., '09:00', '13:30')."
    )
    end_time: str = Field(
        ..., 
        description="End time of the event in 24-hour HH:MM format, zero-padded (e.g., '10:30', '15:00')."
    )
    location: Optional[str] = Field(
        None, 
        description="Room number, building, or location if specified, otherwise None."
    )
    weekly_days: List[DayOfWeek] = Field(
        ...,
        description="List of weekdays on which this event repeats. By default, it contains at least the primary day_of_week."
    )
    category: str = Field(
        ...,
        description="The dynamic grouping category for this event determined by schedule traits (e.g. subject code 'CS 401', professor name, or shift type)."
    )
    color_id: str = Field(
        ...,
        description="Google Calendar event colorId (a string representation of integers '1' through '11') used to visually group related events."
    )

class ScheduleExtractionResponse(BaseModel):
    """
    Wrapper schema containing the list of all parsed timetable events and a contextual name for the schedule.
    """
    calendar_name: str = Field(
        ...,
        description="A contextual name for the schedule calendar (e.g. 'Fall 2026 - B.Tech CSE', 'Shift Chart - Q3') parsed from headers/logos/titles."
    )
    events: List[TimetableEvent] = Field(
        ..., 
        description="List of all extracted timetable events."
    )


