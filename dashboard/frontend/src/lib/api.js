import axios from "axios";

// Default to the local backend when REACT_APP_BACKEND_URL is unset so the app
// works out of the box in dev. Set REACT_APP_BACKEND_URL for other deployments.
const BASE = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
const API = `${BASE}/api`;

const client = axios.create({ baseURL: API, timeout: 12000 });

// Each call returns a promise. Callers use Promise.allSettled and render empty
// states when a source is unreachable, so the dashboard never hard-crashes.
export const api = {
  sections: () => client.get("/sections").then((r) => r.data),
  systemStats: () => client.get("/system/stats").then((r) => r.data),
  memoryNodes: () => client.get("/memory/nodes").then((r) => r.data),
  networkGraph: () => client.get("/network/graph").then((r) => r.data),
  tools: () => client.get("/tools").then((r) => r.data),
  comms: () => client.get("/comms").then((r) => r.data),
  brief: () => client.get("/brief").then((r) => r.data),
  decisions: () => client.get("/decisions").then((r) => r.data),
  leads: () => client.get("/leads").then((r) => r.data),
};

export default api;
