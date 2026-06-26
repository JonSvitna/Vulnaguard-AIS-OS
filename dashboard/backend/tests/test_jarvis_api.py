"""JARVIS OS backend API tests."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://914bd8ad-4512-4e5b-b805-a6ed1986bb1e.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# Root health
def test_root_online(session):
    r = session.get(f"{API}/", timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert data["system"] == "JARVIS OS"
    assert data["status"] == "online"
    assert "time" in data


# Sections
def test_sections(session):
    r = session.get(f"{API}/sections", timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert "sections" in data and isinstance(data["sections"], list)
    ids = [s["id"] for s in data["sections"]]
    assert ids == ["overview", "network", "memory", "systems", "comms"]
    for s in data["sections"]:
        for k in ("id", "label", "code", "scene"):
            assert k in s


# System stats
def test_system_stats(session):
    r = session.get(f"{API}/system/stats", timeout=15)
    assert r.status_code == 200
    d = r.json()
    for k in ("timestamp", "core_temp", "power_output", "cpu_load", "memory_load",
              "network_throughput", "uptime_hours", "active_processes",
              "shield_integrity", "gauges", "throughput_series", "load_series"):
        assert k in d, f"missing {k}"
    assert isinstance(d["gauges"], list) and len(d["gauges"]) == 3
    for g in d["gauges"]:
        assert {"id", "label", "value", "unit"} <= set(g.keys())
    assert len(d["throughput_series"]) == 24
    assert len(d["load_series"]) == 24


# Memory nodes
def test_memory_nodes(session):
    r = session.get(f"{API}/memory/nodes", timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert d["total_nodes"] == 2048
    assert d["indexed"] == 2003
    assert isinstance(d["fragmentation"], (int, float))
    assert isinstance(d["nodes"], list) and len(d["nodes"]) == 8
    for n in d["nodes"]:
        assert {"id", "label", "kind", "size_mb", "integrity", "last_access"} <= set(n.keys())
        assert n["id"].startswith("mem-")


# Network graph
def test_network_graph(session):
    r = session.get(f"{API}/network/graph", timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert d["label"] == "KNOWLEDGE GRAPH"
    assert isinstance(d["nodes"], list) and len(d["nodes"]) == 60
    for n in d["nodes"]:
        assert {"id", "x", "y", "z", "weight"} <= set(n.keys())
    assert isinstance(d["edges"], list) and len(d["edges"]) >= 60
    for e in d["edges"]:
        assert "source" in e and "target" in e
    assert d["active_relations"] == len(d["edges"])


# Tools
def test_tools(session):
    r = session.get(f"{API}/tools", timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert "tools" in d and isinstance(d["tools"], list)
    assert len(d["tools"]) == 6
    online = sum(1 for t in d["tools"] if t["status"] == "online")
    assert d["connected"] == online
    for t in d["tools"]:
        assert {"id", "name", "status", "latency_ms"} <= set(t.keys())


# Globe points
def test_globe_points(session):
    r = session.get(f"{API}/globe/points", timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert isinstance(d["points"], list) and len(d["points"]) == 8
    names = {p["name"] for p in d["points"]}
    assert {"NEW YORK", "LONDON", "TOKYO", "MALIBU"} <= names
    for p in d["points"]:
        assert {"name", "lat", "lng", "level"} <= set(p.keys())


# Comms
def test_comms(session):
    r = session.get(f"{API}/comms", timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert isinstance(d["messages"], list) and len(d["messages"]) == 4
    unread = sum(1 for m in d["messages"] if m["unread"])
    assert d["unread"] == unread
    for m in d["messages"]:
        assert {"from", "channel", "preview", "unread"} <= set(m.keys())
