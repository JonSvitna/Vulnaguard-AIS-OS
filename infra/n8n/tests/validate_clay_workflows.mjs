#!/usr/bin/env node
/**
 * Static validation for Clay n8n workflow JSON (Task 8).
 * Run: node infra/n8n/tests/validate_clay_workflows.mjs
 */

import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const n8nDir = join(__dirname, '..');

const INTAKE = 'clay-lead-intake.workflow.json';
const FINALIZER = 'clay-lead-finalizer.workflow.json';
const APPROVAL = 'clay-slack-approval.workflow.json';

const INLINE_SECRET = /(?:sk-|re_|xox[baprs]-)[A-Za-z0-9_-]{8,}/;
const EMAIL_SEND = /n8n-nodes-base\.emailSend|\/api\/marketing\/send(?:-batch)?\b|resend\.com/i;
const SEQUENCE_MUTATE =
  /PATCH\s*\/api\/marketing\/sequences|\/api\/marketing\/sequences\/|sequence_status\s*[:=]/i;

const failures = [];

function load(name) {
  const path = join(n8nDir, name);
  let raw;
  try {
    raw = readFileSync(path, 'utf8');
  } catch (err) {
    failures.push(`MISSING ${name}: ${err.message}`);
    return { raw: '', json: null, text: '' };
  }
  let json = null;
  try {
    json = JSON.parse(raw);
  } catch (err) {
    failures.push(`INVALID JSON ${name}: ${err.message}`);
  }
  return { raw, json, text: raw };
}

function assert(cond, msg) {
  if (!cond) failures.push(msg);
}

function nodeBlob(json) {
  return JSON.stringify(json ?? {});
}

