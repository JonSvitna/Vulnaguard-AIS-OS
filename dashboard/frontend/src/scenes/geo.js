import * as THREE from "three";

// Convert lat/lng to a point on a sphere of radius r.
export function latLngToVec3(lat, lng, r) {
  const phi = (90 - lat) * (Math.PI / 180);
  const theta = (lng + 180) * (Math.PI / 180);
  return new THREE.Vector3(
    -(r * Math.sin(phi) * Math.cos(theta)),
    r * Math.cos(phi),
    r * Math.sin(phi) * Math.sin(theta)
  );
}

// Flatten GeoJSON country polygons into a single Float32Array of line segments.
export function geoToSegments(geojson, r) {
  const positions = [];
  const pushRing = (ring) => {
    for (let i = 0; i < ring.length - 1; i++) {
      const a = latLngToVec3(ring[i][1], ring[i][0], r);
      const b = latLngToVec3(ring[i + 1][1], ring[i + 1][0], r);
      positions.push(a.x, a.y, a.z, b.x, b.y, b.z);
    }
  };
  for (const f of geojson.features) {
    const g = f.geometry;
    if (!g) continue;
    if (g.type === "Polygon") {
      g.coordinates.forEach(pushRing);
    } else if (g.type === "MultiPolygon") {
      g.coordinates.forEach((poly) => poly.forEach(pushRing));
    }
  }
  return new Float32Array(positions);
}

// Latitude / longitude wireframe grid as line segments.
export function gridSegments(r, latStep = 15, lngStep = 15, res = 64) {
  const positions = [];
  for (let lat = -75; lat <= 75; lat += latStep) {
    for (let i = 0; i < res; i++) {
      const a = latLngToVec3(lat, (i / res) * 360 - 180, r);
      const b = latLngToVec3(lat, ((i + 1) / res) * 360 - 180, r);
      positions.push(a.x, a.y, a.z, b.x, b.y, b.z);
    }
  }
  for (let lng = -180; lng < 180; lng += lngStep) {
    for (let i = 0; i < res; i++) {
      const a = latLngToVec3((i / res) * 180 - 90, lng, r);
      const b = latLngToVec3(((i + 1) / res) * 180 - 90, lng, r);
      positions.push(a.x, a.y, a.z, b.x, b.y, b.z);
    }
  }
  return new Float32Array(positions);
}
