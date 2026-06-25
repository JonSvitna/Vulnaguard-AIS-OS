# Website Creation Tool — Architecture & AI Integration

**Date:** 2026-06-24  
**Status:** Phase 0 complete (scaffolding), Phase 1 design (AI architecture pending)  
**Owner:** Sean + Copilot

---

## Current Architecture (Phase 0 ✅)

### Stack
- **Frontend:** Next.js 15 + TypeScript on Vercel
- **Backend:** Next.js API routes on Vercel
- **Database:** PostgreSQL on Railway (Drizzle ORM)
- **Auth:** NextAuth.js (GitHub/Google OAuth)
- **Code Generation:** ts-morph (React components), Style Dictionary (design tokens)
- **GitHub Integration:** Octokit (create repos, push files)
- **UI Components:** shadcn/ui + Tailwind CSS

### File Structure
```
vulnaguard-website-creation-tool/
├── app/
│   ├── api/auth/[...nextauth]/       # OAuth
│   ├── api/projects/                 # Project CRUD
│   ├── api/generate/config           # Token → Tailwind
│   ├── api/generate/components       # Component codegen
│   ├── api/export/github             # GitHub push
│   ├── login/page.tsx
│   ├── page.tsx
│   └── layout.tsx
├── db/
│   ├── schema.ts                     # Users + Projects
│   ├── client.ts
│   └── migrations/
├── lib/
│   ├── auth.ts
│   ├── design-tokens.ts              # Token generation
│   ├── codegen.ts                    # Component code gen
│   └── github.ts                     # GitHub ops
├── brands/                           # Copied from design-system/brands/
│   └── seanbuilds.tokens.json
└── [config files]
```

### Design System Integration
- **Source:** `design-system/brands/*.tokens.json` (copied as reference)
- **Token Format:** See design-system/PROCESS.md
  - `color.*` (background, surface, accent, text variants)
  - `radius.*` (card, pill)
  - `shadow.*` (glow, radial gradients)
  - `type.*` (eyebrow, display, h2, body — size, weight, leading, tracking)
  - `taste_skill_dials` (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, notes)

### API Routes (Ready)
- `POST /api/projects` — create project
- `POST /api/generate/config` — Tailwind config from tokens
- `POST /api/generate/components` — React component library
- `POST /api/export/github` — create GitHub repo + push files

---

## Phase 1: Multi-Model AI Integration (Pending)

