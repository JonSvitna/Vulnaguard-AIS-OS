import React, { useEffect, useState } from "react";
import StatTile from "../components/StatTile";
import Pill from "../components/Pill";
import NetworkCanvas from "../components/NetworkCanvas";
import { compact, titleCase, toolTone, toolLabel, briefDate } from "../lib/format";

// "2026-06-30" -> "06·30"
function shortDate(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || "");
  return m ? `${m[2]}·${m[3]}` : (iso || "").slice(0, 5);
}

const RELEVANCE = {
  moderate: { tone: "warn", label: "hot" },
  low: { tone: "idle", label: "low" },
  review: { tone: "cyan", label: "review" },
};

function Check({ done, onToggle }) {
  return (
    <button type="button" className="check" onClick={onToggle} aria-pressed={done} aria-label={done ? "Mark incomplete" : "Mark complete"}>
      <svg viewBox="0 0 24 24"><path d="M5 12l5 5L20 6" /></svg>
    </button>
  );
}

export default function Overview({ stats, memory, network, tools, comms, brief, decisions, leads, onNavigate }) {
  // Local done-state keyed by priority title; brief priorities are the source.
  const priorities = brief?.priorities || [];
  const [done, setDone] = useState({});
  useEffect(() => { setDone({}); }, [brief]);
  const toggle = (key) => setDone((d) => ({ ...d, [key]: !d[key] }));

  const skills = stats?.skills;
  const agents = stats?.agents;
  const processes = stats?.active_processes;
  const memNodes = memory?.total_nodes;
  const links = network?.active_relations;
  const connected = tools?.connected;
  const totalTools = tools?.tools?.length;
  const warnTools = (tools?.tools || []).filter((t) => t.status === "standby").length;
  const load = stats?.load_series;
  const flow = stats?.throughput_series;

  const toolRows = (tools?.tools || []).slice(0, 6);
  const commRows = (comms?.messages || []).slice(0, 4);
  const decRows = decisions?.decisions || [];
  const leadRows = leads?.leads || [];

  return (
    <div className="canvas">
      <StatTile
        label="Skills · Agents"
        value={skills != null ? skills : processes != null ? processes : "—"}
        suffix={agents != null ? `·${agents}` : undefined}
        accent
        delta="loaded"
        series={load}
      />
      <StatTile label="Memory Nodes" value={memNodes != null ? memNodes : "—"} delta="indexed" series={load} />
      <StatTile label="Graph Links" value={links != null ? compact(links) : "—"} delta="linked" series={flow} />
      <StatTile
        label="Connections"
        value={connected != null ? connected : "—"}
        suffix={totalTools != null ? `/${totalTools}` : undefined}
        delta={warnTools ? `${warnTools} stale` : "healthy"}
        deltaTone={warnTools ? "flat" : "up"}
      />

      <div className="block brief span-8">
        <div className="block-head"><span className="title display">Daily Brief</span><span className="led" /></div>
        <div className="date">{briefDate(brief?.date ? new Date(brief.date) : new Date())}</div>
        {priorities.length ? priorities.map((p, i) => (
          <div key={p.title} className={`task${done[p.title] ? " done" : ""}`}>
            <Check done={!!done[p.title]} onToggle={() => toggle(p.title)} />
            <span className="label">{p.title}</span>
            <span className="who">P{i + 1}</span>
          </div>
        )) : <div className="empty">No priorities set in context/priorities.md.</div>}
        {brief?.theme ? <div className="callout"><b>Standing</b>{brief.theme}</div> : null}
      </div>

      <div className="block span-4">
        <div className="block-head"><span className="title display">Connected Systems</span><span className="action">manage</span></div>
        {toolRows.length ? toolRows.map((t) => (
          <div key={t.id} className="row">
            <span className="sys">{titleCase(t.name)}</span>
            <Pill tone={toolTone(t.status)}>{toolLabel(t.status)}</Pill>
            <span className="ts">{t.latency_ms ? `${t.latency_ms}ms` : "—"}</span>
          </div>
        )) : <div className="empty">No connections indexed.</div>}
      </div>

      <div className="block netpanel span-8">
        <div className="block-head"><span className="title display">Knowledge Network</span><button type="button" className="action" onClick={() => onNavigate("network")}>expand ↗</button></div>
        <div className="net-canvas-wrap sm">
          <span className="corner tl" /><span className="corner tr" /><span className="corner bl" /><span className="corner br" />
          <NetworkCanvas nodes={network?.nodes} edges={network?.edges} fallbackCount={34} />
          <div className="net-legend">
            <span><b style={{ background: "#22d3ee" }} />AIOS memory</span>
            <span><b style={{ background: "#67e8f9" }} />Vault</span>
          </div>
        </div>
      </div>

      <div className="block span-4">
        <div className="block-head">
          <span className="title display">Comms</span>
          {comms?.simulated !== false ? <span className="sim-tag">SIM</span> : null}
          <span className="led" style={{ marginLeft: "auto", background: comms?.simulated === false ? "var(--cyan)" : "var(--warn)", boxShadow: comms?.simulated === false ? "0 0 6px rgba(34,211,238,.8)" : "0 0 6px rgba(251,191,36,.7)" }} />
        </div>
        {commRows.length ? commRows.map((m, i) => (
          <div key={i} className="comm">
            {m.unread ? <span className="unread" /> : null}
            <span className="ch">{m.channel}</span>
            <span className="msg"><b>{titleCase(m.from)}</b> — {m.preview}</span>
          </div>
        )) : <div className="empty">Relay feed offline.</div>}
      </div>

      <div className="block span-6">
        <div className="block-head"><span className="title display">Decisions Log</span><span className="action">append</span></div>
        {decRows.length ? decRows.map((x) => (
          <div key={x.date + x.title} className="dec">
            <span className="d">{shortDate(x.date)}</span>
            <span className="txt">{x.title}</span>
          </div>
        )) : <div className="empty">No decisions logged.</div>}
      </div>

      <div className="block span-6">
        <div className="block-head"><span className="title display">Leads Pipeline</span><span className="action">triage</span></div>
        <div className="leads-head">
          <div className="leadstat"><div className="n">{leads?.inbox ?? "—"}</div><div className="eyebrow">Inbox</div></div>
          <div className="leadstat"><div className="n hot">{leads?.hot ?? "—"}</div><div className="eyebrow">Hot</div></div>
          <div className="leadstat"><div className="n">{leads?.closed ?? "—"}</div><div className="eyebrow">Closed</div></div>
        </div>
        {leadRows.length ? leadRows.map((l, i) => {
          const r = RELEVANCE[l.relevance] || RELEVANCE.review;
          return (
            <div key={l.name + i} className="lead">
              <div><div className="nm">{l.name}</div><div className="src">{l.location} · {l.source}</div></div>
              <Pill tone={r.tone} style={{ marginLeft: "auto" }}>{r.label}</Pill>
            </div>
          );
        }) : <div className="empty">Lead inbox is empty.</div>}
      </div>
    </div>
  );
}
