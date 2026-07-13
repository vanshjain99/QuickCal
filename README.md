# QuickCal: Schedule to Calendar AI Utility

QuickCal (available at [calendarimport.com](https://calendarimport.com)) is a modern, privacy-focused, and ultra-lean web utility that instantly converts weekly timetables, class schedules, or appointment sheets into recurring events in your Google Calendar. 

Simply upload a screenshot, image, PDF, or Excel spreadsheet of your schedule, verify the extracted details, and sync them directly to your Google Calendar.

---

## 🚀 Key Features

- **AI-Powered Layout Analysis**: Uses Google's **Gemini 3.1 Flash-Lite** (`gemini-3.1-flash-lite`) via the `google-genai` SDK to automatically perform 2D grid document alignment and layout analysis. It detects weekdays, time slots, course/event titles, and room locations.
- **Multi-Format Support**: Instantly uploads and parses PNG, JPG, JPEG, PDF documents, or Excel (`.xls`, `.xlsx`) spreadsheets.
- **Adaptive Theme Engine**: Built-in theme toggle with `localStorage` caching to eliminate flashing. The site defaults to **Dark Mode on desktop screens** (>=768px) and **Light Mode on mobile screens** to align with platform design aesthetics.
- **Interactive Review Workspace**: A sleek responsive workspace that allows you to inspect, modify, add, or delete extracted schedule events (times, days, titles, locations, and recurrence list) in real-time before syncing.
- **One-Click Google Calendar Sync**: Integrates with the **Google Calendar API** client-side (using Google Identity Services OAuth 2.0 flow) to automatically schedule recurring weekly events on your primary calendar.
- **Support Contact Pipeline**: Integrated contact form submitting queries to a backend SMTP client (with automatic console logging fallback when credentials are not configured).
- **SEO & Discoverability**: Automatic compilation of dynamic XML sitemaps (`sitemap-index.xml`, `sitemap-0.xml`) and dynamic `robots.txt` configuration for search engine crawlers.
- **Privacy First**: Processed through secure ephemeral pipelines. We do not store your uploaded documents, schedule data, or Google OAuth credentials.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: [Astro 7.0](https://astro.build/) (Static Site Generation / SSG)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/) (integrated via `@tailwindcss/vite` plugin)
- **Authentication**: Google Identity Services (GIS) OAuth 2.0 & Google Calendar API Client
- **Deployment**: [Cloudflare Pages](https://pages.cloudflare.com/) (managed via Wrangler CLI)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **AI Integration**: [Google GenAI Python SDK](https://github.com/google/generative-ai-python)
- **Data Parser**: [Pandas](https://pandas.pydata.org/) & [OpenPyXL](https://openpyxl.readthedocs.io/) (for structured Excel processing)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Deployment**: [Docker](https://www.docker.com/) containerized, configured for platforms like [Render](https://render.com/) or [Koyeb](https://www.koyeb.com/)

---

## 📁 Repository Structure

```text
QuickCal/
├── backend/                   # FastAPI backend application
│   ├── app/
│   │   ├── routes/
│   │   │   ├── contact.py     # Handles support form SMTP forwarding & console logs
│   │   │   ├── extract.py     # Gemini OCR extraction endpoint for documents/spreadsheets
│   │   │   └── sync.py        # Receives events and pushes them to Google Calendar API
│   │   ├── schemas.py         # Pydantic validation models (TimetableEvent, DayOfWeek)
│   │   ├── services/
│   │   │   └── calendar.py    # Google Calendar event formatting and recurrence rules
│   │   └── main.py            # FastAPI entry point, middleware, & CORS setup
│   ├── .env.example           # Example backend environment variables
│   ├── Dockerfile             # Multi-stage Docker config with dynamic PORT binding
│   ├── requirements.txt       # Python backend dependencies
│   ├── sample_timetable.xlsx  # Sample schedule spreadsheet for testing
│   └── test_extract.py        # Local command-line parsing testing utility
├── frontend/                  # Astro frontend web client
│   ├── public/                # Static assets (favicons, manifests, etc.)
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.astro # Drag-and-drop file uploader & fetch client
│   │   │   └── Welcome.astro  # Welcome component
│   │   ├── layouts/
│   │   │   └── Layout.astro   # Core HTML skeleton, SEO metadata, theme control
│   │   ├── pages/
│   │   │   ├── 404.astro      # Error 404 page
│   │   │   ├── 500.astro      # Error 500 page
│   │   │   ├── about.astro    # About info page
│   │   │   ├── contact.astro  # Support contact page
│   │   │   ├── faq.astro      # Interactive FAQ accordion page
│   │   │   ├── index.astro    # Main dashboard application and grid workspace
│   │   │   ├── privacy.astro  # Privacy policy
│   │   │   ├── terms.astro    # Terms & conditions page
│   │   │   └── robots.txt.ts  # Dynamic robots.txt metadata generator
│   │   └── styles/
│   │       └── global.css     # CSS variable bindings & Tailwind imports
│   ├── astro.config.mjs       # Astro configuration (Vite, Tailwind v4, & Sitemap)
│   └── package.json           # Node scripts and dependencies
└── README.md                  # Root documentation (this file)
```

---

## ⚙️ Environment Configuration

To run both services, create the respective `.env` files in `backend/` and `frontend/` directories:

### Backend `.env` (`backend/.env`)
```env
# Gemini API Key (from Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# Server Binding
HOST=127.0.0.1
PORT=8000

# Support Inquiry Forwarding
CONTACT_RECEIVER_EMAIL=your_admin_email@example.com

# SMTP Server Configurations (Optional; falls back to console logging if omitted)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_sender_email@gmail.com
SMTP_PASSWORD=your_smtp_app_password_here
```

### Frontend `.env` (`frontend/.env`)
```env
# Google Identity Services Configuration (OAuth 2.0 Client ID)
PUBLIC_GOOGLE_CLIENT_ID=your_oauth_client_id.apps.googleusercontent.com

# Backend API Endpoint URL
PUBLIC_API_URL=http://127.0.0.1:8000
```

---

## 🚀 Getting Started

### 1. Backend Setup & Run

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create and configure your local environment file:
   ```bash
   cp .env.example .env
   # Open .env and add your GEMINI_API_KEY and other parameters
   ```

5. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend API will run locally at `http://127.0.0.1:8000` with Swagger docs available at `http://127.0.0.1:8000/docs`.

---

### 2. Frontend Setup & Run

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node modules:
   ```bash
   npm install
   ```

3. Configure your local `.env` file as specified in the [Environment Configuration](#environment-configuration) section.

4. Start the frontend local development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:4321` in your browser to access the QuickCal dashboard.

---

## ⚡ CLI Commands reference

### Frontend (`frontend/`)
| Command | Action |
|:---|:---|
| `npm run dev` | Runs the Astro development server |
| `npm run build` | Compiles the production-ready static assets to `./dist/` |
| `npm run preview` | Runs a local web server to preview the built `./dist/` files |
| `npm run deploy` | Compiles assets and deploys directly to Cloudflare Pages |

### Backend (`backend/`)
| Command | Action |
|:---|:---|
| `uvicorn app.main:app --reload` | Starts the local API server with hot reloading |
| `python test_extract.py` | Command-line utility to test schedule extraction |

---

## 🐳 Deployment & Containerization

### Dockerizing the Backend
The backend includes a Dockerfile optimized for container platforms (Render, Koyeb, AWS, etc.). 

1. **Build the Docker Image**:
   ```bash
   docker build -t quickcal-backend ./backend
   ```

2. **Run the Container locally**:
   ```bash
   docker run -p 8000:8000 --env-file ./backend/.env quickcal-backend
   ```
   *(Ensure to pass your `GEMINI_API_KEY` either via the env file or directly using `-e GEMINI_API_KEY=key`)*.

### Deploying the Frontend (Cloudflare Pages)
To deploy the Astro frontend static build to Cloudflare Pages, use the built-in Wrangler deploy task:
```bash
cd frontend
npm run deploy
```
This builds your static distribution bundle inside `dist/` (which pre-minifies bundles, structures pages, and writes sitemaps) and uploads it directly to your registered Cloudflare project.

---

## 📄 License

This project is licensed under the QuickCal Source-Available & Contribution License - see the [LICENSE](LICENSE) file for details.
