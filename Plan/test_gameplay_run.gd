extends SceneTree

var map_node: Node = null
var frame_counter := 0
var fps_samples: Array[float] = []

func _init():
    print("=== STARTING REAL-TIME GAMEPLAY BENCHMARK & BOUNDARY AUDIT ===")
    var map_packed = ResourceLoader.load("res://scenes/maps/test_map.tscn")
    map_node = map_packed.instantiate()
    root.add_child(map_node)
    print("[Benchmark] Map added to root. Ready called.")

    # Audit PerimeterCompound
    var compound = map_node.get_node_or_null("PerimeterCompound")
    if compound:
        var fence_count := 0
        var barrier_count := 0
        var west_fences := 0
        var east_fences := 0
        var south_fences := 0
        var north_fences := 0
        for child in compound.get_children():
            var cname = child.name
            if cname.begins_with("FenceWest"):
                west_fences += 1
                fence_count += 1
            elif cname.begins_with("FenceEast"):
                east_fences += 1
                fence_count += 1
            elif cname.begins_with("FenceSouth"):
                south_fences += 1
                fence_count += 1
            elif cname.begins_with("FenceNorth"):
                north_fences += 1
                fence_count += 1
            elif cname.begins_with("BarrierWall"):
                barrier_count += 1
        print("[Boundary Audit] Total Fence Panels: %d (West: %d, East: %d, South: %d, North: %d)" % [
            fence_count, west_fences, east_fences, south_fences, north_fences
        ])
        print("[Boundary Audit] 8m Tall Barrier Colliders: %d (West, East, South, North)" % barrier_count)
    else:
        printerr("[Boundary Audit] ERROR: PerimeterCompound node not found!")

    var outside = map_node.get_node_or_null("OutsideEnvironment")
    if outside:
        var tree_count := 0
        var villa_count := 0
        for child in outside.get_children():
            if child.name.begins_with("PineTree"):
                tree_count += 1
            elif child.name.begins_with("BackdropVilla"):
                villa_count += 1
        print("[Environment Audit] Outside Backdrop Trees: %d, Backdrop Villas: %d" % [tree_count, villa_count])

func _process(delta: float) -> bool:
    frame_counter += 1
    if delta > 0.0:
        fps_samples.append(1.0 / delta)
    
    if frame_counter == 10:
        var players = map_node.get_node_or_null("Players")
        var p_count = players.get_child_count() if players else 0
        print("[Benchmark] Frame 10: Players container child count =", p_count)
        if p_count > 0:
            var p1 = players.get_child(0)
            print("[Benchmark] Player 1 Position =", p1.global_position)
            
    if frame_counter >= 120:
        var avg_fps := 0.0
        # average over frames 20 to 120
        var warm_samples = fps_samples.slice(20)
        for s in warm_samples:
            avg_fps += s
        if warm_samples.size() > 0:
            avg_fps /= warm_samples.size()
        print("=== BENCHMARK COMPLETED ===")
        print("Total frames simulated: %d" % frame_counter)
        print("Warmup FPS (Frames 20-120): %.1f FPS (%.2f ms/frame)" % [avg_fps, 1000.0 / avg_fps if avg_fps > 0 else 0])
        print("===========================")
        quit()
        return true
    return false
