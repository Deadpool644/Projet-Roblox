# Active art direction

The user's current requirements are in [docs/Direction-artistique-premium.md](docs/Direction-artistique-premium.md). They supersede the visual compromises in v0.1–v0.5. Follow phases A–G in order and report the verification status of each phase.

- Do not generate foliage from spheres, flattened balls or stacked primitive clouds. Do not substitute primitive trees for missing meshes.
- No invented asset IDs, meshes, texture maps or audio. At the vegetation phase, stop if suitable assets are unavailable and provide the exact import requirements.
- v0.5 is an archived prototype, not a premium-quality baseline. Do not repackage its primitive vegetation as a new completed art pass. Its legacy geometric tests do not prove visual quality.
- Preserve working scripts, spawns and collisions. Notify the user before a terrain migration changes collision support; validate it in Studio before replacing the existing ground.
- The target terrain uses native Roblox Terrain, layered noise, organic materials and protected routes. Native terrain migration is not yet implemented or visually verified.
- Use modular, repeatable editor tools, with generated scenery grouped by Terrain/Vegetation/Props/Effects beneath the map. Global lighting effects must remain direct children of Lighting for Roblox to render them.
- Distinguish source inspection, mock tests, geometry previews and actual Roblox Studio validation. No native Studio executor is currently available in this workspace. Never claim a Studio screenshot, native visual pass or mobile performance result without evidence.
- Asset import requirements and current blockers are in [docs/Assets-premium.md](docs/Assets-premium.md). Phase A evidence is in [docs/Audit-premium-A.md](docs/Audit-premium-A.md).
- This cloud task already has an isolated checkout. Use it; do not create a Git worktree unless explicitly requested.
