#!/usr/bin/env python3
"""
---
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

Slack guest-access mismatch check — deterministic, no AI step.

Compares actual membership of a Slack channel against a SharePoint Excel
sheet's "Approved" column (source of truth) and prints mismatches for
manual review. Never adds, removes, or invites anyone — L2 (Drafted):
this script drafts the mismatch list, a human decides what to do with it.

Scoped 2026-07-27 via /level-up (Brickline Slack guest-access billing
mistake — see decisions/log.md same date).

Usage:
    python3 scripts/slack_guest_check.py \
        --channel C0123456789 \
        --site-id contoso.sharepoint.com,SITE-GUID,WEB-GUID \
        --file-path "/Shared Documents/Brickline Guests.xlsx" \
        --table ApprovedGuests

Reads MS365_CLIENT_ID, MS365_TENANT_ID, MS365_CLIENT_SECRET (app-only
Graph auth, same as scripts/microsoft365_api.py) and SLACK_BOT_TOKEN
(same as scripts/slack_api.py) from .env.

The Excel table must have an "Email" column and an "Approved" column
(TRUE/FALSE or any truthy string). Known blocker as of 2026-07-27: the
remote session's MS365_USER_UPN and related env vars have failed 5
consecutive days running (see decisions/log.md 07-20/22/23/26/27) — fix
that auth path before relying on this script.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def get_graph_token() -> str:
    tenant_id = os.environ["MS365_TENANT_ID"]
    client_id = os.environ["MS365_CLIENT_ID"]
    client_secret = os.environ["MS365_CLIENT_SECRET"]

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
    }).encode()

    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    return body["access_token"]


def graph_request(path: str, token: str):
    req = urllib.request.Request(f"{GRAPH_BASE}{path}", method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_approved_emails(token: str, site_id: str, file_path: str, table: str) -> dict:
    """Returns {email.lower(): approved_bool} from the sheet's table."""
    encoded_path = urllib.parse.quote(file_path)
    rows = graph_request(
        f"/sites/{site_id}/drive/root:{encoded_path}:/workbook/tables/{table}/rows",
        token,
    )
    approved = {}
    for row in rows.get("value", []):
        values = row["values"][0]
        # Expect columns in order: Email, Approved (adjust if the sheet differs)
        email = str(values[0]).strip().lower()
        is_approved = str(values[1]).strip().lower() in ("true", "1", "yes", "approved")
        approved[email] = is_approved
    return approved


def get_slack_channel_emails(bot_token: str, channel: str) -> set:
    req = urllib.request.Request(
        f"https://slack.com/api/conversations.members?channel={channel}&limit=200",
        method="GET",
    )
    req.add_header("Authorization", f"Bearer {bot_token}")
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    if not body.get("ok"):
        print(f"Slack API error: {body.get('error')}", file=sys.stderr)
        sys.exit(1)

    emails = set()
    for user_id in body.get("members", []):
        info_req = urllib.request.Request(
            f"https://slack.com/api/users.info?user={user_id}", method="GET"
        )
        info_req.add_header("Authorization", f"Bearer {bot_token}")
        with urllib.request.urlopen(info_req) as info_resp:
            info = json.loads(info_resp.read())
        email = info.get("user", {}).get("profile", {}).get("email")
        if email:
            emails.add(email.strip().lower())
    return emails


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", required=True, help="Slack channel ID")
    parser.add_argument("--site-id", required=True, help="Graph site ID (hostname,site-guid,web-guid)")
    parser.add_argument("--file-path", required=True, help="Path to the .xlsx within the site's drive")
    parser.add_argument("--table", required=True, help="Excel table name (Email, Approved columns)")
    args = parser.parse_args()

    load_env()
    for var in ("MS365_TENANT_ID", "MS365_CLIENT_ID", "MS365_CLIENT_SECRET", "SLACK_BOT_TOKEN"):
        if var not in os.environ:
            print(f"{var} not set in .env", file=sys.stderr)
            sys.exit(1)

    graph_token = get_graph_token()
    approved = get_approved_emails(graph_token, args.site_id, args.file_path, args.table)
    in_slack = get_slack_channel_emails(os.environ["SLACK_BOT_TOKEN"], args.channel)

    approved_emails = {e for e, ok in approved.items() if ok}

    unapproved_in_slack = in_slack - approved_emails
    approved_not_in_slack = approved_emails - in_slack

    print(f"Checked {len(in_slack)} Slack members against {len(approved_emails)} approved rows.\n")

    if unapproved_in_slack:
        print("FLAG — in Slack channel but NOT marked Approved (review for removal):")
        for e in sorted(unapproved_in_slack):
            print(f"  - {e}")
        print()

    if approved_not_in_slack:
        print("FLAG — Approved on the sheet but NOT yet in the Slack channel (pending invite):")
        for e in sorted(approved_not_in_slack):
            print(f"  - {e}")
        print()

    if not unapproved_in_slack and not approved_not_in_slack:
        print("No mismatches. Slack membership matches the Approved sheet exactly.")


if __name__ == "__main__":
    main()
