import React from "react";
import { motion } from "framer-motion";

// Floating glass HUD panel. `depth` drives parallax offset multiplier.
export default function GlassPanel({
  title, code, children, className = "", style = {}, pointer = { x: 0, y: 0 },
  depth = 1, delay = 0, onClick, testid, floatPhase = 0,
}) {
  const px = -pointer.x * 14 * depth;
  const py = -pointer.y * 14 * depth;

  return (
    <motion.div
      data-testid={testid}
      className={`glass-panel ${className}`}
      onClick={onClick}
      initial={{ opacity: 0, y: 18, filter: "blur(6px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      transition={{ duration: 0.9, delay, ease: [0.2, 0.8, 0.2, 1] }}
      style={{
        ...style,
        transform: `translate3d(${px}px, ${py}px, 0)`,
        "--float-delay": `${floatPhase}s`,
      }}
    >
      <div className="glass-inner">
        {(title || code) && (
          <div className="panel-head">
            <span className="panel-title">{title}</span>
            {code && <span className="panel-code">{code}</span>}
          </div>
        )}
        <div className="panel-body">{children}</div>
      </div>
      <span className="corner tl" />
      <span className="corner tr" />
      <span className="corner bl" />
      <span className="corner br" />
    </motion.div>
  );
}
