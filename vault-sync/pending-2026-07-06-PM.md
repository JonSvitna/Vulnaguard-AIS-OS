# Pending vault updates — 2026-07-06 PM

**Coverage window:** Since the 2026-07-05 AM note (commit `c2356c9`), which ran before the day's commits landed and found nothing new.

---

## What's new

Two back-to-back decisions on 2026-07-05 (commits `63aae8f` and `23e2079`) — both business-level product/architecture. Source: `decisions/log.md`.

- **SAM.gov ownership consolidated under vulnaguard-capture-os** (`63aae8f`, ~11:54 EDT). Fixed a real silent bug: `scripts/sam_gov_api.py` was passing `naicsCode`/`psc`/`q` to the SAM.gov API — all silently ignored, so every "filtered" search was actually the full unfiltered firehose. Real params are `ncode`/`ccode`/`title`. Same bug was already caught and fixed in `vulnaguard-capture-os`. Decision: Capture OS is now the **canonical SAM.gov querying surface** — both repos share the same `SAM_GOV_API_KEY`/`SAM_API_KEY`, and running both independently risks rate-limit collisions and duplicate-but-diverging scoring logic. `connections.md` row 17 updated to reflect pending supersession.

- **SAM.gov cutover completed** (`23e2079`, ~12:49 EDT). Capture OS shipped a live Railway endpoint (repurposed the pre-existing "Contract-Hunter" Railway project: `https://contract-hunter-production-c52f.up.railway.app`). `scripts/sam_gov_api.py` was rewritten to call `GET /api/opportunities/search` on that endpoint instead of SAM.gov directly — the old 21-request loop (4 PSC + 7 NAICS + 10 keyword phrases) deleted, replaced with a single HTTP call. Script no longer reads `SAM_GOV_API_KEY` at all. Capture OS's API gained `notice_id`, `solicitation_number`, `set_aside`, and `point_of_contact` fields to support this. `connections.md` row 17: now marked **live, verified**. Tradeoff accepted: 10 keyword-phrase searches dropped (Capture OS does a single `cybersecurity` keyword + NAICS/PSC codes); NAICS/PSC codes catch the bulk of relevant postings, so narrower single-keyword coverage accepted over 10x request volume.

## Vault target

Both belong under `wiki/domains/sentinel-cmmc/` or a dedicated `vulnaguard-capture-os/` domain page (doesn't exist yet — may be worth creating, now that Capture OS has a live Railway deployment and a defined ownership role). These are product-architecture decisions, not dev churn.

---

*Check confirmed as run. No leads/inbox.md changes. No context/ changes.*
