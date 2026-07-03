import React from "react";

// Tiny inline sparkline. `data` is an array of numbers; `color` sets the stroke.
export default function Sparkline({ data, color = "#22d3ee", w = 78, h = 26 }) {
  const pts = Array.isArray(data) && data.length ? data : [1, 1, 1, 1, 1, 1, 1];
  const min = Math.min(...pts);
  const max = Math.max(...pts);
  const span = max - min || 1;
  const step = w / (pts.length - 1 || 1);
  const coords = pts.map((v, i) => {
    const x = i * step;
    const y = h - 3 - ((v - min) / span) * (h - 6);
    return [x, y];
  });
  const line = coords.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" ");
  const [ex, ey] = coords[coords.length - 1];
  return (
    <svg className="spark" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" aria-hidden="true">
      <polyline fill="none" stroke={color} strokeWidth="1.5" points={line} />
      <circle cx={ex} cy={ey} r="2" fill="#67e8f9" />
    </svg>
  );
}
