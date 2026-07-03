import React, { useMemo, useState } from "react";
import Pill from "../components/Pill";
import { relativeTime, titleCase } from "../lib/format";

const DOMAIN_COLORS = ["#22d3ee", "#7dd3fc", "#67e8f9", "#a5b4fc", "#9fb4c2", "#5b7180"];

// Map a node kind to a pill tone for the table.
function kindTone(kind) {
  const k = (kind || "").toLowerCase();
  if (k.includes("decision")) return "ok";
  if (k.includes("note") || k.includes("wiki")) return "cyan";
  return "idle";
}

export default function Memory({ memory }) {
  const nodes = useMemo(() => memory?.nodes || [], [memory]);
  const [query, setQuery] = useState("");
  const [chip, setChip] = useState("all");

  const kinds = useMemo(() => {
    const set = new Map();
    nodes.forEach((n) => set.set(n.kind, (set.get(n.kind) || 0) + 1));
    return [...set.entries()].map(([name, count], i) => ({ name, count, color: DOMAIN_COLORS[i % DOMAIN_COLORS.length] }));
  }, [nodes]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return nodes.filter((n) => {
      if (chip !== "all" && n.kind !== chip) return false;
      if (!q) return true;
      return (n.label || "").toLowerCase().includes(q) || (n.kind || "").toLowerCase().includes(q);
    });
  }, [nodes, query, chip]);

  const recent = useMemo(() => [...nodes].sort((a, b) => (b.last_access || "").localeCompare(a.last_access || "")).slice(0, 4), [nodes]);

  return (
    <div className="canvas">
      <div className="block span-8">
        <div className="block-head"><span className="title display">Indexed Memory</span><span className="id">MEM-03</span></div>
        <label className="infilter">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="7" /><path d="M21 21l-4.3-4.3" /></svg>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={`filter ${memory?.total_nodes ?? nodes.length} nodes by title or kind…`}
            aria-label="Filter memory"
          />
        </label>
        <div className="chips">
          <button type="button" className={`chip${chip === "all" ? " on" : ""}`} onClick={() => setChip("all")}>all</button>
          {kinds.map((k) => (
            <button type="button" key={k.name} className={`chip${chip === k.name ? " on" : ""}`} onClick={() => setChip(k.name)}>{k.name.toLowerCase()}</button>
          ))}
        </div>
        <div className="mtable">
          <div className="mrow head"><span>Node</span><span style={{ textAlign: "center" }}>Kind</span><span style={{ textAlign: "center" }}>Links</span><span style={{ textAlign: "right" }}>Updated</span></div>
          {filtered.length ? filtered.map((n) => (
            <div key={n.id} className="mrow">
              <span className="mt">{titleCase(n.label)}</span>
              <Pill tone={kindTone(n.kind)} style={{ justifySelf: "center" }}>{(n.kind || "node").toLowerCase()}</Pill>
              <span className="ml">{n.links != null ? n.links : "—"}</span>
              <span className="mu">{relativeTime(n.last_access)}</span>
            </div>
          )) : <div className="empty">No nodes match this filter.</div>}
        </div>
      </div>

      <div className="block span-4">
        <div className="block-head"><span className="title display">Domains</span></div>
        {kinds.length ? kinds.map((k) => (
          <div key={k.name} className="domain">
            <span className="dc" style={{ background: k.color }} />
            <span className="dnm">{titleCase(k.name)}</span>
            <span className="dct">{k.count}</span>
          </div>
        )) : <div className="empty">No domains indexed.</div>}

        <div className="block-head" style={{ marginTop: 20 }}><span className="title display">Recent Captures</span></div>
        {recent.length ? recent.map((n) => (
          <div key={n.id} className="comm">
            <span className="ch">{relativeTime(n.last_access)}</span>
            <span className="msg"><b>{(n.kind || "Note").toLowerCase()}</b> — {titleCase(n.label)}</span>
          </div>
        )) : <div className="empty">No recent captures.</div>}
      </div>
    </div>
  );
}
