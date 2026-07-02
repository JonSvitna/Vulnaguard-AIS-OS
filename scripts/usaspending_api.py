#!/usr/bin/env python3
"""
USASpending.gov scraper — reverse-engineer small federal cyber contracts.

Default mode finds individual awards in a startup-friendly dollar range so you
can see what agencies actually bought (vuln assessments, pen tests, CMMC work)
and who won them. Use this to spot work you could deliver now, build past
performance, and work up to larger contracts.

Usage:
    python3 scripts/usaspending_api.py                         # opportunities (default)
    python3 scripts/usaspending_api.py --dry-run
    python3 scripts/usaspending_api.py --min-amount 5000 --max-amount 75000
    python3 scripts/usaspending_api.py --months 18
    python3 scripts/usaspending_api.py --all-agencies          # not just DoD
    python3 scripts/usaspending_api.py --mode companies      # legacy: big awardees

No API key required. Public USASpending API.
Output CSV : leads/usaspending_opportunities.csv  (default)
             leads/usaspending_awardees.csv       (--mode companies)
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API_BASE = "https://api.usaspending.gov/api/v2"
AWARD_SEARCH = f"{API_BASE}/search/spending_by_award/"
RECIPIENT_SEARCH = f"{API_BASE}/search/spending_by_category/recipient/"
RECIPIENT_PROFILE = f"{API_BASE}/recipient"

REPO_ROOT = Path(__file__).resolve().parent.parent
OPPORTUNITIES_CSV = REPO_ROOT / "leads" / "usaspending_opportunities.csv"
AWARDEES_CSV = REPO_ROOT / "leads" / "usaspending_awardees.csv"

CONTRACT_AWARD_TYPES = ["A", "B", "C", "D"]
DOD_AGENCY = {"type": "awarding", "tier": "toptier", "name": "Department of Defense"}

# Keyword searches — services a startup CMMC/cyber shop could replicate.
SERVICE_KEYWORDS = [
    "vulnerability assessment",
    "vulnerability scan",
    "penetration test",
    "pen test",
    "cybersecurity assessment",
    "cyber assessment",
    "security assessment",
    "NIST 800-171",
    "CMMC",
    "incident response",
    "security audit",
    "compliance assessment",
    "system security plan",
    "CUI compliance",
    "DFARS 252.204",
    "risk assessment",
    "cyber compliance",
]

CYBER_NAICS = {"541512", "541519", "541690", "541611", "541990", "561621"}
CYBER_PSC = {"D310", "D307", "R425", "R408"}

SKIP_NAMES = {"MULTIPLE RECIPIENTS", "MULTIPLE RECIPIENTS/MULTIPLE RECIPIENTS"}

# Description noise — not cyber services work.
NOISE_PATTERNS = [
    r"\bcone penetration\b",
    r"\bgeophysical\b",
    r"\bsoil test\b",
    r"\bembankment\b",
    r"\bmasonry\b",
    r"\bconstruction\b",
    r"\bbuilding equip",
    r"\bmaintenance of maintenance buildings\b",
    r"\bradiant mercury\b",
    r"\btactical security assessment suite\b",
    r"\bfire risk assessment\b",
    r"\bhangar fire\b",
    r"\blaptop",
    r"\bprojector\b",
    r"\bcrash cart\b",
    r"\bfor \w+ upgrades\b",
    r"\bcisco \d+ switch\b",
    r"\bwings penetration test\b",  # aircraft component testing, not cyber
]

AWARD_FIELDS = [
    "Award ID",
    "Recipient Name",
    "Award Amount",
    "Description",
    "Start Date",
    "End Date",
    "Awarding Agency",
    "Awarding Sub Agency",
    "NAICS",
    "PSC",
    "Contract Award Type",
    "Prime Award Recipient UEI",
]

OPPORTUNITY_HEADER = [
    "date_scraped",
    "award_id",
    "award_amount",
    "replicability",
    "service_type",
    "description",
    "awardee",
    "awardee_uei",
    "agency",
    "sub_agency",
    "naics",
    "psc",
    "start_date",
    "match_source",
    "score",
    "award_url",
]

AWARDEE_HEADER = [
    "date_scraped",
    "company_name",
    "uei",
    "duns",
    "recipient_id",
    "city",
    "state",
    "zip",
    "parent_company",
    "business_types",
    "award_amount_12mo",
    "match_source",
    "small_business",
    "usaspending_url",
]


def load_env():
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def api_post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    time.sleep(0.5)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def api_get(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    time.sleep(0.3)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Profile error: {e}", file=sys.stderr)
        return None


def date_range(months: int) -> tuple[str, str]:
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=months * 30)
    return start.isoformat(), end.isoformat()


def naics_code(naics_field) -> str:
    if isinstance(naics_field, dict):
        return str(naics_field.get("code") or "")
    return str(naics_field or "")


def psc_code(psc_field) -> str:
    if isinstance(psc_field, dict):
        return str(psc_field.get("code") or "")
    return str(psc_field or "")


def award_url(row: dict) -> str:
    gid = row.get("generated_internal_id") or ""
    if gid:
        return f"https://www.usaspending.gov/award/{gid}"
    award_id = row.get("Award ID") or ""
    return f"https://www.usaspending.gov/search/?hash={award_id}" if award_id else ""


def is_noise(description: str) -> bool:
    desc = description.lower()
    return any(re.search(p, desc) for p in NOISE_PATTERNS)


def classify_service(description: str) -> str:
    desc = description.lower()
    if any(k in desc for k in ("vulnerability", "vuln scan", "nessus", "qualys")):
        return "vulnerability_assessment"
    if any(k in desc for k in ("penetration test", "pen test", "pentest", "red team")):
        return "penetration_testing"
    if any(k in desc for k in ("cmmc", "nist 800-171", "nist sp 800-171", "dfars 252.204", "cui")):
        return "compliance_assessment"
    if any(k in desc for k in ("incident response", "ir support", "forensic")):
        return "incident_response"
    if any(k in desc for k in ("license", "subscription", "software")):
        return "software_or_license"
    if any(k in desc for k in ("assessment", "audit", "compliance", "cybersecurity", "cyber")):
        return "cyber_consulting"
    return "other"


def score_opportunity(row: dict, match_source: str) -> int:
    """Higher = more likely replicable cyber services work for a startup."""
    desc = (row.get("Description") or "").lower()
    amount = float(row.get("Award Amount") or 0)
    naics = naics_code(row.get("NAICS"))
    psc = psc_code(row.get("PSC"))

    if is_noise(desc):
        return 0

    score = 0

    # Strong service signals in the description.
    signals = [
        ("vulnerability assessment", 40),
        ("vulnerability scan", 35),
        ("database vulnerability", 40),
        ("penetration test", 35),
        ("pen test", 30),
        ("pentest", 30),
        ("cybersecurity assessment", 35),
        ("cyber assessment", 30),
        ("cyber risk assessment", 35),
        ("security assessment", 20),
        ("nist 800-171", 40),
        ("cmmc", 35),
        ("compliance assessment", 25),
        ("security audit", 25),
        ("incident response", 25),
        ("system security plan", 30),
        ("cui compliance", 25),
        ("cui ", 15),
        ("dfars 252.204", 20),
        ("cyber compliance", 30),
        ("cyber security", 20),
    ]
    for term, pts in signals:
        if term in desc:
            score += pts

    # "risk assessment" only counts with cyber context — avoids fire safety noise.
    if "risk assessment" in desc and any(k in desc for k in ("cyber", "security", "information", "compliance")):
        score += 15

    # Code alignment.
    if naics in CYBER_NAICS:
        score += 15
    if psc in CYBER_PSC:
        score += 20

    # Sweet spot for startup entry — not too small, not prime-scale.
    if 5_000 <= amount <= 25_000:
        score += 20
    elif 25_000 < amount <= 75_000:
        score += 15
    elif 75_000 < amount <= 150_000:
        score += 5

    # Software/license buys are useful intel but harder to replicate as a services shop.
    if classify_service(desc) == "software_or_license":
        score = max(score - 15, 10)

    # NAICS/PSC-only hits need real cyber language in the description.
    if score < 25 and match_source.startswith(("naics:", "psc:")):
        return 0

    if match_source.startswith("keyword:"):
        score += 5

    return score


def replicability_tier(score: int, service_type: str) -> str:
    if score == 0:
        return "skip"
    if service_type == "software_or_license":
        return "intel_only"
    if score >= 50:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def fetch_awards(
    match_source: str,
    filters: dict,
    min_amount: float,
    max_amount: float,
    page_limit: int,
) -> list[dict]:
    filters = {
        **filters,
        "award_type_codes": CONTRACT_AWARD_TYPES,
        "award_amounts": [{"lower_bound": min_amount, "upper_bound": max_amount}],
    }

    collected: list[dict] = []
    page = 1

    while len(collected) < page_limit:
        batch = min(100, page_limit - len(collected))
        payload = {
            "filters": filters,
            "fields": AWARD_FIELDS,
            "limit": batch,
            "page": page,
            "sort": "Start Date",
            "order": "desc",
        }
        try:
            data = api_post(AWARD_SEARCH, payload)
        except Exception as e:
            print(f"  {match_source} page {page} error: {e}", file=sys.stderr)
            break

        results = data.get("results") or []
        if not results:
            break

        for row in results:
            row["_match_source"] = match_source
            collected.append(row)
            if len(collected) >= page_limit:
                break

        meta = data.get("page_metadata") or {}
        if not meta.get("hasNext"):
            break
        page += 1

    return collected


def run_opportunities(args):
    start_date, end_date = date_range(args.months)
    dod_only = not args.all_agencies
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    base = {"time_period": [{"start_date": start_date, "end_date": end_date}]}
    if dod_only:
        base["agencies"] = [DOD_AGENCY]

    scope = "DoD" if dod_only else "all agencies"
    print(f"USASpending opportunity scan: {start_date} → {end_date} | {scope}")
    print(f"  Award range: ${args.min_amount:,.0f} – ${args.max_amount:,.0f}")
    print(f"  Limit {args.limit} per query | min score {args.min_score}")

    all_awards: dict[str, dict] = {}

    # Keyword passes — find described services work.
    print("  [Keyword searches]")
    for kw in SERVICE_KEYWORDS:
        source = f"keyword:{kw}"
        filters = {**base, "keywords": [kw]}
        rows = fetch_awards(source, filters, args.min_amount, args.max_amount, args.limit)
        print(f"    '{kw}' → {len(rows)} raw")
        for row in rows:
            aid = row.get("Award ID") or row.get("generated_internal_id")
            if aid and aid not in all_awards:
                all_awards[aid] = row

    # PSC D310 small cyber awards — score descriptions locally.
    print("  [PSC D310 awards]")
    psc_rows = fetch_awards(
        "psc:D310",
        {**base, "psc_codes": ["D310"]},
        args.min_amount,
        args.max_amount,
        args.limit,
    )
    print(f"    → {len(psc_rows)} raw")
    for row in psc_rows:
        aid = row.get("Award ID") or row.get("generated_internal_id")
        if aid and aid not in all_awards:
            all_awards[aid] = row

    # NAICS 541512/541519 IT services in range.
    for naics in ("541512", "541519"):
        print(f"  [NAICS {naics} awards]")
        naics_rows = fetch_awards(
            f"naics:{naics}",
            {**base, "naics_codes": {"require": [naics]}},
            args.min_amount,
            args.max_amount,
            args.limit,
        )
        print(f"    → {len(naics_rows)} raw")
        for row in naics_rows:
            aid = row.get("Award ID") or row.get("generated_internal_id")
            if aid and aid not in all_awards:
                all_awards[aid] = row

    print(f"  Unique awards before scoring: {len(all_awards)}")

    scored = []
    for row in all_awards.values():
        source = row.get("_match_source", "")
        s = score_opportunity(row, source)
        if s < args.min_score:
            continue
        desc = row.get("Description") or ""
        service = classify_service(desc)
        tier = replicability_tier(s, service)
        if tier == "skip":
            continue
        scored.append((s, tier, service, row))

    scored.sort(key=lambda x: (-x[0], float(x[3].get("Award Amount") or 0)))
    print(f"  Scored opportunities: {len(scored)}")

    output = []
    for s, tier, service, row in scored:
        record = {
            "date_scraped": today,
            "award_id": row.get("Award ID") or "",
            "award_amount": f"{float(row.get('Award Amount') or 0):.2f}",
            "replicability": tier,
            "service_type": service,
            "description": (row.get("Description") or "").strip(),
            "awardee": row.get("Recipient Name") or "",
            "awardee_uei": row.get("Prime Award Recipient UEI") or "",
            "agency": row.get("Awarding Agency") or "",
            "sub_agency": row.get("Awarding Sub Agency") or "",
            "naics": naics_code(row.get("NAICS")),
            "psc": psc_code(row.get("PSC")),
            "start_date": row.get("Start Date") or "",
            "match_source": row.get("_match_source", ""),
            "score": s,
            "award_url": award_url(row),
        }
        output.append(record)

        if args.dry_run:
            amt = float(record["award_amount"])
            print(
                f"\n[{tier.upper()} | score {s}] ${amt:,.0f} — {service}"
                f"\n  {record['description'][:120]}"
                f"\n  Awardee: {record['awardee']} | Agency: {record['agency']}"
                f"\n  {record['award_url']}"
            )

    print(f"\nFinal opportunities: {len(output)}")

    if args.dry_run:
        print("\nDry run complete — no data written.")
        return

    if not output:
        print("No opportunities matched filters.")
        return

    OPPORTUNITIES_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OPPORTUNITIES_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OPPORTUNITY_HEADER, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)
    print(f"Wrote {len(output)} rows to {OPPORTUNITIES_CSV}")


# ---------------------------------------------------------------------------
# Legacy mode: aggregate big awardees (not the default use case)
# ---------------------------------------------------------------------------

def fetch_recipients(match_source, code_filter, start_date, end_date, dod_only, page_limit):
    filters = {
        "award_type_codes": CONTRACT_AWARD_TYPES,
        "time_period": [{"start_date": start_date, "end_date": end_date}],
        **code_filter,
    }
    if dod_only:
        filters["agencies"] = [DOD_AGENCY]

    collected = []
    page = 1
    while len(collected) < page_limit:
        batch = min(100, page_limit - len(collected))
        payload = {"category": "recipient", "limit": batch, "page": page, "filters": filters}
        try:
            data = api_post(RECIPIENT_SEARCH, payload)
        except Exception as e:
            print(f"  {match_source} error: {e}", file=sys.stderr)
            break
        results = data.get("results") or []
        if not results:
            break
        for row in results:
            name = (row.get("name") or "").strip()
            if name and name not in SKIP_NAMES:
                collected.append({
                    "name": name,
                    "recipient_id": row.get("recipient_id") or "",
                    "uei": row.get("uei") or "",
                    "duns": row.get("code") or "",
                    "amount": float(row.get("amount") or 0),
                    "match_source": match_source,
                })
            if len(collected) >= page_limit:
                break
        if not (data.get("page_metadata") or {}).get("hasNext"):
            break
        page += 1
    return collected


def is_small_business(business_types):
    types = {t.lower() for t in business_types}
    if "other_than_small_business" in types:
        return False
    return bool(types & {"small_business", "8a_program_participant", "service_disabled_veteran_owned_business"})


def enrich_recipient(recipient_id):
    profile = api_get(f"{RECIPIENT_PROFILE}/{recipient_id}/") if recipient_id else None
    if not profile:
        return {}
    loc = profile.get("location") or {}
    btypes = profile.get("business_types") or []
    return {
        "company_name": profile.get("name") or "",
        "parent_company": profile.get("parent_name") or "",
        "city": loc.get("city_name") or "",
        "state": loc.get("state_code") or "",
        "zip": loc.get("zip") or "",
        "business_types": "; ".join(btypes),
        "small_business": is_small_business(btypes),
    }


def run_companies(args):
    start_date, end_date = date_range(args.months)
    dod_only = not args.all_agencies
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    naics_rows = fetch_recipients("naics_541512", {"naics_codes": {"require": ["541512"]}},
                                  start_date, end_date, dod_only, args.limit)
    psc_rows = fetch_recipients("psc_d310", {"psc_codes": ["D310"]},
                                start_date, end_date, dod_only, args.limit)

    merged = {}
    for row in naics_rows + psc_rows:
        key = row.get("uei") or row.get("recipient_id") or row.get("name")
        if key not in merged:
            merged[key] = {**row}
        else:
            merged[key]["amount"] += row["amount"]

    candidates = sorted(
        [r for r in merged.values() if r["amount"] >= args.min_amount],
        key=lambda r: r["amount"],
        reverse=True,
    )

    output = []
    for row in candidates:
        profile = enrich_recipient(row["recipient_id"])
        if args.small_business and profile and not profile.get("small_business"):
            continue
        output.append({
            "date_scraped": today,
            "company_name": profile.get("company_name") or row["name"],
            "uei": row["uei"],
            "duns": row["duns"],
            "recipient_id": row["recipient_id"],
            "city": profile.get("city", ""),
            "state": profile.get("state", ""),
            "zip": profile.get("zip", ""),
            "parent_company": profile.get("parent_company", ""),
            "business_types": profile.get("business_types", ""),
            "award_amount_12mo": f"{row['amount']:.2f}",
            "match_source": row["match_source"],
            "small_business": profile.get("small_business", ""),
            "usaspending_url": f"https://www.usaspending.gov/recipient/{row['recipient_id']}/latest",
        })

    if args.dry_run:
        for r in output[:20]:
            print(f"${float(r['award_amount_12mo']):,.0f} | {r['company_name']}")
        print(f"\nDry run: {len(output)} companies")
        return

    with AWARDEES_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AWARDEE_HEADER, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)
    print(f"Wrote {len(output)} rows to {AWARDEES_CSV}")


def main():
    parser = argparse.ArgumentParser(
        description="USASpending scraper — small contract opportunities (default) or big awardees"
    )
    parser.add_argument("--mode", choices=["opportunities", "companies"], default="opportunities")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--limit", type=int, default=50, help="Max awards per query (default 50)")
    parser.add_argument("--min-amount", type=float, default=5_000)
    parser.add_argument("--max-amount", type=float, default=150_000)
    parser.add_argument("--min-score", type=int, default=25, help="Replicability score threshold")
    parser.add_argument("--small-business", action="store_true", help="Companies mode only")
    parser.add_argument("--all-agencies", action="store_true")
    args = parser.parse_args()

    load_env()

    if args.mode == "companies":
        run_companies(args)
    else:
        run_opportunities(args)


if __name__ == "__main__":
    main()
