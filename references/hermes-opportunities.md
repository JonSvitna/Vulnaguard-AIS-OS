# Hermes Content Opportunities

<!-- last-scanned: Sentinel-CMMC=32ef67212d19d0ebc143f91d4eabd61c323bad31 -->
<!-- last-scanned: vulnaguard-seo-agent=71d96680b00258a075c62d7b13d79c182a8b9ac5 -->
<!-- last-scanned: AfterSwing=c5cb7a554190387ad4263a8fce4d53f4b66b875a -->
<!-- last-scanned: creative-os=9233e51bd1bb2ef88ab65ce0bfcd7372e990e21a -->

<!-- last-scanned hashes now track services/hermes-cron/state.json, the source of truth since 2026-06-26. Vulnaguard-AIS-OS removed from scope per the hermes-cron config. -->

## Vulnaguard

### [used 2026-06-27] 2026-06-26 — sentinel-closes-out-7-integration-adapters
**Domain:** Vulnaguard
**Pillar guess:** Behind Sentinel — one real feature and the reason it exists
**Source:** commit 32ef672 in Sentinel-CMMC
**Hook:** Sentinel just closed out all 7 continuous-monitoring integration stubs — Azure Policy maps to CMMC 3.4.2, diagnostic logs to 3.3.1, and Google Drive/SharePoint auto-link evidence to controls using the same classifier already built for manual uploads.
**Talking points:**
1. Turned 3 stub provider definitions into real adapters in one session — the _STUB_PROVIDERS list went from 30 lines of placeholders to an empty array
2. Azure ARM adapter reads Policy compliance state and maps it directly to CMMC control 3.4.2 (config management) and diagnostic logging to 3.3.1 (audit) — the control mapping is baked into the connector, not left to the user
3. Google Drive and SharePoint reuse the existing evidence_classifier.suggest_controls() against filenames, so a file called 'Incident-Response-Policy.pdf' gets auto-linked to the right controls the same way a manual upload would
**Screenshot:** screenshots/hermes/sentinel-closes-out-7-integration-adapters.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — aws-continuous-monitoring-adapter
**Domain:** Vulnaguard
**Pillar guess:** Behind Sentinel — one real feature and the reason it exists
**Source:** commit 8e849f7 in Sentinel-CMMC
**Hook:** AWS just moved from stub to live: Sentinel now pulls IAM password policy and MFA enrollment automatically and maps them to CMMC controls 3.5.3 and 3.5.7.
**Talking points:**
1. AWS was a placeholder stub in the integrations list — this commit replaces it with a real read-only boto3 connector using the same ConnectorAdapter pattern already powering GitHub, Entra ID, and Okta
2. Two specific CMMC controls get auto-evidence: 3.5.7 (password complexity — flags any account where MinimumPasswordLength < 8) and 3.5.3 (MFA enrollment — walks every IAM user and surfaces anyone without a device)
3. Credentials follow a zero-secrets-in-config pattern: access key ID and region live in connection.config, the secret key lives in an env var pointed to by secret_ref — same model as the other connectors so there's no new security surface
**Screenshot:** screenshots/hermes/aws-continuous-monitoring-adapter.png
**Status:** unused

