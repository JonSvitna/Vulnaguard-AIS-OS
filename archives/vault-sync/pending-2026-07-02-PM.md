# Pending vault updates — 2026-07-02 PM

**Coverage window:** Since the 2026-07-01 AM note. Note: the 2026-07-01 PM note incorrectly said "nothing new" — `dc839e2` landed at 07:59 AM EDT on July 1, after the AM note was written and before the PM check ran.

---

## Business-relevant items to pull into Obsidian

- **AfterSwing onboarding materials created** — `playbook/engagements/2026-07_AfterSwing_NIST-171/00-onboarding/` now has a live onboarding checklist (tracks NDA/MSA/SOW signatures + deposit status) and a welcome letter ready to send to Don Weston at engagement start. First real client, first delivery artifacts in use. Worth updating the AfterSwing client page in the vault with "onboarding in progress." (`commit dc839e2`)

- **Delivery playbook formalized with Phase 0 + Phase 10** — Phase 0 (Client Onboarding) and Phase 10 (Sentinel Offboarding) are now fully specced phases in `playbook/phases/`, not just implied by the folder structure. Phase 0 defines the full pre-engagement gate: NDA → MSA → SOW → deposit → welcome letter → folder setup → client registration. Nothing billable starts until Phase 0 is complete. This is a repeatable process milestone — worth capturing in `wiki/domains/vulnaguard/delivery-playbook.md` if that page exists, or alongside the AfterSwing page. (`commit dc839e2`)

- **New proposal and BD templates added** — `playbook/templates/` now includes: `proposal.md`, `rules-of-engagement.md`, `welcome-letter.md`, `change-order.md`. These are live documents ready for future engagements, not just scaffolding. (`commit dc839e2`)

- **SAM.gov scanner refined + cache reset** — API filtering now requires title keywords OR a cyber-relevant PSC code (D310/D307/R425/R408) to qualify a result, reducing noise from unrelated contracts. 3-second rate limiting added. Contact cache (`leads/sam_gov_contacts.csv`) cleared and seen list reset — scanner is effectively starting a fresh sweep with better filters. Not a vault-level decision, but worth a note on the SAM.gov pipeline page if one exists. (`commit dc839e2`)

---

## Already logged / skip

- 2026-07-01 AM note covers: AfterSwing engagement kickoff (first client, VG-2026-001, Don Weston, Jul–Nov 2026), SAM.gov scanner operational, delivery playbook initial scaffold, branded BD document suite. Do not re-log those.
- No new entries in `decisions/log.md` or `leads/inbox.md` since the last AM check.
