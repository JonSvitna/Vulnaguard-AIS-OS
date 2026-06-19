const navItems = document.querySelectorAll(".nav-item");
const views = document.querySelectorAll(".view");

function showView(name) {
  navItems.forEach((b) => b.classList.toggle("active", b.dataset.view === name));
  views.forEach((v) => v.classList.toggle("active", v.id === `${name}-view`));
  loaders[name] && loaders[name]();
}

navItems.forEach((btn) => {
  btn.addEventListener("click", () => showView(btn.dataset.view));
});

let memoryLoaded = false;

async function loadMemory() {
  if (memoryLoaded) return;
  memoryLoaded = true;
  const res = await fetch("/api/memory");
  const { entries } = await res.json();
  const listEl = document.getElementById("memory-list");
  listEl.innerHTML = "";
  entries.forEach((entry) => {
    const card = document.createElement("div");
    card.className = "memory-card";
    card.innerHTML = `
      <div class="name">${entry.name}</div>
      <div class="desc">${entry.description}</div>
      <span class="type-tag">${entry.type}</span>
    `;
    card.addEventListener("click", async () => {
      document.querySelectorAll(".memory-card").forEach((c) => c.classList.remove("active"));
      card.classList.add("active");
      const detailRes = await fetch(`/api/memory/${entry.slug}`);
      const { html } = await detailRes.json();
      document.getElementById("memory-detail").innerHTML = html;
    });
    listEl.appendChild(card);
  });
}

let decisionsLoaded = false;
async function loadDecisions() {
  if (decisionsLoaded) return;
  decisionsLoaded = true;
  const res = await fetch("/api/decisions");
  const { html } = await res.json();
  document.getElementById("decisions-body").innerHTML = html;
}

let connectionsLoaded = false;

function spawnStarfield() {
  const field = document.getElementById("hud-starfield");
  if (!field || field.childElementCount) return;
  const count = 90;
  for (let i = 0; i < count; i++) {
    const star = document.createElement("div");
    star.className = "star";
    const size = Math.random() * 2 + 0.5;
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.left = `${Math.random() * 100}%`;
    star.style.top = `${Math.random() * 100}%`;
    star.style.animationDelay = `${Math.random() * 4}s`;
    field.appendChild(star);
  }
}

function gaugeRing(gaugePercent) {
  const r = 22;
  const circumference = 2 * Math.PI * r;
  const filled = (gaugePercent / 100) * circumference;
  return `
    <svg class="hud-gauge" viewBox="0 0 52 52">
      <circle class="track" cx="26" cy="26" r="${r}" />
      <circle class="fill" cx="26" cy="26" r="${r}"
        stroke-dasharray="${filled.toFixed(1)} ${circumference.toFixed(1)}" />
    </svg>
  `;
}

async function loadConnections() {
  if (connectionsLoaded) return;
  connectionsLoaded = true;
  spawnStarfield();
  const res = await fetch("/api/connections/structured");
  const { systems, online, total } = await res.json();

  document.getElementById("hud-core-value").textContent = `${online} / ${total}`;

  const grid = document.getElementById("hud-grid");
  grid.innerHTML = systems
    .map((s) => {
      const readoutRight = s.status.daysSince !== undefined ? `checked ${s.status.daysSince}d ago` : s.lastChecked;
      return `
        <div class="hud-panel state-${s.status.state}">
          <div class="hud-panel-top">
            ${gaugeRing(s.status.gauge)}
            <div class="hud-panel-titles">
              <div class="hud-domain">${s.domain}</div>
              <span class="hud-status-badge">${s.status.label}</span>
            </div>
          </div>
          <div class="hud-tool">${s.tool}</div>
          <div class="hud-readout">
            <span>${s.mechanism}</span>
            <span>${readoutRight}</span>
          </div>
        </div>
      `;
    })
    .join("");
}

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
  memory: loadMemory,
  decisions: loadDecisions,
  connections: loadConnections,
  skills: loadSkills,
  context: loadContext,
};

loadMemory();
