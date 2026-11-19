extends SceneTree

func _init():
    print("=== TESTING PROPS LOAD ===")
    var props = [
        "res://maps/props/yard_jersey_barrier.tscn",
        "res://maps/props/yard_container_red.tscn",
        "res://maps/props/yard_container_blue.tscn",
        "res://maps/props/yard_container_yellow.tscn",
        "res://maps/props/yard_container_ramp_stack.tscn",
        "res://maps/props/yard_crate_stack.tscn",
        "res://maps/props/yard_barrel_cluster.tscn",
        "res://maps/props/yard_freight_boxcar.tscn",
        "res://maps/props/yard_timber_stack.tscn",
        "res://maps/props/yard_perimeter_fence.tscn",
        "res://maps/props/yard_spawn_shed.tscn",
        "res://maps/props/yard_central_warehouse.tscn",
        "res://maps/props/yard_backdrop.tscn"
    ]
    var all_ok = true
    for p in props:
        var res = ResourceLoader.load(p)
        if res:
            var inst = res.instantiate()
            print("  [OK] Loaded:", p, "Nodes:", inst.get_child_count())
            inst.free()
        else:
            print("  [FAIL] Could not load:", p)
            all_ok = false
    if all_ok:
        print("ALL PROPS LOADED PERFECTLY!")
    quit()
