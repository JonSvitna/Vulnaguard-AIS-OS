import { execSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

function authedUrl(githubPath) {
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error('GITHUB_TOKEN is not set');
  return `https://x-access-token:${token}@github.com/${githubPath}.git`;
}

export function cloneShallow(githubPath, depth = 60) {
  const dir = mkdtempSync(join(tmpdir(), 'hermes-'));
  execSync(`git clone --depth ${depth} --quiet ${authedUrl(githubPath)} ${dir}`, { stdio: 'pipe' });
  return dir;
}

export function commitsSince(dir, sinceSha, fallbackCount = 20) {
  const fmt = '%H%x1f%s';
  const args = sinceSha ? `${sinceSha}..HEAD` : `-n ${fallbackCount}`;
  const raw = execSync(`git -C ${dir} log ${args} --pretty=format:${fmt}`, {
    encoding: 'utf8',
  }).trim();
  if (!raw) return [];
  return raw.split('\n').map((line) => {
    const [hash, subject] = line.split('\x1f');
    return { hash, shortHash: hash.slice(0, 7), subject };
  });
}

export function diffFor(dir, hash) {
  try {
    return execSync(`git -C ${dir} show --stat --patch ${hash}`, { encoding: 'utf8', maxBuffer: 1024 * 1024 }).slice(0, 8000);
  } catch {
    return '';
  }
}

export function headSha(dir) {
  return execSync(`git -C ${dir} rev-parse HEAD`, { encoding: 'utf8' }).trim();
}

export function readStateFile(aisOsDir) {
  const path = join(aisOsDir, 'services/hermes-cron/state.json');
  if (!existsSync(path)) return {};
  return JSON.parse(readFileSync(path, 'utf8'));
}

export function writeStateFile(aisOsDir, state) {
  const path = join(aisOsDir, 'services/hermes-cron/state.json');
  writeFileSync(path, JSON.stringify(state, null, 2) + '\n');
}

export function commitAndPush(aisOsDir, message) {
  execSync(`git -C ${aisOsDir} add -A`, { stdio: 'pipe' });
  const status = execSync(`git -C ${aisOsDir} status --porcelain`, { encoding: 'utf8' });
  if (!status.trim()) return false;
  execSync(`git -C ${aisOsDir} -c user.email="hermes-cron@railway" -c user.name="hermes-cron" commit --quiet -m ${JSON.stringify(message)}`, {
    stdio: 'pipe',
  });
  execSync(`git -C ${aisOsDir} push --quiet origin HEAD:main`, { stdio: 'pipe' });
  return true;
}
