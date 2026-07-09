# Content Intelligence Pipeline — SeanBuilds

Goal: stop guessing what content format to use by learning patterns from creators already winning in the AI/automation space, then feeding those patterns into `content-calendar`.

## Scope and ownership

- Orchestrator and system of record: `Vulnaguard-AIS-OS`.
- Creative execution specialist: `creative-os` (asset production/editing only).
- Out of scope for ownership: `vulnaguard-capture-os` publishing workflow.

## Stage 1 — Discover and fetch

Tools: Tavily API for creator/topic discovery, YouTube Data API for metadata retrieval.

Pull per post/video:

- title
- caption or description text
- posting timestamp
- video length
- view count
- like count
- comment count
- hashtags
- thumbnail URL

Trigger:

- n8n cron + Tavily search requests, then YouTube API fetches.

Output: raw JSON per creator and per video.

## Stage 2 — Store (Supabase first)

Start with Supabase (relational + easy query). Pinecone is optional later.

Store:

- raw metadata as structured fields
- embeddings of title/caption text for semantic matching

Core fields:

- `creator_name`
- `content_type`
- `post_date`
- `video_length`
- `engagement_rate`
- `caption_text`
- `hashtags`
- `format_tags` (filled by Stage 3)

## Stage 3 — Analyze (Claude/GPT via n8n)

Stage 3 consumes the normalized Stage 2 record and returns one strict JSON object per video. The contract is documented in `references/content-intelligence-stage3-contract.md`.

When returning to Claude environment after a session-limit handoff, use the setup reminder in `references/content-intelligence-return-setup.md`.

Provider wiring:

- primary: Claude
- fallback: OpenAI
- selection: `STAGE3_MODEL_PROVIDER` env var, with `claude` as the default
- session-limit mode: set `STAGE3_MODEL_PROVIDER=deferred` to mark records `deferred_session_limit` and continue batch persistence without model calls
- if the active provider key is unavailable in the current environment, the workflow remains wired but the model node should stay disabled until credentials exist
- Stage 3 is resumable across sessions: persist `batch_id`, `analysis_status`, and the model payload so interrupted work can continue from the last completed record instead of restarting the batch.

Batch analysis tasks:

1. classify format type: talking head, animated explainer, demo, infographic
2. classify topic category
3. classify engagement tier relative to creator baseline
4. derive repeatable patterns:
   - best format by topic type
   - posting windows (day/time)
   - caption structures
   - hashtag clusters tied to engagement

Output contract:

- structured JSON only
- no markdown
- no prose blobs
- stable enum values for format, topic, and engagement tier
- model output must include evidence fields so Stage 4 can reuse the result without re-deriving it

## Stage 4 — Output (Notion Content Playbook)

n8n writes analysis outputs into Notion database: Content Playbook.

Stage 4 scaffold behavior:

- runs after video upsert so Stage 3 data is already persisted
- maps each analyzed video into a Notion page payload
- writes to Notion when `analysis_status=analyzed`
- marks non-analyzed rows as `playbook_status=skipped_not_analyzed`
- stores Notion sync metadata back into Supabase for replay/debug

Fields:

- Topic type
- Recommended format
- Reasoning
- Example reference

`content-calendar` reads this playbook when deciding format for new ideas.

## Stage 5 — Feedback loop (first-party blend scaffold)

Stage 5 scaffold behavior:

- runs after Stage 4 status persistence
- writes a deterministic feedback status for every processed record
- marks records as `pending_first_party_data` until SeanBuilds post-performance rows exist
- persists a `feedback_payload` contract so later blending can replay without reprocessing Stage 1-4

Once Sean's own posting history exists, Stage 5 will blend first-party performance into format recommendations so outputs shift from external creator mimicry toward SeanBuilds-specific performance.

## Build order

1. Stage 1 -> Stage 2 first; manually inspect data quality.
2. Then Stage 3 (analysis).
3. Then Stage 4 (Notion playbook output).
4. Stage 5 scaffold can run now; first-party weighting activates after enough posting history exists.

## Open decisions

- Finalize 5-8 reference creators to scrape (Nate Zerk + peers).
- Confirm Supabase-first baseline (recommended).
- Lock engagement scoring weights for this system.
- Ensure integration extends existing HyperFrames/Notion Creative OS flow without duplication.

## Publishing autonomy guardrail

Keep publishing at L2: generate and queue support can be automated, but any external post still requires Sean approval.

## Stage 1 and 2 implementation scaffold

### n8n node map

The importable workflow scaffold lives at `references/n8n/workflows/content-intelligence-pipeline-v1.json`.

The matching database migration draft lives at `references/sql/content-intelligence-pipeline.sql`.

#### Canvas layout (for screenshots / readability)

The workflow JSON is laid out as one clean left-to-right spine on lane `y=480`, with branches on dedicated lanes so nothing overlaps:

- Top lane (`y=120`) — parallel bookkeeping: `Supabase Upsert Creators` runs alongside the video path and rejoins at `Merge Upserts` → `Mark Batch Complete`.
- Provider branches (`y=340 / 480 / 680`) — Claude / OpenAI / Deferred fan out from `Stage 3 Provider Switch` and rejoin at `Stage 3 Result Parser`.
- Stage 4 branches (`y=380 / 560`) — Notion write vs. skip, rejoining at `Stage 4 Persist Playbook Status`.

Sticky notes group the canvas into five labeled bands (1 Discover & Fetch, 1b Resolve YouTube, 2/3 Normalize & Analyze, 4 Notion Playbook, 5 Feedback), plus callouts on the two switch nodes. A rendered preview of the layout lives at `references/n8n/workflows/content-intelligence-pipeline-v1-layout.svg`. If you re-space nodes, keep them on these lanes so the flow stays readable when zoomed to fit.

