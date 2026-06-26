import React from "react";
import { AnimatePresence, motion } from "framer-motion";

// Glass overlay that reveals detail when a data point / panel is selected.
export default function DetailOverlay({ detail, onClose }) {
  return (
    <AnimatePresence>
      {detail && (
        <motion.div
          className="detail-backdrop"
          data-testid="detail-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <motion.div
            className="detail-panel glass-panel"
            initial={{ scale: 0.92, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.95, opacity: 0 }}
            transition={{ duration: 0.4, ease: [0.2, 0.8, 0.2, 1] }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="glass-inner">
              <div className="panel-head">
                <span className="panel-title">{detail.title}</span>
                <button className="detail-close" aria-label="Close detail" onClick={onClose} data-testid="detail-close">✕</button>
              </div>
              <div className="panel-body detail-body">
                {detail.code && <div className="detail-code font-display">{detail.code}</div>}
                {detail.rows?.map((r, i) => (
                  <div className="detail-row" key={i}>
                    <span className="dr-label">{r.label}</span>
                    <span className="dr-value">{r.value}</span>
                  </div>
                ))}
                {detail.note && <p className="detail-note">{detail.note}</p>}
              </div>
            </div>
            <span className="corner tl" /><span className="corner tr" />
            <span className="corner bl" /><span className="corner br" />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
