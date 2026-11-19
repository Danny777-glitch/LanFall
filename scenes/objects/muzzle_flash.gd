# ============================================================================
# MuzzleFlash - High impact visual weapon fire burst
# ============================================================================
extends Node3D

@onready var light: OmniLight3D = $OmniLight3D


func _ready() -> void:
	visible = false


func flash() -> void:
	visible = true
	rotation.z = randf_range(0.0, TAU)
	scale = Vector3.ONE * randf_range(0.9, 1.3)
	if light:
		light.light_energy = 2.6
		
	await get_tree().create_timer(0.045).timeout
	visible = false
