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

## Data sources — all real

Every endpoint reads from the repo or a live API. Nothing is randomized; where a
metric has no real source it is omitted rather than faked.

- `/api/system/stats` — skills/agents counts (`.claude/`), node/edge counts and a
  real 14-day knowledge-base activity histogram (memory + vault file mtimes),
  connection health, server uptime.
- `/api/memory/nodes` — AIOS memory notes with real outgoing `[[wikilink]]` counts.
- `/api/network/graph` — AIOS memory + Obsidian vault, linked by `[[wikilinks]]`.
- `/api/tools` — parsed from `../connections.md`, with the real `last_checked` date
  driving each tool's freshness.
- `/api/brief` — top priorities from `context/priorities.md`.
- `/api/decisions` — decision headings from `decisions/log.md`.
- `/api/leads` — staged leads from `leads/inbox.md`; CMMC relevance read from the
  triage-note wording.
- `/api/comms` — **live** feed from Slack + Microsoft Graph via the repo's API
  scripts. Falls back to a clearly-labeled `SIM` stub (`simulated: true`) when the
  tokens/channels aren't configured. Set `SLACK_COMMS_CHANNELS` (defaults to
  `#all-vulnaguard-sentinel`) plus the existing `SLACK_BOT_TOKEN` / `MS365_*`
  secrets in `.env` to go live.

Note: the memory + Obsidian paths in `server.py` are the author's local machine
paths, so `/memory` and `/network` return empty (graceful empty states in the UI)
anywhere those dirs don't exist.

## Stack notes

- Frontend is plain React + Canvas 2D (the knowledge graph). The previous version's
  React Three Fiber / `three` / postprocessing dependencies were dropped in the
  Notion-OS rework — bundle is ~68 KB gzip.
- Views live in `frontend/src/views/`, shared UI in `frontend/src/components/`,
  design tokens + all styling in `frontend/src/index.css`.

The old React-Three-Fiber JARVIS-HUD frontend and the vanilla-JS dashboard before
it are archived under `../archives/`.
