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

**"Slack AI" content contamination, fixed 2026-07-10:** `Parse Classification` was
prefixing every `rawInput` with an internal pipeline label (`"[pillar — Slack
intake] "`) before sending it to the generator — the LLM treated "Slack intake" as a
real topic phrase Sean had mentioned, so drafts kept referencing "Slack AI" out of
nowhere. Not a transcription/knowledge gap (Whisper wouldn't have fixed this) — it
was a direct prompt-construction bug. Fixed by dropping the prefix entirely
(`rawInput = captionNote`, no label). Verified via a direct generate-API call using
Sean's real caption text.

### Caption-and-intent ask flow (added 2026-07-10)

Originally, a drop with no caption text fed the generator a generic "no caption
provided" placeholder. Sean asked for something better: have the bot ask in-thread
and wait for a reply instead of guessing. Built as a second branch off the same
5-minute poll:

- **`Has Caption`** (IF) — gates on whether the drop needs a Slack ask before it can
  be classified. Non-video drops only need the ask if there's no caption text at
  all. **Video drops always need the ask**, even with a caption, because caption
  text alone doesn't say what edit Sean wants (see duration-matching below) —
  `!(($json.file_mimetype||'').startsWith('video/')) && hasCaption` is the skip
  condition.
- **`Ask For Caption`** — posts one message per drop, text depends on file type:
  video drops get a combined caption + edit-intent question ("What's this about,
  and how do you want it edited — full length repost, a highlight cut, or a
  specific max length in seconds? Any style notes?"); non-video drops with no
  caption keep the original topic-only ask.
- **`Track Awaiting Caption`** — pushes the drop onto `staticData.global.awaitingCaption`
  (dedup'd on `ts`).
- **`Load Awaiting Captions` → `Check Thread Replies` → `Extract Caption Reply`** —
  parallel branch off the same trigger, polls each awaiting thread for the first
  human reply (filters out the bot's own `bot_id`/user ID), removes it from the
  queue, and feeds the reply text back into the same `Normalize Message` →
  `Claude Classify` path as a normal caption.
- **`Claude Classify`** now also extracts `edit_mode` (`full` | `highlight` |
  `custom` | `n/a`) and `duration_sec` from the reply text for video drops —
  "full length"/"repost as-is" → `full`; "highlight"/"short clip"/no explicit
  length → `highlight`; an explicit number ("under 30 seconds", "about a minute")
  → `custom` + that many seconds. `Parse Classification` passes these through;
  `Extract Posting Window` merges them into `video_brief` (`{ ..., edit_mode,
  duration_sec }`) before the row lands in `content_intake_video_queue` — no schema
  migration needed since `video_brief` is already `jsonb`.

### Duration-matching fix (2026-07-10)

**Bug:** the render worker (Part C) was producing flat ~10-second clips regardless
of actual source footage length — `IntakeClip.tsx`'s duration was computed purely
from `video_brief.points.length * fixed-beat-length`, completely decoupled from the
real video. A 3-minute drop and a 15-second drop rendered to the same length.

**Fix:** `Root.tsx`'s `calculateMetadata` now probes the source file's real
duration server-side via `@remotion/renderer`'s `getVideoMetadata` (ffprobe-based,
works in the Node render process, not the browser), then bounds it by what Sean
actually asked for in the ask-flow reply above:
`intakeClipDurationFromSource(sourceDurationInSeconds, videoBrief)` in
`IntakeClip.tsx` applies a per-`edit_mode` cap (`full` → 180s, `highlight` → 45s,
`custom` → `min(duration_sec, 90s)`), defaulting to `highlight` if no ask-flow reply
landed. The component plays the source video for its full bounded length (not just
an intro slice) — beat cards only cover the first `points.length` beats, then plain
footage continues to the outro. Falls back to the old beat-count estimate only if
the source file can't be probed at all.

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

## Part D — Storyboard, design-concepts library, auto-flagged HyperFrames handoff

**Added 2026-07-10.** `vulnaguard-seo-agent`'s content-pipeline generation now emits a
`storyboard` (beat-by-beat plan: per-beat timing, content, graphic type, plus a
`hyperframes_recommended` flag + reason) alongside the existing `video_brief`, in the
same LLM call. `content_pipeline_records` gained `storyboard jsonb` and
`voice_skill_slug text` columns; `content_intake_video_queue` gained a matching
`storyboard jsonb` column and a new allowed `status` value,
`hyperframes_pending_manual`. Migration:
`references/sql/storyboard-and-design-concepts.sql` (this repo), run against
`vulnaguard-seo-agent`'s Postgres — same distinction as Part A's migration (not the
Supabase project behind this repo's n8n instance).

- The n8n "Content Intake Pipeline" workflow's `Extract Posting Window` code node now
  also passes through `record.storyboard`, and `Insert Video Queue` inserts it into the
  new column — same pattern as the existing `video_brief` column.
- A malformed/missing storyboard from the LLM degrades to `storyboard: null` (validated
  via zod in `agents/content-pipeline/index.ts`) rather than failing generation — every
  consumer (render-worker, `IntakeClip.tsx`) treats `null` as "fall back to the original
  even-spacing beat placement," so this is additive, not a breaking change.
- **Auto-flagged HyperFrames handoff:** when a queue row's
  `storyboard.hyperframes_recommended` is true, `creative-os-render-worker` skips the
  Remotion path, calls the already-existing `POST /api/content-pipeline/hyperframes`
  (returns a ready-to-paste Claude Code build prompt), posts it to the row's Slack
  thread, and marks the row `hyperframes_pending_manual` instead of `rendered`. Sean
  still runs the actual build himself — full unattended HyperFrames automation was
  explicitly scoped out as a bigger, riskier build. Full details in
  `creative-os/references/creative-systems.md`.
- **Design-concepts library:** new `design_concepts` table (same migration file),
  populated by `creative-os/render-worker/scripts/analyze_video_design.js` — Claude
  vision analysis of sampled frames from both creative-os's own past renders
  (automatic, best-effort, fires right after a successful render) and external
  reference videos Sean drops in (manual CLI invocation for v1). Read back into
  content-pipeline's generation prompt so storyboards reuse real past design
  decisions. Requires `ANTHROPIC_API_KEY` on the `creative-os-render-worker` Railway
  service (added 2026-07-10) and `ffmpeg` in that service's Docker image (added to
  `render-worker/Dockerfile` — separate from Remotion's own bundled compositor, which
  doesn't expose a standalone `ffmpeg` binary this script can shell out to).
- `content_intake_video_queue.status` is read only by `render-worker/index.js` and the
  manual `content-intake-render` fallback skill in `creative-os` — both updated;
  nothing else in `vulnaguard-seo-agent`'s dashboard/UI reads that table's status today.

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
