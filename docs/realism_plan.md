# LanFall — Realism Upgrade Technical Architecture & Execution Plan

**Project**: LanFall (3D Tactical FPS - Godot 4.7.2 Forward+)  
**Target Hardware**: RTX 3050 Laptop GPU 6 GB VRAM, 1080p, Stable 60+ FPS  
**VRAM Budget**: 3.0–3.5 GB (High Preset), Absolute Ceiling: 4.0 GB  
**Installation Ceiling**: 10.0 GB compressed  
**Document**: `docs/realism_plan.md`  

---

## 1. Technical Framework & Forward+ Best Practices

### A. PBR (Physically Based Rendering) Workflow
Godot 4's Forward+ renderer implements a modern Cook-Torrance GGX microfacet specular BRDF with standard metallic-roughness workflow:
1. **Albedo (Base Color)**: Linear sRGB representation of diffuse reflectance. Free of baked directional lighting and baked contact shadows. Calibrated albedos: dark aged wood (0.15–0.30), raw concrete (0.35–0.50), painted container sheet metal (0.25–0.45), rust (0.15–0.25).
2. **Normal Maps (OpenGL +Y Convention)**: Tangent-space normal vector encoding. Godot uses OpenGL standard (+Y Up, +X Right, +Z Out). In Godot 4 import dock, enabling `Compress > Normal Map` automatically compresses as **RGTC / BC5** (2-channel high-precision vector compression where $Z$ is reconstructed via $\sqrt{1 - X^2 - Y^2}$).
3. **Roughness & Ambient Occlusion (AO)**: Grayscale linear data textures.
   - For standalone maps, imported as Linear Data with VRAM compression (BC7 / BPTC).
   - For packed ORM textures: Red = Ambient Occlusion, Green = Roughness, Blue = Metallic. Compressed with BC7 (`Compress > High Quality: Enabled`) to eliminate channel cross-talk and banding artifacts.
4. **Height / Depth / Parallax Mapping**: For heavy macro-detail surfaces (gravel, cobblestones, corrugated siding, weathered timber planks), StandardMaterial3D height/depth mapping with min/max parallax layers (8 to 32 steps) delivers tangible relief without geometric tessellation overhead.

---

### B. Texel Density Consistency
To avoid the "toy" look where one prop looks ultra-sharp while adjacent walls look blurred:
- **Hero & Primary Sightlines**: $1024\text{ px/m}$ (Player weapon viewmodel, first-person hands, containers, crates within 5m).
- **Secondary World Geometry**: $512\text{ px/m}$ (Warehouse interior walls, concrete slab floor, approach barriers, spawn compound structures).
- **Distant & Perimeter Props**: $256\text{ px/m}$ (Perimeter fences, backdrop villas, distant tree canopy).
- **UV Scaling**: Every procedural BoxMesh and world surface uses unified world-space scaling via `uv1_triplanar = true` or calibrated UV tiling to guarantee uniform texel density across all world axes.

---

### C. Surface Variation & Decal System
Godot 4 `Decal` nodes are rendered via screen-space clustered decal passes with near-zero geometry cost:
- **Puddles & Moisture**: High-specular, low-roughness ($0.05$) water decal patches with subtle normal ripples.
- **Industrial Grime & Oil Stains**: Dark, oily albedo decals with high roughness ($0.85$) placed near crate stacks, barrel clusters, and vehicle tracks.
- **Asphalt & Concrete Cracks**: High-frequency normal and albedo fracture decals breaking up uniform walkway seams.
- **Tactical Stencils & Markings**: Weathered military container labeling, safety chevron warning decals, and zone markers.

---

### D. Global Illumination & Interior Lighting Architecture
- **SDFGI (Signed Distance Field Global Illumination)**:
  - Enabled for the overall compound: provides dynamic real-time multi-bounce ambient lighting, sky bounce, and occlusion without static bake delays.
  - Settings: `sdfgi_use_occlusion = true` to prevent light leaking through warehouse siding; `sdfgi_bounce_feedback = 0.45` for balanced daylight bounce; `sdfgi_cascades = 4`; `sdfgi_min_cell_size = 0.25m`.
- **SSIL (Screen-Space Indirect Lighting)**:
  - Enabled alongside SDFGI: captures micro-bounces, color bleeding between painted containers and the ground, and contact crevices that coarse 3D distance fields miss.
- **SSAO (Screen-Space Ambient Occlusion)**:
  - Radius: $1.4m$, Intensity: $1.5$, Light Affect: $0.2$. Accentuates tight corners, container crevices, and floor seams to firmly ground every prop.
