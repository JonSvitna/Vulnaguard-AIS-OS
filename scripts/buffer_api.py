#!/usr/bin/env python3
"""
Buffer API client for the AIOS — queue posts across Facebook, Instagram, LinkedIn.
Stdlib only, matches scripts/slack_api.py conventions.

Usage:
    python3 scripts/buffer_api.py profiles
    python3 scripts/buffer_api.py queue --profile-id <id> --text "..." [--scheduled-at "2026-06-25T15:00:00Z"]

Reads BUFFER_ACCESS_TOKEN from .env. Get a token at https://buffer.com/developers/apps
(create an app, generate an access token for your own account — no OAuth flow needed
for single-account use).

This script only QUEUES posts into Buffer — it never auto-approves content. The
social-post-queue skill is the human review gate; this is the deterministic
"push the approved draft" step downstream of it.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

API_BASE = "https://api.bufferapp.com/1"


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def api_call(path: str, http_method: str = "GET", params: dict | None = None) -> dict:
    token = os.environ["BUFFER_ACCESS_TOKEN"]
    params = dict(params or {})
    params["access_token"] = token
    url = f"{API_BASE}/{path}"
    if http_method == "GET":
        url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
    else:
        req = urllib.request.Request(
            url, data=urllib.parse.urlencode(params, doseq=True).encode(), method="POST"
        )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Buffer API HTTP error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def cmd_profiles(_args):
    data = api_call("profiles.json")
    for p in data:
        print(f"{p['id']}  {p['service']}  {p.get('formatted_username', p.get('service_username', ''))}")


def cmd_queue(args):
    params = {"text": args.text, "now": "false" if args.scheduled_at else "true"}
    if args.scheduled_at:
        params["scheduled_at"] = args.scheduled_at
    data = api_call(f"profiles/{args.profile_id}/updates/create.json", http_method="POST", params=params)
    if data.get("success"):
        print(f"Queued: {data['updates'][0]['id']}")
    else:
        print(f"Buffer error: {data}", file=sys.stderr)
        sys.exit(1)


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Buffer API client")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("profiles")

    p_queue = sub.add_parser("queue")
    p_queue.add_argument("--profile-id", required=True)
    p_queue.add_argument("--text", required=True)
    p_queue.add_argument("--scheduled-at", help="ISO 8601 UTC timestamp; omit to add to next available slot")

    args = parser.parse_args()

    if "BUFFER_ACCESS_TOKEN" not in os.environ:
        print("BUFFER_ACCESS_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    {
        "profiles": cmd_profiles,
        "queue": cmd_queue,
    }[args.command](args)


if __name__ == "__main__":
    main()
