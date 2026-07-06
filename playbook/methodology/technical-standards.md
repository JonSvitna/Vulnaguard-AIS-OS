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

## Solo Starter Stack (buy-first sequence)

The Approved Tooling table lists every sanctioned tool. As a one-person shop, do not buy all of it. Acquire in this order:

1. **Nessus Professional** — the anchor. Standardize on it. DoD's mandated ACAS solution is built on Tenable, so the Nessus name carries credibility with COs and defense contractors. Single seat, unlimited IPs, installs on the scanning host, no server infra. ~$4k/year.
   - **Licensing trap:** Nessus *Essentials* (free) is capped at 16 IPs and its license **prohibits commercial/consulting use**. Never run paid client work on Essentials.
   - **Pre-revenue bridge only:** if the first Nessus license must wait for the first invoice, run **OpenVAS / Greenbone Community** for network scanning in the interim. Free, but more setup/maintenance and less name recognition on a report. Switch to Nessus as soon as revenue allows.
2. **OWASP ZAP + Nmap** — free, keep. ZAP covers the web-application layer only (DAST); it is never the primary scanner for a network/host assessment. Nmap handles enumeration.
3. **Metasploit Framework (Community)** — free, only for authorized exploitation validation per the ROE.
4. **Burp Suite Professional** — add later, only when web-app engagement volume justifies the spend.

Tool brand is table stakes. What makes the deliverable credible is manual validation of every Critical/High finding and mapping findings to NIST 800-171 / 800-53 controls, not the scanner logo.

---

## Scanning Host / OS

Run scans from a dedicated, controlled host, never from a daily-driver machine.

- **Base OS:** **Kali Linux** in a snapshottable VM (VirtualBox / VMware / Proxmox). Kali ships Nmap, Metasploit, and the enumeration toolset, and the name is recognized. Install Nessus Professional from Tenable's Debian package on top. A minimal hardened Ubuntu LTS is an acceptable alternative if Kali's extra tooling isn't wanted.
- **One clean snapshot per engagement.** Snapshot before testing begins and preserve it for evidence integrity and reproducibility. Do not reuse a host across clients without a clean snapshot.
- **External scans need a known source IP.** Stand up a dedicated cloud instance (e.g. a DigitalOcean droplet) with a stable static IP, list that IP in the signed Rules of Engagement, and have the client whitelist it. This keeps attribution clean and satisfies the ROE authorized-source requirement.
- **Internal/credentialed scans** run from a VM placed on the client network or reached over the provisioned VPN (see the VA pre-assessment checklist).
- Client scan data and evidence stay in the engagement folder only, per Data Handling below. Wipe or destroy the engagement snapshot per the retention and destruction rules after closeout.

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
