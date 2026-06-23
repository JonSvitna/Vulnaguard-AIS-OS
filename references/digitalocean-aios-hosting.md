# Hosting Vulnaguard AIOS on DigitalOcean (Always-On, Slack-Connected)

Setup guide for standing up this AIOS — CLAUDE.md, skills, context, connections — as an
always-on service on a DigitalOcean droplet, reachable remotely via Slack instead of the
local Claude Code CLI. Written to be run on a separate machine from scratch.

**Status:** this doc covers provisioning, security, and runtime setup — everything that
can be done before a line of bridge code exists. The actual service (Node process running
the Claude Agent SDK with this repo's CLAUDE.md/skills/context loaded as the system prompt,
fronted by Slack) is a separate build, not yet written. Treat this as the infra layer to
have ready before that build lands.

## Why DigitalOcean + Agent SDK (not Claude Code subscription)

Claude Code (the CLI/Pro/Max subscription) is built for interactive local sessions — there's
no supported way to point the subscription at an unattended server. The path to "same
capabilities, always-on" is the **Claude Agent SDK**: same engine, but embeddable in a custom
service. That means a **separate, metered Anthropic API key** billed per-token — a new cost
line distinct from the Claude Code subscription.

## 1. Prerequisites

- DigitalOcean account with billing set up
- A domain or subdomain (optional — only needed if you want a public HTTPS endpoint; not
  required for a Slack-only bridge, which makes outbound connections to Slack's API)
- Anthropic API key for the Agent SDK (console.anthropic.com → API Keys — separate from your
  Claude Code login)
- SSH key pair on the new machine (`ssh-keygen -t ed25519 -C "vulnaguard-aios"` if you don't
  have one)
- `gh` CLI or git credentials to clone this repo on the new machine

## 2. Create the droplet

1. DigitalOcean dashboard → **Create → Droplets**
2. Image: **Ubuntu 24.04 LTS**
3. Size: Basic, Regular SSD, **1 vCPU / 1GB RAM** is enough to start (this is a chat-driven
   orchestration process, not a compute-heavy service) — bump to 2GB if the SDK process needs
   more headroom once running
4. Region: closest to you or to Slack's edge (US region is fine)
5. Authentication: **SSH key** — paste your public key (`cat ~/.ssh/id_ed25519.pub`), not a
   password
6. Hostname: `vulnaguard-aios`
7. Create the droplet, note the public IP

## 3. Initial server hardening

SSH in as root first:

```bash
ssh root@<droplet-ip>
```

Create a non-root user and lock down SSH:

```bash
adduser sean
usermod -aG sudo sean
rsync --archive --chown=sean:sean ~/.ssh /home/sean
```

Edit `/etc/ssh/sshd_config`:

```
PermitRootLogin no
PasswordAuthentication no
```

```bash
systemctl restart sshd
```

From now on, SSH in as `sean@<droplet-ip>`.

Set up the firewall (only SSH in; outbound is unrestricted so the bridge can reach Slack and
Anthropic's API):

```bash
sudo ufw allow OpenSSH
sudo ufw enable
```

Optional but recommended: enable DigitalOcean's free **Cloud Firewall** on the droplet from
the dashboard as a second layer, and turn on **automated backups** ($/mo, worth it for a
box holding repo context + credentials).

## 4. Install runtime dependencies

```bash
# Node.js (LTS) via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts

# git
sudo apt update && sudo apt install -y git

# process manager
npm install -g pm2
```

## 5. Clone the repo and set secrets

```bash
git clone https://github.com/<your-org-or-user>/Vulnaguard-AIS-OS.git
cd Vulnaguard-AIS-OS
```

Create `.env` (gitignored, never committed — matches the pattern already used for
`scripts/*_api.py` in this repo):

```
ANTHROPIC_API_KEY=sk-ant-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_CHANNEL_ID=C0AMQU5HN2G
```

`ANTHROPIC_API_KEY` is the new Agent SDK key (step 1), **not** anything tied to your Claude
Code login. `SLACK_BOT_TOKEN` can reuse the existing bot token already wired in
`references/slack-api.md` / `scripts/slack_api.py` — see step 6 for the scope additions it
needs.

## 6. Slack app changes (reusing the existing app)

The existing Slack app (bot already invited to `#all-vulnaguard-sentinel`, token in
`references/slack-api.md`) only has outbound scopes (`chat:write`, `channels:read`,
`channels:history`, `users:read`). For a two-way chat bridge it needs to **receive** DMs too:

1. api.slack.com/apps → your existing app → **OAuth & Permissions**
2. Add Bot Token Scopes: `im:history`, `im:read`, `im:write`, `app_mentions:read`
3. **Socket Mode** → enable it (avoids needing a public HTTPS endpoint/webhook URL on the
   droplet) → generate an **app-level token** with `connections:write` scope → this is your
   `SLACK_APP_TOKEN` (`xapp-...`)
4. **Event Subscriptions** → subscribe to `message.im` (DM messages) and optionally
   `app_mention` if you want it to respond in channels too
5. Reinstall the app to the workspace to apply the new scopes — this issues a fresh
   `SLACK_BOT_TOKEN`, update `.env` and `references/slack-api.md`'s stored value
6. DM the bot directly to test once the bridge service (step 7) is running

## 7. The bridge service (not yet built)

This is the piece that doesn't exist yet: a Node process that —

1. Loads `CLAUDE.md`, `context/`, `references/`, and skill definitions from this repo as
   system-prompt context
2. Opens a Slack Socket Mode connection, listens for DMs
3. On each DM, runs it through the Claude Agent SDK with that context loaded, replicating
   the tool-use loop (file read/write, bash, etc. — scoped to what's safe to run unattended)
4. Posts the response back to Slack

Known open problem from prior research: the Agent SDK doesn't give you Claude Code's
permission/guardrail system for free — that has to be re-implemented deliberately before this
runs unattended with write access to real systems. Don't skip that just to get it working.

Once that service exists, run it under `pm2` for crash recovery and boot persistence:

```bash
pm2 start bridge.js --name vulnaguard-aios
pm2 save
pm2 startup   # follow the printed command to enable on-boot start
```

## 8. Verify

- `pm2 status` shows the process running
- `pm2 logs vulnaguard-aios` shows the Slack connection established
- DM the bot from your phone and confirm a response comes back

## Cost ballpark

- Droplet: ~$6-12/mo (1-2GB basic tier)
- Backups: ~20% of droplet cost if enabled
- Anthropic API usage: metered, separate from Claude Code subscription — variable based on
  usage, watch this closely early on

## Rollback / teardown

Destroy the droplet from the DigitalOcean dashboard if this gets abandoned — no other cleanup
needed since secrets live only in that droplet's `.env`, never committed.
