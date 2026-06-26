import React, { useCallback, useEffect, useState } from "react";
import "./App.css";
import { SECTIONS } from "./data/sections";
import api from "./lib/api";
import { usePointer } from "./hooks/usePointer";
import SceneCanvas from "./scenes/SceneCanvas";
import HudFrame from "./components/HudFrame";
import SectionPanels from "./components/SectionPanels";
import Dial from "./components/Dial";
import DetailOverlay from "./components/DetailOverlay";

export default function App() {
  const [active, setActive] = useState(0);
  const [data, setData] = useState({ stats: null, memory: null, network: null, tools: null, comms: null });
  const [points, setPoints] = useState([]);
  const [detail, setDetail] = useState(null);
  const [hovered, setHovered] = useState(null);
  const [booted, setBooted] = useState(false);
  const pointer = usePointer();

  const section = SECTIONS[active];

  // initial load
  useEffect(() => {
    let mounted = true;
    Promise.allSettled([
      api.systemStats(), api.memoryNodes(), api.networkGraph(),
      api.tools(), api.comms(), api.globePoints(),
    ]).then((res) => {
      if (!mounted) return;
      const [stats, memory, network, tools, comms, gp] = res.map((r) => (r.status === "fulfilled" ? r.value : null));
      setData({ stats, memory, network, tools, comms });
      if (gp?.points) setPoints(gp.points);
      setBooted(true);
    });
    return () => { mounted = false; };
  }, []);

  // live-feel polling of system stats
  useEffect(() => {
    const id = setInterval(() => {
      api.systemStats().then((s) => setData((d) => ({ ...d, stats: s }))).catch(() => {});
    }, 4000);
    return () => clearInterval(id);
  }, []);

  const navigate = useCallback((idx) => {
    setActive(((idx % SECTIONS.length) + SECTIONS.length) % SECTIONS.length);
    setDetail(null);
  }, []);

  const onPointSelect = useCallback((p) => {
    setDetail({
      title: p.name, code: p.level.toUpperCase(),
      rows: [
        { label: "LATITUDE", value: p.lat.toFixed(2) },
        { label: "LONGITUDE", value: p.lng.toFixed(2) },
        { label: "PRIORITY", value: p.level.toUpperCase() },
      ],
      note: "Tracked node. Live geospatial relay established.",
    });
  }, []);

  return (
    <div className="app" data-testid="jarvis-app">
      <SceneCanvas
        scene={section.scene}
        points={points}
        graph={data.network}
        onPointHover={setHovered}
        onPointSelect={onPointSelect}
      />

      <div className="hud-grid-overlay" />

      <HudFrame active={section.label} status={booted ? "ONLINE" : "BOOTING"} />

      <SectionPanels active={section.id} data={data} pointer={pointer} onDetail={setDetail} />

      {hovered && (
        <div className="point-tooltip" data-testid="point-tooltip"
          style={{ left: "50%", bottom: "30%" }}>
          <span className="tt-name">{hovered.name}</span>
          <span className="tt-meta">{hovered.lat.toFixed(1)}, {hovered.lng.toFixed(1)} · {hovered.level.toUpperCase()}</span>
        </div>
      )}

      <div className="section-caption" data-testid="section-caption">
        <span className="cap-code font-display">{section.code}</span>
        <span className="cap-desc">{section.desc}</span>
      </div>

      <Dial activeIndex={active} onNavigate={navigate} />

      <DetailOverlay detail={detail} onClose={() => setDetail(null)} />

      {!booted && (
        <div className="boot-screen" data-testid="boot-screen">
          <span className="boot-text font-display">INITIALIZING JARVIS</span>
          <div className="boot-bar"><span /></div>
        </div>
      )}
    </div>
  );
}
