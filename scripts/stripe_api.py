#!/usr/bin/env python3
"""
Stripe API client for the AIOS — revenue/KPI pull + invoicing.
Stdlib only (no `stripe` SDK) so it runs anywhere python3 does.

Usage:
    python3 scripts/stripe_api.py balance
    python3 scripts/stripe_api.py charges [--days 30]
    python3 scripts/stripe_api.py subscriptions
    python3 scripts/stripe_api.py mrr
    python3 scripts/stripe_api.py customer --email <email> [--name <name>]
    python3 scripts/stripe_api.py invoice create --customer <id> --amount <dollars> --description <text> [--days-until-due 7] [--memo <text>]
    python3 scripts/stripe_api.py invoice send <invoice_id>
    python3 scripts/stripe_api.py invoice list
    python3 scripts/stripe_api.py invoice status <invoice_id>

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


def api_post(path: str, data: dict) -> dict:
    secret_key = os.environ["STRIPE_SECRET_KEY"]
    url = f"{API_BASE}{path}"
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {secret_key}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"Stripe API error {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)


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


def cmd_customer(args):
    data = api_get("/customers", {"email": args.email, "limit": 1})
    customers = data.get("data", [])
    if customers:
        c = customers[0]
        print(f"Existing  {c['id']}  {c.get('name', '(no name)'):<30}  <{c.get('email', '')}>")
        return
    payload = {"email": args.email}
    if args.name:
        payload["name"] = args.name
    c = api_post("/customers", payload)
    print(f"Created   {c['id']}  {c.get('name', '(no name)'):<30}  <{c.get('email', '')}>")


def cmd_invoice_create(args):
    amount_cents = int(round(args.amount * 100))
    api_post("/invoiceitems", {
        "customer": args.customer,
        "amount": amount_cents,
        "currency": "usd",
        "description": args.description,
    })
    inv_payload: dict = {
        "customer": args.customer,
        "collection_method": "send_invoice",
        "days_until_due": args.days_until_due,
    }
    if args.memo:
        inv_payload["description"] = args.memo
    inv = api_post("/invoices", inv_payload)
    inv = api_post(f"/invoices/{inv['id']}/finalize", {})
    url = inv.get("hosted_invoice_url", "(no URL — check Stripe dashboard)")
    print(f"Invoice:  {inv['id']}")
    print(f"Amount:   ${inv['amount_due'] / 100:,.2f} {inv['currency'].upper()}")
    print(f"Status:   {inv['status']}")
    print(f"Due in:   {args.days_until_due} day(s)")
    print(f"URL:      {url}")
    print(f"\nTo send the email:  python3 scripts/stripe_api.py invoice send {inv['id']}")


def cmd_invoice_send(args):
    inv = api_post(f"/invoices/{args.invoice_id}/send", {})
    print(f"Sent:     {inv['id']}")
    print(f"Status:   {inv['status']}")
    print(f"To:       {inv.get('customer_email', '(see Stripe dashboard)')}")


def cmd_invoice_list(_args):
    data = api_get("/invoices", {"limit": 20, "status": "open"})
    invoices = data.get("data", [])
    print(f"Open invoices: {len(invoices)}")
    for inv in invoices:
        due = datetime.fromtimestamp(inv["due_date"], tz=timezone.utc).strftime("%Y-%m-%d") if inv.get("due_date") else "no due date"
        print(f"  {inv['id']}  ${inv['amount_due'] / 100:>8,.2f}  due {due}  {inv.get('customer_email', '')}")


def cmd_invoice_status(args):
    inv = api_get(f"/invoices/{args.invoice_id}")
    due = datetime.fromtimestamp(inv["due_date"], tz=timezone.utc).strftime("%Y-%m-%d") if inv.get("due_date") else "no due date"
    print(f"Invoice:  {inv['id']}")
    print(f"Amount:   ${inv['amount_due'] / 100:,.2f} {inv['currency'].upper()}")
    print(f"Status:   {inv['status']}")
    print(f"Due:      {due}")
    print(f"To:       {inv.get('customer_email', '(no email on file)')}")
    url = inv.get("hosted_invoice_url")
    if url:
        print(f"URL:      {url}")


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Stripe API client")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("balance")

    p_charges = sub.add_parser("charges")
    p_charges.add_argument("--days", type=int, default=30)

    sub.add_parser("subscriptions")
    sub.add_parser("mrr")

    p_customer = sub.add_parser("customer", help="find or create a Stripe customer")
    p_customer.add_argument("--email", required=True)
    p_customer.add_argument("--name", default="")

    p_inv = sub.add_parser("invoice", help="invoice subcommands")
    inv_sub = p_inv.add_subparsers(dest="invoice_action", required=True)

    p_inv_create = inv_sub.add_parser("create")
    p_inv_create.add_argument("--customer", required=True, help="Stripe customer ID (cus_...)")
    p_inv_create.add_argument("--amount", type=float, required=True, help="Amount in dollars")
    p_inv_create.add_argument("--description", required=True, help="Line item description")
    p_inv_create.add_argument("--days-until-due", type=int, default=7, dest="days_until_due")
    p_inv_create.add_argument("--memo", default="", help="Invoice-level memo/description")

    p_inv_send = inv_sub.add_parser("send")
    p_inv_send.add_argument("invoice_id")

    inv_sub.add_parser("list")

    p_inv_status = inv_sub.add_parser("status")
    p_inv_status.add_argument("invoice_id")

    args = parser.parse_args()

    if "STRIPE_SECRET_KEY" not in os.environ:
        print("STRIPE_SECRET_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    if args.command == "invoice":
        {
            "create": cmd_invoice_create,
            "send": cmd_invoice_send,
            "list": cmd_invoice_list,
            "status": cmd_invoice_status,
        }[args.invoice_action](args)
        return

    {
        "balance": cmd_balance,
        "charges": cmd_charges,
        "subscriptions": cmd_subscriptions,
        "mrr": cmd_mrr,
        "customer": cmd_customer,
    }[args.command](args)


if __name__ == "__main__":
    main()
