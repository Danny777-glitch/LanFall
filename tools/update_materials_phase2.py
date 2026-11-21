import os
import re

def update_file(path, old_pattern, new_text, is_regex=False):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if is_regex:
        new_content, count = re.subn(old_pattern, new_text, content, flags=re.DOTALL)
    else:
        new_content = content.replace(old_pattern, new_text)
        count = 1 if new_content != content else 0
        
    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {path} ({count} replacements)")
        return True
    else:
        print(f"No changes made to {path}")
        return False

def upgrade_tdm_warehouse():
    path = "scenes/maps/warehouse/props/bgmi_tdm_warehouse.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Replace corrugated iron ExtResources
    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_siding_diff"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_diffuse_4k.jpg" id="1_siding_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_siding_norm"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_nor_gl_4k.jpg" id="2_siding_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_siding_rough"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_arm_4k.jpg" id="3_siding_rough"'
    )

    # Check if dirty concrete 4k exists
    if os.path.exists("assets/textures/pbr_4k/dirty_concrete/dirty_concrete_diffuse_4k.jpg"):
        text = text.replace(
            'path="res://assets/textures/pbr/dirty_concrete_diff_1k.jpg" id="4_concrete_diff"',
            'path="res://assets/textures/pbr_4k/dirty_concrete/dirty_concrete_diffuse_4k.jpg" id="4_concrete_diff"'
        )
        text = text.replace(
            'path="res://assets/textures/pbr/dirty_concrete_nor_gl_1k.jpg" id="5_concrete_norm"',
            'path="res://assets/textures/pbr_4k/dirty_concrete/dirty_concrete_nor_gl_4k.jpg" id="5_concrete_norm"'
        )
        text = text.replace(
            'path="res://assets/textures/pbr/dirty_concrete_rough_1k.jpg" id="6_concrete_rough"',
            'path="res://assets/textures/pbr_4k/dirty_concrete/dirty_concrete_arm_4k.jpg" id="6_concrete_rough"'
        )

    # Update Mat_WarehouseSiding: enable AO from ARM texture channel 0, roughness from channel 1
    old_siding_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_WarehouseSiding"]\n'
        'albedo_texture = ExtResource("1_siding_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_siding_norm")\n'
        'roughness_texture = ExtResource("3_siding_rough")\n'
        'roughness = 0.6\n'
        'metallic = 0.7\n'
        'uv1_scale = Vector3(2.0, 2.0, 2.0)\n'
        'uv1_triplanar = true'
    )
    new_siding_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_WarehouseSiding"]\n'
        'albedo_texture = ExtResource("1_siding_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_siding_norm")\n'
        'roughness_texture = ExtResource("3_siding_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.65\n'
        'metallic = 0.75\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_siding_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(2.0, 2.0, 2.0)\n'
        'uv1_triplanar = true'
    )
    text = text.replace(old_siding_mat, new_siding_mat)

    # Update Mat_Floor
    old_floor_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_Floor"]\n'
        'albedo_texture = ExtResource("4_concrete_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("5_concrete_norm")\n'
        'roughness_texture = ExtResource("6_concrete_rough")\n'
        'roughness = 0.8\n'
        'uv1_scale = Vector3(4.0, 4.0, 4.0)\n'
        'uv1_triplanar = true'
    )
    new_floor_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_Floor"]\n'
        'albedo_texture = ExtResource("4_concrete_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("5_concrete_norm")\n'
        'roughness_texture = ExtResource("6_concrete_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.85\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("6_concrete_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(0.35, 0.35, 0.35)\n'
        'uv1_triplanar = true'
    )
    text = text.replace(old_floor_mat, new_floor_mat)

    # Update Mat_SteelBeams: realistic dark industrial steel with micro-sheen
    old_beam_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_SteelBeams"]\n'
        'albedo_color = Color(0.2, 0.22, 0.26, 1)\n'
        'metallic = 0.85\n'
        'roughness = 0.35'
    )
    new_beam_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_SteelBeams"]\n'
        'albedo_color = Color(0.18, 0.20, 0.24, 1)\n'
        'metallic = 0.88\n'
        'roughness = 0.38\n'
        'metallic_specular = 0.65'
    )
    text = text.replace(old_beam_mat, new_beam_mat)

    # Update Mat_MetalRoof
    old_roof_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_MetalRoof"]\n'
        'albedo_color = Color(0.48, 0.52, 0.56, 1)\n'
        'albedo_texture = ExtResource("1_siding_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_siding_norm")\n'
        'roughness_texture = ExtResource("3_siding_rough")\n'
        'metallic = 0.75\n'
        'roughness = 0.5\n'
        'uv1_scale = Vector3(0.4, 0.4, 0.4)\n'
        'uv1_triplanar = true'
    )
    new_roof_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_MetalRoof"]\n'
        'albedo_color = Color(0.50, 0.54, 0.58, 1)\n'
        'albedo_texture = ExtResource("1_siding_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_siding_norm")\n'
        'roughness_texture = ExtResource("3_siding_rough")\n'
        'roughness_texture_channel = 1\n'
        'metallic = 0.75\n'
        'roughness = 0.55\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_siding_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(0.5, 0.5, 0.5)\n'
        'uv1_triplanar = true'
    )
    text = text.replace(old_roof_mat, new_roof_mat)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Warehouse scene materials upgraded.")

