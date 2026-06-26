import React from "react";

// Sweeping radar / circular scope with concentric rings and rotating beam.
export default function Radar({ size = 120, blips = [] }) {
  const c = size / 2;
  const rings = [0.33, 0.66, 1];
  return (
    <div className="radar" data-testid="radar-scope">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <defs>
          <radialGradient id="radar-sweep" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(34,211,238,0.0)" />
            <stop offset="70%" stopColor="rgba(34,211,238,0.0)" />
            <stop offset="100%" stopColor="rgba(34,211,238,0.45)" />
          </radialGradient>
          <linearGradient id="radar-beam" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="rgba(103,232,249,0.55)" />
            <stop offset="100%" stopColor="rgba(103,232,249,0)" />
          </linearGradient>
        </defs>
        {rings.map((rr, i) => (
          <circle key={i} cx={c} cy={c} r={(size / 2 - 4) * rr} fill="none"
            stroke="rgba(34,211,238,0.22)" strokeWidth="1" />
        ))}
        <line x1={c} y1="4" x2={c} y2={size - 4} stroke="rgba(34,211,238,0.15)" strokeWidth="1" />
        <line x1="4" y1={c} x2={size - 4} y2={c} stroke="rgba(34,211,238,0.15)" strokeWidth="1" />
        <g className="radar-rotor" style={{ transformOrigin: `${c}px ${c}px` }}>
          <path d={`M ${c} ${c} L ${c} 4 A ${c - 4} ${c - 4} 0 0 1 ${c + (c - 4)} ${c} Z`}
            fill="url(#radar-sweep)" />
          <line x1={c} y1={c} x2={c} y2="4" stroke="url(#radar-beam)" strokeWidth="2" />
        </g>
        {blips.map((b, i) => (
          <circle key={i} cx={c + b.x * (c - 8)} cy={c + b.y * (c - 8)} r="2"
            fill="#ecfeff" className="radar-blip" style={{ animationDelay: `${i * 0.4}s` }} />
        ))}
      </svg>
    </div>
  );
}
