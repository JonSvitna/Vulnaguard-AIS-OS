import React, { useCallback, useEffect, useState } from "react";
import api from "./lib/api";
import { SECTIONS, sectionIndex } from "./data/sections";
import Sidebar from "./components/Sidebar";
import CommandBar from "./components/CommandBar";
import Overview from "./views/Overview";
import Network from "./views/Network";
import Memory from "./views/Memory";
import Systems from "./views/Systems";
import Comms from "./views/Comms";

export default function App() {
  const [activeId, setActiveId] = useState("overview");
  const [data, setData] = useState({ stats: null, memory: null, network: null, tools: null, comms: null });
  const [booted, setBooted] = useState(false);
  const [online, setOnline] = useState(false);

  // Initial load — allSettled so one dead endpoint never blanks the whole app.
  useEffect(() => {
    let mounted = true;
    Promise.allSettled([
      api.systemStats(), api.memoryNodes(), api.networkGraph(), api.tools(), api.comms(),
    ]).then((res) => {
      if (!mounted) return;
      const [stats, memory, network, tools, comms] = res.map((r) => (r.status === "fulfilled" ? r.value : null));
      setData({ stats, memory, network, tools, comms });
      setOnline(res.some((r) => r.status === "fulfilled"));
      setBooted(true);
    });
    return () => { mounted = false; };
  }, []);

  // Live-feel: refresh system stats periodically.
  useEffect(() => {
    const id = setInterval(() => {
      api.systemStats()
        .then((s) => { setData((d) => ({ ...d, stats: s })); setOnline(true); })
        .catch(() => setOnline(false));
    }, 5000);
    return () => clearInterval(id);
  }, []);

  const navigate = useCallback((id) => {
    if (sectionIndex(id) >= 0) setActiveId(id);
  }, []);

  const section = SECTIONS[Math.max(0, sectionIndex(activeId))];

  const tools = data.tools?.tools || [];
  const health = {
    online: tools.filter((t) => t.status === "online").length,
    warn: tools.filter((t) => t.status === "standby").length,
    idle: tools.filter((t) => t.status === "offline").length,
    total: tools.length,
  };
  const counts = {
    memory: data.memory?.total_nodes,
    systems: data.tools ? `${data.tools.connected}/${tools.length}` : undefined,
  };

  return (
    <div className="app">
      <Sidebar
        sections={SECTIONS}
        active={activeId}
        onNavigate={navigate}
        counts={counts}
        health={health}
      />
      <main>
        <CommandBar section={section} online={online} />
        {activeId === "overview" && (
          <Overview stats={data.stats} memory={data.memory} network={data.network} tools={data.tools} comms={data.comms} onNavigate={navigate} />
        )}
        {activeId === "network" && <Network network={data.network} />}
        {activeId === "memory" && <Memory memory={data.memory} />}
        {activeId === "systems" && <Systems tools={data.tools} stats={data.stats} />}
        {activeId === "comms" && <Comms comms={data.comms} />}
      </main>

      {!booted && (
        <div className="boot">
          <span className="boot-text display">Initializing Sentinel OS</span>
          <div className="boot-bar"><span /></div>
        </div>
      )}
    </div>
  );
}
