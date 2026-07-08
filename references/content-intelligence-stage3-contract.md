# Content Intelligence Stage 3 Contract

Stage 3 receives one normalized video record from Stage 2 and returns structured JSON only. No markdown, no prose, no code fences.

This stage is resumable across interruptions. Treat the input/output pair as a continuation-safe unit keyed by `batch_id` + `platform_video_id`.

## Input envelope

The model input should carry these fields:

- `analysis_version`
- `batch_id`
- `creator_name`
- `platform`
- `platform_video_id`
- `title`
- `description`
- `published_at`
- `duration_seconds`
- `view_count`
- `like_count`
- `comment_count`
- `hashtags`
- `engagement_rate`
- `format_tags`

## Output shape

The model must return a single JSON object with these top-level keys:

- `analysis_version`
- `batch_id`
- `creator_name`
- `platform`
- `platform_video_id`
- `topic_category`
- `primary_format`
- `engagement_tier`
- `analysis_confidence`
- `pattern_summary`
- `analysis_payload`

## Allowed values

### `primary_format`

- `talking_head`
- `animated_explainer`
- `demo`
- `infographic`
- `screen_recording`
- `short_form`
- `other`

### `engagement_tier`

- `low`
- `medium`
- `high`
- `outlier`

### `topic_category`

Use short, stable labels. Keep the vocabulary narrow and reusable. Examples:

- `ai_automation`
- `workflow`
- `tutorial`
- `business`
- `personal_brand`
- `tooling`
- `other`

## `pattern_summary` object

The `pattern_summary` object must contain these keys:

- `best_format_by_topic`
- `posting_windows`
- `caption_structures`
- `hashtag_clusters`
- `evidence`

Each key should be an array of small JSON objects, not prose.

## `analysis_payload` object

Use `analysis_payload` to capture the full per-video reasoning bundle in machine-readable form. Keep it compact and deterministic.

Recommended fields:

- `format_signals`
- `topic_signals`
- `engagement_signals`
- `reusable_mechanics`
- `risk_notes`

## Non-negotiables

- Output valid JSON only.
- Do not add markdown fences.
- Do not add explanatory prose outside the JSON object.
- Do not invent metrics that are not present in the input envelope.
- If confidence is low, set `analysis_confidence` lower instead of padding with guesses.