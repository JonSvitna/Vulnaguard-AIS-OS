# Pending vault updates — 2026-07-22 AM

**Coverage window:** Since `pending-2026-07-21-AM.md` — commits `05ce063`, `28f0063`, `42a2ac1`, `5fe4c6d`, `e381f92` (2026-07-21 ~23:00 through 2026-07-22 ~10:00 UTC).

---

## New items to consider for Obsidian

### Clay → n8n → SEO agent cutover: PR #10 merged (pipeline architecture milestone)
- **What:** PR #10 (`feat/clay-n8n-cutover`) merged to main. Three n8n workflows are now committed: `clay-lead-intake.workflow.json` (updated), `clay-lead-finalizer.workflow.json` (new), `clay-slack-approval.workflow.json` (new). Ops runbook at `references/clay-lead-automation.md`.
- **Decision:** Clay sources and fit-scores U.S. SMB leads → n8n orchestrates intake/finalization/Slack approval buttons → SEO agent is the only lead, draft, approval, and Resend send database. Nothing sends before human approval.
- **Remaining manual steps (not done):** create `#clay-leads` Slack channel, wire Slack signing secret + interactivity URL, activate finalizer/approval workflows, finish Clay HTTP column mapping + 6 AM schedule.
- **Why it matters:** This is the outreach stack's primary architecture — Clay/n8n fully replaces the Claude-side commercial routines as the lead source of record. Moves from "decision" to "shipped." The two commercial cloud routines (`commercial-lead-sourcing`, `commercial-lead-outreach-bridge`) now have an actual cutover to retire against once Clay/n8n proves out.
- **Commits:** `5fe4c6d` (code), `42a2ac1` (docs/decision log), `28f0063` (merge) | **Decisions log entry:** 2026-07-21 — "Clay cutover: SEO Agent is the only outreach source of truth"
- **Vault target:** `wiki/decisions/` — outreach pipeline architecture + market positioning.

### Lead triage: 2nd consecutive failure (MS365 env vars)
- **What:** Overnight lead-triage run failed again on 2026-07-22. Same root cause: `MS365_TENANT_ID`, `MS365_USER_UPN` (and associated auth vars) missing from cloud session environment. No new leads added.
- **Fix needed:** Set `MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`, `MS365_USER_UPN` in the claude.ai session/environment config.
- **Commit:** `e381f92` | **Decisions log entry:** 2026-07-22 — "Overnight Lead Triage run failed: MS365 env vars still absent (2nd consecutive miss)"
- **Vault target:** Skip (ops/config gap, not a business decision) — flagging here so you know the triage feed has been dark 2 days running.

### Hermes: zombie SEO dashboard deletion logged as content opportunity
- **What:** Hermes-cron flagged commit `609194b` in `vulnaguard-seo-agent` — 1,639 lines of zombie SEO dashboard code deleted (config, GitHub lib, 1,195-line dashboard page). /dashboard now redirects to /marketing-agents. Hermes staged this as a Vulnaguard build-log content moment in `references/hermes-pending/pending-2026-07-22-1784692435564.md`.
- **Why it matters:** Confirms the "SEO agent stripped to one job" decision (carry-forward from 2026-07-18) is now fully executed at the code level. The hermes file also has 3 talking points ready if you want to post about it.
- **Vault target:** Skip for decisions log (already logged as the strip decision). If you want the build-log content, pull from the hermes pending file first.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut (`commit 74deeb5`, flagged in `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **Retired website-design-lead-finder agent** — automation retirement (`commit 68bf73d`, flagged in `pending-2026-07-19-AM.md`). Vault target: `wiki/decisions/`.
- **n8n content workflows paused + creative-os-render-worker already gone** — infra cleanup (`commit 68bf73d`, flagged in `pending-2026-07-19-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning (`commit 4b0197e`, flagged in `pending-2026-07-20-AM.md`). Vault target: `wiki/decisions/`.
- **Cloud routines reset to daily; Clay/n8n as safety net** — tooling architecture call (`commit b50359c`, flagged in `pending-2026-07-21-AM.md`). Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-22 AM. Next check: 2026-07-23 AM.*
