# ============================================================================
# CharacterModel — Stylized 3D Operative Model (Lobby & In-Game)
# ============================================================================
# Supports full real-time customization of suits, armor plates, glowing visors,
# weapons, and skins with procedural idle breathing & interactive rotation.
# ============================================================================
extends Node3D

@onready var torso_mesh: MeshInstance3D = $Rig/Torso
@onready var chest_plate: MeshInstance3D = $Rig/Torso/ChestPlate
@onready var core_mesh: MeshInstance3D = $Rig/Torso/ChestPlate/Core
@onready var head_mesh: MeshInstance3D = $Rig/Head
@onready var visor_mesh: MeshInstance3D = $Rig/Head/Visor
@onready var shoulder_l: MeshInstance3D = $Rig/ShoulderL
@onready var shoulder_r: MeshInstance3D = $Rig/ShoulderR
@onready var leg_l: MeshInstance3D = $Rig/LegL
@onready var leg_r: MeshInstance3D = $Rig/LegR
@onready var rig_node: Node3D = $Rig

# Weapons
@onready var wp_rifle: Node3D = $Rig/WeaponMount/Rifle
@onready var wp_pistol: Node3D = $Rig/WeaponMount/Pistol
@onready var wp_sniper: Node3D = $Rig/WeaponMount/Sniper
@onready var wp_knife: Node3D = $Rig/WeaponMount/Knife
@onready var weapon_mount: Node3D = $Rig/WeaponMount

# Procedural Idle Animation
var idle_time: float = 0.0
var base_torso_y: float = 1.05
var base_head_y: float = 1.58
var base_wp_y: float = 1.08
var target_rotation_y: float = 0.0
var is_dragging: bool = false
var enable_idle: bool = true

# Dynamic Material Copies
var suit_mat: StandardMaterial3D
var armor_mat: StandardMaterial3D
var visor_mat: StandardMaterial3D
var wp_primary_mat: StandardMaterial3D
var wp_accent_mat: StandardMaterial3D
var wp_glow_mat: StandardMaterial3D


func _ready() -> void:
	_init_materials()
	apply_from_profile()


func _init_materials() -> void:
	suit_mat = StandardMaterial3D.new()
	suit_mat.roughness = 0.5
	suit_mat.metallic = 0.3

	armor_mat = StandardMaterial3D.new()
	armor_mat.roughness = 0.35
	armor_mat.metallic = 0.65

	visor_mat = StandardMaterial3D.new()
	visor_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	visor_mat.emission_enabled = true
	visor_mat.emission_energy_multiplier = 3.5

	wp_primary_mat = StandardMaterial3D.new()
	wp_accent_mat = StandardMaterial3D.new()
	wp_glow_mat = StandardMaterial3D.new()
	wp_glow_mat.emission_enabled = true
	wp_glow_mat.emission_energy_multiplier = 2.8

	_bind_materials_to_nodes()


func _bind_materials_to_nodes() -> void:
	if torso_mesh: torso_mesh.material_override = suit_mat
	if leg_l: leg_l.material_override = suit_mat
	if leg_r: leg_r.material_override = suit_mat

	# Arms & Gloves
	var arm_nodes := ["UpperArmL", "UpperArmR", "ForearmL", "ForearmR"]
	for a_name in arm_nodes:
		if rig_node:
			var node = rig_node.get_node_or_null(a_name)
			if node and node is MeshInstance3D:
				(node as MeshInstance3D).material_override = suit_mat

	var hand_nodes := ["HandL", "HandR"]
	for h_name in hand_nodes:
		if rig_node:
			var node = rig_node.get_node_or_null(h_name)
			if node and node is MeshInstance3D:
				(node as MeshInstance3D).material_override = armor_mat

	# Armor & Helmet
	if chest_plate: chest_plate.material_override = armor_mat
	if head_mesh: head_mesh.material_override = armor_mat
	if shoulder_l: shoulder_l.material_override = armor_mat
	if shoulder_r: shoulder_r.material_override = armor_mat

	# Boots
	if rig_node:
		var boot_l = rig_node.get_node_or_null("LegL/BootL")
		if boot_l and boot_l is MeshInstance3D:
			(boot_l as MeshInstance3D).material_override = armor_mat
		var boot_r = rig_node.get_node_or_null("LegR/BootR")
		if boot_r and boot_r is MeshInstance3D:
			(boot_r as MeshInstance3D).material_override = armor_mat

	if core_mesh: core_mesh.material_override = visor_mat
	if visor_mesh: visor_mesh.material_override = visor_mat

	# Weapon nodes
	_apply_weapon_materials(wp_rifle)
	_apply_weapon_materials(wp_pistol)
	_apply_weapon_materials(wp_sniper)
	_apply_weapon_materials(wp_knife)



