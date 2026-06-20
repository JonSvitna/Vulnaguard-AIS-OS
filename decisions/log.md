# Decisions Log

Append-only record of meaningful decisions and why they were made. `/level-up` Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-06-18 — Wire Microsoft 365 via Graph app-only auth, not delegated/MCP

**Decision:** Connected Calendar + mailbox (`seanmurrill@vulnaguard.com`) using a Graph API client-credentials (app-only) flow in a stdlib-only Python script (`scripts/microsoft365_api.py`), instead of an MCP server or delegated OAuth.

**Why:** App-only auth runs unattended (no user sign-in step, no token refresh UI needed) — fits an AIOS that should reach data without Sean re-authenticating. Stdlib-only avoids adding `requests`/`msal` as dependencies for a single script. No MCP server existed for this at the time.

**Alternatives considered:** Delegated OAuth (rejected — needs a human in the loop to refresh); Microsoft Graph MCP server (rejected — adds a dependency for what's currently 3 read/write calls).

**Owner:** Sean.

## 2026-06-18 — Lowered qualifier_min_score 6→4 and pinned qualifier/copywriter to Claude

**Decision:** In `vulnaguard-seo-agent`, dropped `qualifier_min_score` from 6 to 4 and overrode the `qualifier`/`copywriter` agents to use Claude (`claude-sonnet-4-6`) instead of inheriting the OpenAI `gpt-4o` default, via `ai_provider_config`.

**Why:** 728 sales leads from the 2026-06-17 bulk CSV import were stuck at `status='discovered'` — 753 of 920 qualifier calls failed with OpenAI 429 rate-limit errors (30k TPM / 500 RPM tier) during the import, and nothing retried them afterward (no cron/recurring trigger calls `pipeline/run`). Separately, the imported leads are structurally thin — 0/718 have `cmmc_level_sought` or `employee_count`, only 319/718 have `org_type` — so even a working qualifier scores most at ~3/10 against a min score of 6, mostly producing `disqualified`, not outreach. Lowering the threshold to 4 lets thinner-but-plausible leads (named contact + HUBZone/WOSB designation) reach drafting. Safe because sending still requires manual approval (`sequences.status='approved'`, set only via `/api/marketing/approval/approve`) — lowering the qualifier threshold only changes what reaches the review queue, not what gets sent.

**Alternatives considered:** Enriching all 718 leads with missing fields before qualifying (rejected — too slow against the 90-day client-acquisition clock, for an unproven list); leaving the backlog stuck and fixing only future sourcing (rejected — doesn't recover the leads already paid-for/imported).

**Owner:** Sean. Revisit `qualifier_min_score` back up once a higher-quality lead source replaces this CSV batch — 4 is a deliberate, temporary loosening, not the new permanent baseline.

## 2026-06-18 — Personas stored in Postgres, not as markdown files

**Decision:** The marketing-agents persona system (`new-startup-intro`, `cmmc-specialist`) lives in a `personas` DB table in `vulnaguard-seo-agent`, seeded idempotently in `ensureSchema()`, not as `.md` files in a `personas/` folder as an earlier design doc described.

**Why:** The design doc (`docs/superpowers/specs/2026-06-16-bulk-import-personas-ai-provider-design.md`) called for file-based personas, but the actual implementation pivoted to DB-backed storage — found while trying to locate `vulnaguard-marketing-agents/personas/new-startup-intro.md`, which doesn't exist anywhere on disk. The DB seed already matches the spec's intended content.

**Alternatives considered:** Creating the file-based persona doc as originally specced (rejected — would diverge from what the running app actually reads).

**Owner:** Sean.

## 2026-06-18 — Hold off setting up video-use until the next video project

**Decision:** Identified `video-use` (github.com/browser-use/video-use) as the real tool behind Nate Herk's video editing pipeline — handles transcription/trim/filler-word cutting and can dispatch motion-graphics work to HyperFrames. Did not install it yet.

**Why:** Setup requires a new paid third-party dependency (ElevenLabs API key for Scribe transcription) plus a global Claude Code skill install (`~/.claude/skills/video-use`, not project-scoped). No active video project needs it right now — `ai-shovel-video` is already built and working without it.

**Alternatives considered:** Setting it up immediately (rejected — adds a credential and dependency with no immediate use; better to do it when there's a real next video to run through it).

**Owner:** Sean. Revisit when starting the next long-form video project — see `reference_video_use_pipeline` memory for the full setup steps.

## 2026-06-18 — Ship Sentinel CMMC scheduler in two phases, Phase 1 only today

**Decision:** Added an in-process APScheduler to `Sentinel-CMMC/backend` (`app/services/scheduler.py`) that calls the existing `run_due_monitoring_jobs` + `create_compliance_run` across all orgs every `COMPLIANCE_SCAN_INTERVAL_MINUTES` (default 60), wired into the FastAPI `lifespan` hook. Also added `app/services/notifications.py` with a single `deliver_alert()` hook, called from `create_compliance_run` for every generated alert, currently a no-op logger — the foundation for real email/Slack delivery. Did not implement actual delivery transport today.

**Why:** This closed the last open item from the May 11 pilot readiness report ("Continuous operations: BROKEN — no scheduler, no periodic recalculation"). Nearly all the underlying logic already existed (`MonitoringJob` model, `run_due_monitoring_jobs`, `create_compliance_run` with alert generation) — it was only reachable via a manual, authenticated API call. The fix was almost entirely wiring, not new business logic. Splitting delivery into Phase 2 kept today's change small and testable (27/27 backend tests pass, 4 new) instead of also deciding on a notification transport (Resend? Slack?) under time pressure.

**Alternatives considered:** Building real alert delivery today too (rejected — no transport decision made yet, and Resend is currently only connected for `vulnaguard-seo-agent`, not this repo); using an external cron service instead of in-process APScheduler (rejected — deployment is a single long-running Railway process, in-process is simpler and needs no new infra).

**Owner:** Sean. Phase 2 (real alert delivery) deferred to a later session — see `project_sentinel_scheduler_phase2` memory.

## 2026-06-18 — Pushed Sentinel CMMC scheduler to main, deployed to Railway

**Decision:** Committed (`eda2ba1`) and pushed the Phase 1 scheduler changes to `Sentinel-CMMC` `main`. Railway is wired to the repo via `railway.toml` (root, backend, frontend), so the push should trigger an auto-deploy.

**Why:** Sean wanted the compliance scan running unattended overnight ("dream mode") — committed-but-unpushed code does nothing while asleep; only a live deploy actually runs the hourly scan loop.

**Alternatives considered:** Leaving it local for manual review first (rejected by Sean — explicitly asked to push now).

**Owner:** Sean. Verify on next login that the Railway deploy succeeded and the scheduler is ticking (check logs for the `compliance_scan` job, or that `MonitoringJob`/`ComplianceRun` rows are appearing with `source="scheduler"`).

## 2026-06-19 — Shipped Sentinel CMMC Phase 2: real alert delivery via Resend

**Decision:** `deliver_alert()` now emails org owners/admins through Resend instead of just logging. Recipients resolved via `OrganizationMember` (role owner/admin) + Supabase Admin API for email lookup (no local users table — auth lives in Supabase). Pushed to `main` (`024170e`), confirmed deployed and healthy on Railway.

**Why:** Closed the last gap from the continuous-monitoring work — alerts were generating correctly but going nowhere outside the app. Resend was the natural transport (Sean already uses it for `vulnaguard-seo-agent` outreach, has an account and a verified `@vulnaguard.com` domain). Email org owners/admins rather than just Sean, since this is meant to scale across real customer orgs, not just notify him.

**Alternatives considered:** Slack webhook (rejected — Slack isn't connected anywhere yet, would've added a new integration for no reason when Resend was already available); notifying Sean directly for all orgs (rejected — doesn't scale past the first customer, and the product's value prop is *the org* getting notified, not Sean relaying alerts manually).

**Owner:** Sean. `RESEND_API_KEY` and `ALERT_FROM_EMAIL` are set in Railway production. Nothing left open on this thread unless requirements change.

## 2026-06-19 — Audited vulnaguard-seo-agent, fixed M2/GSC, switched SEO engine to Haiku

**Decision:** Audited the SEO half of vulnaguard-seo-agent (M1-M6 dashboard, separate from the already-solid marketing/outreach pipeline) and found it was almost entirely an LLM prompt wrapper — M2's system prompt literally said "Simulate GSC analysis," and a fully correct, real GSC OAuth integration (`/api/gsc`) existed but was never called by anything. Fixed M2 + Full SEO Pass to fetch real GSC data and inject it into the prompt; updated the system prompt to forbid inventing rows. Switched the SEO chat engine (`app/api/agent/route.ts`) from `claude-sonnet-4-6` to `claude-haiku-4-5-20251001` per Sean's explicit call. Along the way, fixed two real credential issues: the Google OAuth app was in "Testing" status (7-day refresh token expiry) — published it to Production — and the client secret had been rotated/was stale — regenerated it in Cloud Console. Verified the full chain live: real GSC data → real M2 classification on Haiku, no fabricated numbers.

**Why:** Sean's actual question was "does the SEO segment actually work" — it didn't. M2 was the highest-leverage fix since the real integration already existed and just needed wiring, unlike M1 (keyword research) and M3 (page audit), which need new capability (a keyword data source, real HTML crawling) and remain unfixed.

**Alternatives considered:** Building all of M1/M2/M3 in one pass (rejected — M1/M3 need new infrastructure decisions Sean hasn't made yet; M2 was a pure wiring fix with the integration already built, so it shipped same-session while M1/M3 didn't).

**Owner:** Sean. M1 (real keyword data source) and M3 (real page crawling for the audit) are still open — see `project_seo_agent_platform_health` memory for next-step priority.
