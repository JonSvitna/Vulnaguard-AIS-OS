import React, { useMemo } from "react";
import StatTile from "../components/StatTile";
import Pill from "../components/Pill";
import { titleCase, toolTone, toolLabel } from "../lib/format";

export default function Systems({ tools, stats }) {
  const list = useMemo(() => tools?.tools || [], [tools]);
  const online = list.filter((t) => t.status === "online").length;
  const standby = list.filter((t) => t.status === "standby").length;
  const offline = list.filter((t) => t.status === "offline").length;
  const total = list.length || 1;
  const healthPct = stats?.shield_integrity != null ? stats.shield_integrity : Math.round((online / total) * 100);
  const uptime = stats?.uptime_hours;

  const dist = [
    { label: "Online", n: online, tone: "var(--ok)" },
    { label: "Standby", n: standby, tone: "var(--warn)" },
    { label: "Offline", n: offline, tone: "var(--text-mut)" },
  ];

  return (
    <div className="canvas">
      <StatTile label="Healthy" value={online} numColor="var(--ok)" delta="online" deltaTone="up" />
      <StatTile label="Standby" value={standby} numColor="var(--warn)" delta="stale check" />
      <StatTile label="Offline" value={offline} numColor="var(--text-mut)" delta="not wired" />
      <StatTile label="Online %" value={healthPct} suffix="%" accent delta={uptime != null ? `${uptime}h up` : "live"} deltaTone="up" />

      <div className="block span-8">
        <div className="block-head"><span className="title display">Connected Tool Array</span><span className="id">PWR-04</span></div>
        {list.length ? (
          <div className="toolgrid">
            {list.map((t) => (
              <div key={t.id} className="tool">
                <div className="tool-top">
                  <div>
                    <div className="tname">{titleCase(t.name)}</div>
                    <div className="trole">node {t.id}</div>
                  </div>
                  <Pill tone={toolTone(t.status)} style={{ marginLeft: "auto" }}>{toolLabel(t.status)}</Pill>
                </div>
                <div className="tool-foot">
                  <span className="tsync">{t.latency_ms ? `${t.latency_ms}ms latency` : "no signal"}</span>
                  <span className="bar" style={{ width: 84 }}>
                    <i style={{ width: `${t.latency_ms ? Math.min(100, t.latency_ms) : offlineWidth(t.status)}%` }} />
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : <div className="empty">No tools registered in connections.md.</div>}
      </div>

      <div className="block span-4">
        <div className="block-head"><span className="title display">Array Health</span><span className="led" /></div>
        {dist.map((d) => (
          <div key={d.label} className="cluster">
            <span className="cn">{d.label}</span>
            <span className="bar"><i style={{ width: `${Math.round((d.n / total) * 100)}%`, background: d.tone }} /></span>
            <span className="cv">{d.n}</span>
          </div>
        ))}
        <div className="callout" style={{ marginTop: 16 }}><b>Next</b>Wire Stripe to unlock the revenue line.</div>
      </div>
    </div>
  );
}

// Give standby/offline a small visible sliver so the bar isn't empty.
function offlineWidth(status) {
  return status === "standby" ? 30 : 6;
}
