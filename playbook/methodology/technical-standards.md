---
title: Technical Standards
version: 1.0
updated: 2026-06-30
---

# Technical Standards

---

## Assessment Methodology

Vulnaguard assessments follow a structured, evidence-based methodology grounded in recognized frameworks. We do not use purely automated tooling — every engagement includes analyst validation and human judgment.

### For Technical Assessments (Vulnerability Assessment)
1. Asset enumeration and scope confirmation
2. External reconnaissance (passive, then active)
3. Vulnerability scanning with validated tooling
4. Manual validation of scanner output
5. Exploitation testing (if authorized in rules of engagement)
6. Evidence documentation
7. Risk analysis and rating

### For Compliance Assessments (CMMC / NIST 800-171 / SPA)
1. Documentation collection and review
2. Stakeholder interviews
3. Technical environment observation (where accessible)
4. Control-by-control assessment
5. Evidence mapping
6. Gap identification and risk rating
7. Roadmap / POA&M development

---

## Frameworks Reference

| Framework | Application |
|---|---|
| NIST SP 800-171 Rev 3 | CMMC L2 baseline; standalone gap assessments |
| CMMC Level 2 | DoD contractor readiness assessments |
| NIST SP 800-53 Rev 5 | Federal agency work; SPA benchmark |
| CIS Controls v8 | Vulnerability assessments; security program baselines |
| NIST Cybersecurity Framework (CSF) 2.0 | Executive risk assessments; security maturity |
| ISO/IEC 27001:2022 | International compliance work |
| SOC 2 Type II | Cloud/SaaS service provider assessments |
| OWASP Top 10 | Web application assessments |

---

## Approved Tooling

### Vulnerability Assessment
| Tool | Purpose | License |
|---|---|---|
| Nessus Professional / Tenable.io | Primary vulnerability scanner | Commercial |
| Rapid7 InsightVM | Alternate scanner | Commercial |
| OpenVAS / Greenbone | Open source scanner (backup) | Open Source |
| Nmap | Port/service enumeration | Open Source |
| Metasploit Framework | Exploitation validation (authorized engagements only) | Community/Commercial |
| Burp Suite Professional | Web application testing | Commercial |
| OWASP ZAP | Web application testing (backup) | Open Source |

### Compliance / Documentation
| Tool | Purpose |
|---|---|
| Sentinel CMMC | Evidence management, POA&M tracking, reporting |
| Microsoft 365 | Client communication, document collaboration |
| Obsidian | Internal knowledge management |

### Reporting
| Tool | Purpose |
|---|---|
| Pandoc | Markdown → Word/PDF export |
| Microsoft Word | Report formatting and client delivery |

---

## Vulnerability Scoring

All CVEs are scored using CVSS v3.1 base scores as a starting point. Vulnaguard applies environmental and temporal adjustments per the risk rating model.

CVSS scores alone do not determine final severity. A CVSS 9.8 on an isolated, air-gapped system may be rated Medium after environmental adjustment. Always apply judgment.

---

## Rules of Engagement Requirements

Technical assessments require a signed Rules of Engagement document before scanning begins. The ROE must specify:

- Authorized target IP ranges and hostnames
- Authorized testing window (dates and times)
- Out-of-scope systems
- Emergency contact and escalation procedure
- Authorization signatures from client's authorized representative
- Explicit statement of authorization for scanning/testing activities

No technical testing begins without a signed ROE on file.

---

## Data Handling

- All client data is handled as confidential
- Scan data and evidence files are stored in the engagement folder only
- No client data stored on personal devices
- Engagement artifacts are retained for 3 years post-closeout
- Destruction of data on request must be documented
