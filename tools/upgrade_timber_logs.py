import os

def upgrade_timber_logs():
    path = "scenes/maps/warehouse/props/bgmi_timber_logs.tscn"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Increase radial segments of Mesh_HorizontalLog from 14 to 32
    text = text.replace("radial_segments = 14", "radial_segments = 32")

    # Add steel band material and mesh if not present
    if "Mat_SteelBand" not in text:
        band_mat_def = '''
[sub_resource type="StandardMaterial3D" id="Mat_SteelBand"]
albedo_color = Color(0.18, 0.19, 0.22, 1)
metallic = 0.95
roughness = 0.32

[sub_resource type="BoxMesh" id="Mesh_StrapH"]
material = SubResource("Mat_SteelBand")
size = Vector3(0.06, 0.03, 2.7)

[sub_resource type="BoxMesh" id="Mesh_StrapV"]
material = SubResource("Mat_SteelBand")
size = Vector3(0.06, 2.2, 0.03)

[sub_resource type="BoxMesh" id="Mesh_RatchetBuckle"]
material = SubResource("Mat_SteelBand")
size = Vector3(0.12, 0.15, 0.08)
'''
        text = text.replace('[sub_resource type="BoxShape3D" id="Col_LogStack"]', band_mat_def + '\n[sub_resource type="BoxShape3D" id="Col_LogStack"]')

        # Add band nodes at the end
        strap_nodes = '''
# Heavy Steel Cargo Tension Straps & Ratchet Buckles
[node name="Strap_Top_L" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.1, 2.25, 0)
mesh = SubResource("Mesh_StrapH")

[node name="Strap_Top_R" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.1, 2.25, 0)
mesh = SubResource("Mesh_StrapH")

[node name="Strap_Front_L" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.1, 1.1, 1.34)
mesh = SubResource("Mesh_StrapV")

[node name="Strap_Front_R" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.1, 1.1, 1.34)
mesh = SubResource("Mesh_StrapV")

[node name="Strap_Back_L" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.1, 1.1, -1.34)
mesh = SubResource("Mesh_StrapV")

[node name="Strap_Back_R" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.1, 1.1, -1.34)
mesh = SubResource("Mesh_StrapV")

[node name="Buckle_L" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.1, 1.45, 1.36)
mesh = SubResource("Mesh_RatchetBuckle")

[node name="Buckle_R" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.1, 1.45, 1.36)
mesh = SubResource("Mesh_RatchetBuckle")
'''
        text += strap_nodes

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Timber logs upgraded with 32 radial segments and steel tension straps.")

if __name__ == "__main__":
    upgrade_timber_logs()
