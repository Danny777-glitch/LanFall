import os

PROPS_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps\warehouse\props"
MAPS_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps"

# =============================================================================
# 1. PINE TREE (Realistic Alpha-Scissor 8-way Crossed Foliage with PBR Bark)
# =============================================================================
PINE_TREE_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://realistic_pine_tree_003"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="1_bark_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="2_bark_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_rough_1k.jpg" id="3_bark_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pine_foliage.png" id="4_foliage"]

[sub_resource type="StandardMaterial3D" id="Mat_TrunkBark"]
albedo_texture = ExtResource("1_bark_diff")
normal_enabled = true
normal_texture = ExtResource("2_bark_norm")
roughness_texture = ExtResource("3_bark_rough")
roughness = 0.85
uv1_scale = Vector3(1, 4, 1)

[sub_resource type="StandardMaterial3D" id="Mat_PineNeedles"]
transparency = 2
alpha_scissor_threshold = 0.3
cull_mode = 0
albedo_color = Color(0.24, 0.38, 0.22, 1)
albedo_texture = ExtResource("4_foliage")
roughness = 0.7
uv1_scale = Vector3(2, 2, 2)

[sub_resource type="CylinderMesh" id="Mesh_Trunk"]
material = SubResource("Mat_TrunkBark")
top_radius = 0.18
bottom_radius = 0.42
height = 9.0
radial_segments = 12

[sub_resource type="QuadMesh" id="Mesh_BranchQuad"]
material = SubResource("Mat_PineNeedles")
size = Vector2(5.4, 6.8)

[sub_resource type="CylinderShape3D" id="Col_Trunk"]
height = 9.0
radius = 0.42

[node name="PineTree" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.5, 0)
shape = SubResource("Col_Trunk")

[node name="Trunk" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.5, 0)
mesh = SubResource("Mesh_Trunk")

