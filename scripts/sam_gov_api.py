#!/usr/bin/env python3
"""
SAM.gov Opportunities scanner for Vulnaguard / Sentinel CMMC.

Queries vulnaguard-capture-os's deployed API (not SAM.gov directly — see
2026-07-05 decisions/log.md entry), deduplicates against a seen-IDs cache,
captures POC contacts to a CSV for follow-up outreach, and posts new
high-scoring opportunities to Slack.

Usage:
    python3 scripts/sam_gov_api.py             # run scan, post to Slack
    python3 scripts/sam_gov_api.py --dry-run   # print without posting
    python3 scripts/sam_gov_api.py --reset     # clear the seen-IDs cache
    python3 scripts/sam_gov_api.py --days 7    # look back N days (default 3)
    python3 scripts/sam_gov_api.py --min-score 20  # relevance threshold (default 40)

Reads SLACK_BOT_TOKEN, SLACK_GOV_CONTRACTS_CHANNEL from .env.
Cache file   : leads/sam_gov_seen.json
Contacts CSV : leads/sam_gov_contacts.csv
"""
import argparse
import csv
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

# vulnaguard-capture-os is the canonical owner of SAM.gov querying — it
# harvests title-keyword + all NAICS/PSC codes server-side and returns
# already-scored opportunities. This script no longer talks to SAM.gov
# directly (see decisions/log.md, 2026-07-05).
CAPTURE_OS_API_BASE = "https://contract-hunter-production-c52f.up.railway.app/api"

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = REPO_ROOT / "leads" / "sam_gov_seen.json"
CONTACTS_CSV = REPO_ROOT / "leads" / "sam_gov_contacts.csv"

CONTACTS_HEADER = [
    "date_found", "notice_id", "solicitation_number", "title",
    "agency", "poc_type", "poc_name", "poc_email", "poc_phone",
    "posted_date", "due_date", "score", "sam_url",
]


# ---------------------------------------------------------------------------
# Env / cache / contacts
# ---------------------------------------------------------------------------

def load_env():
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            pass
    return {"seen": [], "last_run": None}


def save_cache(cache: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def append_contacts(rows: list[dict]):
    """Append POC rows to the contacts CSV, creating it with headers if needed."""
    if not rows:
        return
    CONTACTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    write_header = not CONTACTS_CSV.exists()
    with CONTACTS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CONTACTS_HEADER, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Capture OS API
# ---------------------------------------------------------------------------

def capture_os_search(days: int, min_score: int, keyword: str = "cybersecurity",
                       limit: int = 200) -> list[dict]:
    """One call covers title-keyword + all NAICS/PSC codes server-side —
    replaces this script's old per-code/per-phrase SAM.gov query loop."""
    params = {"keyword": keyword, "days": days, "min_score": min_score, "limit": limit}
    url = f"{CAPTURE_OS_API_BASE}/opportunities/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Capture OS API HTTP {e.code}: {body[:300]}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Capture OS API error: {e}", file=sys.stderr)
        return []


def opportunity_url(opp: dict) -> str:
    return opp.get("source_url") or f"https://sam.gov/opp/{opp.get('notice_id', '')}/view"


def extract_contacts(opp: dict, today: str) -> list[dict]:
    """Pull all POC entries from an opportunity into flat contact rows."""
    pocs = opp.get("point_of_contact") or []
    if not pocs:
        return []
    base = {
        "date_found": today,
        "notice_id": opp.get("notice_id") or "",
        "solicitation_number": opp.get("solicitation_number") or "",
        "title": opp.get("title") or "",
        "agency": opp.get("agency") or "",
        "posted_date": opp.get("posted_date") or "",
        "due_date": opp.get("due_date") or "",
        "score": opp.get("fit_score") or 0,
        "sam_url": opportunity_url(opp),
    }
    rows = []
    for poc in pocs:
        row = {**base}
        row["poc_type"] = poc.get("type") or ""
        row["poc_name"] = poc.get("name") or ""
        row["poc_email"] = poc.get("email") or ""
        row["poc_phone"] = poc.get("phone") or ""
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Slack
# ---------------------------------------------------------------------------

def slack_post(channel: str, blocks: list, token: str, fallback_text: str):
    url = "https://slack.com/api/chat.postMessage"
    payload = json.dumps({
        "channel": channel,
        "text": fallback_text,
        "blocks": blocks,
        "unfurl_links": False,
    }).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode())
    if not result.get("ok"):
        print(f"Slack error: {result.get('error')}", file=sys.stderr)


