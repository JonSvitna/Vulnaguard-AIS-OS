---
title: Sentinel Implementation
service_code: SENTINEL
phases: [discovery, planning, assessment, reporting, closeout]
typical_duration: 1–2 weeks
updated: 2026-06-30
---

# Sentinel Implementation Runbook

**Service Code:** SENTINEL
**Typical Duration:** 1–2 weeks
**Phases:** Discovery → Planning → Implementation → Training → Closeout

---

## Service Description

Sentinel CMMC is Vulnaguard's compliance management platform. A Sentinel Implementation engagement configures and launches a client's Sentinel tenant so they can actively manage their CMMC/NIST 800-171 compliance posture on an ongoing basis.

This service is most commonly sold as an add-on to a CMMC L2 Readiness or NIST 800-171 Gap Assessment, where the engagement artifacts (findings, POA&M, evidence) are imported directly into Sentinel.

---

## Pre-Implementation Checklist

- [ ] Sentinel subscription agreement signed
- [ ] Subscription tier confirmed (determines features and user limit)
- [ ] Client's primary admin contact identified
- [ ] Applicable compliance framework confirmed (CMMC L2, NIST 800-171, other)
- [ ] Prior assessment artifacts available for import (findings, POA&M, evidence files)

---

## Implementation Checklist

### Tenant Provisioning
- [ ] Create client organization in Sentinel admin console
- [ ] Set organization name, primary contact, subscription tier
- [ ] Confirm tenant is isolated — no data from other organizations visible

### Framework Configuration
- [ ] Select applicable framework (CMMC L2 / NIST 800-171 / other)
- [ ] Define system boundary and CUI scope in Sentinel
- [ ] Import in-scope asset inventory

### User Provisioning
- [ ] Create admin account for client's primary contact
- [ ] Create accounts for all additional users per client roster
- [ ] Assign roles: Admin / Contributor / Read-Only
- [ ] Send welcome emails with login credentials and first-login instructions

### Evidence Repository Setup
- [ ] Create folder structure aligned to the framework's practice families
- [ ] Upload existing evidence files from the prior assessment (if applicable)
- [ ] Provide upload guide to client team

### POA&M Import
- [ ] Import all open POA&M items from the prior assessment
- [ ] Assign owners to each item (where client has identified owners)
- [ ] Set milestone dates
- [ ] Confirm POA&M view is accessible to relevant users

### Dashboard Configuration
- [ ] Compliance dashboard configured and reflecting current control status
- [ ] POA&M tracking view configured with open items sorted by priority
- [ ] Executive dashboard configured for leadership view (high-level only)

### Reporting Configuration
- [ ] Configure automated report templates (compliance scorecard, executive summary)
- [ ] Set report delivery schedule and recipients (if using scheduled reports)

---

## Training Session Agenda (60 minutes)

1. Platform overview and navigation (10 min)
2. How to upload and classify evidence (15 min)
3. POA&M management — updating items, attaching evidence, marking closed (15 min)
4. Generating reports (10 min)
5. Q&A (10 min)

Provide a quick reference card (1-page PDF) summarizing the key workflows.

---

## Go-Live Checklist

- [ ] All users can log in successfully
- [ ] At least one evidence file successfully uploaded by the client
- [ ] POA&M populated and at least one item updated by the client
- [ ] First compliance status report generated and reviewed
- [ ] Client admin can add a new user independently
- [ ] Client knows the support contact for Sentinel issues

---

## Deliverables

| Deliverable | Format | Timing |
|---|---|---|
| Configured Sentinel Tenant | Live platform | End of implementation |
| Quick Reference Card | PDF | Training session |
| First Compliance Status Report | PDF | Go-live |
| Closeout Report | Word + PDF | Closeout |

---

## Ongoing Support

After go-live, clients can:

- Submit support requests via [support contact — TBD]
- Request a follow-on check-in at 30 days (optional, can be quoted separately)
- Upgrade their subscription tier for additional features

---

## Sentinel Roadmap Integration

Every manual process in this runbook maps to a future Sentinel automation. As the platform matures, tag implementation tasks that could be partially or fully automated. These feed the Sentinel product roadmap.

Examples:
- User provisioning → self-service onboarding
- POA&M import → automated import from assessment templates
- Evidence upload → email-to-evidence inbox
- Status reporting → scheduled automated delivery

---

## Templates Used

- [Closeout Report](../templates/closeout-report.md)
- [Client Acceptance Form](../templates/acceptance-form.md)
