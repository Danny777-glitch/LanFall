# ============================================================================
# test_spawns.gd — Automated Spawn System Validation Tool
# Run via: godot --script res://tools/test_spawns.gd
# ============================================================================
extends SceneTree

const PLAYER_HEIGHT := 1.8
const PLAYER_RADIUS := 0.40
const MIN_HEADROOM := 4.0
const MAX_GROUND_DISTANCE := 0.1
const MIN_CLEAR_FORWARD := 8.0

var total_pass := 0
var total_fail := 0


func _init() -> void:
	call_deferred("_run_validation")


func _run_validation() -> void:
	print("\n" + "=".repeat(70))
	print("       PHASE 1: AUTOMATED SPAWN SYSTEM VALIDATION REPORT")
	print("=".repeat(70))

	DirAccess.make_dir_recursive_absolute("docs/shots/round2")

	var map_packed := load("res://scenes/maps/warehouse/warehouse_map.tscn")
	var map_node: Node3D = map_packed.instantiate()
	root.add_child(map_node)

	# Allow physics world and colliders to initialize
	for f in range(25):
		await process_frame

	# Clear any auto-spawned practice players before validation
	var p_cont = map_node.get_node_or_null("Players")
	if p_cont:
		for c in p_cont.get_children():
			c.queue_free()
	for f in range(5):
		await process_frame

	var space := map_node.get_world_3d().direct_space_state
	if not space:
		print("CRITICAL ERROR: No physics space state available.")
		quit(1)
		return

	var spawns: Array = map_node.SPAWN_POINTS

	# 1. Test each spawn point individually
	for i in range(spawns.size()):
		var s: Dictionary = spawns[i]
		var pos: Vector3 = s["pos"]
		var rot_y: float = s["rot_y"]
		var team: int = s["team"]
		var fwd := Vector3(sin(rot_y), 0, cos(rot_y)).normalized()
		# When rot_y = PI (180 deg), sin(PI)=0, cos(PI)=-1 -> fwd = (0, 0, -1) [Facing -Z]
		# When rot_y = 0, sin(0)=0, cos(0)=1 -> fwd = (0, 0, 1) [Facing +Z]
		var label := "Spawn %d [Team %d] at %s" % [i, team, pos]
		print("\n--- Testing %s ---" % label)

		var ok_capsule := _check_capsule_overlap(space, pos, label)
		var ok_headroom := _check_headroom(space, pos, label)
		var ok_ground := _check_ground(space, pos, label)
		var ok_forward := _check_clear_forward(space, pos, fwd, label)
		var ok_los := _check_enemy_los(space, pos, team, spawns, label)

		if ok_capsule and ok_headroom and ok_ground and ok_forward and ok_los:
			print("  => ALL CHECKS PASS for %s" % label)
			total_pass += 1
		else:
			print("  => FAILED CHECKS for %s" % label)
			total_fail += 1

	# 2. Simulate actual player physics spawn and 60 physics frames
	print("\n--- Testing Live Player Physics Simulation (60 physics frames) ---")
	var player_packed := load("res://scenes/player/player.tscn")
	for i in range(spawns.size()):
		var s: Dictionary = spawns[i]
		var player_inst: CharacterBody3D = player_packed.instantiate()
		player_inst.position = s["pos"]
		player_inst.rotation.y = s["rot_y"]
		map_node.add_child(player_inst)

		var start_pos := player_inst.global_position
		for f in range(60):
			await process_frame

		var end_pos := player_inst.global_position
		var delta_y := end_pos.y - start_pos.y
		var horizontal_displacement := Vector2(end_pos.x - start_pos.x, end_pos.z - start_pos.z).length()

		# Player should remain stable on ground (delta_y around 0, no falling through world)
		if end_pos.y < -1.0:
			print("  ✗ FAIL: Player %d fell through world! End Y=%.2f" % [i, end_pos.y])
			total_fail += 1
		elif horizontal_displacement > 0.5:
			print("  ✗ FAIL: Player %d got pushed by geometry! Displacement=%.2fm" % [i, horizontal_displacement])
			total_fail += 1
		else:
			print("  ✓ PASS: Player %d simulated 60 physics frames cleanly at Y=%.3f" % [i, end_pos.y])

		# Capture screenshot from player eye position
		var cam := Camera3D.new()
		root.add_child(cam)
		cam.global_position = end_pos + Vector3(0, 1.6, 0)
		cam.rotation.y = s["rot_y"]
		cam.current = true

		for f in range(5):
			await process_frame

		var img := root.get_texture().get_image()
		if img and not img.is_empty():
			var out_file := "docs/shots/round2/spawn_eye_view_%d.png" % i
			img.save_png(out_file)
			print("    Saved eye-view screenshot: %s" % out_file)
		cam.queue_free()
		player_inst.queue_free()

	print("\n" + "=".repeat(70))
	print("  SPAWN VALIDATION SUMMARY: %d PASSED, %d FAILED" % [total_pass, total_fail])
	print("=".repeat(70) + "\n")

	quit(0 if total_fail == 0 else 1)


