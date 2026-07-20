# Pending vault updates — 2026-07-20 AM

**Coverage window:** Since `pending-2026-07-19-AM.md` — commits `4b0197e` and `d19a92f` (2026-07-19 04:55 EDT through 2026-07-20 10:03 UTC).

---

## New items to consider for Obsidian

### Clay wired as lead source → SEO agent via n8n (business architecture)
- **What:** Clay is now the upstream lead-discovery and enrichment tool. Verified-email rows route through a live n8n workflow (`Clay Lead Intake to SEO Agent`, ID `A6kOqisezATjjT2Q`) into the SEO agent's existing import/dedup/qualification endpoint. Clay does not become a parallel outreach system — the SEO agent's approval gate still controls what gets sent.
- **What shipped:** `infra/n8n/clay-lead-intake.workflow.json` (version-controlled workflow source), `references/clay-lead-intake.md` (full runbook with ICP, setup, required columns, guardrails, live IDs), `connections.md` updated with Clay integration row.
- **Next step:** Sean completes the Clay table + HTTP-action mapping in his own authenticated Clay session. Do a 25-row quality test before scaling. Clay workbooks: broad `wb_0tig3j6w3hc4rmRuHmm`, CMMC-focused `wb_0tig3ciNVGjGucRT29T`.
- **Commit:** `4b0197e` | **Decisions log entries:** 2026-07-19 (Clay feeds SEO agent pipeline through n8n)
- **Vault target:** `wiki/decisions/` or `wiki/domains/seo-agent/` — outreach pipeline architecture decision.

### ICP / market strategy: broad U.S. SMBs, not CMMC-only (market positioning)
- **What:** Two log entries in the same session — one narrowed, one immediately corrected. Net decision: Vulnaguard sources private U.S. SMBs broadly (2-200 employees, owner-led), across cybersecurity, compliance, automation, systems/software, and website/design. Government contractors are one lane, not the admission requirement. The capability statement showed the full service range, not a market filter.
- **Excluded:** enterprise/institutional targets that exceed startup delivery capacity. Daily volume target: 200-300 raw sourced, enrich only the best ~50 per day initially.
- **Why it matters:** This supersedes the earlier CMMC-focused sourcing model and widens the commercial TAM significantly.
- **Commit:** `4b0197e` | **Decisions log entries:** 2026-07-19 (Clay ICP narrowed + Correction: Clay market stays broad)
- **Vault target:** `wiki/decisions/` — market positioning correction worth recording.

### Lead-triage failed today — MS365 env vars missing from remote session (ops note)
- **What:** This morning's automated lead-triage run failed: `scripts/microsoft365_api.py` exited with `KeyError: 'MS365_USER_UPN'` and `MS365_TENANT_ID` absent. No new leads added to `leads/inbox.md`.
- **Fix needed:** Set `MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`, and `MS365_USER_UPN` as environment variables in the remote session configuration before the next scheduled run.
- **Commit:** `d19a92f`
- **Vault target:** Skip — operational/infra gap, not a business decision. Flagging here for Sean's awareness only.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut (`commit 74deeb5`, flagged in `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **Retired website-design-lead-finder agent** — automation retirement (`commit 68bf73d`, flagged in `pending-2026-07-19-AM.md`). Vault target: `wiki/decisions/`.
- **n8n content workflows paused + creative-os-render-worker already gone** — infra cleanup + gap discovery (`commit 68bf73d`, flagged in `pending-2026-07-19-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.

---

*Check ran: 2026-07-20 AM. Next check: 2026-07-20 PM.*
