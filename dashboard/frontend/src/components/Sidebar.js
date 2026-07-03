import React from "react";

const ICONS = {
  overview: (
    <svg className="ico" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></svg>
  ),
  network: (
    <svg className="ico" viewBox="0 0 24 24"><circle cx="6" cy="6" r="2.4" /><circle cx="18" cy="7" r="2.4" /><circle cx="12" cy="17" r="2.4" /><path d="M8 7l8 0M7 8l4 7M16 9l-3 6" /></svg>
  ),
  memory: (
    <svg className="ico" viewBox="0 0 24 24"><ellipse cx="12" cy="6" rx="7" ry="3" /><path d="M5 6v6c0 1.6 3.1 3 7 3s7-1.4 7-3V6M5 12v6c0 1.6 3.1 3 7 3s7-1.4 7-3v-6" /></svg>
  ),
  systems: (
    <svg className="ico" viewBox="0 0 24 24"><path d="M13 2L4 14h6l-1 8 9-12h-6z" /></svg>
  ),
  comms: (
    <svg className="ico" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg>
  ),
};

function NavItem({ id, label, tag, active, onClick }) {
  return (
    <button type="button" className={`nav-item${active ? " active" : ""}`} onClick={() => onClick(id)} aria-current={active ? "page" : undefined}>
      {ICONS[id]}
      {label}
      {tag != null ? <span className="tag">{tag}</span> : null}
    </button>
  );
}

// `health` = { online, warn, idle, total } drives the connection strip.
export default function Sidebar({ sections, active, onNavigate, counts = {}, health }) {
  const cells = [];
  const total = health?.total ?? 0;
  const online = health?.online ?? 0;
  const warn = health?.warn ?? 0;
  for (let i = 0; i < Math.max(total, 6); i += 1) {
    let cls = "m";
    if (i < online) cls = "";
    else if (i < online + warn) cls = "w";
    cells.push(<i key={i} className={cls} />);
  }

  return (
    <aside className="rail">
      <div className="brand">
        <span className="dot" />
        <span className="name display"><b>Sentinel</b> <span>OS</span></span>
      </div>

      <nav>
        <div className="nav-label">Workspace</div>
        {sections.map((s) => (
          <NavItem key={s.id} id={s.id} label={s.label} tag={counts[s.id]} active={active === s.id} onClick={onNavigate} />
        ))}
      </nav>

      <div className="health">
        <div className="eyebrow">Connections</div>
        <div className="health-grid">{cells}</div>
        <div className="meta">
          <b>{online} healthy</b>{warn ? ` · ${warn} warn` : ""}{health?.idle ? ` · ${health.idle} idle` : ""}
        </div>
      </div>
    </aside>
  );
}
