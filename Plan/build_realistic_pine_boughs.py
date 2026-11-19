import os
import math

PROPS_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1\scenes\maps\warehouse\props"

# Build realistic 3D pine tree with drooping tiered branch boughs
lines = [
    '[gd_scene load_steps=8 format=3 uid="uid://realistic_pine_boughs_004"]',
    '',
    '[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_diff_1k.jpg" id="1_bark_diff"]',
    '[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_nor_gl_1k.jpg" id="2_bark_norm"]',
    '[ext_resource type="Texture2D" path="res://assets/textures/pbr/bark_brown_01_rough_1k.jpg" id="3_bark_rough"]',
    '[ext_resource type="Texture2D" path="res://assets/textures/pine_branch_realistic.png" id="4_bough"]',
    '',
    '[sub_resource type="StandardMaterial3D" id="Mat_TrunkBark"]',
    'albedo_texture = ExtResource("1_bark_diff")',
    'normal_enabled = true',
    'normal_texture = ExtResource("2_bark_norm")',
    'roughness_texture = ExtResource("3_bark_rough")',
    'roughness = 0.85',
    'uv1_scale = Vector3(1, 4, 1)',
    '',
    '[sub_resource type="StandardMaterial3D" id="Mat_PineBough"]',
    'transparency = 2',
    'alpha_scissor_threshold = 0.25',
    'cull_mode = 0',
    'albedo_texture = ExtResource("4_bough")',
    'roughness = 0.7',
    '',
    '[sub_resource type="CylinderMesh" id="Mesh_Trunk"]',
    'material = SubResource("Mat_TrunkBark")',
    'top_radius = 0.12',
    'bottom_radius = 0.38',
    'height = 8.5',
    'radial_segments = 12',
    '',
    '[sub_resource type="QuadMesh" id="Mesh_BoughL"]',
    'material = SubResource("Mat_PineBough")',
    'size = Vector2(2.6, 3.2)',
    '',
    '[sub_resource type="QuadMesh" id="Mesh_BoughM"]',
    'material = SubResource("Mat_PineBough")',
    'size = Vector2(2.2, 2.6)',
    '',
    '[sub_resource type="QuadMesh" id="Mesh_BoughS"]',
    'material = SubResource("Mat_PineBough")',
    'size = Vector2(1.7, 2.1)',
    '',
    '[sub_resource type="CylinderShape3D" id="Col_Trunk"]',
    'height = 8.5',
    'radius = 0.38',
    '',
    '[node name="PineTree" type="StaticBody3D"]',
    '',
    '[node name="Collision" type="CollisionShape3D" parent="."] ',
    'transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.25, 0)',
    'shape = SubResource("Col_Trunk")',
    '',
    '[node name="Trunk" type="MeshInstance3D" parent="."] ',
    'transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.25, 0)',
    'mesh = SubResource("Mesh_Trunk")',
    ''
]

# Generate tiers of realistic drooping boughs
tiers = [
    # (y_level, count, radius_offset, tilt_deg, mesh_id)
    (2.8, 6, 1.3, -22.0, "Mesh_BoughL"),
    (4.2, 6, 1.1, -20.0, "Mesh_BoughL"),
    (5.4, 5, 0.9, -18.0, "Mesh_BoughM"),
    (6.6, 5, 0.7, -15.0, "Mesh_BoughM"),
    (7.6, 4, 0.5, -12.0, "Mesh_BoughS"),
]

branch_idx = 0
for tier_num, (y_level, count, rad_dist, tilt_deg, mesh_id) in enumerate(tiers):
    offset_ang = (tier_num * 33.0) % 360.0
    tilt_rad = math.radians(tilt_deg)
    
    for i in range(count):
        branch_idx += 1
        ang_deg = offset_ang + (i * 360.0 / count)
        ang_rad = math.radians(ang_deg)
        
        # Position offset outward from trunk
        px = math.cos(ang_rad) * rad_dist
        pz = math.sin(ang_rad) * rad_dist
        py = y_level
        
        # Orientation: Rotate yaw to face outward (around Y), and tilt pitch down (around local X)
        # yaw rotation matrix around Y:
        # [ cos(ang), 0, sin(ang) ]
        # [    0,     1,    0     ]
        # [-sin(ang), 0, cos(ang) ]
        # pitch rotation around X:
        # [ 1,     0,          0      ]
        # [ 0,  cos(tilt), -sin(tilt) ]
        # [ 0,  sin(tilt),  cos(tilt) ]
        cy = math.cos(-ang_rad + math.pi/2)
        sy = math.sin(-ang_rad + math.pi/2)
        cp = math.cos(tilt_rad)
        sp = math.sin(tilt_rad)
        
        # Combined transform
        m00 = cy
        m01 = sy * sp
        m02 = sy * cp
        m10 = 0.0
        m11 = cp
        m12 = -sp
        m20 = -sy
        m21 = cy * sp
        m22 = cy * cp
        
        lines.append(f'[node name="Bough_{branch_idx}" type="MeshInstance3D" parent="."]')
        lines.append(f'transform = Transform3D({m00:.6f}, {m01:.6f}, {m02:.6f}, {m10:.6f}, {m11:.6f}, {m12:.6f}, {m20:.6f}, {m21:.6f}, {m22:.6f}, {px:.3f}, {py:.3f}, {pz:.3f})')
        lines.append(f'mesh = SubResource("{mesh_id}")')
        lines.append('')

with open(os.path.join(PROPS_DIR, "pine_tree.tscn"), "w") as f:
    f.write("\n".join(lines))

print("Saved realistic drooping tiered pine_tree.tscn with", branch_idx, "boughs")
