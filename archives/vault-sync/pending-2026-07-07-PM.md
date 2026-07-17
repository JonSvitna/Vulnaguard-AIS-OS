# Pending vault updates — 2026-07-07 PM

**Coverage window:** Since the 2026-07-06 AM note (which found nothing new beyond what the 2026-07-06 PM note had already covered). PR #6 (`claude/gov-contract-strategy-3yisxk`) merged today carrying three substantive commits — all dated 2026-07-06, all business-level, none covered in any prior vault-sync note.

---

## What's new

### 1. First-federal-win playbook added (commit `eec83eb`)
New reference file: `references/gov-contract-win-playbook.md` (108 lines).
Covers the concrete course of action for landing a first $2.5k–$10k federal award as a newcomer: SAM.gov foundation checklist, micro-purchase strategy (awards under $10k, CO discretion, no competition required), fixed-price service packaging, and three plays in priority order — (1) sell direct to gov under the micro-purchase threshold, (2) sell CMMC readiness to defense prime contractors and subs, (3) subcontract under a prime to build past-performance quickly.

**Vault target:** `wiki/domains/sentinel-cmmc/` or a new `wiki/domains/vulnaguard-gov-contracts/` domain page. This is a strategic reference, not dev notes — belongs in the vault where it can inform the Sentinel CMMC go-to-market narrative.

---

### 2. Scanner tooling standard finalized (commit `63b4a0c`)
Logged in `decisions/log.md` (2026-07-06). Also written into `playbook/methodology/technical-standards.md` (new "Solo Starter Stack" and "Scanning Host / OS" sections).

**Decision summary:**
- **Primary scanner:** Nessus Professional (Tenable) — ACAS lineage makes it the credible DoD-recognized choice; single-seat install, no server infra.
- **Web DAST:** OWASP ZAP (free, kept in its correct web-layer slot — cannot serve as primary since it does no network/host scanning).
- **Pre-revenue bridge:** OpenVAS/Greenbone Community until first invoice funds a Nessus license.
- **Buy sequence:** Nessus Pro → ZAP + Nmap (free) → Metasploit Community → Burp Suite Pro (later).
- **Scanning host:** Kali Linux VM (snapshottable, one clean snapshot per engagement) + dedicated cloud instance (DigitalOcean droplet with static IP, whitelisted in the client's ROE for external scans).

**Vault target:** `wiki/domains/sentinel-cmmc/` or the gov-contracts domain page noted above. This is a product/service-line decision, not a dev config detail.

---

### 3. Documentation made mandatory — process decision (commit `e5d76d9`)
Logged in `decisions/log.md` (2026-07-06).

**Decision summary:** Documentation is now a hard requirement — nothing is "done" until documented. Wired into `CLAUDE.md` so it's enforced every session, not just aspirational. New files:
- `references/documentation-standard.md` — definition-of-done, where-it-lives table, federal/CMMC evidence requirements.
- `references/gov-contract-progress-log.md` — running completion log for the gov-contract initiative, seeded with three completed items (playbook, scanner standard, this doc standard itself).

**Vault target:** This is a business-process decision. Worth a brief note under `wiki/decisions/` or the top of the gov-contracts domain page — it affects all client delivery and is directly tied to federal/CMMC audit-trail requirements.

---

*No changes to `leads/inbox.md` or `context/` since last check.*
