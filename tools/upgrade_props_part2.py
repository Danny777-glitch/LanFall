import os
import re

def update_timber_logs():
    path = "scenes/maps/warehouse/props/bgmi_timber_logs.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Bark 4k
    text = text.replace(
        'path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="1_bark_diff"',
        'path="res://assets/textures/pbr_4k/bark_brown_01/bark_brown_01_diffuse_4k.jpg" id="1_bark_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="2_bark_norm"',
        'path="res://assets/textures/pbr_4k/bark_brown_01/bark_brown_01_nor_gl_4k.jpg" id="2_bark_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/bark_brown_01_rough_1k.jpg" id="3_bark_rough"',
        'path="res://assets/textures/pbr_4k/bark_brown_01/bark_brown_01_arm_4k.jpg" id="3_bark_rough"'
    )
    # Stanchion planks 4k
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_diffuse_4k.jpg" id="4_wood_diff"'
    )

    old_bark_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_Bark"]\n'
        'albedo_color = Color(0.45, 0.38, 0.32, 1)\n'
        'albedo_texture = ExtResource("1_bark_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_bark_norm")\n'
        'roughness_texture = ExtResource("3_bark_rough")\n'
        'roughness = 0.88\n'
        'uv1_scale = Vector3(1, 3, 1)'
    )
    new_bark_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_Bark"]\n'
        'albedo_color = Color(0.65, 0.58, 0.52, 1)\n'
        'albedo_texture = ExtResource("1_bark_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_bark_norm")\n'
        'roughness_texture = ExtResource("3_bark_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.88\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_bark_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(1, 3, 1)'
    )
    text = text.replace(old_bark_mat, new_bark_mat)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Timber logs upgraded to 4K bark.")

def update_pine_tree():
    path = "scenes/maps/warehouse/props/pine_tree.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace(
        'path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="1_bark_diff"',
        'path="res://assets/textures/pbr_4k/bark_brown_01/bark_brown_01_diffuse_4k.jpg" id="1_bark_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="2_bark_norm"',
        'path="res://assets/textures/pbr_4k/bark_brown_01/bark_brown_01_nor_gl_4k.jpg" id="2_bark_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/bark_brown_01_rough_1k.jpg" id="3_bark_rough"',
        'path="res://assets/textures/pbr_4k/bark_brown_01/bark_brown_01_arm_4k.jpg" id="3_bark_rough"'
    )

    old_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_TrunkBark"]\n'
        'albedo_texture = ExtResource("1_bark_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_bark_norm")\n'
        'roughness_texture = ExtResource("3_bark_rough")\n'
        'roughness = 0.85\n'
        'uv1_scale = Vector3(1, 4, 1)'
    )
    new_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_TrunkBark"]\n'
        'albedo_texture = ExtResource("1_bark_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_bark_norm")\n'
        'roughness_texture = ExtResource("3_bark_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.85\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_bark_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(1, 4, 1)'
    )
    text = text.replace(old_mat, new_mat)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Pine tree trunk upgraded to 4K bark.")

def update_tactical_crate():
    path = "scenes/maps/warehouse/props/tactical_crate.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    new_header = (
        '[gd_scene load_steps=10 format=3 uid="uid://tactical_crate_001"]\n\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_diffuse_4k.jpg" id="1_planks_diff"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_nor_gl_4k.jpg" id="2_planks_norm"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_arm_4k.jpg" id="3_planks_arm"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_MilitaryWood"]\n'
        'albedo_color = Color(0.72, 0.65, 0.52, 1)\n'
        'albedo_texture = ExtResource("1_planks_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_planks_norm")\n'
        'roughness_texture = ExtResource("3_planks_arm")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.75\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_planks_arm")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(1.2, 1.2, 1.2)\n'
        'uv1_triplanar = true\n'
    )

    old_header = (
        '[gd_scene load_steps=9 format=3 uid="uid://tactical_crate_001"]\n\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_albedo.png" id="1_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_normal.png" id="2_normal"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_MilitaryWood"]\n'
        'albedo_texture = ExtResource("1_albedo")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_normal")\n'
        'roughness = 0.65\n'
        'uv1_scale = Vector3(1, 1, 1)\n'
    )
    if old_header in text:
        text = text.replace(old_header, new_header)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Tactical crate upgraded to 4K brown planks.")
    else:
        print("Could not match old_header in tactical_crate.tscn")

def update_bgmi_crate_stack():
    path = "scenes/maps/warehouse/props/bgmi_crate_stack.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    new_header = (
        '[gd_scene load_steps=6 format=3 uid="uid://bgmi_crate_stack_003"]\n\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_diffuse_4k.jpg" id="1_crate_diff"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_nor_gl_4k.jpg" id="2_crate_norm"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_arm_4k.jpg" id="3_crate_arm"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_WoodCrate"]\n'
        'albedo_color = Color(0.72, 0.65, 0.52, 1)\n'
        'albedo_texture = ExtResource("1_crate_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_crate_norm")\n'
        'roughness_texture = ExtResource("3_crate_arm")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.82\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_crate_arm")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(1.2, 1.2, 1.2)\n'
        'uv1_triplanar = true\n'
    )
    old_header = (
        '[gd_scene load_steps=5 format=3 uid="uid://bgmi_crate_stack_003"]\n\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_albedo.png" id="1_crate_diff"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/wood_military_crate_normal.png" id="2_crate_norm"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_WoodCrate"]\n'
        'albedo_texture = ExtResource("1_crate_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_crate_norm")\n'
        'roughness = 0.78\n'
    )
    if old_header in text:
        text = text.replace(old_header, new_header)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("BGMI Crate Stack upgraded to 4K brown planks.")
    else:
        print("Could not match old_header in bgmi_crate_stack.tscn")

