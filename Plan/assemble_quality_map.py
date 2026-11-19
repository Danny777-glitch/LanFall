import os

MAP_TSCN_TEMPLATE = """[gd_scene load_steps=22 format=3 uid="uid://bgmi_tdm_quality_map_002"]

[ext_resource type="Script" path="{SCRIPT_PATH}" id="1_script"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/sparse_grass_diff_1k.jpg" id="2_grass_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/sparse_grass_nor_gl_1k.jpg" id="3_grass_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/sparse_grass_rough_1k.jpg" id="4_grass_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/stony_dirt_path_diff_1k.jpg" id="5_dirt_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/stony_dirt_path_nor_gl_1k.jpg" id="6_dirt_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/stony_dirt_path_rough_1k.jpg" id="7_dirt_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/sky_erangel_daylight.png" id="8_sky"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_tdm_warehouse.tscn" id="9_warehouse"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_spawn_sheds.tscn" id="10_spawnsheds"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_perimeter_fence.tscn" id="11_fence"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_train_boxcar.tscn" id="12_boxcar"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_container_ramp.tscn" id="13_container_ramp"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_timber_logs.tscn" id="14_timber_logs"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_wooden_pergola.tscn" id="15_pergola"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_jersey_barrier.tscn" id="16_barrier"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_crate_stack.tscn" id="17_crates"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/bgmi_backdrop_villa.tscn" id="18_villa"]
[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/pine_tree.tscn" id="19_tree"]
[ext_resource type="PackedScene" path="res://scenes/ui/hud.tscn" id="20_hud"]
[ext_resource type="PackedScene" path="res://scenes/ui/pause_menu.tscn" id="21_pause"]
[ext_resource type="PackedScene" path="res://scenes/objects/target_dummy.tscn" id="22_dummy"]

[sub_resource type="PanoramaSkyMaterial" id="PanoramaSkyMaterial_1"]
panorama = ExtResource("8_sky")

[sub_resource type="Sky" id="Sky_1"]
sky_material = SubResource("PanoramaSkyMaterial_1")

[sub_resource type="Environment" id="Environment_BGMI"]
background_mode = 2
sky = SubResource("Sky_1")
ambient_light_source = 3
ambient_light_sky_contribution = 0.7
ambient_light_color = Color(0.85, 0.88, 0.92, 1)
ambient_light_energy = 1.05
tonemap_mode = 3
tonemap_exposure = 1.08
ssao_enabled = false
glow_enabled = true
glow_intensity = 0.16
glow_bloom = 0.06
fog_enabled = true
fog_light_color = Color(0.72, 0.80, 0.88, 1)
fog_density = 0.001
fog_depth_begin = 90.0
fog_depth_end = 280.0

[sub_resource type="StandardMaterial3D" id="Mat_GrassTerrain"]
albedo_texture = ExtResource("2_grass_diff")
normal_enabled = true
normal_texture = ExtResource("3_grass_norm")
roughness_texture = ExtResource("4_grass_rough")
roughness = 0.9
uv1_scale = Vector3(16, 24, 1)

[sub_resource type="StandardMaterial3D" id="Mat_DirtRoadways"]
albedo_texture = ExtResource("5_dirt_diff")
normal_enabled = true
normal_texture = ExtResource("6_dirt_norm")
roughness_texture = ExtResource("7_dirt_rough")
roughness = 0.92
uv1_scale = Vector3(3, 20, 1)

[sub_resource type="BoxShape3D" id="BoxShape3D_Ground"]
size = Vector3(84, 0.4, 120)

[sub_resource type="BoxMesh" id="BoxMesh_GrassFloor"]
material = SubResource("Mat_GrassTerrain")
size = Vector3(84, 0.4, 120)

[sub_resource type="BoxMesh" id="BoxMesh_DirtMainLane"]
material = SubResource("Mat_DirtRoadways")
size = Vector3(10.0, 0.02, 114.0)

[sub_resource type="BoxMesh" id="BoxMesh_DirtCrossLane"]
material = SubResource("Mat_DirtRoadways")
size = Vector3(72.0, 0.02, 8.0)

[node name="WarehouseMap" type="Node3D"]
script = ExtResource("1_script")

[node name="Players" type="Node3D" parent="."]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_BGMI")

[node name="Sun" type="DirectionalLight3D" parent="."]
transform = Transform3D(-0.766044, -0.321394, 0.55667, 0, 0.866025, 0.5, -0.642788, 0.383022, -0.663414, 0, 45, 0)
light_color = Color(1.0, 0.95, 0.86, 1)
light_energy = 1.38
shadow_enabled = true
shadow_bias = 0.02
directional_shadow_split_1 = 0.12
directional_shadow_split_2 = 0.3
directional_shadow_split_3 = 0.6
directional_shadow_blend_splits = false
directional_shadow_max_distance = 80.0
shadow_blur = 1.0

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

[node name="TDM_Warehouse_Center" parent="." instance=ExtResource("9_warehouse")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

[node name="WarehouseCrates_SouthL" parent="." instance=ExtResource("17_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.2, 0, 15.2)

[node name="WarehouseCrates_SouthR" parent="." instance=ExtResource("17_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.2, 0, 15.2)

[node name="WarehouseCrates_NorthL" parent="." instance=ExtResource("17_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.2, 0, -15.2)

[node name="WarehouseCrates_NorthR" parent="." instance=ExtResource("17_crates")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.2, 0, -15.2)

[node name="SouthSpawnCompound" type="Node3D" parent="."]

[node name="TwinSheds_South" parent="SouthSpawnCompound" instance=ExtResource("10_spawnsheds")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 44.0)

[node name="Fence_SouthWest" parent="SouthSpawnCompound" instance=ExtResource("11_fence")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -15.0, 0, 48.0)

[node name="Fence_SouthEast" parent="SouthSpawnCompound" instance=ExtResource("11_fence")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 15.0, 0, 48.0)

[node name="NorthSpawnCompound" type="Node3D" parent="."]

[node name="TwinSheds_North" parent="NorthSpawnCompound" instance=ExtResource("10_spawnsheds")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 0, 0, -44.0)

[node name="Fence_NorthWest" parent="NorthSpawnCompound" instance=ExtResource("11_fence")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, -15.0, 0, -48.0)

[node name="Fence_NorthEast" parent="NorthSpawnCompound" instance=ExtResource("11_fence")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 15.0, 0, -48.0)

[node name="SouthApproach" type="Node3D" parent="."]

[node name="SniperContainerRamp_South" parent="SouthApproach" instance=ExtResource("13_container_ramp")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6.5, 0, 26.5)

[node name="TrainCar_South" parent="SouthApproach" instance=ExtResource("12_boxcar")]
transform = Transform3D(0.965926, 0, 0.258819, 0, 1, 0, -0.258819, 0, 0.965926, 7.5, 0, 27.5)

[node name="Barrier_SouthEntry1" parent="SouthApproach" instance=ExtResource("16_barrier")]
transform = Transform3D(0.984808, 0, -0.173648, 0, 1, 0, 0.173648, 0, 0.984808, -1.8, 0, 20.0)

[node name="Barrier_SouthEntry2" parent="SouthApproach" instance=ExtResource("16_barrier")]
transform = Transform3D(0.984808, 0, 0.173648, 0, 1, 0, -0.173648, 0, 0.984808, 1.8, 0, 20.0)

[node name="NorthApproach" type="Node3D" parent="."]

[node name="SniperContainerRamp_North" parent="NorthApproach" instance=ExtResource("13_container_ramp")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 6.5, 0, -26.5)

[node name="TrainCar_North" parent="NorthApproach" instance=ExtResource("12_boxcar")]
transform = Transform3D(-0.965926, 0, -0.258819, 0, 1, 0, 0.258819, 0, -0.965926, -7.5, 0, -27.5)

[node name="Barrier_NorthEntry1" parent="NorthApproach" instance=ExtResource("16_barrier")]
transform = Transform3D(-0.984808, 0, 0.173648, 0, 1, 0, -0.173648, 0, -0.984808, 1.8, 0, -20.0)

[node name="Barrier_NorthEntry2" parent="NorthApproach" instance=ExtResource("16_barrier")]
transform = Transform3D(-0.984808, 0, -0.173648, 0, 1, 0, 0.173648, 0, -0.984808, -1.8, 0, -20.0)

[node name="WestFlank" type="Node3D" parent="."]

[node name="PergolaGazebo_West" parent="WestFlank" instance=ExtResource("15_pergola")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -16.5, 0, 0)

[node name="CrateStack_WestSouth" parent="WestFlank" instance=ExtResource("17_crates")]
transform = Transform3D(0.866025, 0, 0.5, 0, 1, 0, -0.5, 0, 0.866025, -15.5, 0, 10.5)

[node name="CrateStack_WestNorth" parent="WestFlank" instance=ExtResource("17_crates")]
transform = Transform3D(0.866025, 0, -0.5, 0, 1, 0, 0.5, 0, 0.866025, -15.5, 0, -10.5)

[node name="Barrier_WestMid1" parent="WestFlank" instance=ExtResource("16_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -11.5, 0, 3.8)

[node name="Barrier_WestMid2" parent="WestFlank" instance=ExtResource("16_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -11.5, 0, -3.8)

[node name="EastFlank" type="Node3D" parent="."]

[node name="TrainCar_EastRail" parent="EastFlank" instance=ExtResource("12_boxcar")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 19.5, 0, 0)

[node name="TimberLogs_EastSouth" parent="EastFlank" instance=ExtResource("14_timber_logs")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 14.5, 0, 9.5)

[node name="TimberLogs_EastNorth" parent="EastFlank" instance=ExtResource("14_timber_logs")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 14.5, 0, -9.5)

[node name="TimberLogs_EastMid" parent="EastFlank" instance=ExtResource("14_timber_logs")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 14.5, 0, 0)

[node name="Barrier_EastMid1" parent="EastFlank" instance=ExtResource("16_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 11.5, 0, 4.2)

[node name="Barrier_EastMid2" parent="EastFlank" instance=ExtResource("16_barrier")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 11.5, 0, -4.2)

[node name="PerimeterEnvironment" type="Node3D" parent="."]

[node name="BackdropVilla_NW" parent="PerimeterEnvironment" instance=ExtResource("18_villa")]
transform = Transform3D(0.965926, 0, 0.258819, 0, 1, 0, -0.258819, 0, 0.965926, -26.0, 0, -36.0)

[node name="BackdropVilla_SE" parent="PerimeterEnvironment" instance=ExtResource("18_villa")]
transform = Transform3D(-0.965926, 0, -0.258819, 0, 1, 0, 0.258819, 0, -0.965926, 26.0, 0, 36.0)

[node name="FenceWest1" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, -24.0)

[node name="FenceWest2" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, -16.0)

[node name="FenceWest3" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, -8.0)

[node name="FenceWest4" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, 0)

[node name="FenceWest5" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, 8.0)

[node name="FenceWest6" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, 16.0)

[node name="FenceWest7" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -26.0, 0, 24.0)

[node name="FenceEast1" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 26.0, 0, -24.0)

[node name="FenceEast2" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 26.0, 0, -16.0)

[node name="FenceEast3" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 26.0, 0, -8.0)

[node name="FenceEast4" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 26.0, 0, 0)

[node name="FenceEast5" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 26.0, 0, 8.0)

[node name="FenceEast6" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 26.0, 0, 16.0)

[node name="FenceEast7" parent="PerimeterEnvironment" instance=ExtResource("11_fence")]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 26.0, 0, 24.0)

[node name="PineTree1" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, -29.0, 0, -24.0)

[node name="PineTree2" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.6, 0, 0, 0, 1.6, 0, 0, 0, 1.6, -30.0, 0, -10.0)

[node name="PineTree3" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, -29.5, 0, 12.0)

[node name="PineTree4" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, -30.0, 0, 25.0)

[node name="PineTree5" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, 29.0, 0, -24.0)

[node name="PineTree6" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, 30.0, 0, -10.0)

[node name="PineTree7" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, 29.5, 0, 12.0)

[node name="PineTree8" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.6, 0, 0, 0, 1.6, 0, 0, 0, 1.6, 30.0, 0, 25.0)

[node name="PineTreeNorth1" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, -12.0, 0, -54.0)

[node name="PineTreeNorth2" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.6, 0, 0, 0, 1.6, 0, 0, 0, 1.6, 12.0, 0, -54.0)

[node name="PineTreeSouth1" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, -12.0, 0, 54.0)

[node name="PineTreeSouth2" parent="PerimeterEnvironment" instance=ExtResource("19_tree")]
transform = Transform3D(1.6, 0, 0, 0, 1.6, 0, 0, 0, 1.6, 12.0, 0, 54.0)

[node name="HUD" parent="." instance=ExtResource("20_hud")]

[node name="PauseMenu" parent="." instance=ExtResource("21_pause")]

[node name="TargetDummyCenter" parent="." instance=ExtResource("22_dummy")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

[node name="TargetDummyCourtyard" parent="." instance=ExtResource("22_dummy")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 0, 0, -18.0)
"""

# 1. Write scenes/maps/test_map.tscn
test_map_content = MAP_TSCN_TEMPLATE.replace("{SCRIPT_PATH}", "res://scenes/maps/test_map.gd")
with open(r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps\test_map.tscn", "w", encoding="utf-8") as f:
    f.write(test_map_content)
print("Saved scenes/maps/test_map.tscn")

# 2. Write scenes/maps/warehouse/warehouse_map.tscn
warehouse_map_content = MAP_TSCN_TEMPLATE.replace("{SCRIPT_PATH}", "res://scenes/maps/warehouse/warehouse_map.gd")
with open(r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps\warehouse\warehouse_map.tscn", "w", encoding="utf-8") as f:
    f.write(warehouse_map_content)
print("Saved scenes/maps/warehouse/warehouse_map.tscn")
