---
title: Phase 0 — Client Onboarding
phase: 0
updated: 2026-07-01
---

# Phase 0: Client Onboarding

**Objective:** Execute all pre-engagement paperwork, set up the client's delivery environment, and confirm everything is in place before assessment work begins.

**This phase runs before Phase 1 (Discovery). Nothing billable starts until Phase 0 is complete.**

---

## Entry Criteria

- Verbal or written intent to engage received from the client
- Service scope and rough budget agreed in principle
- Client primary contact and legal contact identified

---

## Activities

### 0.1 Send Proposal
- Generate proposal from template (service description, scope, timeline, pricing)
- Send to client for review
- Follow up within 3 business days if no response

### 0.2 Execute NDA
- Send NDA for signature via DocuSign (or email PDF)
- No sensitive information shared until NDA is countersigned
- File signed NDA in `00-onboarding/` under the client engagement folder

### 0.3 Execute MSA
- Send Master Services Agreement
- Confirm governing law, liability caps, and payment terms with client's legal contact
- File countersigned MSA in `00-onboarding/`

### 0.4 Execute SOW
- Generate SOW from template — fill in: scope, deliverables, timeline, payment schedule, point of contact
- Attach to the executed MSA or reference it as a standalone
- No billable work starts until SOW is countersigned
- File countersigned SOW in `00-onboarding/`

### 0.5 Collect Deposit (if applicable)
- Per SOW payment schedule, confirm deposit invoice is sent and paid before kickoff
- Log payment receipt in the engagement folder

### 0.6 Send Welcome Letter
- Send client a welcome letter confirming: engagement start, primary contacts on both sides, what to expect in Phase 1, and where to direct questions
- CC: client primary + technical contact

### 0.7 Set Up Engagement Folder
- Create client engagement folder: `engagements/YYYY-MM_{ClientName}_{Service}/`
- Scaffold subfolders: `00-onboarding/`, `01-discovery/`, `02-planning/`, `03-assessment/`, `04-analysis/`, `05-reports/`, `06-closeout/`
- Move all signed documents into `00-onboarding/`

### 0.8 Register Client Contacts
- Record client contacts in the engagement README:
  - Primary contact (day-to-day)
  - Executive sponsor
  - Technical / IT contact
  - Legal / contract contact (if different from above)
- Add to CRM or contact log if applicable

---

## Outputs

- Signed NDA, MSA, SOW on file
- Deposit received (if applicable)
- Welcome letter sent
- Engagement folder scaffolded and ready for Phase 1

---

## Deliverables to Client

- Countersigned NDA (their copy)
- Countersigned MSA (their copy)
- Countersigned SOW (their copy)
- Welcome letter

---

## Quality Gate

- [ ] NDA fully executed (both parties signed)
- [ ] MSA fully executed
- [ ] SOW fully executed
- [ ] Deposit received (if SOW requires one)
- [ ] Welcome letter sent
- [ ] Engagement folder created with all signed documents filed
- [ ] Client contacts logged in engagement README

---

## Templates Used

- [Proposal](../templates/proposal.md)
- [NDA](../templates/nda.md)
- [Master Services Agreement](../templates/msa.md)
- [Statement of Work](../templates/sow.md)
- [Welcome Letter](../templates/welcome-letter.md)

---

## Common Issues

**Client wants to start before paperwork is signed:** Hold firm. No billable work, no information sharing, and no kickoff scheduling until NDA + SOW are fully executed. Frame it as protecting both parties.

**Client's legal team redlines the MSA:** Log all redlines and changes. If scope changes materially, escalate before accepting. Keep a clean copy of the final negotiated version on file — that version supersedes the template.

**Client provides their own paper (contract):** Review carefully against Vulnaguard's standard terms. Flag any gaps in liability, IP ownership, payment terms, or termination clauses before signing. When in doubt, have it reviewed by a contract attorney.

**Deposit invoice goes unpaid past due date:** Do not start Phase 1 until resolved. Send a follow-up after 3 business days. Escalate if unpaid by 7 days.
