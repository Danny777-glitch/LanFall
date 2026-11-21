@tool
extends SceneTree

func _init() -> void:
    var mat := StandardMaterial3D.new()
    for prop in mat.get_property_list():
        var pname: String = prop["name"]
        if "ao_" in pname or "roughness_" in pname or "metallic_" in pname or "orm_" in pname:
            print(pname)
    quit()
