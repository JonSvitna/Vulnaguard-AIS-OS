#!/usr/bin/env python3
"""
Stripe API client for the AIOS — revenue/KPI pull, read-only.
Stdlib only (no `stripe` SDK) so it runs anywhere python3 does.

Usage:
    python3 scripts/stripe_api.py balance
    python3 scripts/stripe_api.py charges [--days 30]
    python3 scripts/stripe_api.py subscriptions
    python3 scripts/stripe_api.py mrr

Reads STRIPE_SECRET_KEY from .env.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

API_BASE = "https://api.stripe.com/v1"


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def api_get(path: str, params: dict | None = None) -> dict:
    secret_key = os.environ["STRIPE_SECRET_KEY"]
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {secret_key}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Stripe API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def cmd_balance(_args):
    data = api_get("/balance")
    for bucket in data.get("available", []):
        print(f"Available: {bucket['amount'] / 100:.2f} {bucket['currency'].upper()}")
    for bucket in data.get("pending", []):
        print(f"Pending:   {bucket['amount'] / 100:.2f} {bucket['currency'].upper()}")


def cmd_charges(args):
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    data = api_get("/charges", {"created[gte]": int(since.timestamp()), "limit": 100})
    charges = data.get("data", [])
    total = sum(c["amount"] for c in charges if c.get("paid") and not c.get("refunded"))
    print(f"Charges in last {args.days} days: {len(charges)} (total {total / 100:.2f} {charges[0]['currency'].upper() if charges else 'usd'})")
    for c in charges:
        status = "paid" if c.get("paid") and not c.get("refunded") else c.get("status", "unknown")
        ts = datetime.fromtimestamp(c["created"], tz=timezone.utc).strftime("%Y-%m-%d")
        print(f"  {ts}  {c['amount'] / 100:>8.2f} {c['currency'].upper()}  {status:10}  {c.get('description') or c.get('id')}")


def cmd_subscriptions(_args):
    data = api_get("/subscriptions", {"status": "active", "limit": 100})
    subs = data.get("data", [])
    print(f"Active subscriptions: {len(subs)}")
    for s in subs:
        item = s["items"]["data"][0] if s["items"]["data"] else None
        amount = item["price"]["unit_amount"] / 100 if item else 0
        currency = item["price"]["currency"].upper() if item else "usd"
        interval = item["price"]["recurring"]["interval"] if item else "?"
        print(f"  {s['id']}  {amount:.2f} {currency}/{interval}  customer={s['customer']}")


def cmd_mrr(_args):
    data = api_get("/subscriptions", {"status": "active", "limit": 100})
    subs = data.get("data", [])
    mrr = 0.0
    for s in subs:
        for item in s["items"]["data"]:
            price = item["price"]
            amount = price["unit_amount"] / 100 * item.get("quantity", 1)
            recurring = price.get("recurring")
            if not recurring:
                continue
            interval = recurring["interval"]
            interval_count = recurring.get("interval_count", 1)
            if interval == "month":
                mrr += amount / interval_count
            elif interval == "year":
                mrr += amount / (12 * interval_count)
            elif interval == "week":
                mrr += amount * (52 / 12) / interval_count
            elif interval == "day":
                mrr += amount * (30 / interval_count)
    print(f"MRR (from {len(subs)} active subscriptions): {mrr:.2f}")


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Stripe API client")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("balance")

    p_charges = sub.add_parser("charges")
    p_charges.add_argument("--days", type=int, default=30)

    sub.add_parser("subscriptions")
    sub.add_parser("mrr")

    args = parser.parse_args()

    if "STRIPE_SECRET_KEY" not in os.environ:
        print("STRIPE_SECRET_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    {
        "balance": cmd_balance,
        "charges": cmd_charges,
        "subscriptions": cmd_subscriptions,
        "mrr": cmd_mrr,
    }[args.command](args)


if __name__ == "__main__":
    main()
