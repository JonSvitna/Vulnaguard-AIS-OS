import math
import os
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sentinel OS API")
api = APIRouter(prefix="/api")

SERVER_START = time.time()

REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = Path(os.environ.get("HOME", "")) / ".claude/projects/-Users-seanm-Documents-GitHub-Vulnaguard-AIS-OS/memory"
OBSIDIAN_WIKI_DIR = Path(os.environ.get("HOME", "")) / "Documents/Obsidian Vault/wiki"
SKILLS_DIR = REPO_ROOT / ".claude/skills"
AGENTS_DIR = REPO_ROOT / ".claude/agents"
CONNECTIONS_MD = REPO_ROOT / "connections.md"

SECTIONS = [
    {"id": "overview", "label": "OVERVIEW", "code": "SYS-01", "scene": "globe"},
    {"id": "network", "label": "NETWORK", "code": "NET-02", "scene": "neural"},
    {"id": "memory", "label": "MEMORY", "code": "MEM-03", "scene": "globe"},
    {"id": "systems", "label": "SYSTEMS", "code": "PWR-04", "scene": "neural"},
    {"id": "comms", "label": "COMMS", "code": "COM-05", "scene": "globe"},
]


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _series(n, base, spread):
    return [round(base + random.uniform(-spread, spread), 1) for _ in range(n)]


