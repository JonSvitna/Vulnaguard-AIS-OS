# Pending vault updates — 2026-07-01 AM

**Note:** The PM check (8240e4c, ~00:02 UTC) ran before three large commits landed (03:04–03:53 UTC). Those are all new and none have appeared in a prior vault-sync note.

---

## Business-relevant items to pull into Obsidian

- **FIRST CLIENT: AfterSwing (VG-2026-001)** — NIST SP 800-171 Gap Assessment engagement kicked off. Contact: Don Weston. Period: 2026-07-01 → 2026-11-01. Engagement folder: `playbook/engagements/2026-07_AfterSwing_NIST-171/`. SOW drafted and exported. Logged in `decisions/log.md` (entry dated 2026-06-30). This is the first real paying engagement — milestone worth a wiki page under `wiki/domains/sentinel-cmmc/clients/afterswing.md` or similar. (`commit 3a6e8b3`)

- **SAM.gov contract scanner operational** — `scripts/sam_gov_api.py` scans SAM.gov by Vulnaguard's PSC codes (D310/D307/R425/R408) and NAICS codes (541512/541519 etc.), scores by keyword/code match, deduplicates via `leads/sam_gov_seen.json`, and posts high-score opportunities to `#gov-contracts` Slack. Already captured 310 POC contacts to `leads/sam_gov_contacts.csv`. New automated government lead pipeline — flag in `wiki/domains/sentinel-cmmc/comms/` or a dedicated leads-pipeline page. (`commit 64a612e`)

- **Vulnaguard delivery playbook codified** — 9-phase engagement lifecycle, 7 service runbooks (CMMC L2 readiness, NIST 800-171 gap, sentinel implementation, policy dev, exec risk, vulnerability assessment, security program), 15+ templates (SOW, POA&M, discovery questionnaire, evidence checklist, kickoff agenda, etc.). Source of truth at `playbook/index.md`. This is a strategic capability milestone — Vulnaguard now has a repeatable delivery methodology. Worth logging in `wiki/domains/vulnaguard/delivery-playbook.md`. (`commit 3a6e8b3`)

- **Branded BD document suite ready for government contracting** — Full suite now exists: capability statement (HTML+PDF), pricing matrix, CMMC readiness report template, proposal template, quote template, invoice template, service catalog, QASP, subcontractor agreement, teaming agreement, deliverable acceptance form — all Vulnaguard-branded. Also added `references/vulnaguard-bd-voice.md` (tone/voice guide for external BD outreach). Sales materials are ready to use. (`commit cf34296`)

---

## Already logged / skip

- Hermes cron scan (5b497df, 03:53 UTC) — 1 new entry, AfterSwing camera rotation bug fix. Technical lesson (SeanBuilds content angle), not a business decision. Leave for the `/hermes` merge flow, not the vault.
- Stripe API invoicing enhancements and mail-to-Slack dedup improvements from commit 3a6e8b3 — internal dev tooling, not vault-level.
