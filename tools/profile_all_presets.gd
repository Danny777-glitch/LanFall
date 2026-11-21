# ============================================================================
# profile_all_presets.gd — Forward+ Scalability & Presets Profiler
# ============================================================================
extends SceneTree

func _init() -> void:
	call_deferred("_run_profiler")

func _run_profiler() -> void:
	print("\n" + "=".repeat(75))
	print("       GRAPHICS PRESETS & HARDWARE BUDGET PROFILER (LOW/MED/HIGH/ULTRA)")
	print("=".repeat(75))

	var packed := load("res://scenes/maps/warehouse/warehouse_map.tscn")
	var map_node: Node3D = packed.instantiate()
	root.add_child(map_node)

	var presets := ["LOW", "MEDIUM", "HIGH", "ULTRA"]
	var results := {}

	for preset in presets:
		map_node.apply_quality_preset(preset)
		
		# Warmup frames
		for f in range(45):
			await process_frame

		var total_time := 0.0
		var frames := 90
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

		results[preset] = {
			"fps": avg_fps,
			"ms": avg_ms,
			"min_ms": min_ms,
			"max_ms": max_ms,
			"vram": vram_mb,
			"draw_calls": draw_calls
		}

	print("\n%-10s | %-12s | %-12s | %-14s | %-12s" % ["PRESET", "AVG FPS", "FRAME TIME", "VRAM USED", "DRAW CALLS"])
	print("-".repeat(75))
	for preset in presets:
		var r: Dictionary = results[preset]
		print("%-10s | %8.1f FPS | %8.2f ms | %10.2f MB | %10d" % [
			preset, r["fps"], r["ms"], r["vram"], r["draw_calls"]
		])
	print("=".repeat(75) + "\n")

	quit()