def upgrade_spawn_sheds():
    path = "scenes/maps/warehouse/props/bgmi_spawn_sheds.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Update wood planks ExtResource to 4K
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="1_wood_diff"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_diffuse_4k.jpg" id="1_wood_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="2_wood_norm"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_nor_gl_4k.jpg" id="2_wood_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="3_wood_rough"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_arm_4k.jpg" id="3_wood_rough"'
    )

    # Update roof ExtResource to 4K
    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="4_roof_diff"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_diffuse_4k.jpg" id="4_roof_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="5_roof_norm"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_nor_gl_4k.jpg" id="5_roof_norm"'
    )

    # Update Mat_DarkWoodPlanks
    old_wood_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_DarkWoodPlanks"]\n'
        'albedo_color = Color(0.48, 0.40, 0.32, 1)\n'
        'albedo_texture = ExtResource("1_wood_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_wood_norm")\n'
        'roughness_texture = ExtResource("3_wood_rough")\n'
        'roughness = 0.85\n'
        'uv1_scale = Vector3(2, 3, 1)'
    )
    new_wood_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_DarkWoodPlanks"]\n'
        'albedo_color = Color(0.48, 0.40, 0.32, 1)\n'
        'albedo_texture = ExtResource("1_wood_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_wood_norm")\n'
        'roughness_texture = ExtResource("3_wood_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.85\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_wood_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(2, 3, 1)'
    )
    text = text.replace(old_wood_mat, new_wood_mat)

    # Update Mat_TimberPosts
    old_post_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_TimberPosts"]\n'
        'albedo_color = Color(0.38, 0.30, 0.24, 1)\n'
        'albedo_texture = ExtResource("1_wood_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_wood_norm")\n'
        'roughness_texture = ExtResource("3_wood_rough")\n'
        'roughness = 0.8\n'
        'uv1_scale = Vector3(0.5, 3, 0.5)'
    )
    new_post_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_TimberPosts"]\n'
        'albedo_color = Color(0.38, 0.30, 0.24, 1)\n'
        'albedo_texture = ExtResource("1_wood_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_wood_norm")\n'
        'roughness_texture = ExtResource("3_wood_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.82\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_wood_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(0.5, 3, 0.5)'
    )
    text = text.replace(old_post_mat, new_post_mat)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Spawn sheds scene materials upgraded.")

def upgrade_wooden_pergola():
    path = "scenes/maps/warehouse/props/bgmi_wooden_pergola.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="1_wood_diff"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_diffuse_4k.jpg" id="1_wood_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="2_wood_norm"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_nor_gl_4k.jpg" id="2_wood_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_rough_1k.jpg" id="3_wood_rough"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_arm_4k.jpg" id="3_wood_rough"'
    )

    old_pergola_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_PergolaTimber"]\n'
        'albedo_color = Color(0.42, 0.34, 0.26, 1)\n'
        'albedo_texture = ExtResource("1_wood_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_wood_norm")\n'
        'roughness_texture = ExtResource("3_wood_rough")\n'
        'roughness = 0.85\n'
        'uv1_scale = Vector3(1, 4, 1)'
    )
    new_pergola_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_PergolaTimber"]\n'
        'albedo_color = Color(0.42, 0.34, 0.26, 1)\n'
        'albedo_texture = ExtResource("1_wood_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_wood_norm")\n'
        'roughness_texture = ExtResource("3_wood_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.85\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_wood_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(1, 4, 1)'
    )
    text = text.replace(old_pergola_mat, new_pergola_mat)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Wooden pergola scene materials upgraded.")

def upgrade_perimeter_fence():
    path = "scenes/maps/warehouse/props/bgmi_perimeter_fence.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="1_wood_diff"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_diffuse_4k.jpg" id="1_wood_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="2_wood_norm"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_nor_gl_4k.jpg" id="2_wood_norm"'
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Perimeter fence scene materials upgraded.")

def upgrade_train_boxcar():
    path = "scenes/maps/warehouse/props/bgmi_train_boxcar.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_diff_1k.jpg" id="1_car_diff"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_diffuse_4k.jpg" id="1_car_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_nor_gl_1k.jpg" id="2_car_norm"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_nor_gl_4k.jpg" id="2_car_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/corrugated_iron_02_rough_1k.jpg" id="3_car_rough"',
        'path="res://assets/textures/pbr_4k/corrugated_iron_02/corrugated_iron_02_arm_4k.jpg" id="3_car_rough"'
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Train boxcar scene materials upgraded.")

if __name__ == "__main__":
    upgrade_tdm_warehouse()
    upgrade_spawn_sheds()
    upgrade_wooden_pergola()
    upgrade_perimeter_fence()
    upgrade_train_boxcar()
