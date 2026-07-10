# Content Intake Pipeline (Stage 0) — Slack drop-in + trend sync

Goal: let Sean drop a raw photo, text note, or video into Slack and have the existing
content pipeline (`content-calendar` → `content-pipeline` → `social-post-queue`) take it
from there — classified, drafted, and time-recommended — instead of every post starting
as a typed idea. Paired with a trend-relevance check so an already-shipped idea that
suddenly matches something blowing up (a model release, a tool everyone's talking about)
gets surfaced to post *now* instead of waiting for its rotation slot.

## Scope and ownership

Same split as `references/content-intelligence-pipeline.md`:

- Orchestrator and system of record: `Vulnaguard-AIS-OS`.
- Creative execution specialist: `creative-os` (Remotion render only, via its
  `content-intake-render` skill — see below).
- Out of scope: `vulnaguard-capture-os` (no publishing-workflow ownership there).

No new generation engine — this plugs into what already exists:

- `vulnaguard-seo-agent`'s `POST /api/content-pipeline/generate`
  (`captureMode: "type"|"voice"|"video"`, `brand`, `rawInput`, `voiceSkillSlug` →
  linkedin/instagram/facebook/youtube/video_brief in one call).
- `social-post-queue`'s `GET /api/content-pipeline/next-unposted` — intake-sourced
  records land in the same `content_pipeline_records` table as calendar-sourced ones,
  so they're picked up automatically. No new approval mechanism needed; the L2
  review-before-anything-external gate is unchanged.
- The live n8n instance from the Content Intelligence Pipeline (Railway project
  `n8n-content-pipeline`, `https://n8n-production-a4ee.up.railway.app`, Supabase-backed,
  Anthropic/OpenAI/Notion credentials already in its credential store).
- The existing Slack bot (`SLACK_BOT_TOKEN`, `scripts/slack_api.py`).
- The Notion Content Playbook (Stage 4 output of the Content Intelligence Pipeline) for
  posting-window recommendations.

## Part A — Slack intake

**Built and smoke-tested 2026-07-10.** Two corrections from the original design, found
while actually building it:

- `content_pipeline_records` does **not** live in the Supabase project backing this
  n8n instance — it's in `vulnaguard-seo-agent`'s own Railway Postgres (public proxy
  host in that repo's `.env.local`, `DATABASE_URL`). The SQL migration and the
  workflow's Postgres nodes point there, not at the Content Intelligence Pipeline's
  Supabase project.
- n8n's native Slack Trigger node needs Slack's Event Subscriptions configured in the
  app's admin console (a webhook URL registered outside any API this session had
  access to). Built as a **5-minute Schedule Trigger polling
  `conversations.history`** instead — same pattern the Content Intelligence Pipeline
  already uses elsewhere, no app-config step required. Revisit true event-based
  triggering later if 5-minute latency ever matters.
- The Supabase Storage bucket (`content-intake-assets`, created) turned out to be
  unnecessary for v1: video assets are queued by their Slack `url_private` directly
  (the bot token that reads it is the same one `content-intake-render` already needs),
  so there's no upload/re-host step. Bucket is left in place for a future version that
  wants assets outside Slack's retention window, but nothing writes to it yet.
- Image/video **vision classification was cut from v1** — the classifier reads message
  text + filename/mimetype only, not actual image content. Real vision classification
  is a natural v2 addition once this baseline is proven out.

### Setup (done)

- Slack channel `#content-intake` (`C0BGLHU0BLH`), bot invited, made public so
  `channels:read` scope (already granted) is enough to resolve its ID.
- Supabase Storage bucket `content-intake-assets` (unused in v1, see above).
- `references/sql/content-intake-pipeline.sql` run against `vulnaguard-seo-agent`'s
  Railway Postgres — adds `source` and `recommended_post_window` to
  `content_pipeline_records`, plus `content_intake_video_queue`.
- n8n credentials added: `Slack Bot Bearer` (httpHeaderAuth) and `SEO-Agent Postgres`
  (postgres), alongside the existing Anthropic/Notion credentials this workflow reuses.

### n8n workflow: "Content Intake Pipeline" (`WCw0Mug93fTmPLJR`, same instance as row 18, currently `active: false`)

1. **Schedule Trigger** — every 5 minutes.
2. **Slack History** — `GET conversations.history` on `#content-intake`, `oldest`
   tracked via workflow static data so each poll only sees new messages.
3. **Extract New Messages** — drops the bot's own messages (`bot_id` present),
   advances the static-data cursor to the newest `ts` seen.
4. **Claude Classify** (`claude-haiku-4-5`, reuses the `Anthropic API Key` credential) —
   text-only classification (see v1 cut above) into one of `content-calendar`'s 6
   pillars plus a best-guess `brand`. Verified live: a real test drop classified
   correctly as `building` / `seanbuilds`.
5. **Parse Classification** — builds `rawInput`, maps `brand` → `voiceSkillSlug`
   (`seans-voice-vulnaguard` | `seanbuilds-voice`), maps `pillar` → a Notion `Topic
   type` value for the playbook lookup (own mapping — the 6 content-calendar pillars
   and the Notion database's existing `Topic type` select options don't share a
   vocabulary; see Open items).
6. **Generate Draft** — `POST /api/content-pipeline/generate` on
   `https://vulnaguard-seo-agent-production.up.railway.app`. Verified live end to end
   (real record created, real linkedin/instagram/facebook drafts returned).
7. **Notion Playbook Lookup** — queries the Content Playbook database filtered by the
   mapped `Topic type`. Verified live — returns real rows; `Recommended posting
   window` reads empty on existing rows (written before that property existed) and
   will populate as the Content Intelligence Pipeline's next scheduled runs add new
   ones.
8. **Extract Posting Window** — first non-empty `Recommended posting window` across
   the matched rows, or `null`.
9. **Update Record** — `UPDATE content_pipeline_records SET source='slack_intake',
   recommended_post_window=...`.
10. **Slack Reply** (parallel branch off Update Record) — posts the generated drafts +
    posting window back into the original thread. Verified live.
11. **Is Video → Insert Video Queue** (parallel branch off Update Record) — if
    `captureMode == 'video'`, inserts into `content_intake_video_queue` with the
    Slack `url_private_download` as `asset_url` plus the thread's channel/ts for
    the render worker (Part C) to reply into later.

**Bug found and fixed 2026-07-10, after the pipeline was first marked "verified":**
Slack's `url_private` field on a video file object points at a *thumbnail*, not the
real file — the actual downloadable asset is `url_private_download`. The workflow's
`Extract New Messages` node originally stored the wrong field; every video queued
before this fix would have downloaded a thumbnail instead of real footage. Patched
directly on the live workflow. Confirmed while fixing: the Slack bot also lacked the
`files:read` OAuth scope needed to download file content at all (had `files:write`
but not `files:read`) — every download attempt was silently redirected to a Slack
login page instead of erroring loudly. Sean added the scope and reinstalled the app;
both fixes verified together with a real end-to-end test (Slack upload → queue →
render → Slack reply).

## Part B — Trend-relevance sync

Reuses Stage 1 of the Content Intelligence Pipeline (Tavily creator/topic discovery —
already finds what's getting traction in AI/automation) instead of a second
trend-discovery system.

1. New n8n step appended after Stage 1's Tavily pull, on a **daily** cadence (tighter
   than the weekly full pipeline run — news-driven relevance is time-sensitive).
   Extracts topic/tool keywords from what's trending that day.
2. Matches those keywords against two sources: `content-calendar.md`'s unexpanded rows,
   and `hermes-opportunities.md`'s `[unused]` entries (real things Sean already
   shipped/fixed). Simple keyword/embedding-similarity match is enough for v1.
