# ============================================================================
# capture_bookmarks.gd — Automated Bookmark Screenshot Tool (Non-headless Forward+)
# ============================================================================
extends SceneTree

var bookmarks: Dictionary = {
	"spawn_south": {
		"pos": Vector3(0.0, 1.6, 37.0),
		"rot_deg": Vector3(0.0, 180.0, 0.0) # facing -Z (center)
	},
	"spawn_north": {
		"pos": Vector3(0.0, 1.6, -37.0),
		"rot_deg": Vector3(0.0, 0.0, 0.0) # facing +Z (center)
	},
	"shed_south_interior": {
		"pos": Vector3(-5.0, 1.2, 43.0),
		"rot_deg": Vector3(15.0, 140.0, 0.0)
	},
	"villa_roofs": {
		"pos": Vector3(-20.0, 8.0, 30.0),
		"rot_deg": Vector3(-10.0, -45.0, 0.0)
	},
	"warehouse_interior": {
		"pos": Vector3(0.0, 2.0, 10.0),
		"rot_deg": Vector3(-5.0, 180.0, 0.0)
	},
	"crate_barrel_detail": {
		"pos": Vector3(-2.5, 1.2, -1.0),
		"rot_deg": Vector3(-12.0, -135.0, 0.0)
	},
	"pergola_roof": {
		"pos": Vector3(-16.0, 1.2, -7.0),
		"rot_deg": Vector3(20.0, 0.0, 0.0)
	},
	"container_ramp": {
		"pos": Vector3(-2.0, 2.0, 29.0),
		"rot_deg": Vector3(-5.0, -145.0, 0.0)
	},
	"target_dummy": {
		"pos": Vector3(0.0, 1.5, 3.5),
		"rot_deg": Vector3(-5.0, 180.0, 0.0)
	},
	"yard_overview": {
		"pos": Vector3(-22.0, 18.0, 40.0),
		"rot_deg": Vector3(-25.0, -35.0, 0.0)
	}
}

var output_prefix := "before_"
var output_dir := "docs/shots/round3"


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	for a in args:
		if a.begins_with("--prefix="):
			output_prefix = a.trim_prefix("--prefix=")
		elif a.begins_with("--dir="):
			output_dir = a.trim_prefix("--dir=")
	call_deferred("_run")


func _run() -> void:
	DirAccess.make_dir_recursive_absolute(output_dir)
	var map_packed := load("res://scenes/maps/warehouse/warehouse_map.tscn")
	var map_node: Node3D = map_packed.instantiate()
	root.add_child(map_node)

	var cam := Camera3D.new()
	cam.current = true
	root.add_child(cam)

	# Initial warm up frames
	for f in range(20):
		await process_frame

	for b_name in bookmarks.keys():
		var b: Dictionary = bookmarks[b_name]
		cam.global_position = b["pos"]
		cam.rotation_degrees = b["rot_deg"]

		# Settle frame
		for f in range(6):
			await process_frame

		var img := root.get_texture().get_image()
		if img and not img.is_empty():
			var out_path := "%s/%s%s.png" % [output_dir, output_prefix, b_name]
			img.save_png(out_path)
			print("[Capture] Saved %s" % out_path)

	print("[Capture] Done all bookmarks.")
	quit()
