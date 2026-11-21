# ============================================================================
# TargetDummy - Tactical Steel Humanoid Practice Target
# ============================================================================
extends StaticBody3D

@export var max_health: int = 100
var current_health: int = 100
var is_dead: bool = false

@onready var label: Label3D = $Label3D
@onready var target_body: Node3D = $TargetBody
@onready var torso_mesh: MeshInstance3D = $TargetBody/PlateTorso
@onready var head_mesh: MeshInstance3D = $TargetBody/PlateHead
@onready var bullseye_mesh: MeshInstance3D = $TargetBody/BullseyeZone
@onready var collision_shape: CollisionShape3D = $CollisionShape3D
@onready var destroy_sound: AudioStreamPlayer3D = $DestroySound

const DAMAGE_NUMBER_SCENE = preload("res://scenes/objects/damage_number.tscn")

var default_plate_color := Color(0.24, 0.28, 0.32, 1.0)
var default_bullseye_color := Color(0.92, 0.30, 0.22, 1.0)
var flash_color := Color(1.0, 1.0, 1.0, 1.0)

var mat_torso: StandardMaterial3D
var mat_bullseye: StandardMaterial3D


func _ready() -> void:
	add_to_group("targets")
	mat_torso = StandardMaterial3D.new()
	mat_torso.albedo_color = default_plate_color
	mat_torso.metallic = 0.7
	mat_torso.roughness = 0.4
	torso_mesh.material_override = mat_torso
	head_mesh.material_override = mat_torso

	mat_bullseye = StandardMaterial3D.new()
	mat_bullseye.albedo_color = default_bullseye_color
	mat_bullseye.metallic = 0.5
	mat_bullseye.roughness = 0.35
	bullseye_mesh.material_override = mat_bullseye

	_update_ui()


func take_damage(amount: int) -> void:
	if is_dead:
		return

	current_health = clampi(current_health - amount, 0, max_health)
	_flash_hit()
	_update_ui()
	_spawn_damage_number(amount)

	if current_health <= 0:
		_die()


func _spawn_damage_number(amount: int) -> void:
	var dmg = DAMAGE_NUMBER_SCENE.instantiate()
	get_tree().current_scene.add_child(dmg)
	dmg.global_position = global_position + Vector3(randf_range(-0.2, 0.2), 1.8, randf_range(-0.2, 0.2))
	dmg.setup(amount, amount >= 40)


func _flash_hit() -> void:
	mat_torso.albedo_color = flash_color
	mat_bullseye.albedo_color = flash_color
	await get_tree().create_timer(0.08).timeout
	if not is_dead:
		mat_torso.albedo_color = default_plate_color
		mat_bullseye.albedo_color = default_bullseye_color


func _update_ui() -> void:
	label.text = "Target Dummy\nHP: %d / %d" % [current_health, max_health]
	var ratio := float(current_health) / float(max_health)
	if ratio > 0.6:
		label.modulate = Color(0.4, 1.0, 0.4)
	elif ratio > 0.3:
		label.modulate = Color(1.0, 0.8, 0.2)
	else:
		label.modulate = Color(1.0, 0.3, 0.3)


func _die() -> void:
	is_dead = true
	label.text = "💥 DESTROYED!\n(Resetting...)"
	label.modulate = Color(1.0, 0.2, 0.2)
	collision_shape.disabled = true

	var hud = get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("add_kill"):
		hud.add_kill("TARGET")

	if destroy_sound:
		destroy_sound.play()

	# Collapse / fold flat animation
	var tween := create_tween()
	tween.tween_property(target_body, "scale", Vector3(1.0, 0.05, 1.0), 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)

	# Respawn after 3 seconds
	await get_tree().create_timer(3.0).timeout
	_respawn()


func _respawn() -> void:
	current_health = max_health
	is_dead = false
	collision_shape.disabled = false
	mat_torso.albedo_color = default_plate_color
	mat_bullseye.albedo_color = default_bullseye_color
	_update_ui()

	# Pop-up animation
	var tween := create_tween()
	tween.tween_property(target_body, "scale", Vector3.ONE, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
