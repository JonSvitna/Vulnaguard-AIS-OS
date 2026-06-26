import React, { useMemo, useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import worldGeo from "../data/world.geo.json";
import { geoToSegments, gridSegments, latLngToVec3 } from "./geo";

const R = 2;

function CityPoint({ point, onHover, onSelect }) {
  const [hovered, setHovered] = useState(false);
  const pos = useMemo(() => latLngToVec3(point.lat, point.lng, R * 1.01), [point]);
  const ringRef = useRef();
  const color = point.level === "critical" ? "#fb7185" : point.level === "high" ? "#ecfeff" : "#67e8f9";

  useFrame((state) => {
    if (ringRef.current) {
      const s = 1 + Math.sin(state.clock.elapsedTime * 2 + pos.x) * 0.25;
      ringRef.current.scale.setScalar(s);
      ringRef.current.material.opacity = 0.6 - (s - 1) * 1.5;
    }
  });

  return (
    <group position={pos}>
      <mesh
        onPointerOver={(e) => { e.stopPropagation(); setHovered(true); onHover(point); document.body.style.cursor = "pointer"; }}
        onPointerOut={() => { setHovered(false); onHover(null); document.body.style.cursor = "auto"; }}
        onClick={(e) => { e.stopPropagation(); onSelect(point); }}
      >
        <sphereGeometry args={[hovered ? 0.045 : 0.03, 12, 12]} />
        <meshBasicMaterial color={color} toneMapped={false} />
      </mesh>
      <mesh ref={ringRef} rotation={[Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.05, 0.07, 24]} />
        <meshBasicMaterial color={color} transparent opacity={0.5} side={THREE.DoubleSide} toneMapped={false} />
      </mesh>
    </group>
  );
}

export default function Globe({ points = [], onPointHover, onPointSelect }) {
  const group = useRef();
  const continents = useMemo(() => geoToSegments(worldGeo, R * 1.002), []);
  const grid = useMemo(() => gridSegments(R), []);

  const contGeo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(continents, 3));
    return g;
  }, [continents]);

  const gridGeo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(grid, 3));
    return g;
  }, [grid]);

  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.08;
  });

  return (
    <group ref={group} rotation={[0.35, 0, 0.05]}>
      {/* dark inner core for depth */}
      <mesh>
        <sphereGeometry args={[R * 0.985, 48, 48]} />
        <meshBasicMaterial color="#04141f" transparent opacity={0.55} />
      </mesh>

      {/* lat/long grid */}
      <lineSegments geometry={gridGeo}>
        <lineBasicMaterial color="#22d3ee" transparent opacity={0.18} toneMapped={false} />
      </lineSegments>

      {/* continents */}
      <lineSegments geometry={contGeo}>
        <lineBasicMaterial color="#67e8f9" transparent opacity={0.95} toneMapped={false} />
      </lineSegments>

      {/* atmosphere glow */}
      <mesh>
        <sphereGeometry args={[R * 1.18, 48, 48]} />
        <meshBasicMaterial color="#22d3ee" transparent opacity={0.05} side={THREE.BackSide} toneMapped={false} />
      </mesh>
      <mesh>
        <sphereGeometry args={[R * 1.06, 48, 48]} />
        <meshBasicMaterial color="#22d3ee" transparent opacity={0.06} side={THREE.BackSide} toneMapped={false} />
      </mesh>

      {points.map((p, i) => (
        <CityPoint key={i} point={p} onHover={onPointHover} onSelect={onPointSelect} />
      ))}
    </group>
  );
}
