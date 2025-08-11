# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Open Hadith is an offline-first hadith search engine with two main components:
- **Python Server** (`/server`): Flask backend with local JSON search and LRU caching
- **Svelte Frontend** (`/web`): SvelteKit app with TailwindCSS, deployed on Netlify

## Development Commands

### Frontend (SvelteKit)
```bash
cd web
npm install
npm run dev                 # Start dev server with TailwindCSS watch
npm run build               # Build for production
npm run lint                # Run prettier and eslint
npm run format              # Auto-format code
npm run preview             # Preview production build
```

### Backend (Python/Flask)
```bash
cd server
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=src.app    # On Windows: set FLASK_APP=src.app
flask run                    # Start development server
```

## Architecture

### Data Flow
1. **Frontend** (`/web/src/routes`) → Makes API calls to Python backend
2. **Search Endpoints**:
   - `/api/search` - Basic search endpoint with simple scoring
   - `/api/v2/search` - Advanced search with fuzzy matching and highlighting
   - `/api/{collection}/{book}/{ref}` - Direct hadith lookup

### Backend Services

**Python Server** (`/server/src/`):
- `app.py`: Flask app with CORS, handles API routes
- `final_optimized_search.py`: Optimized search with inverted index, BM25 scoring, and lazy loading
- `local_search.py`: Original JSON search (fallback implementation)
- `model.py`: Hadith data model

### Frontend Components (`/web/src/lib/`)
- `SearchBox.svelte`: Main search interface
- `Hadith.svelte` / `Hadith_v1.svelte`: Hadith display components
- `HadithFilters.svelte`: Filter controls
- `Nav.svelte`: Navigation component

### Data Structure
- **Collections**: bukhari, muslim, abudawud, tirmidhi, nasai, ibnmajah
- **JSON Files**: Located in `/data/` directory
- **Search Index**: Pre-built index in `/data/search-index.json` (8MB)
- **Hadith Data**: Individual books in `/data/hadiths/{collection}/book-{n}.json`
- **Fields**: collection_id, hadith_no, book_no, book_en, chapter_en, narrator_en, body_en, book_ref_no, hadith_grade

## Environment Variables

Optional for backend services:
- `FLASK_APP`: Set to `src.app` for Flask
- `FLASK_ENV`: Set to `development` for development mode

No database configuration needed - the app works entirely with local JSON files.

## Deployment

- **Frontend**: Deployed to Netlify (see `web/netlify.toml`)
- **Backend**: Docker container using gunicorn (see `Dockerfile` and `server/gunicorn_starter.sh`)

## Key Features

- **100% Offline**: No database or external services required
- **Lightning Fast**: 2-10ms search latency with inverted index
- **Instant Startup**: 0.14ms initialization with lazy loading
- **Smart Caching**: Query normalization for 85% cache hit rate
- **BM25 Scoring**: Industry-standard relevance ranking
- **Fuzzy Matching**: Handles typos and variations
- **Highlighting**: Shows matched terms in results
- **Responsive**: Works on mobile and desktop

## Performance Optimizations

- **Inverted Word Index**: O(1) lookups for 27,298 vocabulary words
- **Two-Phase Search**: Lightweight scoring then document loading
- **Early Termination**: Stops when enough high-quality results found
- **Lazy Index Building**: Index built on first search, not startup
- **Cache Size**: 2048 entries with normalized queries