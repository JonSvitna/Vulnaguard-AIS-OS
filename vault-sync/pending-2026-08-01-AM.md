# Pending vault updates — 2026-08-01 AM

**Coverage window:** Since `pending-2026-07-31-AM.md` — commit `6b6af75` (2026-08-01 morning UTC).

---

## New items to consider for Obsidian

### 1. Lead triage failure — day 7 (critical, escalating)
- Lead triage cron failed again on 2026-08-01. `MS365_USER_UPN` still not set. **7th consecutive day** — no solicitation emails reviewed since approximately 2026-07-20.
- Fix: set `MS365_TENANT_ID`, `MS365_USER_UPN`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET` in Claude Code on the web environment settings. Nothing else changed.
- Source: `decisions/log.md` top entry, commit `6b6af75`.
- **Vault target:** If there's a "pipeline blockers" or "action required" note in `wiki/domains/sentinel-cmmc/`, this belongs there with a priority flag. Day 7 means leads may be slipping through unreviewed.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

All items from `pending-2026-07-31-AM.md` remain unconfirmed. High-priority ones:

- **STOP-reply false-positive bug fixed in vulnaguard-seo-agent** — active prospects were damaged; fix deployed 2026-07-29. Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **SeanBuilds "AI Won't Replace You" — first social batch live** — LinkedIn + Instagram + YouTube Shorts. Brand/content milestone. Vault target: `wiki/decisions/` or `wiki/domains/seanbuilds/`.
- **SeanBuilds site: real lead capture live** — Resend Audiences wired, dead-end CTAs converted. Vault target: `wiki/domains/seanbuilds/`.
- **Clay → n8n → SEO agent cutover** — outreach architecture change. Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut. Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning shift. Vault target: `wiki/decisions/`.

---

*Check ran: 2026-08-01 AM. Next check: 2026-08-02 AM.*
