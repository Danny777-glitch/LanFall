# ============================================================================
# profile_map.gd — Forward+ Performance & VRAM Profiler
# ============================================================================
extends SceneTree

func _init() -> void:
	call_deferred("_run_profiler")

func _run_profiler() -> void:
	print("\n" + "=".repeat(70))
	print("       MAP PERFORMANCE & HARDWARE BUDGET PROFILER")
	print("=".repeat(70))

	var packed := load("res://scenes/maps/warehouse/warehouse_map.tscn")
	var map_node: Node3D = packed.instantiate()
	root.add_child(map_node)

	# Warm up frames
	for f in range(60):
		await process_frame

	var total_time := 0.0
	var frames := 120
	var min_ms := 9999.0
	var max_ms := 0.0

	for f in range(frames):
		var t0 := Time.get_ticks_usec()
		await process_frame
		var dt := (Time.get_ticks_usec() - t0) / 1000.0
		total_time += dt
		min_ms = minf(min_ms, dt)
		max_ms = maxf(max_ms, dt)

	var avg_ms := total_time / float(frames)
	var avg_fps := 1000.0 / avg_ms

	var vram_bytes := Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED)
	var vram_mb := vram_bytes / (1024.0 * 1024.0)
	var draw_calls := Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
	var primitives := Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME)

	print("  GPU Device:        %s" % RenderingServer.get_video_adapter_name())
	print("  Average Frame Rate: %.1f FPS" % avg_fps)
	print("  Average Frame Time: %.2f ms (min: %.2f ms, max: %.2f ms)" % [avg_ms, min_ms, max_ms])
	print("  Draw Calls:         %d" % draw_calls)
	print("  Primitives Rendered:%d" % primitives)
	print("  VRAM Memory Used:   %.2f MB" % vram_mb)
	print("=".repeat(70) + "\n")

	quit()
