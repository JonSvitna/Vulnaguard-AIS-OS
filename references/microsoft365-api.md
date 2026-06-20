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
Granted application permissions: `Calendars.Read`, `Mail.Read`, `Mail.Send` (admin consent granted).

**Pending:** `MailboxSettings.ReadWrite` is required for the inbox-rule commands (`rules`, `rule-forward`) but has not been granted yet. To enable:
1. Azure Portal → App registrations → `vulnaguard-aios` → API permissions → Add a permission → Microsoft Graph → Application permissions → `MailboxSettings.ReadWrite`.
2. Click "Grant admin consent for {tenant}" — only a tenant admin can do this.
3. No code change needed after that; the existing `.default` scope picks up new permissions automatically.

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
```

`rule-forward` defaults to `forwardTo` (forwarded message looks like it's from the original sender). Pass `--redirect` to use `redirectTo` instead (message arrives as if sent directly to the new address — usually the better choice for a mailbox handoff).

## Verified working

2026-06-18 — token acquisition and both `calendarView` and `messages` calls confirmed live against the real mailbox.

## Rotating the secret

If the client secret is ever exposed (e.g. pasted in a chat log), rotate it in Azure AD → App registrations → `vulnaguard-aios` → Certificates & secrets → revoke the old value, generate a new one, update `.env`.
