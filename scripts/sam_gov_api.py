#!/usr/bin/env python3
"""
SAM.gov Opportunities scanner for Vulnaguard / Sentinel CMMC.

Searches the SAM.gov Opportunities v2 API for cybersecurity/CMMC-relevant
federal contracts, deduplicates against a seen-IDs cache, scores by
relevance, captures POC contacts to a CSV for follow-up outreach, and
posts new high-scoring opportunities to Slack.

Usage:
    python3 scripts/sam_gov_api.py             # run scan, post to Slack
    python3 scripts/sam_gov_api.py --dry-run   # print without posting
    python3 scripts/sam_gov_api.py --reset     # clear the seen-IDs cache
    python3 scripts/sam_gov_api.py --days 7    # look back N days (default 3)
    python3 scripts/sam_gov_api.py --min-score 20  # relevance threshold (default 25)

Reads SAM_GOV_API_KEY, SLACK_BOT_TOKEN, SLACK_GOV_CONTRACTS_CHANNEL from .env.
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

SAM_API_BASE = "https://api.sam.gov/opportunities/v2/search"
SAM_OPP_BASE = "https://sam.gov/opp"

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = REPO_ROOT / "leads" / "sam_gov_seen.json"
CONTACTS_CSV = REPO_ROOT / "leads" / "sam_gov_contacts.csv"

# Keyword searches — only meaningful when title also contains the term.
# Avoid broad DFARS/CMMC queries: those clauses appear in ALL DoD solicitations
# as mandatory boilerplate, so every rubber gasket and O-ring "matches".
KEYWORD_QUERIES = [
    "cybersecurity assessment",
    "information security",
    "CMMC certification",
    "cyber compliance",
    "zero trust",
    "penetration testing",
    "vulnerability assessment",
    "security operations center",
    "incident response",
    "NIST 800-171 assessment",
]

# NAICS codes to query directly — pre-filtered at the API level to IT/cyber contracts
NAICS_QUERIES = [
    "541512",  # Computer Systems Design Services — primary
    "541519",  # Other Computer Related Services
    "541690",  # Other Scientific and Technical Consulting
    "541611",  # Admin Mgmt Consulting
    "541990",  # All Other Prof/Scientific/Technical Services
    "561621",  # Security Systems Services
    "611420",  # Computer Training
]

# PSC codes to query — D-series = IT; R-series = professional support
PSC_QUERIES = [
    "D310",  # Cyber Security
    "D307",  # IT and Telecom — IT/Telecom Operations and Maintenance
    "R425",  # Support: Policy Review/Development
    "R408",  # Support: Program Management/Support
]

CYBER_NAICS = {
    "541512",  # Computer Systems Design Services — primary
    "541519",  # Other Computer Related Services
    "541690",  # Other Scientific and Technical Consulting
    "541611",  # Admin Mgmt and General Mgmt Consulting
    "541990",  # All Other Professional, Scientific, and Technical Services
    "561621",  # Security Systems Services
    "611420",  # Computer Training
    "541511",  # Custom Computer Programming Services
    "541513",  # Computer Facilities Management
    "541715",  # Research and Development in Physical, Engineering, and Life Sciences
    "541330",  # Engineering Services
}

# PSC (Product/Service Codes) — DoD/federal procurement categories for cyber work
CYBER_PSC = {"D310", "D307", "R425", "R408"}

# NAICS prefixes that are clearly non-IT — skip DoD bonus and derank
HARDWARE_NAICS_PREFIXES = (
    "23",   # construction
    "31", "32", "33",  # manufacturing
    "48", "49",  # transportation/warehousing
    "72",   # food/accommodation
    "56172",  # janitorial
    "811",  # repair services
    "324",  # petroleum
    "326",  # plastics/rubber
    "332", "333", "334", "335", "336",  # fabricated metal / machinery / electronics / transport equip
)

DOD_AGENCIES = [
    "DEPT OF DEFENSE", "DEPARTMENT OF DEFENSE", "DEPT OF THE ARMY",
    "DEPT OF THE NAVY", "DEPT OF THE AIR FORCE", "MARINE CORPS",
    "DISA", "DIA", "NSA", "DARPA", "SOCOM", "CENTCOM", "CYBERCOM",
    "DEFENSE INFORMATION SYSTEMS", "DEFENSE INTELLIGENCE",
    "DEFENSE CONTRACT", "DEFENSE LOGISTICS",
]

CONTACTS_HEADER = [
    "date_found", "notice_id", "solicitation_number", "title",
    "agency", "poc_type", "poc_name", "poc_email", "poc_phone",
    "posted_date", "archive_date", "score", "sam_url",
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
# SAM.gov API
# ---------------------------------------------------------------------------

def sam_search(query: str, posted_from: str, posted_to: str, api_key: str,
               naics_code: str | None = None, psc_code: str | None = None,
               limit: int = 100) -> list[dict]:
    params = {
        "api_key": api_key,
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "active": "Yes",
        "limit": limit,
    }
    if naics_code:
        params["naicsCode"] = naics_code
    elif psc_code:
        params["psc"] = psc_code
    else:
        params["q"] = query
    url = SAM_API_BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("opportunitiesData") or []
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"SAM.gov HTTP {e.code} for query '{query}': {body[:300]}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"SAM.gov error for query '{query}': {e}", file=sys.stderr)
        return []


# ---------------------------------------------------------------------------
# Relevance scoring
# ---------------------------------------------------------------------------

def is_hardware_naics(naics: str) -> bool:
    return any(naics.startswith(p) for p in HARDWARE_NAICS_PREFIXES)


def score_opportunity(opp: dict) -> int:
    title = (opp.get("title") or "").lower()
    agency = (opp.get("fullParentPathName") or "").upper()
    naics = str(opp.get("naicsCode") or "")
    set_aside = (opp.get("typeOfSetAsideDescription") or "").lower()
    opp_type = (opp.get("type") or "").lower()

    # --- Title keyword score ---
    # Only titles are reliable signals. Description-body keyword matches
    # are polluted by mandatory DFARS/CMMC boilerplate on all DoD contracts.
    title_score = 0
    if "cmmc" in title:
        title_score += 50
    if "nist 800-171" in title or "nist sp 800-171" in title:
        title_score += 40
    if "dfars" in title:
        title_score += 25
    if "cui" in title and ("security" in title or "protect" in title or "handling" in title):
        title_score += 25
    if "zero trust" in title:
        title_score += 25
    if "cybersecurity" in title or "cyber security" in title:
        title_score += 20
    if "information security" in title:
        title_score += 18
    if "information assurance" in title:
        title_score += 18
    if "accreditation" in title and "cyber" not in title:
        title_score += 10  # accreditation alone is weaker signal
    if "risk management framework" in title or " rmf " in title:
        title_score += 18
    if "security assessment" in title or "security audit" in title:
        title_score += 15
    if "penetration test" in title or "pen test" in title or "pentest" in title:
        title_score += 20
    if "security operations" in title or " soc " in title:
        title_score += 15
    if "vulnerability" in title:
        title_score += 12
    if "incident response" in title:
        title_score += 12
    if "managed security" in title or "mssp" in title:
        title_score += 15
    if "cyber" in title and "security" in title:
        title_score += 10

    # --- NAICS / PSC baseline score ---
    # These are pre-filtered at the API level to IT/cyber scope.
    # Give a baseline so they clear the threshold even without title keywords.
    psc = str(opp.get("classificationCode") or "")
    naics_score = 25 if naics in CYBER_NAICS else 0
    psc_score = 35 if psc in CYBER_PSC else 0  # PSC D310 = Cyber Security is gold
    code_score = max(naics_score, psc_score)

    # Must have at least one signal to proceed
    base = title_score + code_score
    if base == 0:
        return 0

    score = base

    # --- Context bonuses ---
    is_dod = any(a in agency for a in DOD_AGENCIES)
    if is_dod and not is_hardware_naics(naics):
        score += 15

    if "small business" in set_aside or "8(a)" in set_aside or "8a" in set_aside:
        score += 8

    if "sources sought" in opp_type or "sources sought" in title:
        score += 5

    return score


def opportunity_url(opp: dict) -> str:
    notice_id = opp.get("noticeId") or ""
    return f"{SAM_OPP_BASE}/{notice_id}/view"


def extract_contacts(opp: dict, score: int, today: str) -> list[dict]:
    """Pull all POC entries from an opportunity into flat contact rows."""
    pocs = opp.get("pointOfContact") or []
    if not pocs:
        return []
    base = {
        "date_found": today,
        "notice_id": opp.get("noticeId") or "",
        "solicitation_number": opp.get("solicitationNumber") or "",
        "title": opp.get("title") or "",
        "agency": opp.get("fullParentPathName") or "",
        "posted_date": opp.get("postedDate") or "",
        "archive_date": opp.get("archiveDate") or "",
        "score": score,
        "sam_url": opportunity_url(opp),
    }
    rows = []
    for poc in pocs:
        row = {**base}
        row["poc_type"] = poc.get("type") or ""
        row["poc_name"] = poc.get("fullName") or poc.get("name") or ""
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


def build_slack_blocks(opp: dict, score: int) -> tuple[list, str]:
    title = opp.get("title") or "Untitled"
    agency = opp.get("fullParentPathName") or "Unknown Agency"
    sol_num = opp.get("solicitationNumber") or "N/A"
    posted = opp.get("postedDate") or "N/A"
    opp_type = opp.get("type") or opp.get("baseType") or "N/A"
    naics = opp.get("naicsCode") or "N/A"
    psc = opp.get("classificationCode") or "N/A"
    set_aside = opp.get("typeOfSetAsideDescription") or "None"
    archive_date = opp.get("archiveDate") or "N/A"
    link = opportunity_url(opp)

    # Primary POC for quick display
    pocs = opp.get("pointOfContact") or []
    poc_line = "N/A"
    if pocs:
        p = pocs[0]
        name = p.get("fullName") or p.get("name") or ""
        email = p.get("email") or ""
        phone = p.get("phone") or ""
        parts = [x for x in [name, email, phone] if x]
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
                {"type": "mrkdwn", "text": f"*Closes / Archives*\n{archive_date}"},
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
    parser = argparse.ArgumentParser(description="SAM.gov contract scanner")
    parser.add_argument("--dry-run", action="store_true", help="Print results, don't post to Slack")
    parser.add_argument("--reset", action="store_true", help="Clear seen-IDs cache")
    parser.add_argument("--days", type=int, default=3, help="Days to look back (default 3)")
    parser.add_argument("--min-score", type=int, default=40, help="Minimum relevance score (default 40)")
    args = parser.parse_args()

    load_env()

    api_key = os.environ.get("SAM_GOV_API_KEY")
    if not api_key:
        print("SAM_GOV_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_GOV_CONTRACTS_CHANNEL", "gov-contracts")

    if args.reset:
        save_cache({"seen": [], "last_run": None})
        print("Cache cleared.")
        return

    cache = load_cache()

    today_dt = datetime.now(timezone.utc)
    posted_to = today_dt.strftime("%m/%d/%Y")
    posted_from = (today_dt - timedelta(days=args.days)).strftime("%m/%d/%Y")
    today_str = today_dt.strftime("%Y-%m-%d")

    print(f"Searching SAM.gov {posted_from} → {posted_to} | min score {args.min_score}")

    seen_ids: set = set(cache.get("seen") or [])
    all_opps: dict[str, dict] = {}

    # PSC-based searches — most targeted: D310 = Cyber Security is the money code
    print("  [PSC searches]")
    for psc in PSC_QUERIES:
        results = sam_search("", posted_from, posted_to, api_key, psc_code=psc)
        print(f"  PSC {psc} → {len(results)} results")
        for opp in results:
            nid = opp.get("noticeId")
            if nid and nid not in all_opps:
                all_opps[nid] = opp

    # NAICS-based searches — pre-filtered to IT/cyber service contracts
    print("  [NAICS searches]")
    for naics in NAICS_QUERIES:
        results = sam_search("", posted_from, posted_to, api_key, naics_code=naics)
        print(f"  NAICS {naics} → {len(results)} results")
        for opp in results:
            nid = opp.get("noticeId")
            if nid and nid not in all_opps:
                all_opps[nid] = opp

    # Keyword searches — narrow phrases only found in genuine cyber solicitation titles
    print("  [Keyword searches]")
    for query in KEYWORD_QUERIES:
        results = sam_search(query, posted_from, posted_to, api_key)
        print(f"  '{query}' → {len(results)} results")
        for opp in results:
            nid = opp.get("noticeId")
            if nid and nid not in all_opps:
                all_opps[nid] = opp

    print(f"Total unique opportunities: {len(all_opps)}")

    scored = []
    for nid, opp in all_opps.items():
        if nid in seen_ids:
            continue
        s = score_opportunity(opp)
        if s >= args.min_score:
            scored.append((s, opp))

    scored.sort(key=lambda x: x[0], reverse=True)
    print(f"New opportunities above threshold: {len(scored)}")

    if not scored:
        print("No new relevant opportunities found.")
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

    for score, opp in scored:
        nid = opp.get("noticeId")
        title = opp.get("title") or "Untitled"

        # Extract contacts regardless of dry-run (always capture)
        contact_rows = extract_contacts(opp, score, today_str)
        all_contact_rows.extend(contact_rows)

        if args.dry_run:
            pocs = opp.get("pointOfContact") or []
            poc_str = "; ".join(
                f"{p.get('fullName') or p.get('name', '?')} <{p.get('email', '')}>"
                for p in pocs
            ) or "No POC listed"
            print(f"\n[SCORE {score}] {title}")
            print(f"  Agency  : {opp.get('fullParentPathName')}")
            print(f"  Sol #   : {opp.get('solicitationNumber')}")
            print(f"  Type    : {opp.get('type')}")
            print(f"  NAICS   : {opp.get('naicsCode')}  |  PSC: {opp.get('classificationCode')}")
            print(f"  Posted  : {opp.get('postedDate')}")
            print(f"  Closes  : {opp.get('archiveDate')}")
            print(f"  POC     : {poc_str}")
            print(f"  URL     : {opportunity_url(opp)}")
        else:
            if slack_token:
                blocks, fallback = build_slack_blocks(opp, score)
                slack_post(slack_channel, blocks, slack_token, fallback)
                print(f"  Posted: [{score}] {title}")

        if nid:
            new_ids.append(nid)

    # Save all contacts to CSV
    if all_contact_rows:
        append_contacts(all_contact_rows)
        print(f"\nSaved {len(all_contact_rows)} contacts to {CONTACTS_CSV}")

    # Update cache
    cache["seen"] = list(seen_ids | set(new_ids))
    cache["last_run"] = today_dt.isoformat()
    save_cache(cache)

    print(f"Done. {len(new_ids)} opportunities marked as seen.")


if __name__ == "__main__":
    main()