### [skipped 2026-06-27 — near-duplicate of aws-continuous-monitoring-adapter, same controls/pattern] 2026-06-26 — okta-continuous-monitoring-adapter
**Domain:** Vulnaguard
**Pillar guess:** Behind Sentinel — one real feature and the reason it exists
**Source:** commit d940c9b in Sentinel-CMMC
**Hook:** Okta just moved from stub to real: Sentinel now pulls live MFA enrollment and password policy state directly from your Okta org and maps it to CMMC controls 3.5.3 and 3.5.7.
**Talking points:**
1. Okta was a placeholder in the integrations list — today it became a live read-only connector using Okta's SSWS token scheme, scoped to a service account with only okta.policies.read and okta.users.read roles
2. Two controls auto-mapped on every sync: MFA enrollment policy (3.5.3) flips satisfied/open based on whether at least one active policy requires a factor; password complexity (3.5.7) checks minimum length against NIST's 8-char floor
3. Same ConnectorAdapter pattern as GitHub and Entra ID — validate_connection gives specific error messages for 401 vs 403 vs network failure so contractors know exactly what broke, not just 'connection failed'
**Screenshot:** screenshots/hermes/okta-continuous-monitoring-adapter.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — assessor-export-no-frontend-entry-point
**Domain:** Vulnaguard
**Pillar guess:** Behind Sentinel — one real feature and the reason it exists
**Source:** commit 128330c in Sentinel-CMMC
**Hook:** The SSP export endpoint existed for months but had zero UI — assessors couldn't use it without hitting the API directly.
**Talking points:**
1. The /api/v1/ssp/export endpoint (json/text/pdf) was fully built but buried — no button, no link, nothing on the frontend
2. Added an Assessor Export card to the Reports page explicitly scoped for C3PAO assessors vs. the existing Executive Summary card aimed at boards
3. Refactored the download logic into a single downloadFrom() helper to avoid duplicating auth/fetch/blob code across both cards
**Screenshot:** screenshots/hermes/assessor-export-no-frontend-entry-point.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — pdf-assessment-export-sentinel
**Domain:** Vulnaguard
**Pillar guess:** Behind Sentinel — one real feature and the reason it exists
**Source:** commit 2d05363 in Sentinel-CMMC
**Hook:** Sentinel's assessment export now produces a real color-coded PDF an assessor can open — not just an API response.
**Talking points:**
1. Went from json/text-only export to a downloadable PDF with a color-coded control status table (green = satisfied, red = missing, amber = partial) in one commit
2. Chose reportlab (pure-Python) specifically because Railway doesn't have system-level deps like wkhtmltopdf — deployment constraints drove the library decision
3. The PDF is assessor-facing by design: repeating header rows, per-row status color highlights, and a Content-Disposition filename tied to org ID so auditors get a clean hand-off artifact
**Screenshot:** screenshots/hermes/pdf-assessment-export-sentinel.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — opt-out-handling-outreach-replies
**Domain:** Vulnaguard
**Pillar guess:** Behind the build — process, tools, decisions
**Source:** commit 71d9668 in vulnaguard-seo-agent
**Hook:** Leads who replied 'not interested' were left dangling in the queue — one dashboard action now sends the ack, unsubscribes them, and posts to Slack.
**Talking points:**
1. Before: a 'not interested' reply had no clean resolution — the lead sat in an ambiguous state and could theoretically get touched again
2. After: one 'Opt Out' button drafts an editable ack email, fires it via Resend, flips the lead to unsubscribed (skipped by the send queue), and notifies Slack — all atomic
3. Design detail worth noting: the ack body is editable before send, so you can personalize the goodbye instead of blasting a canned response
**Screenshot:** screenshots/hermes/opt-out-handling-outreach-replies.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — stale-usage-panel-fix-collapse-strip
**Domain:** Vulnaguard
**Pillar guess:** Before/after — a number that changed
**Source:** commit 98dc2ad in vulnaguard-seo-agent
**Hook:** The usage panel showed frozen sent-counts after every send action because it fetched once on mount and never refreshed — fixed with a 30s poll plus a refreshKey that fires on every dashboard action, then collapsed the always-expanded chart block into a one-line strip to reclaim vertical space.
**Talking points:**
1. Bug: panel fetched usage stats once on mount, so sent counts looked frozen even though the backend was updating correctly — classic stale-state trap in dashboards
2. Fix was two-part: poll every 30s for background cron ticks, plus wire a shared refreshKey so approve/send/pipeline actions trigger an immediate refresh
3. UI call: replaced the always-expanded full chart block with a collapsed one-line strip (mini sparkline + key numbers) that expands on click — avoids eating permanent vertical space and avoids adding yet another tab to an already busy tab bar
**Screenshot:** screenshots/hermes/stale-usage-panel-fix-collapse-strip.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — token-capture-was-missing-from-ai-calls
**Domain:** Vulnaguard
**Pillar guess:** Lesson from a mistake — what went wrong, what changed after
**Source:** commit 857c66c in vulnaguard-seo-agent
**Hook:** Built an AI cost dashboard and discovered callAI() had been logging every AI call for months but never recording a single token.
**Talking points:**
1. prompt_runs tracked every AI invocation but the input/output token fields were never populated — there was literally no usage data to show until this fix
2. Had to pull token counts directly off the Anthropic/OpenAI SDK response objects and add static per-model pricing to estimate cost — the data existed, it just wasn't being saved
3. The visible dashboard (30-day sent trend, pipeline funnel, per-agent token breakdown with count-up animation) was the forcing function that exposed the silent data gap
**Screenshot:** screenshots/hermes/token-capture-was-missing-from-ai-calls.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — 52-leads-invisible-naming-mismatch
**Domain:** Vulnaguard
**Pillar guess:** Lesson from a mistake — what went wrong, what changed after
**Source:** commit f6acc36 in vulnaguard-seo-agent
**Hook:** A one-character naming mismatch ('website_design' vs 'website_dev') silently hid 52 new leads inside 550 globally drafted sequences.
**Talking points:**
1. The filter showed zero results and looked correct — no error, no warning, just an empty queue that was actually full
2. Fix required renaming the tag AND adding business_line + company-name filtering to the approval API so a specific batch can be isolated and bulk-approved without scrolling through every pending sequence
3. The real lesson: when your tooling has an established convention, importing data that violates it fails silently — validation at import time would have caught this immediately
**Screenshot:** screenshots/hermes/52-leads-invisible-naming-mismatch.png
**Status:** unused

