# Pending vault updates — 2026-07-24 AM

**Coverage window:** Since `pending-2026-07-23-AM.md` — commits `c8dc365`, `a4bf04c` (2026-07-23 ~10:04 through 2026-07-24 AM UTC).

---

## New items to consider for Obsidian

### Lead triage: 4th consecutive failure (MS365 env vars)
- **What:** Lead-triage run failed again 2026-07-24 AM. Same root cause: `MS365_TENANT_ID`, `MS365_USER_UPN`, and related auth vars missing from cloud session. Lead pipeline has now been dark for 4 consecutive days.
- **Why it matters:** Any solicitation emails that landed since 2026-07-20 are unreviewed and likely past their close dates.
- **Action needed (same as prior 3 notes):** Set `MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`, `MS365_USER_UPN` in the claude.ai session environment config. Until fixed, all lead-triage runs will fail.
- **Commit:** `c8dc365` | **Decisions log entry:** 2026-07-24 — "Lead Triage run failed: MS365 auth still not configured"
- **Vault target:** Skip (ops gap, not a business decision) — noting here because 4 consecutive misses is now a meaningful coverage hole.

### Hermes cron scan — nothing new
- Ran overnight, 0 new content-worthy entries found. No action needed.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **SeanBuilds "AI Won't Replace You" — first social batch live (LinkedIn + Instagram + YouTube Shorts)** — brand/content milestone + new distribution stack. Commit `ce606a5`. Vault target: `wiki/decisions/` or `wiki/domains/seanbuilds/`.
- **Clay → n8n → SEO agent cutover (PR #10 merged)** — outreach pipeline architecture. Commits `5fe4c6d`, `42a2ac1`, `28f0063`, 2026-07-21. Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut (commit `74deeb5`, flagged `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning (commit `4b0197e`, flagged `pending-2026-07-20-AM.md`). Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-24 AM. Next check: 2026-07-25 AM.*
