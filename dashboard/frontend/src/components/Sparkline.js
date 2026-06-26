import React from "react";

// Minimal glowing line chart for telemetry readouts.
export default function Sparkline({ data = [], width = 200, height = 56 }) {
  if (!data.length) return <svg width={width} height={height} />;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const step = width / (data.length - 1);
  const pts = data.map((v, i) => [i * step, height - ((v - min) / range) * (height - 8) - 4]);
  const d = pts.map((p, i) => `${i === 0 ? "M" : "L"} ${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" ");
  const area = `${d} L ${width} ${height} L 0 ${height} Z`;

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="sparkline">
      <defs>
        <linearGradient id="sl-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="rgba(34,211,238,0.35)" />
          <stop offset="100%" stopColor="rgba(34,211,238,0)" />
        </linearGradient>
      </defs>
      <path d={area} fill="url(#sl-fill)" />
      <path d={d} fill="none" stroke="#67e8f9" strokeWidth="1.5"
        style={{ filter: "drop-shadow(0 0 3px rgba(34,211,238,0.9))" }} />
      <circle cx={pts[pts.length - 1][0]} cy={pts[pts.length - 1][1]} r="2.5" fill="#ecfeff" />
    </svg>
  );
}
