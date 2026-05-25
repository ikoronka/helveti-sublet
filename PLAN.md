# Build Plan

## Legend
- [ ] Not started
- [~] In progress
- [x] Done

---

## Phase 1 — Skeleton (mock data, end-to-end flow)

Goal: a working app with fake seeded data, filters wired up, nothing scraped yet.

### Backend
- [x] Add dependencies to `pyproject.toml`: fastapi, uvicorn, strawberry-graphql, sqlalchemy, pydantic-settings
- [x] `db.py` — SQLAlchemy engine, session factory, Base
- [x] `models.py` — `Listing` and `CommuteCache` ORM classes
- [x] `types_.py` — Strawberry types: `ListingType`, `ListingFilterInput`, `PaginatedListings`, `FilterOptions` (at root, named `types_.py` to avoid shadowing Python builtins; `gql/` dir used instead of `graphql/` to avoid shadowing graphql-core package)
- [x] `gql/resolvers.py` — `listings` resolver with price/rooms/city filtering + pagination
- [x] `gql/schema.py` — root `Query` type, assemble schema
- [x] `main.py` — FastAPI app, CORS, mount Strawberry at `/graphql`
- [x] `tasks/seed.py` — 20 realistic Zurich test listings seeded into DB
- [x] Verify: uvicorn starts, GraphQL query returns all 20 listings ✓

### Frontend
- [x] Install Tailwind CSS + villus
- [x] `src/types/listing.ts` — TypeScript interfaces matching GraphQL types
- [x] `src/api/client.ts` — plain fetch wrapper (villus installed but not used yet)
- [x] `src/api/queries.ts` — `LISTINGS_QUERY` + `FILTER_OPTIONS_QUERY`
- [x] `src/stores/filtersStore.ts` — active filter state + `toQueryVars()`
- [x] `src/stores/listingsStore.ts` — fetch listings, store results + pagination, watches filters
- [x] `src/components/listings/ListingCard.vue` — title, price, rooms, city, badges
- [x] `src/components/listings/ListingGrid.vue` — grid layout, loading/error/empty states, pagination
- [x] `src/views/ListingsView.vue` — sidebar + grid layout
- [x] `src/components/filters/PriceRangeSlider.vue` — min/max price inputs
- [x] `src/components/filters/RoomSelector.vue` — room count toggle buttons
- [x] `App.vue` + `router/index.ts` updated to point at ListingsView
- [x] Verify: frontend shows seeded listings, price/room filters work (needs testing in browser)

---

## Phase 2 — First Scraper (Flatfox)

- [x] Investigate Flatfox: open DevTools on `flatfox.ch/en/search/`, identify XHR endpoint
- [x] `scrapers/base.py` — abstract `BaseScraper` with httpx + rate limiter
- [x] `scrapers/flatfox.py` — implement scraper, map response to `Listing` fields
- [x] `scrapers/runner.py` — upsert logic, mark stale listings inactive
- [x] `tasks/scrape_job.py` — CLI entrypoint
- [x] `src/components/listings/SourceBadge.vue` — "Flatfox" / "ImmoScout24" pill
- [x] Verify: run scrape job, real listings appear in frontend

---

## Phase 3 — Smart Filters

- [x] `extraction/text_parser.py` — regex extractors for furnished, gender, stay duration, dates, sublet
- [x] `extraction/llm_extractor.py` — Ollama (llama3.2:3b) local LLM fallback; called once per new listing at scrape time; on VPS will use Gemini or skip — `GEMINI_API_KEY` in `.env` for future use
- [x] Backfill: re-run extraction on all existing descriptions in DB (306 listings via Ollama; results: 23 female, 4 male, 231 furnished, 42 sublet)
- [x] `src/components/filters/SmartFilterChips.vue` — Furnished / Female only / Sublet toggles
- [x] `src/components/filters/DateRangePicker.vue` — available from/to date inputs
- [x] Wire new filters through GraphQL resolver
- [x] Verify: toggle "Female only" → only female-preference listings shown

---

## Phase 4 — Second Scraper + Commute Filter

### Second scraper
- [x] Investigate ImmoScout24 — DataDome blocks headless/httpx; data is SSR-embedded in `window.__INITIAL_STATE__`; accessible via real browser (DataDome cookie already solved)
- [x] `scrapers/immoscout.py` — playwright scraper (non-headless); maps `__INITIAL_STATE__` listings to our model
- [x] `tasks/import_is24.py` — one-shot importer for browser-scraped JSON (Chrome MCP → download → import)
- [x] Backfill: 300 ImmoScout24 listings imported via Chrome DevTools MCP → browser download → DB import

### Commute filter
- [ ] `services/commute_service.py` — search.ch (transit) + OSRM (driving/cycling) + DB cache
- [ ] Add `geocode` query to GraphQL schema
- [ ] `src/components/filters/CommuteFilter.vue` — address input + mode selector + max time slider
- [ ] Wire commute filter into `listings` resolver
- [ ] Verify: enter a Zurich address, set 30min transit → listings outside that radius disappear

---

## Phase 5 — Polish + Deploy

- [ ] Docker Compose: backend + frontend + nginx reverse proxy
- [ ] `.env.example` with all required env vars documented
- [ ] Loading states on ListingGrid
- [ ] Error state (failed fetch)
- [ ] Empty state (no results for filters)
- [ ] README with screenshots and setup instructions
- [ ] Verify: `docker compose up` → full stack runs, filters work end-to-end

---

## Deferred (post-MVP)

- Map view (Leaflet/MapLibre) with listings as pins coloured by commute time
- Listing detail page
- Cross-platform deduplication (same apartment on Flatfox + ImmoScout)
- WG-Zimmer.ch, Ronorp, Homegate scrapers
- New listing notifications (email/push for saved searches)
- LLM-based extraction for ambiguous German descriptions
- User accounts + saved filter presets
