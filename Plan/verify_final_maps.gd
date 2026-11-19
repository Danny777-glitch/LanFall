extends SceneTree

func _init():
    print("=== VERIFYING FINAL QUALITY MAPS LOAD ===")
    for path in ["res://scenes/maps/test_map.tscn", "res://scenes/maps/warehouse/warehouse_map.tscn"]:
        var res = ResourceLoader.load(path)
        if res:
            print("[SUCCESS] Loaded:", path)
            var node = res.instantiate()
            print("          Instantiated successfully! Node name:", node.name, "Child count:", node.get_child_count())
            node.free()
        else:
            print("[FAILURE] Failed to load:", path)
    quit()