3. On a match, post a Slack message (same bot, `#content-intake` or a dedicated
   `#content-trending`) naming the match: what's trending, which calendar row or
   hermes entry it lines up with, and an offer to post today instead of waiting.
4. On Sean's approval, `content-calendar`'s existing "expand an idea" step runs
   immediately, out of normal rotation order — reused as-is, just triggered early.

No new generation logic here — this is a priority signal layered on the existing
calendar + hermes-opportunities flow. `content-calendar`'s `SKILL.md` needs a small
note that a trend-match can pull a row forward out of rotation order (today it assumes
strict day-by-day rotation).

## Part C — creative-os render worker

**Rebuilt 2026-07-10 as an always-on service**, replacing the original
agent-triggered design. `creative-os` still has no HTTP API, so this isn't n8n
calling into creative-os directly — it's a standalone worker that self-polls the
same queue table, decoupled from both n8n and any Claude session:

- `creative-os/render-worker/` — a small Node service (own `package.json`, ~150
  lines, `pg` as its one real dependency). Self-polls `content_intake_video_queue`
  every 2 minutes (`POLL_INTERVAL_MS`), no n8n workflow changes needed — it reads
  the exact same table the workflow already writes to.
- `creative-os/render/src/IntakeClip.tsx` — new generic, props-driven Remotion
  composition (`intake-clip`), registered in `Root.tsx` with `calculateMetadata` for
  dynamic duration based on beat count. **Deliberately a fixed default template, not
  a bespoke edit**: `CornerCard` beat cards cycling through `video_brief.points`,
  brand-specific `Outro` (two presets: `vulnaguard`, `seanbuilds`), no live
  word-synced captions (would need real transcription — out of scope for v1). Every
  real video rendered before this only existed because an agent hand-built a
  one-off composition with actual creative judgment (beat placement, color choices)
  — an unattended worker can't replicate that, so this trades bespoke art direction
  for throughput/reliability. A specific clip can still get a hand-built edit later
  if it earns it.
