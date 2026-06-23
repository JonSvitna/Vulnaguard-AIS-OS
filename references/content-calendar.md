# Content Calendar

30-day idea engine feeding `references/content-bank.md` (full drafts) →
`social-post-queue` (per-platform posting). Generated/maintained by the
`content-calendar` skill. **Ideas + talking points only — not posts.** Nothing
here goes external until it's expanded into the bank and reviewed.

Two domains, alternating by day, 4 fixed pillars per domain (see the skill
for pillar definitions). CTA is fixed per domain, not improvised per row.

Each day has a **hook** (the headline claim) and **3 talking points** — the
specific things to actually say, in order, so recording/writing doesn't turn
into rambling. Talk through the 3 points in order, land the CTA, done. These
are not a script to read verbatim — they're the skeleton that keeps you on topic.

Mark a day `[expanded YYYY-MM-DD]` once it's been written into `content-bank.md`.

## 2026-06-23 — 2026-07-22

### Day 1 — 2026-06-23 — SeanBuilds — Build log
**Hook:** Built a Remotion render engine for creative-os after HyperFrames kept crashing on HDR footage.
1. The problem: HyperFrames' `capture_hdr_layered` render path kept throwing "Target closed" errors on HDR-tagged footage — repeatedly, not once.
2. What I did instead of debugging forever: scaffolded a parallel Remotion project rather than ripping out HyperFrames entirely — different tool for a different job.
3. The number that made the call obvious: same clip, HyperFrames ~12+ minutes (when it didn't crash), Remotion under 5.
**CTA:** Comment "render" or DM me

### Day 2 — 2026-06-24 — Vulnaguard — CMMC myth
**Hook:** CMMC audits don't usually fail because of bad intentions.
1. The real failure mode: evidence scattered across six different folders/drives, nobody can produce it fast enough when the assessor asks.
2. Why this keeps happening: most contractors treat "we have the controls" and "we can prove we have the controls in 30 seconds" as the same thing. They're not.
3. What Sentinel does about it: keeps the evidence in one place, always audit-ready, instead of reconstructed under deadline pressure.
**CTA:** vulnaguard.com

### Day 3 — 2026-06-25 — SeanBuilds — Mistake/lesson
**Hook:** AfterSwing was reporting a "real" metric that was actually two unrelated heuristics ANDed together.
1. The specific bug: `outToInPath` was literally `steepShaft AND swayOffBall` — two crude proxies pretending to be swing-path analysis.
2. How I caught it: read my own code with fresh eyes instead of trusting that it worked because the app ran without errors.
3. What changed: ripped it out, replaced it with three metrics I could actually defend from real pose data — tempo ratio, lateral sway in inches, posture change in degrees.
**CTA:** Comment "honest" or DM me

### Day 4 — 2026-06-26 — Vulnaguard — Behind Sentinel
**Hook:** Sentinel doesn't just show you a compliance score — it shows you which control is about to bite you.
1. The gap with most CMMC tools: a dashboard number tells you where you stand today, not what's about to break.
2. What Sentinel surfaces instead: the specific control trending toward failure and why, before it's a finding.
3. Why that's the real difference: passing an audit vs. actually being secure are not the same outcome, and most tools only optimize for the first one.
**CTA:** vulnaguard.com

### Day 5 — 2026-06-27 — SeanBuilds — Tool I actually use
**Hook:** My content bank doesn't write itself — it stops me from staring at a blank page.
1. The actual problem it solves: not "I have nothing to say," it's "I have too much to say and no system for picking what's next."
2. How it works day to day: calendar generates the idea, I expand it into a draft only when I'm ready to actually write, bank holds it until posting day.
3. The principle behind it: automate the boring 80% (deciding what to talk about), keep the judgment call (how to say it) manual.
**CTA:** Comment "bank" or DM me

### Day 6 — 2026-06-28 — Vulnaguard — SEO agent in action
**Hook:** The SEO agent now runs the audit I used to do by hand every month.
1. What used to happen: manually checking meta tags, broken links, the unglamorous stuff that quietly tanks rankings.
2. What changed: that whole pass is automated now, and it catches things consistently instead of whenever I had a free Friday.
3. The actual ROI: it's not about saving time on the audit, it's about the audit actually happening every month instead of slipping.
**CTA:** vulnaguard.com

### Day 7 — 2026-06-29 — SeanBuilds — Contrarian take
**Hook:** Everyone's selling fully autonomous agents. I shipped mine at L2 — drafts, not auto-publish — on purpose.
1. The temptation: jump straight to "agent does everything," because that's what sounds impressive.
2. Why I didn't: every post I publish still gets a human read before it goes out — that's a hard rule, not a placeholder until the agent gets better.
3. The actual lesson: most workflows don't need the top autonomy level yet — they need the boring middle level proven first.
**CTA:** Comment "L2" or DM me

### Day 8 — 2026-06-30 — Vulnaguard — Credibility
**Hook:** CompTIA PenTest+ and a master's in computer forensics — not to sound smart, but because of where they point.
1. What pen-testing actually teaches: think like the person trying to break in, so you know where they'd start.
2. What forensics actually teaches: assume the evidence is incomplete until you've proven otherwise — don't trust a clean-looking record.
3. How that shows up in the product: Sentinel is built by someone who's looked for the gap an assessor would find, not someone guessing what compliance "probably" requires.
**CTA:** vulnaguard.com

### Day 9 — 2026-07-01 — SeanBuilds — Build log
**Hook:** Spent a session ripping fake swing-path and face-angle numbers out of AfterSwing's pose pipeline.
1. The trigger: a real weekend test with real people coming up — couldn't ship numbers I couldn't defend.
2. The hard call: full swing-path/face-angle biomechanics from one 2D camera isn't honestly buildable in days — chose narrower-but-real over impressive-but-fake.
3. What shipped instead: tempo ratio, lateral sway, posture change — three metrics computed from actual measured joints, not heuristics.
**CTA:** Comment "swing" or DM me

### Day 10 — 2026-07-02 — Vulnaguard — CMMC myth
**Hook:** A passing score on a CMMC checklist tool doesn't mean you're secure.
1. What a checklist score actually measures: whether you answered the questions, not whether the underlying control holds up.
2. Where that gap shows up: the moment an assessor asks for the evidence behind the answer, not the answer itself.
3. The reframe: CMMC readiness is a state you maintain, not a score you hit once.
**CTA:** vulnaguard.com

### Day 11 — 2026-07-03 — SeanBuilds — Mistake/lesson
**Hook:** video-website-agent sat for days as a templates folder with zero actual templates inside it.
1. The trap: it looked finished — folder structure, README, naming all in place — but there was nothing reusable in it.
2. What actually had the working logic: a different repo (`ai-shovel-video`) had 5 real compositions, hardcoded to one specific video.
3. The fix: extracted those 5 into proper parameterized templates with a CONFIG separating structure from per-video content.
**CTA:** Comment "scaffold" or DM me

### Day 12 — 2026-07-04 — Vulnaguard — Behind Sentinel
**Hook:** Every Sentinel feature traces back to one question: where did the evidence live last time, and why couldn't we find it in time.
1. The origin of that question: watching real audit prep scramble to reconstruct evidence trails that should've already existed.
2. How that shapes the roadmap: features get prioritized by "does this close a gap an assessor would actually find," not by what's easy to build.
3. The outcome: a tool built from the audit's point of view, not the vendor's point of view.
**CTA:** vulnaguard.com

### Day 13 — 2026-07-05 — SeanBuilds — Tool I actually use
**Hook:** I don't trust an agent to publish anything externally without me reading it first.
1. Where this rule lives: every post, every client email, every external-facing draft gets a human pass before it ships — written into how the whole system works, not an afterthought.
2. Why it's not a bottleneck: the agent still does the drafting, the adapting per platform, the queuing — review is the one step that stays manual.
3. What it protects: voice, accuracy, and the fact that "AI wrote this and nobody checked" is exactly the kind of mistake that's expensive to walk back.
**CTA:** Comment "review" or DM me

### Day 14 — 2026-07-06 — Vulnaguard — SEO agent in action
**Hook:** Google Search Console data feeds straight into the SEO agent now.
1. What changed: it's not guessing at what's ranking or estimating traffic — it's reading the real query/ranking data straight from Google.
2. Why that matters: recommendations are only as good as the data behind them, and most SEO advice online is generic because it isn't tied to your actual numbers.
3. What it unlocks: the agent can point at a specific page, specific query, specific drop — not "improve your SEO" in the abstract.
**CTA:** vulnaguard.com

### Day 15 — 2026-07-07 — SeanBuilds — Contrarian take
**Hook:** AI didn't make me ship faster by doing my job for me.
1. The common claim: AI replaces the work.
2. What actually happened: it finished the parts of my job I was already bad at finishing — the boring middle steps that used to stall a project for days.
3. The distinction that matters: speed came from closing gaps in my own process, not from outsourcing judgment.
**CTA:** Comment "finish" or DM me

### Day 16 — 2026-07-08 — Vulnaguard — Credibility
**Hook:** Forensics teaches you to assume the evidence is incomplete until proven otherwise.
1. Where that mindset comes from: a forensics investigation never assumes a clean record means nothing happened — you verify, you don't assume.
2. How Sentinel inherits that: every compliance claim gets treated as needing proof, not just a checkbox.
3. Why that's the opposite of how most compliance tools work: most are built to confirm you did the paperwork, not to stress-test whether the paperwork is true.
**CTA:** vulnaguard.com

### Day 17 — 2026-07-09 — SeanBuilds — Build log
**Hook:** My caption-overlay graphics were landing right on the speaker's face in talking-head clips.
1. How it got caught: ran the same clips through the new pipeline and immediately saw text covering the person talking.
2. The fix: built a CornerCard component — beat graphics moved to the upper-right corner instead of dead center.
3. The extra mile: added a slide-rotate-pop entrance and fade-out exit, because the ask wasn't just "fix the overlap," it was "make it feel more alive."
**CTA:** Comment "corner" or DM me

### Day 18 — 2026-07-10 — Vulnaguard — CMMC myth
**Hook:** Most contractors treat CMMC as a one-time event.
1. The misconception: pass the assessment once, move on, compliance is "done."
2. The reality: CMMC determines whether you keep the contract at renewal too — it's a maintained state, not a finish line.
3. What that means practically: the systems and evidence trails need to survive continuously, not just for assessment week.
**CTA:** vulnaguard.com

### Day 19 — 2026-07-11 — SeanBuilds — Mistake/lesson
**Hook:** "Phase detection" was running on fixed time percentages instead of the actual wrist movement in the video.
1. What was actually happening: address/takeaway/top/downswing/impact were just fixed percentage buckets, applied identically to every single swing.
2. Why that's wrong: every swing got graded against a clock, not against itself — two completely different swings got the same phase boundaries.
3. The fix: phase boundaries now come from actual wrist-height extrema in the real video data.
**CTA:** Comment "phases" or DM me

### Day 20 — 2026-07-12 — Vulnaguard — Behind Sentinel
**Hook:** I built Sentinel's evidence tracking the way I'd want it built if I were staring down an assessor's deadline at 11pm.
1. The framing that drives the design: build for the person under pressure, not the person doing a calm demo.
2. What that looks like in practice: evidence findable in seconds, not buried three folders deep.
3. The test I hold features to: would this actually help at 11pm the night before, or does it just look good in a screenshot.
**CTA:** vulnaguard.com

### Day 21 — 2026-07-13 — SeanBuilds — Tool I actually use
**Hook:** Buffer is the thing that lets my posting queue not care which platform it's going to.
1. The problem before: writing platform-specific versions of every post by hand, every time.
2. How it works now: one piece of text, adapted once per platform (LinkedIn long-form, Facebook trimmed, Instagram caption + image flag), queued through Buffer.
3. The one step that stays manual: the platform-adaptation judgment call and the final review — Buffer just removes the busywork around it.
**CTA:** Comment "buffer" or DM me

### Day 22 — 2026-07-14 — Vulnaguard — SEO agent in action
**Hook:** The SEO agent's outreach piece still needs a real send-batch fix before it runs unattended.
1. Being honest about the gap: automation isn't done just because most of it works — the scheduled-send piece still needs a Vercel Cron fix.
2. Why I'm not shipping around it: an outreach pipeline that silently fails to send is worse than one that requires a manual nudge.
3. The principle: automating the boring part doesn't mean skipping the part that has to actually work reliably.
**CTA:** vulnaguard.com

### Day 23 — 2026-07-15 — SeanBuilds — Contrarian take
**Hook:** A real metric you can defend beats an impressive-sounding one you can't.
1. The temptation in any build: report the number that sounds most sophisticated, even if it's shaky underneath.
2. The AfterSwing example: swing-path and face-angle sound more "real" than tempo ratio and lateral sway — but only the second set was honestly measurable with the camera setup I had.
3. The actual standard: would I be comfortable explaining exactly how this number was calculated to the person relying on it.
**CTA:** Comment "honest-data" or DM me

### Day 24 — 2026-07-16 — Vulnaguard — Credibility
**Hook:** Pen-testing teaches you to think like the person trying to break in.
1. The mindset: assume someone is actively looking for the gap, not just hoping nobody finds it.
2. How that translates to compliance: compliance work is mostly about making sure that person has nowhere good to start.
3. Why that's different from "checking boxes": boxes get checked by people who've never had to think offensively about their own systems.
**CTA:** vulnaguard.com

### Day 25 — 2026-07-17 — SeanBuilds — Build log
**Hook:** Wired an IndieHackers branch into my posting pipeline this week.
1. The gap it closes: same content bank, but IndieHackers needs a longer-form, conversational, build-log register — not a trimmed social caption.
2. The constraint: no posting API for IndieHackers, so the pipeline stops at a reviewed draft and hands off for me to copy/paste/submit manually.
3. Why build it anyway: getting the draft written and reviewed is the actual bottleneck — the manual paste step is cheap once that's done.
**CTA:** Comment "indiehackers" or DM me

### Day 26 — 2026-07-18 — Vulnaguard — CMMC myth
**Hook:** "We'll deal with compliance after we win the contract" kills more bids than any technical gap.
1. Why that sentence is the real risk: compliance readiness has a lead time — you can't retrofit it under a contract deadline.
2. What actually happens to contractors who wait: they either lose the bid on the compliance requirement or scramble expensively right when they should be executing the contract.
3. The reframe: compliance prep is part of being bid-ready, not a follow-up task after winning.
**CTA:** vulnaguard.com

### Day 27 — 2026-07-19 — SeanBuilds — Mistake/lesson
**Hook:** Bid alerts I needed were bouncing as "Undeliverable" behind a mail-forwarding rule nobody was watching.
1. What was happening silently: solicitation emails relevant to active CMMC gov contract work were never reaching the inbox they were forwarded to.
2. How it got found: by accident, not by any monitoring — which is the actual problem.
3. The lesson: a forwarding rule is infrastructure, and infrastructure that fails silently is worse than infrastructure that doesn't exist.
**CTA:** Comment "bounce" or DM me

### Day 28 — 2026-07-20 — Vulnaguard — Behind Sentinel
**Hook:** Sentinel exists because "audit-ready" turned into a Slack thread, a shared drive, and someone's memory.
1. What that actually looks like in most orgs: compliance evidence scattered across tools that were never meant to be the system of record.
2. Why none of those survive an audit: an assessor doesn't accept "ask Dave, he remembers where that is."
3. What Sentinel replaces it with: one place, durable, that doesn't depend on anyone's memory.
**CTA:** vulnaguard.com

### Day 29 — 2026-07-21 — SeanBuilds — Tool I actually use
**Hook:** My decision log is the most useful file in this whole repo.
1. What it actually holds: not the code, but the record of why each call was made — the constraint, the alternative considered, the reason one won.
2. Why that beats the code as documentation: code shows what exists today, the log shows why it exists and what was rejected.
3. How it gets used: before redoing or second-guessing a past decision, check the log first — it's usually already been thought through.
**CTA:** Comment "log" or DM me

### Day 30 — 2026-07-22 — Vulnaguard — SEO agent in action
**Hook:** Every solicitation alert now flows into one lead inbox instead of getting buried under 40 other unread subject lines.
1. The before state: bid/solicitation emails mixed into a general inbox, easy to miss among everything else.
2. What changed: a dedicated triage flow pulls agency, location, and contract details out of solicitation emails into a staging table built for outreach.
3. Why that matters for the business: gov contract leads have short windows — a system that surfaces them fast beats one that relies on noticing them in time.
**CTA:** vulnaguard.com

## Archive

(none yet)
