# Clay Lead Automation

Updated: 2026-07-21

## Ownership

| Layer | Owner | System of record |
| --- | --- | --- |
| Source + fit score + enrichment | Clay | Clay tables (non-Enterprise) |
| Intake orchestration + Slack notice + Slack buttons | n8n (Railway) | Workflow executions only |
| Leads, drafts, approval, send | `vulnaguard-seo-agent` | Railway Postgres |

Clay does **not** become a second outreach system. Slack never sends email. n8n never mutates sequence status except by calling SEO Agent approve/reject APIs.

## Daily timing (America/New_York)

1. **6:00 AM** — Clay scheduled source starts. Fit-score in Clay. Enrich contact/email only when `fit_score >= 70`.
2. Clay HTTP API posts each qualified row to the n8n intake webhook.
3. n8n normalizes to the allow-listed contract and POSTs `/api/marketing/leads/clay-batch`.
4. SEO Agent inserts (`source=clay`), drafts immediately, returns `sequence_ids`.
5. **7:00 AM** — Finalizer derives `batch_id=clay-YYYY-MM-DD`, GETs batch summary, posts `#clay-leads`.
6. Sean approves/rejects from Slack buttons or the dashboard. Approve uses the same send path as the UI (touch 1 immediate).

Initial volume: **25–50** enriched leads/day. Ramp toward 200–300 only after bounce/reply/unsubscribe metrics support it.

## Contracts

### Clay → n8n webhook body

Required fields:

- `clay_row_id` (stable Clay row id)
- `batch_id` (`clay-YYYY-MM-DD` Eastern; n8n can default if missing)
- `company_name`, `website`, `email`
- `fit_score` (integer 0–100, must be ≥ 70)
- `fit_reason`
- `recommended_service`: exactly one of `cybersecurity`, `compliance_cmmc`, `website_design`, `systems_automation`

Optional: `contact_name`, `title`, `location`.

Ignored if present: Clay-supplied `category` / `business_line` (SEO Agent derives them).

### SEO Agent intake

`POST /api/marketing/leads/clay-batch`  
`Authorization: Bearer $MARKETING_AUTOMATION_SECRET`

Idempotent on `(source=clay, external_source_id=clay_row_id)`. Replay returns the same `lead_id` / `sequence_ids` and the **stored** `batch_id` (first-write-wins).

### Batch summary

`GET /api/marketing/clay-batches/:batchId` (same bearer)

Returns counts, service breakdown, average fit, up to 3 samples, `dashboard_path`, and `slack_message` Block Kit (actions `clay_batch_approve` / `clay_batch_reject`).

### Approval

`POST /api/marketing/approval/approve` with `{"batch_id":"..."}` or `{"sequence_ids":[...]}`  
`POST /api/marketing/approval/reject` with the same shape.

Replay of an already-terminal batch is a no-op (`approved:0` / `rejected:0`).

## Live workflows (n8n)

| Name | ID | Status |
| --- | --- | --- |
| Clay Lead Intake to SEO Agent | `A6kOqisezATjjT2Q` | **active** (cut over 2026-07-21) |
| Clay Lead Finalizer Slack Notice | `XNI61XnM2jGosa4e` | inactive until `#clay-leads` + secrets wired |
| Clay Slack Batch Approval | `8E3BNYvVRhM5IGKK` | inactive until Slack interactivity + signing secret wired |

Intake webhook (unchanged path):

`https://n8n-production-a4ee.up.railway.app/webhook/clay-leads-7f3d8e1c-52a9-4b67-91d0-6c4a2e8f5b13`

Version-controlled JSON: `infra/n8n/clay-lead-intake.workflow.json`, `clay-lead-finalizer.workflow.json`, `clay-slack-approval.workflow.json`.  
Validator: `node infra/n8n/tests/validate_clay_workflows.mjs`

## Secrets

| Secret | Where |
| --- | --- |
| `MARKETING_AUTOMATION_SECRET` | SEO Agent Railway + n8n (same value) |
| `SEO_AGENT_BASE_URL` | n8n (`https://vulnaguard-seo-agent-production.up.railway.app`) |
| `SLACK_BOT_TOKEN` | n8n |
| `SLACK_SIGNING_SECRET` | n8n (Slack app Basic Information) |
| `SLACK_CLAY_LEADS_CHANNEL_ID` | n8n |
| `SLACK_CLAY_APPROVER_USER_IDS` | n8n (comma-separated Slack user IDs) |
| `NODE_FUNCTION_ALLOW_BUILTIN=crypto` | n8n Railway service (HMAC in Code nodes) |

This Railway n8n often blocks `$env` inside nodes. Prefer credential-store values or literal non-secret URLs. Never commit secrets into workflow JSON in git.

## Pause / retry

- **Pause intake:** deactivate workflow `A6kOqisezATjjT2Q` in n8n, or disable Clay HTTP enrichment.
- **Retry a failed row:** re-run the Clay HTTP enrichment for that row (idempotent on `clay_row_id`).
- **Rotate automation secret:** set new value on SEO Agent Railway first, update n8n Authorization header/credential, then remove the old value.

## Failure diagnosis

| Symptom | Check |
| --- | --- |
| n8n 401 from SEO Agent | `MARKETING_AUTOMATION_SECRET` mismatch |
| 400 `invalid_payload` | Missing fit fields / score &lt; 70 / bad email/domain |
| 500 `draft_failed` retryable | Copywriter/provider error — replay the row |
| Lead stuck `discovered` on old path | Still hitting `/import-confirm` — should be `/clay-batch` |
| Finalizer silent | Workflow inactive, or missing Slack channel/token |
| Slack button no-op | Signing secret / channel / approver allow-list |

## Approval procedure

1. Review `#clay-leads` summary or `/dashboard/marketing-agents?category=clay_leads&batch_id=clay-YYYY-MM-DD`.
2. Approve batch (sends touch 1) or reject (parks sequences).
3. Individual sequence approve/reject still works for exceptions.

## Volume ramp criteria

Stay at 25–50/day until all of the following hold for two consecutive weeks:

- Bounce rate acceptable for the Resend domain
- No unexpected unsubscribe spike
- Fit reasons look accurate on spot-check
- Approval backlog clears same day

Then increase enrichment/export toward the 50–100 band before any larger jump.

## Clay-side setup still required (manual)

1. Create public Slack channel `#clay-leads`, invite the Vulnaguard bot, paste channel ID into n8n.
2. Enable Slack Interactivity → Request URL = Slack approval webhook (from workflow `8E3BNYvVRhM5IGKK`).
3. In Clay HTTP enrichment, map the allow-listed body and Only-run-if `fit_score >= 70` + valid email.
4. Schedule Clay source for 6:00 AM Eastern.
5. Activate finalizer + Slack approval workflows after secrets are set.

## Verified 2026-07-21

- Authorized `clay-batch` create + draft → 201
- Replay same `clay_row_id` → 200, identical lead/sequence
- Live n8n intake webhook → `source=clay`, `category=clay_leads`, status `drafted`
- Batch summary + Slack contract returned for `clay-smoke-2026-07-21`
- Batch reject then replay → `rejected:1` then `rejected:0`
