# Buffer

Connects the AIOS to Facebook, Instagram, and LinkedIn for social posting, via Buffer
as the single broker instead of three separate platform APIs (Meta app review and
LinkedIn's Marketing Developer Platform approval are both slow/uncertain for a solo dev —
Buffer already holds OAuth to all three).

## Auth flow

1. Create a Buffer account (or use an existing one), connect the Facebook Page,
   Instagram Business account, and LinkedIn profile/page inside Buffer's UI —
   this is where the actual per-platform OAuth happens, once, manually.
2. Create a Buffer app at buffer.com/developers/apps to get a personal access token
   (no OAuth dance needed at runtime for single-account use — token is long-lived).
3. Use the access token as a query-param/form-field (`access_token=...`) on all
   Buffer API calls — Buffer's API is older-style REST, not bearer-header auth.

## Credentials

Stored in `.env` (gitignored, never committed):

```
BUFFER_ACCESS_TOKEN=
BUFFER_PROFILE_ID_FACEBOOK=
BUFFER_PROFILE_ID_INSTAGRAM=
BUFFER_PROFILE_ID_LINKEDIN=
```

Profile IDs come from `profiles.json` (see below) — fetch once after connecting accounts
in Buffer's UI, then hardcode into `.env`.

## Common queries

**List connected profiles (to get profile IDs):**
```
GET /profiles.json?access_token=...
```

**Queue a post to a profile (next available slot):**
```
POST /profiles/{profile_id}/updates/create.json
{ "text": "...", "now": "true", "access_token": "..." }
```

**Schedule a post for a specific time:**
```
POST /profiles/{profile_id}/updates/create.json
{ "text": "...", "scheduled_at": "2026-06-25T15:00:00Z", "access_token": "..." }
```

## Script

`scripts/buffer_api.py` — stdlib-only Python, matches `scripts/slack_api.py` conventions.

```
python3 scripts/buffer_api.py profiles
python3 scripts/buffer_api.py queue --profile-id <id> --text "..." [--scheduled-at "2026-06-25T15:00:00Z"]
```

This script only queues — it never decides what gets posted. The `social-post-queue`
skill is the human review/approval step upstream of it (per `CLAUDE.md`'s rule on not
posting externally without a look first).

## Rotating the token

If the access token is ever exposed, revoke the app at buffer.com/developers/apps and
generate a new one, then update `.env`.