### Vision
Vercel tool becomes an **AI-powered design assistant**. Users can:
1. Generate website from tokens (Phase 0)
2. Ask AI to suggest improvements ("make this bolder", "add motion")
3. AI iterates design tokens + components
4. Fallback cascade: Claude → OpenAI → fallback model
5. Session limit tracking (don't burn quota)

### Open Architecture Questions (To be decided)

**1. AI Capabilities — ANSWERED 2026-06-24:**
- All three: generate component code suggestions, suggest design improvements (given taste_skill_dials), iterate on tokens from feedback.
- **Plus image generation:** AI layer also calls OpenAI's Images API (gpt-image-1) for visuals — same pattern as [[feedback_design_visuals]] (ChatGPT/OpenAI handles aesthetics, Claude handles structure/code). Generated images get pulled back into the project and become editable/iterable like any other asset. Note: this is OpenAI's Images API, not a literal "ChatGPT" MCP server — there isn't one; the API achieves the same outcome.

**2. Session Limits Strategy:** — still open, decide when building
- Track Claude usage (tokens/month)?
- Track OpenAI usage (incl. image gen cost — billed per image, track separately from text tokens)?
- Rate limit per user/hour?
- Cost tracking (log to db)?

**3. Model Cascade:** — still open, decide when building
- Model 1: Claude Sonnet (best quality, highest cost)
- Model 2: GPT-4 Turbo (fallback if Claude rate-limited)
- Model 3: Claude Haiku or GPT-4 Mini (cheapest fallback)?
- Retry logic: exponential backoff, 3x total tries?
- Image generation isn't part of this cascade — it's a dedicated OpenAI Images API call, not a fallback chain.

**4. Scope of "Modify Websites" — ANSWERED 2026-06-24:**
- Tokens + components for now. Live HTML/CSS editing not in scope yet.

**5. App's own UI — NEW, 2026-06-24:**
- The website-creation-tool's own Vercel frontend should be designed using the design-system (`design-system/brands/`), same as anything it generates for clients. Sean wants to see the design-system applied to the tool itself before/alongside building client-facing output.

**6. Content loop — NEW, 2026-06-24:**
- Hermes agent should treat this build as a content source (storyboard/content-calendar feeder) — confirmed, not just a one-off note.

**5. Implementation Pattern:**
- New API route: `POST /api/ai/suggest` (takes project + user feedback)
- New API route: `POST /api/ai/iterate` (refine based on AI suggestions)
- New lib: `lib/ai-client.ts` (multi-model abstraction)
- New tracking: `db/schema.ts` adds `aiSessions` table (log usage)

---

## Next Steps (Pickupable on Another PC)

### Before Building Phase 1:
1. **Clarify AI architecture** (see questions above)
2. **Set up API keys:**
   - `ANTHROPIC_API_KEY` (Claude)
   - `OPENAI_API_KEY` (GPT-4)
   - `FALLBACK_MODEL_KEY` (if third model)
3. **Add to .env.example**
4. **Design aiSessions table** (for usage tracking)

### Implementation Checklist (Phase 1):
- [ ] Create `lib/ai-client.ts` (multi-model abstraction layer)
- [ ] Add aiSessions table to `db/schema.ts`
- [ ] Implement Claude + OpenAI clients with retry logic
- [ ] Create `POST /api/ai/suggest` route
- [ ] Create `POST /api/ai/iterate` route
- [ ] Wire session limit tracking + cost logging
- [ ] Frontend: "Get AI Suggestions" button + feedback form
- [ ] Frontend: "Apply AI Changes" modal
- [ ] Test cascade (Claude → OpenAI → fallback)

### Deployment Checklist:
- [ ] Railway PostgreSQL + migrations
- [ ] Vercel environment variables
- [ ] GitHub OAuth app setup
- [ ] Test local dev loop
- [ ] End-to-end test (create project → AI suggests → export to GitHub)

---

## Key Files to Update on Next PC

1. **vulnaguard-website-creation-tool/.env.example**
   - Add ANTHROPIC_API_KEY, OPENAI_API_KEY, FALLBACK_MODEL_KEY

2. **vulnaguard-website-creation-tool/lib/ai-client.ts** (new)
   - Multi-model abstraction
   - Retry logic
   - Session tracking

3. **vulnaguard-website-creation-tool/db/schema.ts**
   - Add aiSessions table (userId, model, prompt, response, tokens_used, cost, timestamp)

4. **vulnaguard-website-creation-tool/app/api/ai/** (new folder)
   - suggest/route.ts
   - iterate/route.ts

5. **Vulnaguard-AIS-OS/references/website-creation-tool-architecture.md** (this file)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ vulnaguard-website-creation-tool (Vercel)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (React)                                          │
│  ├── Dashboard (list projects)                            │
│  ├── Token Editor (colors, type, spacing)                │
│  ├── Component Preview (Tailwind)                        │
│  ├── "Get AI Suggestions" button ← NEW                  │
│  └── "Apply Changes" modal ← NEW                        │
│                                                           │
│  API Routes                                              │
│  ├── /api/projects/route.ts                             │
│  ├── /api/generate/config/route.ts                      │
│  ├── /api/generate/components/route.ts                 │
│  ├── /api/export/github/route.ts                       │
│  ├── /api/ai/suggest/route.ts ← NEW                    │
│  └── /api/ai/iterate/route.ts ← NEW                    │
│                                                          │
│  Libraries                                              │
│  ├── lib/auth.ts (NextAuth)                            │
│  ├── lib/design-tokens.ts (token parsing)              │
│  ├── lib/codegen.ts (component generation)            │
│  ├── lib/github.ts (GitHub ops)                       │
│  └── lib/ai-client.ts ← NEW (multi-model AI)         │
│                                                         │
│  Database (Railway PostgreSQL)                        │
│  ├── users (via NextAuth)                             │
│  ├── projects (design systems)                        │
│  └── aiSessions (AI usage tracking) ← NEW             │
│                                                        │
└────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ External Services                                       │
├─────────────────────────────────────────────────────────┤
│ Claude API (Anthropic)                                │
│ GPT-4 API (OpenAI)                                    │
│ Fallback Model API (TBD)                              │
│ GitHub API (Octokit) — create repos, push files      │
│ Design System Reference (design-system/brands/)      │
└─────────────────────────────────────────────────────────┘
```

---

## Decision: Why This Architecture?

- **Standalone + Design System Reference:** No coupling to creative-os. Uses design-system tokens as data layer.
- **Multi-model AI:** Provides redundancy (if Claude is rate-limited, fall back to OpenAI), cost optimization (cheap fallback for simple tasks), and flexibility.
- **Session Tracking:** Prevents surprise bills, tracks which models/users consume quota.
- **Vercel + Railway:** Cost-efficient, fast iteration, GitHub-native deployment.

---

## Handoff Notes for Next PC

1. **This file is your map.** Read it again before starting Phase 1.
2. **Design system integration is DONE** — tokens.json is copied, codegen respects taste_skill_dials.
3. **Phase 1 is scoped but not built** — answer the open questions first.
4. **All infrastructure is ready** — just needs AI layer + UI.
5. **Test locally before deploying** — `npm run dev` should work once you fill .env.local.

**Ready to pick up?** Answer the Phase 1 questions first, then build the AI client layer.
