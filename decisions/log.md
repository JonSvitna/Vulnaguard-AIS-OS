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

## 2026-06-20 — Wired Slack into the AIOS

**Decision:** Connected Slack via a bot token (`scripts/slack_api.py`, stdlib-only, same pattern as `microsoft365_api.py`/`stripe_api.py`). Bot scopes: `chat:write`, `channels:read`, `channels:history`, `users:read`. Invited the bot to `#all-vulnaguard-sentinel` (`C0AMQU5HN2G`) and confirmed with a live test message. `connections.md` row 4 updated.

**Why:** Closes the loop from the same-day decision to move mail/lead routing to Slack instead of debugging Exchange forwarding further.

**Note:** `conversations.list` currently only requests `public_channel` type — `private_channel` listing returned `missing_scope` (needs `groups:read`, not yet granted). Add that scope and reinstall the app if private-channel access is needed later.

**Owner:** Sean.

## 2026-06-24 — Hosted Claude Code CLI on a DigitalOcean droplet for remote access

**Decision:** Provisioned a DigitalOcean droplet (`vulnaguard-aios`, NYC1, Ubuntu 24.04, `s-1vcpu-1gb`, IP `143.244.148.90`) and installed the real Claude Code CLI (`@anthropic-ai/claude-code`) on it, authenticated via `claude setup-token` directly on the droplet (long-lived credential stored on disk there). Hardened with a non-root `sean` sudo user (key-only SSH), root login and password auth disabled, UFW firewall (SSH only). Repo cloned to `~/Vulnaguard-AIS-OS`, Claude run inside a persistent `tmux` session (`tmux attach -t claude`) so SSH disconnects don't kill work. Access via Termius (SSH key) from phone or any machine.

**Why:** Needed the exact same Claude Code session/interface while away from the home machine or on a work network that blocks claude.ai directly. SSH-only traffic to an owned droplet sidesteps that block. Ruled out two more complex paths first: (1) Claude Code's native Slack integration — confirmed via research it only delegates async tasks to claude.ai/code against GitHub repos, not a live interactive session; (2) a custom Claude Agent SDK + Slack bridge — would need a separate metered API key (new billing line) and rebuilding permission/guardrail logic from scratch. `claude setup-token` run on-machine turned out to be the actual supported path; an env-var (`CLAUDE_CODE_OAUTH_TOKEN`) approach was tried first but the interactive REPL didn't honor it and still prompted for browser login — the on-disk credential from `setup-token` is what actually works.

**Alternatives considered:** Railway (originally favored host, swapped to DigitalOcean per [[references/digitalocean-aios-hosting.md]] — host choice was never the constraint); Slack-based chat bridge via Agent SDK (deferred, still the right call if true chat-via-Slack is ever needed instead of a CLI session); native Claude Code Slack integration (ruled out, wrong capability).

**Note:** Droplet currently only has the public `Vulnaguard-AIS-OS` repo cloned (no GitHub auth configured there yet). Private repos (Sentinel-CMMC, AfterSwing, AI-OS, Jarvis, creative-os, etc.) aren't accessible from the droplet until `gh auth login` or a deploy token is set up there.

**Owner:** Sean.

## 2026-06-20 — Move mail/lead routing to Slack, keep Linear for task tracking (drop ClickUp)

**Decision:** Sean will connect Slack for internal/team communication and lead routing instead of ClickUp. Task tracking stays on Linear (already wired, see `connections.md` row 5) — Slack fills the comms gap, not task tracking.

