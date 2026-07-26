# Pending vault updates — 2026-07-26 AM

**Coverage window:** Since `pending-2026-07-25-AM.md` — commit `5f5b490` (2026-07-26 ~10:04 UTC).

---

## New items to consider for Obsidian

### Lead triage failure — 4th consecutive (2026-07-26, commit `5f5b490`)
- **What:** Lead triage cron failed again today. `MS365_TENANT_ID`, `MS365_USER_UPN`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET` still not set in the cloud environment. `KeyError: 'MS365_USER_UPN'` on every run.
- **Run history:** 2026-07-21, 2026-07-24, 2026-07-25, 2026-07-26 — 4 straight failures.
- **Risk:** Any solicitation emails since 2026-07-20 are unreviewed. Multiple may be past close date.
- **Fix (same every time):** Set those 4 env vars in the claude.ai session environment config.
- **Vault target:** Still ops-only — skip. Flagged here as a persistent action item.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **SeanBuilds site: real lead capture live** — three Resend Audiences, all dead-end CTAs converted to inquiry modal. First time the personal brand site can actually capture leads. Commit `6e196f7` (2026-07-24). Vault target: `wiki/domains/seanbuilds/` (your call — business capability milestone).
- **SeanBuilds "AI Won't Replace You" — first social batch live (LinkedIn + Instagram + YouTube Shorts)** — brand/content milestone + new distribution stack. Commit `ce606a5`. Vault target: `wiki/decisions/` or `wiki/domains/seanbuilds/`.
- **Clay → n8n → SEO agent cutover / Origami now owns Vulnaguard B2B pipeline** — outreach pipeline architecture. Commits `5fe4c6d`, `42a2ac1`, `28f0063` (2026-07-21); `connections.md` row 21 added 2026-07-23. Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut (commit `74deeb5`, flagged `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning (commit `4b0197e`, flagged `pending-2026-07-20-AM.md`). Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-26 AM. Next check: 2026-07-27 AM.*
