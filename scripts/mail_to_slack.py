#!/usr/bin/env python3
"""
Poll the M365 mailbox for new mail since the last run and post each to a
Slack channel. Dedup cursor is read back from Slack itself (the timestamp
embedded in our own last posted message) rather than mutating the mailbox's
isRead state — this only needs Mail.Read, not Mail.ReadWrite, which isn't
granted on this Azure app registration.

Usage:
    python3 scripts/mail_to_slack.py --channel C0123456789 [--top 25] [--lookback-minutes 60]

Reads MS365_CLIENT_ID/MS365_TENANT_ID/MS365_CLIENT_SECRET/MS365_USER_UPN
and SLACK_BOT_TOKEN from .env (or real env vars in production).
"""
import argparse
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


def get_last_cursor(channel: str) -> str | None:
    """Find the receivedDateTime of the last mail we posted, embedded as a
    hidden marker in our own previous Slack message text."""
    data = slack_call("conversations.history", params={"channel": channel, "limit": 50})
    for msg in data.get("messages", []):
        if not msg.get("bot_id"):
            continue
        match = REF_RE.search(msg.get("text", ""))
        if match:
            return match.group(1)
    return None


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
    text = f"*New mail* from `{sender}`\n*{subject}*\n{preview[:300]}\n_ref:{received}_"
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

    cursor = get_last_cursor(args.channel)
    if not cursor:
        cursor = (datetime.now(timezone.utc) - timedelta(minutes=args.lookback_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"No prior cursor found in channel, defaulting to lookback: {cursor}")
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

    for msg in new_mail:
        post_to_slack(args.channel, msg)
        print(f"Posted: {msg.get('subject')} ({msg['receivedDateTime']})")

    print(f"Done: {len(new_mail)} message(s) posted to Slack.")


if __name__ == "__main__":
    main()
