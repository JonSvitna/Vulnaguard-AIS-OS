---
title: Evidence Checklist
template_type: evidence-checklist
updated: 2026-06-30
---

# Evidence Collection Checklist

**Client:** {{CLIENT_NAME}}
**Engagement:** {{SERVICE_NAME}}
**Lead Consultant:** {{CONSULTANT_NAME}}

---

*Use this checklist to track evidence collection. Mark each item Received, Pending, or N/A. For N/A items, document the reason in the Notes column.*

---

## Universal — All Engagements

| # | Item | Status | Received Date | Location | Notes |
|---|---|---|---|---|---|
| 1 | Asset inventory (all systems, servers, endpoints, cloud) | | | | |
| 2 | Network diagram | | | | |
| 3 | Org chart (IT and security roles) | | | | |
| 4 | Existing security policies | | | | |
| 5 | Previous assessment reports (last 3 years) | | | | |
| 6 | Stakeholder contact list | | | | |

---

## Vulnerability Assessment

| # | Item | Status | Received Date | Location | Notes |
|---|---|---|---|---|---|
| 7 | Signed Rules of Engagement | | | | |
| 8 | Authorized IP address / URL list | | | | |
| 9 | VPN credentials (internal assessments) | | | | |
| 10 | Web app test account credentials (web assessments) | | | | |
| 11 | IP whitelist confirmation (if needed for scanning) | | | | |

---

## CMMC L2 / NIST 800-171

| # | Item | Status | Received Date | Location | Notes |
|---|---|---|---|---|---|
| 12 | System Security Plan (SSP) | | | | |
| 13 | CUI scope / system boundary definition | | | | |
| 14 | User access list (privileged and standard) | | | | |
| 15 | MFA configuration evidence | | | | |
| 16 | Patch management records / vulnerability scan reports | | | | |
| 17 | Incident response plan | | | | |
| 18 | Audit log configuration evidence | | | | |
| 19 | Backup and recovery documentation / test records | | | | |
| 20 | Security awareness training records | | | | |
| 21 | Vendor / third-party access list | | | | |
| 22 | Configuration management baseline documentation | | | | |
| 23 | Physical access controls documentation | | | | |
| 24 | Media protection policy and procedures | | | | |
| 25 | Personnel security records (background check policy) | | | | |
| 26 | Previous SPRS score submission (if applicable) | | | | |

---

## Security Program Assessment

| # | Item | Status | Received Date | Location | Notes |
|---|---|---|---|---|---|
| 27 | All security policies and procedures | | | | |
| 28 | Risk register (if exists) | | | | |
| 29 | Cyber insurance policy | | | | |
| 30 | Incident history (last 24 months) | | | | |
| 31 | Security awareness training records | | | | |
| 32 | Vulnerability scan results (most recent) | | | | |
| 33 | Third-party / vendor contracts with security clauses | | | | |

---

## Policy Development

| # | Item | Status | Received Date | Location | Notes |
|---|---|---|---|---|---|
| 34 | All existing policies (security and HR) | | | | |
| 35 | Regulatory requirements list | | | | |
| 36 | Policy approval authority (who signs policies) | | | | |
| 37 | Prior gap assessment identifying policy needs | | | | |

---

## Evidence Naming Convention

`{ControlID_or_FindingID}_{ShortDescription}_{YYYY-MM-DD}.{ext}`

Examples:
- `AC.1.001_UserAccessList_2026-07-01.xlsx`
- `FINDING-007_PatchScanResults_2026-07-01.pdf`

---

## Evidence Storage

Store all evidence in: `engagements/{{ENGAGEMENT_FOLDER}}/03-assessment/evidence/`

Do not store evidence on personal devices or unsecured cloud storage.
