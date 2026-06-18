# Connections

Registry of every system your AIOS can reach. Filled by `/onboard` from Q4-Q7 answers; expanded over time as you wire new tools. `/audit` checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | Stripe (primary, not yet configured); Mercury Bank (invoicing fallback) | not yet connected | — | — |
| 2 | Customer interactions | Cold email + LinkedIn outreach (no traction yet); Resend API for sending; tracked in `references/outreach-log.md` | script (manual log) | — | 2026-06-17 |
| 3 | Calendar | Outlook Calendar via Microsoft Graph (`scripts/microsoft365_api.py`) | key+ref | app-only (client credentials), admin consent granted | 2026-06-18 |
| 4 | Communication | Microsoft 365 mailbox via Microsoft Graph (`scripts/microsoft365_api.py`); Slack (internal/team, not yet connected) | key+ref | app-only (client credentials), admin consent granted | 2026-06-18 |
| 5 | Project / task tracking | None — nothing formal in place | not yet connected | — | — |
| 6 | Meeting intelligence / notes | ChatGPT/OpenAI (de facto notes tool); scattered notepad notes; Obsidian under consideration | not yet connected | — | — |
| 7 | Knowledge / files | GitHub (this repo + project repos, `gh` CLI authenticated); Codex/OpenAI; Claude | script (gh CLI) | logged in via keyring | 2026-06-18 |
| 8 | Outbound content | SEO agent (outreach + planned video editing/auto-post); `seanbuilds-voice` skill for drafting | not yet connected | — | — |
| 9 | Flagship product | Sentinel CMMC (own repo/tool — tracked here as a connection, not folded into this AIOS) | not yet connected | — | — |

**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever.
