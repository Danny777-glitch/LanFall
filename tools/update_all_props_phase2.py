import os
import re

def upgrade_jersey_barrier():
    path = "scenes/maps/warehouse/props/bgmi_jersey_barrier.tscn"
    if not os.path.exists("assets/textures/pbr_4k/chipped_concrete/chipped_concrete_diffuse_4k.jpg"):
        return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace(
        'path="res://assets/textures/pbr/chipped_concrete_diff_1k.jpg" id="1_conc_diff"',
        'path="res://assets/textures/pbr_4k/chipped_concrete/chipped_concrete_diffuse_4k.jpg" id="1_conc_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/chipped_concrete_nor_gl_1k.jpg" id="2_conc_norm"',
        'path="res://assets/textures/pbr_4k/chipped_concrete/chipped_concrete_nor_gl_4k.jpg" id="2_conc_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/chipped_concrete_rough_1k.jpg" id="3_conc_rough"',
        'path="res://assets/textures/pbr_4k/chipped_concrete/chipped_concrete_arm_4k.jpg" id="3_conc_rough"'
    )

    old_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_BarrierConcrete"]\n'
        'albedo_texture = ExtResource("1_conc_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_conc_norm")\n'
        'roughness_texture = ExtResource("3_conc_rough")\n'
        'roughness = 0.85\n'
        'uv1_scale = Vector3(1.5, 1, 1)'
    )
    new_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_BarrierConcrete"]\n'
        'albedo_texture = ExtResource("1_conc_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("2_conc_norm")\n'
        'roughness_texture = ExtResource("3_conc_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.88\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("3_conc_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(1.5, 1, 1)'
    )
    text = text.replace(old_mat, new_mat)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Jersey barrier materials upgraded to 4K chipped concrete.")

def upgrade_backdrop_villa():
    path = "scenes/maps/warehouse/props/bgmi_backdrop_villa.tscn"
    if not os.path.exists("assets/textures/pbr_4k/clay_roof_tiles_02/clay_roof_tiles_02_diffuse_4k.jpg"):
        return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace(
        'path="res://assets/textures/pbr/clay_roof_tiles_02_diff_1k.jpg" id="3_roof_diff"',
        'path="res://assets/textures/pbr_4k/clay_roof_tiles_02/clay_roof_tiles_02_diffuse_4k.jpg" id="3_roof_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/clay_roof_tiles_02_nor_gl_1k.jpg" id="4_roof_norm"',
        'path="res://assets/textures/pbr_4k/clay_roof_tiles_02/clay_roof_tiles_02_nor_gl_4k.jpg" id="4_roof_norm"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/clay_roof_tiles_02_rough_1k.jpg" id="5_roof_rough"',
        'path="res://assets/textures/pbr_4k/clay_roof_tiles_02/clay_roof_tiles_02_arm_4k.jpg" id="5_roof_rough"'
    )

    old_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_VillaRoof"]\n'
        'albedo_texture = ExtResource("3_roof_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("4_roof_norm")\n'
        'roughness_texture = ExtResource("5_roof_rough")\n'
        'roughness = 0.7\n'
        'uv1_scale = Vector3(4, 3, 1)'
    )
    new_mat = (
        '[sub_resource type="StandardMaterial3D" id="Mat_VillaRoof"]\n'
        'albedo_texture = ExtResource("3_roof_diff")\n'
        'normal_enabled = true\n'
        'normal_texture = ExtResource("4_roof_norm")\n'
        'roughness_texture = ExtResource("5_roof_rough")\n'
        'roughness_texture_channel = 1\n'
        'roughness = 0.72\n'
        'ao_enabled = true\n'
        'ao_texture = ExtResource("5_roof_rough")\n'
        'ao_texture_channel = 0\n'
        'uv1_scale = Vector3(4, 3, 1)'
    )
    text = text.replace(old_mat, new_mat)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Backdrop villa roof upgraded to 4K clay roof tiles.")

