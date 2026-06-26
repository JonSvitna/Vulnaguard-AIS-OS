# Hermes Content Opportunities

<!-- last-scanned: Vulnaguard-AIS-OS=e737e21809692b36b0fe1037301df418bdfdbf46 -->
<!-- last-scanned: Sentinel-CMMC=184f5b30e850689fe088b70a9aef610c7709d0b2 -->
<!-- last-scanned: vulnaguard-seo-agent=352609f71603d0d578511fda39d4953db83fd487 -->
<!-- last-scanned: AfterSwing=b763481275ff8e889c79b152c20ac0dd7bdd5f81 -->
<!-- last-scanned: creative-os=ab7b67da061d882efc1f813ddc686a14c9e9cdeb -->

## Vulnaguard

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