def build_slack_blocks(opp: dict) -> tuple[list, str]:
    title = opp.get("title") or "Untitled"
    agency = opp.get("agency") or "Unknown Agency"
    sol_num = opp.get("solicitation_number") or "N/A"
    posted = opp.get("posted_date") or "N/A"
    opp_type = opp.get("notice_type") or "N/A"
    naics = ", ".join(opp.get("naics") or []) or "N/A"
    psc = ", ".join(opp.get("psc") or []) or "N/A"
    set_aside = opp.get("set_aside") or "None"
    due_date = opp.get("due_date") or "N/A"
    score = opp.get("fit_score") or 0
    link = opportunity_url(opp)

    pocs = opp.get("point_of_contact") or []
    poc_line = "N/A"
    if pocs:
        p = pocs[0]
        parts = [x for x in [p.get("name"), p.get("email"), p.get("phone")] if x]
        poc_line = " | ".join(parts) if parts else "N/A"

    if score >= 60:
        tier = "🔥 HIGH MATCH"
    elif score >= 40:
        tier = "⚡ STRONG MATCH"
    else:
        tier = "📋 POTENTIAL"

    fallback = f"{tier}: {title} — {agency}"

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"{tier}: {title[:140]}", "emoji": True},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Agency*\n{agency}"},
                {"type": "mrkdwn", "text": f"*Solicitation #*\n`{sol_num}`"},
                {"type": "mrkdwn", "text": f"*Type*\n{opp_type}"},
                {"type": "mrkdwn", "text": f"*NAICS*\n{naics}"},
                {"type": "mrkdwn", "text": f"*PSC*\n{psc}"},
                {"type": "mrkdwn", "text": f"*Posted*\n{posted}"},
                {"type": "mrkdwn", "text": f"*Due / Closes*\n{due_date}"},
                {"type": "mrkdwn", "text": f"*Set-Aside*\n{set_aside}"},
                {"type": "mrkdwn", "text": f"*Relevance Score*\n{score}/100"},
            ],
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Primary Contact*\n{poc_line}"},
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "📁 Contact saved to `leads/sam_gov_contacts.csv` for follow-up outreach"},
            ],
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "View on SAM.gov"},
                    "url": link,
                    "style": "primary",
                }
            ],
        },
        {"type": "divider"},
    ]

    return blocks, fallback


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SAM.gov contract scanner (via vulnaguard-capture-os)")
    parser.add_argument("--dry-run", action="store_true", help="Print results, don't post to Slack")
    parser.add_argument("--reset", action="store_true", help="Clear seen-IDs cache")
    parser.add_argument("--days", type=int, default=3, help="Days to look back (default 3)")
    parser.add_argument("--min-score", type=int, default=40, help="Minimum relevance score (default 40)")
    args = parser.parse_args()

    load_env()

    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_GOV_CONTRACTS_CHANNEL", "gov-contracts")

    if args.reset:
        save_cache({"seen": [], "last_run": None})
        print("Cache cleared.")
        return

    cache = load_cache()

    today_dt = datetime.now(timezone.utc)
    today_str = today_dt.strftime("%Y-%m-%d")

    print(f"Querying vulnaguard-capture-os | lookback {args.days}d | min score {args.min_score}")

    seen_ids: set = set(cache.get("seen") or [])
    opportunities = capture_os_search(days=args.days, min_score=args.min_score)
    print(f"Capture OS returned {len(opportunities)} opportunities")

    scored = [o for o in opportunities if o.get("notice_id") not in seen_ids]
    scored.sort(key=lambda o: o.get("fit_score") or 0, reverse=True)
    print(f"New opportunities above threshold: {len(scored)}")

    if not scored:
        print("No new relevant opportunities found.")
        if not args.dry_run:
            cache["last_run"] = today_dt.isoformat()
            save_cache(cache)
        return

    # Post summary header to Slack
    if not args.dry_run and slack_token:
        now_str = today_dt.strftime("%Y-%m-%d %H:%M UTC")
        header_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*:satellite: SAM.gov Contract Scan — {now_str}*\n"
                        f"Found *{len(scored)}* new relevant opportunities "
                        f"(lookback: {args.days}d, min score: {args.min_score})\n"
                        f"_Contacts saved to `leads/sam_gov_contacts.csv` for follow-up outreach_"
                    ),
                },
            },
            {"type": "divider"},
        ]
        slack_post(slack_channel, header_blocks, slack_token, f"SAM.gov scan: {len(scored)} new opportunities")

    new_ids = []
    all_contact_rows = []

    for opp in scored:
        nid = opp.get("notice_id")
        title = opp.get("title") or "Untitled"
        score = opp.get("fit_score") or 0

        if args.dry_run:
            pocs = opp.get("point_of_contact") or []
            poc_str = "; ".join(
                f"{p.get('name', '?')} <{p.get('email', '')}>" for p in pocs
            ) or "No POC listed"
            print(f"\n[SCORE {score}] {title}")
            print(f"  Agency  : {opp.get('agency')}")
            print(f"  Sol #   : {opp.get('solicitation_number')}")
            print(f"  Type    : {opp.get('notice_type')}")
            print(f"  NAICS   : {opp.get('naics')}  |  PSC: {opp.get('psc')}")
            print(f"  Posted  : {opp.get('posted_date')}")
            print(f"  Closes  : {opp.get('due_date')}")
            print(f"  POC     : {poc_str}")
            print(f"  URL     : {opportunity_url(opp)}")
        else:
            contact_rows = extract_contacts(opp, today_str)
            all_contact_rows.extend(contact_rows)

            if slack_token:
                blocks, fallback = build_slack_blocks(opp)
                slack_post(slack_channel, blocks, slack_token, fallback)
                print(f"  Posted: [{score}] {title}")

            if nid:
                new_ids.append(nid)

    if args.dry_run:
        print(f"\nDry run complete — no data written.")
        return

    # Save contacts and update cache
    if all_contact_rows:
        append_contacts(all_contact_rows)
        print(f"\nSaved {len(all_contact_rows)} contacts to {CONTACTS_CSV}")

    cache["seen"] = list(seen_ids | set(new_ids))
    cache["last_run"] = today_dt.isoformat()
    save_cache(cache)

    print(f"Done. {len(new_ids)} opportunities marked as seen.")


if __name__ == "__main__":
    main()
