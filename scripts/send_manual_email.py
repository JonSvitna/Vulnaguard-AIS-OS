#!/usr/bin/env python3
"""
Send a one-off BD email via Resend — the send path for drafts written in the
Claude Pro Projects tier (references/claude-projects-drafting.md), so manual
one-off outreach still goes out from the same verified vulnaguard.com domain
as the automated vulnaguard-seo-agent pipeline, not a personal mailbox.

Stdlib only, matches scripts/buffer_api.py conventions.

Usage:
    python3 scripts/send_manual_email.py \
        --to lead@example.com \
        --subject "Marcus — CMMC referral partnership" \
        --body-file /tmp/draft.txt \
        --list partnership

    # or pipe the body in:
    cat draft.txt | python3 scripts/send_manual_email.py --to lead@example.com --subject "..." --list sales

Reads RESEND_API_KEY from .env (same key used by vulnaguard-seo-agent and
Sentinel-CMMC — see references/resend-api.md). Add it to .env before first use.

Does NOT log to references/outreach-log.md automatically — that log tracks
reply status over time and is meant to be updated by hand as things change,
not auto-appended. Add the row yourself after sending.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

API_URL = "https://api.resend.com/emails"
DEFAULT_FROM = "outreach@vulnaguard.com"


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def send_email(to: str, subject: str, body: str, from_addr: str) -> dict:
    api_key = os.environ["RESEND_API_KEY"]
    payload = json.dumps({
        "from": from_addr,
        "to": [to],
        "subject": subject,
        "text": body,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"Resend API error {e.code}: {body_text}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", help="Path to a text file with the email body. Omit to read from stdin.")
    parser.add_argument("--from-addr", default=DEFAULT_FROM, help=f"Verified sender (default: {DEFAULT_FROM})")
    parser.add_argument("--list", choices=["partnership", "sales", "general"], required=True,
                         help="Which Claude Project this draft came from — printed in the confirmation for your own tracking, not sent to Resend.")
    args = parser.parse_args()

    load_env()

    if args.body_file:
        body = Path(args.body_file).read_text()
    else:
        if sys.stdin.isatty():
            print("No --body-file given and stdin is a terminal — pipe the draft in or use --body-file.", file=sys.stderr)
            sys.exit(1)
        body = sys.stdin.read()

    result = send_email(args.to, args.subject, body, args.from_addr)
    print(f"Sent ({args.list}) to {args.to} — Resend id: {result.get('id')}")
    print("Remember to add a row to references/outreach-log.md.")


if __name__ == "__main__":
    main()