**Why:** Triggered by debugging a broken Exchange forwarding rule (BidNet solicitation notifications meant for jessicasayre28@gmail.com weren't landing in her inbox, despite the inbox rules being correctly configured per Graph API). Rather than keep debugging Exchange-level mailbox forwarding, Sean decided to move this kind of routing to Slack. He already has Linear for tracking, so ClickUp was never needed.

**Alternatives considered:** ClickUp (briefly considered, dropped once Sean confirmed Linear already covers task tracking — see `project_clickup_slack_migration` memory, now superseded by this decision); continuing to debug Exchange mailbox-level SMTP forwarding (put on hold — not worth the effort given the planned migration).

**Owner:** Sean. Next step when he sets up Slack: update `connections.md` row 4 (currently "Slack ... not yet connected") and wire it into the AIOS.

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

## 2026-06-21 — `/level-up`: scoped and scaffolded `social-post-queue` (Phase 1 of Bike Method)

**Decision:** First real `/level-up` run (skill existed since kit install but had never fired — Day-14 gate not yet reached, run on-demand instead). Scoped and built `social-post-queue`, a skill that pulls the next unposted draft from `references/content-bank.md`, adapts it per platform (Facebook/Instagram/LinkedIn), shows Sean for review/edit, then queues approved posts into Buffer. Buffer chosen as the broker over direct Meta/LinkedIn API integration — Meta requires app review for publish permissions and LinkedIn's Marketing Developer Platform approval is slow/uncertain for a solo dev; Buffer already holds OAuth to all three and exposes one API.

**Method spec:**
- **Constraint:** social posting is the single most disliked recurring task (`context/about-me.md`) and ties to priority #3 (drive consistent traffic to the site) — `content-bank.md` had 5+ drafts written, zero marked `[posted]`.
- **EAD:** Eliminate rejected — Sean wants posting consistency, not zero presence ("one fewer channel, but we need consistency so regular posting is a must"). Automate selected over Delegate — the disliked part is the grind, not a judgment call worth paying someone else for. Split ~60% deterministic (queue management, scheduling, marking posted) / ~30% AI-assisted (platform adaptation, fresh drafts once the bank runs low) / ~10% manual (final review).
- **Process map:** Trigger = 5 posts/week minimum cadence. Data sources = `content-bank.md`, `seanbuilds-voice` skill for new drafts. Transformation = platform-specific reformatting (LinkedIn long-form, Facebook trimmed, Instagram caption + image flag). Decision point = Sean's review/edit before anything queues (hard rule, not a preference — `CLAUDE.md`'s "don't fake my voice on external content without showing me a draft first"). Destination = Facebook/Instagram/LinkedIn via Buffer.
- **Autonomy level:** L2 (Drafted) — AI drafts/adapts, Sean reviews and edits before shipping. Explicitly confirmed, not just defaulted.
- **KPI:** Bucket = more customers (top-of-funnel). Metric = posts/week sustained at ≥5. Follow-on check once volume is steady: whether GSC referral data shows this channel actually driving site traffic.

**Machine handoff:** Shipped as an AI-assisted skill (`.claude/skills/social-post-queue/SKILL.md`, `bike-method-phase: 1`), not a sub-agent — the only AI step needed is platform adaptation/fresh drafting; queueing and scheduling are plain script (`scripts/buffer_api.py`, stdlib-only, matches `scripts/slack_api.py` conventions). Added `references/buffer-api.md` and a row in `connections.md`. `.env` placeholders added: `BUFFER_ACCESS_TOKEN`, `BUFFER_PROFILE_ID_FACEBOOK`, `BUFFER_PROFILE_ID_INSTAGRAM`, `BUFFER_PROFILE_ID_LINKEDIN` — Sean to fill in after connecting accounts in Buffer's UI.

**Why:** Three candidates surfaced (social posting, lead-triage auto-trigger, SEO send-batch cron); social posting ranked highest — it's the one task hitting frequency + drudgery + an explicitly named top pain simultaneously, and had a visible backlog (unposted drafts) proving the gap was real, not hypothetical.

**Alternatives considered:** Direct Meta Graph API + LinkedIn API integration (rejected — slow/uncertain approval process for a solo dev, not boring); auto-publish without review (rejected — violates standing `CLAUDE.md` rule, and Sean explicitly confirmed he wants to review/edit first); lead-triage auto-trigger or SEO send-batch cron as the candidate (deferred, not rejected — still open for a future `/level-up` run).

**Owner:** Sean. Next step: connect Facebook/Instagram/LinkedIn inside Buffer's UI, generate a personal access token at buffer.com/developers/apps, run `python3 scripts/buffer_api.py profiles` to get profile IDs, fill in the four `.env` placeholders. Skill is usable for drafting/review before that — only the final queue step is blocked on real credentials.

## 2026-06-21 — `/level-up` round 2: Eliminated BidNet solicitation triage, not automated

