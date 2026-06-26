const railItems = document.querySelectorAll(".rail-item");
const views = document.querySelectorAll(".view");

const TYPE_COLOR = {
  user: "#ffd166",
  feedback: "#ff8a3d",
  project: "#b06bff",
  reference: "#5be88a",
};
const TYPE_FALLBACK = "#7fa3ab";

let activeView = "overview";
const viewChangeListeners = [];

function showView(name) {
  activeView = name;
  railItems.forEach((b) => b.classList.toggle("active", b.dataset.view === name));
  views.forEach((v) => v.classList.toggle("active", v.id === `${name}-view`));
  loaders[name] && loaders[name]();
  viewChangeListeners.forEach((fn) => fn(name));
}

railItems.forEach((btn) => {
  btn.addEventListener("click", () => showView(btn.dataset.view));
});

// ---- Rotating nav dial ----
(function setupNavDial() {
  const dial = document.getElementById("nav-dial");
  const ring = document.getElementById("dial-ring");
  if (!dial || !ring) return;

  const dialViews = Array.from(railItems).map((b) => ({
    view: b.dataset.view,
    label: b.querySelector("span").textContent,
  }));
  const count = dialViews.length;
  const segmentAngle = 360 / count;
  const radius = 22;

  const nodes = dialViews.map((v, i) => {
    const node = document.createElement("div");
    node.className = "dial-node";
    node.dataset.view = v.view;
    node.title = v.label;
    const angle = i * segmentAngle - 90;
    const rad = (angle * Math.PI) / 180;
    node.style.left = `${25 + radius * Math.cos(rad)}px`;
    node.style.top = `${25 + radius * Math.sin(rad)}px`;
    node.addEventListener("click", (e) => {
      e.stopPropagation();
      showView(v.view);
    });
    ring.appendChild(node);
    return node;
  });

  function updateActiveDialNode() {
    nodes.forEach((n) => n.classList.toggle("active", n.dataset.view === activeView));
  }
  updateActiveDialNode();

  viewChangeListeners.push((name) => {
    updateActiveDialNode();
    const i = dialViews.findIndex((v) => v.view === name);
    if (i === -1) return;
    rotation = -i * segmentAngle;
    ring.style.transform = `rotate(${rotation}deg)`;
  });

  let rotation = 0;
  let dragging = false;
  let startAngle = 0;
  let startRotation = 0;

  function angleFromCenter(clientX, clientY) {
    const rect = dial.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    return (Math.atan2(clientY - cy, clientX - cx) * 180) / Math.PI;
  }

  dial.addEventListener("pointerdown", (e) => {
    dragging = true;
    dial.classList.add("dragging");
    ring.style.transition = "none";
    startAngle = angleFromCenter(e.clientX, e.clientY);
    startRotation = rotation;
    dial.setPointerCapture(e.pointerId);
  });

  dial.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    const current = angleFromCenter(e.clientX, e.clientY);
    rotation = startRotation + (current - startAngle);
    ring.style.transform = `rotate(${rotation}deg)`;
  });

  dial.addEventListener("pointerup", () => {
    if (!dragging) return;
    dragging = false;
    dial.classList.remove("dragging");
    ring.style.transition = "";

    // snap to the nearest segment and navigate to whichever view
    // ended up under the fixed top pointer.
    const snapped = Math.round(rotation / segmentAngle) * segmentAngle;
    rotation = snapped;
    ring.style.transform = `rotate(${rotation}deg)`;
    let index = Math.round(-rotation / segmentAngle) % count;
    if (index < 0) index += count;
    showView(dialViews[index].view);
    updateActiveDialNode();
  });
})();

// ---- Clock ----
function tickClock() {
  const el = document.getElementById("stat-time");
  if (el) el.textContent = new Date().toISOString().substr(11, 8) + " UTC";
}
tickClock();
setInterval(tickClock, 1000);

// ---- Decorative sparkline / waveform canvases ----
function animateLine(canvasId, color) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;
  const points = Array.from({ length: 40 }, () => h / 2);

  function step() {
    points.shift();
    const last = points[points.length - 1];
    const next = Math.max(2, Math.min(h - 2, last + (Math.random() - 0.5) * h * 0.4));
    points.push(next);

    ctx.clearRect(0, 0, w, h);
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.2;
    points.forEach((p, i) => {
      const x = (i / (points.length - 1)) * w;
      i === 0 ? ctx.moveTo(x, p) : ctx.lineTo(x, p);
    });
    ctx.stroke();
  }
  step();
  setInterval(step, 450);
}
animateLine("topbar-sparkline", "rgba(34, 211, 238, 0.8)");
animateLine("footer-waveform", "rgba(34, 211, 238, 0.6)");