function hasEnvOrCredentialRef(text) {
  return (
    /\$env\.[A-Z0-9_]+/.test(text) ||
    /\$vars\.[A-Z0-9_]+/.test(text) ||
    /"authentication"\s*:\s*"(?:predefinedCredentialType|genericCredentialType)"/.test(text) ||
    /credentials\s*:\s*\{/.test(text)
  );
}

// --- Intake ---
{
  const { text, json } = load(INTAKE);
  assert(text.includes('/api/marketing/leads/clay-batch'), `${INTAKE}: must POST clay-batch`);
  assert(!text.includes('import-confirm'), `${INTAKE}: must not call import-confirm`);
  assert(!INLINE_SECRET.test(text), `${INTAKE}: inline secret token detected`);
  assert(hasEnvOrCredentialRef(text), `${INTAKE}: secrets must be env/credential refs`);
  assert(/MARKETING_AUTOMATION_SECRET/.test(text), `${INTAKE}: Bearer secret ref required`);
  assert(/SEO_AGENT_BASE_URL/.test(text), `${INTAKE}: SEO_AGENT_BASE_URL ref required`);

  const allowList = [
    'clay_row_id',
    'batch_id',
    'company_name',
    'website',
    'contact_name',
    'title',
    'email',
    'location',
    'fit_score',
    'fit_reason',
    'recommended_service',
  ];
  for (const key of allowList) {
    assert(text.includes(key), `${INTAKE}: normalize must include ${key}`);
  }
  assert(!EMAIL_SEND.test(text), `${INTAKE}: must not send email`);
  assert(!SEQUENCE_MUTATE.test(text), `${INTAKE}: must not mutate sequence status`);
  assert(json?.name, `${INTAKE}: workflow name required`);
}

// --- Finalizer ---
{
  const { text, json } = load(FINALIZER);
  assert(/0\s+7\s+\*\s+\*\s+\*/.test(text), `${FINALIZER}: cron must be 0 7 * * *`);
  assert(text.includes('America/New_York'), `${FINALIZER}: timezone America/New_York`);
  assert(
    /clay-\$\{|clay-' \+|['"]clay-['"]\s*\+|batch_id.*clay-|clay-YYYY-MM-DD|toISOString|America\/New_York/.test(
      text,
    ) && /clay-/.test(text),
    `${FINALIZER}: must derive clay-YYYY-MM-DD batch_id`,
  );
  assert(
    text.includes('/api/marketing/clay-batches/'),
    `${FINALIZER}: must GET clay-batches summary`,
  );
  assert(/draft_count/.test(text), `${FINALIZER}: must branch on draft_count`);
  assert(
    /SLACK_CLAY_LEADS_CHANNEL_ID|chat\.postMessage|slack_message\.blocks/.test(text),
    `${FINALIZER}: must post Slack (blocks or empty status)`,
  );
  assert(/slack_message/.test(text), `${FINALIZER}: must use slack_message from SEO Agent`);
  assert(!INLINE_SECRET.test(text), `${FINALIZER}: inline secret token detected`);
  assert(hasEnvOrCredentialRef(text), `${FINALIZER}: secrets must be env/credential refs`);
  assert(!EMAIL_SEND.test(text), `${FINALIZER}: must not send email`);
  assert(!SEQUENCE_MUTATE.test(text), `${FINALIZER}: must not mutate sequence status`);
  assert(json?.name, `${FINALIZER}: workflow name required`);
}

// --- Slack approval ---
{
  const { text, json } = load(APPROVAL);
  assert(/rawBody|raw.?body|binaryPropertyName/i.test(text), `${APPROVAL}: retain raw body`);
  assert(/HMAC|createHmac|timingSafeEqual|X-Slack-Signature/i.test(text), `${APPROVAL}: HMAC verify`);
  assert(/timestamp|five minutes|5\s*\*\s*60|300000|ageMs/i.test(text), `${APPROVAL}: timestamp ≤5 min`);
  assert(/SLACK_SIGNING_SECRET/.test(text), `${APPROVAL}: SLACK_SIGNING_SECRET ref`);
  assert(/SLACK_CLAY_LEADS_CHANNEL_ID/.test(text), `${APPROVAL}: channel allow-list`);
  assert(/SLACK_CLAY_APPROVER_USER_IDS/.test(text), `${APPROVAL}: approver allow-list`);
  assert(/clay_batch_approve/.test(text), `${APPROVAL}: map clay_batch_approve`);
  assert(/clay_batch_reject/.test(text), `${APPROVAL}: map clay_batch_reject`);
  assert(
    text.includes('/api/marketing/approval/approve'),
    `${APPROVAL}: call batch approve endpoint`,
  );
  assert(
    text.includes('/api/marketing/approval/reject'),
    `${APPROVAL}: call batch reject endpoint`,
  );
  assert(/batch_id/.test(text), `${APPROVAL}: send {batch_id}`);
  assert(
    /respondToWebhook|responseMode|Acknowledge|acknowledge/i.test(text),
    `${APPROVAL}: acknowledge Slack promptly`,
  );
  assert(/chat\.update|Update original|actor|retryable/i.test(text), `${APPROVAL}: update Slack message`);
  assert(/NODE_FUNCTION_ALLOW_BUILTIN|require\(['"]crypto['"]\)/.test(text), `${APPROVAL}: crypto for HMAC`);
  assert(!INLINE_SECRET.test(text), `${APPROVAL}: inline secret token detected`);
  assert(hasEnvOrCredentialRef(text), `${APPROVAL}: secrets must be env/credential refs`);
  assert(!EMAIL_SEND.test(text), `${APPROVAL}: must not send email`);
  assert(!SEQUENCE_MUTATE.test(text), `${APPROVAL}: must not mutate sequence status`);
  // Only batch approve/reject — not per-sequence approve with sequence_ids as primary path
  assert(
    !/sequence_ids/.test(text) || /must not|never|batch_id only/i.test(text),
    `${APPROVAL}: must only call batch approve/reject (no sequence_ids path)`,
  );
  assert(json?.name, `${APPROVAL}: workflow name required`);
}

// Cross-check: no workflow invents email/send
for (const name of [INTAKE, FINALIZER, APPROVAL]) {
  const { text } = load(name);
  if (!text) continue;
  assert(!EMAIL_SEND.test(text), `${name}: no email-send nodes`);
  assert(!INLINE_SECRET.test(text), `${name}: no inline sk-/re_/xox secrets`);
}

if (failures.length) {
  console.error('FAIL');
  for (const f of failures) console.error(`  - ${f}`);
  process.exit(1);
}

console.log('PASS');
console.log(`  validated: ${INTAKE}, ${FINALIZER}, ${APPROVAL}`);
