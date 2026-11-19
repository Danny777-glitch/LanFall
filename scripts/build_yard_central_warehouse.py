import os

BASE_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1"
PROPS_DIR = os.path.join(BASE_DIR, "maps", "props")
os.makedirs(PROPS_DIR, exist_ok=True)

WAREHOUSE_TSCN = """[gd_scene load_steps=22 format=3 uid="uid://yard_central_warehouse_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_roof_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_roof_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_roof_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="6_wood_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/dirty_concrete_diff_1k.jpg" id="7_conc_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/dirty_concrete_nor_gl_1k.jpg" id="8_conc_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/dirty_concrete_rough_1k.jpg" id="9_conc_rough"]
[ext_resource type="PackedScene" path="res://assets/models/wooden_military_crate/wooden_military_crate.gltf" id="10_crate"]
[ext_resource type="PackedScene" path="res://assets/models/old_military_crate/old_military_crate.gltf" id="11_oldcrate"]
[ext_resource type="PackedScene" path="res://assets/models/Barrel_01/Barrel_01.gltf" id="12_barrel"]
[ext_resource type="PackedScene" path="res://assets/models/hanging_industrial_lamp/hanging_industrial_lamp.gltf" id="13_lamp"]

[sub_resource type="StandardMaterial3D" id="Mat_Floor"]
albedo_texture = ExtResource("7_conc_diff")
normal_enabled = true
normal_texture = ExtResource("8_conc_norm")
roughness_texture = ExtResource("9_conc_rough")
roughness = 0.38
uv1_scale = Vector3(0.3, 0.3, 0.3)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_WoodTimber"]
albedo_texture = ExtResource("4_wood_diff")
normal_enabled = true
normal_texture = ExtResource("5_wood_norm")
roughness_texture = ExtResource("6_wood_rough")
roughness = 0.8
uv1_scale = Vector3(0.4, 0.4, 0.4)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_RoofMetal"]
albedo_color = Color(0.52, 0.55, 0.58, 1)
albedo_texture = ExtResource("1_roof_diff")
normal_enabled = true
normal_texture = ExtResource("2_roof_norm")
roughness_texture = ExtResource("3_roof_rough")
metallic = 0.8
roughness = 0.52
uv1_scale = Vector3(0.4, 0.4, 0.4)
uv1_triplanar = true

[sub_resource type="BoxShape3D" id="Col_Floor"]
size = Vector3(16.0, 0.1, 24.0)

[sub_resource type="BoxMesh" id="Mesh_Floor"]
material = SubResource("Mat_Floor")
size = Vector3(16.0, 0.1, 24.0)

[sub_resource type="BoxMesh" id="Mesh_TimberPost"]
material = SubResource("Mat_WoodTimber")
size = Vector3(0.45, 5.8, 0.45)

[sub_resource type="BoxShape3D" id="Col_EndWall"]
size = Vector3(5.6, 5.8, 0.35)

[sub_resource type="BoxMesh" id="Mesh_EndWallLower"]
material = SubResource("Mat_WoodTimber")
size = Vector3(5.6, 1.4, 0.35)

[sub_resource type="BoxMesh" id="Mesh_EndWallUpper"]
material = SubResource("Mat_WoodTimber")
size = Vector3(5.6, 3.8, 0.35)

[sub_resource type="BoxMesh" id="Mesh_EndWallHeader"]
material = SubResource("Mat_WoodTimber")
size = Vector3(4.8, 2.0, 0.35)

[sub_resource type="BoxShape3D" id="Col_SideWall"]
size = Vector3(0.35, 5.8, 8.5)

[sub_resource type="BoxMesh" id="Mesh_SideWallLower"]
material = SubResource("Mat_WoodTimber")
size = Vector3(0.35, 1.3, 8.5)

[sub_resource type="BoxMesh" id="Mesh_SideWallUpper"]
material = SubResource("Mat_WoodTimber")
size = Vector3(0.35, 3.8, 8.5)

[sub_resource type="BoxMesh" id="Mesh_SideWallHeader"]
material = SubResource("Mat_WoodTimber")
size = Vector3(0.35, 2.0, 7.0)

[sub_resource type="BoxMesh" id="Mesh_RoofSlope"]
material = SubResource("Mat_RoofMetal")
size = Vector3(9.2, 0.25, 25.0)

[sub_resource type="BoxMesh" id="Mesh_RoofTruss"]
material = SubResource("Mat_WoodTimber")
size = Vector3(16.0, 0.3, 0.3)

[sub_resource type="BoxShape3D" id="Col_CenterCover"]
size = Vector3(3.2, 1.8, 2.4)

[node name="YardCentralWarehouse" type="StaticBody3D"]

[node name="ColFloor" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.05, 0)
shape = SubResource("Col_Floor")

[node name="FloorMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.05, 0)
mesh = SubResource("Mesh_Floor")

[node name="ColSouthL" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.2, 2.9, 12.0)
shape = SubResource("Col_EndWall")

[node name="MeshSouthL_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.2, 0.7, 12.0)
mesh = SubResource("Mesh_EndWallLower")

[node name="MeshSouthL_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.2, 3.9, 12.0)
mesh = SubResource("Mesh_EndWallUpper")

[node name="ColSouthR" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.2, 2.9, 12.0)
shape = SubResource("Col_EndWall")

[node name="MeshSouthR_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.2, 0.7, 12.0)
mesh = SubResource("Mesh_EndWallLower")

[node name="MeshSouthR_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.2, 3.9, 12.0)
mesh = SubResource("Mesh_EndWallUpper")

[node name="MeshSouthHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.8, 12.0)
mesh = SubResource("Mesh_EndWallHeader")

[node name="ColNorthL" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.2, 2.9, -12.0)
shape = SubResource("Col_EndWall")

[node name="MeshNorthL_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.2, 0.7, -12.0)
mesh = SubResource("Mesh_EndWallLower")

[node name="MeshNorthL_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.2, 3.9, -12.0)
mesh = SubResource("Mesh_EndWallUpper")

[node name="ColNorthR" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.2, 2.9, -12.0)
shape = SubResource("Col_EndWall")

[node name="MeshNorthR_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.2, 0.7, -12.0)
mesh = SubResource("Mesh_EndWallLower")

[node name="MeshNorthR_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.2, 3.9, -12.0)
mesh = SubResource("Mesh_EndWallUpper")

[node name="MeshNorthHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.8, -12.0)
mesh = SubResource("Mesh_EndWallHeader")

[node name="ColWestSouth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 2.9, 7.75)
shape = SubResource("Col_SideWall")

[node name="MeshWestSouth_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 0.65, 7.75)
mesh = SubResource("Mesh_SideWallLower")

[node name="MeshWestSouth_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 3.9, 7.75)
mesh = SubResource("Mesh_SideWallUpper")

[node name="ColWestNorth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 2.9, -7.75)
shape = SubResource("Col_SideWall")

[node name="MeshWestNorth_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 0.65, -7.75)
mesh = SubResource("Mesh_SideWallLower")

[node name="MeshWestNorth_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 3.9, -7.75)
mesh = SubResource("Mesh_SideWallUpper")

[node name="MeshWestHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 4.8, 0)
mesh = SubResource("Mesh_SideWallHeader")

[node name="ColEastSouth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 2.9, 7.75)
shape = SubResource("Col_SideWall")

[node name="MeshEastSouth_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 0.65, 7.75)
mesh = SubResource("Mesh_SideWallLower")

[node name="MeshEastSouth_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 3.9, 7.75)
mesh = SubResource("Mesh_SideWallUpper")

[node name="ColEastNorth" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 2.9, -7.75)
shape = SubResource("Col_SideWall")

[node name="MeshEastNorth_Low" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 0.65, -7.75)
mesh = SubResource("Mesh_SideWallLower")

[node name="MeshEastNorth_Up" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 3.9, -7.75)
mesh = SubResource("Mesh_SideWallUpper")

[node name="MeshEastHeader" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8.0, 4.8, 0)
mesh = SubResource("Mesh_SideWallHeader")

[node name="PostSW" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -7.8, 2.9, 11.8)
mesh = SubResource("Mesh_TimberPost")

[node name="PostSE" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 7.8, 2.9, 11.8)
mesh = SubResource("Mesh_TimberPost")

[node name="PostNW" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -7.8, 2.9, -11.8)
mesh = SubResource("Mesh_TimberPost")

[node name="PostNE" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 7.8, 2.9, -11.8)
mesh = SubResource("Mesh_TimberPost")

[node name="RoofSlopeWest" type="MeshInstance3D" parent="."]
transform = Transform3D(0.978148, -0.207912, 0, 0.207912, 0.978148, 0, 0, 0, 1, -4.1, 6.7, 0)
mesh = SubResource("Mesh_RoofSlope")

[node name="RoofSlopeEast" type="MeshInstance3D" parent="."]
transform = Transform3D(0.978148, 0.207912, 0, -0.207912, 0.978148, 0, 0, 0, 1, 4.1, 6.7, 0)
mesh = SubResource("Mesh_RoofSlope")

[node name="Truss1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.6, -8.0)
mesh = SubResource("Mesh_RoofTruss")

[node name="Truss2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.6, 0.0)
mesh = SubResource("Mesh_RoofTruss")

[node name="Truss3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.6, 8.0)
mesh = SubResource("Mesh_RoofTruss")

[node name="ReflectionProbe" type="ReflectionProbe" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.5, 0)
size = Vector3(17.0, 9.0, 25.0)
interior = true
enable_shadows = true

[node name="ColCenterCover" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("Col_CenterCover")

[node name="CenterCrate1" parent="." instance=ExtResource("10_crate")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -0.8, 0, 0)

[node name="CenterCrate2" parent="." instance=ExtResource("10_crate")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 0.8, 0, 0)

[node name="CenterCrateTop" parent="." instance=ExtResource("11_oldcrate")]
transform = Transform3D(1.15, 0, 0, 0, 1.15, 0, 0, 0, 1.15, 0, 0.9, 0)

[node name="BarrelSW" parent="." instance=ExtResource("12_barrel")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, -4.5, 0, 5.5)

[node name="BarrelNE" parent="." instance=ExtResource("12_barrel")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, 4.5, 0, -5.5)

[node name="Lamp1" parent="." instance=ExtResource("13_lamp")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, 0, 5.6, -6.0)

[node name="LampLight1" type="OmniLight3D" parent="Lamp1"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -1.2, 0)
light_color = Color(1.0, 0.88, 0.72, 1)
light_energy = 0.85
omni_range = 8.5
omni_attenuation = 1.2

[node name="Lamp2" parent="." instance=ExtResource("13_lamp")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, 0, 5.6, 6.0)

[node name="LampLight2" type="OmniLight3D" parent="Lamp2"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -1.2, 0)
light_color = Color(1.0, 0.88, 0.72, 1)
light_energy = 0.85
omni_range = 8.5
omni_attenuation = 1.2
"""

with open(os.path.join(PROPS_DIR, "yard_central_warehouse.tscn"), "w", encoding="utf-8") as f:
    f.write(WAREHOUSE_TSCN)

print("Created yard_central_warehouse.tscn successfully.")
