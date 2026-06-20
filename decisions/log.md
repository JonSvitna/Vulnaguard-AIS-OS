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

## 2026-06-19 — Codex/Cursor fallback via `/handoff` skill

**Decision:** Added a `/handoff` skill plus `scripts/sync_agent_manuals.py` and `context/active-task.md` so Sean can switch from Claude Code to Codex CLI or Cursor mid-task without losing context. `CLAUDE.md` stays canonical; the script regenerates `AGENTS.md` (Codex) and `.cursor/rules/aios.mdc` (Cursor) from it. Before switching, the skill snapshots the in-flight task into `context/active-task.md` for the next agent to read first.

**Why:** Sean hits coding usage limits and needs a fallback that doesn't mean re-explaining context from scratch in a different tool. Codex and Cursor don't read `CLAUDE.md` natively, so without this the operating manual would drift or need manual duplication.

**Alternatives considered:** Auto-detecting rate-limit errors and switching automatically — rejected as brittle (each tool surfaces limits differently) and unnecessary; Sean knows when he's hit a limit. Maintaining `AGENTS.md`/Cursor rules by hand — rejected, guaranteed drift over time vs. a one-source-of-truth generator.

**Owner:** Sean

---

## 2026-06-18 — Wire Microsoft 365 via Graph app-only auth, not delegated/MCP

**Decision:** Connected Calendar + mailbox (`seanmurrill@vulnaguard.com`) using a Graph API client-credentials (app-only) flow in a stdlib-only Python script (`scripts/microsoft365_api.py`), instead of an MCP server or delegated OAuth.

**Why:** App-only auth runs unattended (no user sign-in step, no token refresh UI needed) — fits an AIOS that should reach data without Sean re-authenticating. Stdlib-only avoids adding `requests`/`msal` as dependencies for a single script. No MCP server existed for this at the time.

