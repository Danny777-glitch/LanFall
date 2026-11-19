import os

MAP_PATH = "scenes/maps/test_map.tscn"

# Read original map
with open(MAP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Fix PointLight3D to OmniLight3D
content = content.replace('type="PointLight3D"', 'type="OmniLight3D"')

# Update Environment settings for "Super Visuals" (RTX 4060 Forward+)
old_env_str = """[sub_resource type="Environment" id="Environment_1"]
background_mode = 2
sky = SubResource("Sky_1")
ambient_light_source = 2
ambient_light_color = Color(0.55, 0.62, 0.74, 1)
ambient_light_energy = 0.52
tonemap_mode = 3
tonemap_exposure = 0.96
glow_enabled = true
glow_bloom = 0.04
glow_intensity = 0.45
fog_enabled = false"""

new_env_str = """[sub_resource type="Environment" id="Environment_1"]
background_mode = 2
sky = SubResource("Sky_1")
ambient_light_source = 2
ambient_light_color = Color(0.60, 0.68, 0.82, 1)
ambient_light_energy = 0.62
tonemap_mode = 3
tonemap_exposure = 1.06
glow_enabled = true
glow_bloom = 0.06
glow_intensity = 0.58
glow_blend_mode = 0
glow_hdr_threshold = 0.95
fog_enabled = true
fog_light_color = Color(0.70, 0.80, 0.95, 1)
fog_density = 0.002
fog_aerial_perspective = 0.72
fog_sky_affect = 0.65
fog_depth_begin = 35.0
fog_depth_end = 220.0"""

if old_env_str in content:
    content = content.replace(old_env_str, new_env_str)
    print("Replaced Environment settings")
else:
    print("Warning: exact old_env_str not found, check manually")

# Update Sun
old_sun = """[node name="Sun" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.707107, 0.40558, -0.579228, 0, 0.819152, 0.573576, 0.707107, -0.40558, 0.579228, 0, 35, 0)
light_color = Color(1, 0.95, 0.88, 1)
light_energy = 1.05
shadow_enabled = true
shadow_bias = 0.04"""

new_sun = """[node name="Sun" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.707107, 0.40558, -0.579228, 0, 0.819152, 0.573576, 0.707107, -0.40558, 0.579228, 0, 45, 0)
light_color = Color(1, 0.96, 0.90, 1)
light_energy = 1.18
shadow_enabled = true
shadow_bias = 0.03
shadow_blur = 1.8
directional_shadow_split_1 = 0.1
directional_shadow_split_2 = 0.25
directional_shadow_split_3 = 0.55
directional_shadow_blend_splits = true
directional_shadow_max_distance = 180.0"""

if old_sun in content:
    content = content.replace(old_sun, new_sun)
    print("Replaced Sun settings")

# Add new ext_resources after [ext_resource type="Texture2D" path="res://assets/textures/site_stencil_b.png" id="25_stencil_b"]
target_ext = '[ext_resource type="Texture2D" path="res://assets/textures/site_stencil_b.png" id="25_stencil_b"]'

new_ext_resources = """[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-skyscraper-a.glb" id="26_sky_a"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-skyscraper-b.glb" id="27_sky_b"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-skyscraper-c.glb" id="28_sky_c"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-skyscraper-d.glb" id="29_sky_d"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-skyscraper-e.glb" id="30_sky_e"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-a.glb" id="31_bldg_a"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-c.glb" id="32_bldg_c"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-g.glb" id="33_bldg_g"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-h.glb" id="34_bldg_h"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-j.glb" id="35_bldg_j"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-l.glb" id="36_bldg_l"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/building-m.glb" id="37_bldg_m"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/low-detail-building-wide-a.glb" id="38_low_wide_a"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/low-detail-building-wide-b.glb" id="39_low_wide_b"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/low-detail-building-h.glb" id="40_low_h"]
[ext_resource type="PackedScene" path="res://assets/models/commercial/Models/GLB format/low-detail-building-j.glb" id="41_low_j"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/building-sample-tower-a.glb" id="42_tower_a"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/building-sample-tower-b.glb" id="43_tower_b"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/building-sample-tower-c.glb" id="44_tower_c"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/building-sample-tower-d.glb" id="45_tower_d"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/building-sample-house-a.glb" id="46_house_a"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/roof-flat-detail-a.glb" id="47_roof_det_a"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/roof-flat-detail-d.glb" id="48_roof_det_d"]
[ext_resource type="PackedScene" path="res://assets/models/modular/Models/GLB format/detail-ac-a.glb" id="49_roof_ac"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_car_police.tscn" id="50_prop_police"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_truck.tscn" id="51_prop_truck"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_car_suv.tscn" id="52_prop_suv"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_fountain.tscn" id="53_prop_fountain"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_tree_tall.tscn" id="54_prop_tree_tall"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_tree_small.tscn" id="55_prop_tree_sm"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_dumpster.tscn" id="56_prop_dumpster"]
[ext_resource type="PackedScene" path="res://scenes/objects/prop_barrier.tscn" id="57_prop_barrier"]"""

if target_ext in content:
    content = content.replace(target_ext, target_ext + "\n" + new_ext_resources)
    print("Added new ext_resources")

# Calculate new load_steps count
# original load_steps=47 + 32 new ext_resources = 79
content = content.replace('load_steps=47', 'load_steps=79', 1)

# Now define all nodes to append to test_map.tscn
map_extensions = """
[node name="CitySkyline" type="Node3D" parent="."]

# ==================== NORTH SKYLINE (Z = -88 to -125) ====================
[node name="Skyscraper_N_Center" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(20, 0, 0, 0, 24, 0, 0, 0, 20, 0, 0, -88)

[node name="Skyscraper_N_Left" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, -28, 0, -86)

[node name="Skyscraper_N_Right" parent="CitySkyline" instance=ExtResource("28_sky_c")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 28, 0, -86)

[node name="Skyscraper_N_FarLeft" parent="CitySkyline" instance=ExtResource("29_sky_d")]
transform = Transform3D(16, 0, 0, 0, 24, 0, 0, 0, 16, -54, 0, -92)

[node name="Skyscraper_N_FarRight" parent="CitySkyline" instance=ExtResource("30_sky_e")]
transform = Transform3D(16, 0, 0, 0, 20, 0, 0, 0, 16, 54, 0, -92)

[node name="Distant_N_1" parent="CitySkyline" instance=ExtResource("38_low_wide_a")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, -20, 0, -125)

[node name="Distant_N_2" parent="CitySkyline" instance=ExtResource("39_low_wide_b")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, 20, 0, -125)

# ==================== SOUTH SKYLINE (Z = 86 to 125) ====================
[node name="Skyscraper_S_Center" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(20, 0, 0, 0, 24, 0, 0, 0, 20, 0, 0, 88)

[node name="Skyscraper_S_Left" parent="CitySkyline" instance=ExtResource("28_sky_c")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, -28, 0, 86)

[node name="Skyscraper_S_Right" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 28, 0, 86)

[node name="Skyscraper_S_FarLeft" parent="CitySkyline" instance=ExtResource("30_sky_e")]
transform = Transform3D(16, 0, 0, 0, 20, 0, 0, 0, 16, -54, 0, 92)

[node name="Skyscraper_S_FarRight" parent="CitySkyline" instance=ExtResource("29_sky_d")]
transform = Transform3D(16, 0, 0, 0, 24, 0, 0, 0, 16, 54, 0, 92)

[node name="Distant_S_1" parent="CitySkyline" instance=ExtResource("39_low_wide_b")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, -20, 0, 125)

[node name="Distant_S_2" parent="CitySkyline" instance=ExtResource("38_low_wide_a")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, 20, 0, 125)

# ==================== EAST SKYLINE - SITE A (X = 88 to 125) ====================
[node name="Skyscraper_E_Center" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(22, 0, 0, 0, 26, 0, 0, 0, 22, 88, 0, 0)

[node name="Skyscraper_E_North" parent="CitySkyline" instance=ExtResource("28_sky_c")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 90, 0, -32)

[node name="Skyscraper_E_South" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(18, 0, 0, 0, 24, 0, 0, 0, 18, 90, 0, 32)

[node name="Skyscraper_E_FarNorth" parent="CitySkyline" instance=ExtResource("29_sky_d")]
transform = Transform3D(16, 0, 0, 0, 24, 0, 0, 0, 16, 96, 0, -60)

[node name="Skyscraper_E_FarSouth" parent="CitySkyline" instance=ExtResource("30_sky_e")]
transform = Transform3D(16, 0, 0, 0, 20, 0, 0, 0, 16, 96, 0, 60)

[node name="Distant_E_1" parent="CitySkyline" instance=ExtResource("40_low_h")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, 125, 0, -15)

[node name="Distant_E_2" parent="CitySkyline" instance=ExtResource("41_low_j")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, 125, 0, 15)

# ==================== WEST SKYLINE - SITE B (X = -88 to -125) ====================
[node name="Skyscraper_W_Center" parent="CitySkyline" instance=ExtResource("30_sky_e")]
transform = Transform3D(22, 0, 0, 0, 24, 0, 0, 0, 22, -88, 0, 0)

[node name="Skyscraper_W_North" parent="CitySkyline" instance=ExtResource("29_sky_d")]
transform = Transform3D(18, 0, 0, 0, 24, 0, 0, 0, 18, -90, 0, -32)

[node name="Skyscraper_W_South" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(18, 0, 0, 0, 24, 0, 0, 0, 18, -90, 0, 32)

[node name="Skyscraper_W_FarNorth" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(16, 0, 0, 0, 22, 0, 0, 0, 16, -96, 0, -60)

[node name="Skyscraper_W_FarSouth" parent="CitySkyline" instance=ExtResource("28_sky_c")]
transform = Transform3D(16, 0, 0, 0, 22, 0, 0, 0, 16, -96, 0, 60)

[node name="Distant_W_1" parent="CitySkyline" instance=ExtResource("41_low_j")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, -125, 0, -15)

[node name="Distant_W_2" parent="CitySkyline" instance=ExtResource("40_low_h")]
transform = Transform3D(25, 0, 0, 0, 25, 0, 0, 0, 25, -125, 0, 15)

# ==================== 4 CORNER MEGA-TOWERS ====================
[node name="Skyscraper_NE" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(20, 0, 0, 0, 25, 0, 0, 0, 20, 82, 0, -82)

[node name="Skyscraper_NW" parent="CitySkyline" instance=ExtResource("28_sky_c")]
transform = Transform3D(20, 0, 0, 0, 24, 0, 0, 0, 20, -82, 0, -82)

[node name="Skyscraper_SE" parent="CitySkyline" instance=ExtResource("29_sky_d")]
transform = Transform3D(18, 0, 0, 0, 25, 0, 0, 0, 18, 82, 0, 82)

[node name="Skyscraper_SW" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(20, 0, 0, 0, 24, 0, 0, 0, 20, -82, 0, 82)


[node name="UrbanArchitecture" type="Node3D" parent="."]

# ==================== MID AVENUE FLANKING BUILDINGS ====================
[node name="Building_MidEast_Facade" parent="UrbanArchitecture" instance=ExtResource("32_bldg_c")]
transform = Transform3D(-7.5, 0, -6.55671e-07, 0, 7.5, 0, 6.55671e-07, 0, -7.5, 15.5, 0, -25)

[node name="Building_MidWest_Facade" parent="UrbanArchitecture" instance=ExtResource("34_bldg_h")]
transform = Transform3D(7.5, 0, 0, 0, 7.5, 0, 0, 0, 7.5, -15.5, 0, -25)

[node name="Building_SouthEast_Tower" parent="UrbanArchitecture" instance=ExtResource("42_tower_a")]
transform = Transform3D(-3.27835e-07, 0, 7.5, 0, 8.5, 0, -7.5, 0, -3.27835e-07, 17, 0, 38)

[node name="Building_SouthWest_Tower" parent="UrbanArchitecture" instance=ExtResource("44_tower_c")]
transform = Transform3D(-3.27835e-07, 0, -7.5, 0, 8.5, 0, 7.5, 0, -3.27835e-07, -17, 0, 38)

[node name="Building_NorthEast_Plaza" parent="UrbanArchitecture" instance=ExtResource("45_tower_d")]
transform = Transform3D(-3.27835e-07, 0, 7.5, 0, 8.5, 0, -7.5, 0, -3.27835e-07, 17, 0, -48)

[node name="Building_NorthWest_Plaza" parent="UrbanArchitecture" instance=ExtResource("43_tower_b")]
transform = Transform3D(-3.27835e-07, 0, -7.5, 0, 8.5, 0, 7.5, 0, -3.27835e-07, -17, 0, -48)

# ==================== SITE A CORPORATE RESEARCH COMPLEX ====================
[node name="Building_SiteA_Corp" parent="UrbanArchitecture" instance=ExtResource("35_bldg_j")]
transform = Transform3D(-3.0598e-07, 0, 7, 0, 7.5, 0, -7, 0, -3.0598e-07, 53, 0, -10)

[node name="Building_SiteA_Lab" parent="UrbanArchitecture" instance=ExtResource("33_bldg_g")]
transform = Transform3D(-3.0598e-07, 0, 7, 0, 7.5, 0, -7, 0, -3.0598e-07, 53, 0, 25)

[node name="Building_SiteA_Office" parent="UrbanArchitecture" instance=ExtResource("31_bldg_a")]
transform = Transform3D(-3.27835e-07, 0, 7.5, 0, 7.5, 0, -7.5, 0, -3.27835e-07, 48, 0, 8)

# ==================== SITE B HEAVY INDUSTRIAL COMPLEX ====================
[node name="Building_SiteB_Logistics" parent="UrbanArchitecture" instance=ExtResource("37_bldg_m")]
transform = Transform3D(-3.0598e-07, 0, -7, 0, 7.5, 0, 7, 0, -3.0598e-07, -56, 0, -10)

[node name="Building_SiteB_Substation" parent="UrbanArchitecture" instance=ExtResource("36_bldg_l")]
transform = Transform3D(-3.0598e-07, 0, -7, 0, 7.5, 0, 7, 0, -3.0598e-07, -56, 0, 25)

[node name="Building_SiteB_Depot" parent="UrbanArchitecture" instance=ExtResource("46_house_a")]
transform = Transform3D(-3.27835e-07, 0, -7.5, 0, 7.5, 0, 7.5, 0, -3.27835e-07, -50, 0, 8)


[node name="RooftopDetails" type="Node3D" parent="."]

# On Building A Tower Roof
[node name="RoofA_Chiller1" parent="RooftopDetails" instance=ExtResource("47_roof_det_a")]
transform = Transform3D(3.5, 0, 0, 0, 3.5, 0, 0, 0, 3.5, 31, 13, -12)

[node name="RoofA_AC1" parent="RooftopDetails" instance=ExtResource("49_roof_ac")]
transform = Transform3D(3.5, 0, 0, 0, 3.5, 0, 0, 0, 3.5, 37, 13, -8)

# On Building B Warehouse Roof
[node name="RoofB_Vent1" parent="RooftopDetails" instance=ExtResource("48_roof_det_d")]
transform = Transform3D(3.5, 0, 0, 0, 3.5, 0, 0, 0, 3.5, -41, 11.5, -12)

[node name="RoofB_Chiller1" parent="RooftopDetails" instance=ExtResource("47_roof_det_a")]
transform = Transform3D(3.5, 0, 0, 0, 3.5, 0, 0, 0, 3.5, -35, 11.5, -7)

# On Mid Market Roof
[node name="RoofMid_Chiller1" parent="RooftopDetails" instance=ExtResource("47_roof_det_a")]
transform = Transform3D(3.5, 0, 0, 0, 3.5, 0, 0, 0, 3.5, 3, 9.8, -22)


[node name="TacticalStreetProps" type="Node3D" parent="."]

# Central Mid Plaza Fountain
[node name="CentralFountain" parent="TacticalStreetProps" instance=ExtResource("53_prop_fountain")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 5)

# Lush Urban Canopy Trees
[node name="Tree_Plaza_NW" parent="TacticalStreetProps" instance=ExtResource("54_prop_tree_tall")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.5, 0, 5)

[node name="Tree_Plaza_NE" parent="TacticalStreetProps" instance=ExtResource("54_prop_tree_tall")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.5, 0, 5)

[node name="Tree_Plaza_SW" parent="TacticalStreetProps" instance=ExtResource("55_prop_tree_sm")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5.5, 0, -3)

[node name="Tree_Plaza_SE" parent="TacticalStreetProps" instance=ExtResource("55_prop_tree_sm")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5.5, 0, -3)

[node name="Tree_Alley_A" parent="TacticalStreetProps" instance=ExtResource("54_prop_tree_tall")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 17, 0, 42)

[node name="Tree_Alley_B" parent="TacticalStreetProps" instance=ExtResource("54_prop_tree_tall")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -17, 0, 42)

# Tactical Vehicles
[node name="Vehicle_Police_SiteA" parent="TacticalStreetProps" instance=ExtResource("50_prop_police")]
transform = Transform3D(0.866025, 0, 0.5, 0, 1, 0, -0.5, 0, 0.866025, 18, 0, 32)

[node name="Vehicle_Truck_SiteB" parent="TacticalStreetProps" instance=ExtResource("51_prop_truck")]
transform = Transform3D(0.965926, 0, -0.258819, 0, 1, 0, 0.258819, 0, 0.965926, -24, 0, -22)

[node name="Vehicle_SUV_Defender" parent="TacticalStreetProps" instance=ExtResource("52_prop_suv")]
transform = Transform3D(0.984808, 0, 0.173648, 0, 1, 0, -0.173648, 0, 0.984808, 5, 0, 48)

[node name="Vehicle_SUV_Attacker" parent="TacticalStreetProps" instance=ExtResource("52_prop_suv")]
transform = Transform3D(0.984808, 0, -0.173648, 0, 1, 0, 0.173648, 0, 0.984808, -5, 0, -48)

# Choke Barricades
[node name="Barrier_Mid_1" parent="TacticalStreetProps" instance=ExtResource("57_prop_barrier")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.5, 0, -10)

[node name="Barrier_Mid_2" parent="TacticalStreetProps" instance=ExtResource("57_prop_barrier")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.5, 0, -10)

[node name="Barrier_SiteA" parent="TacticalStreetProps" instance=ExtResource("57_prop_barrier")]
transform = Transform3D(0.707107, 0, 0.707107, 0, 1, 0, -0.707107, 0, 0.707107, 26, 0, 20)

[node name="Barrier_SiteB" parent="TacticalStreetProps" instance=ExtResource("57_prop_barrier")]
transform = Transform3D(0.707107, 0, -0.707107, 0, 1, 0, 0.707107, 0, 0.707107, -26, 0, 20)

# Urban Metal Dumpsters
[node name="Dumpster_SiteA" parent="TacticalStreetProps" instance=ExtResource("56_prop_dumpster")]
transform = Transform3D(-4.37114e-08, 0, 1, 0, 1, 0, -1, 0, -4.37114e-08, 15, 0, 10)

[node name="Dumpster_SiteB" parent="TacticalStreetProps" instance=ExtResource("56_prop_dumpster")]
transform = Transform3D(-4.37114e-08, 0, -1, 0, 1, 0, 1, 0, -4.37114e-08, -26, 0, 12)

[node name="Dumpster_Mid" parent="TacticalStreetProps" instance=ExtResource("56_prop_dumpster")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -11, 0, -18)
"""

content = content + map_extensions

with open(MAP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully enriched test_map.tscn with 32 skyscrapers, 12 buildings, 5 rooftop chillers, and 18 tactical street props!")
