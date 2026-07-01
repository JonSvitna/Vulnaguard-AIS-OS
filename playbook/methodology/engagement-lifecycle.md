---
title: Standard Engagement Lifecycle
version: 1.0
updated: 2026-06-30
---

# Standard Engagement Lifecycle

Every Vulnaguard engagement follows this 9-phase structure. Not every phase applies to every service — the service runbook specifies which phases are active and how long each runs.

---

## Phase 1: Discovery

**Objective:** Understand the client's environment, business context, and engagement scope before any technical work begins.

**Inputs:**
- Signed SOW and MSA
- Initial client intake call notes
- Preliminary scope information from sales

**Activities:**
- Send and collect discovery questionnaire
- Conduct discovery call with primary stakeholders
- Collect initial documentation (asset inventory, network diagram, org chart)
- Define CUI scope (for CMMC engagements)
- Identify key contacts and interview targets

**Outputs:**
- Completed discovery questionnaire
- Documented scope boundary
- Stakeholder contact list
- Initial asset inventory

**Deliverables to Client:** None (internal phase)

**Quality Gate:** Scope is agreed upon in writing before Phase 2 begins. No ambiguity on what is in/out of scope.

**Responsible Role:** Lead Consultant

---

## Phase 2: Planning

**Objective:** Translate discovery findings into a structured project plan with defined timelines, responsibilities, and rules of engagement.

**Inputs:**
- Completed discovery outputs
- SOW scope definition
- Client availability and scheduling constraints

**Activities:**
- Finalize rules of engagement (for technical assessments)
- Build project schedule with milestones
- Prepare kickoff agenda
- Identify tools and access requirements
- Schedule stakeholder interviews
- Confirm evidence collection requirements

**Outputs:**
- Signed rules of engagement (technical assessments only)
- Project schedule
- Kickoff agenda

**Deliverables to Client:** Kickoff agenda (sent 48 hours in advance)

**Quality Gate:** Client has reviewed and signed rules of engagement. Kickoff meeting confirmed on calendar.

**Responsible Role:** Lead Consultant + Project Manager

---

## Phase 3: Assessment

**Objective:** Execute the technical or documentary assessment according to the service runbook.

**Inputs:**
- Signed rules of engagement
- Access credentials / documentation package
- Project schedule

**Activities:** Vary by service — see individual service runbooks.

**General Activities:**
- Conduct scheduled stakeholder interviews
- Collect and catalog evidence
- Run technical scans or conduct control reviews
- Document findings in real time
- Flag critical findings immediately to client

**Outputs:**
- Raw scan data / interview notes / evidence library
- Preliminary findings list

**Deliverables to Client:** Weekly status report

**Quality Gate:** All planned assessment activities completed. Evidence catalog is complete. No open access issues.

**Responsible Role:** Lead Consultant (+ Technical Analyst for VA engagements)

---

## Phase 4: Analysis

**Objective:** Turn raw findings into validated, risk-ranked outputs ready for reporting.

**Inputs:**
- Raw findings from Phase 3
- Risk rating model
- Client context from discovery

**Activities:**
- Validate and triage findings (eliminate false positives)
- Apply risk rating model to each finding
- Map findings to applicable framework controls
- Identify root causes and remediation paths
- Draft executive-level summary of findings
- Peer review all findings

**Outputs:**
- Validated findings list with risk ratings
- Control mapping (where applicable)
- Remediation recommendations
- Draft executive summary

**Deliverables to Client:** None (internal phase)

**Quality Gate:** All critical and high findings peer-reviewed. No unvalidated items in the findings list.

**Responsible Role:** Lead Consultant + Peer Reviewer

---

## Phase 5: Reporting

**Objective:** Produce and deliver all engagement deliverables.

**Inputs:**
- Validated findings from Phase 4
- Client context and branding requirements
- Applicable report templates

**Activities:**
- Draft technical report
- Draft executive summary / executive presentation
- Draft POA&M (where applicable)
- Draft risk register (where applicable)
- Internal QA review of all documents
- Client review call — walk through findings
- Incorporate client feedback
- Issue final report package

**Outputs:**
- Final technical report
- Executive summary
- POA&M (if applicable)
- Risk register (if applicable)

**Deliverables to Client:** Full report package (Word/PDF)

**Quality Gate:** QA review sign-off before client delivery. Client has acknowledged receipt of final report.

**Responsible Role:** Lead Consultant + QA Reviewer

---

## Phase 6: Remediation (Advisory)

**Objective:** Support the client in addressing identified findings. Scope varies by SOW.

**Inputs:**
- Final report and POA&M
- Client's internal remediation timeline

**Activities:**
- Remediation guidance calls (per SOW)
- Answer technical questions on specific findings
- Review client-submitted evidence of remediation
- Update POA&M status as items close

**Outputs:**
- Updated POA&M
- Remediation guidance notes

**Deliverables to Client:** Updated POA&M

**Quality Gate:** Client has a documented remediation plan for all critical and high findings before Vulnaguard closes advisory support.

**Responsible Role:** Lead Consultant

---

## Phase 7: Validation

**Objective:** Confirm that remediated items have been resolved. Scope varies by SOW.

**Inputs:**
- Client's evidence of remediation
- Original findings list
- Updated POA&M

**Activities:**
- Re-test remediated findings (technical assessments)
- Review updated documentation / policies (compliance assessments)
- Update findings status (open / closed / accepted risk)
- Issue validation memo

**Outputs:**
- Validation memo
- Final POA&M with updated statuses

**Deliverables to Client:** Validation memo + final POA&M

**Quality Gate:** All critical findings verified closed or formally accepted as risk by client.

**Responsible Role:** Lead Consultant

---

## Phase 8: Closeout

**Objective:** Formally close the engagement and capture lessons learned.

**Inputs:**
- Final deliverables
- Client acceptance form

**Activities:**
- Send closeout report
- Collect signed client acceptance form
- Issue final invoice
- Internal lessons learned debrief
- Archive engagement artifacts
- Offer Sentinel onboarding (if not already sold)

**Outputs:**
- Signed client acceptance form
- Closeout report
- Archived engagement folder

**Deliverables to Client:** Closeout report + acceptance form

**Quality Gate:** Signed acceptance form received. All deliverables transmitted. Invoice issued.

**Responsible Role:** Lead Consultant + Account Manager

---

## Phase 9: Sentinel Onboarding (Optional)

**Objective:** Onboard the client to Sentinel CMMC for ongoing compliance tracking.

**Inputs:**
- Completed engagement artifacts (findings, POA&M, risk register)
- Client's IT environment details

**Activities:**
- See [services/sentinel-implementation.md](../services/sentinel-implementation.md)

**Responsible Role:** Sentinel Implementation Specialist