1. Cron trigger
   - Runs weekly.
   - Inputs: empty.
   - Output: execution start time and target query list.

2. Tavily search
   - Query for AI/automation creators with strong engagement signals.
   - Output fields: creator candidate, profile URL, source snippet, relevance score.

3. Creator filter
   - Keep only creators that match the reference set Sean wants.
   - Output: deduped creator list.

4. YouTube metadata fetch
   - Resolve each creator's channel from `profile_url` (channel ID or @handle parsed directly, no API call), then pull recent uploads via `channels.list` -> `playlistItems.list` -> `videos.list` (~1 unit/call each). Falls back to `search.list` (100 units) only when the URL shape can't be parsed into a handle or ID.
   - This keeps weekly quota cost near-zero regardless of the reference creator count, instead of the ~100 units/creator/week a name-based `search.list` call would cost.
   - Output fields: title, description, publish time, duration, stats, thumbnail, channel metadata.

5. Normalizer
   - Convert each raw response into one canonical record shape.
   - Output: one row per video with computed engagement rate.

6. Supabase upsert
   - Upsert creator and video records.
   - Store embeddings for title + description text.

7. Stage 3 contract builder
   - Package each normalized record into the strict model input shape defined in `references/content-intelligence-stage3-contract.md`.
   - Preserve the raw metrics needed for classification and downstream Notion export.

8. Stage 3 model router
   - Choose Claude or OpenAI from `STAGE3_MODEL_PROVIDER`.
   - If provider is `deferred`, skip model calls and persist `deferred_session_limit` status for later replay.
   - Emit the provider-specific request payload and keep the other branch as fallback wiring.

9. Stage 4 playbook mapper
   - Build a Notion-ready payload from Stage 3 classifications and evidence fields.

10. Stage 4 Notion writer
   - If `analysis_status=analyzed`, create/update a page in the Content Playbook database.
   - If not analyzed, skip Notion write and persist skip status for later replay.

11. Stage 4 status persist
   - Upsert `playbook_status`, `playbook_page_id`, `playbook_synced_at`, and `playbook_payload` to video rows.

12. Stage 5 feedback scaffold
   - Generate `feedback_status`, `feedback_score`, and `feedback_payload` for each record.
   - Default to `pending_first_party_data` until first-party metrics are available.

13. Stage 5 status persist
   - Upsert Stage 5 feedback fields to video rows for replay and future weighting.

14. Stage marker
   - Mark the record batch as ingested so it is not processed twice.

### Supabase tables

`content_intelligence_creators`

- `id` uuid primary key
- `creator_name` text not null unique
- `platform` text not null
- `profile_url` text not null
- `source_query` text
- `created_at` timestamptz not null default now()
- `updated_at` timestamptz not null default now()

`content_intelligence_videos`

- `id` uuid primary key
- `batch_id` uuid
- `creator_id` uuid not null references `content_intelligence_creators(id)`
- `platform_video_id` text not null unique
- `title` text not null
- `description` text
- `published_at` timestamptz not null
- `duration_seconds` integer
- `view_count` integer not null default 0
- `like_count` integer not null default 0
- `comment_count` integer not null default 0
- `thumbnail_url` text
- `hashtags` jsonb not null default '[]'::jsonb
- `engagement_rate` numeric(10,4)
- `analysis_version` text
- `analysis_status` text not null default 'pending'
- `analysis_payload` jsonb not null default '{}'::jsonb
- `topic_category` text
- `primary_format` text
- `engagement_tier` text
- `analysis_confidence` numeric(5,4)
- `pattern_summary` jsonb not null default '{}'::jsonb
- `playbook_status` text not null default 'pending'
- `playbook_page_id` text
- `playbook_synced_at` timestamptz
- `playbook_payload` jsonb not null default '{}'::jsonb
- `feedback_status` text not null default 'pending_first_party_data'
- `feedback_score` numeric(5,4)
- `feedback_payload` jsonb not null default '{}'::jsonb
- `embedding` vector
- `raw_payload` jsonb not null
- `format_tags` jsonb not null default '[]'::jsonb

`content_intelligence_first_party_posts`

- `id` uuid primary key
- `platform` text not null
- `platform_post_id` text not null unique
- `post_title` text
- `posted_at` timestamptz
- `topic_category` text
- `primary_format` text
- `view_count` integer not null default 0
- `like_count` integer not null default 0
- `comment_count` integer not null default 0
- `save_count` integer not null default 0
- `share_count` integer not null default 0
- `engagement_rate` numeric(10,4)
- `source_payload` jsonb not null default '{}'::jsonb
- `created_at` timestamptz not null default now()
- `updated_at` timestamptz not null default now()

`content_intelligence_batches`

- `id` uuid primary key
- `run_started_at` timestamptz not null default now()
- `run_finished_at` timestamptz
- `status` text not null
- `provider` text
- `model` text
- `search_query` text
- `creator_count` integer not null default 0
- `video_count` integer not null default 0
- `attempt_count` integer not null default 0
- `last_completed_step` text
- `last_processed_video_id` text
- `resume_cursor` text
- `error_message` text
- `notes` text

### Minimal build order for the first pass

1. Create the Supabase tables.
2. Build the n8n cron -> Tavily -> YouTube -> Supabase path.
3. Verify one creator and three to five videos ingest cleanly.
4. Only after data looks clean, add Stage 3 analysis contract + model step.

### Done when

- a weekly run produces deduped creator/video records
- each record has raw payload plus normalized fields
- embeddings are stored for later pattern matching
- the pipeline can be re-run without duplicate inserts