def update_container_rust():
    path = "scenes/maps/warehouse/props/container_rust_prop.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    new_header = (
        '[gd_scene load_steps=9 format=3 uid="uid://container_rust_001"]\n\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/container_side/container_side_diffuse_4k.jpg" id="1_cont_diff"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/container_side/container_side_nor_gl_4k.jpg" id="2_cont_norm"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/container_side/container_side_arm_4k.jpg" id="3_cont_arm"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_RustContainer"]\n'
        'albedo_color = Color(0.85, 0.48, 0.38, 1)\n'
        'albedo_texture = ExtResource("1_cont_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_cont_norm")\n'
        'roughness_texture = ExtResource("3_cont_arm")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.65\n'
        'metallic_texture = ExtResource("3_cont_arm")\n'
        'metallic_texture_channel = 2\n'
        'metallic = 0.65\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_cont_arm")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(0.35, 0.35, 0.35)\n'
        'uv1_triplanar = true\n'
    )
    old_header = (
        '[gd_scene load_steps=8 format=3 uid="uid://container_rust_001"]\n\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/container_rust_albedo.png" id="1_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/container_rust_normal.png" id="2_normal"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_RustContainer"]\n'
        'albedo_texture = ExtResource("1_albedo")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_normal")\n'
        'metallic = 0.65\n'
        'roughness = 0.55\n'
        'uv1_scale = Vector3(0.4, 0.4, 0.4)\n'
        'uv1_triplanar = true\n'
    )
    if old_header in text:
        text = text.replace(old_header, new_header)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Container Rust upgraded to 4K container_side.")
    else:
        print("Could not match old_header in container_rust_prop.tscn")

def update_container_yellow():
    path = "scenes/maps/warehouse/props/container_yellow_prop.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    new_block = (
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/container_side/container_side_diffuse_4k.jpg" id="1_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/container_side/container_side_nor_gl_4k.jpg" id="2_normal"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/container_side/container_side_arm_4k.jpg" id="cont_arm_4k"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/container_doors_albedo.png" id="3_door_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/container_doors_normal.png" id="4_door_normal"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_YellowContainer"]\n'
        'albedo_color = Color(0.95, 0.78, 0.28, 1)\n'
        'albedo_texture = ExtResource("1_albedo")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_normal")\n'
        'roughness_texture = ExtResource("cont_arm_4k")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.55\n'
        'metallic_texture = ExtResource("cont_arm_4k")\n'
        'metallic_texture_channel = 2\n'
        'metallic = 0.65\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("cont_arm_4k")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(0.35, 0.35, 0.35)\n'
        'uv1_triplanar = true'
    )
    old_block = (
        '[ext_resource type="Texture2D" path="res://assets/textures/container_yellow_albedo.png" id="1_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/container_yellow_normal.png" id="2_normal"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/container_doors_albedo.png" id="3_door_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/container_doors_normal.png" id="4_door_normal"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_YellowContainer"]\n'
        'albedo_texture = ExtResource("1_albedo")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_normal")\n'
        'metallic = 0.7\n'
        'roughness = 0.45\n'
        'uv1_scale = Vector3(0.4, 0.4, 0.4)\n'
        'uv1_triplanar = true'
    )
    if old_block in text:
        text = text.replace(old_block, new_block)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Container Yellow upgraded to 4K container_side.")
    else:
        print("Could not match old_block in container_yellow_prop.tscn")

def update_prop_barrier():
    path = "scenes/maps/warehouse/props/prop_barrier.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    new_block = (
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/chipped_concrete/chipped_concrete_diffuse_4k.jpg" id="1_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/chipped_concrete/chipped_concrete_nor_gl_4k.jpg" id="2_normal"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/chipped_concrete/chipped_concrete_arm_4k.jpg" id="conc_arm_4k"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_JerseyConcrete"]\n'
        'albedo_texture = ExtResource("1_albedo")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_normal")\n'
        'roughness_texture = ExtResource("conc_arm_4k")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.88\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("conc_arm_4k")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(1.2, 1.2, 1.2)\n'
        'uv1_triplanar = true'
    )
    old_block = (
        '[ext_resource type="Texture2D" path="res://assets/textures/concrete_barrier_albedo.png" id="1_albedo"]\n'
        '[ext_resource type="Texture2D" path="res://assets/textures/concrete_barrier_normal.png" id="2_normal"]\n\n'
        '[sub_resource type="StandardMaterial3D" id="Mat_JerseyConcrete"]\n'
        'albedo_texture = ExtResource("1_albedo")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_normal")\n'
        'roughness = 0.85\n'
        'uv1_scale = Vector3(1, 1, 1)'
    )
    if old_block in text:
        text = text.replace(old_block, new_block)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("Prop barrier upgraded to 4K chipped concrete.")
    else:
        print("Could not match old_block in prop_barrier.tscn")

if __name__ == "__main__":
    update_timber_logs()
    update_pine_tree()
    update_tactical_crate()
    update_bgmi_crate_stack()
    update_container_rust()
    update_container_yellow()
    update_prop_barrier()
