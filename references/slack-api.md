# Slack

Connects the AIOS to Sean's Slack workspace via a bot token (Web API).

## Auth flow

Bot token auth (no OAuth dance needed at runtime — token is long-lived once issued).

1. Created a Slack app at api.slack.com/apps, installed to the workspace.
2. Bot Token Scopes granted: `chat:write`, `channels:read`, `channels:history`, `users:read`.
   - `channels.list` currently only requests `public_channel` type — add `groups:read` scope and reinstall the app if private-channel listing is needed later.
3. Use the Bot User OAuth Token (`xoxb-...`) as a `Bearer` token on all Web API calls.
4. The bot must be invited to a channel (`/invite @botname` in Slack) before it can read or post there — workspace-wide scopes don't grant per-channel access automatically.

## Credentials

Stored in `.env` (gitignored, never committed):

```
SLACK_BOT_TOKEN=xoxb-...
```

## Common queries

**List channels (and whether the bot is a member):**
```
GET /conversations.list?types=public_channel,private_channel&limit=200
```

**Read recent messages in a channel:**
```
GET /conversations.history?channel={channel_id}&limit=20
```

**Send a message:**
```
POST /chat.postMessage
{ "channel": "{channel_id}", "text": "..." }
```

## Script

`scripts/slack_api.py` — stdlib-only Python (no `slack_sdk` dependency).

```
python3 scripts/slack_api.py channels
python3 scripts/slack_api.py history --channel C0123456789 --limit 20
python3 scripts/slack_api.py send --channel C0123456789 --text "Hi"
```

## Rotating the token

If the bot token is ever exposed, go to api.slack.com/apps → the app → OAuth & Permissions → Revoke, then reinstall to workspace to get a new token and update `.env`.
