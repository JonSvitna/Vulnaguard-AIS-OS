#!/usr/bin/env python3
"""
Poll the M365 mailbox for new mail since the last run and post each to a
Slack channel. Dedup state (cursor + seen message ID hashes) is stored in
Slack history itself so no filesystem persistence is needed — Railway-safe.

Usage:
    python3 scripts/mail_to_slack.py --channel C0123456789 [--top 25] [--lookback-minutes 60]

Reads MS365_CLIENT_ID/MS365_TENANT_ID/MS365_CLIENT_SECRET/MS365_USER_UPN
and SLACK_BOT_TOKEN from .env (or real env vars in production).
"""
import argparse
import hashlib
import re
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from microsoft365_api import load_env as load_mail_env, get_token as get_mail_token, graph_request
from slack_api import api_call as slack_call
import os

REF_RE = re.compile(r"_ref:([0-9T:\-\.]+Z)_")
MID_RE = re.compile(r"_mid:([a-f0-9]{12})_")
HISTORY_SCAN = 100  # how many recent Slack messages to scan for seen IDs


def _mid_hash(msg_id: str) -> str:
    """Short stable fingerprint of an M365 message ID."""
    return hashlib.sha256(msg_id.encode()).hexdigest()[:12]


def read_slack_state(channel: str) -> tuple[str | None, set]:
    """Return (last_cursor, seen_mid_hashes) from recent Slack history."""
    data = slack_call("conversations.history", params={"channel": channel, "limit": HISTORY_SCAN})
    cursor = None
    seen = set()
    for msg in data.get("messages", []):
        if not msg.get("bot_id"):
            continue
        text = msg.get("text", "")
        if cursor is None:
            m = REF_RE.search(text)
            if m:
                cursor = m.group(1)
        for m in MID_RE.finditer(text):
            seen.add(m.group(1))
    return cursor, seen


def fetch_since(token: str, upn: str, since_iso: str, top: int):
    params = urllib.parse.urlencode({
        "$filter": f"receivedDateTime gt {since_iso}",
        "$orderby": "receivedDateTime asc",
        "$top": str(top),
        "$select": "id,subject,from,receivedDateTime,bodyPreview",
    })
    path = f"/users/{upn}/messages?{params}"
    result = graph_request(path, token)
    return result.get("value", [])


def post_to_slack(channel: str, msg: dict):
    sender = msg.get("from", {}).get("emailAddress", {}).get("address", "unknown sender")
    subject = msg.get("subject", "(no subject)")
    preview = msg.get("bodyPreview", "").strip().replace("\n", " ")
    received = msg["receivedDateTime"]
    mid = _mid_hash(msg.get("id", received))
    text = f"*New mail* from `{sender}`\n*{subject}*\n{preview[:300]}\n_ref:{received}_ _mid:{mid}_"
    slack_call("chat.postMessage", http_method="POST", params={"channel": channel, "text": text})


def main():
    load_mail_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True)
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument("--lookback-minutes", type=int, default=60,
                         help="Window to check on first run (no prior cursor found in channel)")
    args = parser.parse_args()

    upn = os.environ["MS365_USER_UPN"]
    mail_token = get_mail_token()

    cursor, seen_mids = read_slack_state(args.channel)
    print(f"Loaded {len(seen_mids)} seen message fingerprints from Slack history.")

    if not cursor:
        cursor = (datetime.now(timezone.utc) - timedelta(minutes=args.lookback_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"No prior cursor found, defaulting to lookback: {cursor}")
    else:
        # Graph's `gt` filter on receivedDateTime isn't reliably exclusive at exact
        # second-precision matches — bump by 1s to avoid re-posting the last message.
        cursor_dt = datetime.strptime(cursor, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) + timedelta(seconds=1)
        cursor = cursor_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"Resuming from cursor: {cursor}")

    new_mail = fetch_since(mail_token, upn, cursor, args.top)
    if not new_mail:
        print("No new mail.")
        return

    posted = 0
    skipped = 0
    for msg in new_mail:
        mid = _mid_hash(msg.get("id", msg["receivedDateTime"]))
        if mid in seen_mids:
            print(f"Skipped (duplicate): {msg.get('subject')} ({msg['receivedDateTime']})")
            skipped += 1
            continue
        post_to_slack(args.channel, msg)
        print(f"Posted: {msg.get('subject')} ({msg['receivedDateTime']})")
        posted += 1

    print(f"Done: {posted} posted, {skipped} skipped as duplicates.")


if __name__ == "__main__":
    main()
