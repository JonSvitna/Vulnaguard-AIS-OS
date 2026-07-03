import React, { useState } from "react";
import StatTile from "../components/StatTile";
import Pill from "../components/Pill";
import NetworkCanvas from "../components/NetworkCanvas";
import { compact, titleCase, relativeTime, toolTone, toolLabel, briefDate } from "../lib/format";

// Curated content that has no backend source yet (mirrors the repo's real
// priorities / decisions / leads). Wire to files/APIs when those land.
const TASKS = [
  { label: "Wire Obsidian vault sync into memory graph", who: "AIOS", done: true },
  { label: "Close the last 2 Sentinel CMMC cert gaps", who: "Sean" },
  { label: "SEO agent — send 25 warm-intro outreach emails", who: "SEO" },
  { label: "Publish website content drop to drive traffic", who: "Sean" },
];

const DECISIONS = [
  { d: "07·02", txt: "Archived vanilla-JS dashboard; rebuilt on Notion-OS layout", tone: "cyan", tag: "infra" },
  { d: "06·28", txt: "SEO agent switches to warm-intro outreach over cold", tone: "ok", tag: "growth" },
  { d: "06·24", txt: "Sentinel pricing locked to a 3-tier matrix", tone: "cyan", tag: "product" },
  { d: "06·19", txt: "Obsidian vault set as the business second-brain", tone: "cyan", tag: "infra" },
];

const LEADS = [
  { nm: "Meridian Defense LLC", src: "M365 · solicitation", tone: "warn", st: "hot" },
  { nm: "Cobalt Ridge Mfg", src: "SEO · inbound", tone: "cyan", st: "new" },
  { nm: "Harbor Point Clinic", src: "website · outdated site", tone: "cyan", st: "new" },
];

function Check({ done, onToggle }) {
  return (
    <button type="button" className="check" onClick={onToggle} aria-pressed={done} aria-label={done ? "Mark incomplete" : "Mark complete"}>
      <svg viewBox="0 0 24 24"><path d="M5 12l5 5L20 6" /></svg>
    </button>
  );
}

export default function Overview({ stats, memory, network, tools, comms, onNavigate }) {
  const [tasks, setTasks] = useState(TASKS);
  const toggle = (i) => setTasks((t) => t.map((x, idx) => (idx === i ? { ...x, done: !x.done } : x)));

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
        <div className="date">{briefDate()}</div>
        {tasks.map((t, i) => (
          <div key={t.label} className={`task${t.done ? " done" : ""}`}>
            <Check done={t.done} onToggle={() => toggle(i)} />
            <span className="label">{t.label}</span>
            <span className="who">{t.who}</span>
          </div>
        ))}
        <div className="callout"><b>Ship</b>Close the last 2 Sentinel cert gaps before EOD — everything else waits.</div>
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
        <div className="block-head"><span className="title display">Comms</span><span className="sim-tag">SIM</span><span className="led" style={{ marginLeft: "auto", background: "var(--warn)", boxShadow: "0 0 6px rgba(251,191,36,.7)" }} /></div>
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
        {DECISIONS.map((x) => (
          <div key={x.d} className="dec">
            <span className="d">{x.d}</span>
            <span className="txt">{x.txt}</span>
            <Pill tone={x.tone}>{x.tag}</Pill>
          </div>
        ))}
      </div>

      <div className="block span-6">
        <div className="block-head"><span className="title display">Leads Pipeline</span><span className="action">triage</span></div>
        <div className="leads-head">
          <div className="leadstat"><div className="n">4</div><div className="eyebrow">Inbox</div></div>
          <div className="leadstat"><div className="n hot">1</div><div className="eyebrow">Hot</div></div>
          <div className="leadstat"><div className="n">0</div><div className="eyebrow">Closed</div></div>
        </div>
        {LEADS.map((l) => (
          <div key={l.nm} className="lead">
            <div><div className="nm">{l.nm}</div><div className="src">{l.src}</div></div>
            <Pill tone={l.tone} style={{ marginLeft: "auto" }}>{l.st}</Pill>
          </div>
        ))}
      </div>
    </div>
  );
}
