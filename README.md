# Helvéti Sublet 🏠

[Live demo](https://helvetisublet.ikoronka.com/)

A Zurich apartment listing aggregator with smart filters that native platforms don't offer.

It scrapes Flatfox listings, pulls out useful details from the German or English descriptions using regex plus a local LLM, and lets you filter by furnished status, gender preference, sublet dates, and (soon) commute time.

<!-- TODO: add screenshots -->

---

## ✨ Features

- Aggregated listings from Flatfox, all in one place
- Smart filters pulled straight from the free text descriptions:
  - Furnished or unfurnished
  - Gender preference (female-only, male-only)
  - Sublet vs. long-term
  - Available from / to dates
- Price and room filters
- Zurich district (Kreis) filter

---

## 🧱 Tech stack

| Layer | Tech |
|---|---|
| Frontend | Vue 3 + TypeScript + Tailwind CSS + Pinia |
| Backend | Python + FastAPI + Strawberry GraphQL |
| Database | SQLite via SQLAlchemy (async) |
| Scraping | httpx (Flatfox) |
| Extraction | Regex + local LLM fallback (Ollama, qwen2.5:3b-instruct) |
| Package managers | pnpm (frontend) and uv (backend) |

---

## ✅ Prerequisites

- Node.js 20+ and pnpm
- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com) with `qwen2.5:3b-instruct` pulled:
  ```bash
  ollama pull qwen2.5:3b-instruct
  ```

---

## 🚀 Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/helveti-sublet.git
cd helveti-sublet
```

### 2. Backend

```bash
cd backend
cp ../.env.example .env
# defaults work out of the box, only edit .env if you need to override something

uv sync
uv run uvicorn main:app --reload
```

- API: [http://localhost:8000](http://localhost:8000)
- GraphQL playground: [http://localhost:8000/graphql](http://localhost:8000/graphql)

### 3. Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

- App: [http://localhost:5173](http://localhost:5173)

---

## 🔍 Scraping listings

There's no scheduler yet, so listings are scraped by hand. From the `backend/` directory:

```bash
uv run python -m tasks.scrape_job
```

This scrapes Flatfox, extracts the smart fields, and upserts everything into the database.

### Seed with fake data (for local development)

```bash
uv run python -m tasks.seed
```

### Backfill extraction on existing listings

```bash
uv run python -m tasks.backfill_extraction
```

---

## 📁 Project structure

```
helveti-sublet/
  backend/
    main.py              # FastAPI app
    models.py             # SQLAlchemy ORM models
    gql/                   # GraphQL schema, types, resolvers
    scrapers/             # Flatfox scraper
    extraction/           # Regex + LLM field extraction
    tasks/                 # CLI entrypoints: scrape_job, seed, backfill_extraction
  frontend/
    src/
      components/
        filters/          # PriceRange, RoomSelector, SmartFilterChips, DateRange, Kreis
        listings/          # ListingCard, ListingGrid, SourceBadge
      stores/               # Pinia: filters + listings state
      views/                 # ListingsView (main page)
  .env.example            # Environment variable reference
```

---

## ⚙️ Environment variables

See [`.env.example`](.env.example). Copy it to `backend/.env` if you need to change a default.

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | No | SQLite path (default: `sqlite+aiosqlite:///./helveti.db`) |
| `OLLAMA_URL` | No | Ollama endpoint for LLM extraction (default: `http://localhost:11434/api/generate`) |

---

## 🚧 Work in progress

Things that are actively being worked on right now:

- **Postgres migration**: moving off SQLite to Postgres with Alembic-managed migrations, so the schema can evolve safely. This lives on a separate branch and isn't merged yet.
- **Commute-time filter**: enter a work address and a max commute time (transit, driving, or cycling) and only see listings that fit. Backend service and GraphQL wiring are still to come.

Planned after that, roughly in order:

- Docker Compose polish (backend + frontend + reverse proxy)
- Loading, error, and empty states across the UI
- Screenshots in this README

Longer-term ideas that aren't scheduled yet:

- A map view with listings pinned and coloured by commute time
- A listing detail page
- Cross-platform de-duplication if a second source gets added back
- New-listing notifications for saved searches
- User accounts with saved filter presets
