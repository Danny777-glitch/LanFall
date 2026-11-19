# ============================================================================
# EnemyBot - Tactical AI Opponent for LAN Fall
# ============================================================================
extends CharacterBody3D

const DAMAGE_NUMBER_SCENE = preload("res://scenes/objects/damage_number.tscn")
const TRACER_SCENE = preload("res://scenes/objects/bullet_tracer.tscn")

enum State { PATROL, COMBAT, DEAD }

@export var bot_name: String = "BOT 1"
@export var max_health: int = 100
@export var walk_speed: float = 3.6
@export var detection_range: float = 28.0
@export var attack_damage: int = 12
@export var burst_count: int = 3
@export var burst_interval: float = 0.16
@export var attack_cooldown: float = 1.35

var current_health: int = 100
var current_state: State = State.PATROL
var player_ref: Node3D = null

# AI Timers & Movement
var state_timer: float = 0.0
var burst_shots_left: int = 0
var shot_timer: float = 0.0
var cooldown_timer: float = 0.0
var strafe_dir: float = 1.0
var strafe_timer: float = 0.0
var spawn_pos: Vector3
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

# Node References
@onready var visual_root: Node3D = $Visuals
@onready var label: Label3D = $Label3D
@onready var collision_shape: CollisionShape3D = $CollisionShape3D
@onready var shoot_ray: RayCast3D = $Visuals/ShootRay
@onready var muzzle_point: Marker3D = $Visuals/Rifle/MuzzlePoint
@onready var muzzle_flash = $Visuals/Rifle/MuzzlePoint/MuzzleFlash
@onready var shoot_sound: AudioStreamPlayer3D = $ShootSound
@onready var hit_sound: AudioStreamPlayer3D = $HitSound
@onready var destroy_sound: AudioStreamPlayer3D = $DestroySound


func _ready() -> void:
	current_health = max_health
	spawn_pos = global_position
	_update_ui()
	_find_player()


func _find_player() -> void:
	player_ref = get_tree().get_first_node_in_group("player")


func _physics_process(delta: float) -> void:
	if current_state == State.DEAD:
		return

	if not is_on_floor():
		velocity.y -= gravity * delta

	if not is_instance_valid(player_ref):
		_find_player()

	match current_state:
		State.PATROL:
			_process_patrol(delta)
		State.COMBAT:
			_process_combat(delta)

	move_and_slide()


func _process_patrol(delta: float) -> void:
	# Idle/patrol behavior: wander slowly around spawn post
	state_timer += delta
	if state_timer >= 3.5:
		state_timer = 0.0
		strafe_dir = -strafe_dir
		rotate_y(randf_range(-PI * 0.4, PI * 0.4))

	velocity.x = lerpf(velocity.x, 0.0, 6.0 * delta)
	velocity.z = lerpf(velocity.z, 0.0, 6.0 * delta)

	# Check for player
	if is_instance_valid(player_ref):
		var dist := global_position.distance_to(player_ref.global_position)
		if dist <= detection_range and _has_line_of_sight():
			current_state = State.COMBAT
			cooldown_timer = 0.4


func _process_combat(delta: float) -> void:
	if not is_instance_valid(player_ref):
		current_state = State.PATROL
		return

	var dist := global_position.distance_to(player_ref.global_position)
	if dist > detection_range * 1.3 or not _has_line_of_sight():
		# Lost sight
		state_timer += delta
		if state_timer >= 2.5:
			current_state = State.PATROL
			return
	else:
		state_timer = 0.0

	# Turn smoothly towards player (Y axis only)
	var target_look := player_ref.global_position
	target_look.y = global_position.y
	var look_dir := (target_look - global_position).normalized()
	if look_dir:
		var target_rot_y := atan2(-look_dir.x, -look_dir.z)
		rotation.y = lerp_angle(rotation.y, target_rot_y, 8.0 * delta)

	# Tactical Strafe movement while in gunfight
	strafe_timer += delta
	if strafe_timer >= 1.6:
		strafe_timer = 0.0
		strafe_dir = -strafe_dir if randf() > 0.3 else strafe_dir

	var right_vec := transform.basis.x.normalized()
	velocity.x = lerpf(velocity.x, right_vec.x * strafe_dir * walk_speed, 8.0 * delta)
	velocity.z = lerpf(velocity.z, right_vec.z * strafe_dir * walk_speed, 8.0 * delta)

	# Combat shooting logic
	if cooldown_timer > 0.0:
		cooldown_timer -= delta
	elif burst_shots_left > 0:
		shot_timer -= delta
		if shot_timer <= 0.0:
			_bot_shoot()
			burst_shots_left -= 1
			shot_timer = burst_interval
			if burst_shots_left <= 0:
				cooldown_timer = attack_cooldown
	else:
		# Start next burst
		burst_shots_left = burst_count
		shot_timer = 0.0


