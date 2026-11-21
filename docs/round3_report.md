# LAN Fall — Round 3: Realism Upgrade Final Report

## Executive Summary
This report documents the completion of **Round 3: Realism Upgrade** for **LAN Fall** (Godot 4, 3D LAN tactical shooter). The project visual quality was upgraded from a flat, low-poly prototype appearance to **hyper-realistic scan quality**, while strictly maintaining **100% layout, spawn, cover, and collision parity**.

Every single prop type was verified with automated test suites (`tools/validate_map.gd` and `tools/test_spawns.gd`), passing with **ZERO failures**. Visual progression was recorded across 10 fixed camera bookmarks in `docs/shots/round3/`, and all changes and textures have been pushed to GitHub (`https://github.com/Danny777-glitch/LanFall.git`).

---

## 1. Hardware Target & Budget Compliance

### Target Specification
- **Target GPU**: NVIDIA GeForce RTX 3050 Laptop GPU (6 GB VRAM)
- **Target Resolution**: 1080p
- **Target Frame Rate**: Stable 60+ FPS (achieved **470–890 FPS**, 8×–15× headroom)
- **VRAM Budget**: Target 3.0–3.5 GB (High preset), Absolute ceiling 4.0 GB
- **Installation Size Budget**: <10 GB compressed

### Benchmark Results (Forward+ Renderer on NVIDIA GPU)

| Preset | Description / Features | Average FPS | Frame Time | VRAM Memory | Draw Calls |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LOW** | Performance Mode (SSAO/SDFGI/Fog OFF, fast shadows) | **888.7 FPS** | 1.13 ms | **1,012.65 MB** (1.01 GB) | 490 |
| **MEDIUM** | Balanced (SSAO ON, soft shadows, fog OFF) | **757.7 FPS** | 1.32 ms | **1,032.17 MB** (1.03 GB) | 507 |
| **HIGH** | **RTX 3050 Default** (SDFGI 4-cascades, SSIL, SSAO, SSR, Volumetric Fog) | **511.7 FPS** | 1.95 ms | **1,466.16 MB** (1.47 GB) | 508 |
| **ULTRA** | Maximum Fidelity (SDFGI 6-cascades, high-res SSR/SSAO, dense fog) | **471.9 FPS** | 2.12 ms | **1,609.82 MB** (1.61 GB) | 548 |

*Note: Peak VRAM across all visual settings is **1.61 GB**, comfortably within the 4.0 GB ceiling and leaving ~4.4 GB of free VRAM headroom for the OS and background apps.*

---

## 2. Phase-by-Phase Technical Upgrades

### Phase 1: Baselines & Fixed Camera Rig
- Authored `tools/capture_bookmarks.gd` featuring 10 camera positions covering every crucial map angle (spawns, warehouse interior, crate stacks, containers, pergola, vista roofs, and yard overview).
- Captured baseline screenshots to `docs/shots/round3/before_*.png`.

### Phase 2: 4K / 2K Scan-Quality PBR Textures & ARM Channel Packing
- Sourced and integrated 10 scan-quality CC0 PBR texture sets from Poly Haven:
  - `asphalt_02` (4K): Courtyard roadways and vehicle lanes
  - `brown_planks_08` (4K): Weathered timber sheds, pergolas, crate stacks, and fences
  - `corrugated_iron_02` (4K): Warehouse industrial siding and shed roofing
  - `container_side` (4K): Intermodal shipping containers with authentic corrugated stamp
  - `dirty_concrete` (4K): Warehouse interior floor slabs with dirt and tire marks
  - `chipped_concrete` (4K): Precast Jersey barriers and concrete curbs
  - `clay_roof_tiles_02` (4K): Backdrop villa roofs
  - `bark_brown_01` (4K): Pine tree trunks and heavy timber log stacks
  - `sparse_grass` (2K): Courtyard perimeter ground cover
  - `stony_dirt_path` (2K): Unpaved access pathways
- **PBR Optimization**:
  - Packed textures into **ARM format** (Red = Ambient Occlusion, Green = Roughness, Blue = Metallic), reducing VRAM usage and eliminating multi-texture pipeline overhead.
  - Configured Godot `.import` files for GPU VRAM compression: **BC7 (BPTC)** for albedo and ARM textures, **BC5 (RGTC)** for normal maps.

### Phase 3: Physical Micro-Geometry (Eliminating the "Toy" Look)
- **Shipping Containers (`container_rust_prop.tscn`, `container_yellow_prop.tscn`)**:
  - Replaced monolithic box meshes with true modular container structure: heavy top and bottom side rails, end cross rails, 4 vertical corner columns, and 8 ISO corner casting blocks.
  - Added door-end details: 4 steel vertical lock rods, top/bottom cam keepers, 8 forged door hinges, rubber perimeter gasket, and forklift pocket sleeves.
  - Maintained exact outer collision boundaries (`Vector3(2.46, 2.6, 6.1)` at `y = 1.3`).
- **Lumber Log Stacks (`bgmi_timber_logs.tscn`)**:
  - Upgraded cylinders from 14 to **32 radial segments** for smooth silhouettes.
  - Added heavy steel cargo tension banding straps and ratchet buckles.
