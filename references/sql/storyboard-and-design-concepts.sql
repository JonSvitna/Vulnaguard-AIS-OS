-- Storyboard generation + design-concepts library + auto-flagged HyperFrames handoff
-- Adds a per-record storyboard (beat-by-beat plan) alongside the existing video_brief,
-- a voice_skill_slug column so later steps (e.g. the HyperFrames handoff) can look up
-- which persona a record used, and a design_concepts table fed by analyzing both
-- creative-os's past renders and external reference videos.
--
-- Run against vulnaguard-seo-agent's own Railway Postgres (NOT the Content
-- Intelligence Pipeline's Supabase project) — same distinction the original
-- content-intake-pipeline.sql migration had to get right; content_pipeline_records
-- and content_intake_video_queue both live there, not in Supabase.

alter table content_pipeline_records
  add column if not exists storyboard jsonb;

alter table content_pipeline_records
  add column if not exists voice_skill_slug text;

alter table content_intake_video_queue
  add column if not exists storyboard jsonb;

do $$
begin
  if exists (
    select 1 from pg_constraint where conname = 'content_intake_video_queue_status_check'
  ) then
    alter table content_intake_video_queue
      drop constraint content_intake_video_queue_status_check;
  end if;
  alter table content_intake_video_queue
    add constraint content_intake_video_queue_status_check
    check (status in ('pending', 'rendered', 'failed', 'hyperframes_pending_manual'));
end $$;

create table if not exists design_concepts (
  id uuid primary key default gen_random_uuid(),
  brand text not null,
  source_type text not null check (source_type in ('rendered', 'reference')),
  source_url text not null,
  content_pipeline_record_id uuid references content_pipeline_records(id) on delete set null,
  concept_tags text[] not null default '{}',
  palette jsonb,
  beat_style_notes text,
  transitions_used text[] not null default '{}',
  extracted_at timestamptz not null default now()
);

create index if not exists design_concepts_brand_idx
  on design_concepts (brand, extracted_at desc);
