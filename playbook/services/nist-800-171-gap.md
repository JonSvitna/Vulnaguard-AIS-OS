---
title: NIST SP 800-171 Gap Assessment
service_code: NIST-171
phases: [discovery, planning, assessment, analysis, reporting, closeout]
typical_duration: 3–4 weeks
updated: 2026-06-30
---

# NIST SP 800-171 Gap Assessment Runbook

**Service Code:** NIST-171
**Typical Duration:** 3–4 weeks
**Phases:** Discovery → Planning → Assessment → Analysis → Reporting → Closeout

---

## Service Description

A NIST SP 800-171 Gap Assessment evaluates an organization's implementation of the 110 security practices in NIST SP 800-171 Rev 2. Unlike a CMMC L2 Readiness Assessment, this is framework-agnostic — it can serve any organization that handles CUI or wants to adopt the NIST 800-171 framework as a security baseline.

The output is a gap analysis documenting where the organization meets, partially meets, or does not meet each practice, with a prioritized compliance roadmap.

---

## Difference from CMMC L2 Readiness

| Factor | NIST 800-171 Gap | CMMC L2 Readiness |
|---|---|---|
| Certification path | No | Yes (prepares for C3PAO) |
| SPRS score | Not typically | Yes |
| Scoring method | Qualitative gap | DoD numerical scoring |
| Primary audience | Any CUI handler | DoD contractors |
| Follow-on | Roadmap | POA&M + C3PAO prep |

Use NIST 800-171 Gap for clients who aren't yet on the DoD CMMC path but want to get their 800-171 house in order.

---

## Discovery Additions

- [ ] Current SSP or security documentation
- [ ] List of CUI types handled
- [ ] System boundary / network diagram
- [ ] Existing policies and procedures
- [ ] Any prior assessments or self-assessments

---

## Assessment Checklist

For each of the 110 practices:

- [ ] Review documentation (policies, procedures, SSP)
- [ ] Interview responsible personnel
- [ ] Request evidence (configurations, screenshots, logs, training records)
- [ ] Assign status: Met / Partially Met / Not Met / Not Applicable
- [ ] Document evidence citations
- [ ] Note control gaps for roadmap prioritization

---

## Deliverables

| Deliverable | Format | Timing |
|---|---|---|
| Weekly Status Report | Email | Weekly |
| Gap Analysis Report | Word + PDF | End of engagement |
| Control-by-Control Assessment Table | Excel | End of engagement |
| Compliance Roadmap | Word + PDF | End of engagement |
| Executive Summary | Word + PDF | End of engagement |

---

## Gap Report Structure

1. Executive Summary
2. Assessment Scope and Methodology
3. Overall Gap Summary (met / partially met / not met counts by family)
4. Findings by Practice Family
5. Priority Findings (top 10 by risk)
6. Compliance Roadmap (phased remediation plan)
7. Appendix: Full Control Assessment Table

---

## Compliance Roadmap Format

Phase the roadmap into 3 horizons:

- **30-Day Quick Wins:** Low effort, high impact. Policy gaps, free tool configurations, account hygiene.
- **90-Day Short-Term:** Moderate effort. Missing processes, basic technical controls.
- **12-Month Long-Term:** High effort. Infrastructure changes, tool procurement, training programs.

Each roadmap item should list: practice ID, finding description, recommended action, effort level, estimated cost (if applicable).

---

## Templates Used

- [Discovery Questionnaire](../templates/discovery-questionnaire.md)
- [Evidence Checklist](../templates/evidence-checklist.md)
- [Technical Report](../templates/technical-report.md)
- [Executive Summary](../templates/executive-summary.md)
