import os

PROPS_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps\warehouse\props"
os.makedirs(PROPS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. BGMI SPAWN SHEDS (Twin wooden sheds with 3D tables, ammo boxes, & weapons)
# -----------------------------------------------------------------------------
SPAWN_SHEDS_TSCN = """[gd_scene load_steps=11 format=3 uid="uid://bgmi_spawn_sheds_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_roof_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_roof_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_roof_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="6_wood_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_fence_lattice_albedo.png" id="7_lattice"]
[ext_resource type="PackedScene" path="res://assets/models/wooden_table_02/wooden_table_02.gltf" id="8_table_model"]
[ext_resource type="PackedScene" path="res://assets/models/ammo_box/ammo_box.gltf" id="9_ammobox_model"]
[ext_resource type="PackedScene" path="res://scenes/weapons/tactical_rifle.tscn" id="10_rifle_prop"]

[sub_resource type="StandardMaterial3D" id="Mat_ShedRoof"]
albedo_color = Color(0.42, 0.48, 0.55, 1)
albedo_texture = ExtResource("1_roof_diff")
normal_enabled = true
normal_texture = ExtResource("2_roof_norm")
roughness_texture = ExtResource("3_roof_rough")
roughness = 0.65
metallic = 0.5
uv1_scale = Vector3(3, 3, 3)

[sub_resource type="StandardMaterial3D" id="Mat_TimberWood"]
albedo_texture = ExtResource("4_wood_diff")
normal_enabled = true
normal_texture = ExtResource("5_wood_norm")
roughness_texture = ExtResource("6_wood_rough")
roughness = 0.8
uv1_scale = Vector3(1, 4, 1)

[sub_resource type="StandardMaterial3D" id="Mat_BackWall"]
albedo_texture = ExtResource("7_lattice")
roughness = 0.85
uv1_scale = Vector3(3, 1, 1)

[sub_resource type="BoxShape3D" id="Col_BackWall"]
size = Vector3(22.0, 4.5, 0.4)

[sub_resource type="BoxShape3D" id="Col_ShedFloor"]
size = Vector3(22.0, 0.3, 7.0)

[sub_resource type="BoxMesh" id="Mesh_Post"]
material = SubResource("Mat_TimberWood")
size = Vector3(0.35, 3.8, 0.35)

[sub_resource type="BoxMesh" id="Mesh_RoofSlab"]
material = SubResource("Mat_ShedRoof")
size = Vector3(8.5, 0.25, 6.2)

[node name="BGMI_SpawnSheds" type="StaticBody3D"]

[node name="ColBack" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.25, 2.8)
shape = SubResource("Col_BackWall")

[node name="ColFloor" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.15, 0)
shape = SubResource("Col_ShedFloor")

[node name="FloorDeck" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.15, 0)
mesh = SubResource("Col_ShedFloor")

[node name="BackWallMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.25, 2.8)
mesh = SubResource("Col_BackWall")

[node name="RoofLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.939693, 0.34202, 0, -0.34202, 0.939693, -5.2, 4.0, 0.2)
mesh = SubResource("Mesh_RoofSlab")

[node name="PostL1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -9.0, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="PostL2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.4, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="TableLeft" parent="." instance=ExtResource("8_table_model")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, -5.2, 0.3, 0.5)

[node name="AmmoLeft1" parent="." instance=ExtResource("9_ammobox_model")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -5.7, 1.35, 0.4)

[node name="AmmoLeft2" parent="." instance=ExtResource("9_ammobox_model")]
transform = Transform3D(1.1, 0, 0.5, 0, 1.2, 0, -0.5, 0, 1.1, -4.7, 1.35, 0.4)

[node name="RifleLeft" parent="." instance=ExtResource("10_rifle_prop")]
transform = Transform3D(0.9, 0, 0, 0, 0, -0.9, 0, 0.9, 0, -5.2, 1.38, 0.5)

[node name="RoofRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.939693, 0.34202, 0, -0.34202, 0.939693, 5.2, 4.0, 0.2)
mesh = SubResource("Mesh_RoofSlab")

[node name="PostR1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 1.4, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="PostR2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 9.0, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="TableRight" parent="." instance=ExtResource("8_table_model")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, 5.2, 0.3, 0.5)

[node name="AmmoRight1" parent="." instance=ExtResource("9_ammobox_model")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 4.7, 1.35, 0.4)

[node name="AmmoRight2" parent="." instance=ExtResource("9_ammobox_model")]
transform = Transform3D(1.1, 0, -0.5, 0, 1.2, 0, 0.5, 0, 1.1, 5.7, 1.35, 0.4)

[node name="RifleRight" parent="." instance=ExtResource("10_rifle_prop")]
transform = Transform3D(0.9, 0, 0, 0, 0, -0.9, 0, 0.9, 0, 5.2, 1.38, 0.5)
"""

with open(os.path.join(PROPS_DIR, "bgmi_spawn_sheds.tscn"), "w") as f:
    f.write(SPAWN_SHEDS_TSCN)
print("Saved upgraded bgmi_spawn_sheds.tscn")

# -----------------------------------------------------------------------------
# 2. BGMI MAIN WAREHOUSE (Central Building with PBR corrugated iron & concrete)
# -----------------------------------------------------------------------------
MAIN_WAREHOUSE_TSCN = """[gd_scene load_steps=18 format=3 uid="uid://bgmi_warehouse_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_siding_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_siding_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_siding_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/dirty_concrete_diff_1k.jpg" id="4_concrete_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/dirty_concrete_nor_gl_1k.jpg" id="5_concrete_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/dirty_concrete_rough_1k.jpg" id="6_concrete_rough"]
[ext_resource type="PackedScene" path="res://assets/models/wooden_military_crate/wooden_military_crate.gltf" id="7_crate_model"]
[ext_resource type="PackedScene" path="res://assets/models/old_military_crate/old_military_crate.gltf" id="8_oldcrate_model"]
[ext_resource type="PackedScene" path="res://assets/models/Barrel_01/Barrel_01.gltf" id="9_barrel_model"]
[ext_resource type="PackedScene" path="res://assets/models/hanging_industrial_lamp/hanging_industrial_lamp.gltf" id="10_lamp_model"]

[sub_resource type="StandardMaterial3D" id="Mat_WarehouseSiding"]
albedo_texture = ExtResource("1_siding_diff")
normal_enabled = true
normal_texture = ExtResource("2_siding_norm")
roughness_texture = ExtResource("3_siding_rough")
roughness = 0.6
metallic = 0.7
uv1_scale = Vector3(0.35, 0.35, 0.35)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_Floor"]
albedo_texture = ExtResource("4_concrete_diff")
normal_enabled = true
normal_texture = ExtResource("5_concrete_norm")
roughness_texture = ExtResource("6_concrete_rough")
roughness = 0.8
uv1_scale = Vector3(0.2, 0.2, 0.2)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_SteelBeams"]
albedo_color = Color(0.2, 0.22, 0.26, 1)
metallic = 0.85
roughness = 0.35

[sub_resource type="StandardMaterial3D" id="Mat_MetalRoof"]
albedo_color = Color(0.48, 0.52, 0.56, 1)
albedo_texture = ExtResource("1_siding_diff")
normal_enabled = true
normal_texture = ExtResource("2_siding_norm")
roughness_texture = ExtResource("3_siding_rough")
metallic = 0.75
roughness = 0.5
uv1_scale = Vector3(0.4, 0.4, 0.4)
uv1_triplanar = true

[sub_resource type="BoxMesh" id="Mesh_InteriorFloor"]
material = SubResource("Mat_Floor")
size = Vector3(16.2, 0.05, 28.2)

[sub_resource type="BoxMesh" id="Mesh_EndWallSegment"]
material = SubResource("Mat_WarehouseSiding")
size = Vector3(5.5, 7.0, 0.4)

[sub_resource type="BoxMesh" id="Mesh_EndWallHeader"]
material = SubResource("Mat_WarehouseSiding")
size = Vector3(5.2, 2.8, 0.4)

[sub_resource type="BoxMesh" id="Mesh_SideWallSegment"]
material = SubResource("Mat_WarehouseSiding")
size = Vector3(0.4, 7.0, 12.0)

[sub_resource type="BoxMesh" id="Mesh_SideWallHeader"]
material = SubResource("Mat_WarehouseSiding")
size = Vector3(0.4, 3.4, 4.2)

[sub_resource type="BoxMesh" id="Mesh_SteelColumn"]
material = SubResource("Mat_SteelBeams")
size = Vector3(0.45, 7.2, 0.45)

[sub_resource type="BoxMesh" id="Mesh_RoofSlope"]
material = SubResource("Mat_MetalRoof")
size = Vector3(9.2, 0.3, 29.0)

[sub_resource type="BoxMesh" id="Mesh_RoofTrussBeam"]
material = SubResource("Mat_SteelBeams")
size = Vector3(16.0, 0.3, 0.3)

[sub_resource type="BoxShape3D" id="BoxShape3D_EndWallSegment"]
size = Vector3(5.5, 7.0, 0.4)

[sub_resource type="BoxShape3D" id="BoxShape3D_SideWallSegment"]
size = Vector3(0.4, 7.0, 12.0)

[node name="BGMI_TDM_Warehouse" type="StaticBody3D"]

[node name="InteriorFloor" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.02, 0)
mesh = SubResource("Mesh_InteriorFloor")

[node name="Col_SouthLeft" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.25, 3.5, 14.0)
shape = SubResource("BoxShape3D_EndWallSegment")

[node name="Mesh_SouthLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.25, 3.5, 14.0)
mesh = SubResource("Mesh_EndWallSegment")

[node name="Col_SouthRight" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.25, 3.5, 14.0)
shape = SubResource("BoxShape3D_EndWallSegment")

[node name="Mesh_SouthRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.25, 3.5, 14.0)
mesh = SubResource("Mesh_EndWallSegment")

[node name="Mesh_SouthHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.6, 14.0)
mesh = SubResource("Mesh_EndWallHeader")

[node name="Col_NorthLeft" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.25, 3.5, -14.0)
shape = SubResource("BoxShape3D_EndWallSegment")

[node name="Mesh_NorthLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.25, 3.5, -14.0)
mesh = SubResource("Mesh_EndWallSegment")

[node name="Col_NorthRight" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.25, 3.5, -14.0)
shape = SubResource("BoxShape3D_EndWallSegment")

[node name="Mesh_NorthRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.25, 3.5, -14.0)
mesh = SubResource("Mesh_EndWallSegment")

[node name="Mesh_NorthHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.6, -14.0)
mesh = SubResource("Mesh_EndWallHeader")

[node name="Col_WestNorth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 3.5, -8.0)
shape = SubResource("BoxShape3D_SideWallSegment")

[node name="Mesh_WestNorth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 3.5, -8.0)
mesh = SubResource("Mesh_SideWallSegment")

[node name="Col_WestSouth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 3.5, 8.0)
shape = SubResource("BoxShape3D_SideWallSegment")

[node name="Mesh_WestSouth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 3.5, 8.0)
mesh = SubResource("Mesh_SideWallSegment")

[node name="Mesh_WestHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 5.3, 0)
mesh = SubResource("Mesh_SideWallHeader")

[node name="Col_EastNorth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 3.5, -8.0)
shape = SubResource("BoxShape3D_SideWallSegment")

[node name="Mesh_EastNorth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 3.5, -8.0)
mesh = SubResource("Mesh_SideWallSegment")

[node name="Col_EastSouth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 3.5, 8.0)
shape = SubResource("BoxShape3D_SideWallSegment")

[node name="Mesh_EastSouth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 3.5, 8.0)
mesh = SubResource("Mesh_SideWallSegment")

[node name="Mesh_EastHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 5.3, 0)
mesh = SubResource("Mesh_SideWallHeader")

[node name="Col_CornerSW" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.1, 3.6, 14.1)
mesh = SubResource("Mesh_SteelColumn")

[node name="Col_CornerSE" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.1, 3.6, 14.1)
mesh = SubResource("Mesh_SteelColumn")

[node name="Col_CornerNW" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.1, 3.6, -14.1)
mesh = SubResource("Mesh_SteelColumn")

[node name="Col_CornerNE" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.1, 3.6, -14.1)
mesh = SubResource("Mesh_SteelColumn")

[node name="RoofSlopeWest" type="MeshInstance3D" parent="."]
transform = Transform3D(0.978148, -0.207912, 0, 0.207912, 0.978148, 0, 0, 0, 1, -4.1, 7.9, 0)
mesh = SubResource("Mesh_RoofSlope")

[node name="RoofSlopeEast" type="MeshInstance3D" parent="."]
transform = Transform3D(0.978148, 0.207912, 0, -0.207912, 0.978148, 0, 0, 0, 1, 4.1, 7.9, 0)
mesh = SubResource("Mesh_RoofSlope")

[node name="TrussBeamMid" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6.8, 0)
mesh = SubResource("Mesh_RoofTrussBeam")

[node name="WarehouseLampMid" parent="." instance=ExtResource("10_lamp_model")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, 0, 6.5, 0)

[node name="LightMid" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.5, 0)
light_color = Color(1, 0.94, 0.82, 1)
light_energy = 2.4
omni_range = 18.0
shadow_enabled = true

[node name="WarehouseLampNorth" parent="." instance=ExtResource("10_lamp_model")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, 0, 6.5, -8.0)

[node name="LightNorth" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.5, -8.0)
light_color = Color(1, 0.94, 0.82, 1)
light_energy = 2.0
omni_range = 14.0

[node name="WarehouseLampSouth" parent="." instance=ExtResource("10_lamp_model")]
transform = Transform3D(1.5, 0, 0, 0, 1.5, 0, 0, 0, 1.5, 0, 6.5, 8.0)

[node name="LightSouth" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.5, 8.0)
light_color = Color(1, 0.94, 0.82, 1)
light_energy = 2.0
omni_range = 14.0

[node name="CrateStackL1" parent="." instance=ExtResource("7_crate_model")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -4.2, 0, -2.5)

[node name="CrateStackL2" parent="." instance=ExtResource("8_oldcrate_model")]
transform = Transform3D(1.1, 0, 0.4, 0, 1.2, 0, -0.4, 0, 1.1, -4.2, 1.1, -2.5)

[node name="BarrelL1" parent="." instance=ExtResource("9_barrel_model")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, -5.5, 0, -2.2)

[node name="CrateStackR1" parent="." instance=ExtResource("7_crate_model")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 4.2, 0, 2.5)

[node name="CrateStackR2" parent="." instance=ExtResource("8_oldcrate_model")]
transform = Transform3D(1.1, 0, -0.3, 0, 1.2, 0, 0.3, 0, 1.1, 4.2, 1.1, 2.5)

[node name="BarrelR1" parent="." instance=ExtResource("9_barrel_model")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, 5.5, 0, 2.2)
"""

with open(os.path.join(PROPS_DIR, "bgmi_tdm_warehouse.tscn"), "w") as f:
    f.write(MAIN_WAREHOUSE_TSCN)
print("Saved upgraded bgmi_tdm_warehouse.tscn")

# -----------------------------------------------------------------------------
# 3. BGMI CONTAINER WITH SNIPER BOARDING RAMP (PBR Container & Wood Planks)
# -----------------------------------------------------------------------------
CONTAINER_RAMP_TSCN = """[gd_scene load_steps=10 format=3 uid="uid://bgmi_container_ramp_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_diff_1k.jpg" id="1_cont_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_nor_gl_1k.jpg" id="2_cont_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_rough_1k.jpg" id="3_cont_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="6_wood_rough"]
[ext_resource type="PackedScene" path="res://assets/models/old_military_crate/old_military_crate.gltf" id="7_crate_cover"]

[sub_resource type="StandardMaterial3D" id="Mat_ContainerYellow"]
albedo_color = Color(0.95, 0.76, 0.18, 1)
albedo_texture = ExtResource("1_cont_diff")
normal_enabled = true
normal_texture = ExtResource("2_cont_norm")
roughness_texture = ExtResource("3_cont_rough")
roughness = 0.55
metallic = 0.65
uv1_scale = Vector3(2.5, 1, 1)

[sub_resource type="StandardMaterial3D" id="Mat_RampWood"]
albedo_texture = ExtResource("4_wood_diff")
normal_enabled = true
normal_texture = ExtResource("5_wood_norm")
roughness_texture = ExtResource("6_wood_rough")
roughness = 0.8
uv1_scale = Vector3(1, 4, 1)

[sub_resource type="BoxShape3D" id="Col_Container"]
size = Vector3(6.5, 2.7, 2.6)

[sub_resource type="BoxMesh" id="Mesh_Container"]
material = SubResource("Mat_ContainerYellow")
size = Vector3(6.5, 2.7, 2.6)

[sub_resource type="BoxShape3D" id="Col_Ramp"]
size = Vector3(1.8, 0.25, 5.2)

[sub_resource type="BoxMesh" id="Mesh_Ramp"]
material = SubResource("Mat_RampWood")
size = Vector3(1.8, 0.25, 5.2)

[node name="BGMI_ContainerRamp" type="StaticBody3D"]

[node name="ContainerCol" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.35, 0)
shape = SubResource("Col_Container")

[node name="ContainerMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.35, 0)
mesh = SubResource("Mesh_Container")

[node name="RampCol" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.866025, 0.5, 0, -0.5, 0.866025, 1.6, 1.35, 2.8)
shape = SubResource("Col_Ramp")

[node name="RampMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.866025, 0.5, 0, -0.5, 0.866025, 1.6, 1.35, 2.8)
mesh = SubResource("Mesh_Ramp")

[node name="RoofSniperCover" parent="." instance=ExtResource("7_crate_cover")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, -1.8, 2.7, 0)
"""

with open(os.path.join(PROPS_DIR, "bgmi_container_ramp.tscn"), "w") as f:
    f.write(CONTAINER_RAMP_TSCN)
print("Saved upgraded bgmi_container_ramp.tscn")

# -----------------------------------------------------------------------------
# 4. BGMI TIMBER YARD LOGS (PBR Bark & Wood Planks)
# -----------------------------------------------------------------------------
TIMBER_LOGS_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_timber_logs_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="1_bark_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="2_bark_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_rough_1k.jpg" id="3_bark_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"]

[sub_resource type="StandardMaterial3D" id="Mat_Logs"]
albedo_texture = ExtResource("1_bark_diff")
normal_enabled = true
normal_texture = ExtResource("2_bark_norm")
roughness_texture = ExtResource("3_bark_rough")
roughness = 0.85
uv1_scale = Vector3(1, 3, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Cradle"]
albedo_texture = ExtResource("4_wood_diff")
normal_enabled = true
normal_texture = ExtResource("5_wood_norm")
roughness = 0.8
uv1_scale = Vector3(1, 3, 1)

[sub_resource type="BoxShape3D" id="Col_LogStack"]
size = Vector3(6.2, 2.2, 2.4)

[sub_resource type="CylinderMesh" id="Mesh_SingleLog"]
material = SubResource("Mat_Logs")
top_radius = 0.28
bottom_radius = 0.28
height = 6.0
radial_segments = 14

[sub_resource type="BoxMesh" id="Mesh_CradlePost"]
material = SubResource("Mat_Cradle")
size = Vector3(0.25, 2.4, 0.25)

[node name="BGMI_TimberLogStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
shape = SubResource("Col_LogStack")

[node name="PostFrontL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.6, 1.2, 1.05)
mesh = SubResource("Mesh_CradlePost")

[node name="PostFrontR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.6, 1.2, 1.05)
mesh = SubResource("Mesh_CradlePost")

[node name="PostBackL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.6, 1.2, -1.05)
mesh = SubResource("Mesh_CradlePost")

[node name="PostBackR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.6, 1.2, -1.05)
mesh = SubResource("Mesh_CradlePost")

[node name="Log1" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.35, -0.6)
mesh = SubResource("Mesh_SingleLog")

[node name="Log2" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.35, 0.0)
mesh = SubResource("Mesh_SingleLog")

[node name="Log3" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.35, 0.6)
mesh = SubResource("Mesh_SingleLog")

[node name="Log4" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.9, -0.3)
mesh = SubResource("Mesh_SingleLog")

[node name="Log5" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.9, 0.3)
mesh = SubResource("Mesh_SingleLog")

[node name="Log6" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 1.45, 0.0)
mesh = SubResource("Mesh_SingleLog")
"""

with open(os.path.join(PROPS_DIR, "bgmi_timber_logs.tscn"), "w") as f:
    f.write(TIMBER_LOGS_TSCN)
print("Saved upgraded bgmi_timber_logs.tscn")

# -----------------------------------------------------------------------------
# 5. BGMI WOODEN PERGOLA (PBR Wood Planks & Architectural Rafters)
# -----------------------------------------------------------------------------
PERGOLA_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_pergola_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="1_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="2_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="3_wood_rough"]
[ext_resource type="PackedScene" path="res://assets/models/wooden_military_crate/wooden_military_crate.gltf" id="4_crate_seat"]

[sub_resource type="StandardMaterial3D" id="Mat_PergolaTimber"]
albedo_texture = ExtResource("1_wood_diff")
normal_enabled = true
normal_texture = ExtResource("2_wood_norm")
roughness_texture = ExtResource("3_wood_rough")
roughness = 0.82
uv1_scale = Vector3(1, 3, 1)

[sub_resource type="BoxShape3D" id="Col_PergolaPost"]
size = Vector3(0.4, 3.8, 0.4)

[sub_resource type="BoxMesh" id="Mesh_Pillar"]
material = SubResource("Mat_PergolaTimber")
size = Vector3(0.4, 3.8, 0.4)

[sub_resource type="BoxMesh" id="Mesh_BeamMain"]
material = SubResource("Mat_PergolaTimber")
size = Vector3(6.5, 0.35, 0.3)

[sub_resource type="BoxMesh" id="Mesh_Rafter"]
material = SubResource("Mat_PergolaTimber")
size = Vector3(0.18, 0.25, 5.6)

[node name="BGMI_WoodenPergola" type="StaticBody3D"]

[node name="ColP1" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.6, 1.9, -2.2)
shape = SubResource("Col_PergolaPost")

[node name="MeshP1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.6, 1.9, -2.2)
mesh = SubResource("Mesh_Pillar")

[node name="ColP2" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.6, 1.9, -2.2)
shape = SubResource("Col_PergolaPost")

[node name="MeshP2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.6, 1.9, -2.2)
mesh = SubResource("Mesh_Pillar")

[node name="ColP3" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.6, 1.9, 2.2)
shape = SubResource("Col_PergolaPost")

[node name="MeshP3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.6, 1.9, 2.2)
mesh = SubResource("Mesh_Pillar")

[node name="ColP4" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.6, 1.9, 2.2)
shape = SubResource("Col_PergolaPost")

[node name="MeshP4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.6, 1.9, 2.2)
mesh = SubResource("Mesh_Pillar")

[node name="BeamNorth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.8, -2.2)
mesh = SubResource("Mesh_BeamMain")

[node name="BeamSouth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.8, 2.2)
mesh = SubResource("Mesh_BeamMain")

[node name="Rafter1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.5, 4.05, 0)
mesh = SubResource("Mesh_Rafter")

[node name="Rafter2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.25, 4.05, 0)
mesh = SubResource("Mesh_Rafter")

[node name="Rafter3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.05, 0)
mesh = SubResource("Mesh_Rafter")

[node name="Rafter4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 1.25, 4.05, 0)
mesh = SubResource("Mesh_Rafter")

[node name="Rafter5" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.5, 4.05, 0)
mesh = SubResource("Mesh_Rafter")

[node name="BenchCrate" parent="." instance=ExtResource("4_crate_seat")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, 0, 0, 0)
"""

with open(os.path.join(PROPS_DIR, "bgmi_wooden_pergola.tscn"), "w") as f:
    f.write(PERGOLA_TSCN)
print("Saved upgraded bgmi_wooden_pergola.tscn")

# -----------------------------------------------------------------------------
# 6. BGMI JERSEY BARRIER (PBR Chipped Concrete with Drainage Slots)
# -----------------------------------------------------------------------------
JERSEY_BARRIER_TSCN = """[gd_scene load_steps=7 format=3 uid="uid://bgmi_jersey_barrier_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_diff_1k.jpg" id="1_conc_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_nor_gl_1k.jpg" id="2_conc_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_rough_1k.jpg" id="3_conc_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_BarrierConcrete"]
albedo_texture = ExtResource("1_conc_diff")
normal_enabled = true
normal_texture = ExtResource("2_conc_norm")
roughness_texture = ExtResource("3_conc_rough")
roughness = 0.85
uv1_scale = Vector3(1.5, 1, 1)

[sub_resource type="BoxShape3D" id="Col_Barrier"]
size = Vector3(3.2, 1.15, 0.75)

[sub_resource type="BoxMesh" id="Mesh_Base"]
material = SubResource("Mat_BarrierConcrete")
size = Vector3(3.2, 0.45, 0.75)

[sub_resource type="BoxMesh" id="Mesh_TopStem"]
material = SubResource("Mat_BarrierConcrete")
size = Vector3(3.2, 0.7, 0.4)

[node name="BGMI_JerseyBarrier" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.58, 0)
shape = SubResource("Col_Barrier")

[node name="BaseWide" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.22, 0)
mesh = SubResource("Mesh_Base")

[node name="StemTop" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.78, 0)
mesh = SubResource("Mesh_TopStem")
"""

with open(os.path.join(PROPS_DIR, "bgmi_jersey_barrier.tscn"), "w") as f:
    f.write(JERSEY_BARRIER_TSCN)
print("Saved upgraded bgmi_jersey_barrier.tscn")

# -----------------------------------------------------------------------------
# 7. BGMI CRATE STACK (Built with 3D Scanned Military Crates)
# -----------------------------------------------------------------------------
CRATE_STACK_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://bgmi_crate_stack_pbr_001"]

[ext_resource type="PackedScene" path="res://assets/models/wooden_military_crate/wooden_military_crate.gltf" id="1_crate_scan"]
[ext_resource type="PackedScene" path="res://assets/models/old_military_crate/old_military_crate.gltf" id="2_oldcrate_scan"]

[sub_resource type="BoxShape3D" id="Col_StackBottom"]
size = Vector3(2.6, 1.1, 1.8)

[sub_resource type="BoxShape3D" id="Col_StackTop"]
size = Vector3(2.6, 1.1, 1.8)

[node name="BGMI_CrateStack" type="StaticBody3D"]

[node name="ColBottom" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.55, 0)
shape = SubResource("Col_StackBottom")

[node name="ColTop" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.65, 0)
shape = SubResource("Col_StackTop")

[node name="CrateBL" parent="." instance=ExtResource("1_crate_scan")]
transform = Transform3D(1.15, 0, 0, 0, 1.15, 0, 0, 0, 1.15, -0.65, 0, 0)

[node name="CrateBR" parent="." instance=ExtResource("2_oldcrate_scan")]
transform = Transform3D(1.15, 0, 0, 0, 1.15, 0, 0, 0, 1.15, 0.65, 0, 0)

[node name="CrateTL" parent="." instance=ExtResource("2_oldcrate_scan")]
transform = Transform3D(1.1, 0, 0.1, 0, 1.15, 0, -0.1, 0, 1.1, -0.65, 1.1, 0)

[node name="CrateTR" parent="." instance=ExtResource("1_crate_scan")]
transform = Transform3D(1.15, 0, 0, 0, 1.15, 0, 0, 0, 1.15, 0.65, 1.1, 0)
"""

with open(os.path.join(PROPS_DIR, "bgmi_crate_stack.tscn"), "w") as f:
    f.write(CRATE_STACK_TSCN)
print("Saved upgraded bgmi_crate_stack.tscn")

# -----------------------------------------------------------------------------
# 8. BGMI TRAIN BOXCAR (PBR Corrugated Steel & Freight Wagon bogies)
# -----------------------------------------------------------------------------
TRAIN_BOXCAR_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_train_boxcar_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_car_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_car_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_car_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_Boxcar"]
albedo_color = Color(0.55, 0.22, 0.18, 1)
albedo_texture = ExtResource("1_car_diff")
normal_enabled = true
normal_texture = ExtResource("2_car_norm")
roughness_texture = ExtResource("3_car_rough")
roughness = 0.65
metallic = 0.7
uv1_scale = Vector3(3, 1.2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_UnderCarriage"]
albedo_color = Color(0.18, 0.17, 0.16, 1)
metallic = 0.85
roughness = 0.4

[sub_resource type="BoxShape3D" id="Col_Boxcar"]
size = Vector3(14.0, 3.6, 3.2)

[sub_resource type="BoxMesh" id="Mesh_CarBody"]
material = SubResource("Mat_Boxcar")
size = Vector3(14.0, 3.1, 3.2)

[sub_resource type="CylinderMesh" id="Mesh_Wheel"]
material = SubResource("Mat_UnderCarriage")
top_radius = 0.45
bottom_radius = 0.45
height = 0.22
radial_segments = 14

[node name="BGMI_TrainBoxcar" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.8, 0)
shape = SubResource("Col_Boxcar")

[node name="CarBody" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.05, 0)
mesh = SubResource("Mesh_CarBody")

[node name="WheelFrontLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -4.8, 0.45, 1.45)
mesh = SubResource("Mesh_Wheel")

[node name="WheelFrontRight" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -4.8, 0.45, -1.45)
mesh = SubResource("Mesh_Wheel")

[node name="WheelBackLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 4.8, 0.45, 1.45)
mesh = SubResource("Mesh_Wheel")

[node name="WheelBackRight" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 4.8, 0.45, -1.45)
mesh = SubResource("Mesh_Wheel")
"""

with open(os.path.join(PROPS_DIR, "bgmi_train_boxcar.tscn"), "w") as f:
    f.write(TRAIN_BOXCAR_TSCN)
print("Saved upgraded bgmi_train_boxcar.tscn")

# -----------------------------------------------------------------------------
# 9. BGMI BACKDROP VILLA (PBR Clay Roof Tiles & Stucco Wall)
# -----------------------------------------------------------------------------
VILLA_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_backdrop_villa_pbr_001"]

[ext_resource type="Texture2D" path="res://assets/textures/villa_facade_albedo.png" id="1_facade"]
[ext_resource type="Texture2D" path="res://assets/textures/villa_facade_normal.png" id="2_facade_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/clay_roof_tiles_02_diff_1k.jpg" id="3_roof_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/clay_roof_tiles_02_nor_gl_1k.jpg" id="4_roof_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/clay_roof_tiles_02_rough_1k.jpg" id="5_roof_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_VillaWalls"]
albedo_texture = ExtResource("1_facade")
normal_enabled = true
normal_texture = ExtResource("2_facade_norm")
roughness = 0.75
uv1_scale = Vector3(2, 2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_VillaRoof"]
albedo_texture = ExtResource("3_roof_diff")
normal_enabled = true
normal_texture = ExtResource("4_roof_norm")
roughness_texture = ExtResource("5_roof_rough")
roughness = 0.7
uv1_scale = Vector3(4, 3, 1)

[sub_resource type="BoxShape3D" id="Col_Villa"]
size = Vector3(18.0, 9.0, 12.0)

[sub_resource type="BoxMesh" id="Mesh_VillaBody"]
material = SubResource("Mat_VillaWalls")
size = Vector3(18.0, 6.0, 12.0)

[sub_resource type="BoxMesh" id="Mesh_RoofLeft"]
material = SubResource("Mat_VillaRoof")
size = Vector3(19.0, 0.35, 7.5)

[node name="BGMI_BackdropVilla" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.5, 0)
shape = SubResource("Col_Villa")

[node name="MainBuilding" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.0, 0)
mesh = SubResource("Mesh_VillaBody")

[node name="RoofSlopeSouth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.819152, 0.573576, 0, -0.573576, 0.819152, 0, 7.8, 3.0)
mesh = SubResource("Mesh_RoofLeft")

[node name="RoofSlopeNorth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.819152, -0.573576, 0, 0.573576, 0.819152, 0, 7.8, -3.0)
mesh = SubResource("Mesh_RoofLeft")
"""

with open(os.path.join(PROPS_DIR, "bgmi_backdrop_villa.tscn"), "w") as f:
    f.write(VILLA_TSCN)
print("Saved upgraded bgmi_backdrop_villa.tscn")
print("ALL UPGRADED PROPS GENERATED SUCCESSFULLY!")
