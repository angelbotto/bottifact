## Fleet globe

<!-- nota:ejemplo globo-flota -->

```html
{{EXAMPLE}}
```

**Use and limits:** Explore a declared operational snapshot across Colombian cities with selectable vehicles. Load one Three 0.160.1, geography, globe and fleet. One instance; 1–12 vehicles with unique IDs, distinct endpoints, valid Colombian coordinates, progress 0–100, nonnegative integer orders and a zoned ISO timestamp. Routes are schematic arcs, never streets, GPS, ETA or measured distance. Drag rotates; Shift+drag pans; focused wheel/buttons and pinch zoom. Arrows rotate, Shift+arrows pan, +/- zoom and Home resets. No inertia/camera animation. Rear-hemisphere labels/vehicles hide; collision-prone labels remain accessible in route focus and list. Manual exploration can move endpoints out of view; reset restores framing. Playback demonstrates positions for 45 seconds without sound or delivery-state updates, pausing when hidden and respecting reduced motion/manual progress. A historical snapshot must not be labeled live. Without WebGL retain list/detail/table. `NotaFlota.init/get`, seek(0…100), select(id) and destroy manage lifecycle; destroy/update/reinitialize for another snapshot.
