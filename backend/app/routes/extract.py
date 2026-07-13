import os
import io
import json
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
from google import genai
from google.genai import types
import pandas as pd

from app.schemas import ScheduleExtractionResponse

# Configure logger
logger = logging.getLogger("quickcal.extract")

router = APIRouter(prefix="/api/v1", tags=["Extraction"])

# Initialize Gemini client
# API Key is loaded from environment variables (configured via python-dotenv in main.py)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@router.post("/extract", response_model=ScheduleExtractionResponse)
async def extract_schedule(file: UploadFile = File(...)):
    """
    Endpoint that receives an uploaded schedule file (Image, PDF, or Excel),
    securely interfaces with Google AI Studio, enforces strict structured JSON compliance,
    and returns the extracted weekly events.
    """
    content_type = file.content_type or ""
    filename = file.filename or ""

    logger.info(f"Received file extraction request. Filename: {filename}, Content-Type: {content_type}")

    # Determine file type
    is_image = content_type.startswith("image/")
    is_pdf = content_type == "application/pdf" or filename.endswith(".pdf")
    is_excel = content_type in [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/octet-stream"
    ] or filename.endswith((".xls", ".xlsx"))

    # Strict guard check for supported content types
    if not (is_image or is_pdf or is_excel):
        logger.error(f"Unsupported file format: {content_type}")
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a PNG, JPG, JPEG, PDF, or Excel file."
        )

    # Rigorous system prompt instructing Gemini on 2D document layout analysis and grid alignment
    system_prompt = (
        "You are an expert schedule extraction system. Analyze the provided document containing a weekly timetable or schedule. "
        "It might be structured as a 2D grid where columns represent days of the week "
        "and rows represent time slots, or vice versa, or lists of classes/appointments. "
        "Your task is to perform advanced 2D document layout analysis and grid alignment: cross-reference "
        "column boundaries (days of the week) against row boundaries (time slots or class periods) to extract every weekly event. "
        "For each event, extract the following fields:\n"
        "1. title: The name of the class, lecture, seminar, or event.\n"
        "2. day_of_week: The day it occurs on. Must strictly be one of: MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY. This MUST be in STRICT UPPERCASE (e.g., 'MONDAY', not 'Monday' or 'monday').\n"
        "3. start_time: The start time in zero-padded 24-hour HH:MM format (e.g. '09:00', '13:30').\n"
        "4. end_time: The end time in zero-padded 24-hour HH:MM format (e.g. '10:30', '15:00').\n"
        "5. location: The room number or building if present, otherwise set to null.\n"
        "6. weekly_days: List of weekdays on which this event repeats. It must be populated as an array of uppercase day strings (e.g., ['MONDAY', 'WEDNESDAY']). By default, it contains the primary weekday (day_of_week). If the timetable layout explicitly indicates that the exact same class/event at the exact same time block repeats on other days (e.g., a Monday/Wednesday sequence for the same course), include all those days in this array list.\n\n"
        "Be extremely careful to trace headers, cells, and grid lines to map events to their correct day and time slots."
    )

    try:
        if is_excel:
            # For Excel files, read bytes into pandas and pass as structured text representation
            file_bytes = await file.read()
            df = pd.read_excel(io.BytesIO(file_bytes))
            # Convert to CSV table format (native, requires no optional dependencies like tabulate)
            csv_table = df.to_csv(index=False)
            
            prompt = (
                f"{system_prompt}\n\n"
                "Here is the CSV data extracted from the uploaded Excel spreadsheet. "
                "Extract the scheduled events from this data:\n\n"
                f"{csv_table}"
            )
            
            logger.info("Sending Excel text table to Gemini...")
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ScheduleExtractionResponse,
                    temperature=0.1,
                ),
            )
        else:
            # For Images or PDFs, read bytes and send directly as multimedia parts
            file_bytes = await file.read()
            mime_type = "application/pdf" if is_pdf else content_type
            
            logger.info(f"Sending file bytes ({len(file_bytes)} bytes) to Gemini with MIME type: {mime_type}")
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=[
                    types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                    system_prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ScheduleExtractionResponse,
                    temperature=0.1,
                ),
            )

        logger.info("Successfully received response from Gemini")
        # Load and return the structured JSON output
        result_json = json.loads(response.text)
        return result_json

    except json.JSONDecodeError as jde:
        logger.error(f"Failed to parse Gemini JSON response: {jde}")
        raise HTTPException(
            status_code=500,
            detail="Failed to parse structured JSON response from extraction model."
        )
    except Exception as e:
        logger.error(f"Error during schedule extraction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during schedule extraction: {str(e)}"
        )