func _apply_weapon_materials(wp_node: Node3D) -> void:
	if not wp_node: return
	for child in wp_node.find_children("*", "MeshInstance3D", true, false):
		var m := child as MeshInstance3D
		if "Glow" in m.name or "Edge" in m.name or "Reticle" in m.name:
			m.material_override = wp_glow_mat
		elif "Rail" in m.name or "Accent" in m.name or "Muzzle" in m.name or "Blade" in m.name:
			m.material_override = wp_accent_mat
		else:
			m.material_override = wp_primary_mat


func apply_from_profile() -> void:
	var prof := get_node_or_null("/root/ProfileManager")
	if not prof:
		return
	apply_customization(
		prof.get_current_suit(),
		prof.get_current_visor_color(),
		prof.current_weapon_index,
		prof.get_current_weapon_skin()
	)


func apply_customization(suit: Dictionary, visor_color: Color, weapon_idx: int, skin: Dictionary) -> void:
	if not suit_mat:
		_init_materials()

	# 1. Apply Suit & Armor colors
	suit_mat.albedo_color = suit.get("suit_color", Color(0.12, 0.15, 0.20))
	suit_mat.metallic = suit.get("metallic", 0.4)
	suit_mat.roughness = suit.get("roughness", 0.5)

	armor_mat.albedo_color = suit.get("armor_color", Color(0.2, 0.22, 0.28))
	armor_mat.metallic = clampf(suit.get("metallic", 0.4) + 0.2, 0.0, 1.0)
	armor_mat.roughness = clampf(suit.get("roughness", 0.5) - 0.15, 0.1, 1.0)

	# 2. Apply Visor & Core Glow
	visor_mat.albedo_color = visor_color
	visor_mat.emission = visor_color

	# 3. Apply Weapon Skin
	wp_primary_mat.albedo_color = skin.get("primary_color", Color(0.15, 0.16, 0.18))
	wp_primary_mat.metallic = skin.get("metallic", 0.7)
	wp_primary_mat.roughness = skin.get("roughness", 0.35)

	wp_accent_mat.albedo_color = skin.get("accent_color", Color(0.3, 0.32, 0.36))
	wp_accent_mat.metallic = skin.get("metallic", 0.7)
	wp_accent_mat.roughness = skin.get("roughness", 0.35)

	wp_glow_mat.albedo_color = skin.get("glow_color", visor_color)
	wp_glow_mat.emission = skin.get("glow_color", visor_color)

	# 4. Display Weapon
	set_held_weapon(weapon_idx)


func set_held_weapon(index: int) -> void:
	if wp_rifle: wp_rifle.visible = (index == 0)
	if wp_pistol: wp_pistol.visible = (index == 1)
	if wp_sniper: wp_sniper.visible = (index == 2)
	if wp_knife: wp_knife.visible = (index == 3)


func _process(delta: float) -> void:
	if enable_idle:
		idle_time += delta * 2.2
		var breath := sin(idle_time) * 0.016
		var sway := cos(idle_time * 0.5) * 0.008

		if torso_mesh:
			torso_mesh.position.y = base_torso_y + breath
			torso_mesh.rotation.z = sway * 0.5
		if head_mesh:
			head_mesh.position.y = base_head_y + (breath * 1.2)
		if weapon_mount:
			weapon_mount.position.y = base_wp_y + (breath * 0.8)
			weapon_mount.rotation.x = breath * 0.8

	# Smooth rotation for lobby inspection
	rotation.y = lerp_angle(rotation.y, target_rotation_y, 14.0 * delta)


func rotate_model(delta_degrees: float) -> void:
	target_rotation_y += deg_to_rad(delta_degrees)


func reset_rotation() -> void:
	target_rotation_y = 0.0
