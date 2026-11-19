import os

PROPS_DIR = "c:/Users/danie/Documents/my_projects/lan-fall-phase1/scenes/maps/warehouse/props"
os.makedirs(PROPS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. BGMI Spawn Sheds (Twin wooden sheds with weapon tables & blue slate roofs)
# -----------------------------------------------------------------------------
SPAWN_SHEDS_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_spawn_sheds_001"]

[ext_resource type="Texture2D" path="res://assets/textures/spawn_shed_roof_albedo.png" id="1_roof"]
[ext_resource type="Texture2D" path="res://assets/textures/spawn_shed_roof_normal.png" id="2_roof_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_planks.png" id="3_wood"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_fence_lattice_albedo.png" id="4_fence"]

[sub_resource type="StandardMaterial3D" id="Mat_ShedRoof"]
albedo_texture = ExtResource("1_roof")
normal_enabled = true
normal_texture = ExtResource("2_roof_norm")
roughness = 0.65
uv1_scale = Vector3(2, 2, 2)

[sub_resource type="StandardMaterial3D" id="Mat_TimberWood"]
albedo_texture = ExtResource("3_wood")
roughness = 0.8
uv1_scale = Vector3(1, 4, 1)

[sub_resource type="StandardMaterial3D" id="Mat_BackWall"]
albedo_texture = ExtResource("4_fence")
roughness = 0.85
uv1_scale = Vector3(2, 1, 1)

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

[sub_resource type="BoxMesh" id="Mesh_Table"]
material = SubResource("Mat_TimberWood")
size = Vector3(2.4, 0.85, 1.1)

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

# Left Shed Roof & Posts
[node name="RoofLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.939693, 0.34202, 0, -0.34202, 0.939693, -5.2, 4.0, 0.2)
mesh = SubResource("Mesh_RoofSlab")

[node name="PostL1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -9.0, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="PostL2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.4, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="TableLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.2, 0.45, 0.5)
mesh = SubResource("Mesh_Table")

# Right Shed Roof & Posts
[node name="RoofRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.939693, 0.34202, 0, -0.34202, 0.939693, 5.2, 4.0, 0.2)
mesh = SubResource("Mesh_RoofSlab")

[node name="PostR1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 1.4, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="PostR2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 9.0, 1.9, -2.4)
mesh = SubResource("Mesh_Post")

[node name="TableRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.2, 0.45, 0.5)
mesh = SubResource("Mesh_Table")
"""

with open(os.path.join(PROPS_DIR, "bgmi_spawn_sheds.tscn"), "w") as f:
    f.write(SPAWN_SHEDS_TSCN)
print("Saved bgmi_spawn_sheds.tscn")


# -----------------------------------------------------------------------------
# 2. BGMI Perimeter Fence (Vertical planks with top diamond lattice)
# -----------------------------------------------------------------------------
PERIMETER_FENCE_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://bgmi_fence_001"]

[ext_resource type="Texture2D" path="res://assets/textures/wood_fence_lattice_albedo.png" id="1_fence"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_fence_lattice_normal.png" id="2_fence_norm"]

[sub_resource type="StandardMaterial3D" id="Mat_LatticeFence"]
albedo_texture = ExtResource("1_fence")
normal_enabled = true
normal_texture = ExtResource("2_fence_norm")
roughness = 0.85
uv1_scale = Vector3(2.5, 1, 1)

[sub_resource type="BoxShape3D" id="Col_Fence"]
size = Vector3(8.0, 2.5, 0.25)

[sub_resource type="BoxMesh" id="Mesh_Fence"]
material = SubResource("Mat_LatticeFence")
size = Vector3(8.0, 2.5, 0.25)

[sub_resource type="BoxMesh" id="Mesh_Post"]
material = SubResource("Mat_LatticeFence")
size = Vector3(0.35, 2.7, 0.35)

[node name="BGMI_PerimeterFence" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.25, 0)
shape = SubResource("Col_Fence")

[node name="FenceMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.25, 0)
mesh = SubResource("Mesh_Fence")

[node name="PostLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4.0, 1.35, 0)
mesh = SubResource("Mesh_Post")

[node name="PostRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4.0, 1.35, 0)
mesh = SubResource("Mesh_Post")
"""

with open(os.path.join(PROPS_DIR, "bgmi_perimeter_fence.tscn"), "w") as f:
    f.write(PERIMETER_FENCE_TSCN)
print("Saved bgmi_perimeter_fence.tscn")


# -----------------------------------------------------------------------------
# 3. BGMI Train Freight Boxcar (Railway wagon with roof walk & wheels)
# -----------------------------------------------------------------------------
TRAIN_BOXCAR_TSCN = """[gd_scene load_steps=7 format=3 uid="uid://bgmi_train_boxcar_001"]

[ext_resource type="Texture2D" path="res://assets/textures/train_boxcar_albedo.png" id="1_car"]
[ext_resource type="Texture2D" path="res://assets/textures/train_boxcar_normal.png" id="2_car_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/metal_trim.png" id="3_metal"]

[sub_resource type="StandardMaterial3D" id="Mat_Boxcar"]
albedo_texture = ExtResource("1_car")
normal_enabled = true
normal_texture = ExtResource("2_car_norm")
roughness = 0.65
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
radial_segments = 12

[node name="BGMI_TrainBoxcar" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.8, 0)
shape = SubResource("Col_Boxcar")

[node name="CarBody" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.05, 0)
mesh = SubResource("Mesh_CarBody")

# Wheel Trucks / Bogies
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
print("Saved bgmi_train_boxcar.tscn")


# -----------------------------------------------------------------------------
# 4. BGMI Container with Sniper Boarding Ramp (As shown in frame 28)
# -----------------------------------------------------------------------------
CONTAINER_RAMP_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://bgmi_container_ramp_001"]

[ext_resource type="Texture2D" path="res://assets/textures/container_yellow_albedo.png" id="1_cont"]
[ext_resource type="Texture2D" path="res://assets/textures/container_yellow_normal.png" id="2_cont_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_planks.png" id="3_wood"]

[sub_resource type="StandardMaterial3D" id="Mat_Container"]
albedo_texture = ExtResource("1_cont")
normal_enabled = true
normal_texture = ExtResource("2_cont_norm")
roughness = 0.6
uv1_scale = Vector3(2.5, 1, 1)

[sub_resource type="StandardMaterial3D" id="Mat_RampWood"]
albedo_texture = ExtResource("3_wood")
roughness = 0.85
uv1_scale = Vector3(1, 4, 1)

[sub_resource type="BoxShape3D" id="Col_Container"]
size = Vector3(6.5, 2.7, 2.6)

[sub_resource type="BoxMesh" id="Mesh_Container"]
material = SubResource("Mat_Container")
size = Vector3(6.5, 2.7, 2.6)

[sub_resource type="BoxShape3D" id="Col_Ramp"]
size = Vector3(1.8, 0.25, 4.8)

[sub_resource type="BoxMesh" id="Mesh_Ramp"]
material = SubResource("Mat_RampWood")
size = Vector3(1.8, 0.25, 4.8)

[node name="BGMI_ContainerRamp" type="StaticBody3D"]

[node name="ContainerCol" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.35, 0)
shape = SubResource("Col_Container")

[node name="ContainerMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.35, 0)
mesh = SubResource("Mesh_Container")

# Wooden Boarding Ramp leading onto Container Roof
[node name="RampCol" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.866025, 0.5, 0, -0.5, 0.866025, 1.6, 1.3, 2.8)
shape = SubResource("Col_Ramp")

[node name="RampMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.866025, 0.5, 0, -0.5, 0.866025, 1.6, 1.3, 2.8)
mesh = SubResource("Mesh_Ramp")
"""

with open(os.path.join(PROPS_DIR, "bgmi_container_ramp.tscn"), "w") as f:
    f.write(CONTAINER_RAMP_TSCN)
print("Saved bgmi_container_ramp.tscn")


# -----------------------------------------------------------------------------
# 5. BGMI Timber Yard Log Stack (Cylindrical lumber stacked in wooden cradle)
# -----------------------------------------------------------------------------
TIMBER_LOGS_TSCN = """[gd_scene load_steps=6 format=3 uid="uid://bgmi_timber_logs_001"]

[ext_resource type="Texture2D" path="res://assets/textures/timber_logs_albedo.png" id="1_log"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_planks.png" id="2_wood"]

[sub_resource type="StandardMaterial3D" id="Mat_Logs"]
albedo_texture = ExtResource("1_log")
roughness = 0.88
uv1_scale = Vector3(1, 2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Cradle"]
albedo_texture = ExtResource("2_wood")
roughness = 0.8
uv1_scale = Vector3(1, 3, 1)

[sub_resource type="BoxShape3D" id="Col_LogStack"]
size = Vector3(6.2, 2.2, 2.4)

[sub_resource type="CylinderMesh" id="Mesh_SingleLog"]
material = SubResource("Mat_Logs")
top_radius = 0.28
bottom_radius = 0.28
height = 6.0
radial_segments = 10

[sub_resource type="BoxMesh" id="Mesh_CradlePost"]
material = SubResource("Mat_Cradle")
size = Vector3(0.25, 2.4, 0.25)

[node name="BGMI_TimberLogStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
shape = SubResource("Col_LogStack")

# Cradle Uprights
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

# Logs Tier 1 (Bottom 3 logs)
[node name="Log1" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.35, -0.6)
mesh = SubResource("Mesh_SingleLog")

[node name="Log2" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.35, 0.0)
mesh = SubResource("Mesh_SingleLog")

[node name="Log3" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.35, 0.6)
mesh = SubResource("Mesh_SingleLog")

# Logs Tier 2 (Mid 2 logs)
[node name="Log4" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.9, -0.3)
mesh = SubResource("Mesh_SingleLog")

[node name="Log5" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 0.9, 0.3)
mesh = SubResource("Mesh_SingleLog")

# Logs Tier 3 (Top 1 log)
[node name="Log6" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 0, 1.45, 0.0)
mesh = SubResource("Mesh_SingleLog")
"""

with open(os.path.join(PROPS_DIR, "bgmi_timber_logs.tscn"), "w") as f:
    f.write(TIMBER_LOGS_TSCN)
print("Saved bgmi_timber_logs.tscn")


# -----------------------------------------------------------------------------
# 6. BGMI Wooden Pergola / Gazebo Pavilion (West flank structure)
# -----------------------------------------------------------------------------
PERGOLA_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://bgmi_pergola_001"]

[ext_resource type="Texture2D" path="res://assets/textures/wood_planks.png" id="1_wood"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_fence_lattice_albedo.png" id="2_lattice"]

[sub_resource type="StandardMaterial3D" id="Mat_PergolaTimber"]
albedo_texture = ExtResource("1_wood")
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

# 4 Corner Pillars
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

# Overhead Main Longitudinal Beams
[node name="BeamNorth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.8, -2.2)
mesh = SubResource("Mesh_BeamMain")

[node name="BeamSouth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.8, 2.2)
mesh = SubResource("Mesh_BeamMain")

# Cross Rafters
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
"""

with open(os.path.join(PROPS_DIR, "bgmi_wooden_pergola.tscn"), "w") as f:
    f.write(PERGOLA_TSCN)
print("Saved bgmi_wooden_pergola.tscn")


# -----------------------------------------------------------------------------
# 7. BGMI Jersey Barrier (Detailed highway concrete barrier with drain slots)
# -----------------------------------------------------------------------------
JERSEY_BARRIER_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://bgmi_jersey_barrier_001"]

[ext_resource type="Texture2D" path="res://assets/textures/jersey_barrier_albedo.png" id="1_conc"]
[ext_resource type="Texture2D" path="res://assets/textures/jersey_barrier_normal.png" id="2_conc_norm"]

[sub_resource type="StandardMaterial3D" id="Mat_BarrierConcrete"]
albedo_texture = ExtResource("1_conc")
normal_enabled = true
normal_texture = ExtResource("2_conc_norm")
roughness = 0.8
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
print("Saved bgmi_jersey_barrier.tscn")


# -----------------------------------------------------------------------------
# 8. BGMI 2x2 Crate Stack (Tactical jumpable cover)
# -----------------------------------------------------------------------------
CRATE_STACK_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://bgmi_crate_stack_001"]

[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_albedo.png" id="1_crate"]
[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_normal.png" id="2_crate_norm"]

[sub_resource type="StandardMaterial3D" id="Mat_WoodCrate"]
albedo_texture = ExtResource("1_crate")
normal_enabled = true
normal_texture = ExtResource("2_crate_norm")
roughness = 0.75

[sub_resource type="BoxShape3D" id="Col_Stack"]
size = Vector3(2.5, 2.2, 1.8)

[sub_resource type="BoxMesh" id="Mesh_CrateSingle"]
material = SubResource("Mat_WoodCrate")
size = Vector3(1.15, 1.05, 1.6)

[node name="BGMI_CrateStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
shape = SubResource("Col_Stack")

# Bottom Two Crates
[node name="CrateBottomLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.6, 0.53, 0)
mesh = SubResource("Mesh_CrateSingle")

[node name="CrateBottomRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.6, 0.53, 0)
mesh = SubResource("Mesh_CrateSingle")

# Top Two Crates
[node name="CrateTopLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.6, 1.58, 0)
mesh = SubResource("Mesh_CrateSingle")

[node name="CrateTopRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.6, 1.58, 0)
mesh = SubResource("Mesh_CrateSingle")
"""

with open(os.path.join(PROPS_DIR, "bgmi_crate_stack.tscn"), "w") as f:
    f.write(CRATE_STACK_TSCN)
print("Saved bgmi_crate_stack.tscn")


# -----------------------------------------------------------------------------
# 9. BGMI Backdrop Villa (2-Story White House on North-West)
# -----------------------------------------------------------------------------
VILLA_TSCN = """[gd_scene load_steps=7 format=3 uid="uid://bgmi_backdrop_villa_001"]

[ext_resource type="Texture2D" path="res://assets/textures/villa_facade_albedo.png" id="1_facade"]
[ext_resource type="Texture2D" path="res://assets/textures/villa_facade_normal.png" id="2_facade_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/roof_terracotta_rich_albedo.png" id="3_roof"]
[ext_resource type="Texture2D" path="res://assets/textures/roof_terracotta_rich_normal.png" id="4_roof_norm"]

[sub_resource type="StandardMaterial3D" id="Mat_VillaWalls"]
albedo_texture = ExtResource("1_facade")
normal_enabled = true
normal_texture = ExtResource("2_facade_norm")
roughness = 0.75
uv1_scale = Vector3(2, 2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_VillaRoof"]
albedo_texture = ExtResource("3_roof")
normal_enabled = true
normal_texture = ExtResource("4_roof_norm")
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

# Pitched Terracotta Roof
[node name="RoofSlopeSouth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.819152, 0.573576, 0, -0.573576, 0.819152, 0, 7.8, 3.0)
mesh = SubResource("Mesh_RoofLeft")

[node name="RoofSlopeNorth" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.819152, -0.573576, 0, 0.573576, 0.819152, 0, 7.8, -3.0)
mesh = SubResource("Mesh_RoofLeft")
"""

with open(os.path.join(PROPS_DIR, "bgmi_backdrop_villa.tscn"), "w") as f:
    f.write(VILLA_TSCN)
print("Saved bgmi_backdrop_villa.tscn")
print("ALL BGMI PROPS GENERATED SUCCESSFULLY!")
