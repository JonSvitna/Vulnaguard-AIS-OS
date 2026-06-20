# Stripe API

Revenue/KPI connection — closes the gap flagged in the 2026-06-19 audit: the AIOS had no domain feeding revenue numbers, so marketing-pipeline output (emails sent) couldn't be tied to outcomes (deals, revenue).

## Status

Scaffolded and **live** as of 2026-06-19 — `STRIPE_SECRET_KEY` is set, all four commands verified against the real account. This is the primary revenue plan named in `CLAUDE.md` ("Stripe (primary, not yet configured)"); Mercury Bank is the invoicing fallback, not wired here. Account currently shows $0 balance, 0 charges, 0 subscriptions — expected, no clients yet.

## Auth flow

Simple bearer-token auth on the secret key, no OAuth.

```
Authorization: Bearer {STRIPE_SECRET_KEY}
```

Use a **restricted key** scoped to read-only on Balances, Charges, and Subscriptions if Stripe's dashboard offers it — this connection only ever needs to read revenue data, never to charge or refund.

## Credentials

```
STRIPE_SECRET_KEY=sk_live_... (or sk_test_... while there are no real customers yet)
```

Get it from the Stripe Dashboard → Developers → API keys. Store in `.env` (gitignored).

## Common queries

**Current balance:**
```
GET /v1/balance
```

**Recent charges:**
```
GET /v1/charges?created[gte]={unix_ts}&limit=100
```

**Active subscriptions (for MRR):**
```
GET /v1/subscriptions?status=active&limit=100
```

MRR isn't a native Stripe field — compute it by normalizing each subscription's recurring price to a monthly amount (divide annual by 12, weekly by 12/52, etc.) and summing across active subscriptions. The script below does this.

## Script

`scripts/stripe_api.py` — stdlib-only Python (no `stripe` SDK dependency, matches the convention in `scripts/microsoft365_api.py`).

```
python3 scripts/stripe_api.py balance
python3 scripts/stripe_api.py charges --days 30
python3 scripts/stripe_api.py subscriptions
python3 scripts/stripe_api.py mrr
```

## Verified working

2026-06-19 — all four commands (`balance`, `charges`, `subscriptions`, `mrr`) confirmed live against the real Stripe account. Returned $0 balance / 0 charges / 0 active subscriptions / $0 MRR — consistent with no clients yet, not an error state.

## Next step toward closing the KPI gap

Once this is live, the natural follow-up is wiring it into the SEO agent's marketing dashboard (or a new lightweight KPI view) so "50 emails sent today" can sit next to "$X revenue this month" — that's a `/level-up` capability task, not a Connections task, once this is wired.
