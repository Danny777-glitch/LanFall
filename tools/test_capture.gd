extends SceneTree

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var map_packed := load("res://scenes/maps/warehouse/warehouse_map.tscn")
	var map_node: Node3D = map_packed.instantiate()
	root.add_child(map_node)

	var cam := Camera3D.new()
	cam.position = Vector3(0, 5, 20)
	cam.look_at(Vector3.ZERO, Vector3.UP)
	cam.current = true
	root.add_child(cam)

	# Process frames to let forward+ pipeline render
	for i in range(15):
		await process_frame

	var img := root.get_texture().get_image()
	if img and not img.is_empty():
		DirAccess.make_dir_recursive_absolute("docs/shots/round2")
		var err := img.save_png("docs/shots/round2/test_shot.png")
		print("SUCCESS: Captured test_shot.png, err code: ", err, ", size: ", img.get_size())
	else:
		print("FAILED to get image")
	quit()
