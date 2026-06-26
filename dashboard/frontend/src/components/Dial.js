import React, { useCallback, useEffect, useRef, useState } from "react";
import { SECTIONS } from "../data/sections";

const SEG = 360 / SECTIONS.length;
const TAU = Math.PI * 2;

// Foreground holographic dial. Drag to rotate; nearest segment to the top
// indicator becomes the active section. Concentric rings spin at idle.
export default function Dial({ activeIndex, onNavigate }) {
  const [rotation, setRotation] = useState(-activeIndex * SEG);
  const dragging = useRef(false);
  const lastAngle = useRef(0);
  const moved = useRef(false);
  const downSeg = useRef(null);
  const ref = useRef(null);

  // sync when navigation comes from outside (and not mid-drag)
  useEffect(() => {
    if (!dragging.current) {
      setRotation((prev) => {
        const target = -activeIndex * SEG;
        // choose closest equivalent angle for smooth motion
        let diff = ((target - prev) % 360 + 540) % 360 - 180;
        return prev + diff;
      });
    }
  }, [activeIndex]);

  const pointerAngle = useCallback((e) => {
    const rect = ref.current.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    return (Math.atan2(e.clientY - cy, e.clientX - cx) * 180) / Math.PI;
  }, []);

  const onDown = (e) => {
    dragging.current = true;
    moved.current = false;
    lastAngle.current = pointerAngle(e);
    // record which sector the press started on (deterministic tap navigation)
    const seg = e.target?.closest?.('[data-testid^="dial-segment-"]');
    downSeg.current = seg ? seg.getAttribute("data-testid").replace("dial-segment-", "") : null;
    e.currentTarget.setPointerCapture?.(e.pointerId);
  };

  const onMove = (e) => {
    if (!dragging.current) return;
    const a = pointerAngle(e);
    let d = a - lastAngle.current;
    if (d > 180) d -= 360;
    if (d < -180) d += 360;
    if (Math.abs(d) > 0.5) moved.current = true;
    lastAngle.current = a;
    setRotation((r) => r + d);
  };

  const settle = () => {
    if (!dragging.current) return;
    dragging.current = false;

    // A tap (no drag): navigate to the sector the press started on. Fall back
    // to angle math only if the press did not begin on a specific sector.
    if (!moved.current) {
      if (downSeg.current) {
        const i = SECTIONS.findIndex((s) => s.id === downSeg.current);
        if (i >= 0) { onNavigate?.(i); return; }
      }
      const a = lastAngle.current; // screen angle in degrees (0 = +x, -90 = top)
      let best = 0, bestD = 999;
      for (let i = 0; i < SECTIONS.length; i++) {
        const target = i * SEG - 90 + rotation;
        const d = Math.abs(((a - target) % 360 + 540) % 360 - 180);
        if (d < bestD) { bestD = d; best = i; }
      }
      onNavigate?.(best);
      return;
    }

    // A drag: snap rotation so the nearest sector locks to the top indicator.
    setRotation((r) => {
      const snapped = Math.round(r / SEG) * SEG;
      const idx = ((Math.round(-snapped / SEG) % SECTIONS.length) + SECTIONS.length) % SECTIONS.length;
      onNavigate?.(idx);
      return snapped;
    });
  };

  const ticks = Array.from({ length: 60 });

  return (
    <div className="dial-wrap" data-testid="nav-dial" ref={ref}
      onPointerDown={onDown} onPointerMove={onMove} onPointerUp={settle} onPointerLeave={settle}>
      <div className="dial-pointer" />
      {/* idle counter-rotating decorative ring */}
      <svg className="dial-svg ring-outer" viewBox="0 0 400 400">
        <circle cx="200" cy="200" r="196" fill="none" stroke="rgba(34,211,238,0.18)" strokeWidth="1" />
        {ticks.map((_, i) => {
          const a = (i / 60) * TAU;
          const big = i % 5 === 0;
          const r1 = 196, r2 = big ? 184 : 190;
          return (
            <line key={i}
              x1={200 + Math.cos(a) * r1} y1={200 + Math.sin(a) * r1}
              x2={200 + Math.cos(a) * r2} y2={200 + Math.sin(a) * r2}
              stroke={big ? "rgba(103,232,249,0.55)" : "rgba(34,211,238,0.3)"} strokeWidth="1" />
          );
        })}
      </svg>

      <svg className="dial-svg ring-mid" viewBox="0 0 400 400">
        <circle cx="200" cy="200" r="150" fill="none" stroke="rgba(34,211,238,0.25)" strokeWidth="1" strokeDasharray="3 6" />
        <circle cx="200" cy="200" r="132" fill="none" stroke="rgba(34,211,238,0.15)" strokeWidth="1" />
      </svg>

      {/* main rotating segment ring (driven by drag) */}
      <svg className="dial-svg" viewBox="0 0 400 400"
        style={{ transform: `rotate(${rotation}deg)`, transition: dragging.current ? "none" : "transform .6s cubic-bezier(.2,.8,.2,1)" }}>
        {SECTIONS.map((s, i) => {
          const start = (i * SEG - 90 - SEG / 2) * (Math.PI / 180);
          const end = (i * SEG - 90 + SEG / 2) * (Math.PI / 180);
          const ro = 168, ri = 150;
          const x1 = 200 + Math.cos(start) * ri, y1 = 200 + Math.sin(start) * ri;
          const x2 = 200 + Math.cos(start) * ro, y2 = 200 + Math.sin(start) * ro;
          const x3 = 200 + Math.cos(end) * ro, y3 = 200 + Math.sin(end) * ro;
          const x4 = 200 + Math.cos(end) * ri, y4 = 200 + Math.sin(end) * ri;
          // wider invisible hit-area wedge so clicking anywhere in the sector works
          const hi = 88, ho = 196;
          const hx1 = 200 + Math.cos(start) * hi, hy1 = 200 + Math.sin(start) * hi;
          const hx2 = 200 + Math.cos(start) * ho, hy2 = 200 + Math.sin(start) * ho;
          const hx3 = 200 + Math.cos(end) * ho, hy3 = 200 + Math.sin(end) * ho;
          const hx4 = 200 + Math.cos(end) * hi, hy4 = 200 + Math.sin(end) * hi;
          const active = i === activeIndex;
          const labelA = (i * SEG - 90) * (Math.PI / 180);
          const lx = 200 + Math.cos(labelA) * 159;
          const ly = 200 + Math.sin(labelA) * 159;
          return (
            <g key={s.id} style={{ cursor: "pointer" }}
              data-testid={`dial-segment-${s.id}`}>
              <path d={`M ${hx1} ${hy1} L ${hx2} ${hy2} A ${ho} ${ho} 0 0 1 ${hx3} ${hy3} L ${hx4} ${hy4} A ${hi} ${hi} 0 0 0 ${hx1} ${hy1} Z`}
                fill="rgba(0,0,0,0.001)" style={{ pointerEvents: "all" }} />
              <path d={`M ${x1} ${y1} L ${x2} ${y2} A ${ro} ${ro} 0 0 1 ${x3} ${y3} L ${x4} ${y4} A ${ri} ${ri} 0 0 0 ${x1} ${y1} Z`}
                fill={active ? "rgba(34,211,238,0.28)" : "rgba(34,211,238,0.06)"}
                stroke={active ? "#67e8f9" : "rgba(34,211,238,0.3)"} strokeWidth={active ? 1.5 : 1}
                style={{ filter: active ? "drop-shadow(0 0 6px rgba(34,211,238,0.8))" : "none", transition: "all .4s" }} />
              <text x={lx} y={ly} textAnchor="middle" dominantBaseline="middle"
                transform={`rotate(${-rotation} ${lx} ${ly})`}
                fill={active ? "#ecfeff" : "rgba(103,232,249,0.7)"} fontSize="10"
                style={{ letterSpacing: "1px", fontWeight: active ? 700 : 400 }}>
                {s.label}
              </text>
            </g>
          );
        })}
      </svg>

      {/* core hub */}
      <div className="dial-core">
        <div className="dial-core-glow" />
        <span className="dial-core-code font-display">{SECTIONS[activeIndex].code}</span>
        <span className="dial-core-label">{SECTIONS[activeIndex].label}</span>
        <span className="dial-core-hint">DRAG TO NAVIGATE</span>
      </div>
    </div>
  );
}
