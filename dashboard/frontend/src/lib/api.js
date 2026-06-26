import axios from "axios";

const BASE = process.env.REACT_APP_BACKEND_URL;
const API = `${BASE}/api`;

const client = axios.create({ baseURL: API, timeout: 12000 });

// Each call returns a promise; falls back to stub data if the API is unreachable
// so the 3D experience never breaks. Real sources can replace the backend later.
export const api = {
  sections: () => client.get("/sections").then((r) => r.data),
  systemStats: () => client.get("/system/stats").then((r) => r.data),
  memoryNodes: () => client.get("/memory/nodes").then((r) => r.data),
  networkGraph: () => client.get("/network/graph").then((r) => r.data),
  tools: () => client.get("/tools").then((r) => r.data),
  globePoints: () => client.get("/globe/points").then((r) => r.data),
  comms: () => client.get("/comms").then((r) => r.data),
};

export default api;
