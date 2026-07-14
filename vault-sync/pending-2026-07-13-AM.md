# Pending vault updates — 2026-07-13 AM

**Coverage window:** Since the 2026-07-13 PM vault-sync (`54a0d16`). That note covered MEMORY.md, drafting router, video consolidation, and URL intake Flow B.

---

## Items to pull into Obsidian

### 1. BD email drafting: manual Claude Pro tab replaced by script
*Commit `05a5d48`*

New `scripts/draft_and_send.py` ships a one-shot BD email workflow that replaces the current Claude Pro Projects browser-tab habit for one-off outreach:

- Drafts via a single Anthropic API call (voice rules baked into system prompt — short, not iterative, so token spend per email stays small)
- Shows subject + body, then prompts `[s]end / [r]edraft / [c]ancel` in terminal
- Sends via Resend from the verified `vulnaguard.com` domain (same as the seo-agent pipeline)
- Stdlib only — no new deps

This closes the loop on the drafting-router decision logged 2026-07-12: one-off BD emails now have a real home that runs on API budget, not the Claude Pro flat-rate workaround.

**Vault target:** `wiki/decisions/` or the Sentinel CMMC / SEO agent ops note — adds operational detail to the 2026-07-12 token-discipline entry already worth mirroring there.

---

*Check ran: 2026-07-13 AM. Next check: 2026-07-13 PM.*
