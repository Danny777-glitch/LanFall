@tool
extends SceneTree

func _init():
	print("=================================================================")
	print("AUDIT: MODEL & PROP ORIGINS, BOUNDS, AND PIVOTS")
	print("=================================================================")
	var models = [
		"res://assets/models/Barrel_01/Barrel_01.gltf",
		"res://assets/models/wooden_military_crate/wooden_military_crate.gltf",
		"res://assets/models/old_military_crate/old_military_crate.gltf",
		"res://assets/models/ammo_box/ammo_box.gltf",
		"res://assets/models/hanging_industrial_lamp/hanging_industrial_lamp.gltf",
		"res://assets/models/wooden_table_02/wooden_table_02.gltf"
	]
	for m_path in models:
		var scn = load(m_path)
		if scn:
			var inst = scn.instantiate()
			print("\n[MODEL] %s (%s)" % [m_path.get_file(), m_path])
			_audit_node(inst, "  ")
			inst.free()

	print("\n=================================================================")
	print("AUDIT: PROP SCENES STRUCTURE & COLLIDERS")
	print("=================================================================")
	var props = [
		"res://scenes/maps/warehouse/props/bgmi_tdm_warehouse.tscn",
		"res://scenes/maps/warehouse/props/bgmi_spawn_sheds.tscn",
		"res://scenes/maps/warehouse/props/bgmi_perimeter_fence.tscn",
		"res://scenes/maps/warehouse/props/bgmi_train_boxcar.tscn",
		"res://scenes/maps/warehouse/props/bgmi_container_ramp.tscn",
		"res://scenes/maps/warehouse/props/bgmi_timber_logs.tscn",
		"res://scenes/maps/warehouse/props/bgmi_wooden_pergola.tscn",
		"res://scenes/maps/warehouse/props/bgmi_jersey_barrier.tscn",
		"res://scenes/maps/warehouse/props/bgmi_crate_stack.tscn",
		"res://scenes/maps/warehouse/props/bgmi_backdrop_villa.tscn",
		"res://scenes/maps/warehouse/props/pine_tree.tscn"
	]
	for p_path in props:
		var scn = load(p_path)
		if scn:
			var inst = scn.instantiate()
			print("\n[PROP SCENE] %s (Type: %s)" % [p_path.get_file(), inst.get_class()])
			_audit_node(inst, "  ")
			inst.free()

	quit()

func _audit_node(n: Node, indent: String):
	var info := "%s- %s [%s]" % [indent, n.name, n.get_class()]
	if n is Node3D:
		info += " pos=%s rot_deg=%s scale=%s" % [n.position, n.rotation_degrees, n.scale]
	if n is VisualInstance3D:
		var aabb: AABB = n.get_aabb()
		info += " AABB(min_y=%.3f, max_y=%.3f, size=%s)" % [aabb.position.y, aabb.position.y + aabb.size.y, aabb.size]
	if n is CollisionShape3D and n.shape:
		info += " Shape=[%s]" % [n.shape.get_class()]
	print(info)
	for c in n.get_children():
		_audit_node(c, indent + "  ")
