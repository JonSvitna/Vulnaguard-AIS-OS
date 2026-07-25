# Pending vault updates — 2026-07-25 AM

**Coverage window:** Since `pending-2026-07-24-AM.md` — commits `145c7c5`, `457b17b`, `6e196f7` (2026-07-24 ~20:27 ET through 2026-07-25 AM UTC).

---

## New items to consider for Obsidian

### SeanBuilds site: real lead capture live (2026-07-24, commit `6e196f7`)
- **What:** Audited and rewired the entire `SeanBuilds_Rework` site for lead capture. Before: only one form existed that could capture a lead (`/prism` waitlist), and it was silently broken (unverified `seanbuilds.com` domain in Resend). Every other CTA — home nav, 3 project cards, About, `/websites` page — was a dead-end `mailto:` link.
- **Fix:** Three Resend Audiences created as source of truth: `SeanBuilds PRISM Waitlist`, `SeanBuilds Newsletter`, `SeanBuilds Inquiries` (IDs in `connections.md` row 22). New shared helper splits audience write (works today) from notify email (best-effort fallback). Three API routes live and verified end-to-end. All dead-end `mailto:` CTAs converted to a real inquiry modal.
- **Open action:** Verify `seanbuilds.com` in Resend DNS so notify emails send from a branded address — capture works without it, only the "from" address is affected.
- **Vault target:** Borderline — decisions log marked it "purely technical/infra wiring — not mirrored to vault." But it's also the first time the personal brand site can actually capture leads, which is a business capability milestone. Your call whether `wiki/domains/seanbuilds/` gets a note.
- **Decisions log:** `decisions/log.md`, 2026-07-24 entry. `connections.md` row 22 added.

### Lead triage still dark (3rd consecutive failure, now 2026-07-25)
- **What:** Lead triage ran again today, failed again — `MS365_USER_UPN` and `MS365_TENANT_ID` still not set in the cloud environment. 3rd documented failure: 2026-07-21, 2026-07-24, 2026-07-25.
- **Why it matters:** Any solicitation emails since 2026-07-20 are unreviewed. Some may be past close dates.
- **Fix (same every time):** Set `MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`, `MS365_USER_UPN` in the claude.ai session environment config.
- **Vault target:** Skip (ops gap, not a business decision) — included here as a repeat action flag.

---

## Carry-forward (still unconfirmed pulled into Obsidian)

- **SeanBuilds "AI Won't Replace You" — first social batch live (LinkedIn + Instagram + YouTube Shorts)** — brand/content milestone + new distribution stack. Commit `ce606a5`. Vault target: `wiki/decisions/` or `wiki/domains/seanbuilds/`.
- **Clay → n8n → SEO agent cutover / Origami now owns Vulnaguard B2B pipeline** — outreach pipeline architecture. Commits `5fe4c6d`, `42a2ac1`, `28f0063` (2026-07-21); Origami row added 2026-07-23 (`connections.md` row 21). Vault target: `wiki/decisions/`.
- **Prism OS registered as managed product** — `decisions/log.md` entry 2026-07-15. Vault target: `wiki/decisions/`.
- **SEO agent stripped to one job** — major product direction cut (commit `74deeb5`, flagged `pending-2026-07-18-AM.md`). Vault target: `wiki/decisions/` or `wiki/domains/seo-agent/`.
- **ICP correction: broad U.S. SMBs, not CMMC-only** — market positioning (commit `4b0197e`, flagged `pending-2026-07-20-AM.md`). Vault target: `wiki/decisions/`.

---

*Check ran: 2026-07-25 AM. Next check: 2026-07-26 AM.*
