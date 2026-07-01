---
title: Vulnaguard Delivery Playbook
version: 1.0
updated: 2026-06-30
---

# Vulnaguard Delivery Playbook

The authoritative source for how Vulnaguard delivers every engagement. All runbooks, templates, and checklists originate here. Client-facing documents are generated from these sources.

---

## Service Catalog

| Service | File | Typical Duration | Output |
|---|---|---|---|
| Vulnerability Assessment | [services/vulnerability-assessment.md](services/vulnerability-assessment.md) | 2–3 weeks | VA Report |
| CMMC Level 2 Readiness Assessment | [services/cmmc-l2-readiness.md](services/cmmc-l2-readiness.md) | 4–6 weeks | Readiness Report + POA&M |
| NIST SP 800-171 Gap Assessment | [services/nist-800-171-gap.md](services/nist-800-171-gap.md) | 3–4 weeks | Gap Report + Roadmap |
| Security Program Assessment | [services/security-program.md](services/security-program.md) | 3–5 weeks | Maturity Report |
| Executive Risk Assessment | [services/executive-risk.md](services/executive-risk.md) | 2–3 weeks | Risk Dashboard |
| Security Policy Development | [services/policy-development.md](services/policy-development.md) | 3–6 weeks | Policy Package |
| Sentinel Implementation | [services/sentinel-implementation.md](services/sentinel-implementation.md) | 1–2 weeks | Live Sentinel Tenant |

---

## Standard Engagement Lifecycle

Every engagement follows the same structure. Phase 0 is mandatory before any billable work begins. Phase 10 runs only when a client offboards from Sentinel.

| Phase | File |
|---|---|
| 0. Client Onboarding | [phases/00-client-onboarding.md](phases/00-client-onboarding.md) |
| 1. Discovery | [phases/01-discovery.md](phases/01-discovery.md) |
| 2. Planning | [phases/02-planning.md](phases/02-planning.md) |
| 3. Assessment | [phases/03-assessment.md](phases/03-assessment.md) |
| 4. Analysis | [phases/04-analysis.md](phases/04-analysis.md) |
| 5. Reporting | [phases/05-reporting.md](phases/05-reporting.md) |
| 6. Remediation | [phases/06-remediation.md](phases/06-remediation.md) |
| 7. Validation | [phases/07-validation.md](phases/07-validation.md) |
| 8. Closeout | [phases/08-closeout.md](phases/08-closeout.md) |
| 9. Sentinel Onboarding (Optional) | [phases/09-sentinel-onboarding.md](phases/09-sentinel-onboarding.md) |
| 10. Sentinel Offboarding | [phases/10-sentinel-offboarding.md](phases/10-sentinel-offboarding.md) |

---

## Templates

| Template | File | Used In |
|---|---|---|
| Proposal | [templates/proposal.md](templates/proposal.md) | Phase 0 |
| Statement of Work | [templates/sow.md](templates/sow.md) | Phase 0 |
| Master Services Agreement | [templates/msa.md](templates/msa.md) | Phase 0 |
| NDA | [templates/nda.md](templates/nda.md) | Phase 0 |
| Welcome Letter | [templates/welcome-letter.md](templates/welcome-letter.md) | Phase 0 |
| Discovery Questionnaire | [templates/discovery-questionnaire.md](templates/discovery-questionnaire.md) | Phase 1 |
| Kickoff Agenda | [templates/kickoff-agenda.md](templates/kickoff-agenda.md) | Phase 2 |
| Status Report | [templates/status-report.md](templates/status-report.md) | All phases |
| Evidence Checklist | [templates/evidence-checklist.md](templates/evidence-checklist.md) | Phase 1–3 |
| Executive Summary | [templates/executive-summary.md](templates/executive-summary.md) | Phase 5 |
| Technical Report | [templates/technical-report.md](templates/technical-report.md) | Phase 5 |
| Risk Register | [templates/risk-register.md](templates/risk-register.md) | Phase 4–5 |
| POA&M | [templates/poa-m.md](templates/poa-m.md) | Phase 5 |
| Executive Presentation | [templates/executive-presentation.md](templates/executive-presentation.md) | Phase 5 |
| Closeout Report | [templates/closeout-report.md](templates/closeout-report.md) | Phase 8 |
| Client Acceptance Form | [templates/acceptance-form.md](templates/acceptance-form.md) | Phase 8 |
| Rules of Engagement | [templates/rules-of-engagement.md](templates/rules-of-engagement.md) | Phase 2 |
| Change Order | [templates/change-order.md](templates/change-order.md) | Any phase |

---

## Methodology References

- [Engagement Lifecycle](methodology/engagement-lifecycle.md)
- [Risk Rating Model](methodology/risk-rating-model.md)
- [Quality Standards](methodology/quality-standards.md)
- [Technical Standards](methodology/technical-standards.md)

---

## Export

To generate a client-ready Word or PDF document from any template or runbook:

```bash
./playbook/export.sh templates/sow.md "Acme Defense LLC"
```

Output lands in `engagements/{client-slug}/`.

---

## AIOS Skill

Run `/engagement-start` to scaffold a new client engagement from scratch. Prompts for service type and client name, then generates the full document package.
