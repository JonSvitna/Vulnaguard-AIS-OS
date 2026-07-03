import React, { useEffect, useState } from "react";
import Pill from "./Pill";

function useClock() {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const p = (n) => String(n).padStart(2, "0");
  return `${p(now.getHours())}:${p(now.getMinutes())}:${p(now.getSeconds())}`;
}

export default function CommandBar({ section, online }) {
  const clock = useClock();
  const tone = online ? "ok" : "warn";
  return (
    <div className="cmdbar">
      <div className="cmd-title">
        <h1 className="display">{section.label}</h1>
        <span className="id">{section.code}</span>
      </div>
      <label className="search">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="7" /><path d="M21 21l-4.3-4.3" /></svg>
        <input placeholder="query memory, tools, decisions…" aria-label="Command search" />
        <kbd>/</kbd>
      </label>
      <div className="cmd-right">
        <span className="clock">{clock}</span>
        <Pill tone={tone}>{online ? "All systems" : "Offline"}</Pill>
        <span className="avatar">S</span>
      </div>
    </div>
  );
}
