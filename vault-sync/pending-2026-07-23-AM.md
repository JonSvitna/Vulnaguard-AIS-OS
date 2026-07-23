# Pending vault updates — 2026-07-23 AM

**Coverage window:** Since `pending-2026-07-22-AM.md` — commits `d5c8a66`, `ce606a5`, `78eb540`, `67d31be` (2026-07-22 ~22:42 through 2026-07-23 ~10:04 UTC).

---

## New items to consider for Obsidian

### SeanBuilds "AI Won't Replace You" series — first content batch live on all 3 platforms
- **What:** All 7 clips queued to Buffer (LinkedIn + Instagram Reels) at 15:00 UTC daily, 2026-07-23 through 2026-07-29. Same clips uploaded as YouTube Shorts at identical timestamps so all three platforms drop together per clip.
- **How it got shipped:** Buffer API had rotted to the wrong surface (legacy REST). Rewrote `scripts/buffer_api.py` to Buffer's current GraphQL Publish API. Video files (1.2GB) hosted temporarily via nginx on the existing DigitalOcean droplet — no new process, confirmed ~620MB RAM headroom. Captions first generated from the render manifest, then rewritten through `seanbuilds-voice` after Sean flagged them as sounding bot-written.
- **Milestone:** First end-to-end social batch from this AIOS stack. Buffer + YouTube upload tooling now exercised and documented.
- **Flag:** Commit `d5c8a66` (the YouTube upload code) could not be traced to any active Claude Code session or the droplet's cron at commit time — provenance unresolved. Flagged in `decisions/log.md`.
- **Commits:** `d5c8a66`, `ce606a5` | **Decisions log entry:** 2026-07-22 — "First social batch shipped via Buffer: SeanBuilds 'AI Won't Replace You' series"
- **Vault target:** `wiki/decisions/` or `wiki/domains/seanbuilds/` — brand/content milestone + new distribution stack.

### Lead triage: 3rd consecutive failure (M365 env vars)
- **What:** Lead-triage run failed again 2026-07-23 AM. Same root cause: `MS365_TENANT_ID`, `MS365_USER_UPN`, and related auth vars missing from cloud session. Lead pipeline has been dark since 2026-07-20 — 3 consecutive misses.
- **Action needed:** Set `MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`, `MS365_USER_UPN` in the claude.ai session environment config. Until fixed, no solicitations are being caught.
- **Commit:** `67d31be` | **Decisions log entry:** 2026-07-23 — "Overnight Lead Triage run failed: MS365 env vars still absent (3rd consecutive miss)"
- **Vault target:** Skip (ops gap, not a business decision) — flagged because 3 misses means any solicitation emails in that window are unreviewed.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **Clay → n8n → SEO agent cutover (PR #10 merged)** — outreach pipeline architecture. Commits `5fe4c6d`, `42a2ac1`, `28f0063`, 2026-07-21. Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut (commit `74deeb5`, flagged `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning (commit `4b0197e`, flagged `pending-2026-07-20-AM.md`). Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-23 AM. Next check: 2026-07-24 AM.*
