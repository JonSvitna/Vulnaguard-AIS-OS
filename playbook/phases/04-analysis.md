---
title: Phase 4 — Analysis
phase: 4
updated: 2026-06-30
---

# Phase 4: Analysis

**Objective:** Transform raw assessment data into a validated, risk-rated findings list ready for reporting.

---

## Entry Criteria

- Phase 3 quality gate passed
- Running findings log complete
- Evidence library complete

---

## Activities

### 4.1 False Positive Review
- Review every automated scanner finding for validity
- Cross-reference CVEs against current exploit databases (NVD, ExploitDB, CISA KEV)
- Confirm finding is reproducible / verifiable via evidence
- Document disposition: valid / false positive / needs further investigation

### 4.2 Risk Rating
- Apply the Vulnaguard risk rating model to every validated finding
- Document likelihood and impact scores
- Apply any environmental adjustments (internet-facing, CUI exposure, compensating controls)
- Record the rationale for any non-standard rating

### 4.3 Framework Control Mapping
For compliance assessments:
- Map every finding to the applicable control (NIST 800-171 practice ID, CMMC domain, etc.)
- Record control status: Met / Partially Met / Not Met / Not Applicable
- Document justification for "Not Applicable" designations

### 4.4 Root Cause Analysis
- For each finding, identify the root cause (missing process, misconfiguration, lack of training, technical debt, etc.)
- Group related findings where appropriate (e.g., "5 findings share the root cause of no patch management process")

### 4.5 Remediation Recommendations
- Write specific, actionable remediation guidance for each finding
- Include estimated effort level: Quick Win (< 1 week) / Short-Term (1–90 days) / Long-Term (90+ days)
- Call out any commercial tools or specific configuration steps where relevant

### 4.6 Peer Review
- All Critical and High findings must be independently reviewed by a second consultant
- Document reviewer name and date in the findings log
- Reviewer may challenge severity ratings — resolve disagreements by consensus or escalate to lead

### 4.7 Executive Summary Draft
- Identify the 3–5 most significant findings or themes
- Draft a plain-English narrative for a non-technical executive audience
- Do not use CVE IDs or technical jargon in the executive summary

---

## Outputs

- Validated findings list (no false positives, all items rated)
- Root cause notes
- Remediation recommendations
- Framework control mapping (compliance engagements)
- Peer review documentation
- Draft executive summary

---

## Deliverables to Client

None — this is an internal phase.

---

## Quality Gate

- [ ] No unvalidated findings remain
- [ ] Every finding has a severity rating with documented rationale
- [ ] All Critical and High findings have been peer reviewed
- [ ] Framework mapping complete (compliance engagements)
- [ ] Draft executive summary reviewed internally

---

## Common Issues

**Disagreement on severity rating:** Document both positions, select the more conservative rating, note the disagreement in the QA log.

**Too many findings to write individual recommendations:** Group related findings under a single root cause finding with one recommendation. Don't pad the report — prioritize clarity.

**Scanner output is overwhelming:** Filter to validated, non-informational findings first. Build the report top-down (Critical → High → Medium) and work on lower severities if time permits within scope.