[node name="Branch0" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")

[node name="Branch22" type="MeshInstance3D" parent="."]
transform = Transform3D(0.92388, 0, 0.382683, 0, 1, 0, -0.382683, 0, 0.92388, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")

[node name="Branch45" type="MeshInstance3D" parent="."]
transform = Transform3D(0.707107, 0, 0.707107, 0, 1, 0, -0.707107, 0, 0.707107, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")

[node name="Branch67" type="MeshInstance3D" parent="."]
transform = Transform3D(0.382683, 0, 0.92388, 0, 1, 0, -0.92388, 0, 0.382683, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")

[node name="Branch90" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")

[node name="Branch112" type="MeshInstance3D" parent="."]
transform = Transform3D(-0.382683, 0, 0.92388, 0, 1, 0, -0.92388, 0, -0.382683, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")

[node name="Branch135" type="MeshInstance3D" parent="."]
transform = Transform3D(-0.707107, 0, 0.707107, 0, 1, 0, -0.707107, 0, -0.707107, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")

[node name="Branch157" type="MeshInstance3D" parent="."]
transform = Transform3D(-0.92388, 0, 0.382683, 0, 1, 0, -0.382683, 0, -0.92388, 0, 5.2, 0)
mesh = SubResource("Mesh_BranchQuad")
"""

with open(os.path.join(PROPS_DIR, "pine_tree.tscn"), "w") as f:
    f.write(PINE_TREE_TSCN)
print("Saved 1:1 photorealistic pine_tree.tscn")

# =============================================================================
# 2. BGMI CRATE STACK (1:1 with frame_18_72s.jpg - ZERO FLOATING)
# =============================================================================
CRATE_STACK_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://bgmi_crate_stack_003"]

[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_albedo.png" id="1_crate_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_normal.png" id="2_crate_norm"]

[sub_resource type="StandardMaterial3D" id="Mat_WoodCrate"]
albedo_texture = ExtResource("1_crate_diff")
normal_enabled = true
normal_texture = ExtResource("2_crate_norm")
roughness = 0.78

[sub_resource type="BoxShape3D" id="Col_CrateStack"]
size = Vector3(2.8, 1.7, 1.2)

[sub_resource type="BoxMesh" id="Mesh_CrateSingle"]
material = SubResource("Mat_WoodCrate")
size = Vector3(1.36, 0.85, 1.16)

[node name="BGMI_CrateStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.85, 0)
shape = SubResource("Col_CrateStack")

# Bottom Crates (y=0.425 - bottom at y=0, top at y=0.85)
[node name="CrateBottomLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.7, 0.425, 0)
mesh = SubResource("Mesh_CrateSingle")

[node name="CrateBottomRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.7, 0.425, 0)
mesh = SubResource("Mesh_CrateSingle")

# Top Crates (y=1.275 - bottom at y=0.85, top at y=1.70 - FLUSH RESTING ON BOTTOM CRATES)
[node name="CrateTopLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.7, 1.275, 0)
mesh = SubResource("Mesh_CrateSingle")

[node name="CrateTopRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.7, 1.275, 0)
mesh = SubResource("Mesh_CrateSingle")
"""

with open(os.path.join(PROPS_DIR, "bgmi_crate_stack.tscn"), "w") as f:
    f.write(CRATE_STACK_TSCN)
print("Saved 1:1 photorealistic bgmi_crate_stack.tscn")

# =============================================================================
# 3. BGMI CONTAINER WITH BOARDING RAMP (1:1 with frame_28_112s.jpg)
# =============================================================================
CONTAINER_RAMP_TSCN = """[gd_scene load_steps=10 format=3 uid="uid://bgmi_container_ramp_003"]

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
size = Vector3(6.5, 2.8, 2.6)

[sub_resource type="BoxShape3D" id="Col_Ramp"]
size = Vector3(2.0, 0.2, 6.26)

[sub_resource type="BoxMesh" id="Mesh_ContainerBody"]
material = SubResource("Mat_Container")
size = Vector3(6.5, 2.8, 2.6)

[sub_resource type="BoxMesh" id="Mesh_CornerPost"]
material = SubResource("Mat_ContainerTrims")
size = Vector3(0.22, 2.85, 0.22)

[sub_resource type="BoxMesh" id="Mesh_RampBed"]
material = SubResource("Mat_RampWood")
size = Vector3(2.0, 0.2, 6.26)

[sub_resource type="BoxMesh" id="Mesh_RampCleat"]
material = SubResource("Mat_RampWood")
size = Vector3(1.9, 0.08, 0.12)

[sub_resource type="BoxMesh" id="Mesh_RoofCoverCrate"]
material = SubResource("Mat_CrateRoof")
size = Vector3(1.4, 0.85, 1.1)

[node name="BGMI_ContainerRamp" type="StaticBody3D"]

[node name="ColContainer" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, 0)
shape = SubResource("Col_Container")

[node name="ContainerMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, 0)
mesh = SubResource("Mesh_ContainerBody")

[node name="Post1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.15, 1.4, -1.2)
mesh = SubResource("Mesh_CornerPost")

[node name="Post2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.15, 1.4, -1.2)
mesh = SubResource("Mesh_CornerPost")

[node name="Post3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.15, 1.4, 1.2)
mesh = SubResource("Mesh_CornerPost")

[node name="Post4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.15, 1.4, 1.2)
mesh = SubResource("Mesh_CornerPost")

# Boarding Ramp: Runs from z=4.1 to z=-1.5, ascends from ground y=0 to container roof y=2.8.
[node name="ColRamp" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.4, 1.3)
shape = SubResource("Col_Ramp")

[node name="RampBed" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.4, 1.3)
mesh = SubResource("Mesh_RampBed")

[node name="Cleat1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 0.5, 3.1)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 0.95, 2.2)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.4, 1.3)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 1.85, 0.4)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat5" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 2.3, -0.5)
mesh = SubResource("Mesh_RampCleat")

[node name="Cleat6" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.894427, 0.447214, 0, -0.447214, 0.894427, 2.2, 2.7, -1.4)
mesh = SubResource("Mesh_RampCleat")

# Roof Sniper Cover Crate (Resting directly on roof at y=2.8)
[node name="RoofSniperCover" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.8, 3.225, 0)
mesh = SubResource("Mesh_RoofCoverCrate")
"""

with open(os.path.join(PROPS_DIR, "bgmi_container_ramp.tscn"), "w") as f:
    f.write(CONTAINER_RAMP_TSCN)
print("Saved 1:1 photorealistic bgmi_container_ramp.tscn")

# =============================================================================
# 4. BGMI SPAWN SHED COMPOUND (1:1 with frame_00_0s.jpg & frame_04_16s.jpg)
# =============================================================================
# Open-front covered compound with timber posts, overhead roof, back wall, weapon tables
# =============================================================================
SPAWN_SHED_TSCN = """[gd_scene load_steps=18 format=3 uid="uid://bgmi_spawn_compound_003"]

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
albedo_color = Color(0.48, 0.40, 0.32, 1)
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

[sub_resource type="BoxMesh" id="Mesh_HeavyPost"]
material = SubResource("Mat_TimberPosts")
size = Vector3(0.48, 4.6, 0.48)

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

# Front Timber Posts with wide unobstructed 6m center view
[node name="Post1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10.5, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.2, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.2, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

[node name="Post4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10.5, 2.3, -3.4)
mesh = SubResource("Mesh_HeavyPost")

# Overhead Heavy Corrugated Slate Pitch Roof
[node name="RoofMain" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.984808, 0.173648, 0, -0.173648, 0.984808, 0, 4.8, 0.2)
mesh = SubResource("Mesh_RoofSlab")

[node name="FasciaBeamFront" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.4, -3.6)
mesh = SubResource("Mesh_FasciaBeam")

# Left & Right Weapon Tables
[node name="TableLeft" parent="." instance=ExtResource("10_table")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, -6.5, 0.3, 1.2)

[node name="AmmoLeft1" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -7.2, 1.45, 1.1)

[node name="AmmoLeft2" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.1, 0, 0.4, 0, 1.2, 0, -0.4, 0, 1.1, -6.0, 1.45, 1.1)

[node name="RifleLeft" parent="." instance=ExtResource("12_rifle")]
transform = Transform3D(0.9, 0, 0, 0, 0, -0.9, 0, 0.9, 0, -6.6, 1.48, 1.2)

[node name="TableRight" parent="." instance=ExtResource("10_table")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, 6.5, 0.3, 1.2)

[node name="AmmoRight1" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 6.0, 1.45, 1.1)

[node name="AmmoRight2" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.1, 0, -0.4, 0, 1.2, 0, 0.4, 0, 1.1, 7.2, 1.45, 1.1)

[node name="SniperRight" parent="." instance=ExtResource("13_sniper")]
transform = Transform3D(0.9, 0, 0, 0, 0, -0.9, 0, 0.9, 0, 6.6, 1.48, 1.2)

# Firewood logs stack on the left
[node name="FirewoodLog1" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, -9.0, 0.45, 1.5)
mesh = SubResource("Mesh_FirewoodLog")

[node name="FirewoodLog2" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, -9.0, 0.45, 1.9)
mesh = SubResource("Mesh_FirewoodLog")

[node name="FirewoodLog3" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, -9.0, 0.8, 1.7)
mesh = SubResource("Mesh_FirewoodLog")

# Blue tarp covered cargo pile on the right
[node name="TarpCrates" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 9.0, 1.1, 1.5)
mesh = SubResource("Mesh_TarpCoveredCrates")
"""

with open(os.path.join(PROPS_DIR, "bgmi_spawn_sheds.tscn"), "w") as f:
    f.write(SPAWN_SHED_TSCN)
print("Saved 1:1 photorealistic bgmi_spawn_sheds.tscn")

# =============================================================================
# 5. ASSEMBLE MAP TEMPLATE
# =============================================================================
MAP_TSCN_TEMPLATE = """[gd_scene load_steps=22 format=3 uid="uid://bgmi_tdm_quality_map_003"]

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
fog_enabled = false

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
light_color = Color(1.0, 0.96, 0.88, 1)
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
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6.5, 0, 24.5)

[node name="TrainCar_South" parent="SouthApproach" instance=ExtResource("12_boxcar")]
transform = Transform3D(0.965926, 0, 0.258819, 0, 1, 0, -0.258819, 0, 0.965926, 7.5, 0, 27.5)

[node name="Barrier_SouthEntry1" parent="SouthApproach" instance=ExtResource("16_barrier")]
transform = Transform3D(0.984808, 0, -0.173648, 0, 1, 0, 0.173648, 0, 0.984808, -1.8, 0, 20.0)

[node name="Barrier_SouthEntry2" parent="SouthApproach" instance=ExtResource("16_barrier")]
transform = Transform3D(0.984808, 0, 0.173648, 0, 1, 0, -0.173648, 0, 0.984808, 1.8, 0, 20.0)

[node name="NorthApproach" type="Node3D" parent="."]

[node name="SniperContainerRamp_North" parent="NorthApproach" instance=ExtResource("13_container_ramp")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 6.5, 0, -24.5)

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

# Write test_map.tscn
with open(os.path.join(MAPS_DIR, "test_map.tscn"), "w", encoding="utf-8") as f:
    f.write(MAP_TSCN_TEMPLATE.replace("{SCRIPT_PATH}", "res://scenes/maps/test_map.gd"))
print("Saved scenes/maps/test_map.tscn")

# Write warehouse_map.tscn
with open(os.path.join(MAPS_DIR, "warehouse", "warehouse_map.tscn"), "w", encoding="utf-8") as f:
    f.write(MAP_TSCN_TEMPLATE.replace("{SCRIPT_PATH}", "res://scenes/maps/warehouse/warehouse_map.gd"))
print("Saved scenes/maps/warehouse/warehouse_map.tscn")
