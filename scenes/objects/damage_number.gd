# ============================================================================
# DamageNumber - 3D Floating Combat Text
# ============================================================================
extends Node3D

@onready var label: Label3D = $Label3D
var velocity := Vector3.UP * 1.8
var life_timer := 0.65
var elapsed := 0.0


func setup(damage_amount: int, is_crit: bool = false) -> void:
	if not is_node_ready():
		await ready

	# Random slight horizontal drift
	velocity.x = randf_range(-0.4, 0.4)
	velocity.z = randf_range(-0.4, 0.4)

	if is_crit:
		label.text = "CRIT! %d" % damage_amount
		label.modulate = Color(1.0, 0.25, 0.2, 1.0)
		label.font_size = 48
	else:
		label.text = "-%d" % damage_amount
		label.modulate = Color(1.0, 0.88, 0.25, 1.0)
		label.font_size = 38


func _process(delta: float) -> void:
	elapsed += delta
	position += velocity * delta
	velocity.y = lerpf(velocity.y, 0.4, 4.0 * delta)

	# Fade out near end of life
	var progress := elapsed / life_timer
	if progress > 0.4:
		var alpha := 1.0 - ((progress - 0.4) / 0.6)
		label.modulate.a = clampf(alpha, 0.0, 1.0)

	if elapsed >= life_timer:
		queue_free()
