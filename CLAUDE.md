# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Car Finder CA is an AI-powered used car deal aggregator for Canadian buyers. It aggregates listings from sources like Kijiji Autos, scores each on price fairness, condition red flags, and seller trust, and surfaces the best deals via a single composite `deal_score`. Scrapers are not yet implemented.

## Stack

- **Frontend:** Next.js 15 (App Router) + Tailwind CSS 3 — `frontend/`
- **Backend:** FastAPI + SQLAlchemy (sync) + psycopg2 — `backend/`
- **Database:** PostgreSQL (Docker locally; Supabase in production)
- **AI:** Claude API — listing analysis and NL search (planned)
- **Scraping:** Playwright + BeautifulSoup — `backend/scrapers/` (planned)
- **Scoring:** `backend/scoring/` (planned)

## Running the stack

**Docker (recommended):**
```bash
cp .env.example .env
docker compose up
```
Services: frontend → http://localhost:3000, backend → http://localhost:8000, Postgres → 5432.

**Frontend only:**
```bash
cd frontend && npm install && npm run dev
```

**Backend only** (requires running Postgres):
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Tests:**
```bash
cd backend && pytest
```

**Lint:**
```bash
cd frontend && npm run lint
```

## Key conventions

### Database
- `price` is stored in **CAD cents** (integer), not dollars.
- `mileage` is in **kilometres**.
- `deal_score` is a float 0–100 (null until scoring is implemented); listings sort by it descending, nulls last.
- `source_url` is the deduplication key — it has a UNIQUE constraint.
- Schema lives in `db/schema.sql`. Docker mounts it as an init script on first `docker compose up`. For schema changes, modify `schema.sql` and apply manually or add a migration script alongside it.

### Backend
- DB access uses SQLAlchemy sessions injected via the `get_db` dependency in router functions.
- `app/models.py` = SQLAlchemy ORM; `app/schemas.py` = Pydantic request/response shapes. Keep them separate.
- New scrapers go in `backend/scrapers/`; scoring logic in `backend/scoring/`.

### Frontend
- App Router only — new pages go under `src/app/`.
- Shared UI components go in `src/components/`.
- Backend URL is configured via `NEXT_PUBLIC_API_URL` env var.
