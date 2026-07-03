// Ordered sections for the left rail + command bar. `id` maps to a view.
export const SECTIONS = [
  { id: "overview", label: "Overview", code: "SYS-01", desc: "Primary system telemetry" },
  { id: "network", label: "Network", code: "NET-02", desc: "Live knowledge graph" },
  { id: "memory", label: "Memory", code: "MEM-03", desc: "Indexed memory vault" },
  { id: "systems", label: "Systems", code: "PWR-04", desc: "Connected tool array" },
  { id: "comms", label: "Comms", code: "COM-05", desc: "Secure channel relay" },
];

export const sectionIndex = (id) => SECTIONS.findIndex((s) => s.id === id);
