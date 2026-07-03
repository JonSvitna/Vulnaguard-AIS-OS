# Sentinel OS dashboard

A Notion-layout personal operating-system dashboard with a Jarvis dark-HUD skin.
Plain React (Create React App) frontend + FastAPI backend, wired to real data
(AIOS memory, Obsidian vault, `connections.md`).

Five sections in the left rail — **Overview, Network, Memory, Systems, Comms** —
each a block-based view. The design language: Notion's information calm (sidebar +
command bar + block grid, hairline borders, generous gutters) lit with restrained
cyan. Single dark theme by design (a reactor-lit HUD). See `references/` or the
design-system prompt for the full token spec.

## Run locally

```bash
# backend (http://localhost:8000)
cd backend && source .venv/bin/activate && uvicorn server:app --reload --port 8000

# frontend (http://localhost:3000)
cd frontend && npm start
```

First time setup: `cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
then `cd frontend && npm install`. Backend runs on Python 3.11–3.13.

The frontend defaults to `http://localhost:8000` for the API. Override with
`REACT_APP_BACKEND_URL` for other deployments. Every endpoint is fetched with
`Promise.allSettled`, so a missing source renders an empty state rather than
crashing the app.

## Real vs. stub data

- **Real**: `/api/system/stats` (skills + agents counts, memory/graph size,
  connection health), `/api/memory/nodes`, `/api/network/graph` (AIOS memory +
  Obsidian vault, linked by `[[wikilinks]]`), `/api/tools` (parsed from
  `../connections.md`).
- **Decorative stub, by design**: `/api/comms` — mirrors the real channels this
  AIOS reaches (Slack / M365 / Resend) but is not a live feed yet; surfaced in the
  UI with a `SIM` tag. Wiring it up needs the Microsoft Graph / Slack scripts used
  elsewhere in this repo.
- **Curated (no source yet)**: the Daily Brief tasks, Decisions Log, and Leads
  Pipeline on Overview are hand-kept until file/API sources are wired.

## Stack notes

- Frontend is plain React + Canvas 2D (the knowledge graph). The previous version's
  React Three Fiber / `three` / postprocessing dependencies were dropped in the
  Notion-OS rework — bundle is ~68 KB gzip.
- Views live in `frontend/src/views/`, shared UI in `frontend/src/components/`,
  design tokens + all styling in `frontend/src/index.css`.

The old React-Three-Fiber JARVIS-HUD frontend and the vanilla-JS dashboard before
it are archived under `../archives/`.
