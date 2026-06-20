#!/usr/bin/env python3
"""
Slack Web API client for the AIOS — channels, messages, send.
Stdlib only (no `slack_sdk`) so it runs anywhere python3 does.

Usage:
    python3 scripts/slack_api.py channels
    python3 scripts/slack_api.py history --channel C0123456789 [--limit 20]
    python3 scripts/slack_api.py send --channel C0123456789 --text "Hi"

Reads SLACK_BOT_TOKEN from .env. The bot must be invited to a channel
(`/invite @botname` in Slack) before it can read or post there.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "https://slack.com/api"


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def api_call(method: str, http_method: str = "GET", params: dict | None = None) -> dict:
    token = os.environ["SLACK_BOT_TOKEN"]
    url = f"{API_BASE}/{method}"
    headers = {"Authorization": f"Bearer {token}"}
    if http_method == "GET":
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
    else:
        headers["Content-Type"] = "application/json; charset=utf-8"
        req = urllib.request.Request(url, data=json.dumps(params or {}).encode(), method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Slack API HTTP error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    if not data.get("ok"):
        print(f"Slack API error: {data.get('error')}", file=sys.stderr)
        sys.exit(1)
    return data


def cmd_channels(_args):
    data = api_call("conversations.list", params={"types": "public_channel", "limit": 200})
    for ch in data.get("channels", []):
        member = "member" if ch.get("is_member") else "not-member"
        print(f"{ch['id']}  #{ch['name']}  ({member})")


def cmd_history(args):
    data = api_call("conversations.history", params={"channel": args.channel, "limit": args.limit})
    for msg in data.get("messages", []):
        ts = datetime.fromtimestamp(float(msg["ts"]), tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        user = msg.get("user", msg.get("bot_id", "?"))
        print(f"{ts}  {user}  {msg.get('text', '')}")


def cmd_send(args):
    data = api_call("chat.postMessage", http_method="POST", params={"channel": args.channel, "text": args.text})
    print(f"Sent to {data['channel']} at ts={data['ts']}")


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Slack Web API client")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("channels")

    p_history = sub.add_parser("history")
    p_history.add_argument("--channel", required=True)
    p_history.add_argument("--limit", type=int, default=20)

    p_send = sub.add_parser("send")
    p_send.add_argument("--channel", required=True)
    p_send.add_argument("--text", required=True)

    args = parser.parse_args()

    if "SLACK_BOT_TOKEN" not in os.environ:
        print("SLACK_BOT_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    {
        "channels": cmd_channels,
        "history": cmd_history,
        "send": cmd_send,
    }[args.command](args)


if __name__ == "__main__":
    main()
