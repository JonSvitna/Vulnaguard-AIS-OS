#!/usr/bin/env python3
"""
One-shot BD email drafting + send — replaces the Claude Pro Projects manual
tier. One API call per email (short, single-turn, voice rules baked into the
system prompt) instead of an iterative chat, so token spend per email stays
small; one script instead of a browser tab + copy/paste + separate send step.

Stdlib only, matches scripts/buffer_api.py conventions.

Usage:
    python3 scripts/draft_and_send.py \
        --to lead@example.com \
        --list partnership \
        --context "Marcus runs a MSP in the same regional defense-contractor space, referral fit for CMMC work"

Reads ANTHROPIC_API_KEY and RESEND_API_KEY from .env.

Flow: drafts once, shows you SUBJECT + BODY, then asks [s]end / [r]edraft
(append one line of extra instruction) / [c]ancel. Sends via Resend from
the same verified vulnaguard.com domain as the automated seo-agent pipeline.
Does NOT auto-log to references/outreach-log.md — add that row yourself.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from send_manual_email import send_email, DEFAULT_FROM  # noqa: E402

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"

OUTPUT_FORMAT_RULE = (
    "\n\nRespond in exactly this format, nothing else:\n"
    "SUBJECT: <subject line>\n"
    "BODY:\n<email body>"
)

SYSTEM_PROMPTS = {
    "partnership": (
        "You draft partnership/relationship outreach emails for Vulnaguard, a small cybersecurity "
        "compliance firm (CMMC Level 2, NIST SP 800-171) run by Sean Murrill.\n\n"
        "Voice: peer-level, not a pitch. Professional but direct. No corporate boilerplate, no em dashes, "
        "short sentences.\n\n"
        "Every email: (1) who Vulnaguard is in one sentence, (2) the specific reason you're reaching out "
        "to THIS org — never generic, (3) the overlap/complementary value, (4) one low-pressure ask — a "
        "20-minute call, no agenda.\n\n"
        "Subject line: [First Name] — [short specific hook], e.g. \"Marcus — CMMC referral partnership\"\n\n"
        "Body under 150 words. Sign off: Sean Murrill / Vulnaguard.\n\n"
        "Banned: \"we are pleased to,\" \"our team of experts,\" \"comprehensive solution,\" \"best-in-class,\" "
        "\"leverage,\" \"synergy,\" \"reach out\" as filler."
    ),
    "sales": (
        "You draft cold sales outreach for Vulnaguard's security services (vulnerability scans, security "
        "audits, CMMC/NIST 800-171 gap assessments) to a specific prospect company.\n\n"
        "Voice: first person as Sean — a founder who does the actual security work, not a sales rep on a "
        "script. Calm, direct, human, zero pressure. Not trying to close in the first email.\n\n"
        "Intro email (150-word cap): who you are in one sentence -> the specific pain signal you noticed "
        "about THIS company (no in-house security, recent industry breach, approaching compliance deadline "
        "— never invent one) -> what you can offer, scoped and concrete -> one low-pressure ask (short "
        "call, or \"happy to send a one-pager instead\").\n\n"
        "No em dashes. End the body with:\n"
        "---\nSean Murrill | Vulnaguard LLC | [MAILING ADDRESS] | Reply STOP to opt out.\n\n"
        "Banned phrases: \"I hope this email finds you well,\" \"circle back,\" \"touch base,\" \"leverage,\" "
        "\"synergy,\" \"digital transformation,\" \"cutting-edge,\" \"best-in-class,\" \"game-changer,\" "
        "\"seamless,\" \"comprehensive solution,\" \"disruptive,\" \"we are pleased to,\" \"our team of "
        "experts,\" \"we look forward to the opportunity,\" \"at your earliest convenience,\" \"per my last "
        "email.\""
    ),
    "general": (
        "You draft general BD correspondence for Vulnaguard that doesn't fit a partnership or "
        "sales-prospecting email: RFI responses, solicitation cover notes, and follow-ups on existing "
        "conversations.\n\n"
        "Voice: professional but direct, no corporate boilerplate, no em dashes. Vulnaguard is a small, "
        "focused CMMC/NIST 800-171 compliance firm — write like a knowledgeable peer who's done the work, "
        "not a vendor pitching features.\n\n"
        "Opening formula, always in this order: (1) who we are, one sentence, (2) what we noticed / why "
        "we're responding, tied to their specific solicitation or situation, (3) how we can help, concrete "
        "not generic.\n\n"
        "Under 200 words for outreach, under 100 for follow-ups. Sign off: Sean Murrill / Vulnaguard / "
        "seanmurrill@vulnaguard.com."
    ),
}


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def call_claude(system_prompt: str, user_message: str) -> str:
    api_key = os.environ["ANTHROPIC_API_KEY"]
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 1024,
        "system": system_prompt + OUTPUT_FORMAT_RULE,
        "messages": [{"role": "user", "content": user_message}],
    }).encode("utf-8")
    req = urllib.request.Request(
        ANTHROPIC_URL,
        data=payload,
        method="POST",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"Anthropic API error {e.code}: {body_text}", file=sys.stderr)
        sys.exit(1)
    return result["content"][0]["text"]


def parse_draft(text: str) -> tuple[str, str]:
    match = re.match(r"SUBJECT:\s*(.+?)\nBODY:\s*\n?(.*)", text, re.DOTALL)
    if not match:
        print("Could not parse SUBJECT/BODY from model output:", file=sys.stderr)
        print(text, file=sys.stderr)
        sys.exit(1)
    return match.group(1).strip(), match.group(2).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--list", choices=list(SYSTEM_PROMPTS), required=True)
    parser.add_argument("--context", required=True,
                         help="One or two sentences: who this is, why you're reaching out, any specific hook.")
    parser.add_argument("--from-addr", default=DEFAULT_FROM)
    args = parser.parse_args()

    load_env()

    system_prompt = SYSTEM_PROMPTS[args.list]
    user_message = f"Recipient/context: {args.context}"

    while True:
        draft_text = call_claude(system_prompt, user_message)
        subject, body = parse_draft(draft_text)

        print(f"\n--- SUBJECT ---\n{subject}\n--- BODY ---\n{body}\n")
        choice = input("[s]end / [r]edraft with extra instruction / [c]ancel: ").strip().lower()

        if choice == "s":
            result = send_email(args.to, subject, body, args.from_addr)
            print(f"Sent ({args.list}) to {args.to} — Resend id: {result.get('id')}")
            print("Remember to add a row to references/outreach-log.md.")
            break
        elif choice == "r":
            extra = input("Extra instruction: ").strip()
            user_message = f"Recipient/context: {args.context}\n\nRevision instruction: {extra}"
            continue
        else:
            print("Cancelled, nothing sent.")
            break


if __name__ == "__main__":
    main()
