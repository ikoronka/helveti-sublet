# helveti-sublet — Agent Context

This file is the source of truth for any AI assistant or agent working on this project. Read it fully before making changes.

---

## What this project is

A web app that aggregates Swiss apartment listings (Flatfox, ImmoScout24, etc.) for the Zurich area and adds smart filters that native platforms don't offer:
- Roommate gender preference (extracted from description text)
- Furnished / unfurnished
- Minimum and maximum stay duration
- Sublet date range matching (July–August use case)
- Commute-time filtering (enter a work address, set a max commute time)

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Vue 3 + TypeScript + Tailwind + Pinia | User knows Vue, wanted to learn it deeply |
| Package manager (FE) | pnpm | Faster, disk-efficient |
| Backend | Python + FastAPI | User has Python background, good scraping ecosystem |
| GraphQL | Strawberry | Integrates with FastAPI, clean filter pattern, portfolio signal |
| Database | SQLite via SQLAlchemy ORM | Simple, no infra dependencies for MVP |
| Dependency manager (BE) | uv | Modern, fast, handles venvs |

---

## Project structure

```
helveti-sublet/
  CLAUDE.md               ← short pointer file (model-agnostic)
  AGENTS.md               ← this file
  PLAN.md                 ← current build plan + progress
  docker-compose.yml
  .env.example
  backend/
    pyproject.toml        # uv-managed dependencies
    main.py               # FastAPI app + Strawberry GraphQL mount
    config.py             # pydantic-settings (env vars)
    db.py                 # SQLAlchemy engine + session + Base
    models.py             # ORM models: Listing, CommuteCache
    graphql/
      __init__.py
      types.py            # Strawberry types: ListingType, ListingFilterInput, etc.
      resolvers.py        # Query resolver logic
      schema.py           # Root Query + schema assembly
    scrapers/
      __init__.py
      base.py             # Abstract BaseScraper (httpx + rate limiter)
      flatfox.py          # Flatfox scraper (method TBD — inspect DevTools)
      immoscout.py        # ImmoScout24 hidden API scraper
      runner.py           # Scrape → extract → upsert orchestrator
    extraction/
      __init__.py
      text_parser.py      # Regex extraction for smart fields
    services/
      __init__.py
      commute_service.py  # search.ch (transit) + OSRM (driving/cycling) + cache
    tasks/
      scrape_job.py       # CLI entrypoint: python -m tasks.scrape_job
  frontend/
    package.json
    vite.config.ts
    src/
      App.vue
      main.ts
      router/index.ts
      types/listing.ts    # TypeScript interfaces matching GraphQL types
      api/
        client.ts         # GraphQL client (villus or plain fetch)
        queries.ts        # GraphQL query/variable definitions
      stores/
        listingsStore.ts  # Pinia: fetched listings, pagination state
        filtersStore.ts   # Pinia: active filter values, toQueryVars()
      views/
        ListingsView.vue  # Main page
      components/
        filters/
          PriceRangeSlider.vue
          RoomSelector.vue
          DateRangePicker.vue
          SmartFilterChips.vue  # Furnished, gender pref, sublet toggles
          CommuteFilter.vue     # Address input + mode + max time slider
        listings/
          ListingCard.vue
          ListingGrid.vue
          SourceBadge.vue       # "Flatfox" / "ImmoScout24" pill
```

---

## Data model

### `listings` table

| Column | Type | Notes |
|---|---|---|
| id | String PK | SHA256(source + source_id) |
| source | String | "flatfox" or "immoscout24" |
| source_id | String | Original platform ID |
| source_url | String | Direct link to listing |
| title | String | |
| description | String | Raw description text |
| price_chf | Integer | Monthly rent in CHF |
| rooms | Float | 1, 1.5, 2, etc. |
| area_m2 | Integer? | |
| address | String? | |
| city | String | |
| zip_code | String? | |
| latitude | Float? | |
| longitude | Float? | |
| is_furnished | Boolean? | Extracted from description |
| gender_preference | String? | "female" / "male" / null |
| min_stay_days | Integer? | Extracted from description |
| max_stay_days | Integer? | Extracted from description |
| available_from | Date? | Extracted or from structured fields |
| available_to | Date? | Extracted or from structured fields |
| is_sublet | Boolean | Default false |
| images | String | JSON array of image URLs |
| first_seen | DateTime | |
| last_seen | DateTime | |
| is_active | Boolean | False after 3 missed scrape cycles |

