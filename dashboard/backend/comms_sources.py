"""Live Comms sources — Slack + Microsoft Graph.

Reuses the repo's stdlib API scripts (`scripts/slack_api.py`,
`scripts/microsoft365_api.py`) rather than duplicating their auth. Every call
is defensively wrapped: the scripts are CLI tools that `sys.exit` or raise on
error, so a missing token or a dead API returns an empty list here instead of
taking down the FastAPI worker. When nothing real is available the endpoint
falls back to a clearly-labeled SIM stub.
"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"

# Bot is invited to #all-vulnaguard-sentinel (see connections.md). Override with
# SLACK_COMMS_CHANNELS in .env (comma-separated channel IDs).
DEFAULT_SLACK_CHANNELS = "C0AMQU5HN2G"


def _load_scripts():
    """Import the two API scripts lazily; return (slack, ms365) or (None, None)."""
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import slack_api  # noqa: WPS433
        import microsoft365_api  # noqa: WPS433
        return slack_api, microsoft365_api
    except Exception:  # pragma: no cover - import guard
        return None, None


def _epoch(ts_iso_or_unix):
    """Normalize a Slack unix ts or a Graph ISO timestamp to epoch seconds."""
    if ts_iso_or_unix is None:
        return 0.0
    try:
        return float(ts_iso_or_unix)  # Slack ts, e.g. "1719000000.001"
    except (TypeError, ValueError):
        try:
            return datetime.fromisoformat(str(ts_iso_or_unix).replace("Z", "+00:00")).timestamp()
        except ValueError:
            return 0.0


def _truncate(text, limit=90):
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def fetch_slack(limit=4):
    """Recent messages from the configured Slack channel(s). Never raises."""
    slack, _ = _load_scripts()
    if slack is None:
        return []
    channels = [c.strip() for c in os.environ.get("SLACK_COMMS_CHANNELS", DEFAULT_SLACK_CHANNELS).split(",") if c.strip()]
    if not channels:
        return []
    try:
        slack.load_env()
        # Resolve channel id -> #name once.
        names = {}
        try:
            listing = slack.api_call("conversations.list", params={"types": "public_channel", "limit": 200})
            for ch in listing.get("channels", []):
                names[ch["id"]] = ch.get("name")
        except BaseException:  # noqa: B036 - api_call may sys.exit
            pass

        out = []
        for channel_id in channels:
            try:
                data = slack.api_call("conversations.history", params={"channel": channel_id, "limit": limit})
            except BaseException:  # noqa: B036 - api_call may sys.exit on error
                continue
            label = f"#{names.get(channel_id, channel_id)}"
            for msg in data.get("messages", []):
                if msg.get("subtype") == "channel_join":
                    continue
                out.append({
                    "from": "Slack",
                    "channel": label,
                    "preview": _truncate(msg.get("text", "")),
                    "unread": False,
                    "ts": _epoch(msg.get("ts")),
                })
        return out
    except BaseException:  # noqa: B036 - belt and suspenders
        return []


def fetch_mail(top=4):
    """Recent inbox messages via Microsoft Graph. Never raises."""
    _, ms365 = _load_scripts()
    if ms365 is None:
        return []
    try:
        ms365.load_env()
        upn = os.environ.get("MS365_USER_UPN")
        if not upn:
            return []
        token = ms365.get_token()
        import urllib.parse

        params = urllib.parse.urlencode({
            "$orderby": "receivedDateTime desc",
            "$top": str(top),
            "$select": "subject,from,receivedDateTime,isRead",
        })
        result = ms365.graph_request(f"/users/{upn}/messages?{params}", token)
        if not result:
            return []
        out = []
        for msg in result.get("value", []):
            sender = (msg.get("from", {}).get("emailAddress", {}) or {}).get("name") or "Mail"
            out.append({
                "from": "M365",
                "channel": "inbox",
                "preview": _truncate(f"{sender}: {msg.get('subject', '(no subject)')}"),
                "unread": not msg.get("isRead", True),
                "ts": _epoch(msg.get("receivedDateTime")),
            })
        return out
    except Exception:
        return []


def _sim_messages():
    return [
        {"from": "Slack", "channel": "#build", "preview": "Sentinel cert checklist updated · 2 items left", "unread": True, "ts": 0},
        {"from": "M365", "channel": "inbox", "preview": "2 solicitation notices flagged for triage", "unread": True, "ts": 0},
        {"from": "Resend", "channel": "outreach", "preview": "25 warm-intro emails queued for send", "unread": False, "ts": 0},
        {"from": "Slack", "channel": "#pipeline", "preview": "Meridian Defense moved to hot", "unread": False, "ts": 0},
    ]


def build_comms(limit=6):
    """Merge live Slack + Graph feeds; fall back to a labeled SIM stub."""
    messages = fetch_slack() + fetch_mail()
    if messages:
        messages.sort(key=lambda m: m.get("ts", 0), reverse=True)
        trimmed = messages[:limit]
        for m in trimmed:
            m.pop("ts", None)
        return {
            "simulated": False,
            "unread": sum(1 for m in trimmed if m.get("unread")),
            "messages": trimmed,
        }

    stub = _sim_messages()
    for m in stub:
        m.pop("ts", None)
    return {
        "simulated": True,
        "unread": sum(1 for m in stub if m.get("unread")),
        "messages": stub,
    }
