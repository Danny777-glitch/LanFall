import os

BASE_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1"
PROPS_DIR = os.path.join(BASE_DIR, "maps", "props")
os.makedirs(PROPS_DIR, exist_ok=True)

BACKDROP_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://yard_backdrop_001"]

[ext_resource type="PackedScene" path="res://scenes/maps/warehouse/props/pine_tree.tscn" id="1_tree"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/stony_dirt_path_diff_1k.jpg" id="2_dirt"]

[sub_resource type="StandardMaterial3D" id="Mat_MountainRidge"]
albedo_color = Color(0.24, 0.28, 0.32, 1)
roughness = 0.95

[sub_resource type="StandardMaterial3D" id="Mat_DistantGround"]
albedo_color = Color(0.20, 0.23, 0.22, 1)
albedo_texture = ExtResource("2_dirt")
roughness = 0.95
uv1_scale = Vector3(10, 10, 10)

[sub_resource type="PrismMesh" id="Mesh_MountainPeak"]
material = SubResource("Mat_MountainRidge")
left_to_right = 0.3
size = Vector3(45.0, 22.0, 20.0)

[sub_resource type="PlaneMesh" id="Mesh_OuterTerrain"]
material = SubResource("Mat_DistantGround")
size = Vector2(160.0, 160.0)

[node name="YardBackdrop" type="Node3D"]

[node name="OuterGround" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -0.22, 0)
mesh = SubResource("Mesh_OuterTerrain")

[node name="MountainNorth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6.0, -75.0)
mesh = SubResource("Mesh_MountainPeak")

[node name="MountainSouth" type="MeshInstance3D" parent="."]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 0, 6.0, 75.0)
mesh = SubResource("Mesh_MountainPeak")

[node name="MountainWest" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -75.0, 5.0, 0)
mesh = SubResource("Mesh_MountainPeak")

[node name="MountainEast" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, -1, 0, 1, 0, 1, 0, 0, 75.0, 5.0, 0)
mesh = SubResource("Mesh_MountainPeak")

[node name="Tree_NW1" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, -33.0, 0, -32.0)

[node name="Tree_NW2" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, -36.0, 0, -22.0)

[node name="Tree_W1" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -34.0, 0, 0.0)

[node name="Tree_SW1" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, -33.0, 0, 32.0)

[node name="Tree_SW2" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, -36.0, 0, 22.0)

[node name="Tree_NE1" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, 33.0, 0, -32.0)

[node name="Tree_NE2" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, 36.0, 0, -22.0)

[node name="Tree_E1" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 34.0, 0, 0.0)

[node name="Tree_SE1" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.3, 0, 0, 0, 1.3, 0, 0, 0, 1.3, 33.0, 0, 32.0)

[node name="Tree_SE2" parent="." instance=ExtResource("1_tree")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, 36.0, 0, 22.0)
"""

with open(os.path.join(PROPS_DIR, "yard_backdrop.tscn"), "w", encoding="utf-8") as f:
    f.write(BACKDROP_TSCN)

print("Created yard_backdrop.tscn successfully.")
