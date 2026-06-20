# Connections

Registry of every system your AIOS can reach. Filled by `/onboard` from Q4-Q7 answers; expanded over time as you wire new tools. `/audit` checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | Stripe (primary) — `scripts/stripe_api.py` + `references/stripe-api.md`, live 2026-06-19 ($0 balance/charges/subscriptions, expected — no clients yet); Mercury Bank (invoicing fallback, not wired) | key+ref | live, verified | 2026-06-19 |
| 2 | Customer interactions | vulnaguard-seo-agent's real marketing pipeline (lead DB, qualifier/copywriter agents, Resend send) — 95 outreach emails queued, 50 sent live 2026-06-19; cold email + LinkedIn outreach manually logged in `references/outreach-log.md` | key+ref | live, verified | 2026-06-19 |
| 3 | Calendar | Outlook Calendar via Microsoft Graph (`scripts/microsoft365_api.py`) | key+ref | app-only (client credentials), admin consent granted | 2026-06-18 |
| 4 | Communication | Microsoft 365 mailbox via Microsoft Graph (`scripts/microsoft365_api.py`); Slack (internal/team, not yet connected) | key+ref | app-only (client credentials), admin consent granted | 2026-06-18 |
| 5 | Project / task tracking | None — nothing formal in place | not yet connected | — | — |
| 6 | Meeting intelligence / notes / second brain | Obsidian vault (`~/Documents/Obsidian Vault`) connected via `claude-obsidian` plugin — domain-first wiki (Sentinel CMMC, SEO Agent, Client Work) scaffolded and existing notes ingested 2026-06-19, cross-project reference point per `wiki/overview.md`; ChatGPT/OpenAI (de facto notes tool) still used loosely alongside it | plugin (claude-obsidian, Obsidian CLI transport) | live, verified | 2026-06-19 |
| 7 | Knowledge / files | GitHub (this repo + project repos, `gh` CLI authenticated); Codex/OpenAI; Claude | script (gh CLI) | logged in via keyring | 2026-06-18 |
| 8 | Outbound content / SEO | vulnaguard-seo-agent SEO dashboard (M1-M3 fixed and live 2026-06-19: real GSC-grounded keyword research, real ranking monitor, real cheerio-based page audit); `seanbuilds-voice` skill for drafting | key+ref | live, verified | 2026-06-19 |
| 9 | Search performance | Google Search Console for vulnaguard.com via OAuth (`/api/gsc` in vulnaguard-seo-agent) — feeds SEO modules M1/M2 with real ranking/query data | key+ref | OAuth app published to Production, secret regenerated 2026-06-19 | 2026-06-19 |
| 10 | Flagship product | Sentinel CMMC (own repo/tool — tracked here as a connection, not folded into this AIOS) | not yet connected | — | — |

**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever.
