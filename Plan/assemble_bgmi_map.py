import os

MAP_TSCN_PATH = "c:/Users/danie/Documents/my_projects/lan-fall-phase1/scenes/maps/warehouse/warehouse_map.tscn"
TEST_MAP_TSCN_PATH = "c:/Users/danie/Documents/my_projects/lan-fall-phase1/scenes/maps/test_map.tscn"

MAP_CONTENT = """[gd_scene load_steps=22 format=3 uid="uid://bgmi_tdm_warehouse_map_001"]

[ext_resource type="Script" path="res://scenes/maps/warehouse/warehouse_map.gd" id="1_script"]
[ext_resource type="PackedScene" path="res://scenes/player/player.tscn" id="2_player"]
[ext_resource type="PackedScene" path="res://scenes/ui/hud.tscn" id="3_hud"]
[ext_resource type="PackedScene" path="res://scenes/ui/pause_menu.tscn" id="4_pause"]
[ext_resource type="PackedScene" path="res://scenes/objects/target_dummy.tscn" id="5_dummy"]
[ext_resource type="Texture2D" path="res://assets/textures/terrain_grass_albedo.png" id="6_grass_albedo"]
[ext_resource type="Texture2D" path="res://assets/textures/terrain_grass_normal.png" id="7_grass_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/terrain_gravel_dirt_albedo.png" id="8_dirt_albedo"]
[ext_resource type="Texture2D" path="res://assets/textures/terrain_gravel_dirt_normal.png" id="9_dirt_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/sky_erangel_daylight.png" id="10_sky"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_tdm_warehouse.tscn" id="ext_warehouse"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_spawn_sheds.tscn" id="ext_spawnsheds"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_perimeter_fence.tscn" id="ext_fence"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_train_boxcar.tscn" id="ext_boxcar"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_container_ramp.tscn" id="ext_container_ramp"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_timber_logs.tscn" id="ext_timber_logs"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_wooden_pergola.tscn" id="ext_pergola"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_jersey_barrier.tscn" id="ext_barrier"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_crate_stack.tscn" id="ext_crates"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_backdrop_villa.tscn" id="ext_villa"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/pine_tree.tscn" id="ext_tree"]

[sub_resource type="PanoramaSkyMaterial" id="PanoramaSkyMaterial_1"]
panorama = ExtResource("10_sky")

[sub_resource type="Sky" id="Sky_1"]
sky_material = SubResource("PanoramaSkyMaterial_1")

[sub_resource type="Environment" id="Environment_BGMI"]
background_mode = 2
sky = SubResource("Sky_1")
ambient_light_source = 3
ambient_light_sky_contribution = 0.65
ambient_light_color = Color(0.85, 0.88, 0.92, 1)
ambient_light_energy = 0.95
tonemap_mode = 3
tonemap_exposure = 1.08
ssao_enabled = false
glow_enabled = true
glow_intensity = 0.18
glow_bloom = 0.08
fog_enabled = true
fog_light_color = Color(0.78, 0.86, 0.92, 1)
fog_density = 0.0006
fog_depth_begin = 60.0
fog_depth_end = 250.0

[sub_resource type="StandardMaterial3D" id="Mat_GrassTerrain"]
albedo_texture = ExtResource("6_grass_albedo")
normal_enabled = true
normal_texture = ExtResource("7_grass_norm")
roughness = 0.9
uv1_scale = Vector3(18, 26, 1)

[sub_resource type="StandardMaterial3D" id="Mat_DirtRoadways"]
albedo_texture = ExtResource("8_dirt_albedo")
normal_enabled = true
normal_texture = ExtResource("9_dirt_norm")
roughness = 0.92
uv1_scale = Vector3(4, 24, 1)

[sub_resource type="BoxShape3D" id="BoxShape3D_Ground"]
size = Vector3(76, 0.4, 116)

[sub_resource type="BoxMesh" id="BoxMesh_GrassFloor"]
material = SubResource("Mat_GrassTerrain")
size = Vector3(76, 0.4, 116)

[sub_resource type="BoxMesh" id="BoxMesh_DirtMainLane"]
material = SubResource("Mat_DirtRoadways")
size = Vector3(9.0, 0.02, 110.0)

[sub_resource type="BoxMesh" id="BoxMesh_DirtCrossLane"]
material = SubResource("Mat_DirtRoadways")
size = Vector3(68.0, 0.02, 7.5)

[node name="WarehouseMap" type="Node3D"]
script = ExtResource("1_script")

[node name="Players" type="Node3D" parent="."]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_BGMI")

# Warm Erangel Golden Sun
[node name="Sun" type="DirectionalLight3D" parent="."]
transform = Transform3D(-0.766044, -0.321394, 0.55667, 0, 0.866025, 0.5, -0.642788, 0.383022, -0.663414, 0, 45, 0)
light_color = Color(1.0, 0.96, 0.88, 1)
light_energy = 1.35
shadow_enabled = true
shadow_bias = 0.02
directional_shadow_split_1 = 0.12
directional_shadow_split_2 = 0.3
directional_shadow_split_3 = 0.6
directional_shadow_blend_splits = false
directional_shadow_max_distance = 80.0
shadow_blur = 1.0

# -----------------------------------------------------------------------------
# TERRAIN & GROUND PATHWAYS
# -----------------------------------------------------------------------------
[node name="Terrain" type="Node3D" parent="."]

[node name="GrassField" type="StaticBody3D" parent="Terrain"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -0.2, 0)

[node name="Collision" type="CollisionShape3D" parent="Terrain/GrassField"]
shape = SubResource("BoxShape3D_Ground")

[node name="Mesh" type="MeshInstance3D" parent="Terrain/GrassField"]
mesh = SubResource("BoxMesh_GrassFloor")

[node name="DirtWalkwayMain" type="MeshInstance3D" parent="Terrain"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.015, 0)
mesh = SubResource("BoxMesh_DirtMainLane")

[node name="DirtWalkwayCross" type="MeshInstance3D" parent="Terrain"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.016, 0)
mesh = SubResource("BoxMesh_DirtCrossLane")

# -----------------------------------------------------------------------------
# CENTERPIECE: BGMI TDM MAIN WAREHOUSE (At (0, 0, 0))
# -----------------------------------------------------------------------------
[node name="TDM_Warehouse_Center" parent="." instance=ExtResource("ext_warehouse")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

# Outside Warehouse Entrance Cover
[node name="WarehouseCrates_SouthL" parent="." instance=ExtResource("ext_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.8, 0, 15.2)

[node name="WarehouseCrates_SouthR" parent="." instance=ExtResource("ext_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.8, 0, 15.2)

[node name="WarehouseCrates_NorthL" parent="." instance=ExtResource("ext_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.8, 0, -15.2)

[node name="WarehouseCrates_NorthR" parent="." instance=ExtResource("ext_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.8, 0, -15.2)

# -----------------------------------------------------------------------------
# SOUTH SPAWN COMPOUND (TEAM 1 / ATTACKERS - Z = +42)
# -----------------------------------------------------------------------------
[node name="SouthSpawnCompound" type="Node3D" parent="."]

[node name="TwinSheds_South" parent="SouthSpawnCompound" instance=ExtResource("ext_spawnsheds")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 44.0)

[node name="Fence_SouthWest" parent="SouthSpawnCompound" instance=ExtResource("ext_fence")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -15.0, 0, 48.0)

[node name="Fence_SouthEast" parent="SouthSpawnCompound" instance=ExtResource("ext_fence")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 15.0, 0, 48.0)

# -----------------------------------------------------------------------------
# NORTH SPAWN COMPOUND (TEAM 2 / DEFENDERS - Z = -42)
# -----------------------------------------------------------------------------
[node name="NorthSpawnCompound" type="Node3D" parent="."]

[node name="TwinSheds_North" parent="NorthSpawnCompound" instance=ExtResource("ext_spawnsheds")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 0, 0, -44.0)

[node name="Fence_NorthWest" parent="NorthSpawnCompound" instance=ExtResource("ext_fence")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -15.0, 0, -48.0)

[node name="Fence_NorthEast" parent="NorthSpawnCompound" instance=ExtResource("ext_fence")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 15.0, 0, -48.0)

# -----------------------------------------------------------------------------
# SOUTH-CENTER APPROACH (Z = +22 to +32)
# -----------------------------------------------------------------------------
[node name="SouthApproach" type="Node3D" parent="."]

# Yellow Container with Sniper Wooden Ramp leading to roof
[node name="ContainerRamp_South" parent="SouthApproach" instance=ExtResource("ext_container_ramp")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6.5, 0, 26.0)

# Train Boxcar Parked on Right of Approach
[node name="TrainCar_South" parent="SouthApproach" instance=ExtResource("ext_boxcar")]
transform = Transform3D(0.965926, 0, 0.258819, 0, 1, 0, -0.258819, 0, 0.965926, 8.5, 0, 27.0)

# Concrete Jersey Barriers for South Peek Angles
[node name="Barrier_SouthMain1" parent="SouthApproach" instance=ExtResource("ext_barrier")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.8, 0, 21.0)

[node name="Barrier_SouthMain2" parent="SouthApproach" instance=ExtResource("ext_barrier")]
transform = Transform3D(0.866025, 0, 0.5, 0, 1, 0, -0.5, 0, 0.866025, 2.5, 0, 20.0)

# -----------------------------------------------------------------------------
# NORTH-CENTER APPROACH (Z = -22 to -32)
# -----------------------------------------------------------------------------
[node name="NorthApproach" type="Node3D" parent="."]

# Mirrored Container with Ramp
[node name="ContainerRamp_North" parent="NorthApproach" instance=ExtResource("ext_container_ramp")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 6.5, 0, -26.0)

# Mirrored Train Boxcar
[node name="TrainCar_North" parent="NorthApproach" instance=ExtResource("ext_boxcar")]
transform = Transform3D(-0.965926, 0, -0.258819, 0, 1, 0, 0.258819, 0, -0.965926, -8.5, 0, -27.0)

# Concrete Jersey Barriers for North Peek Angles
[node name="Barrier_NorthMain1" parent="NorthApproach" instance=ExtResource("ext_barrier")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 1.8, 0, -21.0)

[node name="Barrier_NorthMain2" parent="NorthApproach" instance=ExtResource("ext_barrier")]
transform = Transform3D(0.866025, 0, -0.5, 0, 1, 0, 0.5, 0, 0.866025, -2.5, 0, -20.0)

# -----------------------------------------------------------------------------
# WEST FLANK (LEFT LANE - X = -16 to -28)
# -----------------------------------------------------------------------------
[node name="WestFlank" type="Node3D" parent="."]

# Wooden Pergola / Trellis Gazebo (as seen in video frame 8)
[node name="Pergola_WestSouth" parent="WestFlank" instance=ExtResource("ext_pergola")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -19.5, 0, 18.0)

# 2x2 Crate Stack along West Fence
[node name="CrateStack_WestSouth" parent="WestFlank" instance=ExtResource("ext_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -16.0, 0, 10.0)

[node name="CrateStack_WestMid" parent="WestFlank" instance=ExtResource("ext_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -14.5, 0, 0.0)

[node name="CrateStack_WestNorth" parent="WestFlank" instance=ExtResource("ext_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -16.0, 0, -10.0)

# Concrete Barriers along West Lane
[node name="Barrier_West1" parent="WestFlank" instance=ExtResource("ext_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -12.5, 0, 16.0)

[node name="Barrier_West2" parent="WestFlank" instance=ExtResource("ext_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -12.5, 0, -16.0)

# Perimeter Wooden Lattice Fence
[node name="Fence_WestSouth" parent="WestFlank" instance=ExtResource("ext_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, 20.0)

[node name="Fence_WestMid" parent="WestFlank" instance=ExtResource("ext_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, 0.0)

[node name="Fence_WestNorth" parent="WestFlank" instance=ExtResource("ext_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, -20.0)

# Background White Villa House (North-West)
[node name="Villa_Backdrop_NW" parent="WestFlank" instance=ExtResource("ext_villa")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -30.0, 0, -42.0)

# -----------------------------------------------------------------------------
# EAST FLANK (RIGHT LANE / TIMBER YARD - X = +16 to +28)
# -----------------------------------------------------------------------------
[node name="EastFlank" type="Node3D" parent="."]

# Stacked Timber Logs in Wooden Cradles
[node name="TimberLogs_South" parent="EastFlank" instance=ExtResource("ext_timber_logs")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 19.5, 0, 18.0)

[node name="TimberLogs_Mid" parent="EastFlank" instance=ExtResource("ext_timber_logs")]
transform = Transform3D(0.965926, 0, -0.258819, 0, 1, 0, 0.258819, 0, 0.965926, 21.0, 0, 2.0)

[node name="TimberLogs_North" parent="EastFlank" instance=ExtResource("ext_timber_logs")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 19.5, 0, -18.0)

# Long Railway Boxcar on East Railway Track
[node name="TrainCar_EastTrack" parent="EastFlank" instance=ExtResource("ext_boxcar")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 22.0, 0, -6.0)

# Concrete Barriers along East Lane
[node name="Barrier_East1" parent="EastFlank" instance=ExtResource("ext_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 12.5, 0, 16.0)

[node name="Barrier_East2" parent="EastFlank" instance=ExtResource("ext_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 12.5, 0, -16.0)

# Perimeter Wooden Lattice Fence
[node name="Fence_EastSouth" parent="EastFlank" instance=ExtResource("ext_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 26.0, 0, 20.0)

[node name="Fence_EastMid" parent="EastFlank" instance=ExtResource("ext_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 26.0, 0, 0.0)

[node name="Fence_EastNorth" parent="EastFlank" instance=ExtResource("ext_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 26.0, 0, -20.0)

# Background Barn (North-East)
[node name="Barn_Backdrop_NE" parent="EastFlank" instance=ExtResource("ext_villa")]
transform = Transform3D(0.866025, 0, -0.5, 0, 1, 0, 0.5, 0, 0.866025, 30.0, 0, -42.0)

# -----------------------------------------------------------------------------
# FOLIAGE & SCENERY TREES
# -----------------------------------------------------------------------------
[node name="PerimeterTrees" type="Node3D" parent="."]

[node name="Tree_SW" parent="PerimeterTrees" instance=ExtResource("ext_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, -29, 0, 36)

[node name="Tree_SE" parent="PerimeterTrees" instance=ExtResource("ext_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, 29, 0, 36)

[node name="Tree_NW" parent="PerimeterTrees" instance=ExtResource("ext_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, -28, 0, -32)

[node name="Tree_NE" parent="PerimeterTrees" instance=ExtResource("ext_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, 28, 0, -32)

# -----------------------------------------------------------------------------
# TARGET PRACTICE DUMMIES (Tactical Choke Points)
# -----------------------------------------------------------------------------
[node name="TargetDummies" type="Node3D" parent="."]

# Center Warehouse Inside
[node name="Dummy_WarehouseInside" parent="TargetDummies" instance=ExtResource("5_dummy")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 0)

# South Main Warehouse Door
[node name="Dummy_SouthDoor" parent="TargetDummies" instance=ExtResource("5_dummy")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 12.0)

# North Main Warehouse Door
[node name="Dummy_NorthDoor" parent="TargetDummies" instance=ExtResource("5_dummy")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 0, 0.8, -12.0)

# West Flank (Pergola choke)
[node name="Dummy_WestFlank" parent="TargetDummies" instance=ExtResource("5_dummy")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -16.5, 0.8, 4.0)

# East Flank (Timber logs choke)
[node name="Dummy_EastFlank" parent="TargetDummies" instance=ExtResource("5_dummy")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 16.5, 0.8, -4.0)

# -----------------------------------------------------------------------------
# PLAYER & USER INTERFACE
# -----------------------------------------------------------------------------
[node name="Player" parent="." instance=ExtResource("2_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.2, 42.0)

[node name="HUD" parent="." instance=ExtResource("3_hud")]
[node name="PauseMenu" parent="." instance=ExtResource("4_pause")]
"""

with open(MAP_TSCN_PATH, "w") as f:
    f.write(MAP_CONTENT)
print("Saved warehouse_map.tscn")

# Also update test_map.tscn with matching script path
TEST_CONTENT = MAP_CONTENT.replace('res://scenes/maps/warehouse/warehouse_map.gd', 'res://scenes/maps/test_map.gd')
with open(TEST_MAP_TSCN_PATH, "w") as f:
    f.write(TEST_CONTENT)
print("Saved test_map.tscn")
