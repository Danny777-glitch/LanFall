extends SceneTree

var frame_count := 0
var map_node: Node = null
var cam: Camera3D = null

func _init():
    print("=== CAPTURING VALIDATION SCREENSHOTS ===")
    var map_packed = ResourceLoader.load("res://scenes/maps/test_map.tscn")
    map_node = map_packed.instantiate()
    root.add_child(map_node)
    
    # Create dedicated photo camera
    cam = Camera3D.new()
    cam.current = true
    map_node.add_child(cam)

func _process(delta: float) -> bool:
    frame_count += 1
    
    if frame_count == 5:
        # Shot 1: South Spawn Compound interior looking at weapon tables & doorway
        cam.global_position = Vector3(0.0, 1.6, 42.0)
        cam.look_at(Vector3(0.0, 1.4, 25.0), Vector3.UP)
    elif frame_count == 8:
        save_shot("shot_1_spawn_compound.png")
        # Shot 2: Container & Ramp
        cam.global_position = Vector3(-4.0, 1.6, 32.0)
        cam.look_at(Vector3(-6.5, 1.8, 25.0), Vector3.UP)
    elif frame_count == 11:
        save_shot("shot_2_container_ramp.png")
        # Shot 3: Crate Stacks outside warehouse
        cam.global_position = Vector3(0.0, 1.6, 22.0)
        cam.look_at(Vector3(-3.2, 1.0, 15.2), Vector3.UP)
    elif frame_count == 14:
        save_shot("shot_3_crate_stacks.png")
        # Shot 4: Timber Yard log piles & freight car
        cam.global_position = Vector3(10.0, 1.6, 18.0)
        cam.look_at(Vector3(14.5, 1.5, 9.5), Vector3.UP)
    elif frame_count == 17:
        save_shot("shot_4_timber_yard.png")
        print("=== ALL 4 SHOTS CAPTURED! ===")
        quit()
        return true
    return false

func save_shot(filename: String):
    var img = root.get_viewport().get_texture().get_image()
    if img:
        img.save_png("Plan/" + filename)
        print("Saved Plan/" + filename)
    else:
        print("Failed to get image for " + filename)
