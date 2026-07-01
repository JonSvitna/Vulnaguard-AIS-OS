---
title: Rules of Engagement Template
version: 1.0
updated: 2026-07-01
---

# Rules of Engagement
**Engagement:** {{Service Name}} — {{Client Organization Name}}
**Document Date:** {{Date}}
**Effective During:** {{Start Date}} through {{End Date}}
**Prepared by:** Vulnaguard LLC
**Client Authorized Signatory:** {{Name, Title}}

---

## Purpose

This document defines the boundaries, authorizations, and procedures governing Vulnaguard's technical assessment activities for {{Client Organization Name}}. Both parties must sign this document before any active technical testing begins.

---

## Authorized Scope

### In-Scope Systems

| System / Asset | IP Address / Hostname | Environment |
|---|---|---|
| {{System Name}} | {{IP or hostname}} | {{Production / Staging / Dev}} |
| | | |
| | | |

### In-Scope Networks / Ranges

- {{CIDR range or description}}

### Out-of-Scope Systems (Do Not Test)

- {{System 1 — reason}}
- {{System 2 — reason}}

---

## Authorized Activities

The following activities are authorized within the defined scope:

- [ ] Passive reconnaissance (OSINT, DNS enumeration)
- [ ] Network scanning (port scans, service detection)
- [ ] Vulnerability scanning (authenticated / unauthenticated)
- [ ] Manual testing and exploitation (per scope above)
- [ ] Social engineering / phishing simulation
- [ ] Physical security testing
- [ ] Web application testing
- [ ] API testing

**Note:** Any activity not explicitly listed above requires written authorization before execution.

---

## Testing Window

| Parameter | Value |
|---|---|
| Testing hours | {{e.g., M–F, 9am–5pm ET / or 24/7}} |
| Blackout dates | {{Dates when no testing should occur}} |
| Emergency stop contact | {{Name + Phone — reached immediately if issue arises}} |

---

## Points of Contact

### Client Side

| Role | Name | Phone | Email |
|---|---|---|---|
| Authorization Contact | {{Name}} | {{Phone}} | {{Email}} |
| Technical Contact | {{Name}} | {{Phone}} | {{Email}} |
| Emergency Contact | {{Name}} | {{Phone}} | {{Email}} |

### Vulnaguard Side

| Role | Name | Phone | Email |
|---|---|---|---|
| Lead Consultant | Sean Murrill | {{Phone}} | seanmurrill@vulnaguard.com |

---

## Emergency Stop Procedure

If at any point either party determines that testing must be halted immediately:

1. Vulnaguard lead contacts the client emergency contact by **phone** (not email)
2. All active testing activities are suspended within 5 minutes of the call
3. Vulnaguard documents the stop time, reason, and any in-progress activities
4. No testing resumes until both parties confirm in writing

---

## Data Handling

- All data collected during testing (scan results, credentials, sensitive information) is treated as client confidential per the executed NDA
- Data is stored only on Vulnaguard systems in encrypted form
- Data is destroyed within 30 days of final report delivery unless the client requests extended retention in writing
- No client data is shared with third parties

---

## Liability

Testing is performed under the terms of the Master Services Agreement executed on {{MSA Date}}. Vulnaguard's liability for any unintended impact is governed by the limitation of liability clause in that agreement. Client acknowledges that penetration testing and vulnerability scanning carry inherent risk and has authorized these activities on the systems listed above.

---

## Authorization

By signing below, the authorized representatives of both parties confirm that:
- The scope defined above is accurate and complete
- The listed systems and activities are authorized for testing
- Both parties have read and agree to the procedures in this document

**Client Authorization**

Signed: _____________________________ Date: _______________
Name: {{Name}}
Title: {{Title}}
Organization: {{Client Organization Name}}

**Vulnaguard Authorization**

Signed: _____________________________ Date: _______________
Name: Sean Murrill
Title: Founder
Organization: Vulnaguard LLC
