import React, { useMemo } from "react";
import * as THREE from "three";
import { EffectComposer, Bloom, ChromaticAberration, Vignette } from "@react-three/postprocessing";
import { BlendFunction } from "postprocessing";

// Cinematic post: volumetric-style bloom, slight chromatic aberration, vignette.
export default function Effects() {
  const offset = useMemo(() => new THREE.Vector2(0.0009, 0.0011), []);
  return (
    <EffectComposer multisampling={4}>
      <Bloom
        intensity={1.15}
        luminanceThreshold={0.15}
        luminanceSmoothing={0.9}
        mipmapBlur
        radius={0.7}
      />
      <ChromaticAberration blendFunction={BlendFunction.NORMAL} offset={offset} radialModulation={false} />
      <Vignette eskil={false} offset={0.25} darkness={0.85} />
    </EffectComposer>
  );
}
