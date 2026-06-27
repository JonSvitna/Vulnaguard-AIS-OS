# Pending vault updates — 2026-06-27 PM

Reviewed everything since the last note (`pending-2026-06-26-AM.md`, commit `b8c5bd3`) through current `HEAD` (`f6566f4`). Several real items landed in that window via commits `dbbfdab`, `d8c5035`, `2c6ea79`, `f6566f4` — the AM note's "nothing new" call was overtaken by a merge that brought in older branch work.

- **Mail→Slack bounce root cause fixed, infra question resolved.** `decisions/log.md` (2026-06-25, commit `dbbfdab`): deleted the broken catch-all inbox rule (`AQAAAC31xzc=`) that was redirecting all mail to a Slack channel-email address — that feature isn't on Sean's Slack plan, so every redirected message bounced. The real bridge is confirmed to be `mail_to_slack.py` cron **on the DigitalOcean droplet** (`connections.md` row 4, updated 2026-06-25). This also closes the Railway-vs-DigitalOcean contradiction the 06-26 PM note flagged as unresolved — DigitalOcean is the one actually running. Manual NDR cleanup in Outlook still on Sean, per the log.

- **Hermes scanner duplication resolved (architecture decision).** `decisions/log.md` (2026-06-26, commit `2c6ea79`): `hermes-cron` (Railway) is now the single scanner; the `.claude/agents/hermes.md` subagent only merges staged entries from `references/hermes-pending/` going forward. Also marked Buffer and the Website Creation Tool as explicitly **DEFERRED** in `connections.md` (rows 11, 15) instead of ambiguous "live" status.

- **New connection: YouTube channel branding API, live and verified 2026-06-26.** `connections.md` row 16 — `scripts/youtube_api.py`, OAuth-based, can read channel info and update title/bio (`update-branding`). No support for avatar/banner upload or @handle change (stays manual in YouTube Studio). Relevant to the SeanBuilds content line.

- **AfterSwing (side project) — swing-metric scope decision closed out.** `decisions/log.md` (2026-06-26, commit `f6566f4`): confirmed `outToInPath`/`inToOutPath`/`earlyExtension`/`faceToPathDeg` were correctly dropped, not pending — they're not recoverable from single-camera 2D pose data. Real metrics (`tempoRatio`, `swayInches`, `postureChangeDeg`) stay. Flagged as a deliberate scope decision, not a TODO, if swing-path/face-angle ever comes back as a feature ask (would need club-head tracking or LiDAR-gated ARKit depth).

- **6 new leads triaged into `leads/inbox.md`** (dated 2026-06-24/25, landed via the `dbbfdab` merge): mostly low CMMC relevance (branding/wayfinding, EHR privacy software, water-authority construction RFP — noise from the BidNet profile). Two worth a second look: **Weld County, CO** — Dell maintenance/support solicitation (closes 07/16), county IT spend signal; **City of Greeley, CO** — SCADA/I&C/networking solicitation (closes 07/02), touches critical infrastructure, moderate infosec angle even though not DoD/CUI-scoped.

No `context/` file changes in this window.
