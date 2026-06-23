# Active task

Updated whenever Sean switches coding agents mid-task (Claude Code ↔ Codex ↔ Cursor) so the next agent can pick up cold. If this file says "none," there's nothing in flight — read CLAUDE.md and proceed normally.

**Status:** in progress
**Switched from:** Cursor → Codex (manual switch)
**Updated:** 2026-06-22

## What we're doing

Clean handoff — no specific coding task was active in the Cursor session that triggered this. Repo is on `main` with a clean working tree. Sean is switching to Codex for general AIOS work; tell Codex what to pick up next.

## Done so far

- NEXUS OS dashboard revamp shipped (`5c8e7ab`): `dashboard/public/` UI overhaul, `command.css`, `/api/graph` + `/api/overview` in `dashboard/server.js`
- Website-design lead finder added (`c0ec25f`): `.claude/agents/website-design-lead-finder.md`, `leads/website-design-inbox.md` populated with 6 Baltimore-metro prospects
- Agent manuals synced: `scripts/sync_agent_manuals.py` was missing from repo (documented but never committed) — recreated and run; `AGENTS.md` + `.cursor/rules/aios.mdc` now include the Obsidian vault section from `CLAUDE.md`

## Next step

Ask Sean what to work on, or pick from open priorities in `decisions/log.md`:

1. **Website dev pipeline** — run `website-design-lead-finder` for another industry/city, or qualify the 6 leads in `leads/website-design-inbox.md` (several flagged borderline on "not solo" ICP)
2. **Sentinel CMMC pilot readiness** — control catalog divergence is still CRITICAL (`decisions/log.md` 2026-06-19 entry): production loads 48-control copy vs 110-control repo root
3. **Dashboard** — start with `cd dashboard && npm start` (not `npm run dev` from repo root; no root `package.json`)

## Key files

- `context/priorities.md` — quarter goals (Sentinel cert, 10 clients, SEO traffic)
- `decisions/log.md` — append-only decisions; read tail for latest context
- `leads/website-design-inbox.md` — website dev lead staging (6 rows, needs qualification)
- `dashboard/server.js` — Express server; graph + overview APIs
- `dashboard/public/app.js` — NEXUS OS frontend (3D memory graph, orbit, sparklines)
- `CLAUDE.md` — canonical operating manual (Codex reads generated `AGENTS.md`)

## Watch out for

- `scripts/sync_agent_manuals.py` was referenced everywhere but never committed until this handoff — re-run after any `CLAUDE.md` edit
- Dashboard has no `dev` script — use `npm start` from `dashboard/`
- Several website-design leads lack public email; phone-only outreach may need a different channel than Resend cold email

<!--
Template for an in-flight task:

**Status:** in progress
**Switched from:** Claude Code → Codex (hit usage limit)
**Updated:** 2026-06-19 14:30

## What we're doing
One or two sentences on the goal.

## Done so far
- Bullet list of concrete completed steps, with file paths.

## Next step
The single next action to take. Be specific — file, function, what to change.

## Key files
- path/to/file.ts — why it matters
- path/to/other.py — why it matters

## Watch out for
Anything non-obvious the next agent would otherwise rediscover the hard way.
-->