def read_safe(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(raw: str):
    """Split a markdown file's YAML frontmatter from its body. Returns (data, content)."""
    if not raw:
        return {}, ""
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return {}, raw
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        data = {}
    return data, m.group(2)


def list_md_files(directory: Path):
    try:
        return sorted(p for p in directory.iterdir() if p.suffix == ".md")
    except OSError:
        return []


def list_md_files_recursive(directory: Path):
    results = []
    try:
        entries = sorted(directory.iterdir())
    except OSError:
        return results
    for entry in entries:
        if entry.name.startswith(".") or entry.name.startswith("_"):
            continue
        if entry.is_dir():
            results.extend(list_md_files_recursive(entry))
        elif entry.suffix == ".md":
            results.append(entry)
    return results


def parse_connections_table(raw: str):
    lines = [l for l in raw.splitlines() if l.strip().startswith("|")]
    data_lines = lines[2:]  # drop header + separator
    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 6:
            continue
        num, domain, tool, mechanism, auth, last_checked = cells[:6]
        rows.append({"num": num, "domain": domain, "tool": tool, "mechanism": mechanism, "auth": auth, "lastChecked": last_checked})
    return rows


def compute_status(row):
    mechanism = (row.get("mechanism") or "").lower()
    last_checked = row.get("lastChecked")
    if "not yet connected" in mechanism:
        return "offline"
    if not last_checked or last_checked in ("—", "-"):
        return "standby"
    try:
        checked = datetime.fromisoformat(last_checked)
    except ValueError:
        return "standby"
    days_since = (datetime.now(timezone.utc) - checked.replace(tzinfo=timezone.utc)).days
    return "online" if days_since <= 14 else "standby"


def fibonacci_sphere_point(i, n):
    phi = math.acos(1 - 2 * (i + 0.5) / n)
    theta = math.pi * (1 + 5 ** 0.5) * i
    return (
        round(math.cos(theta) * math.sin(phi), 4),
        round(math.sin(theta) * math.sin(phi), 4),
        round(math.cos(phi), 4),
    )


def build_knowledge_graph():
    """Combined real graph: AIOS memory notes + Obsidian vault notes, linked by [[wikilinks]]."""
    nodes = []
    node_ids = set()
    link_targets = {}

    def ingest(files, source, id_prefix, default_type):
        for file_path in files:
            raw = read_safe(file_path)
            if not raw:
                continue
            data, content = parse_frontmatter(raw)
            file_slug = file_path.stem
            name = data.get("title") or data.get("name") or file_slug
            node_id = f"{id_prefix}:{name}"
            if node_id in node_ids:
                continue
            node_ids.add(node_id)
            node_type = data.get("type") or (data.get("metadata") or {}).get("type") or default_type
            nodes.append({"id": node_id, "name": name, "source": source, "type": node_type})
            targets = {f"{id_prefix}:{m.strip()}" for m in re.findall(r"\[\[([^\]|#]+)", content)}
            link_targets[node_id] = targets

    ingest(
        [f for f in list_md_files(MEMORY_DIR) if f.name != "MEMORY.md"],
        "aios-memory", "mem", "unknown",
    )
    ingest(list_md_files_recursive(OBSIDIAN_WIKI_DIR), "obsidian-vault", "wiki", "note")

    seen = set()
    edges = []
    for source_id, targets in link_targets.items():
        for target_id in targets:
            if target_id not in node_ids or target_id == source_id:
                continue
            key = tuple(sorted((source_id, target_id)))
            if key in seen:
                continue
            seen.add(key)
            edges.append({"source": source_id, "target": target_id})

    n = max(len(nodes), 1)
    for i, node in enumerate(nodes):
        x, y, z = fibonacci_sphere_point(i, n)
        node["x"], node["y"], node["z"] = x, y, z

    return nodes, edges


@api.get("/")
async def root():
    return {"system": "JARVIS OS", "status": "online", "time": _now_iso()}


@api.get("/sections")
async def get_sections():
    return {"sections": SECTIONS}


@api.get("/system/stats")
async def system_stats():
    nodes, edges = build_knowledge_graph()
    connections_raw = read_safe(CONNECTIONS_MD) or ""
    rows = parse_connections_table(connections_raw)
    statuses = [compute_status(r) for r in rows]
    online_count = statuses.count("online")
    online_pct = round(100 * online_count / len(statuses), 0) if statuses else 0

    skill_count = sum(1 for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else 0
    agent_count = sum(1 for p in AGENTS_DIR.iterdir() if p.suffix == ".md") if AGENTS_DIR.is_dir() else 0

    uptime_hours = round((time.time() - SERVER_START) / 3600, 2)

    return {
        "timestamp": _now_iso(),
        # decorative flavor — no real sensor behind these, kept for the HUD feel
        "core_temp": round(random.uniform(38, 46), 1),
        "power_output": round(random.uniform(82, 99), 1),
        "cpu_load": round(random.uniform(28, 74), 1),
        # grounded in real data
        "memory_load": min(100, round(len(nodes) / 2, 1)),
        "network_throughput": len(edges) * 10,
        "uptime_hours": uptime_hours,
        "active_processes": skill_count + agent_count,
        "skills": skill_count,
        "agents": agent_count,
        "shield_integrity": online_pct,
        "gauges": [
            {"id": "reactor", "label": "ARC REACTOR", "value": online_pct, "unit": "%"},
            {"id": "thermal", "label": "THERMAL", "value": round(random.uniform(40, 70), 0), "unit": "%"},
            {"id": "bandwidth", "label": "BANDWIDTH", "value": round(random.uniform(55, 92), 0), "unit": "%"},
        ],
        "throughput_series": _series(24, 60, 30),
        "load_series": _series(24, 55, 22),
    }


@api.get("/memory/nodes")
async def memory_nodes():
    files = [f for f in list_md_files(MEMORY_DIR) if f.name != "MEMORY.md"]
    entries = []
    for file_path in files:
        raw = read_safe(file_path)
        if not raw:
            continue
        data, _ = parse_frontmatter(raw)
        node_type = data.get("type") or (data.get("metadata") or {}).get("type") or "unknown"
        stat = file_path.stat()
        entries.append({
            "id": file_path.stem,
            "label": (data.get("name") or file_path.stem).upper().replace("-", " "),
            "kind": str(node_type).upper(),
            "size_mb": round(stat.st_size / (1024 * 1024), 3),
            "integrity": round(random.uniform(96, 100), 1),
            "last_access": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        })
    entries.sort(key=lambda e: e["last_access"], reverse=True)
    return {
        "total_nodes": len(entries),
        "indexed": len(entries),
        "fragmentation": round(random.uniform(1.2, 4.8), 1),
        "nodes": entries[:8],
    }


@api.get("/network/graph")
async def network_graph():
    nodes, edges = build_knowledge_graph()
    return {
        "label": "KNOWLEDGE GRAPH",
        "active_relations": len(edges),
        "nodes": nodes,
        "edges": edges,
    }


@api.get("/tools")
async def connected_tools():
    raw = read_safe(CONNECTIONS_MD) or ""
    rows = parse_connections_table(raw)
    tools = []
    for row in rows:
        status = compute_status(row)
        tools.append({
            "id": row["num"],
            "name": row["domain"].upper(),
            "status": status,
            "latency_ms": random.randint(20, 90) if status == "online" else 0,
        })
    return {"connected": sum(1 for t in tools if t["status"] == "online"), "tools": tools}


@api.get("/globe/points")
async def globe_points():
    # Decorative city markers — visual flavor for the literal-globe scene,
    # not tied to a real geo data source (this AIOS has no live location feed).
    pts = [
        {"name": "NEW YORK", "lat": 40.71, "lng": -74.00, "level": "high"},
        {"name": "LONDON", "lat": 51.50, "lng": -0.12, "level": "high"},
        {"name": "TOKYO", "lat": 35.68, "lng": 139.69, "level": "high"},
        {"name": "MALIBU", "lat": 34.02, "lng": -118.78, "level": "critical"},
        {"name": "DUBAI", "lat": 25.20, "lng": 55.27, "level": "mid"},
        {"name": "SYDNEY", "lat": -33.86, "lng": 151.20, "level": "mid"},
        {"name": "SAO PAULO", "lat": -23.55, "lng": -46.63, "level": "mid"},
        {"name": "GENEVA", "lat": 46.20, "lng": 6.14, "level": "high"},
    ]
    return {"points": pts}


@api.get("/comms")
async def comms_feed():
    # Decorative — wiring this to a real feed needs the Microsoft Graph / Slack
    # scripts already in this repo; left as a clearly-labeled stub (surfaced as
    # "SIM" in the UI) that at least mirrors the real channels this AIOS reaches.
    msgs = [
        {"from": "Slack", "channel": "#build", "preview": "Sentinel cert checklist updated · 2 items left", "unread": True},
        {"from": "M365", "channel": "inbox", "preview": "2 solicitation notices flagged for triage", "unread": True},
        {"from": "Resend", "channel": "outreach", "preview": "25 warm-intro emails queued for send", "unread": False},
        {"from": "Slack", "channel": "#pipeline", "preview": "Meridian Defense moved to hot", "unread": False},
    ]
    return {"unread": sum(1 for m in msgs if m["unread"]), "messages": msgs}


app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
