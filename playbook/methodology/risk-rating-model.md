---
title: Risk Rating Model
version: 1.0
updated: 2026-06-30
---

# Risk Rating Model

Vulnaguard uses a consistent risk rating model across all engagements. Every finding is assigned a severity level using this model. This ensures clients understand relative risk and can prioritize remediation correctly.

---

## Severity Levels

### Critical

**Definition:** A finding that poses an immediate, severe threat to the confidentiality, integrity, or availability of the organization's systems or data. Exploitation is likely with low effort, or evidence of active exploitation exists.

**Remediation SLA:** 24–72 hours (notify client immediately upon discovery)

**Examples:**
- Unauthenticated remote code execution on an internet-facing system
- Exposed credentials providing privileged access to production systems
- Active malware or indicators of compromise
- Complete absence of any access controls on CUI systems

---

### High

**Definition:** A finding that significantly increases risk to the organization. Exploitation is plausible without advanced skill, or the control gap directly violates a required framework control with no compensating control.

**Remediation SLA:** 30 days

**Examples:**
- Missing MFA on privileged accounts
- Unpatched critical CVEs (CVSS 9.0+) on internal systems
- No data backup or recovery capability
- Absence of incident response plan with staff who have never trained

---

### Medium

**Definition:** A finding that represents meaningful risk but requires additional conditions, effort, or access to exploit. Or a framework control gap that has a partial compensating control in place.

**Remediation SLA:** 90 days

**Examples:**
- Unpatched high CVEs (CVSS 7.0–8.9) on internal systems
- Missing vulnerability management program
- Incomplete or outdated security policy documentation
- Absence of audit logging on non-critical systems

---

### Low

**Definition:** A finding that represents minimal risk on its own but could contribute to a larger attack chain, or a control gap that is informational with negligible near-term impact.

**Remediation SLA:** 180 days

**Examples:**
- Informational CVEs with no known exploit path
- Minor policy documentation gaps
- Outdated but non-critical software versions
- Missing security awareness training attestation records

---

### Informational

**Definition:** An observation that does not represent a direct risk but is noted as a best practice recommendation or for client awareness.

**Remediation SLA:** At client's discretion

**Examples:**
- Suggested hardening configurations
- Process improvement recommendations
- Industry benchmark comparisons

---

## Risk Calculation

For technical assessments, risk is calculated using the standard formula:

**Risk = Likelihood × Impact**

| Likelihood | Score |
|---|---|
| Certain (actively exploited or trivial to exploit) | 3 |
| Likely (known exploit path, moderate skill required) | 2 |
| Possible (theoretical or requires rare conditions) | 1 |

| Impact | Score |
|---|---|
| Critical (data exfiltration, full system compromise, operational disruption) | 3 |
| Significant (privilege escalation, partial data exposure, service degradation) | 2 |
| Minor (low data sensitivity, isolated system, limited blast radius) | 1 |

| Score | Severity |
|---|---|
| 9 | Critical |
| 6–8 | High |
| 3–5 | Medium |
| 1–2 | Low |

For compliance assessments (CMMC, NIST 800-171), severity is driven primarily by control criticality, presence of compensating controls, and CUI exposure risk.

---

## Adjustments

**Upgrade triggers:**
- Finding is on an internet-facing system
- Finding involves CUI or sensitive data
- Client has no compensating controls

**Downgrade triggers:**
- Strong compensating control reduces exploitability
- Finding is on an isolated, non-production system
- No sensitive data in scope

All adjustments must be documented with rationale in the findings notes.

---

## False Positive Process

1. Analyst flags suspected false positive during analysis
2. Lead consultant independently validates
3. If confirmed false positive: remove from findings list, note in QA log
4. If uncertain: retain as finding at lowest plausible severity, note caveat

Never remove a finding from the report without independent validation.
