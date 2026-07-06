# Gov Contract Initiative — Progress Log

Running record of everything completed on the "secure a first federal win" initiative. Per the mandatory Documentation Standard (`references/documentation-standard.md`), every completed item is logged here as it's done.

Newest entries first.

---

## 2026-07-06 — Documentation made mandatory

- Created `references/documentation-standard.md` — the standing rule that nothing is "done" until documented, with a where-it-lives table and the federal/CMMC client-documentation requirements.
- Wired the standard into `CLAUDE.md` so it's enforced every session.
- Created this progress log and seeded it with the session's completed work.
- Logged the process decision in `decisions/log.md`.

## 2026-07-06 — Scanner tooling standard set

- Decision: **Nessus Professional** is the primary network/host scanner (credibility anchor via DoD ACAS lineage); **OWASP ZAP** kept for the web-app layer only; **OpenVAS/Greenbone** as pre-revenue bridge.
- Added **Solo Starter Stack** (buy-first sequence) and **Scanning Host / OS** (Kali VM, per-engagement snapshots, static-IP cloud instance for external scans) sections to `playbook/methodology/technical-standards.md`.
- Logged in `decisions/log.md` (2026-07-06 scanner entry).
- **Open for Sean:** confirm Nessus Pro purchase; pick scanning-host location (local Kali VM vs. persistent DigitalOcean droplet).

## 2026-07-06 — First-win strategy documented

- Created `references/gov-contract-win-playbook.md` — course of action for landing a first $2.5k–$10k federal award as a newcomer.
- Core points: the $2.5k–$10k range is the **micro-purchase zone** (under $10k, no formal competition required); SAM.gov registration + UEI is the required foundation; lead with one fixed-price service (Network Vulnerability Assessment); three plays (sell services to gov, sell CMMC to defense contractors, subcontract for past performance).
- **Open for Sean:** confirm SAM.gov entity registration is ACTIVE (not just the API key); check set-aside eligibility; draft the one-page capability statement.

---

## Standing next actions (not yet done)

1. Verify SAM.gov entity registration is active with a UEI.
2. Check socioeconomic set-aside eligibility (veteran / 8(a) / HUBZone / WOSB).
3. Draft the one-page capability statement.
4. Package the fixed-price Network Vulnerability Assessment offering.
5. Confirm Nessus Pro purchase and stand up the scanning host.
