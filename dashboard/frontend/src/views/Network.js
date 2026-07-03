import React, { useMemo } from "react";
import StatTile from "../components/StatTile";
import NetworkCanvas from "../components/NetworkCanvas";
import { titleCase } from "../lib/format";

// Derive degree, top node + neighbors, clusters, and orphans from the raw graph.
function analyze(network) {
  const nodes = network?.nodes || [];
  const edges = network?.edges || [];
  if (!nodes.length) return null;

  const byId = new Map(nodes.map((n) => [n.id, n]));
  const degree = new Map();
  const neighbors = new Map();
  const bump = (a, b) => {
    degree.set(a, (degree.get(a) || 0) + 1);
    if (!neighbors.has(a)) neighbors.set(a, new Set());
    neighbors.get(a).add(b);
  };
  edges.forEach((e) => {
    if (byId.has(e.source) && byId.has(e.target)) {
      bump(e.source, e.target);
      bump(e.target, e.source);
    }
  });

  let topId = null;
  let topDeg = -1;
  degree.forEach((deg, id) => {
    if (deg > topDeg) { topDeg = deg; topId = id; }
  });

  const topNode = topId ? byId.get(topId) : nodes[0];
  const topNeighbors = topId
    ? [...(neighbors.get(topId) || [])]
        .map((id) => ({ node: byId.get(id), deg: degree.get(id) || 0 }))
        .sort((a, b) => b.deg - a.deg)
        .slice(0, 6)
    : [];

  // Clusters by node type.
  const typeCount = new Map();
  nodes.forEach((n) => {
    const t = n.type || "unknown";
    typeCount.set(t, (typeCount.get(t) || 0) + 1);
  });
  const clusters = [...typeCount.entries()]
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 6);
  const maxCluster = clusters.length ? clusters[0].count : 1;

  const orphans = nodes.filter((n) => !degree.has(n.id)).length;

  return {
    nodeCount: nodes.length,
    edgeCount: edges.length,
    clusterCount: typeCount.size,
    orphans,
    topNode,
    topDeg: Math.max(topDeg, 0),
    topNeighbors,
    clusters,
    maxCluster,
  };
}

export default function Network({ network }) {
  const a = useMemo(() => analyze(network), [network]);

  return (
    <div className="canvas">
      <StatTile label="Nodes" value={a ? a.nodeCount : "—"} delta="indexed" />
      <StatTile label="Links" value={a ? a.edgeCount : "—"} delta="relations" />
      <StatTile label="Clusters" value={a ? a.clusterCount : "—"} accent delta="by type" />
      <StatTile label="Orphans" value={a ? a.orphans : "—"} delta="unlinked" />

      <div className="block netpanel span-8">
        <div className="block-head"><span className="title display">Live Knowledge Graph</span><span className="id">NET-02</span></div>
        <div className="net-canvas-wrap lg">
          <span className="corner tl" /><span className="corner tr" /><span className="corner bl" /><span className="corner br" />
          <NetworkCanvas nodes={network?.nodes} edges={network?.edges} fallbackCount={60} />
          <div className="net-legend">
            <span><b style={{ background: "#22d3ee" }} />AIOS memory</span>
            <span><b style={{ background: "#67e8f9" }} />Obsidian vault</span>
          </div>
        </div>
      </div>

      <div className="block span-4">
        <div className="block-head"><span className="title display">Node Inspector</span></div>
        {a && a.topNode ? (
          <>
            <div className="insp-node">
              <span className="glyph"><b /></span>
              <div>
                <div className="nm">{a.topNode.name}</div>
                <div className="sub">{a.topNode.type || "node"} · {a.topDeg} links · {a.topNode.source}</div>
              </div>
            </div>
            {a.topNeighbors.length ? a.topNeighbors.map((n) => (
              <div key={n.node.id} className="conn">
                <span className="arrow">→</span>
                <span className="cname">{n.node.name}</span>
                <span className="w">{n.deg}</span>
              </div>
            )) : <div className="empty">No links from this node.</div>}
          </>
        ) : <div className="empty">Graph is empty — no memory or vault notes indexed.</div>}
      </div>

      <div className="block span-12">
        <div className="block-head"><span className="title display">Densest Clusters</span><span className="action">by type</span></div>
        {a && a.clusters.length ? a.clusters.map((c) => (
          <div key={c.name} className="cluster">
            <span className="cn">{titleCase(c.name)}</span>
            <span className="bar"><i style={{ width: `${Math.round((c.count / a.maxCluster) * 100)}%` }} /></span>
            <span className="cv">{c.count}</span>
          </div>
        )) : <div className="empty">No clusters to compute.</div>}
      </div>
    </div>
  );
}