func _has_line_of_sight() -> bool:
	if not is_instance_valid(player_ref):
		return false
	var space_state := get_world_3d().direct_space_state
	var query := PhysicsRayQueryParameters3D.create(global_position + Vector3(0, 1.4, 0), player_ref.global_position + Vector3(0, 1.2, 0))
	query.exclude = [self]
	var result := space_state.intersect_ray(query)
	if result.is_empty():
		return true
	if result.collider == player_ref:
		return true
	return false


func _bot_shoot() -> void:
	if not is_instance_valid(player_ref):
		return

	# Audio & Muzzle Flash
	if shoot_sound:
		shoot_sound.pitch_scale = randf_range(0.95, 1.05)
		shoot_sound.play()

	if muzzle_flash and muzzle_flash.has_method("flash"):
		muzzle_flash.flash()

	# Aim slightly imperfectly at player head/chest
	var target_pt := player_ref.global_position + Vector3(randf_range(-0.25, 0.25), randf_range(0.8, 1.5), randf_range(-0.25, 0.25))
	var muzzle_pos := muzzle_point.global_position if muzzle_point else (global_position + Vector3(0, 1.2, 0))

	# Spawn glowing orange/red bullet tracer
	_spawn_tracer(muzzle_pos, target_pt, Color(1.0, 0.35, 0.15))

	# Raycast hit test to player
	var space_state := get_world_3d().direct_space_state
	var query := PhysicsRayQueryParameters3D.create(muzzle_pos, target_pt)
	query.exclude = [self]
	var hit := space_state.intersect_ray(query)

	if not hit.is_empty() and hit.collider == player_ref:
		if player_ref.has_method("take_damage"):
			player_ref.take_damage(attack_damage)


func _spawn_tracer(from: Vector3, to: Vector3, col: Color) -> void:
	var tracer = TRACER_SCENE.instantiate()
	get_tree().current_scene.add_child(tracer)
	tracer.setup(from, to, col)


func take_damage(amount: int) -> void:
	take_damage_with_attacker(amount, "PLAYER", 1)


func take_damage_with_attacker(amount: int, attacker_name: String, attacker_id: int) -> void:
	if current_state == State.DEAD:
		return

	current_health = clampi(current_health - amount, 0, max_health)
	_update_ui()
	_spawn_damage_number(amount)

	# React to hit: alert and face player immediately
	if is_instance_valid(player_ref):
		current_state = State.COMBAT
		if cooldown_timer > 0.3:
			cooldown_timer = 0.2

	if hit_sound:
		hit_sound.pitch_scale = randf_range(0.95, 1.05)
		hit_sound.play()

	# White hit flash on mesh
	_flash_hit()

	if current_health <= 0:
		_die()


func _flash_hit() -> void:
	if visual_root:
		visual_root.position.z += 0.08
		await get_tree().create_timer(0.06).timeout
		if is_instance_valid(visual_root):
			visual_root.position.z = 0.0


func _spawn_damage_number(amount: int) -> void:
	var dmg = DAMAGE_NUMBER_SCENE.instantiate()
	get_tree().current_scene.add_child(dmg)
	dmg.global_position = global_position + Vector3(randf_range(-0.2, 0.2), 1.9, randf_range(-0.2, 0.2))
	dmg.setup(amount, amount >= 35)


func _update_ui() -> void:
	if not label:
		return
	label.text = "[%s]\nHP: %d / %d" % [bot_name, current_health, max_health]
	var ratio := float(current_health) / float(max_health)
	if ratio > 0.6:
		label.modulate = Color(0.4, 1.0, 0.4)
	elif ratio > 0.3:
		label.modulate = Color(1.0, 0.85, 0.2)
	else:
		label.modulate = Color(1.0, 0.25, 0.2)


func _die() -> void:
	current_state = State.DEAD
	collision_shape.disabled = true
	label.text = "💥 ELIMINATED!"
	label.modulate = Color(1.0, 0.2, 0.2)

	# Notify HUD for kill feed banner
	var hud = get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("add_kill"):
		hud.add_kill(bot_name)

	if destroy_sound:
		destroy_sound.play()

	# Shrink animation
	var tween := create_tween()
	tween.tween_property(visual_root, "scale", Vector3.ZERO, 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)

	# Respawn after 4.5 seconds
	await get_tree().create_timer(4.5).timeout
	_respawn()


func _respawn() -> void:
	global_position = spawn_pos
	current_health = max_health
	current_state = State.PATROL
	collision_shape.disabled = false
	_update_ui()

	if visual_root:
		var tween := create_tween()
		tween.tween_property(visual_root, "scale", Vector3.ONE, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
