# AIS-OS Intake

This is the source-of-truth file for your AIOS. Fill it in by typing, voice-pasting (Wispr Flow / OS dictation), or running `/onboard` for a guided conversation. Whichever mode, this file is what `/onboard` reads to scaffold your Day-1 setup.

**Hard cap: 7 questions.** Each answerable in under 60 seconds. Don't overthink — you can edit and re-run `/onboard` any time.

---

## Q1 — Who are you, what do you sell, who do you sell it to?

Identity, offer, ICP. One paragraph each is fine.

```
I serve people who need software or website builds — mainly. It's my passion, plus it gives me the opportunity to learn new technology. I've built and shipped a wide range of applications: some were learning lessons, some were practical. Recent projects are tools to either help myself (the SEO agent) or client websites, but my BABY is Sentinel CMMC. I have a diverse background in hacking (CompTIA PenTest+) and information security, a Master's in Computer Forensics, and a BS in Computer Networking. I love working with tech and learning how to implement and simplify complex processes.

What I most enjoy building, creatively, is SaaS products — not agentic flows. I'm familiar with and use both, but SaaS is the primary craft; agents/automation are tools I reach for to take workload off myself as a solo developer/solo entrepreneur.
```

---

## Q2 — Paste 1-2 things you've written recently. Don't edit them.

An email, a LinkedIn post, a DM, a doc — anything that sounds like you when you're not trying. **Paste verbatim.** Do not type these mid-conversation with Claude — chat-shaped samples are worse than no samples (voice contamination).

```
Satisfied by an installed skill instead of raw paste: .claude/skills/seanbuilds-voice/SKILL.md
("SeanBuilds Voice & Persona" — covers SeanBuilds, Vulnaguard, Mectofitness, BlueAlamo.
Builder-explaining-it-over-coffee register. Banned words list, storytelling arc
(Situation -> Frustration -> Observation -> Build -> Result), per-channel format rules.)
```

---

## Q3 — What are your 2-3 biggest priorities for the next 90 days?

Quarterly priorities. Not yearly aspirations. Things that, if not done by July, would make you say "I wasted Q2."

```
1. Complete Sentinel CMMC certification — hard deadline driven by government agency contract requirements.
2. Secure up to 10 clients via the SEO platform — outreach feature built and automated end-to-end.
3. Drive consistent feeds/traffic to the website via the SEO optimization agent.

(Underlying theme: solo developer/solo entrepreneur — automation that takes workload off is a standing ask, not just for these three.)
```

---

## Q4 — Where does revenue actually land, and where is it tracked?

Multiple answers OK. Stripe? Skool? GoHighLevel? QuickBooks? A spreadsheet?

```
[Your answer here]
```

---

## Q5 — Where do you talk to customers, your team, and the outside world day-to-day?

Email (which one — Gmail / Outlook)? Slack? Teams? DMs (Skool / Discord / iMessage)? Phone?

```
[Your answer here]
```

---

## Q6 — Where do meeting recordings, notes, and important docs live?

Granola? Otter? Fireflies? Google Drive? Notion? Dropbox? A folder on your desktop you keep meaning to organize?

```
[Your answer here]
```

---

## Q7 — What's the one task that eats your week, and where do you currently track work?

The single biggest time-suck or recurring drudgery. Plus where tasks/projects live (ClickUp / Asana / Linear / Notion / a notebook).

```
[Your answer here]
```

---

When this file is filled, run `/onboard` (or re-run it) and the wizard will scaffold your Day-1 file set: `context/`, `references/voice.md`, populated `connections.md`, and a filled `CLAUDE.md`.