def upgrade_container_ramp():
    path = "scenes/maps/warehouse/props/bgmi_container_ramp.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Upgrade wood ramp to 4K brown planks
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_diff_1k.jpg" id="4_wood_diff"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_diffuse_4k.jpg" id="4_wood_diff"'
    )
    text = text.replace(
        'path="res://assets/textures/pbr/brown_planks_08_nor_gl_1k.jpg" id="5_wood_norm"',
        'path="res://assets/textures/pbr_4k/brown_planks_08/brown_planks_08_nor_gl_4k.jpg" id="5_wood_norm"'
    )

    if os.path.exists("assets/textures/pbr_4k/container_side/container_side_diffuse_4k.jpg"):
        text = text.replace(
            'path="res://assets/textures/pbr/container_side_diff_1k.jpg" id="1_cont_diff"',
            'path="res://assets/textures/pbr_4k/container_side/container_side_diffuse_4k.jpg" id="1_cont_diff"'
        )
        text = text.replace(
            'path="res://assets/textures/pbr/container_side_nor_gl_1k.jpg" id="2_cont_norm"',
            'path="res://assets/textures/pbr_4k/container_side/container_side_nor_gl_4k.jpg" id="2_cont_norm"'
        )
        text = text.replace(
            'path="res://assets/textures/pbr/container_side_rough_1k.jpg" id="3_cont_rough"',
            'path="res://assets/textures/pbr_4k/container_side/container_side_arm_4k.jpg" id="3_cont_rough"'
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Container ramp upgraded.")

def upgrade_warehouse_map_terrain():
    path = "scenes/maps/warehouse/warehouse_map.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Check if asphalt 4k exists
    if os.path.exists("assets/textures/pbr_4k/asphalt_02/asphalt_02_diffuse_4k.jpg"):
        # Add asphalt ext resources if not present
        if 'id="asphalt_diff_4k"' not in text:
            # Add after 8_sky
            insert_marker = '[ext_resource type="Texture2D" path="res://assets/textures/sky_erangel_daylight.png" id="8_sky"]'
            asphalt_resources = (
                '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/asphalt_02/asphalt_02_diffuse_4k.jpg" id="asphalt_diff_4k"]\n'
                '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/asphalt_02/asphalt_02_nor_gl_4k.jpg" id="asphalt_norm_4k"]\n'
                '[ext_resource type="Texture2D" path="res://assets/textures/pbr_4k/asphalt_02/asphalt_02_arm_4k.jpg" id="asphalt_arm_4k"]\n'
            )
            text = text.replace(insert_marker, insert_marker + '\n' + asphalt_resources)

        # Update Mat_DirtRoadways to use 4K Asphalt!
        old_road_mat = (
            '[sub_resource type="StandardMaterial3D" id="Mat_DirtRoadways"]\n'
            'albedo_texture = ExtResource("5_dirt_diff")\n'
            'normal_enabled = true\n'
            'normal_texture = ExtResource("6_dirt_norm")\n'
            'roughness_texture = ExtResource("7_dirt_rough")\n'
            'roughness = 0.92\n'
            'uv1_scale = Vector3(3, 3, 3)\n'
            'uv1_triplanar = true'
        )
        new_road_mat = (
            '[sub_resource type="StandardMaterial3D" id="Mat_DirtRoadways"]\n'
            'albedo_texture = ExtResource("asphalt_diff_4k")\n'
            'normal_enabled = true\n'
            'normal_texture = ExtResource("asphalt_norm_4k")\n'
            'roughness_texture = ExtResource("asphalt_arm_4k")\n'
            'roughness_texture_channel = 1\n'
            'roughness = 0.82\n'
            'ao_enabled = true\n'
            'ao_texture = ExtResource("asphalt_arm_4k")\n'
            'ao_texture_channel = 0\n'
            'uv1_scale = Vector3(0.5, 0.5, 0.5)\n'
            'uv1_triplanar = true'
        )
        text = text.replace(old_road_mat, new_road_mat)

    # If sparse_grass 2k exists
    if os.path.exists("assets/textures/pbr_4k/sparse_grass/sparse_grass_diffuse_2k.jpg"):
        text = text.replace(
            'path="res://assets/textures/pbr/sparse_grass_diff_1k.jpg" id="2_grass_diff"',
            'path="res://assets/textures/pbr_4k/sparse_grass/sparse_grass_diffuse_2k.jpg" id="2_grass_diff"'
        )
        text = text.replace(
            'path="res://assets/textures/pbr/sparse_grass_nor_gl_1k.jpg" id="3_grass_norm"',
            'path="res://assets/textures/pbr_4k/sparse_grass/sparse_grass_nor_gl_2k.jpg" id="3_grass_norm"'
        )
        text = text.replace(
            'path="res://assets/textures/pbr/sparse_grass_rough_1k.jpg" id="4_grass_rough"',
            'path="res://assets/textures/pbr_4k/sparse_grass/sparse_grass_arm_2k.jpg" id="4_grass_rough"'
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Warehouse map terrain materials upgraded.")

if __name__ == "__main__":
    upgrade_jersey_barrier()
    upgrade_backdrop_villa()
    upgrade_container_ramp()
    upgrade_warehouse_map_terrain()
