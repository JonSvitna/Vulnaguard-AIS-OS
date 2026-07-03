// Small formatting helpers shared across views.

export function relativeTime(iso) {
  if (!iso) return "—";
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return "—";
  const secs = Math.max(0, Math.floor((Date.now() - then) / 1000));
  if (secs < 60) return "now";
  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins}m`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h`;
  const days = Math.floor(hrs / 24);
  if (days < 30) return `${days}d`;
  return `${Math.floor(days / 30)}mo`;
}

// Compact number: 1240 -> "1.2k"
export function compact(n) {
  if (n == null) return "—";
  if (n < 1000) return String(n);
  return `${(n / 1000).toFixed(1)}k`;
}

export function titleCase(s) {
  if (!s) return "";
  return s
    .toLowerCase()
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

// Backend tool status (online | standby | offline) -> pill tone + short label.
export function toolTone(status) {
  if (status === "online") return "ok";
  if (status === "standby") return "warn";
  return "idle";
}
export function toolLabel(status) {
  if (status === "online") return "ok";
  if (status === "standby") return "stale";
  return "idle";
}

// Today's date as "FRI · JUL 03 2026"
export function briefDate(d = new Date()) {
  const days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
  const mons = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
  const dd = String(d.getDate()).padStart(2, "0");
  return `${days[d.getDay()]} · ${mons[d.getMonth()]} ${dd} ${d.getFullYear()}`;
}
