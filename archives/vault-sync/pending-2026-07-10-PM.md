# Pending vault updates — 2026-07-10 PM

**Coverage window:** Since the 2026-07-09-AM note. Covers commits `eda1675`, `cbd72b9`, `c195f0e`, `d6f49cc`, `0347644`, `305acdd`, `12d115d` (and the #7 PR merge).

---

## SeanBuilds/Contract Hunter separation — fully resolved, SMB outreach launch unblocked (decisions/log.md, 2026-07-09)

**What happened:**
- Sean reported `officialseanbuilds.com/outreach` was serving broken/wrong content — suspected a file-level "blend" between Contract Hunter and SMB Outreach repos.
- Initial diagnosis (commit `eda1675`): Contract-Hunter repo is clean. The blend was Contract-Hunter code copied into `vulnaguard-smb-automation`.
- Corrected diagnosis (commit `cbd72b9`): `vulnaguard-smb-automation` was also clean. Real cause: `microfrontends.json` in `JonSvitna/seanbuilds` was routing `/outreach` to the Vercel project named `contract-hunter` — which actually deploys from `vulnaguard-capture-os`, not the SMB repo. The correct `smb-outreach-dashboard` Vercel project (sourced from `vulnaguard-smb-automation`) existed but was never wired into the routing config.
- Fix: PR #2 changed the routing key from `contract-hunter` to `smb-outreach-dashboard`. Merged and verified live (commit `c195f0e`).

**Current state:** `officialseanbuilds.com/outreach` now correctly serves the SeanBuilds SMB Outreach landing page. SMB outreach launch is unblocked. Non-blocking cleanup remains: SMB page code still lives in `vulnaguard-capture-os/apps/web`, and the Vercel project named `contract-hunter` is a misleading label for a Capture OS deployment — both are future-session items, not blockers.

**Vault action:** Log under `wiki/domains/seanbuilds/` (or equivalent). This is a product-separation milestone: two distinct products (Vulnaguard gov-contract tool vs. SeanBuilds SMB outreach) are now correctly isolated and routing to independent deployments. Cross-reference the decision entries in `decisions/log.md` at 2026-07-09 (initial diagnosis) and 2026-07-09 (correction + resolution).

---

## Content Intelligence Pipeline — two of three remaining blockers now closed (commits `d6f49cc`, `0347644`)

**Context:** As of the 2026-07-09-AM note, the pipeline had run its first end-to-end test (10 creator rows loaded), but three blockers remained before enabling the weekly cron schedule.

**Closed today:**
1. **Stage 4 Notion database ID wired** (commit `d6f49cc`): `NOTION_CONTENT_PLAYBOOK_DATABASE_ID` is no longer a placeholder — the Notion Content Playbook database is now connected. Stage 4 (write recommendations to Notion, consumed by `content-calendar`) is fully wired.
2. **Stage 1 Tavily query bug fixed** (commit `0347644`): Tavily was only ever searching the first query in the list (a real bug, not a tuning issue). Fixed — all configured seed queries now run.

**Still open before enabling the weekly schedule:**
- Workflow is still `active:false` in n8n — Sean needs to review and manually flip to active.

**Vault action:** Update the content intelligence page (`wiki/domains/seo-agent/content-intelligence/` or similar). Status: 2 of 3 post-launch blockers resolved. Add: Stage 4 Notion DB now wired, Tavily multi-query bug fixed. One open item: Sean to activate the cron schedule.

---

## No lead or context changes

No new entries in `leads/inbox.md` or `context/` files since the prior note.
