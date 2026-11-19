# Map Research & Architectural Blueprint: Warehouse Yard TDM

## 1. Competitive TDM Level Design (BGMI / Warehouse Analysis)

### Core Layout & Flow Principles
* **Rotational & Mirror Symmetry:** Competitive fairness requires both teams (South and North) to experience identical timings, angles, and cover opportunities. Neither team possesses an asymmetric geographic advantage.
* **Compact Footprint (60m x 60m):** Standard competitive TDM maps benefit from a 50m–60m play area. Spawning to first engagement takes approximately 3–4 seconds of tactical sprinting, ensuring continuous engagement loops without spawn-trap frustration.
* **The Three-Lane Structure:**
  1. **West Lane (Container Flank):** Stacked shipping containers, container ramps, and heavy steel/concrete cover. Encourages close-to-medium range peeks (10m–20m) and dynamic flanking around container corners.
  2. **Central Lane (Main Open Warehouse):** A grand gabled-roof industrial warehouse with open sides and slatted timber walls. Serves as the high-risk, high-reward epicenter for direct combat, crossfire angles, and fast lane transitions.
  3. **East Lane (Rail & Yard Flank):** Train boxcar, timber log piles, concrete jersey barriers, and perimeter fencing. Offers longer sightlines for marksman/rifle duels and sneaky flank attacks behind the enemy's rear guard.
* **Sightline & Choke Point Control:**
  - Zero direct spawn-to-spawn line of sight. Protected spawn compounds with angled exits and visual blockers prevent instantaneous sniper kills.
  - Interior warehouse sightlines are interrupted by stacked wooden pallets, military weapon crates, steel barrels, and internal structural timber columns.
  - Typical gunfight engagement distance: 5m–25m.
* **Vertical Spaces & Micro-Elevation:**
  - Low-incline container ramps enabling players to scale 2-high shipping containers.
  - Elevated vantage perches with counter-angles (exposed from sides so campers cannot hold single invincible spots).

---

## 2. Visual Art Style & Environmental Aesthetics

* **Industrial "Warehouse Yard" Archetype:**
  - Weathered wood planks with natural grain, knotting, and aged grey/brown stain.
  - Heavy rusted corrugated metal siding and roof paneling.
  - Painted shipping containers in oxidized red, industrial teal/blue, and safety yellow with realistic edge wear and stenciled markings.
  - Chipped and dirty concrete flooring with wet sheen (low roughness values simulating recent rain).
  - Concrete Jersey barriers with scuffs, scratches, and chipped aggregate.
  - Distant mountain ridges and pine tree silhouettes bounding the horizon to establish grounded realism without geometry performance cost.
* **Atmospheric Lighting:**
  - Overcast daylight HDRI skybox producing soft, realistic ambient shadows without harsh pitch-black pockets.
  - ACES / Filmic tonemapper with gentle depth haze and aerial perspective fog.

---

## 3. Godot 4 Forward+ Technical Decisions & Budgets

* **Target Hardware & Target FPS:** 
  - Target: RTX 3050 6GB Laptop (and budget GPUs). 1080p @ stable 60+ FPS with 8 networked players.
  - Total package size: < 1.5 GB (achieved with 1K/2K compressed textures).
* **Lighting Strategy: Forward+ Direct Sun + Reflection Probes vs SDFGI:**
  - **SDFGI Verdict:** While dynamic, SDFGI is exceptionally GPU ray-tracing intensive and causes substantial frame rate variance on 3050 mobile GPUs (often dropping 15–25 FPS in complex multi-room geometry) and can introduce splotchy artifacts on moving characters.
  - **Selected Approach:** Optimized DirectionalLight3D with 3 PSSM shadow cascades (max distance 75m, blur 1.0, 1024/2048 atlas) paired with High-Quality Ambient Sky contribution and strategically placed box-projection `ReflectionProbe` nodes inside the warehouse interior and key lanes. This delivers crisp reflections, zero ray-tracing lag, rock-solid 60+ FPS, and zero visual ghosting.
* **SSAO, SSR & Post-Processing:**
  - SSAO enabled with subtle radius (0.8m) and intensity (1.2) for deep contact shadows under crates, barrels, and eaves.
  - SSR (Screen-Space Reflections) enabled for wet concrete and puddle surfaces.
  - Subtle glow/bloom (intensity 0.15, threshold 0.95) to accentuate weapon sights, muzzle flash, and exterior lighting.
* **Collision & Physics Fidelity:**
  - Only simple convex or box shapes for all cover props (containers, barriers, crates, barrels) to prevent player snagging, erratic bouncing, or edge clipping.
  - Trimesh static collision only on complex structural floor/roofing.
  - High-precision boundary collision walls (8m height) completely sealing the 60m x 60m perimeter to make map escapes impossible.
