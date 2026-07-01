---
title: Technical Report
template_type: technical-report
updated: 2026-06-30
---

# {{SERVICE_NAME}} — Technical Report

**Client:** {{CLIENT_NAME}}
**Assessment Period:** {{START_DATE}} – {{END_DATE}}
**Report Date:** {{REPORT_DATE}}
**Prepared By:** {{CONSULTANT_NAME}}, Vulnaguard
**Version:** {{VERSION}}
**Classification:** Confidential — For {{CLIENT_NAME}} Internal Use Only

---

## Table of Contents

1. Executive Summary
2. Scope and Methodology
3. Findings Summary
4. Findings — Critical
5. Findings — High
6. Findings — Medium
7. Findings — Low
8. Findings — Informational
9. Appendix A: Scope Detail
10. Appendix B: Tools and Versions Used
11. Appendix C: Evidence Index

---

## 1. Executive Summary

*[Insert or reference the separate Executive Summary document here.]*

---

## 2. Scope and Methodology

### 2.1 Scope

{{SCOPE_DESCRIPTION}}

**In Scope:**
- {{IN_SCOPE_ITEM_1}}
- {{IN_SCOPE_ITEM_2}}

**Out of Scope:**
- {{OUT_OF_SCOPE_ITEM_1}}
- {{OUT_OF_SCOPE_ITEM_2}}

### 2.2 Methodology

{{BRIEF_METHODOLOGY_DESCRIPTION}}

Vulnaguard conducted this assessment in accordance with {{APPLICABLE_FRAMEWORK}} and the Vulnaguard Technical Standards. All findings were manually validated prior to inclusion in this report.

### 2.3 Limitations

{{ANY_LIMITATIONS — e.g., "Assessment was limited to external-facing systems only. No internal network access was provided."}}

*If no limitations: "No material limitations were identified. Assessment was conducted as scoped."*

---

## 3. Findings Summary

| Severity | Count | % of Total |
|---|---|---|
| Critical | {{N}} | {{%}} |
| High | {{N}} | {{%}} |
| Medium | {{N}} | {{%}} |
| Low | {{N}} | {{%}} |
| Informational | {{N}} | {{%}} |
| **Total** | **{{N}}** | |

{{1–2 sentences on overall findings theme.}}

---

## 4. Critical Findings

---

### FINDING-001: {{FINDING_TITLE}}

| | |
|---|---|
| **Severity** | Critical |
| **Affected Asset / Control** | {{ASSET_OR_CONTROL}} |
| **Framework Reference** | {{e.g., NIST 800-171 AC.1.001 / CVE-XXXX-XXXX / CIS Control 5}} |
| **Date Identified** | {{DATE}} |
| **Validated By** | {{CONSULTANT_NAME}} |

**Description**

{{DETAILED DESCRIPTION OF THE FINDING. What was found, where, and why it is a risk. Be specific. Include system names, configurations, or control gaps. This section is for technical readers.}}

**Evidence**

{{DESCRIPTION OF EVIDENCE. Reference the evidence by filename or exhibit number. Example: "Nessus scan output dated 2026-07-01 (Exhibit A-001) confirmed the presence of CVE-XXXX-XXXX on host 10.0.1.25."}}

**Business Impact**

{{WHAT COULD HAPPEN IF THIS FINDING IS EXPLOITED OR REMAINS UNADDRESSED. Tie to business risk: data loss, downtime, regulatory penalty, loss of contract.}}

**Recommendation**

{{SPECIFIC, ACTIONABLE REMEDIATION GUIDANCE. Include the specific configuration change, tool, policy, or process needed. Where relevant, cite vendor documentation.}}

**Effort:** {{Quick Win / Short-Term / Long-Term}}

---

*(Repeat for each Critical finding. Use the same structure for High, Medium, Low, and Informational findings, adjusting the severity field.)*

---

## 5. High Findings

*(Same structure as Critical)*

---

## 6. Medium Findings

*(Same structure — findings include description, evidence, impact, recommendation.)*

---

## 7. Low Findings

*(Same structure — may be abbreviated for efficiency.)*

---

## 8. Informational

*(Brief descriptions — no evidence citations required unless notable.)*

---

## Appendix A: Scope Detail

Full list of in-scope IPs, systems, applications, or NIST 800-171 controls.

---

## Appendix B: Tools and Versions Used

| Tool | Version | Purpose |
|---|---|---|
| {{TOOL_1}} | {{VERSION}} | {{PURPOSE}} |
| {{TOOL_2}} | {{VERSION}} | {{PURPOSE}} |

---

## Appendix C: Evidence Index

| Exhibit | File Name | Description | Finding Reference |
|---|---|---|---|
| A-001 | {{FILENAME}} | {{DESCRIPTION}} | FINDING-001 |
| A-002 | {{FILENAME}} | {{DESCRIPTION}} | FINDING-002 |

---

*This report is confidential and intended solely for {{CLIENT_NAME}}. Unauthorized disclosure is prohibited. Vulnaguard is not responsible for actions taken based on this report by parties other than {{CLIENT_NAME}}.*

**Vulnaguard LLC | vulnaguard.com | seanmurrill@vulnaguard.com | CAGE: 21QQ7 | UEI: CJ7ZXTUSN3W8**
