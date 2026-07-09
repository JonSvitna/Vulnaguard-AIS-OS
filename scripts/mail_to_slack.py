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

# Senders routed to --noise-channel instead of --channel, when provided.
# Recurring automated feeds and one-off newsletter mail, not human replies.
NOISE_SENDER_PATTERNS = [
    "noreply@bidnet.com",
    "@send.calendly.com",
    "@indiehackers.com",
]


def is_noise_sender(sender: str) -> bool:
    sender = sender.lower()
    return any(pattern in sender for pattern in NOISE_SENDER_PATTERNS)


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


def resolve_cursor(cursor: str | None, lookback_minutes: int) -> str:
    if not cursor:
        return (datetime.now(timezone.utc) - timedelta(minutes=lookback_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Graph's `gt` filter on receivedDateTime isn't reliably exclusive at exact
    # second-precision matches — bump by 1s to avoid re-posting the last message.
    cursor_dt = datetime.strptime(cursor, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) + timedelta(seconds=1)
    return cursor_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    load_mail_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True)
    parser.add_argument("--noise-channel", default=None,
                         help="If set, mail from NOISE_SENDER_PATTERNS is routed here instead of --channel")
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument("--lookback-minutes", type=int, default=60,
                         help="Window to check on first run (no prior cursor found in channel)")
    args = parser.parse_args()

    upn = os.environ["MS365_USER_UPN"]
    mail_token = get_mail_token()

    raw_cursor, seen_mids = read_slack_state(args.channel)
    print(f"[{args.channel}] Loaded {len(seen_mids)} seen message fingerprints from Slack history.")
    cursor = resolve_cursor(raw_cursor, args.lookback_minutes)
    print(f"[{args.channel}] " + ("No prior cursor found, defaulting to lookback: " if not raw_cursor else "Resuming from cursor: ") + cursor)

    noise_seen_mids: set = set()
    if args.noise_channel:
        raw_noise_cursor, noise_seen_mids = read_slack_state(args.noise_channel)
        print(f"[{args.noise_channel}] Loaded {len(noise_seen_mids)} seen message fingerprints from Slack history.")
        noise_cursor = resolve_cursor(raw_noise_cursor, args.lookback_minutes)
        print(f"[{args.noise_channel}] " + ("No prior cursor found, defaulting to lookback: " if not raw_noise_cursor else "Resuming from cursor: ") + noise_cursor)
        # Fetch from the older of the two cursors so neither channel misses mail;
        # per-message routing + per-channel seen-set below handles the rest.
        cursor = min(cursor, noise_cursor)

    new_mail = fetch_since(mail_token, upn, cursor, args.top)
    if not new_mail:
        print("No new mail.")
        return

    posted = 0
    skipped = 0
    for msg in new_mail:
        sender = msg.get("from", {}).get("emailAddress", {}).get("address", "unknown sender")
        target = args.noise_channel if (args.noise_channel and is_noise_sender(sender)) else args.channel
        target_seen = noise_seen_mids if target == args.noise_channel else seen_mids

        mid = _mid_hash(msg.get("id", msg["receivedDateTime"]))
        if mid in target_seen:
            print(f"Skipped (duplicate): {msg.get('subject')} ({msg['receivedDateTime']})")
            skipped += 1
            continue
        post_to_slack(target, msg)
        print(f"Posted to {target}: {msg.get('subject')} ({msg['receivedDateTime']})")
        posted += 1

    print(f"Done: {posted} posted, {skipped} skipped as duplicates.")


if __name__ == "__main__":
    main()
