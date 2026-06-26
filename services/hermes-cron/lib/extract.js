import Anthropic from '@anthropic-ai/sdk';
import { ANTHROPIC_MODEL } from './config.js';

const PILLARS = [
  'Behind Sentinel — one real feature and the reason it exists',
  'CMMC myth or pain point contractors actually hit',
  'SEO agent in action — a specific thing it caught or automated',
  'Lesson from a mistake — what went wrong, what changed after',
  'Builder philosophy — how Sean thinks about building',
  'Before/after — a number that changed',
  'Client/web-dev friction fix',
  'Behind the build — process, tools, decisions',
];

const SYSTEM_PROMPT = `You are Hermes, a content-opportunity scanner for Sean's solo dev/founder build log (Sentinel CMMC, the SEO agent, AfterSwing, creative-os).

Given a single commit's message and diff, judge whether it is content-worthy: a real before/after, a mistake explicitly caught and fixed, a sharp number, a dramatic time-savings, a "removed X because Y" call. Most commits are noise (formatting, routine deps, merges, small refactors with no story) — reject those.

The "hook" must state the measurable result of the change, not just that something was broken. "Found and fixed a bug" is not a hook. State what's concretely better now — a number, a before/after, a capability that didn't exist a moment ago. If you cannot state what's measurably better as a result of this commit, reply {"worthy": false} even if the bug itself was interesting.

Reply with ONLY a JSON object, no prose, no markdown fences:
{"worthy": false} — if not content-worthy
or
{
  "worthy": true,
  "slug": "kebab-case-slug",
  "pillarGuess": "<one of the 8 pillars listed>",
  "hook": "one sentence, specific, states the measurable result — not just the bug",
  "talkingPoints": ["point 1", "point 2", "point 3"]
}

Pillars: ${PILLARS.join(' | ')}`;

export async function extractFromCommit({ subject, diff }) {
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const message = await client.messages.create({
    model: ANTHROPIC_MODEL,
    max_tokens: 500,
    system: SYSTEM_PROMPT,
    messages: [
      {
        role: 'user',
        content: `Commit message: ${subject}\n\nDiff (truncated):\n${diff}`,
      },
    ],
  });

  const text = message.content.map((b) => (b.type === 'text' ? b.text : '')).join('').trim();
  try {
    return JSON.parse(text);
  } catch {
    return { worthy: false };
  }
}
