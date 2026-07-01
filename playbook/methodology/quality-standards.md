---
title: Quality Standards
version: 1.0
updated: 2026-06-30
---

# Quality Standards

Every Vulnaguard deliverable goes through QA before client delivery. These standards are non-negotiable regardless of engagement size.

---

## QA Checklist — All Engagements

### Scope Validation
- [ ] All assets/systems/controls in scope are accounted for in findings
- [ ] No out-of-scope items appear in the findings list
- [ ] Scope boundary is documented and consistent with signed SOW

### Findings Quality
- [ ] Every finding has: title, severity, description, evidence, recommendation
- [ ] No findings left at "unrated" severity
- [ ] All critical and high findings independently validated (not just self-reviewed)
- [ ] False positive review completed and documented
- [ ] Remediation recommendations are specific and actionable — not generic

### Report Quality
- [ ] Executive summary is readable by a non-technical stakeholder
- [ ] Technical report accurately reflects all validated findings
- [ ] Risk ratings are consistent with the risk rating model
- [ ] No client name errors, placeholder text, or formatting issues
- [ ] Document version and date are correct

### Deliverables
- [ ] All SOW-required deliverables are present
- [ ] Files are named using the standard naming convention
- [ ] Documents are in both editable (Word) and signed (PDF) format where required

---

## QA Checklist — Technical Assessments (VA)

- [ ] All target IPs/URLs confirmed in scope and scanned
- [ ] Scan coverage report reviewed — no unexpected gaps
- [ ] Critical/high CVEs cross-referenced against public exploit databases
- [ ] Plugin/scanner version documented
- [ ] No scan data from out-of-scope systems included in report

---

## QA Checklist — Compliance Assessments (CMMC / NIST 800-171)

- [ ] All 110 NIST SP 800-171 controls reviewed (or applicable subset documented)
- [ ] Each control status is one of: Met / Partially Met / Not Met / Not Applicable
- [ ] "Not Applicable" designations are justified in writing
- [ ] Evidence cited for every "Met" determination
- [ ] POA&M covers every "Not Met" and "Partially Met" item
- [ ] POA&M milestones are realistic (not all set to the same far-future date)

---

## Peer Review Requirements

| Severity of Findings | Peer Review Required? |
|---|---|
| Any Critical | Yes — mandatory before client delivery |
| Any High | Yes |
| Medium only | Recommended but not required |
| Low / Informational only | Not required |

Peer review means a second qualified consultant reads the finding and agrees with the severity rating and recommendation. Document who reviewed and when.

---

## Naming Conventions

**Engagement folder:** `{YYYY-MM}_{ClientSlug}_{ServiceCode}`

Example: `2026-07_AcmeDefense_CMMC-L2`

**Service codes:**
- `VA` — Vulnerability Assessment
- `CMMC-L2` — CMMC Level 2 Readiness
- `NIST-171` — NIST 800-171 Gap
- `SPA` — Security Program Assessment
- `ERA` — Executive Risk Assessment
- `POLICY` — Policy Development
- `SENTINEL` — Sentinel Implementation

**Report files:** `{ClientSlug}_{ServiceCode}_Report_v{N}.{ext}`

Example: `AcmeDefense_CMMC-L2_Report_v1.docx`

**Final versions:** Append `_FINAL` when issuing the signed/approved version.

---

## File Storage Structure

```
engagements/
  {YYYY-MM}_{ClientSlug}_{ServiceCode}/
    01-discovery/
    02-planning/
    03-assessment/
    04-analysis/
    05-reports/
      drafts/
      final/
    06-closeout/
```

---

## Client Acceptance Gate

No engagement closes without a signed acceptance form. This is the formal record that the client received and accepted all deliverables. File the signed acceptance form in `06-closeout/`.
