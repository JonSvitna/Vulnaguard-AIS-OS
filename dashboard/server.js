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
