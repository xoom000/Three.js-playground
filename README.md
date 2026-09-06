# Three.js Playground — Digital Gnosis Studio World

Dedicated React + TypeScript + Three.js / React Three Fiber workspace for the walkable Digital Gnosis spatial office.

This repository is intentionally separate from:
- `xoom000/DigitalGnosis` — public/company website
- `DigitalGnosis/dg-studio` — 3D model catalog / native creative operator app

## Stack
- React 19
- React Three Fiber
- Drei
- Three.js
- Vite
- Procedurally generated modular GLB assets

## Build
`npm run build` installs the Python geometry dependencies, generates the modular GLB kit + authored room layouts, then builds the Vite app. This is intentionally compatible with Vercel Git auto-deploys.

## Current kit
48 independent reusable assets plus Research, Lobby, Meeting, and Corridor room studies. Generated models are build artifacts and are not committed to Git.