**Decision:** Considered building an auto-trigger for `lead-triage` (currently manual-only — runs only when Sean asks, despite BidNet solicitation emails arriving constantly, 4 in one morning brief alone). Confirmed with Sean that nothing real breaks if these go untriaged: "nothing real breaks, those are mainly noise emails." Did not build a trigger. No artifact shipped this round.

**Why:** EAD's eliminate-first check caught this before any automation work started — the constraint wasn't "triage is too manual," it was "most of what's being triaged doesn't matter." Automating a noisy, low-signal feed would have added standing infrastructure (mailbox watcher, trigger logic) in service of work that doesn't need to happen at all. "Don't automate waste."

**Alternatives considered:** Building the auto-trigger anyway with a higher relevance filter (rejected — adds complexity to solve a problem that mostly isn't there; if BidNet's signal-to-noise improves later, revisit); leaving `lead-triage` as-is and doing nothing (this is effectively the outcome — no code changed).

**Owner:** Sean. Worth revisiting only if BidNet notification quality changes, or if Sean starts actively bidding on NCTCOG/municipal-scale solicitations rather than treating them as background noise. Until then, leave `lead-triage` manual-trigger as-is — don't re-flag this candidate in future `/level-up` runs unless something changes.

## 2026-06-21 — Jarvis becomes its own peer AIOS, not folded into Vulnaguard-AIS-OS

