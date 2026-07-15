---
name: engagement-start
description: Scaffold a new Vulnaguard client engagement. Creates the engagement folder structure, populates all relevant templates with client details, and exports Word documents ready for delivery. Trigger on "new engagement", "start engagement", "new client", "spin up engagement", or /engagement-start.
---

## What this skill does

Collects a service type and client details, then in one shot:
1. Creates `playbook/engagements/{YYYY-MM}_{ClientSlug}_{ServiceCode}/` with the standard subfolder structure
2. Populates all relevant templates with client info (replacing `{{PLACEHOLDER}}` tokens)
3. Exports Word (.docx) files for every client-facing document via `playbook/export.sh`
4. Logs the new engagement to `decisions/log.md`

## Execution

### Step 1: Collect inputs (conversational)

Ask these in sequence. Keep it fast — two turns max.

**Turn 1:**
> "What's the client name and which service are we kicking off?"

If they give both in one message, skip Turn 2.

**Turn 2 (if needed):**
> "Got it. A few quick details:
> - Primary contact name and email?
> - Engagement start date and estimated end date?
> - Consultant name for the docs? (or just confirm it's Sean)"

If any detail is missing, use a sensible placeholder and note it at the end. Don't block on optional fields.

---

### Step 2: Resolve service code

Map what the user says to a service code:

| What they say | Service Code | Service Name |
|---|---|---|
| vulnerability assessment / VA / vuln scan | VA | Vulnerability Assessment |
| CMMC / CMMC L2 / cmmc readiness | CMMC-L2 | CMMC Level 2 Readiness Assessment |
| NIST 800-171 / nist gap / 800-171 | NIST-171 | NIST SP 800-171 Gap Assessment |
| security program / SPA / maturity | SPA | Security Program Assessment |
| executive risk / ERA / board | ERA | Executive Risk Assessment |
| policy / policies | POLICY | Security Policy Development |
| sentinel / onboarding | SENTINEL | Sentinel Implementation |

If ambiguous, ask once to confirm before proceeding.

---

### Step 3: Build variables

From inputs, derive:

```
CLIENT_NAME    = e.g., "Acme Defense LLC"
CLIENT_SLUG    = lowercase-hyphenated, e.g., "acme-defense-llc"
SERVICE_CODE   = e.g., "CMMC-L2"
SERVICE_NAME   = e.g., "CMMC Level 2 Readiness Assessment"
ENGAGEMENT_ID  = {YYYY-MM}_{ClientSlug}_{ServiceCode}
                 e.g., "2026-07_AcmeDefense_CMMC-L2"
FOLDER         = playbook/engagements/{ENGAGEMENT_ID}/
START_DATE     = from input or today's date
CONSULTANT     = from input or "Sean Murrill"
CONSULTANT_EMAIL = seanmurrill@vulnaguard.com
```

---

### Step 4: Create folder structure

```
playbook/engagements/{ENGAGEMENT_ID}/
  01-discovery/
  02-planning/
  03-assessment/
    evidence/
  04-analysis/
  05-reports/
    drafts/
    final/
  06-closeout/
```

Use Bash to create all directories in one shot.

---

### Step 5: Generate populated markdown files

For each template relevant to the service (see template map below), create a populated copy in the engagement folder by substituting `{{PLACEHOLDER}}` tokens with real values.

**Discovery questionnaire is always Excel, never Word.**
Generate it with:
```bash
python3 scripts/generate_questionnaire.py \
  --client "{CLIENT_NAME}" \
  --service-code "{SERVICE_CODE}" \
  --service-name "{SERVICE_NAME}" \
  --due "{DUE_DATE}" \
  --output "playbook/engagements/{ENGAGEMENT_ID}/01-discovery/{ClientSlug}_DiscoveryQuestionnaire.xlsx"
```

**Evidence checklist is always Excel, never Word.**
Generate it with:
```bash
python3 scripts/generate_evidence_checklist.py \
  --client "{CLIENT_NAME}" \
  --service-code "{SERVICE_CODE}" \
  --service-name "{SERVICE_NAME}" \
  --output "playbook/engagements/{ENGAGEMENT_ID}/03-assessment/{ClientSlug}_EvidenceChecklist.xlsx"
```

**Universal templates (all services):**
- `discovery-questionnaire.md` → `01-discovery/discovery-questionnaire.md` (internal reference only — client receives the .xlsx)
- `kickoff-agenda.md` → `02-planning/kickoff-agenda.md`
- `status-report.md` → `02-planning/status-report-template.md`
- `evidence-checklist.md` → `03-assessment/evidence-checklist.md`
- `sow.md` → `05-reports/drafts/sow.md`
- `closeout-report.md` → `06-closeout/closeout-report.md`
- `acceptance-form.md` → `06-closeout/acceptance-form.md`

**Service-specific templates:**

| Service | Additional Templates |
|---|---|
| VA | technical-report.md, executive-summary.md |
| CMMC-L2 | technical-report.md, executive-summary.md, poa-m.md, executive-presentation.md |
| NIST-171 | technical-report.md, executive-summary.md, poa-m.md |
| SPA | technical-report.md, executive-summary.md, risk-register.md, executive-presentation.md |
| ERA | executive-summary.md, risk-register.md, executive-presentation.md |
| POLICY | technical-report.md, executive-summary.md |
| SENTINEL | closeout-report.md, acceptance-form.md |

**Token substitution map:**

Replace these tokens in every file:
```
{{CLIENT_NAME}}      → actual client name
{{SERVICE_NAME}}     → full service name
{{ENGAGEMENT_ID}}    → engagement folder ID
{{START_DATE}}       → engagement start date
{{CONSULTANT_NAME}}  → Sean Murrill (or input value)
{{CONSULTANT_EMAIL}} → seanmurrill@vulnaguard.com
{{REPORT_DATE}}      → today's date
{{DATE}}             → today's date
{{VERSION}}          → v1.0
```

Write the populated files using the Read + Write tools. Read the source template, do the substitution, write the output to the engagement subfolder.

---

### Step 6: Export Word documents

Run `export.sh` for each client-facing document (not internal templates like evidence-checklist):

```bash
./playbook/export.sh {path_to_populated_md} "{CLIENT_NAME}"
```

Move exported .docx files into the correct engagement subfolder after export. Use descriptive names:
- `{ClientSlug}_SOW_{SOW_NUMBER}.docx`
- `{ClientSlug}_DiscoveryQuestionnaire.docx`
- `{ClientSlug}_TechnicalReport_v1.0.docx`

If pandoc is not installed, skip export silently and note it at the end.

**CRITICAL — Email sends must use attachments, never inline content.**

When sending documents to clients, always use `--attach` with the Word file. Never paste document content into the email body — this is unprofessional and a data handling risk.

```bash
python3 scripts/microsoft365_api.py send \
  --to "{CLIENT_EMAIL}" \
  --subject "{SHORT SUBJECT}" \
  --body "{SHORT COVER NOTE ONLY — 3-5 lines max}" \
  --attach "{path_to_docx}"
```

The email body is a cover note only. The document is the attachment.

---

### Step 7: Create an engagement README

Write `playbook/engagements/{ENGAGEMENT_ID}/README.md` with:
- Client name and service
- Engagement ID and folder path
- Key contacts (from input)
- Timeline
- Which templates are populated and where
- Next steps checklist:
  - [ ] Send discovery questionnaire to client
  - [ ] Get SOW signed
  - [ ] Schedule kickoff meeting
  - [ ] Confirm access requirements

---

### Step 8: Log to decisions log

Append to `decisions/log.md`:

```markdown
## {DATE} — New Engagement: {CLIENT_NAME} ({SERVICE_CODE})

Started {SERVICE_NAME} engagement for {CLIENT_NAME}. Engagement ID: {ENGAGEMENT_ID}. Folder: playbook/engagements/{ENGAGEMENT_ID}/. Contact: {CLIENT_CONTACT}.
```

---

### Step 9: Close screen

Print one clean summary:

```
✓ Engagement scaffolded: {ENGAGEMENT_ID}

Folder:    playbook/engagements/{ENGAGEMENT_ID}/
Documents: {N} templates populated, {N} Word files exported
Service:   {SERVICE_NAME}

Next 3 actions:
1. Send discovery questionnaire → 01-discovery/discovery-questionnaire.md
2. Send SOW for signature → 05-reports/drafts/sow.docx
3. Schedule kickoff meeting
```

---

## Rules

- One-shot scaffold. Don't ask for confirmation before creating files.
- If a field is missing, use a placeholder like `[TBD]` and flag it in the close screen.
- Don't overwrite an existing engagement folder. If it already exists, warn and stop.
- All token replacement is case-sensitive — match `{{CLIENT_NAME}}` exactly.
- Consultant defaults to Sean Murrill / seanmurrill@vulnaguard.com unless told otherwise.
- Log every new engagement to `decisions/log.md` without exception.
