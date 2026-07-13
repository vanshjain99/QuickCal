# calendarimport.com: Schedule to Calendar AI Utility

calendarimport.com is a modern, privacy-focused, and ultra-lean web utility that instantly converts weekly timetables, class schedules, or appointment sheets into recurring events in your Google Calendar. 

Simply upload a screenshot, image, PDF, or Excel spreadsheet of your schedule, verify the extracted details, and sync them directly to your Google Calendar.

---

## 🚀 Key Features

- **AI-Powered Layout Analysis**: Uses Google's **Gemini 3.1 Flash-Lite** to automatically detect 2D grid alignments, days of the week, times, course codes/titles, and classroom locations.
- **Multi-Format Support**: Upload PNG, JPG, JPEG, PDF documents, or Excel (`.xls`, `.xlsx`) spreadsheets.
- **Interactive Review & Editing**: Inspect and edit the extracted classes, times, and recurrences before making them permanent.
- **One-Click Google Calendar Sync**: Integrates with the **Google Calendar API** to automatically schedule recurring weekly events on your calendar.
- **Modern Responsive Design**: A sleek, dark-mode-first dashboard built with Astro, Tailwind CSS, and custom glassmorphic styling.
- **Privacy First**: Processed through secure API pipelines with no persistent storage of your private schedule documents or Google OAuth credentials.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: [Astro 7.0](https://astro.build/) (Static Site Generation / SSG)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Auth & Integration**: Google Identity Services (GIS) OAuth 2.0 & Google Calendar API Client

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **AI Core**: [Google GenAI SDK](https://github.com/google/generative-ai-python)
- **Data Parser**: [Pandas](https://pandas.pydata.org/) & [OpenPyXL](https://openpyxl.readthedocs.io/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)

---

## 📁 Repository Structure

```text
schedule_to_calendar/
├── backend/                   # FastAPI backend application
│   ├── app/
│   │   ├── routes/            # API Router endpoints (extract, sync, contact)
│   │   ├── schemas/           # Pydantic data models & validation
│   │   ├── services/          # Business logic & Google Calendar Service
│   │   └── main.py            # FastAPI entry point
│   ├── .env.example           # Example backend configuration environment file
│   ├── requirements.txt       # Python package dependencies
│   └── test_extract.py        # Backend endpoint tests
├── frontend/                  # Astro frontend application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── layouts/           # Page structures (Layout.astro)
│   │   ├── pages/             # App routing (index, about, contact, faq, privacy, terms)
│   │   └── styles/            # Tailwind Global Styles
│   ├── public/                # Static assets (Favicons, manifests)
│   ├── astro.config.mjs       # Astro configuration (registered sitemap & tailwind)
│   └── package.json           # Node.js dependencies
└── README.md                  # Project overview and developer guide
```

---

## ⚙️ Setup & Configuration

### Prerequisites
- **Node.js** (v22.12.0 or higher)
- **Python** (v3.11 or higher)
- A **Google Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/))
- A **Google Cloud Console OAuth 2.0 Client ID** (Configured for web applications with the `https://www.googleapis.com/auth/calendar.events` scope. Set Authorized JavaScript Origins to include your local development URL e.g., `http://localhost:4321`).

---

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Add your Google Gemini API Key inside `.env`:
   ```env
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   ```

6. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will be running at `http://127.0.0.1:8000`.

---

### 2. Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install the node packages:
   ```bash
   npm install
   ```

3. Configure your environment variables:
   Create a `.env` file in the `frontend/` directory and configure the Google Client ID:
   ```env
   PUBLIC_GOOGLE_CLIENT_ID=your-google-oauth-client-id-here
   ```

4. Start the frontend local development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:4321` in your browser to access the app.

---

## 🏗️ Production Build

To compile the application for production:

```bash
# Frontend
cd frontend
npm run build
```

This generates a fully optimized static directory in `frontend/dist/`, which contains:
- Pre-rendered static pages
- Pre-compiled assets (JS, CSS, images)
- `sitemap-index.xml` and `sitemap-0.xml` (SEO optimization)
- `robots.txt` (pointing to the sitemap index)

---

## 📄 License

This project is licensed under the calendarimport.com Source-Available & Contribution License - see the [LICENSE](LICENSE) file for details.
