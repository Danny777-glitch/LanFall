# ============================================================================
# perf_log.gd — Performance & Hardware Metrics Profiler
# ============================================================================
extends SceneTree

var bookmarks: Array[Dictionary] = [
	{ "name": "spawn_south", "pos": Vector3(0.0, 1.6, 37.0), "rot_deg": Vector3(0.0, 180.0, 0.0) },
	{ "name": "warehouse_interior", "pos": Vector3(0.0, 2.0, 10.0), "rot_deg": Vector3(-5.0, 180.0, 0.0) },
	{ "name": "crate_barrel_detail", "pos": Vector3(-2.5, 1.2, -1.0), "rot_deg": Vector3(-12.0, -135.0, 0.0) },
	{ "name": "container_ramp", "pos": Vector3(-2.0, 2.0, 29.0), "rot_deg": Vector3(-5.0, -145.0, 0.0) },
	{ "name": "yard_overview", "pos": Vector3(-22.0, 18.0, 40.0), "rot_deg": Vector3(-25.0, -35.0, 0.0) },
	{ "name": "target_dummy", "pos": Vector3(0.0, 1.5, 3.5), "rot_deg": Vector3(-5.0, 180.0, 0.0) },
	{ "name": "pergola_roof", "pos": Vector3(-16.0, 1.2, -7.0), "rot_deg": Vector3(20.0, 0.0, 0.0) },
	{ "name": "villa_roofs", "pos": Vector3(-20.0, 8.0, 30.0), "rot_deg": Vector3(-10.0, -45.0, 0.0) },
	{ "name": "shed_south_interior", "pos": Vector3(-5.0, 1.2, 43.0), "rot_deg": Vector3(15.0, 140.0, 0.0) },
	{ "name": "spawn_north", "pos": Vector3(0.0, 1.6, -37.0), "rot_deg": Vector3(0.0, 0.0, 0.0) },
]

var output_csv := "docs/perf/baseline_engine.csv"
var total_duration := 90.0
var fps_cap := 0
var quality_preset := "HIGH"


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	for a in args:
		if a.begins_with("--out="):
			output_csv = a.trim_prefix("--out=")
		elif a.begins_with("--duration="):
			total_duration = float(a.trim_prefix("--duration="))
		elif a.begins_with("--cap="):
			fps_cap = int(a.trim_prefix("--cap="))
		elif a.begins_with("--preset="):
			quality_preset = a.trim_prefix("--preset=").to_upper()

	if fps_cap > 0:
		Engine.max_fps = fps_cap
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	else:
		Engine.max_fps = 0
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)

	call_deferred("_run_benchmark")


func _run_benchmark() -> void:
	print("\n" + "=".repeat(75))
	print("       PERFORMANCE LOGGER STARTING (Duration: %.1fs, Cap: %d, Preset: %s)" % [total_duration, fps_cap, quality_preset])
	print("=".repeat(75))

	var map_packed := load("res://scenes/maps/warehouse/warehouse_map.tscn")
	var map_node: Node3D = map_packed.instantiate()
	root.add_child(map_node)

	if map_node.has_method("apply_quality_preset"):
		map_node.apply_quality_preset(quality_preset)

	var perf = root.get_node_or_null("PerfSettings")
	if perf:
		perf.max_fps = fps_cap
		perf.set_in_menu(false)
	Engine.max_fps = fps_cap

	var cam := Camera3D.new()
	cam.current = true
	root.add_child(cam)

	var f := FileAccess.open(output_csv, FileAccess.WRITE)
	if not f:
		printerr("Failed to open output CSV: ", output_csv)
		quit()
		return

	f.store_line("second,bookmark,fps,frame_time_ms,draw_calls,primitives,vram_mb,texture_mem_mb,objects")

	# Warm up frames
	for w in range(30):
		await process_frame

	var start_time := Time.get_ticks_msec() / 1000.0
	var last_sec := -1
	var sec_samples := 0
	var sec_dt_sum := 0.0

	var time_per_bookmark := total_duration / float(bookmarks.size())

	while true:
		var now := Time.get_ticks_msec() / 1000.0
		var elapsed := now - start_time
		if elapsed >= total_duration:
			break

		var current_sec := int(elapsed)
		var b_idx := clampi(int(elapsed / time_per_bookmark), 0, bookmarks.size() - 1)
		var b_data: Dictionary = bookmarks[b_idx]

		# Position camera at current bookmark
		cam.global_position = b_data["pos"]
		cam.rotation_degrees = b_data["rot_deg"]

		var t0 := Time.get_ticks_usec()
		await process_frame
		var frame_dt := (Time.get_ticks_usec() - t0) / 1000.0
		sec_dt_sum += frame_dt
		sec_samples += 1

		if current_sec > last_sec:
			last_sec = current_sec
			var avg_ms := sec_dt_sum / float(maxi(1, sec_samples))
			var current_fps := Performance.get_monitor(Performance.TIME_FPS)
			if current_fps <= 0.0:
				current_fps = 1000.0 / avg_ms if avg_ms > 0 else 0.0
			var draw_calls := int(Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
			var primitives := int(Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME))
			var vram_mb := Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED) / (1024.0 * 1024.0)
			var tex_mb := Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED) / (1024.0 * 1024.0)
			var objects := int(Performance.get_monitor(Performance.OBJECT_COUNT))

			f.store_line("%d,%s,%.1f,%.2f,%d,%d,%.2f,%.2f,%d" % [
				current_sec, b_data["name"], current_fps, avg_ms, draw_calls, primitives, vram_mb, tex_mb, objects
			])
			f.flush()

			if current_sec % 10 == 0 or current_sec == 1:
				print("[%3ds/%3ds] %-20s | %6.1f FPS | %5.2f ms | %7.1f MB VRAM | %4d DC" % [
					current_sec, int(total_duration), b_data["name"], current_fps, avg_ms, vram_mb, draw_calls
				])

			sec_dt_sum = 0.0
			sec_samples = 0

	f.close()
	print("\nBenchmark completed. Saved to %s\n" % output_csv)
	quit()
