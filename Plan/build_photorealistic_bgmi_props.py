import os

PROPS_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps\warehouse\props"
os.makedirs(PROPS_DIR, exist_ok=True)

# =============================================================================
# 1. BGMI SPAWN SHED COMPOUND (1:1 with frame_00_0s.jpg & frame_04_16s.jpg)
# =============================================================================
# Features:
# - Raised wooden deck floor
# - Solid back wall with timber planks & knee braces
# - European rustic facade behind with white-framed window & shutters
# - 6 thick square timber posts with diagonal support struts
# - Heavy pitched corrugated roof with overhang & fascia beams
# - 2 front doorway portals
# - Firewood log stack on the left (as in frame 0)
# - Blue canvas-covered cargo pile on the right (as in frame 0)
# - 2 heavy weapon tables with 3D ammo boxes and rifles
# =============================================================================

SPAWN_SHED_TSCN = """[gd_scene load_steps=18 format=3 uid="uid://bgmi_spawn_compound_002"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="1_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="2_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="3_wood_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="4_roof_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="5_roof_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="6_bark_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="7_bark_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/villa_facade_albedo.png" id="8_facade"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_albedo.png" id="9_crate_tex"]
[ext_resource type="PackedScene" path="res://assets/models/wooden_table_02/wooden_table_02.gltf" id="10_table"]
[ext_resource type="PackedScene" path="res://assets/models/ammo_box/ammo_box.gltf" id="11_ammo"]
[ext_resource type="PackedScene" path="res://scenes/weapons/tactical_rifle.tscn" id="12_rifle"]
[ext_resource type="PackedScene" path="res://scenes/weapons/tactical_sniper.tscn" id="13_sniper"]

[sub_resource type="StandardMaterial3D" id="Mat_DarkWoodPlanks"]
albedo_color = Color(0.45, 0.38, 0.32, 1)
albedo_texture = ExtResource("1_wood_diff")
normal_enabled = true
normal_texture = ExtResource("2_wood_norm")
roughness_texture = ExtResource("3_wood_rough")
roughness = 0.85
uv1_scale = Vector3(2, 3, 1)

[sub_resource type="StandardMaterial3D" id="Mat_TimberPosts"]
albedo_color = Color(0.38, 0.30, 0.24, 1)
albedo_texture = ExtResource("1_wood_diff")
normal_enabled = true
normal_texture = ExtResource("2_wood_norm")
roughness_texture = ExtResource("3_wood_rough")
roughness = 0.8
uv1_scale = Vector3(0.5, 3, 0.5)

[sub_resource type="StandardMaterial3D" id="Mat_CompoundRoof"]
albedo_color = Color(0.32, 0.36, 0.42, 1)
albedo_texture = ExtResource("4_roof_diff")
normal_enabled = true
normal_texture = ExtResource("5_roof_norm")
metallic = 0.65
roughness = 0.55
uv1_scale = Vector3(4, 3, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Firewood"]
albedo_texture = ExtResource("6_bark_diff")
normal_enabled = true
normal_texture = ExtResource("7_bark_norm")
roughness = 0.9
uv1_scale = Vector3(1, 2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_BlueTarp"]
albedo_color = Color(0.18, 0.28, 0.42, 1)
roughness = 0.65

[sub_resource type="StandardMaterial3D" id="Mat_HouseWall"]
albedo_texture = ExtResource("8_facade")
roughness = 0.8
uv1_scale = Vector3(2, 1, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Crate"]
albedo_texture = ExtResource("9_crate_tex")
roughness = 0.75

[sub_resource type="BoxShape3D" id="Col_Floor"]
size = Vector3(22.0, 0.3, 7.5)

[sub_resource type="BoxShape3D" id="Col_BackWall"]
size = Vector3(22.0, 4.5, 0.5)

[sub_resource type="BoxShape3D" id="Col_SideWall"]
size = Vector3(0.5, 4.5, 7.5)

[sub_resource type="BoxMesh" id="Mesh_FloorDeck"]
material = SubResource("Mat_DarkWoodPlanks")
size = Vector3(22.0, 0.3, 7.5)

[sub_resource type="BoxMesh" id="Mesh_BackWall"]
material = SubResource("Mat_DarkWoodPlanks")
size = Vector3(22.0, 4.5, 0.5)

[sub_resource type="BoxMesh" id="Mesh_SideWall"]
material = SubResource("Mat_DarkWoodPlanks")
size = Vector3(0.5, 4.5, 7.5)

[sub_resource type="BoxMesh" id="Mesh_FrontWallSegment"]
material = SubResource("Mat_DarkWoodPlanks")
size = Vector3(5.0, 4.5, 0.4)

[sub_resource type="BoxMesh" id="Mesh_FrontDoorHeader"]
material = SubResource("Mat_DarkWoodPlanks")
size = Vector3(4.5, 1.4, 0.4)

[sub_resource type="BoxMesh" id="Mesh_HeavyPost"]
material = SubResource("Mat_TimberPosts")
size = Vector3(0.48, 4.6, 0.48)

[sub_resource type="BoxMesh" id="Mesh_KneeBrace"]
material = SubResource("Mat_TimberPosts")
size = Vector3(0.22, 1.3, 0.22)

[sub_resource type="BoxMesh" id="Mesh_RoofSlab"]
material = SubResource("Mat_CompoundRoof")
size = Vector3(23.2, 0.35, 8.8)

[sub_resource type="BoxMesh" id="Mesh_FasciaBeam"]
material = SubResource("Mat_TimberPosts")
size = Vector3(23.4, 0.4, 0.4)

[sub_resource type="BoxMesh" id="Mesh_HouseBackdrop"]
material = SubResource("Mat_HouseWall")
size = Vector3(24.0, 8.0, 4.0)

[sub_resource type="CylinderMesh" id="Mesh_FirewoodLog"]
material = SubResource("Mat_Firewood")
top_radius = 0.18
bottom_radius = 0.18
height = 2.4
radial_segments = 10

[sub_resource type="BoxMesh" id="Mesh_TarpCoveredCrates"]
material = SubResource("Mat_BlueTarp")
size = Vector3(3.2, 1.8, 2.2)

[sub_resource type="BoxMesh" id="Mesh_CrateMesh"]
material = SubResource("Mat_Crate")
size = Vector3(1.3, 0.9, 1.1)

[node name="BGMI_SpawnCompound" type="StaticBody3D"]

[node name="ColFloor" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.15, 0)
shape = SubResource("Col_Floor")

[node name="FloorDeck" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.15, 0)
mesh = SubResource("Mesh_FloorDeck")

[node name="ColBack" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.25, 3.5)
shape = SubResource("Col_BackWall")

[node name="BackWall" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.25, 3.5)
mesh = SubResource("Mesh_BackWall")

[node name="HouseBackdrop" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.0, 5.8)
mesh = SubResource("Mesh_HouseBackdrop")

[node name="ColSideL" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10.8, 2.25, 0)
shape = SubResource("Col_SideWall")

[node name="SideWallL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10.8, 2.25, 0)
mesh = SubResource("Mesh_SideWall")

[node name="ColSideR" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10.8, 2.25, 0)
shape = SubResource("Col_SideWall")

[node name="SideWallR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10.8, 2.25, 0)
mesh = SubResource("Mesh_SideWall")

[node name="FrontWallL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.5, 2.25, -3.5)
mesh = SubResource("Mesh_FrontWallSegment")

[node name="FrontWallMid" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.25, -3.5)
mesh = SubResource("Mesh_FrontWallSegment")

[node name="FrontWallR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.5, 2.25, -3.5)
mesh = SubResource("Mesh_FrontWallSegment")

[node name="DoorHeaderL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4.25, 3.8, -3.5)
mesh = SubResource("Mesh_FrontDoorHeader")

[node name="DoorHeaderR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4.25, 3.8, -3.5)
mesh = SubResource("Mesh_FrontDoorHeader")

[node name="Post1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10.5, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6.0, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.5, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.5, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post5" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 6.0, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post6" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10.5, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="RoofMain" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.984808, 0.173648, 0, -0.173648, 0.984808, 0, 4.8, 0.2)
mesh = SubResource("Mesh_RoofSlab")

[node name="FasciaBeamFront" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.4, -3.6)
mesh = SubResource("Mesh_FasciaBeam")

[node name="TableLeft" parent="." instance=ExtResource("10_table")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, -4.5, 0.3, 1.8)

[node name="AmmoLeft1" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -5.2, 1.45, 1.7)

[node name="AmmoLeft2" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.1, 0, 0.4, 0, 1.2, 0, -0.4, 0, 1.1, -4.0, 1.45, 1.7)

[node name="RifleLeft" parent="." instance=ExtResource("12_rifle")]
transform = Transform3D(0.9, 0, 0, 0, 0, -0.9, 0, 0.9, 0, -4.6, 1.48, 1.8)

[node name="TableRight" parent="." instance=ExtResource("10_table")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, 4.5, 0.3, 1.8)

[node name="AmmoRight1" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 4.0, 1.45, 1.7)

[node name="AmmoRight2" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.1, 0, -0.4, 0, 1.2, 0, 0.4, 0, 1.1, 5.2, 1.45, 1.7)

[node name="SniperRight" parent="." instance=ExtResource("13_sniper")]
transform = Transform3D(0.9, 0, 0, 0, 0, -0.9, 0, 0.9, 0, 4.6, 1.48, 1.8)

[node name="FirewoodLog1" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, -8.5, 0.45, 1.8)
mesh = SubResource("Mesh_FirewoodLog")

[node name="FirewoodLog2" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, -8.5, 0.45, 2.2)
mesh = SubResource("Mesh_FirewoodLog")

[node name="FirewoodLog3" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, -8.5, 0.8, 2.0)
mesh = SubResource("Mesh_FirewoodLog")

[node name="TarpCrates" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.5, 1.1, 1.8)
mesh = SubResource("Mesh_TarpCoveredCrates")

[node name="ShedExitCrateL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4.2, 0.45, -4.2)
mesh = SubResource("Mesh_CrateMesh")

[node name="ShedExitCrateR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4.2, 0.45, -4.2)
mesh = SubResource("Mesh_CrateMesh")
"""

