-- Content Intake Pipeline (Stage 0) — Slack drop-in → content-pipeline
-- Adds intake provenance + a posting-time recommendation to the existing
-- content_pipeline_records table (owned by vulnaguard-seo-agent, lives in
-- the same Supabase project as the Content Intelligence Pipeline), plus a
-- handoff queue for creative-os's Remotion render step.
--
-- Run against the same Supabase project backing the n8n instance
-- (project czswxlkfhrwncwuxiflm, schema public).

alter table content_pipeline_records
  add column if not exists source text not null default 'calendar';

alter table content_pipeline_records
  add column if not exists recommended_post_window text;

do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'content_pipeline_records_source_check'
  ) then
    alter table content_pipeline_records
      add constraint content_pipeline_records_source_check
      check (source in ('calendar', 'slack_intake'));
  end if;
end $$;

create table if not exists content_intake_video_queue (
  id uuid primary key default gen_random_uuid(),
  content_pipeline_record_id uuid not null references content_pipeline_records(id) on delete cascade,
  asset_url text not null,
  video_brief jsonb not null,
  slack_channel text,
  slack_thread_ts text,
  status text not null default 'pending' check (status in ('pending', 'rendered', 'failed')),
  created_at timestamptz not null default now(),
  rendered_at timestamptz
);

create index if not exists content_intake_video_queue_status_idx
  on content_intake_video_queue (status);
