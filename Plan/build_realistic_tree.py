import os

PROPS_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps\warehouse\props"

PINE_TREE_TSCN = """[gd_scene load_steps=10 format=3 uid="uid://realistic_pine_tree_002"]

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
alpha_scissor_threshold = 0.45
cull_mode = 0
albedo_color = Color(0.22, 0.35, 0.20, 1)
albedo_texture = ExtResource("4_foliage")
roughness = 0.7
uv1_scale = Vector3(2, 2, 2)

[sub_resource type="CylinderMesh" id="Mesh_Trunk"]
material = SubResource("Mat_TrunkBark")
top_radius = 0.2
bottom_radius = 0.45
height = 9.0
radial_segments = 12

[sub_resource type="QuadMesh" id="Mesh_BranchQuadLarge"]
material = SubResource("Mat_PineNeedles")
size = Vector2(5.5, 3.2)

[sub_resource type="QuadMesh" id="Mesh_BranchQuadMid"]
material = SubResource("Mat_PineNeedles")
size = Vector2(4.2, 2.6)

[sub_resource type="QuadMesh" id="Mesh_BranchQuadTop"]
material = SubResource("Mat_PineNeedles")
size = Vector2(3.0, 2.2)

[sub_resource type="CylinderShape3D" id="Col_Trunk"]
height = 9.0
radius = 0.45

[node name="PineTree" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.5, 0)
shape = SubResource("Col_Trunk")

[node name="Trunk" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.5, 0)
mesh = SubResource("Mesh_Trunk")

# Bottom Tier Foliage (Crossed planes)
[node name="BranchBottom_0" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.2, 0)
mesh = SubResource("Mesh_BranchQuadLarge")

[node name="BranchBottom_45" type="MeshInstance3D" parent="."]
transform = Transform3D(0.707107, 0, 0.707107, 0, 1, 0, -0.707107, 0, 0.707107, 0, 4.2, 0)
mesh = SubResource("Mesh_BranchQuadLarge")

[node name="BranchBottom_90" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 4.2, 0)
mesh = SubResource("Mesh_BranchQuadLarge")

[node name="BranchBottom_135" type="MeshInstance3D" parent="."]
transform = Transform3D(-0.707107, 0, 0.707107, 0, 1, 0, -0.707107, 0, -0.707107, 0, 4.2, 0)
mesh = SubResource("Mesh_BranchQuadLarge")

# Mid Tier Foliage
[node name="BranchMid_20" type="MeshInstance3D" parent="."]
transform = Transform3D(0.939693, 0, 0.34202, 0, 1, 0, -0.34202, 0, 0.939693, 0, 6.0, 0)
mesh = SubResource("Mesh_BranchQuadMid")

[node name="BranchMid_70" type="MeshInstance3D" parent="."]
transform = Transform3D(0.34202, 0, 0.939693, 0, 1, 0, -0.939693, 0, 0.34202, 0, 6.0, 0)
mesh = SubResource("Mesh_BranchQuadMid")

[node name="BranchMid_110" type="MeshInstance3D" parent="."]
transform = Transform3D(-0.34202, 0, 0.939693, 0, 1, 0, -0.939693, 0, -0.34202, 0, 6.0, 0)
mesh = SubResource("Mesh_BranchQuadMid")

[node name="BranchMid_160" type="MeshInstance3D" parent="."]
transform = Transform3D(-0.939693, 0, 0.34202, 0, 1, 0, -0.34202, 0, -0.939693, 0, 6.0, 0)
mesh = SubResource("Mesh_BranchQuadMid")

# Top Tier Foliage
[node name="BranchTop_0" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 7.6, 0)
mesh = SubResource("Mesh_BranchQuadTop")

[node name="BranchTop_90" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 7.6, 0)
mesh = SubResource("Mesh_BranchQuadTop")

[node name="BranchTop_45" type="MeshInstance3D" parent="."]
transform = Transform3D(0.707107, 0, 0.707107, 0, 1, 0, -0.707107, 0, 0.707107, 0, 7.6, 0)
mesh = SubResource("Mesh_BranchQuadTop")
"""

with open(os.path.join(PROPS_DIR, "pine_tree.tscn"), "w") as f:
    f.write(PINE_TREE_TSCN)
print("Saved realistic alpha-scissor pine_tree.tscn")