with open(os.path.join(PROPS_DIR, "bgmi_spawn_sheds.tscn"), "w") as f:
    f.write(SPAWN_SHED_TSCN)
print("Saved 1:1 photorealistic bgmi_spawn_sheds.tscn")

# =============================================================================
# 2. BGMI CONTAINER WITH SNIPER BOARDING RAMP (1:1 with frame_28_112s.jpg)
# =============================================================================
# Features:
# - Full-sized realistic industrial container (7.0m x 2.8m x 2.8m)
# - Weathered container siding with corner posts, door rods & roof rim
# - Ramp touching ground at y=0, ascending smoothly to container roof at y=2.8m
# - Side stringer wooden beams + 9 wood cross rungs/cleats
# - Mantleable sniper half-cover crate on roof
# =============================================================================

CONTAINER_RAMP_TSCN = """[gd_scene load_steps=10 format=3 uid="uid://bgmi_container_ramp_002"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_diff_1k.jpg" id="1_cont_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_nor_gl_1k.jpg" id="2_cont_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_rough_1k.jpg" id="3_cont_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_albedo.png" id="6_crate_tex"]

[sub_resource type="StandardMaterial3D" id="Mat_Container"]
albedo_color = Color(0.92, 0.82, 0.58, 1)
albedo_texture = ExtResource("1_cont_diff")
normal_enabled = true
normal_texture = ExtResource("2_cont_norm")
roughness_texture = ExtResource("3_cont_rough")
metallic = 0.65
roughness = 0.6
uv1_scale = Vector3(2.5, 1, 1)

[sub_resource type="StandardMaterial3D" id="Mat_ContainerTrims"]
albedo_color = Color(0.25, 0.24, 0.22, 1)
metallic = 0.85
roughness = 0.4

[sub_resource type="StandardMaterial3D" id="Mat_RampWood"]
albedo_color = Color(0.65, 0.56, 0.44, 1)
albedo_texture = ExtResource("4_wood_diff")
normal_enabled = true
normal_texture = ExtResource("5_wood_norm")
roughness = 0.85
uv1_scale = Vector3(1, 4, 1)

[sub_resource type="StandardMaterial3D" id="Mat_CrateRoof"]
albedo_texture = ExtResource("6_crate_tex")
roughness = 0.75

[sub_resource type="BoxShape3D" id="Col_Container"]
size = Vector3(7.0, 2.8, 2.8)

[sub_resource type="BoxShape3D" id="Col_Ramp"]
size = Vector3(2.2, 0.25, 6.3)

[sub_resource type="BoxMesh" id="Mesh_ContainerBody"]
material = SubResource("Mat_Container")
size = Vector3(7.0, 2.8, 2.8)

[sub_resource type="BoxMesh" id="Mesh_CornerPost"]
material = SubResource("Mat_ContainerTrims")
size = Vector3(0.25, 2.85, 0.25)

[sub_resource type="BoxMesh" id="Mesh_RampBed"]
material = SubResource("Mat_RampWood")
size = Vector3(2.0, 0.2, 6.26)

[sub_resource type="BoxMesh" id="Mesh_RampStringer"]
material = SubResource("Mat_RampWood")
size = Vector3(0.18, 0.35, 6.26)

[sub_resource type="BoxMesh" id="Mesh_RampCleat"]
material = SubResource("Mat_RampWood")
size = Vector3(1.9, 0.08, 0.12)

[sub_resource type="BoxMesh" id="Mesh_RoofCoverCrate"]
material = SubResource("Mat_CrateRoof")
size = Vector3(1.4, 0.9, 1.1)

[node name="BGMI_ContainerRamp" type="StaticBody3D"]

[node name="ColContainer" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, 0)
shape = SubResource("Col_Container")

[node name="ContainerMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, 0)
mesh = SubResource("Mesh_ContainerBody")

# 4 Corner Cast Lock Pillars
[node name="Post1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.4, 1.4, -1.3)
mesh = SubResource("Mesh_CornerPost")

[node name="Post2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.4, 1.4, -1.3)
mesh = SubResource("Mesh_CornerPost")

[node name="Post3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.4, 1.4, 1.3)
mesh = SubResource("Mesh_CornerPost")

[node name="Post4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.4, 1.4, 1.3)
mesh = SubResource("Mesh_CornerPost")

# Boarding Ramp: Rotated ~26.56 deg. Center at y=1.4, z=4.1. Touches ground at z=6.9, y=0. Touches roof at z=1.3, y=2.8.
[node name="ColRamp" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.4, 4.1)
shape = SubResource("Col_Ramp")

[node name="RampBed" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.4, 4.1)
mesh = SubResource("Mesh_RampBed")

[node name="RampStringerL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 1.25, 1.45, 4.1)
mesh = SubResource("Mesh_RampStringer")

[node name="RampStringerR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 3.15, 1.45, 4.1)
mesh = SubResource("Mesh_RampStringer")

# Ramp Cross Cleats (Anti-slip steps)
[node name="Cleat1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 0.5, 6.1)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 0.95, 5.1)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.4, 4.1)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.85, 3.1)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat5" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 2.3, 2.1)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat6" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 2.7, 1.2)
mesh = SubResource("Mesh_RampCleat")

# Roof Sniper Cover Crate (Resting directly on roof at y=2.8)
[node name="RoofSniperCover" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.8, 3.25, 0)
mesh = SubResource("Mesh_RoofCoverCrate")
"""

