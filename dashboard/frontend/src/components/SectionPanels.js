import React from "react";
import { AnimatePresence } from "framer-motion";
import GlassPanel from "./GlassPanel";
import Gauge from "./Gauge";
import Sparkline from "./Sparkline";
import Radar from "./Radar";

const Stat = ({ label, value, unit }) => (
  <div className="stat">
    <span className="stat-label">{label}</span>
    <span className="stat-value font-display">{value}<small>{unit}</small></span>
  </div>
);

const Bar = ({ label, pct }) => (
  <div className="bar-row">
    <span className="bar-label">{label}</span>
    <span className="bar-track"><span className="bar-fill" style={{ width: `${pct}%` }} /></span>
    <span className="bar-pct">{Math.round(pct)}%</span>
  </div>
);

export default function SectionPanels({ active, data, pointer, onDetail }) {
  const { stats, memory, network, tools, comms } = data;
  const blips = [
    { x: 0.4, y: -0.3 }, { x: -0.5, y: 0.2 }, { x: 0.15, y: 0.55 }, { x: -0.25, y: -0.5 },
  ];

  return (
    <AnimatePresence mode="wait">
      <div className="panel-layer" key={active} data-testid={`panels-${active}`}>

        {active === "overview" && (
          <>
            <GlassPanel testid="panel-system-core" title="SYSTEM CORE" code="SYS-01"
              className="pos-tl" pointer={pointer} depth={1.4} delay={0.05} floatPhase={0}>
              <div className="gauge-grid">
                {(stats?.gauges || []).map((g) => (
                  <Gauge key={g.id} label={g.label} value={g.value} unit={g.unit} />
                ))}
              </div>
            </GlassPanel>

            <GlassPanel testid="panel-telemetry" title="TELEMETRY" code="DATA-FLOW"
              className="pos-tr" pointer={pointer} depth={1.1} delay={0.18} floatPhase={1.2}>
              <Sparkline data={stats?.throughput_series || []} width={220} height={54} />
              <Bar label="CPU LOAD" pct={stats?.cpu_load || 0} />
              <Bar label="MEMORY" pct={stats?.memory_load || 0} />
              <Stat label="THROUGHPUT" value={stats?.network_throughput || 0} unit=" MB/S" />
            </GlassPanel>

            <GlassPanel testid="panel-radar" title="PERIMETER SCAN" code="RDR-09"
              className="pos-bl" pointer={pointer} depth={1.7} delay={0.3} floatPhase={2.1}>
              <div className="radar-row">
                <Radar blips={blips} size={118} />
                <div className="radar-readout">
                  <Stat label="CONTACTS" value={blips.length} unit="" />
                  <Stat label="SHIELD" value={stats?.shield_integrity || 0} unit="%" />
                  <Stat label="CORE TEMP" value={stats?.core_temp || 0} unit="°" />
                </div>
              </div>
            </GlassPanel>

            <GlassPanel testid="panel-power" title="ARC OUTPUT" code="PWR"
              className="pos-rmid" pointer={pointer} depth={0.8} delay={0.4} floatPhase={0.6}>
              <Stat label="POWER OUTPUT" value={stats?.power_output || 0} unit="%" />
              <Stat label="PROCESSES" value={stats?.active_processes || 0} unit="" />
              <Stat label="UPTIME" value={stats?.uptime_hours || 0} unit="H" />
            </GlassPanel>
          </>
        )}

        {active === "network" && (
          <>
            <GlassPanel testid="panel-graph" title="KNOWLEDGE GRAPH" code="NET-02"
              className="pos-tl" pointer={pointer} depth={1.4} delay={0.05}>
              <Stat label="NODES" value={network?.nodes?.length || 0} unit="" />
              <Stat label="RELATIONS" value={network?.active_relations || 0} unit="" />
              <Bar label="SYNC" pct={92} />
              <Bar label="COHERENCE" pct={87} />
            </GlassPanel>

            <GlassPanel testid="panel-relations" title="RELATION STREAM" code="LIVE"
              className="pos-tr" pointer={pointer} depth={1.1} delay={0.18}>
              <ul className="feed">
                {(network?.edges || []).slice(0, 6).map((e, i) => (
                  <li key={i}><span className="feed-dot" />{e.source.toUpperCase()} → {e.target.toUpperCase()}</li>
                ))}
              </ul>
            </GlassPanel>

            <GlassPanel testid="panel-pulse" title="NEURAL PULSE" code="HZ"
              className="pos-bl" pointer={pointer} depth={1.7} delay={0.3}>
              <Sparkline data={[20, 60, 35, 80, 45, 90, 55, 75, 40, 85]} width={200} height={50} />
              <Stat label="FIRING RATE" value={42} unit=" HZ" />
            </GlassPanel>
          </>
        )}

        {active === "memory" && (
          <>
            <GlassPanel testid="panel-vault" title="MEMORY VAULT" code="MEM-03"
              className="pos-tl" pointer={pointer} depth={1.4} delay={0.05}>
              <Stat label="TOTAL NODES" value={memory?.total_nodes || 0} unit="" />
              <Stat label="INDEXED" value={memory?.indexed || 0} unit="" />
              <Bar label="FRAGMENTATION" pct={memory?.fragmentation || 0} />
            </GlassPanel>

            <GlassPanel testid="panel-nodes" title="NODE INDEX" code="VAULT"
              className="pos-tr" pointer={pointer} depth={1.1} delay={0.18}>
              <ul className="feed scroll">
                {(memory?.nodes || []).map((n) => (
                  <li key={n.id} className="clickable" data-testid={`mem-node-${n.id}`}
                    onClick={() => onDetail({
                      title: n.label, code: n.id.toUpperCase(),
                      rows: [
                        { label: "KIND", value: n.kind },
                        { label: "SIZE", value: `${n.size_mb} MB` },
                        { label: "INTEGRITY", value: `${n.integrity}%` },
                      ],
                      note: "Memory node available for recall and cross-reference.",
                    })}>
                    <span className="feed-dot" />{n.label}<span className="feed-tag">{n.kind}</span>
                  </li>
                ))}
              </ul>
            </GlassPanel>
          </>
        )}

        {active === "systems" && (
          <>
            <GlassPanel testid="panel-tools" title="TOOL ARRAY" code="PWR-04"
              className="pos-tl" pointer={pointer} depth={1.4} delay={0.05}>
              <ul className="feed">
                {(tools?.tools || []).map((t) => (
                  <li key={t.id} className="clickable" data-testid={`tool-${t.id}`}
                    onClick={() => onDetail({
                      title: t.name, code: t.id.toUpperCase(),
                      rows: [
                        { label: "STATUS", value: t.status.toUpperCase() },
                        { label: "LATENCY", value: `${t.latency_ms} ms` },
                      ],
                      note: "Connected subsystem reporting to the core relay.",
                    })}>
                    <span className={`feed-dot ${t.status}`} />{t.name}
                    <span className="feed-tag">{t.status.toUpperCase()}</span>
                  </li>
                ))}
              </ul>
            </GlassPanel>

            <GlassPanel testid="panel-sysgauge" title="SUBSYSTEMS" code="DIAG"
              className="pos-tr" pointer={pointer} depth={1.1} delay={0.18}>
              <div className="gauge-grid">
                {(stats?.gauges || []).map((g) => (
                  <Gauge key={g.id} label={g.label} value={g.value} unit={g.unit} />
                ))}
              </div>
            </GlassPanel>
          </>
        )}

        {active === "comms" && (
          <>
            <GlassPanel testid="panel-channels" title="SECURE CHANNELS" code="COM-05"
              className="pos-tl" pointer={pointer} depth={1.4} delay={0.05}>
              <ul className="feed">
                {(comms?.messages || []).map((m, i) => (
                  <li key={i} className="clickable" data-testid={`msg-${i}`}
                    onClick={() => onDetail({
                      title: m.from, code: m.channel,
                      rows: [{ label: "CHANNEL", value: m.channel }, { label: "STATE", value: m.unread ? "UNREAD" : "READ" }],
                      note: m.preview,
                    })}>
                    <span className={`feed-dot ${m.unread ? "online" : ""}`} />{m.from}
                    <span className="feed-tag">{m.channel}</span>
                  </li>
                ))}
              </ul>
            </GlassPanel>

            <GlassPanel testid="panel-signal" title="SIGNAL" code="RF"
              className="pos-tr" pointer={pointer} depth={1.1} delay={0.18}>
              <Sparkline data={[40, 55, 48, 70, 60, 82, 75, 90, 68, 80]} width={200} height={50} />
              <Stat label="UNREAD" value={comms?.unread || 0} unit="" />
              <Stat label="ENCRYPTION" value="AES-256" unit="" />
            </GlassPanel>
          </>
        )}
      </div>
    </AnimatePresence>
  );
}