setInterval(() => {
  const el = document.getElementById("status-latency");
  if (el) el.textContent = `${(6 + Math.random() * 4).toFixed(1)} ms`;
}, 2000);

// ---- Shared graph data cache ----
let graphDataCache = null;
async function getGraphData() {
  if (!graphDataCache) {
    graphDataCache = await fetch("/api/graph").then((r) => r.json());
  }
  return graphDataCache;
}

let knowledgeGraphCache = null;
async function getKnowledgeGraphData() {
  if (!knowledgeGraphCache) {
    knowledgeGraphCache = await fetch("/api/knowledge-graph").then((r) => r.json());
  }
  return knowledgeGraphCache;
}

function formatUptime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h}h ${m}m ${s}s`;
}

// ---- Overview ----
async function loadOverview() {
  const [overview, graph] = await Promise.all([
    fetch("/api/overview").then((r) => r.json()),
    getGraphData(),
  ]);

  document.getElementById("stat-nodes").textContent = overview.memoryNodes;
  document.getElementById("stat-links").textContent = graph.links.length;
  document.getElementById("stat-patterns").textContent = overview.activePatterns;
  document.getElementById("status-nodes-online").textContent = `${overview.connectionsOnline} / ${overview.connectionsTotal}`;
  document.getElementById("status-uptime").textContent = formatUptime(overview.uptimeSeconds);

  const grid = document.getElementById("overview-grid");
  grid.innerHTML = `
    <div class="overview-card"><div class="label">MEMORY NODES</div><div class="value">${overview.memoryNodes}</div><div class="sub">entries in long-term memory</div></div>
    <div class="overview-card"><div class="label">RELATIONSHIPS</div><div class="value">${graph.links.length}</div><div class="sub">linked memory pairs</div></div>
    <div class="overview-card"><div class="label">TOOLS ONLINE</div><div class="value">${overview.connectionsOnline}/${overview.connectionsTotal}</div><div class="sub">connected systems reporting healthy</div></div>
    <div class="overview-card"><div class="label">ACTIVE PATTERNS</div><div class="value">${overview.activePatterns}</div><div class="sub">skills + agents installed</div></div>
    <div class="overview-card"><div class="label">UPTIME</div><div class="value">${formatUptime(overview.uptimeSeconds)}</div><div class="sub">dashboard server session</div></div>
  `;

  loadHeroSphere();
}

// ---- Hero neural sphere (Overview) ----
const SOURCE_COLOR = {
  "aios-memory": "#22d3ee",
  "obsidian-vault": "#bdeeff",
};

let heroGraphInstance = null;
let heroGraphLoaded = false;
let heroRotateAngle = 0;
let heroUserInteracting = false;
let heroInteractionTimer = null;

async function loadHeroSphere() {
  if (heroGraphLoaded) return;
  heroGraphLoaded = true;

  const data = await getKnowledgeGraphData();
  const sub = document.getElementById("hero-sphere-sub");
  if (sub) {
    const memCount = data.nodes.filter((n) => n.source === "aios-memory").length;
    const wikiCount = data.nodes.filter((n) => n.source === "obsidian-vault").length;
    sub.textContent = `${memCount} MEMORY NODES · ${wikiCount} VAULT NODES`;
  }

  const degree = {};
  data.links.forEach((l) => {
    degree[l.source] = (degree[l.source] || 0) + 1;
    degree[l.target] = (degree[l.target] || 0) + 1;
  });

  const container = document.getElementById("hero-sphere-container");
  container.innerHTML = "";
  heroGraphInstance = ForceGraph3D()(container)
    .backgroundColor("rgba(0,0,0,0)")
    .graphData(data)
    .nodeId("id")
    .nodeLabel((n) => `${n.name} [${n.source === "obsidian-vault" ? "vault" : "memory"}]`)
    .nodeColor((n) => SOURCE_COLOR[n.source] || "#67e8f9")
    .nodeVal((n) => 1 + (degree[n.id] || 0) * 0.5)
    .nodeOpacity(0.95)
    .nodeResolution(12)
    .linkColor(() => "rgba(103, 232, 249, 0.55)")
    .linkWidth(0.9)
    .linkDirectionalParticles(4)
    .linkDirectionalParticleWidth(2.2)
    .linkDirectionalParticleColor(() => "#ecfeff")
    .linkDirectionalParticleSpeed(0.012)
    .showNavInfo(false)
    .width(container.clientWidth)
    .height(container.clientHeight);

  window.addEventListener("resize", () => {
    if (activeView === "overview" && heroGraphInstance) {
      heroGraphInstance.width(container.clientWidth).height(container.clientHeight);
    }
  });

  container.addEventListener("pointerdown", () => {
    heroUserInteracting = true;
    clearTimeout(heroInteractionTimer);
  });
  container.addEventListener("pointerup", () => {
    heroInteractionTimer = setTimeout(() => (heroUserInteracting = false), 3000);
  });

  (function autoRotateHero() {
    if (activeView === "overview" && heroGraphInstance && !heroUserInteracting) {
      heroRotateAngle += 0.0012;
      const distance = 260;
      heroGraphInstance.cameraPosition({
        x: distance * Math.sin(heroRotateAngle),
        z: distance * Math.cos(heroRotateAngle),
      });
    }
    requestAnimationFrame(autoRotateHero);
  })();
}

// ---- Memory graph (3D) ----
let graphInstance = null;
let graphLoaded = false;
let rotateAngle = 0;
let userInteracting = false;
let interactionTimer = null;

async function showNodeDetail(node) {
  const detail = document.getElementById("memory-detail");
  detail.innerHTML = `<p class="placeholder">Loading…</p>`;
  const isVault = node.source === "obsidian-vault";
  const url = isVault
    ? `/api/vault-note?path=${encodeURIComponent(node.path)}`
    : `/api/memory/${node.slug}`;
  const res = await fetch(url);
  if (!res.ok) {
    detail.innerHTML = `<p class="placeholder">No detail found for this node.</p>`;
    return;
  }
  const { html } = await res.json();
  const color = isVault ? SOURCE_COLOR["obsidian-vault"] : TYPE_COLOR[node.type] || TYPE_FALLBACK;
  detail.innerHTML = `
    <div class="node-tooltip" style="color:${color}">
      <div class="nt-name">${node.name}</div>
      <div class="nt-type">${isVault ? "obsidian vault" : "aios memory"} · ${node.type}</div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(34,211,238,0.15);margin:12px 0;">
    ${html}
  `;
}

function resizeGraph() {
  if (!graphInstance) return;
  const container = document.getElementById("graph-container");
  graphInstance.width(container.clientWidth).height(container.clientHeight);
}

async function loadMemoryGraph() {
  const data = await getKnowledgeGraphData();
  if (graphLoaded) return;
  graphLoaded = true;

  const degree = {};
  data.links.forEach((l) => {
    degree[l.source] = (degree[l.source] || 0) + 1;
    degree[l.target] = (degree[l.target] || 0) + 1;
  });

  const container = document.getElementById("graph-container");
  graphInstance = ForceGraph3D()(container)
    .backgroundColor("rgba(0,0,0,0)")
    .graphData(data)
    .nodeId("id")
    .nodeLabel((n) => `${n.name} [${n.source === "obsidian-vault" ? "vault" : n.type}]`)
    .nodeColor((n) => (n.source === "obsidian-vault" ? SOURCE_COLOR["obsidian-vault"] : TYPE_COLOR[n.type] || TYPE_FALLBACK))
    .nodeVal((n) => 1.4 + (degree[n.id] || 0) * 0.6)
    .nodeOpacity(0.92)
    .linkColor(() => "rgba(103, 232, 249, 0.55)")
    .linkWidth(0.8)
    .linkDirectionalParticles(4)
    .linkDirectionalParticleWidth(2)
    .linkDirectionalParticleColor(() => "#ecfeff")
    .linkDirectionalParticleSpeed(0.01)
    .onNodeClick((node) => showNodeDetail(node))
    .showNavInfo(false);

  resizeGraph();
  window.addEventListener("resize", () => {
    if (activeView === "memory") resizeGraph();
  });

  container.addEventListener("pointerdown", () => {
    userInteracting = true;
    clearTimeout(interactionTimer);
  });
  container.addEventListener("pointerup", () => {
    interactionTimer = setTimeout(() => (userInteracting = false), 2500);
  });

  (function autoRotate() {
    if (activeView === "memory" && graphInstance && !userInteracting) {
      rotateAngle += 0.0018;
      const distance = 320;
      graphInstance.cameraPosition({
        x: distance * Math.sin(rotateAngle),
        z: distance * Math.cos(rotateAngle),
      });
    }
    requestAnimationFrame(autoRotate);
  })();
}

// ---- Decisions ----
let decisionsLoaded = false;
async function loadDecisions() {
  if (decisionsLoaded) return;
  decisionsLoaded = true;
  const res = await fetch("/api/decisions");
  const { html } = await res.json();
  document.getElementById("decisions-body").innerHTML = html;
}

// ---- Ecosystem orbit ----
let ecosystemData = null;
async function loadEcosystem() {
  if (!ecosystemData) {
    const [connRes, skillsRes] = await Promise.all([
      fetch("/api/connections/structured").then((r) => r.json()),
      fetch("/api/skills").then((r) => r.json()),
    ]);
    const nodes = connRes.systems.map((s) => ({
      label: s.domain,
      sub: s.status.label,
      state: s.status.state,
      icon: "◆",
      url: s.url,
    }));
    nodes.push({ label: "SKILLS", sub: `${skillsRes.skills.length} INSTALLED`, state: "online", icon: "✺" });
    nodes.push({ label: "AGENTS", sub: `${skillsRes.agents.length} INSTALLED`, state: "online", icon: "◈" });
    ecosystemData = nodes;
  }
  renderOrbit(ecosystemData);
}

function renderOrbit(nodes) {
  const wrap = document.getElementById("orbit-wrap");
  wrap.innerHTML = "";
  const rect = wrap.getBoundingClientRect();
  const cx = rect.width / 2;
  const cy = rect.height / 2;
  const radius = Math.max(140, Math.min(rect.width, rect.height) / 2 - 100);

  const svgNS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("class", "orbit-rings");
  svg.setAttribute("width", radius * 2 + 40);
  svg.setAttribute("height", radius * 2 + 40);
  [0.45, 0.72, 1].forEach((f) => {
    const c = document.createElementNS(svgNS, "circle");
    c.setAttribute("cx", radius + 20);
    c.setAttribute("cy", radius + 20);
    c.setAttribute("r", radius * f);
    svg.appendChild(c);
  });
  wrap.appendChild(svg);

  const core = document.createElement("div");
  core.className = "orbit-core";
  core.innerHTML = `<div class="core-title">NEXUS OS</div><div class="core-sub">CORE</div>`;
  wrap.appendChild(core);

  nodes.forEach((n, i) => {
    const angle = (i / nodes.length) * Math.PI * 2 - Math.PI / 2;
    const x = cx + radius * Math.cos(angle);
    const y = cy + radius * Math.sin(angle);
    const len = Math.hypot(x - cx, y - cy);
    const ang = (Math.atan2(y - cy, x - cx) * 180) / Math.PI;

    const tether = document.createElement("div");
    tether.className = "orbit-tether";
    tether.style.width = `${len}px`;
    tether.style.transform = `rotate(${ang}deg)`;
    wrap.appendChild(tether);

    const node = document.createElement("div");
    node.className = `orbit-node state-${n.state}${n.url ? " linkable" : ""}`;
    node.style.left = `${x}px`;
    node.style.top = `${y}px`;
    node.innerHTML = `<div class="node-hex">${n.icon}</div><div class="node-label">${n.label}</div><div class="node-sub">${n.sub}</div>`;
    if (n.url) {
      node.title = `Open ${n.label}`;
      node.addEventListener("click", () => window.open(n.url, "_blank", "noopener"));
    }
    wrap.appendChild(node);
  });
}

window.addEventListener("resize", () => {
  if (activeView === "ecosystem" && ecosystemData) renderOrbit(ecosystemData);
});

// ---- Skills & Agents ----
let skillsLoaded = false;
async function loadSkills() {
  if (skillsLoaded) return;
  skillsLoaded = true;
  const res = await fetch("/api/skills");
  const { skills, agents } = await res.json();
  const el = document.getElementById("skills-body");

  const skillCards = skills
    .map((s) => `<div class="card"><div class="name">/${s.name}</div><div class="desc">${s.description}</div></div>`)
    .join("");
  const agentCards = agents
    .map((a) => `<div class="card"><div class="name">${a.name}</div><div class="desc">${a.description}</div></div>`)
    .join("");

  el.innerHTML = `
    <div class="section-title">Skills (${skills.length})</div>
    <div class="card-grid">${skillCards}</div>
    <div class="section-title">Agents (${agents.length})</div>
    <div class="card-grid">${agentCards || '<p class="placeholder">None defined.</p>'}</div>
  `;
}

// ---- Context ----
let contextLoaded = false;
async function loadContext() {
  if (contextLoaded) return;
  contextLoaded = true;
  const res = await fetch("/api/context");
  const { sections } = await res.json();
  const el = document.getElementById("context-body");
  el.innerHTML = sections
    .map((s) => `<div class="context-section markdown">${s.html}</div>`)
    .join("");
}

const loaders = {
  overview: loadOverview,
  memory: loadMemoryGraph,
  decisions: loadDecisions,
  ecosystem: loadEcosystem,
  skills: loadSkills,
  context: loadContext,
};

loadOverview();
