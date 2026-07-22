# Clay Lead Intake

Updated: 2026-07-21

## Purpose

Use Clay to source small-business prospects for Vulnaguard's cybersecurity,
compliance/CMMC, systems/automation, and website/design services, then send
only fit-scored (70+), email-bearing rows into the existing
`vulnaguard-seo-agent` Clay batch pipeline. Human approval in Slack
`#clay-leads` or the marketing dashboard is required before any send.

Clay does not provide a general synchronous API on non-Enterprise plans. The
supported API-like pattern is:

1. Find, score, and enrich leads in a Clay table (enrich contacts only when
   `fit_score >= 70`).
2. Use Clay's **HTTP API** enrichment to POST each completed row to n8n.
3. Let n8n validate and normalize to the allow-listed Clay contract.
4. Import via SEO Agent `POST /api/marketing/leads/clay-batch` (not the legacy
   CSV import route).

Official references:

- https://university.clay.com/docs/using-clay-as-an-api
- https://university.clay.com/docs/webhook-integration-guide
- https://university.clay.com/docs/http-api-integration-overview

## Live connection (cutover 2026-07-21)

| Piece | Detail |
|---|---|
| Intake workflow | `Clay Lead Intake to SEO Agent` — `infra/n8n/clay-lead-intake.workflow.json` |
| Finalizer workflow | `Clay Lead Finalizer Slack Notice` — `infra/n8n/clay-lead-finalizer.workflow.json` (cron `0 7 * * *`, `America/New_York`) |
| Slack approval workflow | `Clay Slack Batch Approval` — `infra/n8n/clay-slack-approval.workflow.json` |
| Clay → n8n webhook | `POST https://n8n-production-a4ee.up.railway.app/webhook/clay-leads-7f3d8e1c-52a9-4b67-91d0-6c4a2e8f5b13` |
| SEO Agent intake | `POST {{SEO_AGENT_BASE_URL}}/api/marketing/leads/clay-batch` with `Authorization: Bearer {{MARKETING_AUTOMATION_SECRET}}` |
| Batch summary | `GET {{SEO_AGENT_BASE_URL}}/api/marketing/clay-batches/clay-YYYY-MM-DD` |
| Approve / reject | `POST …/api/marketing/approval/approve` or `/reject` with `{ "batch_id": "clay-YYYY-MM-DD" }` |
| Slack channel | `#clay-leads` (`SLACK_CLAY_LEADS_CHANNEL_ID`) |
| Validator | `node infra/n8n/tests/validate_clay_workflows.mjs` |

Registry: `connections.md` row 21. Full ops runbook lands in Task 10 as
`references/clay-lead-automation.md`.

### n8n env / credentials

Prefer `$env` placeholders in the exported JSON. This Railway n8n instance often
blocks node-level `$env` (`N8N_BLOCK_ENV_ACCESS_IN_NODE`); if so, map the same
names into the n8n credential store — never inline secrets.

Required:

- `SEO_AGENT_BASE_URL` (e.g. `https://vulnaguard-seo-agent-production.up.railway.app`)
- `MARKETING_AUTOMATION_SECRET` (must match SEO Agent)
- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`
- `SLACK_CLAY_LEADS_CHANNEL_ID`
- `SLACK_CLAY_APPROVER_USER_IDS` (comma-separated Slack user IDs)
- `NODE_FUNCTION_ALLOW_BUILTIN=crypto` (HMAC + `timingSafeEqual` in the
  approval Code node)

## Allow-listed Clay → SEO Agent body

n8n normalizes each row to exactly these fields (Task 4 contract):

```json
{
  "clay_row_id": "row_123",
  "batch_id": "clay-2026-07-21",
  "company_name": "Acme Plumbing",
  "website": "https://acme.example",
  "contact_name": "Alex Smith",
  "title": "Owner",
  "email": "alex@acme.example",
  "location": "Baltimore, MD",
  "fit_score": 84,
  "fit_reason": "Small local company with an outdated website.",
  "recommended_service": "website_design"
}
```

`recommended_service` must be one of: `cybersecurity`, `compliance_cmmc`,
`website_design`, `systems_automation`.

If Clay omits `batch_id`, intake derives `clay-YYYY-MM-DD` in
`America/New_York`.

## Ideal customer profile

The capability statement dated 2026-06-30 defines what Vulnaguard can deliver;
it does **not** restrict the market to government contractors. This corrected
profile is saved in Clay under **Settings > AI context**.

- Search the full United States across legitimate commercial industries.
- Prioritize privately held, owner-led companies with ~1-20 employees when size
  data exists (delivery-capacity filter).
- Government contractors remain one valuable lane for CMMC/NIST services, but
  government-contract status is never required for general sourcing.

### Service lanes

- **General cybersecurity:** vulnerability/risk assessment, remediation, policy.
- **Compliance/CMMC:** CMMC, NIST SP 800-171, GRC, evidence, monitoring.
- **Systems/automation:** manual workflow / integration problems.
- **Website/design:** no site or clearly outdated/poor-performing site.

### Exclusions

- Fortune 500, major health systems, national enterprises, centralized
  franchises, government-only targeting, companies outside delivery capacity.
- Direct competitors (cyber, CMMC/MSSP, web, marketing, automation agencies).

## Live Clay sources

### Broad U.S. SMB source

- Workbook: `Private US Companies, 2-10 Employees, Diverse Industries`
- Workbook ID: `wb_0tig3j6w3hc4rmRuHmm`
- Table ID: `t_0tig3j6r9TbnpFZvxim`
- View ID: `gv_0tig3j8HAw5f6vkfTud`

### Focused CMMC source

- Workbook: `Defense Manufacturing, Engineering, US`
- Workbook ID: `wb_0tig3ciNVGjGucRT29T`
- Table ID: `t_0tig3cjNBuBdAB3vkFB`

The earlier workbook `wb_0tig31gNrEaVfSZnptP` is a rejected exploration. Do not
run or schedule it.

## Clay-side HTTP body (map columns 1:1)

```json
{
  "clay_row_id": "{{clay_row_id}}",
  "batch_id": "{{batch_id}}",
  "company_name": "{{company_name}}",
  "website": "{{website}}",
  "contact_name": "{{contact_name}}",
  "title": "{{title}}",
  "email": "{{email}}",
  "location": "{{location}}",
  "fit_score": "{{fit_score}}",
  "fit_reason": "{{fit_reason}}",
  "recommended_service": "{{recommended_service}}"
}
```

Only run when `fit_score >= 70` and email is present/valid.

## Daily timing

- **~6:00 AM Eastern** — Clay source/enrichment (Task 9).
- **Through the morning** — Clay HTTP posts → n8n intake → SEO Agent drafts.
- **7:00 AM Eastern** — Finalizer GETs `clay-YYYY-MM-DD`, posts `#clay-leads`
  (status-only if `draft_count=0`; otherwise SEO Agent `slack_message.blocks`
  with Approve/Reject).
- **Approve/Reject** — Slack buttons or dashboard; both call the same SEO Agent
  batch approval APIs. n8n never sends email or changes sequence status itself.

## Validation

```bash
node infra/n8n/tests/validate_clay_workflows.mjs
```

Expected: `PASS`.

## Trial-credit guardrails

- Start at 25–50 qualified/enriched leads/day. Ramp toward 200–300 only after
  quality, approval, reply, bounce, and unsubscribe metrics support it.
- Enrich contacts only for rows scoring 70+.
- Keep outreach review/approval in SEO Agent + `#clay-leads`. Clay supplies
  data; it does not bypass the approval gate.
