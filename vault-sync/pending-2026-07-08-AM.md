# Pending vault updates — 2026-07-08 AM

**Coverage window:** Since the 2026-07-08 PM note (nothing new logged then). Covers the overnight hermes-cron run at 03:54 UTC.

---

## SEO agent content opportunities (hermes-cron, 4 new entries)

Commit `c139d5d` — `hermes-pending/pending-2026-07-08-1783482858326.md`

These are candidate "Behind the Build" / "Lesson from a Mistake" content posts surfaced from recent vulnaguard-seo-agent commits. All tagged `Vulnaguard` domain, all `unused` — ready to promote to `references/hermes-opportunities.md` if Sean approves.

- **four-touch-sequence-scheduling-bug** — 4th email touch had `scheduled_at = NULL` due to hardcoded touch numbers; fixed by querying actual touch numbers from DB dynamically. `commercial_security` now gets a 4-touch cadence; other lines stay at 3.
- **llm-ignores-hard-rules-deterministic-fix** — The AI sent a live LinkedIn message with an em dash despite a hard no-em-dash rule. Two-layer fix: rewritten checklist prompt + deterministic post-processing substitution before any message leaves the system.
- **llm-dodges-exact-string-ban-by-inflecting** — Model used "circling back" to dodge a "circle back" ban. Fix: prompt now names inflected forms explicitly + regex backstop (`/circl\w* back/i`) fires before human approval.
- **can-spam-footer-deterministic-backstop** — Live test showed the AI skipped the CAN-SPAM opt-out footer. Fix: FINAL CHECKLIST prompt shows footer verbatim in JSON schema example + code-level post-processing appends it if the model still skips.

**Vault action:** These are builder-insight stories worth saving under `wiki/domains/seo-agent/content-bank/` or similar. Run `/hermes` to merge into `hermes-opportunities.md` first.

---

## No other new business items

No new entries in `decisions/log.md`, `leads/inbox.md`, or `context/` files since the PM check.