### [used 2026-06-27] 2026-06-26 — cross-app-dedup-at-import
**Domain:** Vulnaguard
**Pillar guess:** SEO agent in action — a specific thing it caught or automated
**Source:** commit 97313b8 in vulnaguard-seo-agent
**Hook:** New leads now get auto-rejected at import time if the other marketing app already emailed them — no more manual dedup passes.
**Talking points:**
1. Built a permanent cross-app dedup check that matches by email, domain, then company name against Ai-Marketing's sent-email history — runs automatically on every import instead of as a one-off manual step.
2. Added a draft-only pipeline route for business lines (like website_design) that have no qualifier rubric yet — leads were sitting at 'discovered' forever because the CMMC scoring rubric would score them wrong, now they skip straight to drafting.
3. The pipeline run log now tracks an `already_contacted` count alongside qualified/disqualified, so there's a real audit trail of how many leads got filtered out before any scoring happened.
**Screenshot:** screenshots/hermes/cross-app-dedup-at-import.png
**Status:** unused

### [used 2026-06-24] 2026-06-20 — control-catalog-44-percent
**Domain:** Vulnaguard
**Pillar guess:** Behind Sentinel — one real feature and the reason it exists
**Source:** commit 459f17a in Sentinel-CMMC
**Hook:** Sentinel's readiness scores now check against the full 110-control NIST 800-171 catalog — not the stale 48-control duplicate it was silently scoring against before, a gap that had it grading at 44% coverage.
**Talking points:**
1. A stale partial duplicate of the control-matrix directory lived inside backend/ — only 48 of 110 controls, with no mappings/ subdirectory at all.
2. Because Railway deploys from backend/ as the working directory, the loader resolved to the stale copy first every time, and the YAML mapping engine silently fell back to keyword-only heuristics instead of erroring out.
3. Fix was just deleting the duplicate so resolution falls through to the real 110-control tree — plus a regression test that pins the control count so this can't silently regress again.
**Status:** unused

### [used 2026-06-24] 2026-06-21 — scanner-rules-never-fired
**Domain:** Vulnaguard
**Pillar guess:** Behind Sentinel — one real feature and the reason it exists
**Source:** commit 0fed78d in Sentinel-CMMC
**Hook:** Sentinel's Tenable and Rapid7 scanner integrations went from zero working rules to ~13 real keyword-based detections per scanner — SMBv1, SQLi, RCE, and expired certs now actually get caught.
**Talking points:**
1. The rule matcher special-cased only the wildcard plugin_id "*" for non-generic sources and returned False for everything else, so any granular keyword/category rule added to tenable.yaml or rapid7.yaml silently never fired.
2. Fixed the matcher to apply the same category/keyword logic to source-specific rules as generic ones, gated by a source check.
3. Replaced the placeholder rules with ~13 real keyword-based rules per scanner — SMBv1, SQLi, RCE, expired/self-signed certs for Tenable; exposed RDP, weak passwords, EOL software for Rapid7 — covering the actual finding types in the sample CSVs.
**Status:** unused

### [used 2026-06-24] 2026-06-21 — five-pages-too-few
**Domain:** Vulnaguard
**Pillar guess:** CMMC myth or pain point contractors actually hit
**Source:** commit ff92c82 in Sentinel-CMMC
**Hook:** Raised Sentinel's evidence-extraction cap from 5 pages to 12 — every control suggestion on a real policy doc now reads the whole thing instead of silently grading off half of it.
**Talking points:**
1. The cap existed as an arbitrary default, not a deliberate compliance decision.
2. Raised the cap to 12 pages / 40k characters to actually cover the documents contractors really submit.
3. Small fix, but it's the kind of silent truncation that would have quietly degraded every control suggestion made from a long policy doc.
**Status:** unused

