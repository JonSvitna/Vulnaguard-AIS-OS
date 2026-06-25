# Google Search Console

Feeds SEO modules M1 (keyword research) and M2 (ranking monitor) in the
`vulnaguard-seo-agent` repo with real ranking/query data for vulnaguard.com. Wired as
OAuth (refresh-token flow), proxied through that repo's own `/api/gsc` route — this
AIOS repo doesn't call GSC directly, it relies on the SEO agent app.

## Where it lives

- Route: `vulnaguard-seo-agent/app/api/gsc/route.ts`
- Settings/setup UI: `vulnaguard-seo-agent/app/(app)/settings/page.tsx` (has a built-in
  step-by-step OAuth setup guide rendered in the UI)
- Consumed by: `app/(app)/dashboard/page.tsx` (M1/M2/Full SEO Pass prompts pull GSC rows
  into the agent prompt) and `components/content-pipeline/GeneratingScreen.tsx`

## Auth flow

OAuth 2.0, refresh-token grant (no live user OAuth dance at runtime — token is long-lived
once obtained):

1. Google Cloud Console → create/select a project → enable the **Search Console API**.
2. Credentials → create an OAuth 2.0 Client ID (Web application type) → add
   `https://developers.google.com/oauthplayground` as an authorized redirect URI.
3. Copy Client ID + Client Secret into the app's settings page (stored as env vars, see below).
4. Go to [developers.google.com/oauthplayground](https://developers.google.com/oauthplayground)
   → gear icon → check "Use your own OAuth credentials" → paste Client ID/Secret.
5. In the scope picker, use `https://www.googleapis.com/auth/webmasters.readonly`
   (read-only is sufficient — this is query/ranking data only, no property management) →
   Authorize APIs → sign in with the account that has access to the vulnaguard.com GSC property.
6. Click "Exchange authorization code for tokens" → copy the **refresh token**.
7. The app exchanges that refresh token for short-lived access tokens itself on every
   request (`getAccessToken()` in `route.ts`), via `https://oauth2.googleapis.com/token`.

Per `connections.md`: OAuth app is published to **Production** (not stuck in Google's
testing/unverified-app limbo), secret last regenerated 2026-06-19.

## Credentials

Stored in `vulnaguard-seo-agent`'s `.env.local` (gitignored; see `.env.local.example`):

```
GSC_CLIENT_ID=...
GSC_CLIENT_SECRET=...
GSC_REFRESH_TOKEN=...
```

If `GSC_CLIENT_ID` is unset, the `/api/gsc` route returns mock data instead of failing —
useful for local dev without real credentials, but the app surfaces this to the LLM as
an explicit "GSC not configured, don't fabricate numbers" instruction rather than silently
swapping in fake data unannounced.

## Key endpoint

**Search Analytics: query** — the only GSC endpoint actually wired:

```
POST https://searchconsole.googleapis.com/webmasters/v3/sites/sc-domain:{domain}/searchAnalytics/query
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "startDate": "YYYY-MM-DD",
  "endDate": "YYYY-MM-DD",
  "dimensions": ["query"],
  "rowLimit": 100
}
```

Returns rows of `{ keys: [query], clicks, impressions, ctr, position }`. The repo's
`/api/gsc` route wraps this: `GET /api/gsc?domain=vulnaguard.com&days=90` computes the
date range (last N days) and proxies the call, returning the raw GSC response (or the
mock payload above if unconfigured).

Note the site is addressed as `sc-domain:{domain}` (domain-property syntax), not a
URL-prefix property — confirm the GSC property in question is registered as a domain
property, not a URL-prefix property, or this 404s.

## Common query patterns (per M1/M2 usage in this repo)

- **M1 (keyword research)**: dimension `query`, full available row set, used to cluster
  keyword tiers and find adjacent opportunities — must ground suggestions in real rows
  only, never invented search volume/difficulty numbers (no data source for those).
- **M2 (ranking monitor)**: same query shape, classified client-side into buckets —
  Quick Wins (position 6-20), Declining, Indexing Gaps, Stable.
- Other GSC dimensions (`page`, `country`, `device`, `date`) and other endpoints
  (Sitemaps, URL Inspection) are **not currently used** — only the single
  `query`-dimension Search Analytics call exists in the codebase today.

## Gotchas

- Read-only scope only (`webmasters.readonly`) — can't submit sitemaps or request
  indexing through this integration as currently scoped.
- `rowLimit: 100` is hardcoded in the route — large query sets get truncated silently;
  there's no pagination handling.
- Access token is fetched fresh on every request (no caching) — fine at current volume,
  would need caching if call volume grows.
- This doc reflects the actual live route in `vulnaguard-seo-agent/app/api/gsc/route.ts`
  as of this writing — re-check that file if the SEO agent's GSC integration changes.

## Rotating credentials

If the client secret or refresh token is ever exposed: Google Cloud Console → revoke/
regenerate the OAuth client secret, then redo the OAuth Playground exchange (steps 4-6
above) for a new refresh token, and update `.env.local` in `vulnaguard-seo-agent`.
