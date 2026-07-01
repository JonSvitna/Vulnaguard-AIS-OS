---
title: Phase 9 — Sentinel Onboarding (Optional)
phase: 9
updated: 2026-06-30
---

# Phase 9: Sentinel Onboarding

**Objective:** Onboard the client to Sentinel CMMC for ongoing compliance tracking and evidence management.

**This phase is optional. It runs either as a standalone engagement or as an add-on to a completed compliance assessment.**

---

## Entry Criteria

- Client has signed Sentinel subscription agreement
- Admin contact identified on client side
- Assessment artifacts available (findings, POA&M, evidence) if onboarding post-assessment

---

## Activities

### 9.1 Tenant Provisioning
- Create client tenant in Sentinel
- Configure organization name, branding (if applicable), and subscription tier

### 9.2 Environment Configuration
- Configure applicable framework (CMMC L2, NIST 800-171, etc.)
- Import in-scope systems and asset inventory
- Define CUI scope and system boundaries

### 9.3 User Provisioning
- Create admin account for client's primary contact
- Create additional user accounts per client's roster
- Configure role-based access (admin, contributor, read-only)
- Send welcome emails with login credentials

### 9.4 Import Assessment Artifacts
- Import findings from the prior engagement (if applicable)
- Import POA&M items into Sentinel's task/tracking module
- Upload evidence files to the evidence repository

### 9.5 Dashboard Configuration
- Configure the compliance dashboard to reflect current control status
- Set up POA&M tracking view with open items and milestones
- Configure executive dashboard view for client leadership

### 9.6 Evidence Repository Setup
- Create folder structure aligned with NIST 800-171 practice families
- Set naming conventions and upload guidance for client's team

### 9.7 Reporting Configuration
- Configure automated report templates (executive summary, compliance scorecard)
- Set reporting frequency and recipients

### 9.8 Training
- Conduct a 60-minute walkthrough session with the client's team
- Cover: dashboard navigation, evidence uploads, POA&M updates, report generation
- Provide a quick reference guide

### 9.9 Go-Live Checklist
- [ ] Tenant active and accessible
- [ ] All users provisioned and logged in successfully
- [ ] Framework and scope configured
- [ ] POA&M items imported
- [ ] Evidence repository populated with existing artifacts
- [ ] Client team trained and questions addressed
- [ ] First report generated and reviewed with client

---

## Outputs

- Active Sentinel tenant configured for client
- Trained client team
- Populated POA&M and evidence repository

---

## Deliverables to Client

- Sentinel tenant access (credentials)
- Quick reference guide
- First compliance status report

---

## Quality Gate

- [ ] Go-live checklist fully checked off
- [ ] Client's admin user can independently log in, upload evidence, and generate a report
- [ ] No data from other clients visible in client's tenant

---

## Common Issues

**Client loses credentials:** Admin password reset via Sentinel admin console. Document the reset.

**Client imports wrong evidence:** Review and reclassify during the first check-in. Use this as a training opportunity, not a blame moment.

**Client expects Sentinel to do the compliance work for them:** Reset expectations. Sentinel is a management and tracking tool — it organizes the work, it doesn't do the work. Their team still owns evidence collection and POA&M execution.
