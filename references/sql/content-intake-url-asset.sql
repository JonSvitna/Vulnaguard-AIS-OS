-- Content Intake Pipeline — URL-based intake (Flow B bridge)
-- Lets a video dropped as an external URL (YouTube/Drive/etc.) in #content-intake
-- route to the render worker, not just a Slack file upload. The worker already has
-- yt-dlp baked into its Dockerfile (creative-os, 2026-07-11); this column tells it
-- whether to yt-dlp-fetch an external URL or Slack-download a hosted file before render.
--
-- Run against vulnaguard-seo-agent's Railway Postgres (where content_intake_video_queue
-- actually lives — NOT the Supabase project behind this repo's n8n instance; see the
-- correction note in references/content-intake-pipeline.md, Part A).

alter table content_intake_video_queue
  add column if not exists asset_kind text not null default 'slack_file';

do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'content_intake_video_queue_asset_kind_check'
  ) then
    alter table content_intake_video_queue
      add constraint content_intake_video_queue_asset_kind_check
      check (asset_kind in ('slack_file', 'external_url'));
  end if;
end $$;

-- Existing rows keep 'slack_file' (backward compatible). New URL drops set
-- asset_kind='external_url' with asset_url = the raw external link.
