// Ordered sections — each maps to one segment of the foreground dial.
export const SECTIONS = [
  { id: "overview", label: "OVERVIEW", code: "SYS-01", scene: "globe", desc: "Primary system telemetry" },
  { id: "network", label: "NETWORK", code: "NET-02", scene: "neural", desc: "Live knowledge graph" },
  { id: "memory", label: "MEMORY", code: "MEM-03", scene: "globe", desc: "Indexed memory vault" },
  { id: "systems", label: "SYSTEMS", code: "PWR-04", scene: "neural", desc: "Connected tool array" },
  { id: "comms", label: "COMMS", code: "COM-05", scene: "globe", desc: "Secure channel relay" },
];

export const sectionIndex = (id) => SECTIONS.findIndex((s) => s.id === id);
