# ============================================================================
# BulletTracer - High-speed glowing tracer line
# ============================================================================
extends Node3D

@export var speed: float = 120.0
@export var tracer_color: Color = Color(0.2, 0.9, 1.0, 1.0) # Vibrant cyan

var start_point: Vector3
var end_point: Vector3
var distance: float
var traveled: float = 0.0

@onready var mesh_instance: MeshInstance3D = $MeshInstance3D


func setup(from: Vector3, to: Vector3, color: Color = Color(0.2, 0.9, 1.0, 1.0)) -> void:
	start_point = from
	end_point = to
	global_position = from
	distance = from.distance_to(to)
	
	if distance > 0.1:
		look_at(to, Vector3.UP)
		
	# Setup glowing material
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_color = color
	mat.emission_enabled = true
	mat.emission = color
	mat.emission_energy_multiplier = 3.0
	mesh_instance.material_override = mat


func _process(delta: float) -> void:
	traveled += speed * delta
	if traveled >= distance:
		queue_free()
		return
		
	global_position = start_point.lerp(end_point, traveled / distance)
