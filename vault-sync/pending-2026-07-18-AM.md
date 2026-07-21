# Pending vault updates — 2026-07-18 AM

**Coverage window:** Since `pending-2026-07-17-PM.md` (commit `6d3a96b`).

---

## New items to consider for Obsidian

### SEO agent: stripped to one job (major product direction change)
- **What:** Deleted 5,101 lines from `vulnaguard-seo-agent` in a single commit (`74deeb5`) — removed the original M1–M6 SEO modules, content pipeline, video-brief UI, GitHub/GSC/Pexels integrations, and session-management API.
- **Surviving surface:** import leads → qualify → draft multi-touch email sequence → approve to send. Nothing else.
- **Why it's vault-worthy:** This is a hard product direction call — the content pipeline had its own docs, brand-voice prompts, and DB schema. Killing it is a "kill your darlings" moment worth recording as intent, not just a commit diff.
- **Hermes source:** `references/hermes-pending/pending-2026-07-17-1784260443122.md` (staged, not yet merged to hermes-opportunities)
- **Vault target:** `wiki/domains/sentinel-cmmc/` or a new `wiki/domains/seo-agent/` page; or `wiki/decisions/` if you want to track the rationale.

### SEO agent: approve now sends immediately (workflow fix)
- **What:** Collapsed the Approve → Release two-step into a single action (`commit 1dca53f`). Approved sequences now fire immediately and report a sent count. Added a bulk "Approve & send all drafted" action to clear the backlog. No-email leads park in a dead-letter state before consuming an AI scoring call.
- **Why it's vault-worthy:** This unblocked an actual lead backlog — emails were approved but never sent because the release step was a forgotten manual step. Good candidate for a "process lesson" note (hidden queues = invisible debt).
- **Hermes source:** same pending file above.
- **Vault target:** same as above, or as a process note.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`. Reference doc: `references/prism-os.md`.

---

---

## Re-check — 2026-07-18 AM (second pass)

**Commit reviewed:** `f35de5b` (hermes-cron scan run, 1 new entry)
**Finding:** Only new item is a technical bug fix — Resend settings page showed "unset" even when actually configured on Railway. Fixed with a live server check (`/api/marketing/config`). Technical only; not business-relevant. Not staged for Obsidian.

**No new vault-worthy items since the first AM pass.**

*Re-check ran: 2026-07-18 AM. Next check: 2026-07-18 PM.*
