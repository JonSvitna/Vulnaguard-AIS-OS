# Resend API

Email-sending transport for the `vulnaguard-seo-agent` marketing/outreach pipeline (lead sequences) and the Sentinel CMMC alert-delivery system (`deliver_alert()`).

## Auth flow

Simple bearer-token auth, no OAuth.

```
Authorization: Bearer {RESEND_API_KEY}
```

Used via the official `resend` npm SDK in both projects, not raw HTTP calls.

## Credentials

| Project | Env var | Notes |
|---|---|---|
| vulnaguard-seo-agent | `RESEND_API_KEY` | Set in Railway production AND must also be set in local `.env.local` for dev — these are separate environments, not shared. We lost an afternoon (2026-06-19) because local was missing it while prod had it. |
| Sentinel-CMMC | `RESEND_API_KEY`, `ALERT_FROM_EMAIL` | Set in Railway production. |

From-address must be on a domain verified in the Resend dashboard — `outreach@vulnaguard.com` / `seanmurrill@vulnaguard.com` are verified for vulnaguard.com.

## Rate limit — the thing that bit us

**5 requests/second**, hard limit, returns a 429 ("Too many requests... contact support to increase rate limit") if exceeded. No automatic backoff in the SDK.

vulnaguard-seo-agent's batch sender (`app/api/marketing/send-queue/send-batch/route.ts`) sends sequentially in a loop — at full speed this blew through the limit on a 50-email batch (5 of 50 failed). Fixed by adding a 250ms delay between sends (`app/api/marketing/send-queue/send-batch/route.ts`), which keeps it at ~4 req/sec.

**If you build a new Resend-sending flow anywhere, throttle it to ≥200ms between calls or you will hit this.**

## Common queries

**Send an email:**
```ts
import { Resend } from 'resend'
const resend = new Resend(apiKey)
const { data, error } = await resend.emails.send({
  from: 'outreach@vulnaguard.com',
  to: 'lead@example.com',
  subject: '...',
  html: '...',
  text: '...',
})
```

Returns `{ data: { id }, error: null }` on success, or `{ data: null, error: { message } }` on failure (including rate-limit 429s) — the SDK doesn't throw, always check `error`.

## Daily send cap (app-level, not Resend's)

vulnaguard-seo-agent enforces its own daily cap independent of Resend's rate limit — `agent_config.daily_send_limit` (default 50), checked against `COUNT(*) FROM emails WHERE sent_at >= CURRENT_DATE` before each batch. This is a deliberate outreach-volume throttle, not a Resend constraint.

## Verified working

2026-06-19 — live test send + full 50-email batch send confirmed via production Railway deployment, `re.id` returned for each successful send. Failed sends (due to the rate limit) reset cleanly back to `status='drafted'` for retry — no data loss, no duplicate sends observed.
