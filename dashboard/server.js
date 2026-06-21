const path = require("path");
const fs = require("fs");
const express = require("express");
const matter = require("gray-matter");
const { marked } = require("marked");

const REPO_ROOT = path.join(__dirname, "..");
const MEMORY_DIR = path.join(
  process.env.HOME || "",
  ".claude/projects/-Users-seanm-Documents-GitHub-Vulnaguard-AIS-OS/memory",
);
const MEMORY_INDEX = path.join(path.dirname(MEMORY_DIR), "MEMORY.md");

const app = express();
const PORT = process.env.PORT || 4400;
const SERVER_START = Date.now();

app.use(express.static(path.join(__dirname, "public")));

function readSafe(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return null;
  }
}

function listMdFiles(dir) {
  try {
    return fs
      .readdirSync(dir)
      .filter((f) => f.endsWith(".md"))
      .map((f) => path.join(dir, f));
  } catch {
    return [];
  }
}

// --- Memory ---
app.get("/api/memory", (req, res) => {
  const files = listMdFiles(MEMORY_DIR);
  const entries = files.map((filePath) => {
    const raw = readSafe(filePath);
    const { data } = matter(raw || "");
    return {
      slug: path.basename(filePath, ".md"),
      name: data.name || path.basename(filePath, ".md"),
      description: data.description || "",
      type: (data.metadata && data.metadata.type) || data.type || "unknown",
    };
  });
  const indexRaw = readSafe(MEMORY_INDEX) || "";
  res.json({ entries, indexHtml: marked.parse(indexRaw) });
});

app.get("/api/memory/:slug", (req, res) => {
  const filePath = path.join(MEMORY_DIR, `${req.params.slug}.md`);
  const raw = readSafe(filePath);
  if (!raw) return res.status(404).json({ error: "not found" });
  const { data, content } = matter(raw);
  res.json({ frontmatter: data, html: marked.parse(content) });
});

// --- Memory graph (nodes + [[wikilink]] edges) ---
app.get("/api/graph", (req, res) => {
  const files = listMdFiles(MEMORY_DIR).filter((f) => path.basename(f) !== "MEMORY.md");
  const nodes = [];
  const linkSlugs = new Map();

  files.forEach((filePath) => {
    const raw = readSafe(filePath);
    if (!raw) return;
    const { data, content } = matter(raw);
    const fileSlug = path.basename(filePath, ".md");
    const id = data.name || fileSlug;
    nodes.push({
      id,
      slug: fileSlug,
      name: data.name || fileSlug,
      description: data.description || "",
      type: (data.metadata && data.metadata.type) || data.type || "unknown",
    });
    const targets = new Set();
    const re = /\[\[([^\]|]+)\]\]/g;
    let m;
    while ((m = re.exec(content))) targets.add(m[1].trim());
    linkSlugs.set(id, targets);
  });

  const nodeIds = new Set(nodes.map((n) => n.id));
  const seen = new Set();
  const links = [];
  linkSlugs.forEach((targets, source) => {
    targets.forEach((target) => {
      if (!nodeIds.has(target) || target === source) return;
      const key = [source, target].sort().join("::");
      if (seen.has(key)) return;
      seen.add(key);
      links.push({ source, target });
    });
  });

  res.json({ nodes, links });
});

// --- Overview (live aggregate stats) ---
app.get("/api/overview", (req, res) => {
  const memoryFiles = listMdFiles(MEMORY_DIR);
  const connectionsRaw = readSafe(path.join(REPO_ROOT, "connections.md")) || "";
  const connRows = parseConnectionsTable(connectionsRaw);
  const connStatuses = connRows.map(computeStatus);
  const onlineCount = connStatuses.filter((s) => s.state === "online").length;

  const skillsDir = path.join(REPO_ROOT, ".claude/skills");
  const agentsDir = path.join(REPO_ROOT, ".claude/agents");
  let skillCount = 0;
  let agentCount = 0;
  try {
    skillCount = fs.readdirSync(skillsDir).filter((n) => fs.statSync(path.join(skillsDir, n)).isDirectory()).length;
  } catch {}
  try {
    agentCount = fs.readdirSync(agentsDir).filter((f) => f.endsWith(".md")).length;
  } catch {}

  res.json({
    memoryNodes: memoryFiles.length,
    connectionsOnline: onlineCount,
    connectionsTotal: connRows.length,
    activePatterns: skillCount + agentCount,
    uptimeSeconds: Math.floor((Date.now() - SERVER_START) / 1000),
  });
});

