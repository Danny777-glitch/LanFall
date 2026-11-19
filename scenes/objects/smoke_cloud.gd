# ============================================================================
# SmokeCloud - Stylized Tactical Billowing Smoke Cloud
# ============================================================================
extends Node3D

@export var duration: float = 12.0
@onready var core_smoke: CPUParticles3D = $CoreSmoke
@onready var ground_ring: MeshInstance3D = $GroundRing
@onready var area: Area3D = $Area3D
@onready var bloom_sound: AudioStreamPlayer3D = $BloomSound

var elapsed: float = 0.0
var local_player_inside: bool = false


func _ready() -> void:
	add_to_group("smoke")

	if area:
		area.body_entered.connect(_on_body_entered)
		area.body_exited.connect(_on_body_exited)

	# Sound whoosh on bloom
	if bloom_sound:
		bloom_sound.play()

	# Ground ring animation on detonation
	if ground_ring:
		ground_ring.scale = Vector3(0.01, 1.0, 0.01)
		var ring_tween := create_tween()
		ring_tween.tween_property(ground_ring, "scale", Vector3.ONE, 0.45).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

	# Smoke scale expand
	scale = Vector3.ZERO
	var tween := create_tween()
	tween.tween_property(self, "scale", Vector3.ONE, 0.35).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)


func _process(delta: float) -> void:
	elapsed += delta

	# Slowly rotate ground ring for high-tech tactical look
	if ground_ring:
		ground_ring.rotate_y(0.2 * delta)

	# Fade shrink out at the end
	if elapsed >= duration - 1.2:
		var remain := duration - elapsed
		scale = Vector3.ONE * clampf(remain / 1.2, 0.0, 1.0)

	if elapsed >= duration:
		_cleanup()


func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player") and ("is_local_player" in body and body.is_local_player):
		local_player_inside = true
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("set_smoke_blind"):
			hud.set_smoke_blind(true)


func _on_body_exited(body: Node) -> void:
	if body.is_in_group("player") and ("is_local_player" in body and body.is_local_player):
		local_player_inside = false
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("set_smoke_blind"):
			hud.set_smoke_blind(false)


func _cleanup() -> void:
	if local_player_inside:
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("set_smoke_blind"):
			hud.set_smoke_blind(false)
	queue_free()
