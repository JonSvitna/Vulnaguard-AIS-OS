import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { REPOS, OUTPUT_REPO, COMMIT_LOOKBACK } from './config.js';
import { cloneShallow, commitsSince, diffFor, headSha, readStateFile, writeStateFile, commitAndPush } from './git.js';
import { extractFromCommit } from './extract.js';
import { screenshotHomepage } from './screenshot.js';

function todayStamp() {
  return new Date().toISOString().slice(0, 10);
}

function formatEntry(entry, repo, commit) {
  const lines = [
    `### [unused] ${todayStamp()} — ${entry.slug}`,
    `**Domain:** ${repo.domain}`,
    `**Pillar guess:** ${entry.pillarGuess}`,
    `**Source:** commit ${commit.shortHash} in ${repo.name}`,
    `**Hook:** ${entry.hook}`,
    '**Talking points:**',
    ...entry.talkingPoints.map((p, i) => `${i + 1}. ${p}`),
  ];
  if (entry.screenshotPath) {
    lines.push(`**Screenshot:** ${entry.screenshotPath}`);
  }
  lines.push('**Status:** unused');
  return lines.join('\n');
}

export async function runHermesScan() {
  console.log('[hermes-cron] scan starting', new Date().toISOString());

  const outputDir = cloneShallow(OUTPUT_REPO.github, 5);
  const state = readStateFile(outputDir);
  const stagedEntries = [];
  const newState = { ...state };

  for (const repo of REPOS) {
    let repoDir;
    try {
      repoDir = cloneShallow(repo.github);
    } catch (err) {
      console.error(`[hermes-cron] clone failed for ${repo.name}:`, err.message);
      continue;
    }

    const sinceSha = state[repo.name];
    const commits = commitsSince(repoDir, sinceSha, COMMIT_LOOKBACK);
    if (commits.length === 0) continue;

    for (const commit of commits) {
      const diff = diffFor(repoDir, commit.hash);
      let result;
      try {
        result = await extractFromCommit({ subject: commit.subject, diff });
      } catch (err) {
        console.error(`[hermes-cron] extraction failed for ${commit.shortHash}:`, err.message);
        continue;
      }
      if (!result.worthy) continue;

      if (repo.liveUrl) {
        const path = await screenshotHomepage(repo.liveUrl, outputDir, result.slug);
        if (path) result.screenshotPath = path;
      }

      stagedEntries.push({ markdown: formatEntry(result, repo, commit), domain: repo.domain });
    }

    newState[repo.name] = headSha(repoDir);
  }

  writeStateFile(outputDir, newState);

  if (stagedEntries.length > 0) {
    const pendingDir = join(outputDir, 'references', 'hermes-pending');
    mkdirSync(pendingDir, { recursive: true });
    const filename = `pending-${todayStamp()}-${Date.now()}.md`;
    const grouped = { Vulnaguard: [], SeanBuilds: [] };
    for (const e of stagedEntries) grouped[e.domain].push(e.markdown);

    const body = [
      `# Hermes pending — ${todayStamp()}`,
      '',
      'Auto-staged by the hermes-cron Railway service. Review and merge worthwhile entries into `references/hermes-opportunities.md`, then delete this file.',
      '',
      ...(grouped.Vulnaguard.length ? ['## Vulnaguard', '', ...grouped.Vulnaguard.flatMap((m) => [m, ''])] : []),
      ...(grouped.SeanBuilds.length ? ['## SeanBuilds', '', ...grouped.SeanBuilds.flatMap((m) => [m, ''])] : []),
    ].join('\n');

    writeFileSync(join(pendingDir, filename), body);
    console.log(`[hermes-cron] staged ${stagedEntries.length} entries in ${filename}`);
  } else {
    console.log('[hermes-cron] no content-worthy commits this run');
  }

  const pushed = commitAndPush(outputDir, `hermes-cron: scan run (${stagedEntries.length} new entries)`);
  console.log(`[hermes-cron] scan complete, pushed=${pushed}`);
}
