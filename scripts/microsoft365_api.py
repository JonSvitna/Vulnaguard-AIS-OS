#!/usr/bin/env python3
"""
Microsoft Graph API client for the AIOS — calendar + mail, app-only auth.
Stdlib only (no requests/msal) so it runs anywhere python3 does.

Usage:
    python3 scripts/microsoft365_api.py events [--days 7]
    python3 scripts/microsoft365_api.py mail [--top 10]
    python3 scripts/microsoft365_api.py send --to a@b.com --subject "Hi" --body "Text"

Reads MS365_CLIENT_ID, MS365_TENANT_ID, MS365_CLIENT_SECRET, MS365_USER_UPN from .env.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone
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


def get_token() -> str:
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


def graph_request(path: str, token: str, method: str = "GET", body: dict | None = None):
    url = f"{GRAPH_BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        if resp.status == 202 or resp.length == 0:
            return None
        return json.loads(resp.read())


def list_events(token: str, upn: str, days: int):
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)
    params = urllib.parse.urlencode({
        "startDateTime": now.isoformat(),
        "endDateTime": end.isoformat(),
        "$orderby": "start/dateTime",
        "$top": "25",
    })
    path = f"/users/{upn}/calendarView?{params}"
    result = graph_request(path, token)
    for ev in result.get("value", []):
        start = ev["start"]["dateTime"]
        print(f"{start}  {ev['subject']}")


def list_mail(token: str, upn: str, top: int):
    params = urllib.parse.urlencode({
        "$orderby": "receivedDateTime desc",
        "$top": str(top),
        "$select": "subject,from,receivedDateTime",
    })
    path = f"/users/{upn}/messages?{params}"
    result = graph_request(path, token)
    for msg in result.get("value", []):
        sender = msg.get("from", {}).get("emailAddress", {}).get("address", "?")
        print(f"{msg['receivedDateTime']}  {sender}  {msg['subject']}")


def send_mail(token: str, upn: str, to: str, subject: str, body: str):
    path = f"/users/{upn}/sendMail"
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": to}}],
        }
    }
    graph_request(path, token, method="POST", body=payload)
    print(f"Sent to {to}")


def list_rules(token: str, upn: str):
    path = f"/users/{upn}/mailFolders/inbox/messageRules"
    result = graph_request(path, token)
    for rule in result.get("value", []):
        actions = rule.get("actions", {})
        forward = actions.get("forwardTo") or actions.get("redirectTo") or []
        targets = ", ".join(a.get("emailAddress", {}).get("address", "?") for a in forward)
        print(f"{rule['id']}  enabled={rule['isEnabled']}  '{rule['displayName']}'  -> {targets or '(no forward action)'}")


def set_rule_forward(token: str, upn: str, rule_id: str, to: str, redirect: bool = False):
    action_key = "redirectTo" if redirect else "forwardTo"
    path = f"/users/{upn}/mailFolders/inbox/messageRules/{rule_id}"
    payload = {"actions": {action_key: [{"emailAddress": {"address": to}}]}}
    graph_request(path, token, method="PATCH", body=payload)
    print(f"Rule {rule_id} {action_key} -> {to}")


def create_rule(token: str, upn: str, name: str, sender: str | None, to: str, redirect: bool = False):
    action_key = "redirectTo" if redirect else "forwardTo"
    list_path = f"/users/{upn}/mailFolders/inbox/messageRules"
    existing = graph_request(list_path, token)
    next_sequence = max((r.get("sequence", 0) for r in existing.get("value", [])), default=0) + 1
    conditions = {"fromAddresses": [{"emailAddress": {"address": sender}}]} if sender else {}
    payload = {
        "displayName": name,
        "sequence": next_sequence,
        "isEnabled": True,
        "conditions": conditions,
        "actions": {action_key: [{"emailAddress": {"address": to}}], "stopProcessingRules": False},
    }
    result = graph_request(list_path, token, method="POST", body=payload)
    print(f"Created rule {result['id']}  '{name}'  {sender or '(all mail)'} -> {to}")


def main():
    load_env()
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_events = sub.add_parser("events")
    p_events.add_argument("--days", type=int, default=7)

    p_mail = sub.add_parser("mail")
    p_mail.add_argument("--top", type=int, default=10)

    p_send = sub.add_parser("send")
    p_send.add_argument("--to", required=True)
    p_send.add_argument("--subject", required=True)
    p_send.add_argument("--body", required=True)

    sub.add_parser("rules")

    p_rule_forward = sub.add_parser("rule-forward")
    p_rule_forward.add_argument("--rule-id", required=True)
    p_rule_forward.add_argument("--to", required=True)
    p_rule_forward.add_argument("--redirect", action="store_true",
                                 help="Use redirectTo (keep original sender) instead of forwardTo")

    p_create_rule = sub.add_parser("create-rule")
    p_create_rule.add_argument("--name", required=True)
    p_create_rule.add_argument("--sender", required=False, default=None,
                                help="Exact from-address to match (omit to match all mail)")
    p_create_rule.add_argument("--to", required=True)
    p_create_rule.add_argument("--redirect", action="store_true",
                                help="Use redirectTo (keep original sender) instead of forwardTo")

    args = parser.parse_args()
    upn = os.environ["MS365_USER_UPN"]
    token = get_token()

    if args.command == "events":
        list_events(token, upn, args.days)
    elif args.command == "mail":
        list_mail(token, upn, args.top)
    elif args.command == "send":
        send_mail(token, upn, args.to, args.subject, args.body)
    elif args.command == "rules":
        list_rules(token, upn)
    elif args.command == "rule-forward":
        set_rule_forward(token, upn, args.rule_id, args.to, args.redirect)
    elif args.command == "create-rule":
        create_rule(token, upn, args.name, args.sender, args.to, args.redirect)


if __name__ == "__main__":
    main()