func _check_capsule_overlap(space: PhysicsDirectSpaceState3D, pos: Vector3, label: String) -> bool:
	var shape := CapsuleShape3D.new()
	shape.radius = PLAYER_RADIUS
	shape.height = PLAYER_HEIGHT

	var query := PhysicsShapeQueryParameters3D.new()
	query.shape = shape
	query.transform = Transform3D(Basis.IDENTITY, pos + Vector3(0, PLAYER_HEIGHT * 0.5, 0))
	query.collision_mask = 0xFFFFFFFF

	var hits := space.intersect_shape(query, 8)
	if hits.is_empty():
		print("  [Overlap]  PASS: 0 intersecting colliders inside player capsule.")
		return true
	else:
		var names: Array[String] = []
		for h in hits:
			if h.collider:
				names.append(h.collider.name)
		print("  [Overlap]  FAIL: Overlaps %d collider(s): %s" % [hits.size(), ", ".join(names)])
		return false


func _check_headroom(space: PhysicsDirectSpaceState3D, pos: Vector3, label: String) -> bool:
	# Raycast from head (pos + 1.8m) up to pos + 1.8m + MIN_HEADROOM
	var ray_start := pos + Vector3(0, PLAYER_HEIGHT, 0)
	var ray_end := ray_start + Vector3.UP * MIN_HEADROOM
	var query := PhysicsRayQueryParameters3D.create(ray_start, ray_end)
	var hit := space.intersect_ray(query)

	if hit.is_empty():
		print("  [Headroom] PASS: > %.1fm clear open headroom above." % MIN_HEADROOM)
		return true
	else:
		var hit_pos: Vector3 = hit["position"]
		var dist: float = ray_start.distance_to(hit_pos)
		print("  [Headroom] FAIL: Blocked overhead at %.2fm by %s" % [dist, hit.collider.name if hit.collider else "unknown"])
		return false


func _check_ground(space: PhysicsDirectSpaceState3D, pos: Vector3, label: String) -> bool:
	var ray_start := pos + Vector3(0, 0.5, 0)
	var ray_end := pos + Vector3.DOWN * 1.5
	var query := PhysicsRayQueryParameters3D.create(ray_start, ray_end)
	var hit := space.intersect_ray(query)

	if hit.is_empty():
		print("  [Ground]   FAIL: No ground detected below spawn.")
		return false
	var hit_pos: Vector3 = hit["position"]
	var dist_below: float = pos.y - hit_pos.y
	if abs(dist_below) <= MAX_GROUND_DISTANCE:
		print("  [Ground]   PASS: Ground detected at y=%.3f (dist=%.3fm <= %.2fm)." % [hit_pos.y, dist_below, MAX_GROUND_DISTANCE])
		return true
	else:
		print("  [Ground]   FAIL: Ground distance %.3fm exceeds %.2fm." % [dist_below, MAX_GROUND_DISTANCE])
		return false


func _check_clear_forward(space: PhysicsDirectSpaceState3D, pos: Vector3, fwd: Vector3, label: String) -> bool:
	var ray_start := pos + Vector3(0, 1.2, 0) # chest height
	var ray_end := ray_start + fwd * MIN_CLEAR_FORWARD
	var query := PhysicsRayQueryParameters3D.create(ray_start, ray_end)
	var hit := space.intersect_ray(query)

	if hit.is_empty():
		print("  [Forward]  PASS: Clear forward vision >= %.1fm." % MIN_CLEAR_FORWARD)
		return true
	else:
		var hit_pos: Vector3 = hit["position"]
		var dist: float = ray_start.distance_to(hit_pos)
		if dist >= MIN_CLEAR_FORWARD:
			print("  [Forward]  PASS: Obstacle at %.2fm (>= %.1fm)." % [dist, MIN_CLEAR_FORWARD])
			return true
		else:
			print("  [Forward]  FAIL: Forward line blocked at %.2fm by %s" % [dist, hit.collider.name if hit.collider else "unknown"])
			return false


func _check_enemy_los(space: PhysicsDirectSpaceState3D, pos: Vector3, my_team: int, all_spawns: Array, label: String) -> bool:
	var eye_pos := pos + Vector3(0, 1.6, 0)
	var all_blocked := true

	for s in all_spawns:
		if s["team"] != my_team:
			var enemy_eye: Vector3 = s["pos"] + Vector3(0, 1.6, 0)
			var query := PhysicsRayQueryParameters3D.create(eye_pos, enemy_eye)
			var hit := space.intersect_ray(query)
			if hit.is_empty():
				print("  [LOS Check] FAIL: Unobstructed direct line of sight to enemy spawn at %s!" % s["pos"])
				all_blocked = false
			else:
				# Blocked by geometry as required!
				pass

	if all_blocked:
		print("  [LOS Check] PASS: Direct line of sight to all enemy spawns is fully BLOCKED by central structures.")
		return true
	return false
