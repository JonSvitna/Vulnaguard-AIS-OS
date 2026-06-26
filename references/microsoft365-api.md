# Microsoft 365 / Graph API

Connects the AIOS to Sean's Microsoft 365 mailbox (Calendar + Outlook) via app-only auth.

## Auth flow

OAuth2 client-credentials grant (app-only, no user sign-in needed — runs unattended).

1. POST `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token`
   - `grant_type=client_credentials`
   - `client_id`, `client_secret`
   - `scope=https://graph.microsoft.com/.default`
2. Use the returned `access_token` as a `Bearer` token on all Graph calls.
3. Token expires in ~1 hour — the script re-fetches a fresh one on every run, no caching needed at current call volume.

## Credentials

Stored in `.env` (gitignored, never committed):

```
MS365_CLIENT_ID=...
MS365_TENANT_ID=...
MS365_CLIENT_SECRET=...
MS365_USER_UPN=seanmurrill@vulnaguard.com
```

App registration: `vulnaguard-aios` in Azure AD, tenant `b2168f2a-36e6-4821-9b0b-602124dd3b54`.
Granted application permissions: `Calendars.Read`, `Mail.Read`, `Mail.Send`, `MailboxSettings.ReadWrite` (admin consent granted — confirmed live 2026-06-24, `rules`/`rule-forward` commands work).

Because this is app-only auth, every Graph call targets a specific mailbox via `/users/{upn}/...` — there's no `/me` endpoint without a signed-in user.

## Common queries

**Upcoming calendar events:**
```
GET /users/{upn}/calendarView?startDateTime={iso}&endDateTime={iso}&$orderby=start/dateTime
```

**Recent mail:**
```
GET /users/{upn}/messages?$orderby=receivedDateTime desc&$top=10&$select=subject,from,receivedDateTime
```

**Send mail:**
```
POST /users/{upn}/sendMail
{
  "message": {
    "subject": "...",
    "body": { "contentType": "Text", "content": "..." },
    "toRecipients": [{ "emailAddress": { "address": "..." } }]
  }
}
```

## Script

`scripts/microsoft365_api.py` — stdlib-only Python (no `requests`/`msal` dependency).

```
python3 scripts/microsoft365_api.py events --days 7
python3 scripts/microsoft365_api.py mail --top 10
python3 scripts/microsoft365_api.py send --to a@b.com --subject "Hi" --body "Text"
python3 scripts/microsoft365_api.py rules
python3 scripts/microsoft365_api.py rule-forward --rule-id <id> --to jessicasayre28@gmail.com
python3 scripts/microsoft365_api.py create-rule --name "All mail to Slack" --to leads-inbox-...@vulnaguardsentinel.slack.com --redirect
python3 scripts/microsoft365_api.py create-rule --name "Bidnet to Slack" --sender noreply@bidnet.com --to leads-inbox-...@vulnaguardsentinel.slack.com --redirect
python3 scripts/microsoft365_api.py delete-rule --rule-id <id>
python3 scripts/microsoft365_api.py search-mail --sender <address> --subject-contains "text" --top 50
python3 scripts/microsoft365_api.py delete-mail --message-id <id>
```

**Do not create a redirect rule pointing at a Slack channel's "email address."** Slack's native email-to-channel feature isn't available on Sean's plan, so any message redirected there bounces — every bounce shows up twice (an NDR in the inbox, and again in Slack via `mail_to_slack.py`'s indiscriminate poller). The working mail→Slack bridge is the cron-based poller, not an Exchange rule. `delete-mail` will currently fail with `403 ErrorAccessDenied` — only `Mail.Read`/`Mail.Send`/`MailboxSettings.ReadWrite` are granted, not `Mail.ReadWrite`, which DELETE requires. Don't request that scope for one-off cleanup; have Sean delete manually in Outlook instead.

`rule-forward` defaults to `forwardTo` (forwarded message looks like it's from the original sender). Pass `--redirect` to use `redirectTo` instead (message arrives as if sent directly to the new address — usually the better choice for a mailbox handoff).

`create-rule` makes a new inbox rule. Omit `--sender` to match all mail (catch-all); pass it for an exact from-address filter. Requires a unique `sequence` field — the script auto-assigns the next free sequence number. Note: creating a catch-all redirect rule can cause Exchange to auto-disable other rules it considers superseded — check `rules` output after creating one.

## Verified working

2026-06-18 — token acquisition and both `calendarView` and `messages` calls confirmed live against the real mailbox.
2026-06-24 — `MailboxSettings.ReadWrite` confirmed live; created inbox rule `AQAAAC31xzc=` redirecting all mail to the `#leads-inbox` Slack channel email (`leads-inbox-aaaauxdzsvnzooqfpgmmgjttyy@vulnaguardsentinel.slack.com`).
2026-06-25 — Deleted rule `AQAAAC31xzc=` (it was generating Undeliverable bounces — see note above; the real mail→Slack bridge is the cron poller, not a rule). Added `delete-rule`, `search-mail`, `delete-mail` commands. `delete-mail` confirmed it needs `Mail.ReadWrite` (403 without it) — not requested, scope kept minimal.

## Rotating the secret

If the client secret is ever exposed (e.g. pasted in a chat log), rotate it in Azure AD → App registrations → `vulnaguard-aios` → Certificates & secrets → revoke the old value, generate a new one, update `.env`.
