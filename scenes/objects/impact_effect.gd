# ============================================================================
# ImpactEffect - Bullet impact sparks and flash
# ============================================================================
extends Node3D

@onready var light: OmniLight3D = $OmniLight3D


func _ready() -> void:
	# Fade light quickly
	if light:
		var tween := create_tween()
		tween.tween_property(light, "light_energy", 0.0, 0.15)
	
	# Clean up after particles expire
	await get_tree().create_timer(0.4).timeout
	queue_free()
