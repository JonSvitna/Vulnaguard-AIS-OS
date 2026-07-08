# Content Intelligence Return Setup

Use this checklist when you return to the Claude environment and want to continue Stage 3 without losing continuity.

## 1) Confirm current workflow and schema files

- references/n8n/workflows/content-intelligence-pipeline-v1.json
- references/sql/content-intelligence-pipeline.sql
- references/content-intelligence-stage3-contract.md
- references/content-intelligence-pipeline.md

## 2) Ensure Stage 3 environment variables exist

- STAGE3_MODEL_PROVIDER
  - claude for primary Claude route
  - openai for OpenAI route
  - deferred for no-model session-limit mode
- STAGE3_BATCH_ID (optional, set when replaying or resuming a known batch)
- CLAUDE_MODEL
- OPENAI_MODEL
- ANTHROPIC_API_KEY
- OPENAI_API_KEY

## 3) Select mode before execution

- If model access is available in Claude environment:
  - set STAGE3_MODEL_PROVIDER to claude
- If model access is temporarily unavailable:
  - set STAGE3_MODEL_PROVIDER to deferred
  - this marks rows as deferred_session_limit and preserves batch continuity

## 4) Resume from known batch when needed

- If replaying interrupted work, set STAGE3_BATCH_ID to the interrupted batch id.
- Keep provider and model fields consistent for auditability in content_intelligence_batches.

## 5) Verify deterministic creator linkage remains active

- Creator rows must upsert with deterministic id.
- Video rows must carry creator_id and batch_id.
- creator_id remains not null in schema and should not be relaxed unless a new resolver plan is documented.

## 6) Quick sanity checks after run

- content_intelligence_videos rows have:
  - batch_id
  - creator_id
  - analysis_status
- deferred mode runs should show analysis_status = deferred_session_limit.
- claude or openai mode runs should show analysis_status = analyzed for completed rows.

## 7) If anything is broken

- Do not remove continuity fields.
- First check:
  - STAGE3_MODEL_PROVIDER value
  - API key presence
  - Stage 3 Provider Switch branch wiring in workflow JSON
  - last_completed_step and last_processed_video_id in content_intelligence_batches

## 8) Continuation note

The pipeline is intentionally designed so session limits do not force restarts. Keep using batch_id plus deferred_session_limit status as the handoff-safe boundary.