import React from "react";

// Concentric circular gauge with tick marks and an animated arc value.
export default function Gauge({ value = 70, label = "", unit = "%", size = 92 }) {
  const r = size / 2 - 8;
  const c = size / 2;
  const circ = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(100, value));
  const dash = (pct / 100) * circ * 0.75; // 270deg sweep
  const ticks = Array.from({ length: 36 });

  return (
    <div className="gauge" data-testid={`gauge-${label.toLowerCase().replace(/\s+/g, "-")}`}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <defs>
          <linearGradient id={`gg-${label}`} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#22d3ee" />
            <stop offset="100%" stopColor="#ecfeff" />
          </linearGradient>
        </defs>
        {ticks.map((_, i) => {
          const a = (i / ticks.length) * Math.PI * 2;
          const x1 = c + Math.cos(a) * (r + 4);
          const y1 = c + Math.sin(a) * (r + 4);
          const x2 = c + Math.cos(a) * (r + (i % 3 === 0 ? 7 : 5));
          const y2 = c + Math.sin(a) * (r + (i % 3 === 0 ? 7 : 5));
          return (
            <line key={i} x1={x1} y1={y1} x2={x2} y2={y2}
              stroke="rgba(34,211,238,0.35)" strokeWidth="1" />
          );
        })}
        <circle cx={c} cy={c} r={r} fill="none" stroke="rgba(34,211,238,0.12)" strokeWidth="3" />
        <circle
          cx={c} cy={c} r={r} fill="none"
          stroke={`url(#gg-${label})`} strokeWidth="3" strokeLinecap="round"
          strokeDasharray={`${dash} ${circ}`}
          transform={`rotate(135 ${c} ${c})`}
          style={{ transition: "stroke-dasharray 1.2s cubic-bezier(.2,.8,.2,1)", filter: "drop-shadow(0 0 4px rgba(34,211,238,0.8))" }}
        />
        <text x={c} y={c - 2} textAnchor="middle" className="gauge-val font-display"
          fill="#ecfeff" fontSize="18">{Math.round(pct)}</text>
        <text x={c} y={c + 13} textAnchor="middle" fill="rgba(103,232,249,0.7)" fontSize="8">{unit}</text>
      </svg>
      <span className="gauge-label">{label}</span>
    </div>
  );
}