**Decision:** Scaffolded `~/Documents/GitHub/Jarvis` (Helm AI — Sean's half-built mobile-first AI operator product) with its own AIOS structure (`CLAUDE.md`, `context/`, `connections.md`, `decisions/log.md`, `aios-intake.md`, `/onboard` + `/audit` + `/level-up` skills copied in). Registered as a peer connection in both repos (`connections.md` row 12 here, row 6 there) — no shared files or context, just a registry pointer in each direction.

**Why:** Sean wanted a "Jarvis, handle everything" assistant for low-energy sessions — narrow, focused coding work, separate from this AIOS's business-context scope (Sentinel CMMC, SEO agent, leads). Rather than build that from scratch, surfaced that he already has a half-built product literally named Jarvis with its own charter/build-rules/phase-roadmap docs already in the repo — better to finish/assess that than start a third thing. Mixing it into this AIOS would drag business config into Jarvis sessions and vice versa.

**Alternatives considered:** Folding Jarvis into this repo as a sub-folder (rejected — different job, same reasoning as why Sub-OS folders in `EXPANSIONS.md` get scoped operating manuals but stay isolated); building a new lightweight personal-assistant tool instead of touching the existing Jarvis repo (rejected — redundant with a real, more-built product already on disk).

**Owner:** Sean. Next step on the Jarvis side: run `/audit` there, then decide whether to resume Phase 1 build work or shelve it.

## 2026-06-21 — `/level-up` round 3: extracted `ai-shovel-video`'s compositions into `video-website-agent`'s reusable template library

**Decision:** `video-website-agent` was scaffolded (2026-06-19) as a generic HyperFrames block library but had zero actual compositions built — `ai-shovel-video` (built 2026-06-18) was the real, working design system, with content hardcoded to its specific script. Extracted its 5 compositions into `video-website-agent/video/templates/` as parameterized templates (`caption-pills.html`, `beat-text-emphasis.html`, `beat-word-stack.html`, `beat-data-bar-race.html`, `outro-brand-card.html`), each with a `CONFIG` object separating reusable structure/animation from per-video content (text, transcript, stats, colors). Added a catalog `README.md` and `hyperframes-registry-blocks.md` (a reference list of additional pre-built HyperFrames registry blocks — captions, VFX, social overlays, maps, etc. — for beats the 5 core templates don't cover). Shipped the AI-assisted half as `video-website-agent/.claude/skills/template-composer/SKILL.md`.

**Method spec:**
- **Constraint:** both time-per-video (hand-authoring HTML/GSAP each time) and design consistency across videos — confirmed both break roughly equally at 5x volume.
- **EAD:** Eliminate rejected — Sean confirmed weekly+ video output going forward, tied to content/traffic goals. Automate selected: ~60% deterministic (template structure/timing, content substitution), ~30% AI-assisted (picking which beats fit new footage's transcript), ~10% manual (footage selection, final review, posting).
- **Process map:** Trigger = Sean drops in new raw footage. Data sources = footage + whisper transcript + brand tokens (color/font). Transformation = transcript-driven beat selection and CONFIG population. Decision point = which of the 5 templates (+ optional registry blocks) fit the new content, and where they land in time. Destination = rendered MP4 into the existing `social-post-queue`/Buffer pipeline to Instagram.
- **Autonomy level:** L2 (Drafted) — explicitly chosen over the stated long-term goal of full agent autonomy (L3/L4); pushed back per the framework since lower levels haven't been run yet. The skill drafts the full composition (template choice + CONFIG + timing) and stops before render/publish for Sean's review.
- **KPI:** Bucket = less cost (time-per-video is the proximate lever), with cadence/reach as the downstream business result it unlocks. Metric = minutes from raw footage to rendered MP4, tracked informally across the next few videos before deciding if L3 is warranted.

**Why:** Sean's framing was "the goal is to have an agent handle my media essentially" — a real L3/L4 ambition — but `/level-up`'s Method step explicitly defaults to the lowest autonomy level that solves the problem and pushes back on jumping straight to autonomous. Sean agreed: ship L2 now, prove it out, escalate later as a deliberate future decision.

**Alternatives considered:** Building the full agent wrapper same-session (rejected — Sean explicitly chose "extract templates tonight, agent comes later" when asked about timeline, before the interview reframed scope toward an AI-assisted skill rather than a bare deterministic scaffold); scrapping `video-website-agent` and making `ai-shovel-video` itself the source of truth (rejected — `ai-shovel-video` is one video's hardcoded content, not a reusable system; `video-website-agent` was always meant to hold the reusable layer, it just hadn't been built yet).

**Owner:** Sean. Next real video through this pipeline is the validation test — if `template-composer`'s drafts need heavy rework, the template parameterization needs another pass before trusting it further. If it works cleanly across 2-3 videos, revisit autonomy level (L3).

## 2026-06-22 — `/level-up` round 4: extended `social-post-queue` with an IndieHackers branch

**Decision:** Added a separate IndieHackers branch to the existing `social-post-queue` skill rather than building a new skill or sub-agent. It pulls from the same `references/content-bank.md`, filters for build-in-public/technical/lessons-learned entries (not generic promo), rewrites into IndieHackers' longer-form build-log register (distinct from the social caption adaptation used for FB/IG/LinkedIn), shows Sean the draft for approval, then hands off — IndieHackers has no posting API, so Sean copies/pastes/submits manually. Tracked separately in `content-bank.md` via a `[posted-ih YYYY-MM-DD]` tag so the same entry can run on both tracks independently.

**Method spec:**
- **Constraint:** growth-lever gap (priority #2, securing clients via outreach/brand awareness) plus the most-disliked recurring task (content creation + posting, per `context/about-me.md`).
- **EAD:** Eliminate rejected — Sean explicitly wants more IndieHackers presence, not less. Automate selected: ~60% deterministic (pull from content bank), ~30% AI-assisted (filter for audience fit + rewrite register), ~10% manual (Sean reviews, then personally posts since no API exists).
- **Process map:** Trigger = weekly cadence (piggybacking on the existing social-posting cadence; exact day/frequency still being figured out by Sean, default to weekly until proven otherwise). Data source = `content-bank.md`. Transformation = social-caption → IndieHackers build-log voice. Decision point = which bank entries fit IndieHackers' audience. Destination = drafted post handed to Sean for manual copy/paste/submit.
- **Autonomy level:** L2 (Drafted) — and in this case it's a hard ceiling, not a conservative choice: IndieHackers has no API, so L3/L4 aren't physically possible without browser automation, which wasn't considered.
- **KPI:** Bucket = more customers. Metric = IndieHackers posts/week (proxy metric — Sean flagged that real attribution needs seanbuilds.com on its own domain with signup tracking wired up first; currently sits on Vercel without a domain).

**Why:** `/level-up` Mindset interview surfaced three candidates (IndieHackers posting, a skill-discovery research loop, devops config); Sean picked IndieHackers because it directly serves the priorities #2/#3 growth lever and the existing `social-post-queue` infrastructure (content bank + AI-assisted adaptation + review gate) already does 90% of what's needed — only the final posting step differs (manual instead of Buffer).

**Alternatives considered:** New standalone skill (rejected — would duplicate the content-bank pull and review-gate logic already in `social-post-queue` for no benefit, since the only real difference is the destination); sub-agent (rejected — no multi-step reasoning or tool-use beyond a single AI rewrite call, agent would be overkill).

**Owner:** Sean. Revisit cadence (currently defaulted to weekly) once he's actually run it a few times. Revisit the proxy KPI once seanbuilds.com has its own domain and signup tracking — that's when posts/week should be replaced with a real attribution metric.

## 2026-06-22 — Website dev lead pipeline: ICP is "public email, no website," small local-service businesses

**Decision:** Scaffolded a website-design lead pipeline separate from the Sentinel CMMC bid inbox: `leads/website-design-inbox.md` (staging table) and a new `website-design-lead-finder` agent that web-searches business directories (yellowpages.com and similar) for prospects. Defined the ICP: businesses with a public email address but **no website** (the qualifying signal — directly fixable, concrete pitch), small (~5-10 employees, not solo freelancers or chains), in target industries dental, law (small/solo practices), lawn care/landscaping, and advertising/marketing agencies.

**Why:** Sean wants website dev (one of three revenue lines, see `context/about-business.md`) to start generating leads but had no source identified yet — he'd been manually looking at yellowpages.com. "Has email but no website" is a directory-detectable signal that doubles as the sales hook (you can point to the literal gap), unlike "outdated website," which requires more judgment per prospect to qualify.

**Alternatives considered:** Folding website-design leads into the existing `leads/inbox.md` with a type tag (rejected — Sean explicitly wanted it kept separate from CMMC gov-contract bid leads, different qualification criteria and source entirely); waiting for a clearer lead source before scaffolding anything (rejected — Sean asked to scaffold now, structure can absorb a better source later if one appears).

**Open question, not yet built:** Sean also wants outreach sent under whichever brand fits the business attached (SeanBuilds, Vulnaguard, or others he adds later) rather than a single fixed identity. Today's Resend setup (`connections.md` row 9 / row 2) is verified only for the `@vulnaguard.com` domain through the `vulnaguard-seo-agent` pipeline. Multi-brand sending needs a sender-identity decision (per-brand verified Resend domain or sub-domain, plus the SEO agent's lead/outreach schema picking which identity to send under) before it's real — flagging, not building blind.

**Owner:** Sean. Next step: pick a real industry + city/region and run `website-design-lead-finder` to populate the inbox; revisit the multi-brand sending question once there's a brand beyond Vulnaguard actually attached to a deal.

## 2026-06-22 — AfterSwing: dropped fake swing-path/face-angle metrics, ship only real measurements before weekend test

**Decision:** Audited `~/Documents/GitHub/AfterSwing`'s swing analysis pipeline ahead of Sean's weekend golf test. Found the existing iOS pose analysis (`PoseVision.swift`) was fabricating its core signal: `outToInPath` was literally `steepShaft AND swayOffBall`, two crude unrelated proxies (wrist-height trend, shoulder-X range), and `inToOutPath`/`earlyExtension`/`faceToPathDeg` were declared but never computed (always false/0). Worse, `PhaseDetector.detectPhases` was named as if it analyzed wrist data but actually ignored it — address/takeaway/top/downswing/impact/follow-through were fixed time-percentage buckets applied identically to every swing. Backend `feedback.py` rules built on those fake features meant 3 of 6 feedback templates could never fire, and the reachable ones were driven by noise, not real biomechanics.

Replaced with three real, defensible metrics computed from actual Apple Vision body-pose joints (wrist, hip-mid, shoulder-mid) across the full clip: **tempo ratio** (backswing:downswing time, real ~3:1 instructional benchmark), **lateral sway in inches** (hip displacement during backswing, calibrated off measured shoulder width), and **posture change in degrees** (spine-angle shift from address to impact — the real signature of early extension). Phase boundaries (address/top/impact) are now found from actual wrist-height extrema instead of fixed percentages. Backend feedback rules rewritten to use only these three metrics, phrased as observation + drill rather than claiming to know swing path or face angle — that needs real trajectory/depth tracking a single 2D camera can't honestly provide. iOS build verified (`xcodebuild` succeeded for simulator); backend tests verified (7/7 pass, rewritten for the new contract).

**Why:** Sean is testing with real people this weekend and wanted to know if the app actually measures anything before relying on it for live feedback. Full swing-path/face-angle biomechanics from one 2D camera isn't buildable correctly in days — would need either two camera angles or real trajectory tracking (`VNDetectTrajectoriesRequest`, per the reference doc Sean shared). Chose honesty over scope: real numbers a golfer can trust, even if narrower, beat fabricated path/face claims that happened to sound more sophisticated.

**Alternatives considered:** Keep current heuristics and ship as-is, treating this weekend purely as a UX/capture-flow test with verbally-caveated feedback text (rejected by Sean — chose the honest-metrics path instead); add real phase detection only and leave path/face proxies in place (rejected — still ships fabricated claims).

**Known gap, explicitly deferred:** capture still uses plain `UIImagePickerController` at default frame rate (likely 30fps), not the 60/120fps lock the reference doc calls for — fast clubhead motion will still blur some sampled frames. Fixing this needs a custom `AVCaptureSession` pipeline (bigger lift, in progress as the next step in this same session).

**Owner:** Sean.

## 2026-06-22 — Creative OS gets a native Remotion render engine; HyperFrames kept for talking-head/explainer video

**Decision:** After HyperFrames' `capture_hdr_layered` render path repeatedly crashed (`Protocol error (Runtime.callFunctionOn): Target closed`) on HDR-tagged footage during the Agent_OS edit, Sean asked about Remotion as an alternative. Rather than ripping out HyperFrames (a whole template library + skill ecosystem already built and validated on it this session), split by content type: **Remotion** (scaffolded fresh at `creative-os/render/`, a real project with its own `package.json`) becomes the render engine for product-focused/polished video work; **HyperFrames** (`video-website-agent`, Pool 3) stays the tool specifically for "speaking on information" — talking-head/explainer video with caption-pill overlays and beat graphics over real footage. This is an explicit, documented exception to Creative OS's own stated rule ("doesn't do creative work itself, doesn't invent a fourth pool") — updated `creative-os/CLAUDE.md`, `creative-dispatch/SKILL.md`, and `creative-systems.md` to record it as a deliberate carve-out rather than silent drift. Proved the Remotion pipeline end-to-end with a placeholder composition (`npx remotion render` succeeded in seconds, vs. HyperFrames' 12+ minute HDR-crash-prone path for comparable length).

**Why:** Remotion is more mature/React-native with a much larger ecosystem, and would likely have handled the HDR-tagged source footage more gracefully. But HyperFrames' caption/beat-overlay pattern (the thing this whole session's template library was built around) is exactly the right shape for talking-head explainer content — rebuilding that in React wasn't worth it just to dodge one render-stability bug. Splitting by content type keeps both tools' strengths instead of forcing a full migration.

**Alternatives considered:** Full migration off HyperFrames to Remotion (rejected — would mean re-porting the entire template library built this session; HyperFrames' actual problem was one render-path bug, not a fundamental fit issue for explainer content). Keep HyperFrames only, debug the HDR crash further or use `--docker` (still valid as a fallback per `template-composer/SKILL.md`, but doesn't address Sean's broader interest in evaluating Remotion for product video work).

**Owner:** Sean. Revisit once a few real product videos have gone through the Remotion pipeline — confirm the content-type split actually holds rather than one tool creeping into the other's territory.

## 2026-06-22 — Remotion promoted to default first-pass video layer; HyperFrames demoted to optional handoff

**Decision:** After running the same 4 clips through both HyperFrames and Remotion side-by-side (see prior same-day entry), Sean refined the split further: Remotion is now the **default first pass for all video work**, not just product-focused content as originally scoped — it renders in well under 5 minutes per clip vs. HyperFrames' 10-15+, with far less CPU/RAM/battery cost. HyperFrames becomes an optional second-layer handoff, reached for only when a video specifically needs its caption-pill/beat-overlay treatment, not the default carrier for everything. Updated `creative-os/CLAUDE.md`, `creative-dispatch/SKILL.md`, `creative-systems.md`, and `video-website-agent/.claude/skills/template-composer/SKILL.md` to reflect the new default ordering.

Also fixed a real bug found on the first Remotion batch: beat graphics (word-stack/text-emphasis/data-bar-race) were centered, landing directly on top of the speaker's face in talking-head footage. Repositioned to the upper-right corner via a new shared `CornerCard` component (`creative-os/render/src/components/CornerCard.tsx`), with a slide+rotate+pop entrance and fade-out exit — Sean explicitly asked for more lively transitions/animation, not less. Re-rendered all 4 clips with the fix.

**Why:** Direct empirical comparison (same content, same day) made the resource-cost gap undeniable — Sean's own framing was that HyperFrames-as-default is "a drain of resources, a drain of RAM, and a drain of battery power." Splitting by content type (the original same-day plan) undersold how much faster/lighter Remotion is across the board.

**Owner:** Sean. Also wants future short-form clips kept under a tighter length cap (exact number not yet specified) and is open to future hand-tracking-aware graphic placement (parked, not built).

## 2026-06-23 — Svitna gets its Jon Svitna brand identity: coach voice + goal-tailored accountability engine

**Decision:** Ground-truthed Svitna (separate repo, `~/Documents/GitHub/Svitna`) before any soft-test push — confirmed the app actually builds, the backend is live on Railway, and all API routes are real (not stubs), contradicting Sean's initial read that it was "wiring that doesn't connect." The real gap was identity: the app had no personality and read like every other fitness app. Sean revealed Svitna is named after his alter-ego "Jon Svitna" (his serious/intense persona, distinct from the earlier-misheard "John's Fitness" alias) and wants the app to embody that: tough-love accountability, zero tolerance for excuses, genuinely invested in the user winning.

Shipped in one pass (commit `8de19a8`, pushed to `main`):
1. Rewrote the AI coach's system prompt (`backend/src/lib/coachPrompt.ts`) to speak as Jon Svitna — direct, intense, calls out the user's stated `mainStruggle`, holds them to the standard tied to their stated `goal`, while keeping existing safety guardrails (pain handling, no diagnosis, 120-word cap) untouched.
2. Built a goal-tailored accountability engine (`AccountabilityEngine.swift`, extended `ReminderService`, new `AppState.evaluateAccountability()`) that schedules a same-day local notification nudge when today's workout isn't done, tailored copy per goal/struggle, cancelled the moment the workout is completed. Deliberately scoped to use data that already exists (workout completion, streaks) rather than inventing calorie/weight tracking that has no data source yet.
3. Targeted copy pass across onboarding, coach screen, dashboard empty states, and notification settings to carry the voice.

Also folded in two pre-existing fixes from the ground-truth audit: refactored `ProgramCalendarView`'s exercise-swap off an inline API client onto the established `CoachServicing` repository pattern, and stopped tracking `Secrets.xcconfig` going forward (confirmed it's *not* a real secret — Auth0 app is type `Native`/PKCE, so the client ID is meant to be public; walked back the original audit's "rotate credentials" call).

**Why:** Sean's actual blocker to an App Store soft test (10-20 users) wasn't broken plumbing, it was that the product had no differentiated voice — "this feels like there's another app on the marketplace." The old `svitna_product_roadmap.md` was explicitly declared stale/out of scope (written before Sean had real structure on how to build), so this work didn't follow it. Real push notifications (APNs, reaching a user who never opens the app) and calorie/nutrition-based triggers were explicitly deferred — no backend push infra exists yet, and inventing nutrition tracking for the sake of one example trigger would have been scope creep beyond what's needed for a soft test.

**Alternatives considered:** Building full APNs-based push + nutrition tracking now (rejected — bigger lift, no current data source, not needed to validate the soft test); rewriting the entire app from the old roadmap's MVP definition (rejected — Sean explicitly called the roadmap outdated and said the MVP definition itself needs to be redone, not followed).

**Owner:** Sean. Next: live walkthrough in the simulator (onboarding → coach → missed-day nudge) to confirm the voice and accountability trigger feel right before wider soft-test rollout. Real push-to-a-no-show (APNs + backend) is a flagged fast-follow, not blocking.
