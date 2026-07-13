# QuickCal Frontend: Astro & Tailwind CSS Web Client

This is the frontend client for **QuickCal**, built using Astro (v7.0) and styled with Tailwind CSS (v4). It provides a responsive, single-page application dashboard to upload schedule documents, inspect parsed events, and synchronize them with Google Calendar via the Google Identity Services OAuth 2.0 flow.

---

## 🎨 Design and Key Features

- **Drag-and-Drop Uploader**: An interactive file uploader widget supporting images, PDFs, and spreadsheets.
- **Glassmorphic UI**: Sleek, modern dashboard UI with fluid animations, custom card layouts, and a responsive grid structure.
- **Dark/Light Mode Sync**: Immediate theme switching using standard color-scheme classes and `localStorage` caching to prevent FOUC (Flash of Unstyled Content).
- **Interactive Review Table**: Allow users to edit, add, or delete timetable events (times, days, titles, locations) in real-time before syncing.
- **Google Identity Services integration**: Seamless client-side authentication requesting temporary calendar permissions.
- **SEO & Discoverability**: Integrated `@astrojs/sitemap` and dynamic `robots.txt` configuration to maximize web crawler visibility.

---

## 📁 Folder Structure

```text
frontend/
├── public/                    # Static assets
│   ├── favicon.svg            # Site vector favicon
│   └── site.webmanifest       # Web application manifest
├── src/
│   ├── components/
│   │   ├── UploadZone.astro   # Drag-and-drop file uploader & fetch integration
│   │   └── Welcome.astro      # Optional landing welcome section
│   ├── layouts/
│   │   └── Layout.astro       # Master HTML layout, SEO meta tags, navigation & footer
│   ├── pages/
│   │   ├── about.astro        # Team/Project description page
│   │   ├── contact.astro      # Contact form endpoint
│   │   ├── faq.astro          # FAQ Accordion component
│   │   ├── index.astro        # Dashboard and primary schedule processing engine
│   │   ├── privacy.astro      # Privacy policy
│   │   ├── terms.astro        # Terms and conditions page
│   │   └── robots.txt.ts      # Dynamic robot metadata generation endpoint
│   └── styles/
│       └── global.css         # Global Tailwind directives & theme tokens
├── astro.config.mjs           # Astro integration configurations
├── package.json               # Node dependencies and build scripts
└── tsconfig.json              # TypeScript compilation setup
```

---

## 🛠️ Getting Started

### Prerequisites
- **Node.js** v22.12.0 or higher.
- A running instance of the calendarimport.com Backend (see the root [README](../README.md)).

### Installation

1. Install the NPM packages:
   ```bash
   npm install
   ```

2. Create a `.env` file at the root of the `frontend/` directory:
   ```env
   PUBLIC_GOOGLE_CLIENT_ID=your-google-oauth-client-id.apps.googleusercontent.com
   ```

3. Launch the development server:
   ```bash
   npm run dev
   ```
   The site will be available at `http://localhost:4321`.

### Commands

| Command | Action |
|:---|:---|
| `npm run dev` | Runs the Astro development server |
| `npm run build` | Compiles the production-ready static assets to `./dist/` |
| `npm run preview` | Runs a local web server to preview the built `./dist/` files |

---

## ⚡ Build Optimizations

When running `npm run build`, Astro will compile the static site inside `dist/`. The following optimizations are completed automatically:
- HTML/CSS bundle minification.
- Static generation of all marketing pages (`about`, `faq`, `contact`, `privacy`, `terms`).
- Production generation of the dynamic `/robots.txt` and XML sitemaps (`sitemap-index.xml`, `sitemap-0.xml`).
