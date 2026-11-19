# LAN Fall - Game Development Roadmap & Architecture Plan

> **Project Goal**: A fast-paced, joyful LAN FPS arena with a **Valorant-style stylized aesthetic**, built to run at **butter-smooth 60+ FPS even on budget laptops (Intel Core i3 11th/12th Gen with integrated Intel UHD / Iris Xe graphics)**.

---

## 1. Current State (Phase 1 Sandbox Completed)

### Player Controller & Mechanics
- **Movement**: WASD Walking (5.0 m/s), Sprinting with Shift (8.5 m/s), Smooth acceleration and friction.
- **Jumping & Gravity**: Space jump (5.0 m/s), realistic gravity, air control (0.3).
- **Head Bob**: Dynamic camera bobbing while moving, dampens when aiming.
- **ADS (Aim Down Sights)**: Right-Click (RMB) smooth zoom from 75 to 50 FOV, centered weapon sights, tighter recoil kick, and reduced mouse sensitivity for precision shooting.
- **Weapon & Recoil**: Blaster-A model with procedural kickback and pitch lift recovery, ammo tracking (30 magazine / 90 reserve), manual reload (R) with gun dip animation.

### Audio System (100% Native .ogg Assets)
- **Gunshot**: blaster.ogg with random pitch variation on every shot.
- **Reload**: reload.ogg mechanical reload sound.
- **Hit Confirm**: hit.ogg played via HUD on hitting targets.
- **Dummy Destroyed**: destroy.ogg spatial 3D audio when dummies reach 0 HP.
- **Jump**: jump.ogg played on jump take-off.
- **Landing**: land.ogg played when hitting the floor from a fall.
- **Footsteps**: Dynamic rhythmic footstep system (0.44s interval walking, 0.28s sprinting) with natural pitch variation.

### Combat Juice & Visual Feedback
- **Muzzle Flash**: Dynamic OmniLight3D at blaster barrel flashing on each shot.
- **Impact Sparks**: impact_effect.tscn emitting bright golden sparks and flash on bullet hit.
- **Hitmarker**: Dynamic diagonal 'X' crosshair feedback in HUD on hit.
- **Interactive Targets**: Target Dummies with floating 3D HP labels, hit flash, destruction shrink animation, and 3-second auto-respawn.

### Valorant-Style Tactical Map (70x70 Arena)
- **Atmosphere & Sky**: Vibrant sunset procedural sky (twilight blue to glowing orange horizon), ACES tonemapping, warm bloom, depth fog, and low-angle golden hour sun casting long dramatic shadows.
- **The Valorant House ("Veedu")**:
  - 2-Story Mediterranean building with plaster walls and terracotta roof.
  - Walk-in ground floor doorway.
  - 2nd-floor Sniper Balcony / A-Heaven overlooking the courtyard with low peeking parapet.
  - Exterior access ramp to run straight up to the balcony.
- **Site A Courtyard**: Raised plant platform, glowing teal Radianite tech crates with emissive lighting, tactical orange crates, jump-boost boxes.
- **Mid Choke Point**: Dividing wall with an archway doorway choke and corner peek boxes.
- **Elevated Catwalk**: High-ground sniper ledge with ramp and railing.
- **4 Tactical Dummies**: Positioned on Site, in the 2nd-Floor House Balcony, Mid choke, and Catwalk.

---

## 2. Performance Philosophy (The "i3 60+ FPS Rule")

- **Target Hardware**: Intel Core i3 (11th/12th Gen) with Intel UHD / Iris Xe Graphics (No dedicated GPU required).
- **Optimization Strategy**:
  1. **Stylized over Heavy Photorealism**: High-contrast, clean textures instead of heavy voxel ray-marching (No laggy SDFGI).
  2. **Lightweight Shaders**: Low-overhead cel-shading / outlines.
  3. **Efficient Draw Calls**: CSG / modular meshes with shared materials.
  4. **Smooth 60-100+ FPS Guaranteed** for college & home budget laptops.

---

## 3. Next Milestones & Feature Roadmap

### Milestone 1: Stylized Visual Polish (Valorant Look)
- [ ] Add clean stylized textures (cobblestone paths, clean stone bricks, wood plank trims, Mediterranean roof tiles).
- [ ] Lightweight anime / comic outline or cel-shading post-processing shader.
- [ ] Subtle floating ambient dust particles in the sunset light.
- [ ] Visual settings toggle (Low / Medium / High) so players can customize performance.

### Milestone 2: Weapon Arsenal & Polish
- [ ] Weapon switching (1, 2, 3): Pistol / Blaster, Assault Rifle, Shotgun.
- [ ] Bullet tracers (visual glowing line showing bullet path).
- [ ] Weapon bob / sway when turning mouse.

### Milestone 3: Game Loop & HUD Polish
- [ ] Scoreboard & Target Dummy kill counter.
- [ ] Kill feed or damage popup numbers (+25 floating damage numbers).
- [ ] Tactical mini-map or radar.

### Milestone 4: LAN Multiplayer Foundation
- [ ] ENetMultiplayerPeer host / join lobby (Local IP connection).
- [ ] Player synchronization (position, rotation, shoot replication).
- [ ] Health and damage synchronization over LAN.

---

## 4. Controls Reference

- **Move**: W, A, S, D
- **Sprint**: Shift
- **Jump**: Space
- **Shoot**: Left Mouse Button
- **Aim Down Sights (ADS)**: Right Mouse Button (Hold)
- **Reload**: R
- **Release Mouse**: Escape