### [used 2026-06-24 — duplicate of Day 14, not slotted] 2026-06-19 — seo-agent-stopped-faking-data
**Domain:** Vulnaguard
**Pillar guess:** SEO agent in action — a specific thing it caught or automated
**Source:** commit fd5fac3 in vulnaguard-seo-agent
**Hook:** The SEO agent's modules were telling Claude to "simulate" rankings and guess SEO scores blind — now every module is grounded in real crawled data instead of invented numbers.
**Talking points:**
1. Before: M1 Research invented keyword volume/difficulty numbers from nothing, M2 was told to "simulate" search rankings, and M3's on-page audit scored pages without ever actually fetching them.
2. Fix: a real /api/seo-audit endpoint crawls and parses the actual page (title, meta, H1/H2, word count, schema, alt-text coverage), M2 now pulls real Google Search Console data, and M1's keyword suggestions cluster around queries the site actually gets impressions for.
3. Where real data still doesn't exist (keyword volume), the system prompt now says so explicitly rather than fabricating a number — a deliberate "say I don't know" rule baked into the agent.
**Status:** unused

### [used 2026-06-24] 2026-06-18 — wrong-domain-in-outreach
**Domain:** Vulnaguard
**Pillar guess:** Lesson from a mistake — what went wrong, what changed after
**Source:** commit 9c6c852 in vulnaguard-seo-agent
**Hook:** Every cold outreach email now points to the real vulnaguard.com waitlist instead of a placeholder domain that wasn't ours.
**Talking points:**
1. A wrong/placeholder domain had been baked into the copywriter prompt, so outreach emails were pointing leads somewhere that wasn't ours.
2. Fixed to point at the real vulnaguard.com waitlist.
3. Also tightened the copy to stop implying Sentinel is a finished product — it clarifies the tool is in active development, so expectations match reality.
**Status:** unused

### [used 2026-06-24] 2026-06-19 — five-of-fifty-sends-failed
**Domain:** Vulnaguard
**Pillar guess:** SEO agent in action — a specific thing it caught or automated
**Source:** commit 937cf55 in vulnaguard-seo-agent
**Hook:** Vulnaguard's first real batch send went from 5 failed sends out of 50 to 0 — just by spacing sends 250ms apart to respect Resend's rate limit.
**Talking points:**
1. The send loop fired requests as fast as possible with no throttling, ignoring Resend's 5 req/sec cap.
2. Fix was simple — space sends 250ms apart so the batch never crosses the limit in the first place.
3. Failed sends already reset cleanly to "drafted" for retry, so nothing was lost, but it's a clean before/after number (5 failures out of 50 → 0) from the very first real production batch.
**Status:** unused

## SeanBuilds

### [unused] 2026-06-21 — tmp-directory-vanishing-videos
**Domain:** SeanBuilds
**Pillar guess:** Lesson from a mistake — what went wrong, what changed after
**Source:** commit d72c8d1 in AfterSwing
**Hook:** AfterSwing swing recordings now reliably survive from capture to upload — no longer at risk of the OS purging the temp file mid-pipeline.
**Talking points:**
1. UIImagePickerController hands back a video URL inside NSTemporaryDirectory(), which iOS can purge whenever it wants. The app held that raw tmp URL across preflight validation, analysis, and upload — three steps where the file could already be gone.
2. Fix: copy the file into Documents immediately on capture and use that durable URL for every step after.
3. Also replaced a sheet-dismiss-via-sleep hack with an explicit picker.dismiss(animated:) call — a second "stop faking it with a timer" fix in the same commit.
**Status:** unused

### [used 2026-06-24 — duplicate of Days 9/15/23, not slotted] 2026-06-22 — honest-metrics-not-heuristics
**Domain:** SeanBuilds
**Pillar guess:** Lesson from a mistake — what went wrong, what changed after
**Source:** commit a3cd119 in AfterSwing
**Hook:** AfterSwing's swing feedback used to be built on heuristic path/face guesses — now it's rebuilt on real measured tempo, sway, and posture numbers.
**Talking points:**
1. Before: feedback relied on speculative path/face heuristics — boolean claims with no real measurement behind them.
2. After: feedback.py now uses numeric thresholds on measured tempoRatio, swayInches, and postureChangeDeg, flagging rushed/slow tempo, lateral sway, and posture change from actual pose-sample data.
3. Also added a dedicated high-frame-rate SwingCameraView/Controller to replace the old UIImagePicker capture path — better data in means better (and honest) feedback out.
**Status:** unused
