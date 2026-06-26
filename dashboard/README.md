# JARVIS OS dashboard

React Three Fiber frontend + FastAPI backend, generated via emergent.sh from a JARVIS-HUD brief
and wired here to real data (AIOS memory, Obsidian vault, `connections.md`).

## Run locally

```bash
# backend (http://localhost:8000)
cd backend && source .venv/bin/activate && uvicorn server:app --reload --port 8000

# frontend (http://localhost:3000)
cd frontend && npm start
```

First time setup: `cd backend && python3.13 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
then `cd frontend && npm install`. Needs Python ≤3.13 (pydantic-core has no 3.14 wheel yet).

## Real vs. stub data

- **Real**: `/api/system/stats` (skills+agents count, memory/graph size, connection health),
  `/api/memory/nodes`, `/api/network/graph` (AIOS memory + Obsidian vault, linked by `[[wikilinks]]`),
  `/api/tools` (parsed from `../connections.md`)
- **Decorative stub, by design**: `/api/globe/points` (no real geo feed), `/api/comms`
  (would need the Microsoft Graph/Slack scripts wired in — not done yet)

The old vanilla-JS dashboard (Express + 3d-force-graph) is archived at
`../archives/dashboard-vanilla-js-2026-06-25/`.
