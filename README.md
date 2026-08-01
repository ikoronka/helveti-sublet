# Helvéti Sublet

A Zurich apartment listing aggregator with smart filters that native platforms don't offer.

Scrapes Flatfox and ImmoScout24, extracts structured fields from German/English listing descriptions using regex + Gemini, and lets you filter by furnished status, gender preference, sublet dates, and commute time.

<!-- TODO: add screenshots -->

---

## Features

- **Aggregated listings** from Flatfox and ImmoScout24 in one place
- **Smart filters** extracted from free-text descriptions:
  - Furnished / unfurnished
  - Gender preference (female-only, male-only)
  - Sublet vs. long-term
  - Available from / to dates
- **Price and room filters**
- **Commute-time filter** — enter a work address and max minutes by transit, driving, or cycling *(in progress)*

---

## Tech stack

| Layer | Tech |
|---|---|
| Frontend | Vue 3 + TypeScript + Tailwind CSS + Pinia |
| Backend | Python + FastAPI + Strawberry GraphQL |
| Database | SQLite via SQLAlchemy (async) |
| Scraping | httpx (Flatfox) + Playwright (ImmoScout24) |
| Extraction | Regex + Gemini API fallback |
| Package managers | pnpm (frontend) · uv (backend) |

---

## Prerequisites

- Node.js 20+ and pnpm
- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com) with `qwen2.5:3b-instruct` pulled (`ollama pull qwen2.5:3b-instruct`)

---

## Setup

### 1. Clone

```bash
git clone https://github.com/your-username/helveti-sublet.git
cd helveti-sublet
```

### 2. Backend

```bash
cd backend
cp ../.env.example .env
# Edit .env and add your GEMINI_API_KEY

uv sync                     # install dependencies
uv run uvicorn main:app --reload
# → API running at http://localhost:8000
# → GraphQL playground at http://localhost:8000/graphql
```

### 3. Frontend

```bash
cd frontend
pnpm install
pnpm dev
# → App running at http://localhost:5173
```

---

## Scraping listings

Listings are scraped manually (no scheduler in MVP). Run from the `backend/` directory:

```bash
uv run python -m tasks.scrape_job
```

This runs both scrapers (Flatfox + ImmoScout24), extracts smart fields, and upserts results into the database.

> **ImmoScout24 note:** ImmoScout uses DataDome bot protection. The playwright scraper launches a visible Chrome window — this is expected. The window closes automatically when done.

### Seed with fake data (development)

```bash
uv run python -m tasks.seed
```

---

## Project structure

```
helveti-sublet/
  backend/
    main.py              # FastAPI app
    models.py            # SQLAlchemy ORM models
    gql/                 # GraphQL schema, types, resolvers
    scrapers/            # Flatfox + ImmoScout24 scrapers
    extraction/          # Regex + LLM field extraction
    services/            # Commute time service (search.ch + OSRM)
    tasks/               # CLI entrypoints: scrape_job, seed, import_is24
  frontend/
    src/
      components/
        filters/         # PriceRange, RoomSelector, SmartFilterChips, DateRange, Commute
        listings/        # ListingCard, ListingGrid, SourceBadge
      stores/            # Pinia: filters + listings state
      views/             # ListingsView (main page)
  .env.example           # Environment variable reference
```

---

## Environment variables

See [`.env.example`](.env.example). Copy it to `backend/.env`:

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | No | SQLite path (default: `sqlite+aiosqlite:///./helveti.db`) |