- **SSR (Screen-Space Reflections)**:
  - Active on smooth and wet surfaces (puddle decals, polished gunmetal, wet concrete patches).
- **Interior ReflectionProbes**:
  - Box-projected ReflectionProbes inside `TDM_Warehouse_Center` and `BGMI_SpawnCompound` provide accurate local reflection cubemaps without relying solely on the infinite sky.

---

### E. Atmosphere, Volumetric Fog & Tonemapping
- **HDRI Sky**: Poly Haven 4K/8K CC0 overcast daylight HDRI (`farmland_overcast_4k.hdr` / `kloppenheim_06_puresky_4k.hdr`).
- **Directional Light**: Color temperature $5800K$, light energy $1.2$, matching HDRI sun elevation and azimuth. Angular diameter $1.5^\circ$ for soft, realistic contact shadow penumbras (PCSS-style penumbra).
- **Volumetric Fog**: Godot 4 Forward+ clustered volumetric fog with density $0.003$, albedo matching sky haze, emitting subtle atmospheric god rays through warehouse doors, skylights, and roof slats.
- **Tonemapper**: ACES Fitted tonemapping curve (`tonemap_mode = 3`, `exposure = 0.96`), preserving high dynamic range in sunlight without clipping highlights into flat white, while lifting dark shadow details.

---

### F. Anti-Aliasing Strategy
- **Primary Anti-Aliasing**: **TAA (Temporal Anti-Aliasing)**. Mandatory for Forward+ photorealism: resolves specular shimmering, normal map aliasing, and stabilizes SSAO/SSIL noise.
- **Upscaling / Performance**: FSR 2.2 / FSR 1.0 integration in graphics presets for Low/Medium settings.
- **MSAA**: Disabled when TAA is active to prevent redundant GPU overhead and driver conflicts.

---

### G. Texture Compression & VRAM Budget Strategy
- **Albedo / Base Color**: BC7 (BPTC) with mipmaps enabled and anisotropic filtering 16x.
- **Normal Maps**: BC5 (RGTC 2-channel) with normal map mode enabled.
- **Roughness / AO / Metallic**: Single-channel BC4 or 3-channel BC7 packed ORM maps.
- **VRAM Budget Plan (High Preset)**:
  - Textures (4K main sets, 2K props, 1K micro-props): ~2,200 MB
  - Render Targets & G-Buffers (Forward+ 1080p, Depth, Normal, Motion, SSAO, SSR): ~450 MB
  - SDFGI Cascades & Buffers: ~320 MB
  - Shadow Atlases (2048 Directional, 1024 Omni/Spot): ~180 MB
  - Meshes & Vertex Buffers: ~120 MB
  - **Total Projected VRAM**: ~3,270 MB (Well within the 3.0–3.5 GB target, far below the 4.0 GB hard ceiling).

---

## 2. Asset Sourcing & Selection Catalog (100% CC0 / Permissive)

All sourced from Poly Haven, ambientCG, and Kenney (all licensed under CC0 Public Domain).

### A. Master PBR Texture Sets (4K / 2K)

| Surface Type | Asset ID | Source | Resolution | Maps Included | License | Intended Usage |
|---|---|---|---|---|---|---|
| **Dirty Concrete Floor** | `concrete_floor_worn_001` | Poly Haven | 4K | Diff, Nor, Rough, AO, Disp | CC0 | Central warehouse floor slab |
| **Wet / Cracked Asphalt** | `asphalt_02` / `cracked_asphalt` | ambientCG | 4K | Diff, Nor, Rough, AO | CC0 | Yard roads & approach lanes |
| **Weathered Wood Planks** | `brown_planks_08` / `wood_planks_02` | Poly Haven | 4K | Diff, Nor, Rough, AO, Disp | CC0 | Spawn shed deck, pergola, timber fences |
| **Corrugated Siding Metal** | `corrugated_iron_02` | Poly Haven | 4K | Diff, Nor, Rough, AO, Disp | CC0 | Warehouse exterior, train cars, shed roof |
| **Painted Container Metal** | `metal_plate_02` / `shipping_container` | Poly Haven | 4K | Diff, Nor, Rough, AO | CC0 | Shipping containers & ramps |
| **Clay Roof Tiles** | `clay_roof_tiles_02` | Poly Haven | 4K | Diff, Nor, Rough, AO | CC0 | Backdrop villa roofs & shed accents |
| **Terrain Grass Blend** | `sparse_grass` / `aerial_grass_rock` | Poly Haven | 4K | Diff, Nor, Rough, AO | CC0 | Yard ground plane |
| **Packed Dirt & Gravel** | `stony_dirt_path` / `gravel_concrete` | Poly Haven | 4K | Diff, Nor, Rough, AO | CC0 | Perimeter walkways & rail ballast |
| **Stucco / Villa Wall** | `concrete_wall_008` / `plaster_grey_04`| ambientCG | 4K | Diff, Nor, Rough, AO | CC0 | Villa exterior walls |
| **Weathered Timber Bark** | `bark_brown_01` | Poly Haven | 2K | Diff, Nor, Rough, AO | CC0 | East flank timber log stacks |

