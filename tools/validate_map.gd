# ============================================================================
# validate_map.gd — Comprehensive Level Geometry & Placement Validator
# Run via: godot --headless --script res://tools/validate_map.gd
# ============================================================================
extends SceneTree

const MAP_SCENE_PATH := "res://scenes/maps/warehouse/warehouse_map.tscn"

const MAX_FLOATING_DIST := 0.08
const MAX_TILT_DEG := 5.0
const MAP_BOUNDS_X := 24.5
const MAP_BOUNDS_Z := 53.0

var total_props := 0
var pass_count := 0
var fail_count := 0
var failure_reports: Array[Dictionary] = []


func _init() -> void:
	call_deferred("_run_validation")


func _run_validation() -> void:
	print("\n" + "=".repeat(75))
	print("       PHASE 3: AUTOMATED MAP PLACEMENT & PROP VALIDATION REPORT")
	print("=".repeat(75))

	var packed := load(MAP_SCENE_PATH)
	if not packed:
		print("CRITICAL: Failed to load map scene: %s" % MAP_SCENE_PATH)
		quit(1)
		return

	var map_root: Node3D = packed.instantiate()
	root.add_child(map_root)

	# Process frames so transforms and physics state are initialized
	for f in range(20):
		await process_frame

	var space := map_root.get_world_3d().direct_space_state
	if not space:
		print("CRITICAL: Physics space not available.")
		quit(1)
		return

	# Collect all prop instances in the scene
	_validate_node_recursive(map_root, space)

	print("\n" + "=".repeat(75))
	print("  PROP VALIDATION SUMMARY: Checked %d props | %d PASS | %d FAIL" % [
		total_props, pass_count, fail_count
	])
	print("=".repeat(75))

	if failure_reports.is_empty():
		print("\n>>> ALL MAP PROPS ARE ZERO-DEFECT: 0 floating, 0 shear, 0 out-of-bounds, all collisions verified! <<<\n")
		quit(0)
	else:
		print("\nFAILURES LIST (%d items):" % failure_reports.size())
		for r in failure_reports:
			print("  ✗ [%s] at %s" % [r["path"], r["pos"]])
			for issue in r["issues"]:
				print("      - %s" % issue)
		print("\n")
		quit(1)


func _validate_node_recursive(node: Node, space: PhysicsDirectSpaceState3D) -> void:
	# Check if this node is an instanced prop or static body (excluding player/terrain base)
	if node is CollisionObject3D and node.name != "GrassField" and node.name != "Player" and not node.name.begins_with("BarrierWall"):
		_validate_prop(node, space)

	for child in node.get_children():
		_validate_node_recursive(child, space)


func _validate_prop(prop: CollisionObject3D, space: PhysicsDirectSpaceState3D) -> void:
	total_props += 1
	var issues: Array[String] = []
	var g_pos := prop.global_position
	var g_rot := prop.global_rotation
	var g_scale := prop.global_transform.basis.get_scale()
	var path := str(prop.get_path())

	# 1. Bounds Check
	# Background backdrop villas and outside pine trees are intentionally outside perimeter (-28m, etc.)
	var is_backdrop := "OutsideEnvironment" in path or "Backdrop" in prop.name or "PineTree" in prop.name
	if not is_backdrop:
		if abs(g_pos.x) > MAP_BOUNDS_X or abs(g_pos.z) > MAP_BOUNDS_Z:
			issues.append("Out of map bounds: pos=(%.2f, %.2f, %.2f) exceeds limit (%.1f, %.1f)" % [
				g_pos.x, g_pos.y, g_pos.z, MAP_BOUNDS_X, MAP_BOUNDS_Z
			])

	# 2. Non-uniform scale / Shear check
	var sx := g_scale.x
	var sy := g_scale.y
	var sz := g_scale.z
	var max_scale_diff := maxf(abs(sx - sy), maxf(abs(sy - sz), abs(sx - sz)))
	if max_scale_diff > 0.05 and not is_backdrop and not ("Barrier" in prop.name):
		# Some barriers or long walls are scaled, check if shear exists
		var b := prop.global_transform.basis
		var dot_xy: float = absf(b.x.normalized().dot(b.y.normalized()))
		var dot_yz: float = absf(b.y.normalized().dot(b.z.normalized()))
		var dot_xz: float = absf(b.x.normalized().dot(b.z.normalized()))
		if dot_xy > 0.05 or dot_yz > 0.05 or dot_xz > 0.05:
			issues.append("Basis contains shear distortion: dotXY=%.3f, dotYZ=%.3f, dotXZ=%.3f" % [dot_xy, dot_yz, dot_xz])

	# 3. Tilt / Roll Check
	var is_ramp := "ramp" in prop.name.to_lower() or "ramp" in path.to_lower()
	if not is_ramp:
		var pitch_deg := rad_to_deg(abs(g_rot.x))
		var roll_deg := rad_to_deg(abs(g_rot.z))
		# Normalize around 180 if flipped
		if pitch_deg > 90.0:
			pitch_deg = abs(pitch_deg - 180.0)
		if roll_deg > 90.0:
			roll_deg = abs(roll_deg - 180.0)

		if pitch_deg > MAX_TILT_DEG or roll_deg > MAX_TILT_DEG:
			issues.append("Unintended tilt/roll: pitch=%.1f°, roll=%.1f° (max %.1f°)" % [pitch_deg, roll_deg, MAX_TILT_DEG])

	# 4. Collision check
	var has_col := false
	for c in prop.get_children():
		if c is CollisionShape3D and not c.disabled:
			has_col = true
			break
	if not has_col:
		issues.append("Missing active CollisionShape3D")

	# 5. Ground / Seating Raycast Check
	# Raycast down from prop position
	if not is_backdrop and g_pos.y >= 0.0:
		var ray_from := g_pos + Vector3(0, 0.2, 0)
		var ray_to := g_pos + Vector3(0, -1.5, 0)
		var q := PhysicsRayQueryParameters3D.create(ray_from, ray_to)
		q.exclude = [prop.get_rid()]
		var hit := space.intersect_ray(q)
		if hit.is_empty():
			issues.append("Floating: no supporting geometry found below within 1.5m")
		else:
			var hit_pos: Vector3 = hit["position"]
			var gap := g_pos.y - hit_pos.y
			# Props resting on ground (y=0) or stacked on crates
			if gap > MAX_FLOATING_DIST and g_pos.y > 0.1:
				# Check if this prop has child shapes that touch ground
				var touching := false
				for c in prop.get_children():
					if c is CollisionShape3D:
						var c_bottom: float = c.global_position.y
						if c.shape is BoxShape3D:
							c_bottom -= (c.shape as BoxShape3D).size.y * 0.5
						elif c.shape is CylinderShape3D:
							c_bottom -= (c.shape as CylinderShape3D).height * 0.5
						if abs(c_bottom - hit_pos.y) <= MAX_FLOATING_DIST:
							touching = true
							break
				if not touching:
					issues.append("Floating gap of %.3fm above %s" % [gap, hit.collider.name if hit.collider else "surface"])

	if issues.is_empty():
		pass_count += 1
	else:
		fail_count += 1
		failure_reports.append({
			"path": path,
			"pos": g_pos,
			"issues": issues
		})
