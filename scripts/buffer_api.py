#!/usr/bin/env python3
"""
Buffer API client for the AIOS — queue posts across Facebook, Instagram, LinkedIn.
Stdlib only, matches scripts/slack_api.py conventions.

Uses Buffer's current GraphQL Publish API (https://api.buffer.com), authenticated
with a personal API key (Buffer account settings -> API -> Create a Personal Key).
Buffer's old REST API (api.bufferapp.com/1) no longer accepts new developer app
registrations, so that path is dead for new setups — this script targets the
GraphQL API instead.

Usage:
    python3 scripts/buffer_api.py organizations
    python3 scripts/buffer_api.py profiles --org-id <organizationId>
    python3 scripts/buffer_api.py queue --profile-id <channelId> --text "..." \\
        [--scheduled-at "2026-06-25T15:00:00Z"] [--video-url "https://..."] [--image-url "https://..."]

Reads BUFFER_ACCESS_TOKEN from .env (a personal API key, Bearer-auth'd).

This script only QUEUES posts into Buffer — it never auto-approves content. The
social-post-queue skill is the human review gate; this is the deterministic
"push the approved draft" step downstream of it.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

API_URL = "https://api.buffer.com"


def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def graphql_call(query: str, variables: dict | None = None) -> dict:
    token = os.environ["BUFFER_ACCESS_TOKEN"]
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Buffer API HTTP error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    if data.get("errors"):
        print(f"Buffer GraphQL error: {json.dumps(data['errors'], indent=2)}", file=sys.stderr)
        sys.exit(1)
    return data["data"]


def cmd_organizations(_args):
    data = graphql_call("""
        query {
          account {
            organizations {
              id
              name
            }
          }
        }
    """)
    for org in data["account"]["organizations"]:
        print(f"{org['id']}  {org['name']}")


def cmd_profiles(args):
    org_id = args.org_id
    if not org_id:
        orgs = graphql_call("""
            query {
              account {
                organizations { id name }
              }
            }
        """)["account"]["organizations"]
        if not orgs:
            print("No organizations found on this Buffer account.", file=sys.stderr)
            sys.exit(1)
        if len(orgs) > 1:
            print("Multiple organizations found — pass --org-id to pick one:", file=sys.stderr)
            for org in orgs:
                print(f"  {org['id']}  {org['name']}", file=sys.stderr)
            sys.exit(1)
        org_id = orgs[0]["id"]

    data = graphql_call(
        """
        query channels($input: ChannelsInput!) {
          channels(input: $input) {
            id
            name
            service
            descriptor
          }
        }
        """,
        {"input": {"organizationId": org_id}},
    )
    for ch in data["channels"]:
        print(f"{ch['id']}  {ch['service']}  {ch.get('name', '')}  ({ch.get('descriptor', '')})")


def cmd_queue(args):
    assets = []
    if args.video_url:
        assets.append({"video": {"url": args.video_url}})
    if args.image_url:
        assets.append({"image": {"url": args.image_url}})

    if args.scheduled_at:
        mode = "customScheduled"
        due_at = args.scheduled_at
    else:
        mode = "addToQueue"
        due_at = None

    post_input = {
        "channelId": args.profile_id,
        "text": args.text,
        "mode": mode,
        "schedulingType": args.scheduling_type,
        "assets": assets,
    }
    if due_at:
        post_input["dueAt"] = due_at
    if args.instagram_type:
        post_input["metadata"] = {
            "instagram": {"type": args.instagram_type, "shouldShareToFeed": True}
        }

    data = graphql_call(
        """
        mutation createPost($input: CreatePostInput!) {
          createPost(input: $input) {
            ... on PostActionSuccess {
              post {
                id
                text
                dueAt
                status
              }
            }
            ... on NotFoundError { message }
            ... on UnauthorizedError { message }
            ... on UnexpectedError { message }
            ... on RestProxyError { message }
            ... on LimitReachedError { message }
            ... on InvalidInputError { message }
          }
        }
        """,
        {"input": post_input},
    )
    result = data["createPost"]
    if "post" in result:
        post = result["post"]
        print(f"Queued: {post['id']}  status={post['status']}  dueAt={post.get('dueAt')}")
    else:
        print(f"Buffer error: {result.get('message')}", file=sys.stderr)
        sys.exit(1)


def cmd_edit(args):
    post_input = {
        "id": args.post_id,
        "text": args.text,
        "mode": args.mode,
        "schedulingType": args.scheduling_type,
    }
    if args.due_at:
        post_input["dueAt"] = args.due_at
    if args.video_url:
        post_input["assets"] = [{"video": {"url": args.video_url}}]
    if args.instagram_type:
        post_input["metadata"] = {
            "instagram": {"type": args.instagram_type, "shouldShareToFeed": True}
        }

    data = graphql_call(
        """
        mutation editPost($input: EditPostInput!) {
          editPost(input: $input) {
            ... on PostActionSuccess {
              post { id text dueAt status }
            }
            ... on NotFoundError { message }
            ... on UnauthorizedError { message }
            ... on UnexpectedError { message }
            ... on RestProxyError { message }
            ... on LimitReachedError { message }
            ... on InvalidInputError { message }
          }
        }
        """,
        {"input": post_input},
    )
    result = data["editPost"]
    if "post" in result:
        post = result["post"]
        print(f"Updated: {post['id']}  status={post['status']}  dueAt={post.get('dueAt')}")
    else:
        print(f"Buffer error: {result.get('message')}", file=sys.stderr)
        sys.exit(1)


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Buffer GraphQL API client")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("organizations")

    p_profiles = sub.add_parser("profiles")
    p_profiles.add_argument("--org-id", help="Organization ID; auto-detected if the account has only one")

    p_queue = sub.add_parser("queue")
    p_queue.add_argument("--profile-id", required=True, help="Buffer channel ID")
    p_queue.add_argument("--text", required=True)
    p_queue.add_argument("--scheduled-at", help="ISO 8601 UTC timestamp; omit to add to the next available queue slot")
    p_queue.add_argument("--video-url", help="Video asset URL (e.g. for Instagram Reels)")
    p_queue.add_argument("--image-url", help="Image asset URL")
    p_queue.add_argument(
        "--scheduling-type",
        default="automatic",
        choices=["automatic", "notification"],
        help="'automatic' publishes directly; 'notification' sends a mobile reminder (required by some networks without direct publish permissions)",
    )
    p_queue.add_argument(
        "--instagram-type",
        choices=["post", "reel", "story", "carousel"],
        help="Required for Instagram posts: post, reel, story, or carousel",
    )

    p_edit = sub.add_parser("edit")
    p_edit.add_argument("--post-id", required=True)
    p_edit.add_argument("--text", required=True)
    p_edit.add_argument("--mode", default="customScheduled", choices=["addToQueue", "shareNext", "shareNow", "customScheduled"])
    p_edit.add_argument("--scheduling-type", default="automatic", choices=["automatic", "notification"])
    p_edit.add_argument("--instagram-type", choices=["post", "reel", "story", "carousel"])
    p_edit.add_argument("--due-at", help="ISO 8601 UTC timestamp; required when --mode is customScheduled")
    p_edit.add_argument("--video-url", help="Video asset URL; must be re-sent or the post's video is cleared")

    args = parser.parse_args()

    if "BUFFER_ACCESS_TOKEN" not in os.environ:
        print("BUFFER_ACCESS_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    {
        "organizations": cmd_organizations,
        "profiles": cmd_profiles,
        "queue": cmd_queue,
        "edit": cmd_edit,
    }[args.command](args)


if __name__ == "__main__":
    main()
