# ============================================================================
# SmokeProjectile - Throwable smoke capsule
# ============================================================================
extends RigidBody3D

const SMOKE_CLOUD_SCENE = preload("res://scenes/objects/smoke_cloud.tscn")
var has_bloomed: bool = false


func _ready() -> void:
	contact_monitor = true
	max_contacts_reported = 4
	body_entered.connect(_on_body_entered)


func _on_body_entered(_body: Node) -> void:
	if has_bloomed:
		return
	has_bloomed = true

	# Raycast downward to ensure the smoke cloud plants firmly on the ground
	var space_state := get_world_3d().direct_space_state
	var query := PhysicsRayQueryParameters3D.create(global_position + Vector3.UP * 0.4, global_position + Vector3.DOWN * 4.0)
	query.exclude = [get_rid()]
	var result := space_state.intersect_ray(query)

	var spawn_pos: Vector3 = result.position if result else global_position

	var cloud = SMOKE_CLOUD_SCENE.instantiate()
	get_tree().current_scene.add_child(cloud)
	cloud.global_position = spawn_pos
	queue_free()
