import React from "react";

// Status pill. `tone` is one of ok | warn | crit | idle | cyan.
export default function Pill({ tone = "idle", children, style }) {
  return (
    <span className={`pill ${tone}`} style={style}>
      <i />
      {children}
    </span>
  );
}
