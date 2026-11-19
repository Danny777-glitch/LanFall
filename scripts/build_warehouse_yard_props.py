import os

BASE_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1"
PROPS_DIR = os.path.join(BASE_DIR, "maps", "props")
os.makedirs(PROPS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. YARD JERSEY BARRIER
# -----------------------------------------------------------------------------
JERSEY_BARRIER_TSCN = """[gd_scene load_steps=6 format=3 uid="uid://yard_jersey_barrier_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_diff_1k.jpg" id="1_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_nor_gl_1k.jpg" id="2_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_rough_1k.jpg" id="3_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_JerseyBarrier"]
albedo_color = Color(0.85, 0.85, 0.85, 1)
albedo_texture = ExtResource("1_diff")
normal_enabled = true
normal_texture = ExtResource("2_norm")
roughness_texture = ExtResource("3_rough")
roughness = 0.85
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="BoxShape3D" id="Col_JerseyBarrier"]
size = Vector3(3.0, 1.05, 0.6)

[sub_resource type="BoxMesh" id="Mesh_JerseyBarrier"]
material = SubResource("Mat_JerseyBarrier")
size = Vector3(3.0, 1.05, 0.6)

[node name="YardJerseyBarrier" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.525, 0)
shape = SubResource("Col_JerseyBarrier")

[node name="Mesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.525, 0)
mesh = SubResource("Mesh_JerseyBarrier")
"""

# -----------------------------------------------------------------------------
# 2. YARD SHIPPING CONTAINERS (Red, Blue, Yellow)
# -----------------------------------------------------------------------------
def get_container_tscn(uid, color_rgb, color_name):
    return f"""[gd_scene load_steps=6 format=3 uid="{uid}"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_diff_1k.jpg" id="1_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_nor_gl_1k.jpg" id="2_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_rough_1k.jpg" id="3_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_Container"]
albedo_color = Color({color_rgb})
albedo_texture = ExtResource("1_diff")
normal_enabled = true
normal_texture = ExtResource("2_norm")
roughness_texture = ExtResource("3_rough")
metallic = 0.75
roughness = 0.5
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="BoxShape3D" id="Col_Container"]
size = Vector3(2.4, 2.6, 6.0)

[sub_resource type="BoxMesh" id="Mesh_Container"]
material = SubResource("Mat_Container")
size = Vector3(2.4, 2.6, 6.0)

[node name="YardContainer_{color_name}" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.3, 0)
shape = SubResource("Col_Container")

[node name="Mesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.3, 0)
mesh = SubResource("Mesh_Container")
"""

# -----------------------------------------------------------------------------
# 3. YARD CONTAINER 2-STACK WITH CLIMBABLE RAMP
# -----------------------------------------------------------------------------
CONTAINER_RAMP_STACK_TSCN = """[gd_scene load_steps=15 format=3 uid="uid://yard_container_ramp_stack_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_diff_1k.jpg" id="1_cont_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_nor_gl_1k.jpg" id="2_cont_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/container_side_rough_1k.jpg" id="3_cont_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="6_wood_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_ContainerRed"]
albedo_color = Color(0.72, 0.22, 0.18, 1)
albedo_texture = ExtResource("1_cont_diff")
normal_enabled = true
normal_texture = ExtResource("2_cont_norm")
roughness_texture = ExtResource("3_cont_rough")
metallic = 0.75
roughness = 0.55
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_ContainerBlue"]
albedo_color = Color(0.20, 0.42, 0.65, 1)
albedo_texture = ExtResource("1_cont_diff")
normal_enabled = true
normal_texture = ExtResource("2_cont_norm")
roughness_texture = ExtResource("3_cont_rough")
metallic = 0.75
roughness = 0.55
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_WoodRamp"]
albedo_texture = ExtResource("4_wood_diff")
normal_enabled = true
normal_texture = ExtResource("5_wood_norm")
roughness_texture = ExtResource("6_wood_rough")
roughness = 0.8
uv1_scale = Vector3(1, 3, 1)

[sub_resource type="BoxShape3D" id="Col_ContainerBox"]
size = Vector3(2.4, 2.6, 6.0)

[sub_resource type="BoxMesh" id="Mesh_ContainerRed"]
material = SubResource("Mat_ContainerRed")
size = Vector3(2.4, 2.6, 6.0)

[sub_resource type="BoxMesh" id="Mesh_ContainerBlue"]
material = SubResource("Mat_ContainerBlue")
size = Vector3(2.4, 2.6, 6.0)

[sub_resource type="BoxShape3D" id="Col_Ramp"]
size = Vector3(1.6, 0.2, 5.8)

[sub_resource type="BoxMesh" id="Mesh_Ramp"]
material = SubResource("Mat_WoodRamp")
size = Vector3(1.6, 0.2, 5.8)

[sub_resource type="BoxMesh" id="Mesh_RampPost"]
material = SubResource("Mat_WoodRamp")
size = Vector3(0.2, 1.8, 0.2)

[node name="YardContainerRampStack" type="StaticBody3D"]

[node name="Col_Lower" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.3, 0)
shape = SubResource("Col_ContainerBox")

[node name="Mesh_Lower" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.3, 0)
mesh = SubResource("Mesh_ContainerRed")

[node name="Col_Upper" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.9, 0)
shape = SubResource("Col_ContainerBox")

[node name="Mesh_Upper" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.9, 0)
mesh = SubResource("Mesh_ContainerBlue")

[node name="Col_Ramp" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.906308, -0.422618, 0, 0.422618, 0.906308, 0, 1.3, 5.2)
shape = SubResource("Col_Ramp")

[node name="Mesh_Ramp" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.906308, -0.422618, 0, 0.422618, 0.906308, 0, 1.3, 5.2)
mesh = SubResource("Mesh_Ramp")

[node name="RampPostL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.7, 0.9, 4.2)
mesh = SubResource("Mesh_RampPost")

[node name="RampPostR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.7, 0.9, 4.2)
mesh = SubResource("Mesh_RampPost")
"""

# -----------------------------------------------------------------------------
# 4. YARD CRATE STACK
# -----------------------------------------------------------------------------
CRATE_STACK_TSCN = """[gd_scene load_steps=8 format=3 uid="uid://yard_crate_stack_001"]

[ext_resource type="PackedScene" path="res://assets/models/wooden_military_crate/wooden_military_crate.gltf" id="1_crate"]
[ext_resource type="PackedScene" path="res://assets/models/old_military_crate/old_military_crate.gltf" id="2_oldcrate"]
[ext_resource type="PackedScene" path="res://assets/models/ammo_box/ammo_box.gltf" id="3_ammobox"]

[sub_resource type="BoxShape3D" id="Col_Crates"]
size = Vector3(2.4, 1.8, 1.6)

[node name="YardCrateStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("Col_Crates")

[node name="CrateBottomL" parent="." instance=ExtResource("1_crate")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -0.6, 0, 0)

[node name="CrateBottomR" parent="." instance=ExtResource("1_crate")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 0.6, 0, 0)

[node name="CrateTopMid" parent="." instance=ExtResource("2_oldcrate")]
transform = Transform3D(1.15, 0, 0, 0, 1.15, 0, 0, 0, 1.15, 0, 0.9, 0)

[node name="AmmoBoxTop" parent="." instance=ExtResource("3_ammobox")]
transform = Transform3D(1.4, 0, 0, 0, 1.4, 0, 0, 0, 1.4, 0.6, 0.9, 0.2)
"""

# -----------------------------------------------------------------------------
# 5. YARD BARREL CLUSTER
# -----------------------------------------------------------------------------
BARREL_CLUSTER_TSCN = """[gd_scene load_steps=5 format=3 uid="uid://yard_barrel_cluster_001"]

[ext_resource type="PackedScene" path="res://assets/models/Barrel_01/Barrel_01.gltf" id="1_barrel"]

[sub_resource type="CylinderShape3D" id="Col_Barrel1"]
height = 1.05
radius = 0.35

[sub_resource type="CylinderShape3D" id="Col_Barrel2"]
height = 1.05
radius = 0.35

[sub_resource type="CylinderShape3D" id="Col_Barrel3"]
height = 1.05
radius = 0.35

[node name="YardBarrelCluster" type="StaticBody3D"]

[node name="Col1" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.35, 0.525, 0.2)
shape = SubResource("Col_Barrel1")

[node name="Col2" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.35, 0.525, 0.2)
shape = SubResource("Col_Barrel2")

[node name="Col3" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.525, -0.38)
shape = SubResource("Col_Barrel3")

[node name="Barrel1" parent="." instance=ExtResource("1_barrel")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, -0.35, 0, 0.2)

[node name="Barrel2" parent="." instance=ExtResource("1_barrel")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, 0.35, 0, 0.2)

[node name="Barrel3" parent="." instance=ExtResource("1_barrel")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, 0, 0, -0.38)
"""

# -----------------------------------------------------------------------------
# 6. YARD FREIGHT BOXCAR
# -----------------------------------------------------------------------------
FREIGHT_BOXCAR_TSCN = """[gd_scene load_steps=12 format=3 uid="uid://yard_freight_boxcar_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_iron_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_iron_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_iron_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]

[sub_resource type="StandardMaterial3D" id="Mat_BoxcarSteel"]
albedo_color = Color(0.48, 0.24, 0.20, 1)
albedo_texture = ExtResource("1_iron_diff")
normal_enabled = true
normal_texture = ExtResource("2_iron_norm")
roughness_texture = ExtResource("3_iron_rough")
metallic = 0.8
roughness = 0.55
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_BoxcarUndercarriage"]
albedo_color = Color(0.18, 0.18, 0.20, 1)
metallic = 0.9
roughness = 0.4

[sub_resource type="BoxShape3D" id="Col_CarBody"]
size = Vector3(2.8, 3.2, 9.6)

[sub_resource type="BoxMesh" id="Mesh_CarBody"]
material = SubResource("Mat_BoxcarSteel")
size = Vector3(2.8, 2.7, 9.6)

[sub_resource type="BoxMesh" id="Mesh_Undercarriage"]
material = SubResource("Mat_BoxcarUndercarriage")
size = Vector3(2.6, 0.5, 9.8)

[sub_resource type="CylinderMesh" id="Mesh_Wheel"]
material = SubResource("Mat_BoxcarUndercarriage")
top_radius = 0.45
bottom_radius = 0.45
height = 0.25

[node name="YardFreightBoxcar" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
shape = SubResource("Col_CarBody")

[node name="BodyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.85, 0)
mesh = SubResource("Mesh_CarBody")

[node name="BaseMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.25, 0)
mesh = SubResource("Mesh_Undercarriage")

[node name="WheelFL" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 1.35, 0.45, 3.2)
mesh = SubResource("Mesh_Wheel")

[node name="WheelFR" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -1.35, 0.45, 3.2)
mesh = SubResource("Mesh_Wheel")

[node name="WheelRL" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, 1.35, 0.45, -3.2)
mesh = SubResource("Mesh_Wheel")

[node name="WheelRR" type="MeshInstance3D" parent="."]
transform = Transform3D(0, 0, 1, 0, 1, 0, -1, 0, 0, -1.35, 0.45, -3.2)
mesh = SubResource("Mesh_Wheel")
"""

# -----------------------------------------------------------------------------
# 7. YARD TIMBER LOG STACK
# -----------------------------------------------------------------------------
TIMBER_STACK_TSCN = """[gd_scene load_steps=7 format=3 uid="uid://yard_timber_stack_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="1_bark_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="2_bark_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_rough_1k.jpg" id="3_bark_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_Bark"]
albedo_texture = ExtResource("1_bark_diff")
normal_enabled = true
normal_texture = ExtResource("2_bark_norm")
roughness_texture = ExtResource("3_bark_rough")
roughness = 0.9
uv1_scale = Vector3(1, 2, 1)

[sub_resource type="BoxShape3D" id="Col_TimberStack"]
size = Vector3(2.2, 1.25, 4.2)

[sub_resource type="CylinderMesh" id="Mesh_Log"]
material = SubResource("Mat_Bark")
top_radius = 0.32
bottom_radius = 0.32
height = 4.2

[node name="YardTimberStack" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.625, 0)
shape = SubResource("Col_TimberStack")

[node name="Log1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0, 1, 0, -1, 0, -0.65, 0.32, 0)
mesh = SubResource("Mesh_Log")

[node name="Log2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0, 1, 0, -1, 0, 0.0, 0.32, 0)
mesh = SubResource("Mesh_Log")

[node name="Log3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0, 1, 0, -1, 0, 0.65, 0.32, 0)
mesh = SubResource("Mesh_Log")

[node name="Log4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0, 1, 0, -1, 0, -0.32, 0.88, 0)
mesh = SubResource("Mesh_Log")

[node name="Log5" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0, 1, 0, -1, 0, 0.32, 0.88, 0)
mesh = SubResource("Mesh_Log")
"""

# -----------------------------------------------------------------------------
# 8. YARD PERIMETER FENCE PANEL (6m wide)
# -----------------------------------------------------------------------------
PERIMETER_FENCE_TSCN = """[gd_scene load_steps=10 format=3 uid="uid://yard_perimeter_fence_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_iron_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_iron_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_iron_rough"]

[sub_resource type="StandardMaterial3D" id="Mat_FenceSteel"]
albedo_color = Color(0.45, 0.48, 0.52, 1)
albedo_texture = ExtResource("1_iron_diff")
normal_enabled = true
normal_texture = ExtResource("2_iron_norm")
roughness_texture = ExtResource("3_iron_rough")
metallic = 0.8
roughness = 0.5
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_SteelPost"]
albedo_color = Color(0.2, 0.22, 0.25, 1)
metallic = 0.85
roughness = 0.4

[sub_resource type="BoxShape3D" id="Col_Fence"]
size = Vector3(6.0, 3.2, 0.3)

[sub_resource type="BoxMesh" id="Mesh_FencePanel"]
material = SubResource("Mat_FenceSteel")
size = Vector3(5.8, 3.0, 0.12)

[sub_resource type="BoxMesh" id="Mesh_SteelPost"]
material = SubResource("Mat_SteelPost")
size = Vector3(0.25, 3.4, 0.25)

[node name="YardPerimeterFence" type="StaticBody3D"]

[node name="Collision" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
shape = SubResource("Col_Fence")

[node name="PanelMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
mesh = SubResource("Mesh_FencePanel")

[node name="PostL" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.95, 1.7, 0)
mesh = SubResource("Mesh_SteelPost")

[node name="PostR" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.95, 1.7, 0)
mesh = SubResource("Mesh_SteelPost")
"""

# -----------------------------------------------------------------------------
# 9. YARD SAFE SPAWN SHED COMPOUND
# -----------------------------------------------------------------------------
SPAWN_SHED_TSCN = """[gd_scene load_steps=18 format=3 uid="uid://yard_spawn_shed_001"]

[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_roof_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_roof_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_roof_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="6_wood_rough"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_diff_1k.jpg" id="7_conc_diff"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_nor_gl_1k.jpg" id="8_conc_norm"]
[ext_resource type="Texture2D" path="res://assets/textures/pbr/chipped_concrete_rough_1k.jpg" id="9_conc_rough"]
[ext_resource type="PackedScene" path="res://assets/models/wooden_table_02/wooden_table_02.gltf" id="10_table"]
[ext_resource type="PackedScene" path="res://assets/models/ammo_box/ammo_box.gltf" id="11_ammo"]
[ext_resource type="PackedScene" path="res://assets/models/wooden_military_crate/wooden_military_crate.gltf" id="12_crate"]

[sub_resource type="StandardMaterial3D" id="Mat_ShedRoof"]
albedo_color = Color(0.45, 0.48, 0.52, 1)
albedo_texture = ExtResource("1_roof_diff")
normal_enabled = true
normal_texture = ExtResource("2_roof_norm")
roughness_texture = ExtResource("3_roof_rough")
metallic = 0.7
roughness = 0.55
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_ShedWood"]
albedo_texture = ExtResource("4_wood_diff")
normal_enabled = true
normal_texture = ExtResource("5_wood_norm")
roughness_texture = ExtResource("6_wood_rough")
roughness = 0.85
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="StandardMaterial3D" id="Mat_BlastWall"]
albedo_texture = ExtResource("7_conc_diff")
normal_enabled = true
normal_texture = ExtResource("8_conc_norm")
roughness_texture = ExtResource("9_conc_rough")
roughness = 0.88
uv1_scale = Vector3(0.5, 0.5, 0.5)
uv1_triplanar = true

[sub_resource type="BoxShape3D" id="Col_BackWall"]
size = Vector3(14.0, 4.0, 0.4)

[sub_resource type="BoxMesh" id="Mesh_BackWall"]
material = SubResource("Mat_ShedWood")
size = Vector3(14.0, 4.0, 0.4)

[sub_resource type="BoxMesh" id="Mesh_TimberPost"]
material = SubResource("Mat_ShedWood")
size = Vector3(0.4, 3.8, 0.4)

[sub_resource type="BoxMesh" id="Mesh_RoofSlab"]
material = SubResource("Mat_ShedRoof")
size = Vector3(14.4, 0.25, 6.0)

[sub_resource type="BoxShape3D" id="Col_BlastWall"]
size = Vector3(8.0, 2.8, 0.6)

[sub_resource type="BoxMesh" id="Mesh_BlastWall"]
material = SubResource("Mat_BlastWall")
size = Vector3(8.0, 2.8, 0.6)

[node name="YardSpawnShed" type="StaticBody3D"]

[node name="ColBack" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.0, 2.8)
shape = SubResource("Col_BackWall")

[node name="MeshBack" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.0, 2.8)
mesh = SubResource("Mesh_BackWall")

[node name="Post1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6.6, 1.9, -2.4)
mesh = SubResource("Mesh_TimberPost")

[node name="Post2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 6.6, 1.9, -2.4)
mesh = SubResource("Mesh_TimberPost")

[node name="Post3" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.2, 1.9, -2.4)
mesh = SubResource("Mesh_TimberPost")

[node name="Post4" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.2, 1.9, -2.4)
mesh = SubResource("Mesh_TimberPost")

[node name="RoofMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.984808, 0.173648, 0, -0.173648, 0.984808, 0, 3.8, 0.2)
mesh = SubResource("Mesh_RoofSlab")

[node name="ColBlastWall" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, -4.5)
shape = SubResource("Col_BlastWall")

[node name="MeshBlastWall" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.4, -4.5)
mesh = SubResource("Mesh_BlastWall")

[node name="TableLeft" parent="." instance=ExtResource("10_table")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, -4.5, 0, 1.5)

[node name="TableRight" parent="." instance=ExtResource("10_table")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, 4.5, 0, 1.5)

[node name="AmmoLeft" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, -4.5, 0.85, 1.5)

[node name="AmmoRight" parent="." instance=ExtResource("11_ammo")]
transform = Transform3D(1.2, 0, 0, 0, 1.2, 0, 0, 0, 1.2, 4.5, 0.85, 1.5)

[node name="CrateL" parent="." instance=ExtResource("12_crate")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, -2.8, 0, 2.0)

[node name="CrateR" parent="." instance=ExtResource("12_crate")]
transform = Transform3D(1.1, 0, 0, 0, 1.1, 0, 0, 0, 1.1, 2.8, 0, 2.0)
"""

# Write all prop files
files_to_write = {
    "yard_jersey_barrier.tscn": JERSEY_BARRIER_TSCN,
    "yard_container_red.tscn": get_container_tscn("uid://yard_container_red_001", "0.72, 0.22, 0.18, 1", "Red"),
    "yard_container_blue.tscn": get_container_tscn("uid://yard_container_blue_001", "0.20, 0.42, 0.65, 1", "Blue"),
    "yard_container_yellow.tscn": get_container_tscn("uid://yard_container_yellow_001", "0.85, 0.65, 0.18, 1", "Yellow"),
    "yard_container_ramp_stack.tscn": CONTAINER_RAMP_STACK_TSCN,
    "yard_crate_stack.tscn": CRATE_STACK_TSCN,
    "yard_barrel_cluster.tscn": BARREL_CLUSTER_TSCN,
    "yard_freight_boxcar.tscn": FREIGHT_BOXCAR_TSCN,
    "yard_timber_stack.tscn": TIMBER_STACK_TSCN,
    "yard_perimeter_fence.tscn": PERIMETER_FENCE_TSCN,
    "yard_spawn_shed.tscn": SPAWN_SHED_TSCN,
}

for filename, content in files_to_write.items():
    filepath = os.path.join(PROPS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created prop: {filename} ({len(content)} bytes)")

print("Modular props built successfully.")
