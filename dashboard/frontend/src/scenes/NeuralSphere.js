import React, { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

const R = 2.2;
const _m = new THREE.Matrix4();
const _v = new THREE.Vector3();
const _s = new THREE.Vector3();
const _q = new THREE.Quaternion();

export default function NeuralSphere({ graph }) {
  const group = useRef();
  const nodesRef = useRef();
  const pulsesRef = useRef();

  const { positions, edges, edgeGeo, count } = useMemo(() => {
    if (!graph || !graph.nodes) return { positions: [], edges: [], edgeGeo: null, count: 0 };
    const map = {};
    const positions = graph.nodes.map((n) => {
      const v = new THREE.Vector3(n.x, n.y, n.z).multiplyScalar(R);
      map[n.id] = v;
      return v;
    });
    const edges = [];
    const pos = [];
    graph.edges.forEach((e) => {
      const a = map[e.source];
      const b = map[e.target];
      if (!a || !b) return;
      edges.push({ a, b });
      pos.push(a.x, a.y, a.z, b.x, b.y, b.z);
    });
    const edgeGeo = new THREE.BufferGeometry();
    edgeGeo.setAttribute("position", new THREE.BufferAttribute(new Float32Array(pos), 3));
    return { positions, edges, edgeGeo, count: edges.length };
  }, [graph]);

  // place node spheres
  useFrame((state) => {
    const t = state.clock.elapsedTime;
    if (group.current) group.current.rotation.y += 0.0016;
    if (nodesRef.current) {
      positions.forEach((p, i) => {
        const pulse = 1 + Math.sin(t * 2 + i) * 0.25;
        _s.setScalar(0.03 * pulse + 0.02);
        _m.compose(p, _q, _s);
        nodesRef.current.setMatrixAt(i, _m);
      });
      nodesRef.current.instanceMatrix.needsUpdate = true;
    }
    if (pulsesRef.current && edges.length) {
      edges.forEach((e, i) => {
        const tt = (t * 0.35 + i * 0.137) % 1;
        _v.lerpVectors(e.a, e.b, tt);
        const fade = Math.sin(tt * Math.PI); // bright in middle
        _s.setScalar(0.018 + 0.05 * fade);
        _m.compose(_v, _q, _s);
        pulsesRef.current.setMatrixAt(i, _m);
      });
      pulsesRef.current.instanceMatrix.needsUpdate = true;
    }
  });

  if (!positions.length) return null;

  return (
    <group ref={group}>
      <mesh>
        <sphereGeometry args={[R * 1.16, 40, 40]} />
        <meshBasicMaterial color="#22d3ee" transparent opacity={0.04} side={THREE.BackSide} toneMapped={false} />
      </mesh>

      <lineSegments geometry={edgeGeo}>
        <lineBasicMaterial color="#22d3ee" transparent opacity={0.22} toneMapped={false} />
      </lineSegments>

      <instancedMesh ref={nodesRef} args={[null, null, positions.length]}>
        <sphereGeometry args={[1, 10, 10]} />
        <meshBasicMaterial color="#67e8f9" toneMapped={false} />
      </instancedMesh>

      <instancedMesh ref={pulsesRef} args={[null, null, Math.max(count, 1)]}>
        <sphereGeometry args={[1, 8, 8]} />
        <meshBasicMaterial color="#ecfeff" toneMapped={false} />
      </instancedMesh>
    </group>
  );
}
