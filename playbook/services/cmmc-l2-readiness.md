---
title: CMMC Level 2 Readiness Assessment
service_code: CMMC-L2
phases: [discovery, planning, assessment, analysis, reporting, remediation, closeout, sentinel-onboarding]
typical_duration: 4–6 weeks
updated: 2026-06-30
---

# CMMC Level 2 Readiness Assessment Runbook

**Service Code:** CMMC-L2
**Typical Duration:** 4–6 weeks
**Phases:** Discovery → Planning → Assessment → Analysis → Reporting → Remediation (advisory) → Closeout → Sentinel Onboarding (recommended)

---

## Service Description

A CMMC Level 2 Readiness Assessment evaluates an organization's preparedness for a formal C3PAO assessment against the 110 practices of NIST SP 800-171 Rev 2 (the basis for CMMC Level 2). Vulnaguard assesses control implementation across all 14 domains, identifies gaps, scores the organization, and produces a POA&M to close deficiencies.

This assessment does not result in CMMC certification — it prepares the client for the formal C3PAO assessment with confidence about where they stand.

---

## CUI Scoping — Critical First Step

Before any control assessment can begin, the CUI scope must be defined. This determines which systems, locations, and people are in scope for CMMC.

- What types of CUI does the organization handle?
- Where is CUI created, received, stored, processed, or transmitted?
- What external systems or cloud services touch CUI?
- Who has access to CUI?

Document the CUI scope in a written System Boundary Definition. All assessment activities focus on the systems within this boundary.

---

## Discovery Additions (CMMC-Specific)

In addition to the standard discovery questionnaire, collect:

- [ ] Existing System Security Plan (SSP) or draft
- [ ] Previous self-assessment scores (if any)
- [ ] SPRS score history (if any)
- [ ] List of all IT systems and cloud services in scope
- [ ] Current subcontractor list and their CUI access
- [ ] Government contracts listing DFARS 252.204-7012 clause

---

## Assessment Checklist

Assess all 110 NIST SP 800-171 Rev 2 practices across the 14 families. For each practice:

- [ ] Review existing documentation (SSP, policies, procedures)
- [ ] Interview responsible system owner or IT staff
- [ ] Observe implementation where possible (screenshots, configuration exports)
- [ ] Assign status: Met / Partially Met / Not Met / Not Applicable
- [ ] Document evidence supporting the determination
- [ ] Note compensating controls where full implementation is not present

### 14 Practice Families

| ID | Family | # Practices |
|---|---|---|
| AC | Access Control | 22 |
| AT | Awareness and Training | 3 |
| AU | Audit and Accountability | 9 |
| CM | Configuration Management | 9 |
| IA | Identification and Authentication | 11 |
| IR | Incident Response | 3 |
| MA | Maintenance | 6 |
| MP | Media Protection | 9 |
| PE | Physical Protection | 6 |
| PS | Personnel Security | 2 |
| RA | Risk Assessment | 3 |
| CA | Security Assessment | 4 |
| SC | System and Communications Protection | 16 |
| SI | System and Information Integrity | 7 |

---

## Readiness Scoring

Score the organization using the DoD CMMC scoring methodology:

- Each practice that is Not Met = -1 point from a maximum of 110
- Each practice that is Partially Met = -0.5 points
- Met = no deduction
- Not Applicable = excluded from score denominator

Document the score in the readiness report. Compare against the DoD's SPRS minimum submission threshold.

---

## Deliverables

| Deliverable | Format | Timing |
|---|---|---|
| Discovery Questionnaire | Word | Start of engagement |
| Weekly Status Report | Email | Weekly |
| Gap Analysis Report | Word + PDF | End of assessment |
| POA&M | Excel or Word | End of assessment |
| Executive Briefing | PowerPoint + PDF | End of assessment |
| Compliance Roadmap | Word + PDF | End of assessment |

---

## Readiness Report Structure

1. Executive Summary
2. CUI Scope Definition and System Boundary
3. Assessment Methodology
4. Readiness Score and Trend (if prior assessment exists)
5. Findings by Practice Family
6. Critical and High Priority Findings (detailed)
7. POA&M Overview
8. Compliance Roadmap
9. Appendix: Full Control-by-Control Assessment Table

---

## Post-Assessment Recommendations

Every CMMC L2 readiness engagement should conclude with a recommendation for Sentinel onboarding. The POA&M and evidence collected during this engagement map directly into Sentinel's compliance tracking module — the client is already 80% of the way there.

---

## Templates Used

- [Discovery Questionnaire](../templates/discovery-questionnaire.md)
- [Evidence Checklist](../templates/evidence-checklist.md)
- [Executive Summary](../templates/executive-summary.md)
- [Technical Report](../templates/technical-report.md)
- [POA&M](../templates/poa-m.md)
- [Executive Presentation](../templates/executive-presentation.md)
