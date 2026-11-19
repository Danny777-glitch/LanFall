import os

MAP_PATH = "scenes/maps/test_map.tscn"

with open(MAP_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 1. Update DirectionalLight3D shadow max distance to 65.0 to eliminate lag
content = "".join(lines)
content = content.replace("directional_shadow_max_distance = 180.0", "directional_shadow_max_distance = 65.0\nshadow_blur = 1.2")

# 2. Cut out from [node name="CitySkyline" type="Node3D" parent="."] to the end
idx_cut = content.find('[node name="CitySkyline"')
if idx_cut == -1:
    print("Error: CitySkyline not found")
    exit(1)

base_content = content[:idx_cut].strip()

# 3. New Valorant-style Tactical Architecture & Cover
valorant_layout = """
[node name="CitySkyline" type="Node3D" parent="."]

[node name="Sky_North_1" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, -15, 0, -88)

[node name="Sky_North_2" parent="CitySkyline" instance=ExtResource("28_sky_c")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 15, 0, -88)

[node name="Sky_South_1" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, -15, 0, 88)

[node name="Sky_South_2" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 15, 0, 88)

[node name="Sky_East_1" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(20, 0, 0, 0, 24, 0, 0, 0, 20, 88, 0, -20)

[node name="Sky_East_2" parent="CitySkyline" instance=ExtResource("27_sky_b")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 88, 0, 20)

[node name="Sky_West_1" parent="CitySkyline" instance=ExtResource("30_sky_e")]
transform = Transform3D(20, 0, 0, 0, 22, 0, 0, 0, 20, -88, 0, -20)

[node name="Sky_West_2" parent="CitySkyline" instance=ExtResource("29_sky_d")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, -88, 0, 20)

[node name="Sky_Corner_NE" parent="CitySkyline" instance=ExtResource("28_sky_c")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 80, 0, -80)

[node name="Sky_Corner_NW" parent="CitySkyline" instance=ExtResource("29_sky_d")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, -80, 0, -80)

[node name="Sky_Corner_SE" parent="CitySkyline" instance=ExtResource("30_sky_e")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, 80, 0, 80)

[node name="Sky_Corner_SW" parent="CitySkyline" instance=ExtResource("26_sky_a")]
transform = Transform3D(18, 0, 0, 0, 22, 0, 0, 0, 18, -80, 0, 80)


[node name="ValorantBuildings" type="Node3D" parent="."]

[node name="MidEast_Shop" parent="ValorantBuildings" instance=ExtResource("32_bldg_c")]
transform = Transform3D(-3.0598e-07, 0, 7, 0, 7.5, 0, -7, 0, -3.0598e-07, 9, 0, -5)

[node name="MidEast_Tower" parent="ValorantBuildings" instance=ExtResource("42_tower_a")]
transform = Transform3D(-3.0598e-07, 0, 7, 0, 8, 0, -7, 0, -3.0598e-07, 9, 0, 14)

[node name="MidWest_Hotel" parent="ValorantBuildings" instance=ExtResource("34_bldg_h")]
transform = Transform3D(-3.0598e-07, 0, -7, 0, 7.5, 0, 7, 0, -3.0598e-07, -9, 0, -5)

[node name="MidWest_Tower" parent="ValorantBuildings" instance=ExtResource("44_tower_c")]
transform = Transform3D(-3.0598e-07, 0, -7, 0, 8, 0, 7, 0, -3.0598e-07, -9, 0, 14)

[node name="MidNorth_ArchFacade" parent="ValorantBuildings" instance=ExtResource("46_house_a")]
transform = Transform3D(7, 0, 0, 0, 7.5, 0, 0, 0, 7, 0, 0, -34)

[node name="ALong_East_Tower" parent="ValorantBuildings" instance=ExtResource("45_tower_d")]
transform = Transform3D(-3.0598e-07, 0, 7, 0, 8, 0, -7, 0, -3.0598e-07, 19, 0, 30)

[node name="ALong_West_Shop" parent="ValorantBuildings" instance=ExtResource("31_bldg_a")]
transform = Transform3D(-3.0598e-07, 0, 7, 0, 7.5, 0, -7, 0, -3.0598e-07, 19, 0, 10)

[node name="SiteA_Corp_Wing" parent="ValorantBuildings" instance=ExtResource("35_bldg_j")]
transform = Transform3D(-2.84124e-07, 0, 6.5, 0, 7.5, 0, -6.5, 0, -2.84124e-07, 46, 0, -10)

[node name="SiteA_Lab_Wing" parent="ValorantBuildings" instance=ExtResource("33_bldg_g")]
transform = Transform3D(-2.84124e-07, 0, 6.5, 0, 7.5, 0, -6.5, 0, -2.84124e-07, 46, 0, 22)

[node name="BLong_West_Tower" parent="ValorantBuildings" instance=ExtResource("43_tower_b")]
transform = Transform3D(-3.0598e-07, 0, -7, 0, 8, 0, 7, 0, -3.0598e-07, -19, 0, 30)

[node name="BLong_East_Substation" parent="ValorantBuildings" instance=ExtResource("36_bldg_l")]
transform = Transform3D(-3.0598e-07, 0, -7, 0, 7.5, 0, 7, 0, -3.0598e-07, -19, 0, 10)

[node name="SiteB_Logistics_Wing" parent="ValorantBuildings" instance=ExtResource("37_bldg_m")]
transform = Transform3D(-2.84124e-07, 0, -6.5, 0, 7.5, 0, 6.5, 0, -2.84124e-07, -48, 0, -10)

[node name="SiteB_Depot_Wing" parent="ValorantBuildings" instance=ExtResource("46_house_a")]
transform = Transform3D(-2.84124e-07, 0, -6.5, 0, 7.5, 0, 6.5, 0, -2.84124e-07, -48, 0, 22)


[node name="RooftopDetails" type="Node3D" parent="."]

[node name="RoofA_Chiller" parent="RooftopDetails" instance=ExtResource("47_roof_det_a")]
transform = Transform3D(3.2, 0, 0, 0, 3.2, 0, 0, 0, 3.2, 31, 13, -12)

[node name="RoofA_AC" parent="RooftopDetails" instance=ExtResource("49_roof_ac")]
transform = Transform3D(3.2, 0, 0, 0, 3.2, 0, 0, 0, 3.2, 37, 13, -8)

[node name="RoofB_Vent" parent="RooftopDetails" instance=ExtResource("48_roof_det_d")]
transform = Transform3D(3.2, 0, 0, 0, 3.2, 0, 0, 0, 3.2, -41, 11.5, -12)

[node name="RoofB_Chiller" parent="RooftopDetails" instance=ExtResource("47_roof_det_a")]
transform = Transform3D(3.2, 0, 0, 0, 3.2, 0, 0, 0, 3.2, -35, 11.5, -7)

[node name="RoofMid_Chiller" parent="RooftopDetails" instance=ExtResource("47_roof_det_a")]
transform = Transform3D(3.2, 0, 0, 0, 3.2, 0, 0, 0, 3.2, 3, 9.8, -22)


[node name="TacticalValorantCover" type="Node3D" parent="."]

[node name="CentralFountain" parent="TacticalValorantCover" instance=ExtResource("53_prop_fountain")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 4)

[node name="PlazaTreeLeft" parent="TacticalValorantCover" instance=ExtResource("54_prop_tree_tall")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4.5, 0, 4)

[node name="PlazaTreeRight" parent="TacticalValorantCover" instance=ExtResource("54_prop_tree_tall")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4.5, 0, 4)

[node name="RadStack_SiteA_Base1" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 31.5, 0.4, 25)

[node name="RadStack_SiteA_Base2" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 33.1, 0.4, 25)

[node name="RadStack_SiteA_Top" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 32.3, 1.9, 25)

[node name="RadCrate_SiteA_Back" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 38, 0.4, 30)

[node name="RadStack_SiteB_Base1" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -34.5, 0.4, 25)

[node name="RadStack_SiteB_Base2" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -36.1, 0.4, 25)

[node name="RadStack_SiteB_Top" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -35.3, 1.9, 25)

[node name="RadCrate_SiteB_Catwalk" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -41, 0.4, 28)

[node name="RadStack_Mid_Base1" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.5, 0, -8)

[node name="RadStack_Mid_Base2" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.5, 0, -9.6)

[node name="RadStack_Mid_Top" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3.5, 1.5, -8.8)

[node name="RadCrate_Mid_West" parent="TacticalValorantCover" instance=ExtResource("18_radcrate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3.5, 0, -8.5)

[node name="TacticalCrate_ALong_1" parent="TacticalValorantCover" instance=ExtResource("17_crate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 18, 0, 22)

[node name="TacticalCrate_ALong_2" parent="TacticalValorantCover" instance=ExtResource("17_crate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 18, 1.4, 22)

[node name="TacticalCrate_BLong_1" parent="TacticalValorantCover" instance=ExtResource("17_crate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -18, 0, 22)

[node name="TacticalCrate_BLong_2" parent="TacticalValorantCover" instance=ExtResource("17_crate")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -18, 1.4, 22)

[node name="TacticalBarrier_A_Site" parent="TacticalValorantCover" instance=ExtResource("57_prop_barrier")]
transform = Transform3D(0.707107, 0, 0.707107, 0, 1, 0, -0.707107, 0, 0.707107, 26, 0, 18)

[node name="TacticalBarrier_B_Site" parent="TacticalValorantCover" instance=ExtResource("57_prop_barrier")]
transform = Transform3D(0.707107, 0, -0.707107, 0, 1, 0, 0.707107, 0, 0.707107, -26, 0, 18)

[node name="TacticalBarrier_Mid_North" parent="TacticalValorantCover" instance=ExtResource("57_prop_barrier")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -12)
"""

final_content = base_content + "\n" + valorant_layout

with open(MAP_PATH, "w", encoding="utf-8") as f:
    f.write(final_content)

print("Applied Valorant-style tight building lanes, Radianite double-stacked crate cover, zero vehicles, and optimized performance!")
