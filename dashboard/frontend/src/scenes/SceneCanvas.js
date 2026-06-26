import React, { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import Globe from "./Globe";
import NeuralSphere from "./NeuralSphere";
import Particles from "./Particles";
import Effects from "./Effects";

export default function SceneCanvas({ scene, points, graph, onPointHover, onPointSelect }) {
  return (
    <Canvas
      className="r3f-canvas"
      dpr={[1, 2]}
      camera={{ position: [0, 0.6, 7], fov: 48 }}
      gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
    >
      <color attach="background" args={["#04060c"]} />
      <fog attach="fog" args={["#04060c", 9, 18]} />
      <ambientLight intensity={0.6} />

      <Suspense fallback={null}>
        <Particles />
        {scene === "neural" ? (
          <NeuralSphere graph={graph} />
        ) : (
          <Globe points={points} onPointHover={onPointHover} onPointSelect={onPointSelect} />
        )}
        <Effects />
      </Suspense>

      <OrbitControls
        enablePan={false}
        enableZoom
        minDistance={4.5}
        maxDistance={11}
        autoRotate
        autoRotateSpeed={0.45}
        enableDamping
        dampingFactor={0.06}
        rotateSpeed={0.5}
      />
    </Canvas>
  );
}
