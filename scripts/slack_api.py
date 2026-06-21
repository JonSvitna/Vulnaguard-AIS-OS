#!/usr/bin/env python3
"""
Slack Web API client for the AIOS — channels, messages, send.
Stdlib only (no `slack_sdk`) so it runs anywhere python3 does.

Usage:
    python3 scripts/slack_api.py channels
    python3 scripts/slack_api.py history --channel C0123456789 [--limit 20]
    python3 scripts/slack_api.py send --channel C0123456789 --text "Hi"
    python3 scripts/slack_api.py upload --channel C0123456789 --file draft.png --text "v2 draft"

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


def api_call(method: str, http_method: str = "GET", params: dict | None = None, form_encoded: bool = False) -> dict:
    token = os.environ["SLACK_BOT_TOKEN"]
    url = f"{API_BASE}/{method}"
    headers = {"Authorization": f"Bearer {token}"}
    if http_method == "GET":
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
    elif form_encoded:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        req = urllib.request.Request(url, data=urllib.parse.urlencode(params or {}).encode(), method="POST")
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


def cmd_upload(args):
    token = os.environ["SLACK_BOT_TOKEN"]
    path = Path(args.file)
    file_bytes = path.read_bytes()

    # Step 1: get an upload URL + file id.
    step1 = api_call(
        "files.getUploadURLExternal",
        http_method="POST",
        params={"filename": path.name, "length": len(file_bytes)},
        form_encoded=True,
    )
    upload_url = step1["upload_url"]
    file_id = step1["file_id"]

    # Step 2: PUT the raw bytes to the upload URL (no auth header needed/used here).
    req = urllib.request.Request(upload_url, data=file_bytes, method="POST")
    with urllib.request.urlopen(req) as resp:
        resp.read()

    # Step 3: complete the upload, attaching it to the channel.
    complete_params = {
        "files": [{"id": file_id, "title": args.title or path.name}],
        "channel_id": args.channel,
    }
    if args.text:
        complete_params["initial_comment"] = args.text
    data = api_call("files.completeUploadExternal", http_method="POST", params=complete_params)
    print(f"Uploaded {path.name} to {args.channel}")
    return data


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

    p_upload = sub.add_parser("upload")
    p_upload.add_argument("--channel", required=True)
    p_upload.add_argument("--file", required=True)
    p_upload.add_argument("--title")
    p_upload.add_argument("--text")

    args = parser.parse_args()

    if "SLACK_BOT_TOKEN" not in os.environ:
        print("SLACK_BOT_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    {
        "channels": cmd_channels,
        "history": cmd_history,
        "send": cmd_send,
        "upload": cmd_upload,
    }[args.command](args)


if __name__ == "__main__":
    main()
