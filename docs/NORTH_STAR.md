# Digital Gnosis: visual acceptance contract

The owner's Research, Meeting, Corridor, and Lobby concept images supplied on
2026-09-06 are the art-direction target. Better FPS alone is not acceptance.
The target is industrial-modern cyberpunk: charcoal structural steel, convincing
smoked glazing, dark mottled concrete, restrained DG-green identity, warm
architectural light, cyan/magenta screen spill, leather upholstery, real-looking
plants and detailed equipment. Not pastel, cute, bubbly, unlit black boxes or
low-resolution pixel art.

## Keep the projects separate

This repository (`xoom000/Three.js-playground`) is the React Three Fiber office
world and reusable environment kit. `DigitalGnosis/dg-studio` is the owner's 3D
model catalog. `xoom000/DigitalGnosis` is a different project. Do not write to
those repositories or change their deployment connections for this work.

## Non-negotiables

- Preserve separate reusable components, stable placement IDs, picking and GLB
  export. Runtime instancing is allowed; permanently flattening the authoring
  model or removing detail just to inflate FPS is not the solution.
- Keep antialiasing enabled. Balanced mode resolves at DPR 1.75 when stationary
  (limited by the device); camera motion can use DPR 1.25. High mode targets
  DPR 2 at rest and 1.5 in motion. Actual phone performance must be measured.
- Plants stay green, highlights retain color, and concrete is dark but readable.
  No white foliage, stair-step silhouettes, shadow-acne dots or overlapping
  transparent planes. Document runtime material corrections separately from
  source GLB changes.
- Room views start at an elevated front-corner angle. Do not let a normal swipe
  leave the visitor staring at the opaque back wall or under the floor. Full
  orbit/pan remains available when inspecting an individual component.
- Warm light, soft contact shading, material roughness and controlled reflections
  establish depth. Do not make everything pitch-black to conceal weak models.
- A green deployment check proves a build, not image quality or phone FPS.
  Compare real browser captures at the same camera, viewport and quality.

## Evidence required for visual changes

Render all four rooms and at least one standalone component. Check mobile controls,
room switching, instance selection, glass/wireframe toggles, reset and console
errors. Report actual draw/texture counts separately from device FPS. Do not use
a generated concept image as proof of runtime output. Demand-render idle time is
not slow GPU frame time; the performance HUD reports frame intervals, not GPU
profiler timings. Texture counts are resource counts, not GPU-memory MB.

## North-star repair preview, not final art approval

The current pass corrects non-textured palette factors, shares library materials,
batches opaque repetitions, keeps glass separately sortable, restores antialiasing,
and caches one higher-resolution shadow map. Contact grounding is an inexpensive
approximation, not baked global illumination. Original GLB downloads are unchanged;
preview materials are corrected by `src/kit/core/materials.ts`.

Higher-detail hero furniture, richer surface artwork, physically coherent baked
lighting/contact AO, room-specific light placement and more faithful reference
composition still need art review. Do not mark reference parity complete without
the owner's approval.