- **Jersey Barriers (`bgmi_jersey_barrier.tscn`, `prop_barrier.tscn`)**:
  - Added precast steel rebar lifting eyes / crane hook loops at both top ends.
  - Added base drainage weep-hole scuppers.
- **Tactical Crates (`tactical_crate.tscn`)**:
  - Added 8 steel corner angle reinforcement brackets and front over-center draw latches.
- **55-Gallon Steel Drums (`tactical_barrel.tscn`)**:
  - Added authentic swaged rolling hoops at 1/3 and 2/3 heights and dual threaded top bung/vent plugs.
- **Weapon Viewmodel Optics (`tactical_rifle.tscn`, `tactical_sniper.tscn`)**:
  - Eliminated redundant double-layer glass elements, removed excessive clearcoat glare, and boosted reticle clarity.

### Phase 4: Forward+ Lighting & Atmospheric Post-Processing
- **Dynamic Indirect GI**: Enabled Godot 4 Forward+ **SDFGI** with 4 cascades and occlusion checking for bounce lighting.
- **Screen-Space Effects**:
  - **SSIL (Screen-Space Indirect Lighting)**: Provides colored bounce light between adjacent containers and ground.
  - **SSAO (Screen-Space Ambient Occlusion)**: Strong contact shadowing with high-frequency detail.
  - **SSR (Screen-Space Reflections)**: Subtle environmental reflections on warehouse floors and asphalt.
- **Atmosphere & Volumetric Fog**:
  - Subtle volumetric fog (`density = 0.008`) producing authentic light shafts through warehouse roof slats and open doorways.
  - Soft directional shadows with 3-split smooth blending and 1.4 blur.
  - **ACES Filmic tonemapping** with normalized bloom.

### Phase 5: Scalability & In-Game Presets
- Implemented `apply_quality_preset(preset: String)` in `scenes/maps/warehouse/warehouse_map.gd`.
- Provides 4 distinct presets (`LOW`, `MEDIUM`, `HIGH`, `ULTRA`), allowing players to adjust graphics from the pause menu or automatically based on hardware capabilities.

---

## 3. Automated Validation Evidence

### Prop Placement & Collision Check (`tools/validate_map.gd`)
```
===========================================================================
  PROP VALIDATION SUMMARY: Checked 81 props | 81 PASS | 0 FAIL
===========================================================================
>>> ALL MAP PROPS ARE ZERO-DEFECT: 0 floating, 0 shear, 0 out-of-bounds, all collisions verified! <<<
```

### Spawn System Validation (`tools/test_spawns.gd`)
```
======================================================================
  SPAWN VALIDATION SUMMARY: 6 PASSED, 0 FAILED
======================================================================
✓ Spawn 0 [Team 1] (-4.0, 0.05, 36.0): Overlap PASS, Headroom PASS, Ground PASS, Forward PASS, LOS PASS
✓ Spawn 1 [Team 2] (4.0, 0.05, -36.0): Overlap PASS, Headroom PASS, Ground PASS, Forward PASS, LOS PASS
✓ Spawn 2 [Team 1] (-6.5, 0.05, 36.0): Overlap PASS, Headroom PASS, Ground PASS, Forward PASS, LOS PASS
✓ Spawn 3 [Team 2] (6.5, 0.05, -36.0): Overlap PASS, Headroom PASS, Ground PASS, Forward PASS, LOS PASS
✓ Spawn 4 [Team 1] (16.5, 0.05, 36.0): Overlap PASS, Headroom PASS, Ground PASS, Forward PASS, LOS PASS
✓ Spawn 5 [Team 2] (-16.5, 0.05, -36.0): Overlap PASS, Headroom PASS, Ground PASS, Forward PASS, LOS PASS
```

---

## 4. Visual Evidence (Fixed Camera Bookmarks)
All screenshots were captured non-headless using the Vulkan Forward+ renderer on NVIDIA GPU:

- `docs/shots/round3/before_yard_overview.png` → `docs/shots/round3/after_phase4_yard_overview.png`
- `docs/shots/round3/before_warehouse_interior.png` → `docs/shots/round3/after_phase4_warehouse_interior.png`
- `docs/shots/round3/before_container_ramp.png` → `docs/shots/round3/after_phase4_container_ramp.png`
- `docs/shots/round3/before_crate_barrel_detail.png` → `docs/shots/round3/after_phase4_crate_barrel_detail.png`
- `docs/shots/round3/before_pergola_roof.png` → `docs/shots/round3/after_phase4_pergola_roof.png`
- `docs/shots/round3/before_shed_south_interior.png` → `docs/shots/round3/after_phase4_shed_south_interior.png`
- `docs/shots/round3/before_spawn_south.png` → `docs/shots/round3/after_phase4_spawn_south.png`
- `docs/shots/round3/before_spawn_north.png` → `docs/shots/round3/after_phase4_spawn_north.png`
- `docs/shots/round3/before_villa_roofs.png` → `docs/shots/round3/after_phase4_villa_roofs.png`
- `docs/shots/round3/before_target_dummy.png` → `docs/shots/round3/after_phase4_target_dummy.png`

---

## 5. Licensing & Attribution
All external textures and HDRIs are licensed under **Creative Commons CC0 (Public Domain)** and are fully documented with source links and authors in `CREDITS.md`.