**Alternatives considered:** Delegated OAuth (rejected — needs a human in the loop to refresh); Microsoft Graph MCP server (rejected — adds a dependency for what's currently 3 read/write calls).

**Owner:** Sean.

## 2026-06-19 — Sentinel CMMC pilot-readiness punch list (verified against code, not just docs)

**Decision:** Treat `docs/pilot_readiness_report.md` and `docs/technical_debt_report.md` (dated 2026-05-11) as stale — 73 commits have landed since, including a VUL-261–268 gap-closure pass that already fixed several items those docs still list as broken. Going forward, verify claims against current code before acting on them, not just the docs.

**Confirmed priority order to close the gap to pilot-ready:**

1. **CRITICAL — control catalog divergence (data bug, not a risk).** `control-matrix/frameworks/` (repo root, 110 NIST 800-171 controls) and `backend/control-matrix/frameworks/` (48 controls) have already diverged — missing 62 controls including 3.1.4, 3.1.8–3.1.22, most of 3.4/3.5/3.7/3.8/3.13 families. The loader (`backend/app/services/control_seeder.py:22-45`) resolves `cwd/control-matrix` first, and Railway's deploy cwd is `backend/` (`backend/railway.toml`), so **production loads the 48-control copy**. Every readiness score, contract-eligibility calc, and control-coverage view today is silently evaluated against 44% of the real catalog. Fix: make one tree authoritative (likely point the loader explicitly at repo-root `control-matrix/`, or replace the backend copy with the full 110-control file), then add a CI check that fails the build if the two trees diverge again.
2. Evidence expiry enforcement job — `expires_at` field and UI warnings exist, but `backend/app/services/scheduler.py` only runs `run_due_monitoring_jobs` + `create_compliance_run`; no job expires stale evidence or fires renewal alerts despite `settings.py:55` describing it as intended.
3. Findings update endpoint — `backend/app/routers/findings.py` is GET-only (list). Contracts already has PATCH (`contracts.py:64`), findings doesn't.
4. POA&M closure-evidence workflow — `closure_evidence_id` is settable manually via PATCH (`poam.py:179-188`) but nothing suggests or validates evidence against open POA&M items.
5. Continuous monitoring integration adapters — still `status: "stubbed"` by default (`backend/app/services/integrations/base.py:17`). No active AWS/GitHub/etc. connectors.
6. Document content parsing/OCR — not implemented anywhere. Evidence control-suggestion works on filename/title/description metadata only, never file contents.
7. Mapping rule depth (data-quality gap, not a wiring gap) — the YAML mapping loader IS wired as primary (`readiness.py:121-146`, VUL-265; keyword dict is fallback-only), but `control-matrix/mappings/*.yaml` files are thin: each scanner (Tenable/Rapid7/generic) has essentially one wildcard "match everything" rule, not granular per-finding-type rules. Plumbing works; the rules behind it don't yet justify auditor trust.

**Already done — verified working, don't re-build:** evidence upload/review/control-linking end-to-end (`evidence.py`), scanner CSV import (`importer.py`), auditor export bundle at `/ssp/export` (SSP + controls + evidence + policies, VUL-263), contracts CRUD including update, dashboard hardcoded fallback values already removed.

**Why:** Sean wants the app "as close to 100 as possible" for pilot readiness. Acting on stale audit docs would have wasted effort re-building already-shipped features (mapping loader, export bundle, contracts update) while missing the most damaging live bug (control catalog truncation), which neither the stale docs nor an initial code-search subagent pass caught — only direct file diffing + loader/deploy-config tracing surfaced it.

**Alternatives considered:** Trusting the existing `docs/*_report.md` audit docs as-is (rejected — confirmed stale and wrong on 3+ items); trusting a single Explore-agent pass without independent verification (rejected — it missed the catalog divergence entirely and incorrectly called the mapping loader "not implemented").

**Owner:** Sean.

## 2026-06-20 — Sentinel CMMC punch list: shipped 1-5, scoped 6-8 instead of building blind

**Decision:** Implemented and pushed to `main` (Railway auto-deploys): the control-catalog fix (item 1, commit `459f17a`), the Findings PATCH endpoint (item 3, `4ed8d6b`), and POA&M closure-evidence suggestion/validation (item 4, `68057cf`). Items 6-8 (integration adapter, OCR, mapping rule depth) got scoped into `docs/post_pilot_fixes_scope.md` instead of being built same-session — see that file for size/risk per item.

**Corrections to the 2026-06-19 punch list, found while implementing:**
- Item 1 was worse than logged: `backend/control-matrix/` wasn't just a truncated duplicate of `frameworks/` — it had no `mappings/` subdirectory at all. Since `get_mapping_service()` (`control_mapping.py:138`) looks for `mappings/` inside whatever directory the loader resolves to, production wasn't just running a 48-control catalog — the entire YAML mapping engine (VUL-265) was silently returning `None` and falling back to keyword-only heuristics for every finding. Deleting `backend/control-matrix/` (it had no references anywhere — `git log` confirmed it was abandoned after 2026-05-06, while the root copy got a real update on 2026-06-01) fixed both problems with one change. Verified by simulating Railway's actual deploy cwd (`backend/`) and confirming resolution now lands on the 110-control tree with `mappings/` present; added `backend/tests/test_control_matrix_resolution.py` to pin this.
- Item 2 (evidence expiry) was already fully built — `monitoring.py:84-143` generates `evidence_expiry` `ComplianceAlert`s on a 14-day window (dedup'd against unresolved alerts) on every scheduled compliance run, and `notifications.py:57-107` actually POSTs to Resend's API. No code needed; flagged that it depends on `RESEND_API_KEY` being set in Railway's env to fire for real.

**Why:** Direct verification while implementing (not just reading docs or trusting a prior pass) kept surfacing things that were either worse or already-fixed compared to what got logged the first time. Two real lessons: (1) "the loader is wired" isn't the same claim as "the loader's dependent service can actually find what it needs" — same root cause, two failure modes; (2) before building something flagged as missing, grep for where it'd actually be wired in — `monitoring.py` had the evidence-expiry logic the whole time, just not in the file (`scheduler.py`) I'd looked at originally.

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
