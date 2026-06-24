# Website Creation Tool on Vercel — Architecture Plan

**Date:** 2026-06-24  
**Scope:** Design system generator + component builder, hosted on Vercel  
**Video editing:** Separate concern (local/Claude-driven), NOT part of this tool

---

## Vision

A design token → code pipeline. User inputs:
- Brand colors, typography, spacing, shadow system
- Component specs (buttons, cards, forms, layouts)
- Page templates

Tool outputs:
- Tailwind config or CSS-in-JS theme
- React component library (TypeScript)
- HTML/CSS static site or Next.js project
- Design tokens as JSON/YAML (portable)

**Scale:** Cost-efficient. Leverage Vercel's edge functions, serverless storage (Vercel KV or S3), and GitHub Actions for generation jobs.

---

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend** | Next.js App Router + TypeScript | Native Vercel, fast iteration, file-based routing |
| **UI Components** | Shadcn/ui + Tailwind CSS | Extensible, design-system-ready, open source |
| **State / Forms** | TanStack Query + React Hook Form | Handles async generation, form validation |
| **Design tokens** | Style Dictionary or token-transformer | Standard format, portable to figma-tokens, Storybook |
| **Code generation** | ts-morph or Codegen (GraphQL approach) | AST manipulation, reproducible output |
| **Hosting** | Vercel | Functions, Edge, KV store, GitHub integration |
| **Storage** | Vercel KV (Redis) + GitHub Gists or private repo | User projects, audit trail, version history |
| **Auth** | NextAuth.js (GitHub/Google) | Zero friction, OIDC-ready |
| **Exports** | npm package + zip download + GitHub repo push | Flexible delivery; use gh CLI for automation |

---

## Feasibility Check

### What's Easy ✅
- Design token input → Tailwind/CSS output (design-tokens libraries exist)
- Component code generation (ts-morph can template React components)
- React + Next.js on Vercel (native fit)
- User auth + project storage (NextAuth + KV)
- GitHub integration (push generated code to user repo)

### What's Hard ❌
- Real-time visual preview during design (would need a Figma/Penpot embed or custom canvas renderer)
- Live code editing + hot reload (doable but adds complexity)
- Video integration (SKIP — separate tool)

### Workaround: Preview-Driven Workflow
1. User inputs design tokens via form
2. Tool generates a static HTML/Tailwind preview site (cheap, hosted on Vercel edge)
3. User can download, fork, or push to GitHub
4. For visual iteration: link to Figma or Storybook (user can refine in Figma → re-export tokens → re-generate)

---

## MVP Scope (Week 1)

**Deliverables:**
1. Design token form (colors, typography, spacing, shadows)
2. Tailwind config generator (JSON out)
3. 5-10 base components (button, card, form input, modal, navbar)
4. React component export (TypeScript)
5. Static HTML demo site (Tailwind classes applied)
6. GitHub auth + project list/save
7. Export: Zip file with project, or push to GitHub

**Out of scope:**
- Visual builder / drag-and-drop
- Video editing
- Figma plugin
- Design token versioning (future)

---

## Video Editing Integration (Separate Tool)

**How it fits:**
- User generates website in Vercel tool
- If they want video content: prompt in the output ("💬 Add a video hero banner?")
- Clicking that button → launches Claude Code with a template prompt
- Claude Code opens locally (video-website-agent or custom video tool)
- Generate MP4, WebM, or frame sequence
- Return video file path / URL back to Vercel tool (or manual paste)
- Embed in generated site

**Architecture:**
```
[Vercel Website Tool] 
  → (output has video section stubs)
  → User clicks "Edit video"
  → Prompt launches Claude Code with video-website-agent context
  → User edits locally, commits to repo or exports MP4
  → Vercel tool consumes output, embeds in final site
```

---

## File Structure (Next.js)

```
website-creation-tool/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── callback/page.tsx
│   ├── (app)/
│   │   ├── dashboard/page.tsx          # Project list
│   │   ├── editor/[projectId]/page.tsx # Token editor
│   │   ├── preview/[projectId]/page.tsx # Live preview
│   │   └── export/[projectId]/route.ts # Download/GitHub push
│   ├── api/
│   │   ├── auth/[...nextauth]/route.ts
│   │   ├── projects/route.ts
│   │   ├── generate/tokens/route.ts
│   │   ├── generate/components/route.ts
│   │   └── export/github/route.ts
│   ├── layout.tsx
│   └── page.tsx                         # Landing
├── lib/
│   ├── design-tokens/
│   │   ├── generator.ts   # Tailwind config out
│   │   ├── validator.ts   # Schema validation
│   │   └── templates.ts   # Built-in palettes
│   ├── codegen/
│   │   ├── react-component.ts # ts-morph templates
│   │   ├── tailwind-config.ts
│   │   └── html-demo.ts
│   ├── storage/
│   │   ├── kv-client.ts    # Vercel KV wrapper
│   │   └── github-client.ts
│   └── auth.ts             # NextAuth config
├── components/
│   ├── TokenForm.tsx       # Design token inputs
│   ├── ComponentPreview.tsx # Live Tailwind preview
│   ├── CodeEditor.tsx      # Read-only code display
│   └── ExportModal.tsx
├── public/
│   └── ...
├── .env.local.example
└── package.json
```

---

## Implementation Phases

### Phase 0: Setup (Day 1)
- [ ] Next.js project scaffold (create-next-app)
- [ ] Vercel deployment + KV store provisioned
- [ ] NextAuth.js wired (GitHub OAuth)
- [ ] Basic dashboard (list/create project UI)

### Phase 1: Token Editor (Days 2-3)
- [ ] Design token form (colors, typography, spacing)
- [ ] Form validation + live Tailwind config preview
- [ ] Save project to KV store

### Phase 2: Component Generator (Days 4-5)
- [ ] Component template library (button, card, form, etc.)
- [ ] Code generation → React TypeScript
- [ ] Render preview (static HTML with Tailwind)

### Phase 3: Export (Days 6-7)
- [ ] Zip download (project files)
- [ ] GitHub push (via gh CLI + token)
- [ ] npm package export option

### Phase 4+: Refinements & Video Integration
- [ ] Figma → design tokens plugin
- [ ] Video editing integration (Claude Code prompt)
- [ ] Component versioning
- [ ] Storybook integration

---

## Decision Checkpoints

1. **Design token format:** Use open-source standard (Design Tokens Community Group format)? Yes.
2. **Code generation:** ts-morph or template strings? ts-morph (AST-safe).
3. **Video fallback:** Claude Code prompt + local rendering? Yes. Add link in export UI.
4. **Auth:** GitHub-only or Google too? GitHub + Google (lower friction for non-devs).
5. **Pricing / Limits:** Free tier? Start unlimited during beta, meter later (Vercel's serverless limits are the boundary).

---

## Next Steps

1. Create Next.js skeleton + Vercel setup
2. Write `lib/design-tokens/generator.ts` (Tailwind config builder)
3. Build `TokenForm` component
4. Set up NextAuth + KV storage
5. Test token → config → HTML preview pipeline

**Worst case fallback:** If Vercel functions get complex, use a local Express server on your DigitalOcean droplet for code generation, and Vercel calls it via API.
