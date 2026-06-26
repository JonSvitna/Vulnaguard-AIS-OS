// Same allowlist as .claude/agents/hermes.md — keep the two in sync if it changes.
export const REPOS = [
  { name: 'Sentinel-CMMC', github: 'JonSvitna/Sentinel-CMMC', domain: 'Vulnaguard', liveUrl: 'https://sentinel-cmmc.vercel.app/' },
  { name: 'vulnaguard-seo-agent', github: 'JonSvitna/vulnaguard-seo-agent', domain: 'Vulnaguard', liveUrl: 'https://vulnaguard-seo-agent.vercel.app/' },
  { name: 'AfterSwing', github: 'JonSvitna/AfterSwing', domain: 'SeanBuilds', liveUrl: null },
  { name: 'creative-os', github: 'JonSvitna/creative-os', domain: 'SeanBuilds', liveUrl: null },
];

export const OUTPUT_REPO = { name: 'Vulnaguard-AIS-OS', github: 'JonSvitna/Vulnaguard-AIS-OS' };

export const ANTHROPIC_MODEL = process.env.HERMES_MODEL || 'claude-sonnet-4-6';
export const INTERVAL_HOURS = Number(process.env.HERMES_INTERVAL_HOURS) || 24;
export const COMMIT_LOOKBACK = 30; // fallback when a repo has no recorded last-scanned SHA
