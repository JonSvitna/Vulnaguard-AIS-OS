import React, { useEffect, useRef } from "react";

const GROUP_COLORS = {
  "aios-memory": "#22d3ee",
  "obsidian-vault": "#67e8f9",
  default: "#9fb4c2",
};

// 2D node-link canvas. Renders the real knowledge graph when `nodes`/`edges`
// are supplied; otherwise falls back to a decorative graph of `fallbackCount`
// nodes so the panel is never blank. Respects prefers-reduced-motion.
export default function NetworkCanvas({ nodes, edges, fallbackCount = 34 }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;
    const ctx = canvas.getContext("2d");
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let W = 0;
    let H = 0;
    let sim = [];
    let links = [];
    let raf = 0;

    const hasReal = Array.isArray(nodes) && nodes.length > 0;

    function seed() {
      if (hasReal) {
        const idx = new Map();
        // Cap nodes so a very large vault stays legible and fast.
        const capped = nodes.slice(0, 180);
        capped.forEach((n, i) => idx.set(n.id, i));
        sim = capped.map((n) => {
          const color = GROUP_COLORS[n.source] || GROUP_COLORS.default;
          const px = typeof n.x === "number" ? (n.x + 1) / 2 : Math.random();
          const py = typeof n.y === "number" ? (n.y + 1) / 2 : Math.random();
          return {
            x: 8 + px * (W - 16),
            y: 8 + py * (H - 16),
            vx: (Math.random() - 0.5) * 0.16,
            vy: (Math.random() - 0.5) * 0.16,
            r: 2.6,
            color,
            pulse: Math.random() * 6.28,
          };
        });
        links = (edges || [])
          .map((e) => [idx.get(e.source), idx.get(e.target)])
          .filter(([a, b]) => a !== undefined && b !== undefined);
      } else {
        const N = fallbackCount;
        const palette = ["#22d3ee", "#67e8f9", "#9fb4c2"];
        sim = Array.from({ length: N }, (_, i) => {
          const g = i < N * 0.42 ? 0 : i < N * 0.74 ? 1 : 2;
          return {
            x: Math.random() * W,
            y: Math.random() * H,
            vx: (Math.random() - 0.5) * 0.16,
            vy: (Math.random() - 0.5) * 0.16,
            r: g === 0 ? 3.2 : 2.2,
            color: palette[g],
            pulse: Math.random() * 6.28,
          };
        });
        links = [];
        for (let i = 0; i < N; i += 1) {
          const k = 1 + ((Math.random() * 2) | 0);
          for (let m = 0; m < k; m += 1) {
            const j = (Math.random() * N) | 0;
            if (j !== i) links.push([i, j]);
          }
        }
      }
    }

    function resize() {
      const rect = canvas.getBoundingClientRect();
      if (!rect.width) return;
      W = rect.width;
      H = rect.height;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function frame() {
      ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = 1;
      for (let e = 0; e < links.length; e += 1) {
        const a = sim[links[e][0]];
        const b = sim[links[e][1]];
        if (!a || !b) continue;
        const dist = Math.hypot(a.x - b.x, a.y - b.y);
        const alpha = Math.max(0, 0.24 - dist / 1500);
        if (alpha <= 0) continue;
        ctx.strokeStyle = `rgba(34,211,238,${alpha})`;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
      for (let i = 0; i < sim.length; i += 1) {
        const n = sim[i];
        if (!reduce) {
          n.x += n.vx;
          n.y += n.vy;
          n.pulse += 0.03;
          if (n.x < 6 || n.x > W - 6) n.vx *= -1;
          if (n.y < 6 || n.y > H - 6) n.vy *= -1;
        }
        const glow = 0.5 + 0.5 * Math.sin(n.pulse);
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r + 3 * glow, 0, 7);
        ctx.fillStyle = `${n.color}22`;
        ctx.fill();
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, 7);
        ctx.fillStyle = n.color;
        ctx.fill();
      }
      if (!reduce) raf = requestAnimationFrame(frame);
    }

    resize();
    seed();
    frame();

    const ro = new ResizeObserver(() => {
      resize();
      seed();
      if (reduce) frame();
    });
    ro.observe(canvas);

    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
    };
  }, [nodes, edges, fallbackCount]);

  return <canvas ref={canvasRef} />;
}
