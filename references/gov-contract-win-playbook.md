# First Federal Win Playbook — $2.5k / $5k / $10k Contracts

How Sean lands his first federal award in the micro-purchase range. Written for a newcomer with zero past performance. Source of truth for the "secure a win" push.

Updated: 2026-07-06

---

## The one thing to understand first

Your target range ($2,500 to $10,000) is not normal contracting. It is the **micro-purchase zone**.

- **Micro-purchase threshold = $10,000** (FAR 2.101, services).
- Below $10k, the government does **not** have to compete the buy. No RFP, no formal bid, no lowest-price shootout.
- A Contracting Officer, or even a government purchase-card (GPC) holder, can just **buy it from any registered vendor they trust**.

That changes everything about how you win. Below $10k you are not "beating" competitors on a scorecard. You are being the **registered, credible, responsive vendor in front of the right buyer at the right moment**. It is relationship + readiness, not proposal gymnastics.

This is the correct entry point for someone with no past performance. You win small to earn the past performance that unlocks the bigger stuff. Do not start by chasing $250k competed solicitations — you will lose to incumbents every time.

---

## Foundation — must exist before any award (do this first)

You cannot be paid by the federal government without these. Check each honestly.

1. **Active SAM.gov entity registration + UEI.**
   - Note: having a SAM.gov *API key* (data access) is NOT the same as an *entity registration* (ability to receive an award). Confirm the registration is ACTIVE, not just that we scrape SAM.
   - Free. Do it at SAM.gov directly, never a paid "registration service."
   - Takes 1–3 weeks (identity validation is the slow part). This is the long pole. Start today if not already done.

2. **NAICS + PSC codes on the registration.**
   - Lead NAICS: **541512** (Computer Systems Design), **541519** (Other Computer Related Services), plus **541690 / 541611** (consulting).
   - PSC codes from our own award data: **DA01, DA10** (IT/telecom services).
   - These are exactly the codes the agencies in `leads/usaspending_opportunities.csv` bought cyber services under.

3. **Small business self-certification** in SAM. Free, instant.
   - **Check set-aside eligibility — this is the single biggest lever if it applies.** SDVOSB (veteran), 8(a), HUBZone, WOSB each let you win contracts competitors are legally barred from. If Sean qualifies for any, register for it. Worth an hour to check.

4. **One-page capability statement.**
   - The most-requested document a CO asks a new vendor for. We have proposal/SOW templates in the playbook but no cap statement yet — worth drafting one.
   - Must fit on one page: company name, UEI/CAGE, NAICS/PSC, 3 core services, differentiators (PenTest+, MS Computer Forensics, Sentinel CMMC), past performance (say "emerging small business" honestly if none), POC.

---

## Fastest path to the first win

### Play A — Sell services TO the government (a real federal contract)

This is what "government contract" means and what the $2.5k–$10k range is built for.

**Lead with ONE fixed-price productized service.** Fixed price + micro-purchase size = the easiest thing on earth for a CO to say yes to. Best candidate from our playbook and award data:

> **Network Vulnerability Assessment — fixed $X,XXX, 2–3 weeks, one report.**

Why this one: `leads/usaspending_opportunities.csv` shows agencies (DHS, Interior, VA, Navy, DoE) buying vulnerability assessment / pen testing / risk assessment / cyber compliance at $14k–$76k. The sub-$10k versions of these exist and get bought on purchase cards constantly. It maps directly to `playbook/services/vulnerability-assessment.md` — the service is already built.

**Two channels to get in front of buyers:**

1. **Posted small solicitations.** Filter capture-os / `sam_gov_api.py` output to services NAICS and small dollar value. Watch notice types: *Combined Synopsis/Solicitation* and *Sources Sought*. These are where sub-SAT buys surface.

2. **Direct outreach to POCs we already collect.** `leads/sam_gov_contacts.csv` is already capturing contracting POC names/emails. For a micro-purchase, a warm, specific email to a CO — "fixed-price $5k network vulnerability assessment, 2-week turnaround, registered small business, PenTest+ / MS Computer Forensics" — can turn into a card-swipe buy without a formal solicitation ever posting. This is the newcomer's cheat code.

**Respond to Sources Sought / RFIs even with no dollar attached.** They are free. They get your name in front of the CO before the requirement is written, and can lead directly to a sole-source micro-purchase (they already know you can do it, it's under $10k, they just buy it).

### Play B — Sell CMMC TO defense contractors (faster money, not a federal contract)

Worth naming because it may close faster than a federal award and it is what Sentinel/Vulnaguard is actually built for.

- CMMC is a requirement imposed **on** DoD contractors, not something the government buys from you directly.
- Selling a **$5k CMMC gap assessment** to a small defense contractor is a commercial B2B sale — same dollar size, no SAM registration needed to get paid, much shorter sales cycle.
- This is exactly what the SEO agent outreach pipeline targets. If the goal is "a win in the $2.5k–$10k range this quarter," this path has fewer gates than a federal award.
- Maps to `playbook/services/cmmc-l2-readiness.md` and `nist-800-171-gap.md`.

### Play C — Subcontract to a prime (fastest past performance)

- Get on an established prime's team as a sub for one small cyber task.
- You inherit their vehicle and compliance overhead. You walk away with **past performance** — the thing that unlocks everything bigger.
- Solves the chicken-and-egg (need past performance to win, get it by winning small or subbing).

---

## Recommended sequence

Run Play A and Play B in parallel. They share the same capability statement and service packaging.

**This week**
1. Confirm SAM.gov entity registration is ACTIVE with UEI. If not, start it today (long pole).
2. Check set-aside eligibility (veteran / 8(a) / HUBZone / WOSB).
3. Draft the one-page capability statement.
4. Package the fixed-price Network Vulnerability Assessment offering ($X, 2–3 weeks, one report) from the playbook.

**Next 2–3 weeks**
5. Point capture-os / the scraper at services NAICS + small-dollar + Sources Sought, and start responding to every relevant RFI.
6. Warm-email 10 contracting POCs from `sam_gov_contacts.csv` with the fixed-price offer.
7. In parallel, aim the SEO agent outreach at small defense contractors needing CMMC (Play B).

**Ongoing**
8. Every RFI response and every micro-purchase is past performance. Log each one. After 2–3 small wins, you have a real record and can step up toward the Simplified Acquisition range ($10k–$250k), where small-business set-asides start working in your favor.

---

## Traps to avoid

- **Do not pay for SAM registration or a "capability statement service."** Both are free / DIY.
- **Do not lead with a competed $100k+ solicitation.** You have no past performance. You will lose to the incumbent and burn weeks writing the proposal.
- **Do not confuse the SAM API key with entity registration.** Verify the actual registration status.
- **Do not price the first job to lose money "to get in."** Micro-purchases are relationship buys, not lowball auctions. Fixed, fair, fast.
