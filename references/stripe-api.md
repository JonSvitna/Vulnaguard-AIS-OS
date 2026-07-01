# Stripe API

Revenue/KPI connection — closes the gap flagged in the 2026-06-19 audit: the AIOS had no domain feeding revenue numbers, so marketing-pipeline output (emails sent) couldn't be tied to outcomes (deals, revenue).

## Status

**Read commands** live as of 2026-06-19 — `STRIPE_SECRET_KEY` set, all four verified. **Invoicing commands** added 2026-07-01 to support first client payment (AfterSwing deposit, SOW VG-2026-001). Mercury Bank invoicing fallback is not wired here.

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

### Read commands
```
python3 scripts/stripe_api.py balance
python3 scripts/stripe_api.py charges --days 30
python3 scripts/stripe_api.py subscriptions
python3 scripts/stripe_api.py mrr
```

### Customer + invoicing workflow
```bash
# Step 1: find or create the client as a Stripe customer
python3 scripts/stripe_api.py customer --email "don@afterswing.com" --name "Don Weston"
# → prints customer ID, e.g. cus_XXXXXXXXXXXX

# Step 2: create and finalize an invoice (prints hosted URL + invoice ID)
python3 scripts/stripe_api.py invoice create \
  --customer cus_XXXXXXXXXXXX \
  --amount 3500 \
  --description "NIST SP 800-171 Gap Assessment — Deposit (SOW VG-2026-001)" \
  --days-until-due 7 \
  --memo "Vulnaguard engagement VG-2026-001, 50% deposit per payment schedule"

# Step 3: send the invoice email via Stripe
python3 scripts/stripe_api.py invoice send in_XXXXXXXXXXXX

# Check status later
python3 scripts/stripe_api.py invoice status in_XXXXXXXXXXXX

# List all open invoices
python3 scripts/stripe_api.py invoice list
```

**Payment flow:** `collection_method=send_invoice` — Stripe emails the client a hosted payment page, they pay by card. Funds land in your Stripe balance minus fees.

## Verified working

2026-06-19 — all four commands (`balance`, `charges`, `subscriptions`, `mrr`) confirmed live against the real Stripe account. Returned $0 balance / 0 charges / 0 active subscriptions / $0 MRR — consistent with no clients yet, not an error state.

## Next step toward closing the KPI gap

Once this is live, the natural follow-up is wiring it into the SEO agent's marketing dashboard (or a new lightweight KPI view) so "50 emails sent today" can sit next to "$X revenue this month" — that's a `/level-up` capability task, not a Connections task, once this is wired.
