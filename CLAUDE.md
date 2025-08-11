# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Open Hadith is a hadith search engine with three main components:
- **Go API** (`/api`): Handles search requests with MongoDB integration and LRU caching
- **Python Server** (`/server`): Flask backend with MongoDB Atlas Search integration
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

### Go API
```bash
go mod download
go run api/search.go         # Run the search handler
```

## Architecture

### Data Flow
1. **Frontend** (`/web/src/routes`) → Makes API calls to either Go or Python backend
2. **Search Endpoints**:
   - `/api/search` - Legacy Python endpoint using text search
   - `/api/v2/search` - Atlas Search endpoint with fuzzy matching and highlighting
   - Go handler provides cached search with direct MongoDB queries

### Backend Services

**Python Server** (`/server/src/`):
- `app.py`: Flask app with CORS, handles API routes
- `atlas_search.py`: MongoDB Atlas Search with compound queries, fuzzy matching, and text highlighting
- `mongo_client.py`: Legacy search using MongoDB text indexes across 6 hadith collections
- `model.py`: Hadith data model

**Go API** (`/api/search.go`):
- LRU cache (512 entries) for search results
- Direct MongoDB queries with pagination (PAGE_SIZE=50)
- Special handling for collection+number queries (e.g., "bukhari 123")

### Frontend Components (`/web/src/lib/`)
- `SearchBox.svelte`: Main search interface
- `Hadith.svelte` / `Hadith_v1.svelte`: Hadith display components
- `HadithFilters.svelte`: Filter controls
- `Nav.svelte`: Navigation component

### Database Structure
- **Collections**: bukhari, muslim, abudawud, tirmidhi, nasai, ibnmajah
- **Fields**: collection_id, hadith_no, book_no, book_en, chapter_en, narrator_en, body_en, book_ref_no, hadith_grade

## Environment Variables

Required for backend services:
- `MONGO_URL`: MongoDB connection string for legacy search
- `ATLAS_URL`: MongoDB Atlas connection string for Atlas Search
- `FLASK_APP`: Set to `src.app` for Flask

## Deployment

- **Frontend**: Deployed to Netlify (see `web/netlify.toml`)
- **Backend**: Docker container using gunicorn (see `Dockerfile` and `server/gunicorn_starter.sh`)