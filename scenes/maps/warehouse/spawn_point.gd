# ============================================================================
# spawn_point.gd — Dedicated Tactical Spawn Marker
# ============================================================================
class_name SpawnPoint
extends Marker3D

@export_enum("Team1_South:1", "Team2_North:2") var team: int = 1
@export var safe_radius: float = 2.5
@export var facing_direction: Vector3 = Vector3.FORWARD

func get_spawn_transform() -> Transform3D:
	var t := global_transform
	# Ensure facing direction matches transform basis
	return t
