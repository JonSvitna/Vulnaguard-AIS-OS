import React from "react";
import Sparkline from "./Sparkline";

// A single KPI tile: eyebrow label, big number (with optional cyan accent +
// suffix), a delta line, and an optional sparkline.
export default function StatTile({ label, value, suffix, accent, delta, deltaTone = "flat", series, span = "span-3", numColor }) {
  return (
    <div className={`block stat ${span}`}>
      <div className="eyebrow">{label}</div>
      <div className="num" style={numColor ? { color: numColor } : undefined}>
        {accent ? <span className="c">{value}</span> : value}
        {suffix ? <small>{suffix}</small> : null}
      </div>
      <div className="stat-foot">
        <span className={`delta ${deltaTone}`}>{delta}</span>
        {series ? <Sparkline data={series} color={deltaTone === "flat" ? "#5b7180" : "#22d3ee"} /> : null}
      </div>
    </div>
  );
}
