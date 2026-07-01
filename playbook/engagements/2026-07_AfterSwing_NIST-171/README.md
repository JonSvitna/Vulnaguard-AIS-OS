# AfterSwing — NIST SP 800-171 Gap Assessment

**Engagement ID:** 2026-07_AfterSwing_NIST-171
**Service:** NIST SP 800-171 Gap Assessment
**Client Contact:** Don Weston — seanmurrill@gmail.com
**Vulnaguard Lead:** Sean Murrill — seanmurrill@vulnaguard.com
**Period:** 2026-07-01 – 2026-11-01

---

## Folder Structure

```
2026-07_AfterSwing_NIST-171/
  00-onboarding/
    onboarding-checklist.md         ← Track NDA/MSA/SOW signatures + deposit
    welcome-letter.md               ← Send to Don Weston at engagement start
  01-discovery/
    discovery-questionnaire.md     ← Send to Don Weston, due 2026-07-08
  02-planning/
    kickoff-agenda.md              ← Send 48hr before kickoff
    status-report-template.md     ← Copy and fill weekly
  03-assessment/
    evidence-checklist.md         ← Track all evidence collection here
    evidence/                     ← All client evidence files go here
  04-analysis/                    ← Findings notes, peer review docs
  05-reports/
    drafts/
      sow.md                      ← Get signed before work begins
      technical-report.md         ← Fill as findings are validated
      executive-summary.md        ← Fill after analysis phase
      poa-m.md                    ← Fill from findings list
    final/                        ← Final signed/approved versions
  06-closeout/
    closeout-report.md
    acceptance-form.md
```

---

## Next Steps

- [ ] Send discovery questionnaire to Don Weston — due 2026-07-08
- [ ] Send SOW for signature — target by 2026-07-01
- [ ] Schedule kickoff meeting
- [ ] Confirm access requirements and stakeholder interview schedule
- [ ] Verify pandoc installed (`brew install pandoc`) then run exports:
  ```bash
  ./playbook/export.sh playbook/engagements/2026-07_AfterSwing_NIST-171/05-reports/drafts/sow.md "AfterSwing"
  ```

---

## Key Dates

| Milestone | Date |
|---|---|
| Engagement start | 2026-07-01 |
| Discovery questionnaire due | 2026-07-08 |
| Final deliverables | 2026-11-01 |
| Engagement end | 2026-11-01 |

---

## Notes

*Client contact: Don Weston — seanmurrill@gmail.com*
