#!/usr/bin/env python3
"""
YouTube Data API v3 client for the AIOS — manage channel branding (title, bio).
Stdlib only, matches scripts/buffer_api.py conventions.

Usage:
    python3 scripts/youtube_api.py auth                          # one-time OAuth, saves refresh token to .env
    python3 scripts/youtube_api.py channel                       # show current branding
    python3 scripts/youtube_api.py update-branding --title "..." --description "..."

Reads YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN from .env.
Get client_id/secret from a Google Cloud OAuth "Desktop app" client (Testing mode,
scope https://www.googleapis.com/auth/youtube). Run `auth` once to get the refresh
token, then every other command uses it to mint short-lived access tokens.

Note: the YouTube Data API has no endpoint for uploading a channel avatar/banner
image or changing the @handle — those stay manual in YouTube Studio. This script
only covers what the API actually exposes: title, description, and keywords.
"""
import argparse
import http.server
import json
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
API_BASE = "https://www.googleapis.com/youtube/v3"
SCOPE = "https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.force-ssl"
REDIRECT_PORT = 8765
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def load_env():
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def save_refresh_token(token: str):
    lines = ENV_PATH.read_text().splitlines()
    out = []
    found = False
    for line in lines:
        if line.startswith("YOUTUBE_REFRESH_TOKEN="):
            out.append(f"YOUTUBE_REFRESH_TOKEN={token}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"YOUTUBE_REFRESH_TOKEN={token}")
    ENV_PATH.write_text("\n".join(out) + "\n")


def cmd_auth(_args):
    client_id = os.environ["YOUTUBE_CLIENT_ID"]
    client_secret = os.environ["YOUTUBE_CLIENT_SECRET"]
    redirect_uri = f"http://localhost:{REDIRECT_PORT}"

    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{AUTH_URI}?{urllib.parse.urlencode(auth_params)}"

    code_holder = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            code_holder["code"] = params.get("code", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>Auth complete, you can close this tab.</body></html>")

        def log_message(self, *_args):
            pass

    server = http.server.HTTPServer(("localhost", REDIRECT_PORT), Handler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    print(f"Opening browser for Google consent...\n{auth_url}")
    webbrowser.open(auth_url)
    thread.join(timeout=120)
    server.server_close()

    code = code_holder.get("code")
    if not code:
        print("No auth code received (timed out or denied).", file=sys.stderr)
        sys.exit(1)

    data = urllib.parse.urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request(TOKEN_URI, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            tokens = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Token exchange failed: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        print("No refresh_token in response (already authorized once? revoke access at "
              "https://myaccount.google.com/permissions and retry).", file=sys.stderr)
        sys.exit(1)

    save_refresh_token(refresh_token)
    print("Saved YOUTUBE_REFRESH_TOKEN to .env. Auth complete.")


def get_access_token() -> str:
    data = urllib.parse.urlencode({
        "client_id": os.environ["YOUTUBE_CLIENT_ID"],
        "client_secret": os.environ["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": os.environ["YOUTUBE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(TOKEN_URI, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())["access_token"]
    except urllib.error.HTTPError as e:
        print(f"Token refresh failed: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def api_call(path: str, http_method: str = "GET", params: dict | None = None, body: dict | None = None) -> dict:
    token = get_access_token()
    params = dict(params or {})
    url = f"{API_BASE}/{path}?{urllib.parse.urlencode(params, doseq=True)}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(
        url, data=json.dumps(body).encode() if body is not None else None,
        headers=headers, method=http_method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"YouTube API HTTP error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def cmd_channel(_args):
    data = api_call("channels", params={"part": "snippet,brandingSettings", "mine": "true"})
    item = data["items"][0]
    snippet = item["snippet"]
    print(f"Title: {snippet['title']}")
    print(f"Description: {snippet.get('description', '')}")
    print(f"Channel ID: {item['id']}")


def api_upload_call(url: str, http_method: str, data: bytes, content_type: str,
                     extra_headers: dict | None = None) -> tuple[dict, dict]:
    """Raw upload POST/PUT that returns (response_json, response_headers) — used for
    both the resumable-session init call and the actual byte upload, since only the
    init call returns a body we care about (the Location header) while the byte
    upload returns the created video resource."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": content_type}
    headers.update(extra_headers or {})
    req = urllib.request.Request(url, data=data, headers=headers, method=http_method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read()
            parsed = json.loads(body.decode()) if body else {}
            return parsed, dict(resp.headers)
    except urllib.error.HTTPError as e:
        print(f"YouTube upload HTTP error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def cmd_upload(args):
    video_path = Path(args.file).expanduser()
    if not video_path.exists():
        print(f"File not found: {video_path}", file=sys.stderr)
        sys.exit(1)
    size = video_path.stat().st_size

    snippet = {"title": args.title, "description": args.description or "", "categoryId": args.category_id}
    if args.tags:
        snippet["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    body = {"snippet": snippet, "status": {"privacyStatus": args.privacy}}

    init_url = ("https://www.googleapis.com/upload/youtube/v3/videos"
                "?uploadType=resumable&part=snippet,status")
    _, headers = api_upload_call(
        init_url, "POST", json.dumps(body).encode(), "application/json",
        extra_headers={
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(size),
        },
    )
    session_uri = headers.get("Location") or headers.get("location")
    if not session_uri:
        print("No resumable session URI returned.", file=sys.stderr)
        sys.exit(1)

    print(f"Uploading {video_path.name} ({size / 1e6:.1f} MB)...")
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    result, _ = api_upload_call(session_uri, "PUT", video_bytes, "video/mp4")
    video_id = result.get("id")
    if not video_id:
        print(f"Upload finished but no video id in response: {result}", file=sys.stderr)
        sys.exit(1)
    print(f"Uploaded. Video ID: {video_id}")
    print(f"URL: https://www.youtube.com/watch?v={video_id}")

    if args.thumbnail:
        thumb_path = Path(args.thumbnail).expanduser()
        ext = thumb_path.suffix.lower()
        content_type = "image/png" if ext == ".png" else "image/jpeg"
        thumb_bytes = thumb_path.read_bytes()
        thumb_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
        api_upload_call(thumb_url, "POST", thumb_bytes, content_type)
        print("Thumbnail set.")


def cmd_update_branding(args):
    data = api_call("channels", params={"part": "brandingSettings", "mine": "true"})
    item = data["items"][0]
    channel_branding = item["brandingSettings"].setdefault("channel", {})
    if args.title:
        channel_branding["title"] = args.title
    if args.description is not None:
        channel_branding["description"] = args.description

    body = {"id": item["id"], "brandingSettings": item["brandingSettings"]}
    result = api_call("channels", http_method="PUT", params={"part": "brandingSettings"}, body=body)
    print(f"Updated: {result['brandingSettings']['channel']['title']}")


def main():
    load_env()
    parser = argparse.ArgumentParser(description="YouTube Data API client")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("auth")
    sub.add_parser("channel")

    p_branding = sub.add_parser("update-branding")
    p_branding.add_argument("--title")
    p_branding.add_argument("--description")

    p_upload = sub.add_parser("upload")
    p_upload.add_argument("--file", required=True)
    p_upload.add_argument("--title", required=True)
    p_upload.add_argument("--description")
    p_upload.add_argument("--privacy", default="private", choices=["public", "unlisted", "private"])
    p_upload.add_argument("--category-id", default="28")  # Science & Technology
    p_upload.add_argument("--tags")
    p_upload.add_argument("--thumbnail")

    args = parser.parse_args()

    for key in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET"):
        if not os.environ.get(key):
            print(f"{key} not set in .env", file=sys.stderr)
            sys.exit(1)
    if args.command != "auth" and not os.environ.get("YOUTUBE_REFRESH_TOKEN"):
        print("YOUTUBE_REFRESH_TOKEN not set — run `python3 scripts/youtube_api.py auth` first", file=sys.stderr)
        sys.exit(1)

    {
        "auth": cmd_auth,
        "channel": cmd_channel,
        "update-branding": cmd_update_branding,
        "upload": cmd_upload,
    }[args.command](args)


if __name__ == "__main__":
    main()