- Deployed as its own Railway project/service, **`creative-os-render-worker`**
  (`https://creative-os-render-worker-production.up.railway.app`), Dockerfile at
  `creative-os/render-worker/Dockerfile` (build context = repo root via
  `creative-os/railway.json`'s `dockerfilePath`, since the image needs both
  `render/` and `render-worker/`). Chromium/ffmpeg system deps followed Remotion's
  documented Docker recipe — built clean on the first attempt, no iteration needed.
  Own env vars (`DATABASE_URL`, `SLACK_BOT_TOKEN`, `POLL_INTERVAL_MS`) — not shared
  automatically from any other service.
- Verified end to end with a real Slack upload → queue insert → worker poll →
  Remotion render → Slack upload back into the thread, all live, no mocks.
- The original `creative-os/.claude/skills/content-intake-render/SKILL.md` Claude
  skill still exists as a manual/on-demand fallback (e.g. to force a render without
  waiting for the next poll), but the worker is the primary path now. The local
  `/loop` job that used to run that skill every 30 minutes was cancelled once the
  Railway worker went live — it was session-bound (died when the session closed);
  the worker has no such dependency.

## Build order

1. ✅ Run `references/sql/content-intake-pipeline.sql` (against `vulnaguard-seo-agent`'s
   Railway Postgres, not the Supabase project — see correction above).
2. ✅ Create `#content-intake` in Slack, invite the bot, create the
   `content-intake-assets` storage bucket (still unused — video assets are read
   straight from Slack, see the v1 correction above).
3. ✅ Build the n8n "Content Intake Pipeline" workflow (`WCw0Mug93fTmPLJR`). Each step
   smoke-tested individually, then activated (`active: true`) 2026-07-10 — polling
   live.
4. ✅ Build and deploy the always-on render worker (Part C) — replaces the original
   agent-triggered plan.
5. Add the daily trend-check step (Part B) — not yet built. Depends on the Content
   Intelligence Pipeline's Stage 1 Tavily query surfacing usable topics; worth
   checking that query's output quality first (see row 18's open note about
   blog/tool-page results instead of real creator URLs).

## Open items

- Pillar → Notion `Topic type` mapping is a rough v1 heuristic (`content-calendar`'s 6
  pillars don't share a vocabulary with the Notion database's existing select options:
  `ai_automation`/`business`/`personal_brand`/`relationships`/`other`/`uncategorized`).
  Revisit once there's evidence of bad matches.
- No image/video vision classification yet — text/filename-only (see v1 cut above).
- `vulnaguard-seo-agent`'s existing `captureMode: "video"` path and
  `video-website-agent`'s HyperFrames `template-composer` predate creative-os's
  "Remotion is the default first pass" decision (2026-06-22). This pipeline routes new
  video intake to creative-os per that decision, but doesn't retire the older
  `video-website-agent` path — worth a follow-up call on whether that's still live.
- `Recommended posting window` will read empty for a while — it only started being
  written 2026-07-10 (see row 18's correction in `content-intelligence-pipeline.md`),
  so existing Notion Content Playbook rows predate it. Populates naturally as the
  Content Intelligence Pipeline's future scheduled runs add new analyzed rows.

## Publishing autonomy guardrail

Same as the rest of the pipeline: L2. Drafts and queue-prep can run automatically;
nothing external posts without Sean's explicit approval.
