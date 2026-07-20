# Active task

**Status:** in progress
**Switched from:** Codex → Claude Code (manual switch requested by Sean)
**Updated:** 2026-07-19

## What we're doing

Implementing the approved Clay lead automation across the separate SEO Agent and AIOS repositories. Clay will source U.S. small-business leads at 6:00 AM Eastern, enrich only leads scoring 70+, feed the existing Vulnaguard SEO Agent pipeline, and support dashboard or Slack approval before the existing send process runs.

## Target repositories

- Application: `/Users/seanm/Documents/GitHub/vulnaguard-seo-agent`
- n8n workflows and operating documentation: `/Users/seanm/Documents/GitHub/Vulnaguard-AIS-OS`

Do application work in `vulnaguard-seo-agent`, not this AIOS repository. The AIOS repo only owns Tasks 8–10 workflow/connection/runbook work.

## Approved design and plan

- Design: `/Users/seanm/Documents/GitHub/vulnaguard-seo-agent/docs/superpowers/specs/2026-07-19-clay-batch-review-slack-approval-design.md`
- Implementation plan: `/Users/seanm/Documents/GitHub/vulnaguard-seo-agent/docs/superpowers/plans/2026-07-19-clay-batch-review-slack-approval.md`
- Design commit: `fede1dc`
- Plan commit: `5354ec8`

The approved architecture is binding:

- Clay scheduled source starts daily at 6:00 AM `America/New_York`.
- Clay performs fit scoring and enriches contacts only at `fit_score >= 70`.
- n8n owns intake orchestration, 7:00 AM finalization, Slack notification, and signed Slack interaction handling.
- SEO Agent is the only lead, sequence, approval, and send source of truth.
- Slack approval calls the same SEO Agent approval service used by the dashboard.
- No manual-run path in this phase and no second lead database.

## Done so far

All work below is on branch `fix/resend-settings-live-status` in `/Users/seanm/Documents/GitHub/vulnaguard-seo-agent`.

### Task 1: Clay lead metadata and validation — complete and reviewed

- Added pure Clay normalization, score threshold, service mapping, email/domain validation, metadata fields, schema columns/indexes, and config default.
- Added `tsx` and the normal `npm test` regression gate.
- Commits: `ebc7511`, `7f1ec2a`, `88ec3e4`, `bd6fa88`, `7a06e7d`.

### Task 2: systems-automation drafting — complete and reviewed

- Added a dedicated three-touch `systems_automation` prompt and pure prompt selection so these leads never fall through to CMMC copy.
- Included outreach tests in `npm test`.
- Commits: `44f5bd0`, `6cdf4da`.

### Task 3: reusable drafting service — complete and reviewed

- Extracted dependency-injected `draftLeadIds` and kept the old route as a thin compatible wrapper.
- Added explicit drafted/skipped/failed results and skip telemetry.
- Made per-lead persistence transactional with `SELECT ... FOR UPDATE`, rollback, current-state/suppression revalidation, concurrency serialization, stable error codes, and extensive behavioral tests.
- Commits: `3b3522b`, `f6666d5`, `3eb6d55`, `bbb4ecb`.
- Final review: spec compliant and quality reviewer marked Ready.

### Task 4: authenticated Clay intake API — implementation committed, final hardening interrupted

- Added bearer authentication, `POST /api/marketing/leads/clay-batch`, Task 1 validation, concurrency-safe `INSERT ... ON CONFLICT`, Task 3 drafting, authoritative sequence IDs, stable errors, and `.env.example` documentation.
- Added stateful replay coverage proving one lead/sequence and identical sequence ID on retry.
- Commits: `ad9c73f`, `341aa3c`.
- Spec review passed.
- Quality review found one Important issue and three minor hardening items. Work began, then Sean said pause and requested this handoff.

## Exact next step

Resume Task 4 quality hardening in `/Users/seanm/Documents/GitHub/vulnaguard-seo-agent`.

There are two intentional, uncommitted partial edits:

- `lib/marketing/service-auth.ts`
- `lib/marketing/service-auth.test.mjs`

They fix the Important timing issue by adding `constantTimeEqual()` that always invokes the padded comparator even when input lengths differ. Review them, run the focused/full tests, and keep them if correct.

Then finish these remaining Task 4 quality items in the route/tests:

1. Before returning retryable 500 for any unsuccessful drafting result, call `deps.onError` with safe structured context. Logging failure must never change the response.
2. On replay, return the stored lead's authoritative `batch_id`, not the incoming batch ID. Add a test replaying one `clay_row_id` with a different batch and document first-write-wins behavior.
3. Add `export const runtime = 'nodejs'` and `Cache-Control: no-store` to intake responses if it can be applied consistently.
4. Add the strongest safe concurrent `Promise.all` duplicate-request test possible. Do not point tests at a production database. A live PostgreSQL smoke remains part of Task 10 because this repo has no isolated test-DB harness.
5. Run `npm test`, touched-file lint, scoped TypeScript checks, and `git diff --check`.
6. Commit the Task 4 hardening, then repeat spec review followed by code-quality review. Do not start Task 5 until both pass.

The interrupted implementer had not edited the route yet. At handoff time only the two service-auth files above were modified.

## Remaining plan tasks

- Task 5: batch summary and shared approval APIs.
- Task 6: shared Slack message contract.
- Task 7: `Clay Leads` dashboard category and batch controls.
- Task 8: AIOS n8n intake, 7:00 AM finalizer, and signed Slack approval workflows.
- Task 9: configure Clay, Slack, production n8n, and secrets.
- Task 10: end-to-end verification and required documentation/decision mirroring.
- Final cross-task review and branch handoff.

## Verification state

- Latest complete suite before the interrupted auth edit: `npm test` passed 42 tests.
- Repo-wide TypeScript is currently polluted by pre-existing `.next` duplicate declarations and errors in the unrelated untracked dashboard file. Use touched/scoped TypeScript checks and do not claim those unrelated failures as introduced.

## Watch out for

- Do not modify, stage, delete, or commit `/Users/seanm/Documents/GitHub/vulnaguard-seo-agent/app/(app)/dashboard/page.tsx`. It is an unrelated untracked user file.
- The SEO Agent branch is not a clean feature branch; it is `fix/resend-settings-live-status`. Do not reset or rewrite history.
- Preserve all existing Vulnaguard sender/signature/footer, suppression, unsubscribe, approval, and Resend behavior.
- Slack signed actions must terminate at an n8n webhook per the approved design. n8n verifies signature/timestamp/channel/user, acknowledges, calls SEO Agent approval/rejection, and updates the Slack message.
- Clay non-Enterprise scheduling constraint is already decided: Clay starts at 6:00 AM; n8n finalizes at 7:00 AM. Do not redesign this as an n8n-triggered Clay run.
- Initial operating volume is 25–50 qualified/enriched leads daily. Ramp toward 200–300 only after deliverability and quality metrics support it.
- The AIOS repository already has unrelated dirty files (`connections.md`, `decisions/log.md`, `infra/`, and `references/clay-lead-intake.md`). Treat them as Sean's existing work, inspect before overlapping, and never discard them.

## Completion protocol

Follow the plan task by task. For each task, require implementation, spec-compliance review, then code-quality review. When the entire implementation and live configuration are complete, reset this file to `**Status:** none` and finish the required AIOS/Obsidian documentation.