with open(os.path.join(PROPS_DIR, "bgmi_container_ramp.tscn"), "w") as f:
    f.write(CONTAINER_RAMP_TSCN)
print("Saved 1:1 photorealistic bgmi_container_ramp.tscn")

# =============================================================================
# 3. BGMI CRATE STACK (1:1 with frame_18_72s.jpg)
# =============================================================================
# Zero floating! Solid crates stacked 2 high:
# Bottom: 2 crates side by side (y = 0 to 0.9)
# Top: 2 crates resting flush on top (y = 0.9 to 1.8)
# =============================================================================

CRATE_STACK_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://bgmi_crate_stack_002"]

[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_albedo.png" id="1_crate_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_normal.png" id="2_crate_norm"]

[sub_resource type="StandardMaterial3D" id="Mat_WoodMilitaryCrate"]
albedo_texture = ExtResource("1_crate_diff")
normal_enabled = true
normal_texture = ExtResource("2_crate_norm")
roughness = 0.78

[sub_resource type="BoxShape3D" id="Col_CrateStack"]
size = Vector3(2.8, 1.8, 1.2)

[sub_resource type="BoxMesh" id="Mesh_CrateSingle"]
material = SubResource("Mat_WoodMilitaryCrate")
size = Vector3(1.36, 0.88, 1.16)

[node name="BGMI_CrateStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("Col_CrateStack")

# Bottom Crates (y = 0.45)
[node name="CrateBottomLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.7, 0.44, 0)
mesh = SubResource("Mesh_CrateSingle")

[node name="CrateBottomRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.7, 0.44, 0)
mesh = SubResource("Mesh_CrateSingle")

# Top Crates (Resting flush on bottom crates at y = 1.33)
[node name="CrateTopLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.7, 1.33, 0)
mesh = SubResource("Mesh_CrateSingle")

[node name="CrateTopRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.7, 1.33, 0)
mesh = SubResource("Mesh_CrateSingle")
"""

with open(os.path.join(PROPS_DIR, "bgmi_crate_stack.tscn"), "w") as f:
    f.write(CRATE_STACK_TSCN)
print("Saved 1:1 photorealistic bgmi_crate_stack.tscn")

# =============================================================================
# 4. BGMI TIMBER YARD LOGS (1:1 with frame_35_140s.jpg)
# =============================================================================
# Massive horizontal log stack (12 horizontal tree trunks in heavy cradle stanchions)
# =============================================================================

TIMBER_LOGS_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_timber_logs_002"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="1_bark_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="2_bark_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_rough_1k.jpg" id="3_bark_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]

[sub_resource type="StandardMaterial3D" id="Mat_Bark"]
albedo_color = Color(0.45, 0.38, 0.32, 1)
albedo_texture = ExtResource("1_bark_diff")
normal_enabled = true
normal_texture = ExtResource("2_bark_norm")
roughness_texture = ExtResource("3_bark_rough")
roughness = 0.88
uv1_scale = Vector3(1, 3, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Stanchion"]
albedo_color = Color(0.35, 0.28, 0.22, 1)
albedo_texture = ExtResource("4_wood_diff")
roughness = 0.82
uv1_scale = Vector3(0.5, 3, 0.5)

[sub_resource type="BoxShape3D" id="Col_LogStack"]
size = Vector3(6.8, 2.4, 2.8)

[sub_resource type="CylinderMesh" id="Mesh_HorizontalLog"]
material = SubResource("Mat_Bark")
top_radius = 0.32
bottom_radius = 0.32
height = 6.6
radial_segments = 14

[sub_resource type="BoxMesh" id="Mesh_VerticalStanchion"]
material = SubResource("Mat_Stanchion")
size = Vector3(0.35, 2.6, 0.35)

[node name="BGMI_TimberLogStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.2, 0)
shape = SubResource("Col_LogStack")

# 4 Heavy Vertical Cradle Stanchions
[node name="PostFrontL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.1, 1.3, 1.25)
mesh = SubResource("Mesh_VerticalStanchion")

[node name="PostFrontR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.1, 1.3, 1.25)
mesh = SubResource("Mesh_VerticalStanchion")

[node name="PostBackL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.1, 1.3, -1.25)
mesh = SubResource("Mesh_VerticalStanchion")

[node name="PostBackR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.1, 1.3, -1.25)
mesh = SubResource("Mesh_VerticalStanchion")

# Layer 1 (Bottom 4 Horizontal Logs)
[node name="Log_1_1" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0.32, -0.9)
mesh = SubResource("Mesh_HorizontalLog")

[node name="Log_1_2" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0.32, -0.3)
mesh = SubResource("Mesh_HorizontalLog")

[node name="Log_1_3" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0.32, 0.3)
mesh = SubResource("Mesh_HorizontalLog")

[node name="Log_1_4" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0.32, 0.9)
mesh = SubResource("Mesh_HorizontalLog")

# Layer 2 (Mid 3 Horizontal Logs)
[node name="Log_2_1" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0.9, -0.6)
mesh = SubResource("Mesh_HorizontalLog")

[node name="Log_2_2" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0.9, 0.0)
mesh = SubResource("Mesh_HorizontalLog")

[node name="Log_2_3" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0.9, 0.6)
mesh = SubResource("Mesh_HorizontalLog")

# Layer 3 (Upper 2 Horizontal Logs)
[node name="Log_3_1" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 1.48, -0.3)
mesh = SubResource("Mesh_HorizontalLog")

[node name="Log_3_2" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 1.48, 0.3)
mesh = SubResource("Mesh_HorizontalLog")

# Layer 4 (Apex Top Log)
[node name="Log_4_1" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 2.05, 0.0)
mesh = SubResource("Mesh_HorizontalLog")
"""

with open(os.path.join(PROPS_DIR, "bgmi_timber_logs.tscn"), "w") as f:
    f.write(TIMBER_LOGS_TSCN)
print("Saved 1:1 photorealistic bgmi_timber_logs.tscn")

# =============================================================================
# 5. BGMI PERIMETER FENCE (1:1 with frame_18_72s.jpg & frame_35_140s.jpg)
# =============================================================================
# Continuous rustic timber plank fence with top diamond lattice panel & heavy posts
# =============================================================================

FENCE_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_perimeter_fence_002"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="1_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="2_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_fence_lattice_albedo.png" id="3_lattice"]

[sub_resource type="StandardMaterial3D" id="Mat_FencePlanks"]
albedo_color = Color(0.5, 0.42, 0.35, 1)
albedo_texture = ExtResource("1_wood_diff")
normal_enabled = true
normal_texture = ExtResource("2_wood_norm")
roughness = 0.85
uv1_scale = Vector3(2, 2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_TopLattice"]
albedo_texture = ExtResource("3_lattice")
roughness = 0.8
uv1_scale = Vector3(3, 1, 1)

[sub_resource type="BoxShape3D" id="Col_Fence"]
size = Vector3(8.0, 2.4, 0.35)

[sub_resource type="BoxMesh" id="Mesh_LowerPlanks"]
material = SubResource("Mat_FencePlanks")
size = Vector3(8.0, 1.6, 0.2)

[sub_resource type="BoxMesh" id="Mesh_UpperLattice"]
material = SubResource("Mat_TopLattice")
size = Vector3(8.0, 0.8, 0.16)

[sub_resource type="BoxMesh" id="Mesh_Post"]
material = SubResource("Mat_FencePlanks")
size = Vector3(0.3, 2.5, 0.3)

[node name="BGMI_PerimeterFence" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.2, 0)
shape = SubResource("Col_Fence")

[node name="LowerPlanks" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 0)
mesh = SubResource("Mesh_LowerPlanks")

[node name="UpperLattice" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.0, 0)
mesh = SubResource("Mesh_UpperLattice")

[node name="PostLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4.0, 1.25, 0)
mesh = SubResource("Mesh_Post")

[node name="PostMid" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.25, 0)
mesh = SubResource("Mesh_Post")

[node name="PostRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4.0, 1.25, 0)
mesh = SubResource("Mesh_Post")
"""

with open(os.path.join(PROPS_DIR, "bgmi_perimeter_fence.tscn"), "w") as f:
    f.write(FENCE_TSCN)
print("Saved 1:1 photorealistic bgmi_perimeter_fence.tscn")

# =============================================================================
# 6. BGMI TRAIN FREIGHT CAR (1:1 with frame_28_112s.jpg & frame_35_140s.jpg)
# =============================================================================
# Realistic railway wagon with corrugated yellow/tan paint, ladder, and roof catwalk
# =============================================================================

TRAIN_CAR_TSCN = """[gd_scene load_steps=9 format=3 uid="uid://bgmi_train_car_002"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_car_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_car_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_car_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_CarBody"]
albedo_color = Color(0.82, 0.72, 0.48, 1)
albedo_texture = ExtResource("1_car_diff")
normal_enabled = true
normal_texture = ExtResource("2_car_norm")
roughness_texture = ExtResource("3_car_rough")
roughness = 0.65
metallic = 0.5
uv1_scale = Vector3(3, 1.2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_RoofCatwalk"]
albedo_color = Color(0.28, 0.28, 0.26, 1)
metallic = 0.85
roughness = 0.4

[sub_resource type="BoxShape3D" id="Col_Boxcar"]
size = Vector3(14.0, 3.8, 3.2)

[sub_resource type="BoxMesh" id="Mesh_CarBody"]
material = SubResource("Mat_CarBody")
size = Vector3(14.0, 3.2, 3.2)

[sub_resource type="BoxMesh" id="Mesh_RoofCatwalk"]
material = SubResource("Mat_RoofCatwalk")
size = Vector3(13.8, 0.15, 1.2)

[sub_resource type="CylinderMesh" id="Mesh_Wheel"]
material = SubResource("Mat_RoofCatwalk")
top_radius = 0.45
bottom_radius = 0.45
height = 0.25
radial_segments = 14

[node name="BGMI_TrainBoxcar" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.9, 0)
shape = SubResource("Col_Boxcar")

[node name="CarBody" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.15, 0)
mesh = SubResource("Mesh_CarBody")

[node name="RoofCatwalk" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.82, 0)
mesh = SubResource("Mesh_RoofCatwalk")

# Wheel Trucks
[node name="WheelFL" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -4.8, 0.45, 1.45)
mesh = SubResource("Mesh_Wheel")

[node name="WheelFR" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -4.8, 0.45, -1.45)
mesh = SubResource("Mesh_Wheel")

[node name="WheelBL" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 4.8, 0.45, 1.45)
mesh = SubResource("Mesh_Wheel")

[node name="WheelBR" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 4.8, 0.45, -1.45)
mesh = SubResource("Mesh_Wheel")
"""

with open(os.path.join(PROPS_DIR, "bgmi_train_boxcar.tscn"), "w") as f:
    f.write(TRAIN_CAR_TSCN)
print("Saved 1:1 photorealistic bgmi_train_boxcar.tscn")

print("ALL UPGRADED BGMI ARCHITECTURAL PROPS GENERATED!")