Unique constraint: `(source, source_id)`

### `commute_cache` table

| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| origin_lat | Float | Rounded to 3 decimal places |
| origin_lng | Float | |
| dest_lat | Float | |
| dest_lng | Float | |
| mode | String | "transit" / "driving" / "bicycling" |
| duration_minutes | Integer | |
| fetched_at | DateTime | TTL: discard after 7 days |

Unique constraint: `(origin_lat, origin_lng, dest_lat, dest_lng, mode)`

---

## GraphQL schema

```graphql
type Query {
  listings(filters: ListingFilterInput, page: Int, pageSize: Int): PaginatedListings!
  filterOptions: FilterOptions!
}

input ListingFilterInput {
  priceMin: Int
  priceMax: Int
  roomsMin: Float
  roomsMax: Float
  city: String
  isFurnished: Boolean
  genderPreference: String
  availableFrom: Date
  availableTo: Date
  maxStayDays: Int
  isSublet: Boolean
  commuteDestLat: Float
  commuteDestLng: Float
  commuteMode: String
  commuteMaxMinutes: Int
}

type PaginatedListings {
  items: [Listing!]!
  total: Int!
  page: Int!
  pageSize: Int!
  totalPages: Int!
}
```

Full type definitions live in `backend/graphql/types.py`.

---

## Smart filter extraction

Listing descriptions are in German and/or English. We extract structured fields using regex in `backend/extraction/text_parser.py`.

Key patterns to handle:
- **Gender preference:** "Frauen-WG", "nur weiblich", "female only", "wir suchen eine Mitbewohnerin" → `"female"`; "Männer-WG", "men only" → `"male"`
- **Furnished:** "möbliert", "furnished", "eingerichtet" → `true`; "unmöbliert", "ohne Möbel" → `false`
- **Sublet:** "Zwischenmiete", "Untermiete", "sublet" → `is_sublet = true`
- **Stay duration:** "Mindestmietdauer 3 Monate", "minimum 6 months" → `min_stay_days`
- **Dates:** "ab 1. Juli", "vom 01.07 bis 31.08" → `available_from`, `available_to`

Regex covers ~80% of cases. Gemini API fallback for fields regex misses (gender preference especially) — `extraction/llm_extractor.py`, called once per new listing at scrape time, result stored in DB. `GEMINI_API_KEY` env var required.

---

## Commute service

- **Transit:** search.ch route API (`timetable.search.ch/api/route.json`) — free, covers SBB + ZVV
- **Driving / cycling:** OSRM public API — free, open-source
- Cache results for 7 days; round coordinates to 3 decimal places for cache key
- Compute on demand (not pre-computed in MVP)

---

## Scraping

- **Flatfox:** No public API. Inspect browser DevTools network tab on `flatfox.ch/en/search/` to find internal XHR endpoints. Fall back to HTML scraping if needed.
- **ImmoScout24:** Hidden REST API — use browser DevTools to discover the endpoint pattern.
- Rate limit: max 10 requests/min per platform. Set `User-Agent: HelvétiSublet/1.0`.
- Respect `robots.txt`. Do not store personal contact info.
- Run manually via `python -m tasks.scrape_job` for MVP.

---

## Working conventions

- Backend: all async (FastAPI + async SQLAlchemy sessions)
- Frontend: Composition API only (no Options API)
- No comments explaining what the code does — only why if it's non-obvious
- No features beyond what's in PLAN.md Phase 1 until Phase 1 is complete
- User wants to understand every step — discuss before implementing
