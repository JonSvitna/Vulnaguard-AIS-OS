# Pending vault updates — 2026-07-21 AM

**Coverage window:** Since `pending-2026-07-20-AM.md` — commits `b50359c` and `c4f4a16` (2026-07-20 through 2026-07-21 07:00 UTC).

---

## New items to consider for Obsidian

### Cloud routines cadence reset to daily; Clay/n8n safety net decision (tool management)
- **What:** 4 claude.ai cloud Routines were running well above cadence (some up to 6x/day). Sean reset all to 1x/day: `commercial-lead-sourcing` → 6:00 AM daily; `commercial-lead-outreach-bridge` → 6:00 AM daily; `Overnight Lead Triage` → unpaused, 6:00 AM daily; `AM Vault Sync Check` → confirmed kept at 7:00 AM daily.
- **Key call:** The two commercial routines (`commercial-lead-sourcing`, `commercial-lead-outreach-bridge`) were flagged as likely superseded by the new Clay + n8n pipeline. Sean chose to keep them alive at low frequency rather than retire them — optionality while Clay/n8n is still unproven. Revisit retirement once Clay/n8n has a longer track record.
- **Why it matters:** Represents a deliberate product/tooling architecture call: Claude-side routines run as a parallel safety net, not the primary lead pipeline. Establishes a "low frequency + keep optionality" pattern for deprioritized automations.
- **Commit:** `b50359c` (decisions log entry) | **Decisions log entry:** 2026-07-20 — "Cut all cloud Routines to daily, kept them alive instead of retiring"
- **Note:** These routines live only in claude.ai's Routines UI — not visible from any Claude Code session.
- **Vault target:** `wiki/decisions/` — tooling architecture + market positioning for the outreach stack.

### Lead triage failure: MS365 auth still not configured (ops note)
- **What:** Today's overnight lead-triage run failed again — `MS365_USER_UPN` and `MS365_TENANT_ID` are missing from the remote session environment. No new leads added to `leads/inbox.md`. Same root cause as yesterday.
- **Fix:** Set `MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`, and `MS365_USER_UPN` in the session/environment config.
- **Commit:** `b50359c` | **Decisions log entry:** 2026-07-21 — "Overnight Lead Triage run failed: MS365 auth not configured"
- **Vault target:** Skip — operational/infra gap, not a business decision. Flagging here for awareness only.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut (`commit 74deeb5`, flagged in `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **Retired website-design-lead-finder agent** — automation retirement (`commit 68bf73d`, flagged in `pending-2026-07-19-AM.md`). Vault target: `wiki/decisions/`.
- **n8n content workflows paused + creative-os-render-worker already gone** — infra cleanup + gap discovery (`commit 68bf73d`, flagged in `pending-2026-07-19-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **Clay wired as lead source → SEO agent via n8n** — pipeline architecture (`commit 4b0197e`, flagged in `pending-2026-07-20-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning (`commit 4b0197e`, flagged in `pending-2026-07-20-AM.md`). Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-21 AM. Next check: 2026-07-22 AM.*
