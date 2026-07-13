# calendarimport.com Backend: FastAPI & Gemini AI Server

This is the backend API service for **calendarimport.com**, built with FastAPI. It handles parsing and extracting timetable events from screenshots, images, PDFs, and spreadsheets using Google's Gemini LLMs, and coordinates direct synchronization of events to Google Calendar.

---

## ⚙️ Core Responsibilities

- **Gemini Extraction Pipeline**: Orchestrates calls to the `google-genai` SDK, using the `gemini-3.1-flash-lite` model with a strict Pydantic schema structure to guarantee valid JSON outputs.
- **Excel & Document Parsing**: Extracts tabular data from Excel files using Pandas and forwards clean CSV strings to Gemini, reducing LLM token overhead and maximizing parsing accuracy.
- **Google Calendar Sync**: Reconstructs recurring event payloads, maps days to RFC 5545 recurrence rules (`RRULE`), and inserts them into the user's primary Google Calendar via the Google Calendar API client.
- **Structured Validation**: Validates incoming schemas and responses using Pydantic models.

---

## 📁 Folder Structure

```text
backend/
├── app/
│   ├── routes/
│   │   ├── contact.py         # Handles support requests and feedback
│   │   ├── extract.py         # Receives documents, calls Gemini API, returns parsed events
│   │   └── sync.py            # Interfaces with Google Calendar API using client-provided token
│   ├── schemas/
│   │   └── __init__.py        # Pydantic schemas (TimetableEvent, ScheduleExtractionResponse)
│   ├── services/
│   │   ├── __init__.py
│   │   └── calendar.py        # Calendar client builder & recurrence formatting rules
│   └── main.py                # FastAPI app initialization, middleware, and CORS configuration
├── .env                       # Local environment secrets (not committed)
├── requirements.txt           # Python package dependencies
├── test_extract.py            # Command-line testing utility for the extraction endpoint
└── README.md                  # Backend architecture and setup documentation
```

---

## 🚀 Setup & Execution

### Prerequisites
- **Python 3.11** or higher.
- A **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/)).

### Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment secrets:
   Create a `.env` file inside `backend/`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend API will run locally at `http://127.0.0.1:8000` with Swagger docs available at `/docs`.

---

## 🧪 API Endpoints

- **`POST /api/v1/extract`**: Accepts a multipart form file upload (`png`, `jpg`, `jpeg`, `pdf`, `xls`, `xlsx`) and returns structured JSON with extracted events.
- **`POST /api/v1/sync`**: Syncs the array of events to Google Calendar. Requires a valid Google OAuth access token and timezone identifier.
- **`POST /api/v1/contact`**: Simple messaging/contact endpoint.
- **`GET /health`**: Operational vitality and health check endpoint.
