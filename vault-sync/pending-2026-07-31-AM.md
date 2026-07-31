# Pending vault updates — 2026-07-31 AM

**Coverage window:** Since `pending-2026-07-30-AM.md` — commits `95ef6f2`, `4dc877e` (2026-07-30 evening through 2026-07-31 AM UTC).

---

## New items to consider for Obsidian

### 1. Lead triage failure — day 6 (escalating blocker)
- Lead triage cron failed again on 2026-07-31 with `KeyError: 'MS365_USER_UPN'`. **6th consecutive day.** No solicitation emails have been reviewed since approximately 2026-07-20.
- Fix remains the same: set `MS365_TENANT_ID`, `MS365_USER_UPN`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET` in Claude Code on the web environment settings.
- Source: `decisions/log.md` (top entry), commit `95ef6f2`.
- **Vault target:** Only worth mirroring if you want a "persistent pipeline blocker" marker in `wiki/domains/sentinel-cmmc/` to prompt action. Otherwise it's already tracked in `decisions/log.md`.

### 2. decisions/log.md merge conflict resolved
- The raw `<<<<<<<` conflict flagged in yesterday's note has been cleaned up via commits `95ef6f2` and `4dc877e`. Automated appends should work again.
- This is technical/dev — no Obsidian mirror needed.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

All items from `pending-2026-07-30-AM.md` remain unconfirmed. Key ones:

- **STOP-reply false-positive bug fixed in vulnaguard-seo-agent** — active prospects were damaged by outreach system error; fix deployed 2026-07-29. Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **SeanBuilds "AI Won't Replace You" — first social batch live** — LinkedIn + Instagram + YouTube Shorts. Brand/content milestone. Vault target: `wiki/decisions/` or `wiki/domains/seanbuilds/`.
- **SeanBuilds site: real lead capture live** — Resend Audiences wired, dead-end CTAs converted. Commit `6e196f7`. Vault target: `wiki/domains/seanbuilds/`.
- **Clay → n8n → SEO agent cutover** — outreach architecture change. Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut. Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning shift. Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-31 AM. Next check: 2026-08-01 AM.*
