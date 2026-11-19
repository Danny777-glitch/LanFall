# ============================================================================
# TargetDummy - Practice Target for LAN Fall Sandbox
# ============================================================================
# Takes damage, shows health overhead using a Label3D, flashes when hit,
# and respawns after 3 seconds when destroyed.
# ============================================================================
extends StaticBody3D

@export var max_health: int = 100
var current_health: int = 100
var is_dead: bool = false

@onready var label: Label3D = $Label3D
@onready var mesh: MeshInstance3D = $MeshInstance3D
@onready var collision_shape: CollisionShape3D = $CollisionShape3D
@onready var destroy_sound: AudioStreamPlayer3D = $DestroySound

const DAMAGE_NUMBER_SCENE = preload("res://scenes/objects/damage_number.tscn")

var default_color := Color(0.85, 0.25, 0.2, 1.0)
var flash_color := Color(1.0, 1.0, 1.0, 1.0)
var material: StandardMaterial3D


func _ready() -> void:
	add_to_group("targets")
	# Duplicate material so this dummy's flash doesn't affect other dummies
	material = StandardMaterial3D.new()
	material.albedo_color = default_color
	material.roughness = 0.5
	mesh.material_override = material
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
	material.albedo_color = flash_color
	await get_tree().create_timer(0.08).timeout
	if not is_dead:
		material.albedo_color = default_color


func _update_ui() -> void:
	label.text = "Dummy\nHP: %d / %d" % [current_health, max_health]
	var ratio := float(current_health) / float(max_health)
	if ratio > 0.6:
		label.modulate = Color(0.4, 1.0, 0.4)
	elif ratio > 0.3:
		label.modulate = Color(1.0, 0.8, 0.2)
	else:
		label.modulate = Color(1.0, 0.3, 0.3)


func _die() -> void:
	is_dead = true
	label.text = "💥 DESTROYED!\n(Respawning...)"
	label.modulate = Color(1.0, 0.2, 0.2)
	collision_shape.disabled = true

	var hud = get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("add_kill"):
		hud.add_kill("DUMMY")

	if destroy_sound:
		destroy_sound.play()

	# Shrink animation
	var tween := create_tween()
	tween.tween_property(mesh, "scale", Vector3.ZERO, 0.3).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)

	# Respawn after 3 seconds
	await get_tree().create_timer(3.0).timeout
	_respawn()


func _respawn() -> void:
	current_health = max_health
	is_dead = false
	collision_shape.disabled = false
	material.albedo_color = default_color
	_update_ui()

	# Pop-in animation
	var tween := create_tween()
	tween.tween_property(mesh, "scale", Vector3.ONE, 0.4).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
