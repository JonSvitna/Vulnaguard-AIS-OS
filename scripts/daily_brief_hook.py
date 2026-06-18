#!/usr/bin/env python3
"""
SessionStart hook: pulls today's M365 calendar + recent mail and injects
it as additionalContext so Claude opens the session with a daily brief.
"""
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import microsoft365_api as m


def capture(fn, *args):
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            fn(*args)
    except Exception as e:
        return f"(error: {e})"
    return buf.getvalue().strip() or "(none)"


def main():
    m.load_env()
    try:
        token = m.get_token()
    except Exception as e:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"M365 daily brief unavailable: {e}",
            }
        }))
        return

    upn = m.os.environ["MS365_USER_UPN"]
    events = capture(m.list_events, token, upn, 1)
    mail = capture(m.list_mail, token, upn, 10)

    context = (
        "## Daily M365 Brief\n\n"
        f"### Today's calendar events\n{events}\n\n"
        f"### Recent mail (top 10)\n{mail}\n\n"
        "Summarize this for Sean at the start of the conversation. Flag anything "
        "time-sensitive, especially bid/solicitation notifications relevant to "
        "Sentinel CMMC gov contract work. Keep it short."
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
