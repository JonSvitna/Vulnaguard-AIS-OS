import React, { useEffect, useState } from "react";

function Clock() {
  const [t, setT] = useState(new Date());
  useEffect(() => {
    const id = setInterval(() => setT(new Date()), 1000);
    return () => clearInterval(id);
  }, []);
  const hh = String(t.getHours()).padStart(2, "0");
  const mm = String(t.getMinutes()).padStart(2, "0");
  const ss = String(t.getSeconds()).padStart(2, "0");
  return (
    <span className="hud-clock font-display" data-testid="hud-clock">
      {hh}<span className="blink">:</span>{mm}<span className="blink">:</span>{ss}
    </span>
  );
}

export default function HudFrame({ active, status = "ONLINE" }) {
  return (
    <>
      {/* top bar */}
      <header className="hud-top" data-testid="hud-top">
        <div className="hud-brand">
          <span className="brand-mark" />
          <div className="brand-text">
            <span className="brand-name font-display">JARVIS</span>
            <span className="brand-sub">OPERATING SYSTEM v4.7</span>
          </div>
        </div>
        <div className="hud-top-center">
          <span className="sys-tag">SECTOR // {active}</span>
        </div>
        <div className="hud-top-right">
          <span className={`status-dot ${status.toLowerCase()}`} />
          <span className="status-text">{status}</span>
          <Clock />
        </div>
      </header>

      {/* screen corner brackets */}
      <div className="frame-corner fc-tl" />
      <div className="frame-corner fc-tr" />
      <div className="frame-corner fc-bl" />
      <div className="frame-corner fc-br" />

      {/* side rails */}
      <div className="rail rail-left">
        {Array.from({ length: 22 }).map((_, i) => (
          <span key={i} style={{ opacity: i % 4 === 0 ? 0.7 : 0.25 }} />
        ))}
      </div>
      <div className="scanline" />
    </>
  );
}