### B. Decals & Micro-Details

| Decal Type | Source | Resolution | Format | Purpose |
|---|---|---|---|---|
| **Oil Spill & Industrial Stains** | ambientCG | 2K | Albedo + Roughness Decal | Floor under train cars & barrels |
| **Asphalt Cracks & Potholes** | ambientCG | 2K | Albedo + Normal Decal | Walkways, breaking tiling seams |
| **Water Puddles** | Procedural / ambientCG | 2K | Normal + Roughness Decal | Low-lying courtyard depressions |
| **Military Shipping Stencils** | Custom Vector / Kenney | 2K | Albedo + Alpha Decal | Container sides, crate sides |

### C. 3D Meshes & Geometry Enhancements

| Asset / Prop | Replacement Plan | Geometry Details |
|---|---|---|
| **Shipping Containers** | Procedural / Poly Haven | Real 3D corrugated side profile, locking bars, corner casting pockets, beveled structural frame. |
| **Jersey Concrete Barriers** | Poly Haven / Custom Chamfered | Real chamfered top edge, drainage slot at bottom, lifting pin holes, surface chip decals. |
| **Pallets & Crates** | Poly Haven CC0 glTF models | Slatted individual boards, visible nail holes, corner bracket brackets. |
| **Metal Barrels** | Poly Haven `Barrel_01` (4K textures) | Stamped structural ribs, top rim lip, threaded bung caps, rust gradients. |
| **Pavilion & Shed Beams** | Custom ArrayMesh Bevels | 2 cm beveled structural edges catching specular light highlights. |
| **3D Trees & Vegetation** | Poly Haven CC0 3D foliage | High-poly 3D pine & broadleaf models, MultiMeshInstance3D ground grass & ferns. |
| **Weapon Viewmodels** | High-poly PBR tactical firearms | Realistic matte metal, polymer stippling, optic glass, realistic recoil pivots. |
| **Target Dummy** | Tactical Steel Silhouette | IPSC steel plate silhouette, vertical tubing, heavy base stand, steel strike ring. |

---

## 3. Execution Roadmap

1. **Phase 2 (Textures & Materials)**:
   - Download & stage 4K PBR texture sets from Poly Haven / ambientCG.
   - Configure Godot import settings (VRAM Compressed BC7/BC5, Mipmaps, Anisotropic 16x).
   - Rebuild all material resources with complete PBR maps (Albedo, Normal, Roughness, AO, Height where applicable).
   - Add surface decal systems (oil, cracks, puddles).
   - Validate map (`validate_map.gd`), test spawns (`test_spawns.gd`), capture bookmarks, profile, commit.
2. **Phase 3 (High-Fidelity Models & Beveled Geometry)**:
   - Enhance shipping container geometry with real corrugated extrusion and corner castings.
   - Upgrade wooden pergola and spawn shed timber posts with beveled structural framing.
   - Deploy MultiMeshInstance3D 3D foliage and ground clutter.
   - Upgrade weapon viewmodel with realistic PBR materials.
   - Validate map, test spawns, capture bookmarks, profile, commit.
3. **Phase 4 (Lighting, Atmosphere & Post-Processing)**:
   - Deploy 4K HDRI overcast sky with matching directional sunlight.
   - Tune SDFGI, SSAO, SSIL, SSR, and Volumetric Fog.
   - Validate map, test spawns, capture bookmarks, profile, commit.
4. **Phase 5 (Presets & Performance Optimization)**:
   - Implement settings menu with Low, Medium, High, Ultra presets.
   - Add GPU VRAM auto-detection.
   - Profile all bookmarks and verify budgets.
   - Validate map, test spawns, capture bookmarks, profile, commit.
5. **Phase 6 (Final Documentation & GitHub Push)**:
   - Comprehensive `docs/round3_report.md` with complete before/after evidence.
