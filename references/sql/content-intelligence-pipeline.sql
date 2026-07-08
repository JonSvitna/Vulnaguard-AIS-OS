create extension if not exists vector;

create table if not exists content_intelligence_creators (
  id uuid primary key default gen_random_uuid(),
  creator_name text not null unique,
  platform text not null,
  profile_url text not null,
  source_query text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists content_intelligence_videos (
  id uuid primary key default gen_random_uuid(),
  batch_id uuid,
  creator_id uuid not null references content_intelligence_creators(id) on delete cascade,
  platform_video_id text not null unique,
  title text not null,
  description text,
  published_at timestamptz not null,
  duration_seconds integer,
  view_count integer not null default 0,
  like_count integer not null default 0,
  comment_count integer not null default 0,
  thumbnail_url text,
  hashtags jsonb not null default '[]'::jsonb,
  engagement_rate numeric(10,4),
  analysis_version text,
  analysis_status text not null default 'pending',
  analysis_payload jsonb not null default '{}'::jsonb,
  topic_category text,
  primary_format text,
  engagement_tier text,
  analysis_confidence numeric(5,4),
  pattern_summary jsonb not null default '{}'::jsonb,
  embedding vector,
  raw_payload jsonb not null,
  format_tags jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists content_intelligence_videos_creator_id_idx
  on content_intelligence_videos (creator_id);

create index if not exists content_intelligence_videos_published_at_idx
  on content_intelligence_videos (published_at desc);

create index if not exists content_intelligence_videos_platform_video_id_idx
  on content_intelligence_videos (platform_video_id);

create index if not exists content_intelligence_videos_batch_id_idx
  on content_intelligence_videos (batch_id);

create table if not exists content_intelligence_batches (
  id uuid primary key default gen_random_uuid(),
  run_started_at timestamptz not null default now(),
  run_finished_at timestamptz,
  status text not null,
  provider text,
  model text,
  search_query text,
  creator_count integer not null default 0,
  video_count integer not null default 0,
  attempt_count integer not null default 0,
  last_completed_step text,
  last_processed_video_id text,
  resume_cursor text,
  error_message text,
  notes text
);

create index if not exists content_intelligence_batches_run_started_at_idx
  on content_intelligence_batches (run_started_at desc);

alter table content_intelligence_videos
  drop constraint if exists content_intelligence_videos_batch_id_fkey;

alter table content_intelligence_videos
  add constraint content_intelligence_videos_batch_id_fkey
  foreign key (batch_id) references content_intelligence_batches(id) on delete set null;
