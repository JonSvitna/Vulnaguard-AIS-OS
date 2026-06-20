#!/usr/bin/env python3
"""
Poll the M365 mailbox for unread mail and post each to a Slack channel,
then mark it read. Stateless across runs (dedup via isRead, not a local file)
so it's safe to run from an ephemeral cron container.

Usage:
    python3 scripts/mail_to_slack.py --channel C0123456789 [--top 25]

Reads MS365_CLIENT_ID/MS365_TENANT_ID/MS365_CLIENT_SECRET/MS365_USER_UPN
and SLACK_BOT_TOKEN from .env (or real env vars in production).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from microsoft365_api import load_env as load_mail_env, get_token as get_mail_token, graph_request
from slack_api import api_call as slack_call
import os


def fetch_unread(token: str, upn: str, top: int):
    params = "&".join([
        "$filter=isRead eq false",
        "$orderby=receivedDateTime desc",
        f"$top={top}",
        "$select=id,subject,from,receivedDateTime,bodyPreview",
    ])
    path = f"/users/{upn}/messages?{params}"
    result = graph_request(path, token)
    return result.get("value", [])


def mark_read(token: str, upn: str, message_id: str):
    path = f"/users/{upn}/messages/{message_id}"
    graph_request(path, token, method="PATCH", body={"isRead": True})


def post_to_slack(channel: str, msg: dict):
    sender = msg.get("from", {}).get("emailAddress", {}).get("address", "unknown sender")
    subject = msg.get("subject", "(no subject)")
    preview = msg.get("bodyPreview", "").strip().replace("\n", " ")
    text = f"*New mail* from `{sender}`\n*{subject}*\n{preview[:300]}"
    slack_call("chat.postMessage", http_method="POST", params={"channel": channel, "text": text})


def main():
    load_mail_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True)
    parser.add_argument("--top", type=int, default=25)
    args = parser.parse_args()

    upn = os.environ["MS365_USER_UPN"]
    mail_token = get_mail_token()

    unread = fetch_unread(mail_token, upn, args.top)
    if not unread:
        print("No unread mail.")
        return

    for msg in unread:
        post_to_slack(args.channel, msg)
        mark_read(mail_token, upn, msg["id"])
        print(f"Posted + marked read: {msg.get('subject')}")

    print(f"Done: {len(unread)} message(s) posted to Slack.")


if __name__ == "__main__":
    main()