// --- Decisions ---
app.get("/api/decisions", (req, res) => {
  const raw = readSafe(path.join(REPO_ROOT, "decisions/log.md")) || "";
  res.json({ html: marked.parse(raw) });
});

// --- Connections ---
app.get("/api/connections", (req, res) => {
  const raw = readSafe(path.join(REPO_ROOT, "connections.md")) || "";
  res.json({ html: marked.parse(raw) });
});

function parseConnectionsTable(raw) {
  const lines = raw.split("\n").filter((l) => l.trim().startsWith("|"));
  // drop header row + separator row
  const dataLines = lines.slice(2);
  return dataLines
    .map((line) => {
      const cells = line
        .split("|")
        .slice(1, -1)
        .map((c) => c.trim());
      if (cells.length < 6) return null;
      const [num, domain, tool, mechanism, auth, lastChecked] = cells;
      return { num, domain, tool, mechanism, auth, lastChecked };
    })
    .filter(Boolean);
}

function computeStatus(row) {
  const mechanism = (row.mechanism || "").toLowerCase();
  const lastChecked = row.lastChecked;
  if (mechanism.includes("not yet connected")) {
    return { state: "offline", gauge: 0, label: "OFFLINE" };
  }
  if (!lastChecked || lastChecked === "—" || lastChecked === "-") {
    return { state: "unverified", gauge: 55, label: "UNVERIFIED" };
  }
  const checkedDate = new Date(lastChecked);
  if (isNaN(checkedDate.getTime())) {
    return { state: "unverified", gauge: 55, label: "UNVERIFIED" };
  }
  const daysSince = Math.floor((Date.now() - checkedDate.getTime()) / 86400000);
  if (daysSince <= 14) {
    return { state: "online", gauge: 100, label: "ONLINE", daysSince };
  }
  return { state: "stale", gauge: 70, label: "STALE", daysSince };
}

app.get("/api/connections/structured", (req, res) => {
  const raw = readSafe(path.join(REPO_ROOT, "connections.md")) || "";
  const rows = parseConnectionsTable(raw);
  const systems = rows.map((row) => ({
    ...row,
    status: computeStatus(row),
  }));
  const online = systems.filter((s) => s.status.state === "online").length;
  res.json({ systems, online, total: systems.length });
});

// --- Skills & Agents ---
app.get("/api/skills", (req, res) => {
  const skillsDir = path.join(REPO_ROOT, ".claude/skills");
  const agentsDir = path.join(REPO_ROOT, ".claude/agents");

  let skills = [];
  try {
    skills = fs
      .readdirSync(skillsDir)
      .filter((name) => fs.statSync(path.join(skillsDir, name)).isDirectory())
      .map((name) => {
        const raw = readSafe(path.join(skillsDir, name, "SKILL.md"));
        const { data } = matter(raw || "");
        return {
          name: data.name || name,
          description: data.description || "",
        };
      });
  } catch {
    skills = [];
  }

  let agents = [];
  try {
    agents = fs
      .readdirSync(agentsDir)
      .filter((f) => f.endsWith(".md"))
      .map((f) => {
        const raw = readSafe(path.join(agentsDir, f));
        const { data } = matter(raw || "");
        return {
          name: data.name || path.basename(f, ".md"),
          description: data.description || "",
        };
      });
  } catch {
    agents = [];
  }

  res.json({ skills, agents });
});

// --- Context ---
app.get("/api/context", (req, res) => {
  const files = ["about-me.md", "about-business.md", "priorities.md"];
  const sections = files.map((f) => {
    const raw = readSafe(path.join(REPO_ROOT, "context", f)) || "";
    return { slug: f.replace(".md", ""), html: marked.parse(raw) };
  });
  res.json({ sections });
});

app.listen(PORT, () => {
  console.log(`AIOS dashboard running at http://localhost:${PORT}`);
});
