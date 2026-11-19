# ============================================================================
# Player - Tactical FPS Controller (LAN Multiplayer & Singleplayer)
# ============================================================================
extends CharacterBody3D

const IMPACT_SCENE = preload("res://scenes/objects/impact_effect.tscn")
const TRACER_SCENE = preload("res://scenes/objects/bullet_tracer.tscn")
const SMOKE_PROJECTILE_SCENE = preload("res://scenes/objects/smoke_projectile.tscn")
const DAMAGE_NUMBER_SCENE = preload("res://scenes/objects/damage_number.tscn")

# -- Networking & Identity --
@export var peer_id: int = 1
@export var player_name: String = "OPERATIVE"

# -- Movement Settings (Valorant-Style Snappy Response) --
@export_group("Movement")
@export var walk_speed := 5.2
@export var sprint_speed := 8.8
@export var crouch_speed := 2.8
@export var jump_velocity := 5.2
@export var acceleration := 32.0
@export var friction := 28.0
@export var air_control := 0.35

# -- Valorant-Style Tactical Weapon Audio --
const SOUND_RIFLE = preload("res://assets/sounds/rifle_shot.ogg")
const SOUND_PISTOL = preload("res://assets/sounds/pistol_shot.ogg")
const SOUND_SNIPER = preload("res://assets/sounds/sniper_shot.ogg")
const SOUND_KNIFE = preload("res://assets/sounds/knife_slash.wav")

# -- Camera & ADS Settings --
@export_group("Camera & ADS")
@export var mouse_sensitivity := 0.003
@export var fov := 75.0
@export var ads_speed := 16.0
@export var ads_sens_multiplier := 0.65

# -- Feel & Juice (Head Bob disabled for competitive crosshair stability) --
@export_group("Feel & Juice")
@export var head_bob_enabled := false
@export var bob_frequency := 2.2
@export var bob_amplitude := 0.02
@export var sway_amount := 0.0014
@export var sway_max := 0.035
@export var sway_smooth := 18.0

# -- Weapon Arsenal Data --
class WeaponData:
	var name: String
	var node: Node3D
	var damage: int
	var fire_rate: float
	var max_ammo: int
	var current_ammo: int
	var reserve_ammo: int
	var ads_gun_pos: Vector3
	var default_pos: Vector3
	var default_rot: Vector3
	var ads_fov: float
	var recoil_kick: float
	var recoil_lift: float
	var tracer_color: Color

	func _init(n: String, node_ref: Node3D, dmg: int, rate: float, max_mag: int, res: int, ads_pos: Vector3, ads_f: float, kick: float, lift: float, col: Color):
		name = n
		node = node_ref
		damage = dmg
		fire_rate = rate
		max_ammo = max_mag
		current_ammo = max_mag
		reserve_ammo = res
		ads_gun_pos = ads_pos
		default_pos = node_ref.position
		default_rot = node_ref.rotation
		ads_fov = ads_f
		recoil_kick = kick
		recoil_lift = lift
		tracer_color = col

# -- Node References --
@onready var head: Node3D = $Head
@onready var camera: Camera3D = $Head/Camera3D
@onready var shoot_ray: RayCast3D = $Head/Camera3D/ShootRay
@onready var weapons_container: Node3D = $Head/Camera3D/Weapons
@onready var rifle_node: Node3D = $Head/Camera3D/Weapons/TacticalRifle
@onready var pistol_node: Node3D = $Head/Camera3D/Weapons/TacticalPistol
@onready var sniper_node: Node3D = $Head/Camera3D/Weapons/TacticalSniper
@onready var knife_node: Node3D = $Head/Camera3D/Weapons/TacticalKnife
@onready var muzzle_light: OmniLight3D = $Head/Camera3D/MuzzleFlashLight

# 3D Visuals & Third-Person Rig
@onready var visuals_3d: Node3D = $Visuals3D
@onready var label_3d: Label3D = $Label3D
@onready var tp_rifle: MeshInstance3D = $Visuals3D/TPWeapons/TPRifle
@onready var tp_pistol: MeshInstance3D = $Visuals3D/TPWeapons/TPPistol
@onready var tp_sniper: MeshInstance3D = $Visuals3D/TPWeapons/TPSniper
@onready var tp_knife: Node3D = $Visuals3D/TPWeapons/TPKnife

# Sounds
@onready var jump_sound: AudioStreamPlayer = $JumpSound
@onready var land_sound: AudioStreamPlayer = $LandSound
@onready var step_sound: AudioStreamPlayer = $FootstepSound
@onready var shoot_sound: AudioStreamPlayer = $ShootSound
@onready var reload_sound: AudioStreamPlayer = $ReloadSound

# -- Arsenal State --
var weapons: Array[WeaponData] = []
var active_weapon_index: int = 0
var fire_timer: float = 0.0
var is_reloading: bool = false
var is_aiming: bool = false
var is_switching: bool = false
var is_inspecting: bool = false
var smoke_cooldown: float = 0.0
var hud_cache: Node = null
var _last_scope_state: bool = false
var _last_smoke_ready: bool = true

# -- Movement & Feel State --
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var current_speed := walk_speed
var bob_timer := 0.0
var step_timer := 0.0
var was_on_floor := true
var last_y_velocity := 0.0
var original_camera_y: float
var crouch_camera_y: float
var is_crouching := false
var mouse_input := Vector2.ZERO
var mouse_look_delta := Vector2.ZERO
var max_health: int = 100
var current_health: int = 100
var is_dead: bool = false
var spawn_position := Vector3.ZERO

# -- Network Sync Targets --
var is_local_player: bool = true
var target_pos: Vector3 = Vector3.ZERO
var target_rot_y: float = 0.0
var target_head_x: float = 0.0
var net_sync_timer: float = 0.0
const NET_SYNC_INTERVAL: float = 0.033 # ~30 ticks / second


func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _ready() -> void:
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		is_local_player = (multiplayer.get_unique_id() == peer_id)
		var p_dict = net.get("players")
		if p_dict and p_dict.has(peer_id):
			player_name = p_dict[peer_id].get("name", "OPERATIVE")
	else:
		is_local_player = true
		player_name = net.get("local_player_name") if net else "OPERATIVE"

	spawn_position = global_position
	target_pos = global_position
	target_rot_y = rotation.y
	original_camera_y = head.position.y
	crouch_camera_y = 1.05
	shoot_ray.add_exception(self)
	floor_snap_length = 0.35
	floor_constant_speed = true
	floor_max_angle = deg_to_rad(50.0)

	# Label tag update
	_update_label()

	if is_local_player:
		add_to_group("player")
		add_to_group("players")
		camera.current = true
		physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_INHERIT
		head.physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_INHERIT
		camera.physics_interpolation_mode = Node.PHYSICS_INTERPOLATION_MODE_INHERIT
		visuals_3d.visible = false
		label_3d.visible = false
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		camera.fov = fov

		# Initialize Arsenal for local player
		var rifle = WeaponData.new(
			"VANGUARD AR [1]",
			rifle_node,
			26,
			0.11,
			30,
			90,
			Vector3(0.0, -0.165, -0.32),
			50.0,
			0.05,
			2.4,
			Color(0.2, 0.9, 1.0)
		)
		var pistol = WeaponData.new(
			"PHANTOM PISTOL [2]",
			pistol_node,
			38,
			0.22,
			12,
			48,
			Vector3(0.0, -0.145, -0.28),
			55.0,
			0.04,
			3.2,
			Color(0.3, 1.0, 0.45)
		)
		var sniper = WeaponData.new(
			"OPERATOR SNIPER [3]",
			sniper_node,
			95,
			0.9,
			5,
			20,
			Vector3(0.0, -0.165, -0.25),
			22.0,
			0.12,
			6.5,
			Color(0.2, 0.9, 1.0)
		)
		var knife = WeaponData.new(
			"TACTICAL BLADE [4]",
			knife_node,
			55,
			0.35,
			1,
			1,
			Vector3(0.12, -0.12, -0.25),
			75.0,
			0.03,
			1.0,
			Color(0.2, 0.9, 1.0)
		)
		weapons = [rifle, pistol, sniper, knife]
		_apply_profile_customization()
	else:
		# Remote peer
		camera.current = false
		visuals_3d.visible = true
		label_3d.visible = true
		weapons_container.visible = false
		_set_tp_weapon(0)


func _update_label() -> void:
	if label_3d:
		label_3d.text = "[%s]\nHP: %d / %d" % [player_name, current_health, max_health]
		if current_health > 60:
			label_3d.modulate = Color(0.2, 1.0, 0.4)
		elif current_health > 30:
			label_3d.modulate = Color(1.0, 0.85, 0.2)
		else:
			label_3d.modulate = Color(1.0, 0.25, 0.25)


func _unhandled_input(event: InputEvent) -> void:
	if not is_local_player or is_dead:
		return

	# Mouse Look (Smooth, high refresh-rate accumulation)
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		var sens := mouse_sensitivity * (ads_sens_multiplier if is_aiming else 1.0)
		mouse_look_delta.x -= event.relative.x * sens
		mouse_look_delta.y -= event.relative.y * sens
		mouse_input += event.relative
		mouse_input = mouse_input.limit_length(50.0)

	# Weapon Switching
	if event.is_action_pressed("weapon_1"):
		_switch_weapon(0)
	elif event.is_action_pressed("weapon_2"):
		_switch_weapon(1)
	elif event.is_action_pressed("weapon_3"):
		_switch_weapon(2)
	elif event.is_action_pressed("weapon_4") or event.is_action_pressed("melee_v"):
		_switch_weapon(3)
	elif event.is_action_pressed("next_weapon"):
		_switch_weapon((active_weapon_index + 1) % weapons.size())
	elif event.is_action_pressed("prev_weapon"):
		_switch_weapon((active_weapon_index - 1 + weapons.size()) % weapons.size())

	# Tactical Smoke (E)
	if event.is_action_pressed("ability_e"):
		_throw_smoke()

	# Inspect (F)
	if event.is_action_pressed("inspect"):
		_inspect_weapon()


func _process(delta: float) -> void:
	if not is_local_player:
		return

	# Apply accumulated mouse look at full render framerate (zero physics tick stutter)
	if mouse_look_delta != Vector2.ZERO:
		rotate_y(mouse_look_delta.x)
		head.rotate_x(mouse_look_delta.y)
		head.rotation.x = clampf(head.rotation.x, deg_to_rad(-89.0), deg_to_rad(89.0))
		mouse_look_delta = Vector2.ZERO

	var cur_w := get_current_weapon()
	if not cur_w:
		return

	# Cached HUD Reference
	if not hud_cache or not is_instance_valid(hud_cache):
		hud_cache = get_tree().get_first_node_in_group("hud")

	# Smoke Cooldown Timer - only updates HUD when active or when resetting to READY
	if smoke_cooldown > 0.0:
		smoke_cooldown -= delta
		_last_smoke_ready = false
		if hud_cache and hud_cache.has_method("update_ability"):
			hud_cache.update_ability("[E] SMOKE (%.1fs)" % maxf(smoke_cooldown, 0.0), false)
	elif not _last_smoke_ready:
		_last_smoke_ready = true
		if hud_cache and hud_cache.has_method("update_ability"):
			hud_cache.update_ability("[E] SMOKE: READY", true)

	# Handle ADS state (disabled on knife)
	if active_weapon_index != 3:
		is_aiming = Input.is_action_pressed("aim") and not is_reloading and not is_switching and not is_dead
	else:
		is_aiming = false
		# Knife right click: heavy stab attack
		if Input.is_action_just_pressed("aim") and fire_timer <= 0.0 and not is_switching and not is_dead:
			_perform_knife_attack(true)

	# Sniper Scope Overlay - state change only
	if active_weapon_index == 2:
		if is_aiming != _last_scope_state:
			_last_scope_state = is_aiming
			if hud_cache and hud_cache.has_method("set_scope_overlay"):
				hud_cache.set_scope_overlay(is_aiming)
			if cur_w.node:
				cur_w.node.visible = not is_aiming
	else:
		if _last_scope_state:
			_last_scope_state = false
			if hud_cache and hud_cache.has_method("set_scope_overlay"):
				hud_cache.set_scope_overlay(false)

	# FOV Transition
	var target_fov := cur_w.ads_fov if is_aiming else fov
	camera.fov = lerpf(camera.fov, target_fov, ads_speed * delta)

	# Decay Muzzle Flash Light
	if muzzle_light and muzzle_light.light_energy > 0.0:
		muzzle_light.light_energy = lerpf(muzzle_light.light_energy, 0.0, 32.0 * delta)

	# Weapon Fire Timer
	if fire_timer > 0.0:
		fire_timer -= delta

	# Shooting / Slashing
	if not is_dead and Input.is_action_pressed("shoot") and not is_reloading and not is_switching:
		if active_weapon_index == 3:
			if fire_timer <= 0.0:
				_perform_knife_attack(false)
		else:
			if cur_w.current_ammo > 0 and fire_timer <= 0.0:
				_shoot()
			elif cur_w.current_ammo <= 0 and Input.is_action_just_pressed("shoot"):
				_reload()

	# Reload (only for guns)
	if active_weapon_index != 3 and not is_dead and Input.is_action_just_pressed("reload") and not is_reloading and not is_switching:
		_reload()

	# Weapon Sway
	_process_weapon_sway(cur_w, delta)


func _process_weapon_sway(cur_w: WeaponData, delta: float) -> void:
	var w_node := cur_w.node
	if not w_node or is_reloading or is_switching:
		return

	var target_pos := cur_w.ads_gun_pos if is_aiming else cur_w.default_pos
	var target_rot := cur_w.default_rot

	if not is_aiming:
		var sway_x := clampf(-mouse_input.x * sway_amount, -sway_max, sway_max)
		var sway_y := clampf(mouse_input.y * sway_amount, -sway_max, sway_max)
		target_pos += Vector3(sway_x, sway_y, 0)
		target_rot += Vector3(-sway_y * 1.5, sway_x * 2.0, -sway_x * 3.0)

	mouse_input = mouse_input.lerp(Vector2.ZERO, sway_smooth * delta)
	w_node.position = w_node.position.lerp(target_pos, 24.0 * delta)
	w_node.rotation.x = lerp_angle(w_node.rotation.x, target_rot.x, 24.0 * delta)
	w_node.rotation.y = lerp_angle(w_node.rotation.y, target_rot.y, 24.0 * delta)
	w_node.rotation.z = lerp_angle(w_node.rotation.z, target_rot.z, 24.0 * delta)


func _physics_process(delta: float) -> void:
	if is_local_player:
		_process_local_movement(delta)

		# Broadcast transform to remote peers
		var net := _get_net_mgr()
		if net and net.get("is_multiplayer_active"):
			net_sync_timer += delta
			if net_sync_timer >= NET_SYNC_INTERVAL:
				net_sync_timer = 0.0
				rpc("sync_transform", global_position, rotation.y, head.rotation.x, is_crouching)
	else:
		# Interpolate remote peer transform
		global_position = global_position.lerp(target_pos, 18.0 * delta)
		rotation.y = lerp_angle(rotation.y, target_rot_y, 18.0 * delta)
		head.rotation.x = lerp_angle(head.rotation.x, target_head_x, 18.0 * delta)


func _process_local_movement(delta: float) -> void:
	if is_dead:
		velocity = Vector3.ZERO
		move_and_slide()
		return

	if not is_on_floor():
		velocity.y -= gravity * delta

	if not was_on_floor and is_on_floor():
		if last_y_velocity < -3.0 and land_sound:
			var land_vol := clampf(abs(last_y_velocity) * 0.75 - 2.0, -4.0, 3.0)
			land_sound.volume_db = land_vol
			land_sound.pitch_scale = randf_range(0.88, 0.98)
			land_sound.play()
	was_on_floor = is_on_floor()
	last_y_velocity = velocity.y

	is_crouching = Input.is_action_pressed("crouch") and is_on_floor()
	var target_head_y := crouch_camera_y if is_crouching else original_camera_y
	head.position.y = lerpf(head.position.y, target_head_y, 12.0 * delta)

	if Input.is_action_just_pressed("jump") and is_on_floor() and not is_crouching:
		velocity.y = jump_velocity
		if jump_sound:
			jump_sound.volume_db = 0.0
			jump_sound.pitch_scale = randf_range(1.0, 1.08)
			jump_sound.play()

	# Movement Speed - Fast tactical knife run!
	var knife_speed_mult := 1.2 if active_weapon_index == 3 else 1.0
	if is_crouching:
		current_speed = crouch_speed
	elif Input.is_action_pressed("sprint") and is_on_floor() and not is_aiming:
		current_speed = sprint_speed * knife_speed_mult
	else:
		current_speed = walk_speed * knife_speed_mult

	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_backward")
	var direction := (transform.basis * Vector3(input_dir.x, 0.0, input_dir.y)).normalized()
	var accel := acceleration if is_on_floor() else acceleration * air_control

	if direction:
		velocity.x = lerpf(velocity.x, direction.x * current_speed, accel * delta)
		velocity.z = lerpf(velocity.z, direction.z * current_speed, accel * delta)
	else:
		velocity.x = lerpf(velocity.x, 0.0, friction * delta)
		velocity.z = lerpf(velocity.z, 0.0, friction * delta)

	if is_on_floor() and direction.length() > 0.1:
		var step_interval := 0.28 if current_speed > walk_speed else (0.55 if is_crouching else 0.44)
		step_timer += delta
		if step_timer >= step_interval:
			step_timer = 0.0
			if step_sound:
				if current_speed > walk_speed:
					step_sound.volume_db = -1.5
					step_sound.pitch_scale = randf_range(1.10, 1.20)
				elif is_crouching:
					step_sound.volume_db = -10.0
					step_sound.pitch_scale = randf_range(0.85, 0.92)
				else:
					step_sound.volume_db = -5.5
					step_sound.pitch_scale = randf_range(0.96, 1.04)
				step_sound.play()
	else:
		step_timer = 0.22

	if head_bob_enabled and is_on_floor() and direction and not is_crouching:
		var amp := bob_amplitude * (0.2 if is_aiming else 1.0)
		bob_timer += delta * velocity.length()
		camera.position.y = sin(bob_timer * bob_frequency) * amp
	else:
		camera.position.y = lerpf(camera.position.y, 0.0, 10.0 * delta)
		bob_timer = 0.0

	move_and_slide()


func _shoot() -> void:
	var cur_w := get_current_weapon()
	if not cur_w:
		return

	fire_timer = cur_w.fire_rate
	cur_w.current_ammo -= 1
	_update_hud()

	if shoot_sound:
		if active_weapon_index == 0:
			# Vanguard AR (Vandal style): Punchy, crisp ballistic rifle shot
			shoot_sound.stream = SOUND_RIFLE
			shoot_sound.volume_db = 1.0
			shoot_sound.pitch_scale = randf_range(0.97, 1.03)
		elif active_weapon_index == 1:
			# Phantom Pistol (Classic / Ghost): Snappy high-crack report
			shoot_sound.stream = SOUND_PISTOL
			shoot_sound.volume_db = 2.0
			shoot_sound.pitch_scale = randf_range(0.98, 1.05)
		elif active_weapon_index == 2:
			# Operator Sniper: Heavy booming high-caliber shot
			shoot_sound.stream = SOUND_SNIPER
			shoot_sound.volume_db = 4.0
			shoot_sound.pitch_scale = randf_range(0.96, 1.02)
			camera.rotation.x += deg_to_rad(3.5)
		shoot_sound.play()

	if muzzle_light:
		muzzle_light.light_energy = 2.8

	var w_node := cur_w.node
	if w_node:
		var kick := cur_w.recoil_kick * (0.55 if is_aiming else 1.0)
		var lift := cur_w.recoil_lift * (0.55 if is_aiming else 1.0)
		w_node.position.z += kick
		w_node.rotation.x += deg_to_rad(lift)

		if w_node.has_node("MuzzlePoint/MuzzleFlash"):
			w_node.get_node("MuzzlePoint/MuzzleFlash").flash()

	var muzzle_pos := camera.global_position + (-camera.global_transform.basis.z * 0.4) + (camera.global_transform.basis.x * 0.2) + (-camera.global_transform.basis.y * 0.15)
	if w_node.has_node("MuzzlePoint"):
		var m_marker: Marker3D = w_node.get_node("MuzzlePoint")
		muzzle_pos = m_marker.global_position

	# RayCast Hit Detection
	shoot_ray.force_raycast_update()
	var hit_target := camera.global_position - (camera.global_transform.basis.z * 80.0)

	if shoot_ray.is_colliding():
		var collider := shoot_ray.get_collider()
		hit_target = shoot_ray.get_collision_point()
		var hit_normal := shoot_ray.get_collision_normal()

		_spawn_impact(hit_target, hit_normal)

		if collider and collider != self:
			if collider.has_method("take_damage_with_attacker"):
				collider.take_damage_with_attacker(cur_w.damage, player_name, peer_id)
				_show_hitmarker()
			elif collider.has_method("take_damage"):
				collider.take_damage(cur_w.damage)
				_show_hitmarker()

	# Spawn Local Tracer
	_spawn_tracer(muzzle_pos, hit_target, cur_w.tracer_color)

	# Broadcast shot effects to peers
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		rpc("rpc_fire_fx", muzzle_pos, hit_target, active_weapon_index)


func _perform_knife_attack(is_heavy: bool) -> void:
	fire_timer = 0.52 if is_heavy else 0.32
	var dmg := 100 if is_heavy else 55

	if shoot_sound:
		shoot_sound.stream = SOUND_KNIFE
		if is_heavy:
			# Heavy thrust: Solid blade slice
			shoot_sound.volume_db = 2.0
			shoot_sound.pitch_scale = randf_range(0.85, 0.95)
		else:
			# Fast slash: Swift metallic swoosh
			shoot_sound.volume_db = 0.0
			shoot_sound.pitch_scale = randf_range(1.05, 1.20)
		shoot_sound.play()

	# Knife Slash Animation
	if knife_node:
		var cur_w := get_current_weapon()
		var def_p := cur_w.default_pos if cur_w else knife_node.position
		var tween := create_tween()
		if is_heavy:
			# Heavy Forward Thrust
			tween.tween_property(knife_node, "position:z", def_p.z - 0.22, 0.08)
			tween.parallel().tween_property(knife_node, "rotation:x", deg_to_rad(-25.0), 0.08)
			tween.chain().tween_property(knife_node, "position", def_p, 0.2)
			tween.parallel().tween_property(knife_node, "rotation", Vector3.ZERO, 0.2)
		else:
			# Fast Horizontal Slash
			tween.tween_property(knife_node, "position:x", def_p.x - 0.24, 0.08)
			tween.parallel().tween_property(knife_node, "rotation:y", deg_to_rad(65.0), 0.08)
			tween.chain().tween_property(knife_node, "position", def_p, 0.16)
			tween.parallel().tween_property(knife_node, "rotation", Vector3.ZERO, 0.16)

	# Melee range raycast (2.6 meters)
	var space_state := get_world_3d().direct_space_state
	var from := camera.global_position
	var to := from - (camera.global_transform.basis.z * 2.6)
	var query := PhysicsRayQueryParameters3D.create(from, to)
	query.exclude = [get_rid()]
	var result := space_state.intersect_ray(query)

	if result:
		var collider = result.collider
		_spawn_impact(result.position, result.normal)
		if collider and collider != self:
			if collider.has_method("take_damage_with_attacker"):
				collider.take_damage_with_attacker(dmg, player_name, peer_id)
				_show_hitmarker()
			elif collider.has_method("take_damage"):
				collider.take_damage(dmg)
				_show_hitmarker()


@rpc("any_peer", "call_remote", "unreliable")
func rpc_fire_fx(origin: Vector3, hit_point: Vector3, weapon_idx: int) -> void:
	if weapon_idx == 3:
		# Knife sound for remote peer
		if shoot_sound:
			shoot_sound.pitch_scale = randf_range(1.5, 1.7)
			shoot_sound.play()
		return

	# Third-person muzzle flash
	var tp_flash_marker: Node3D = null
	if weapon_idx == 0:
		tp_flash_marker = tp_rifle.get_node_or_null("MuzzlePoint/MuzzleFlash")
	elif weapon_idx == 1:
		tp_flash_marker = tp_pistol.get_node_or_null("MuzzlePoint/MuzzleFlash")
	elif weapon_idx == 2:
		tp_flash_marker = tp_sniper.get_node_or_null("MuzzlePoint/MuzzleFlash")

	if tp_flash_marker and tp_flash_marker.has_method("flash"):
		tp_flash_marker.flash()

	if shoot_sound:
		shoot_sound.pitch_scale = randf_range(0.95, 1.05)
		shoot_sound.play()

	var col := Color(0.2, 0.9, 1.0) if weapon_idx != 1 else Color(0.3, 1.0, 0.45)
	_spawn_tracer(origin, hit_point, col)


@rpc("any_peer", "call_remote", "unreliable")
func sync_transform(pos: Vector3, rot_y: float, head_x: float, crouching: bool) -> void:
	target_pos = pos
	target_rot_y = rot_y
	target_head_x = head_x
	is_crouching = crouching


func _set_tp_weapon(idx: int) -> void:
	if tp_rifle:
		tp_rifle.visible = (idx == 0)
	if tp_pistol:
		tp_pistol.visible = (idx == 1)
	if tp_sniper:
		tp_sniper.visible = (idx == 2)
	if tp_knife:
		tp_knife.visible = (idx == 3)


@rpc("any_peer", "call_local", "reliable")
func rpc_set_active_weapon(idx: int) -> void:
	_set_tp_weapon(idx)


func _spawn_tracer(from: Vector3, to: Vector3, col: Color) -> void:
	var tracer = TRACER_SCENE.instantiate()
	var spawn_parent = get_tree().current_scene if get_tree().current_scene else get_tree().root
	spawn_parent.add_child(tracer)
	tracer.setup(from, to, col)


func _spawn_impact(point: Vector3, normal: Vector3) -> void:
	var impact = IMPACT_SCENE.instantiate()
	var spawn_parent = get_tree().current_scene if get_tree().current_scene else get_tree().root
	spawn_parent.add_child(impact)
	impact.global_position = point
	if normal.is_equal_approx(Vector3.UP):
		impact.look_at(point + normal, Vector3.FORWARD)
	elif normal.is_equal_approx(Vector3.DOWN):
		impact.look_at(point + normal, Vector3.BACK)
	else:
		impact.look_at(point + normal, Vector3.UP)


func _show_hitmarker() -> void:
	var hud = get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("show_hitmarker"):
		hud.show_hitmarker()


func _reload() -> void:
	var cur_w := get_current_weapon()
	if not cur_w or is_reloading or cur_w.current_ammo == cur_w.max_ammo or cur_w.reserve_ammo <= 0:
		return

	is_reloading = true
	if reload_sound:
		reload_sound.play()

	var w_node := cur_w.node
	if w_node:
		var tween := create_tween()
		tween.tween_property(w_node, "position:y", cur_w.default_pos.y - 0.22, 0.35)
		tween.tween_interval(0.3)
		tween.tween_property(w_node, "position:y", cur_w.default_pos.y, 0.35)

	await get_tree().create_timer(1.0).timeout

	if is_instance_valid(self):
		var needed := cur_w.max_ammo - cur_w.current_ammo
		var reload_amount := mini(needed, cur_w.reserve_ammo)
		cur_w.current_ammo += reload_amount
		cur_w.reserve_ammo -= reload_amount
		is_reloading = false
		_update_hud()


func _switch_weapon(new_index: int) -> void:
	if new_index == active_weapon_index or is_switching or new_index < 0 or new_index >= weapons.size():
		return

	is_switching = true
	is_reloading = false
	var old_w := get_current_weapon()

	if old_w and old_w.node:
		var tween := create_tween()
		tween.tween_property(old_w.node, "position:y", old_w.default_pos.y - 0.35, 0.15)
		await tween.finished

	_select_weapon(new_index)

	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		rpc("rpc_set_active_weapon", new_index)

	var cur_w := get_current_weapon()
	if cur_w and cur_w.node:
		cur_w.node.position.y = cur_w.default_pos.y - 0.35
		var tween := create_tween()
		tween.tween_property(cur_w.node, "position:y", cur_w.default_pos.y, 0.18)
		await tween.finished

	is_switching = false


func _select_weapon(index: int) -> void:
	active_weapon_index = index
	for i in range(weapons.size()):
		var w := weapons[i]
		if w.node:
			w.node.visible = (i == active_weapon_index)
			w.node.position = w.default_pos
			w.node.rotation = w.default_rot
	_set_tp_weapon(index)
	_update_hud()


func get_current_weapon() -> WeaponData:
	if active_weapon_index >= 0 and active_weapon_index < weapons.size():
		return weapons[active_weapon_index]
	return null


func _update_hud() -> void:
	var hud = get_tree().get_first_node_in_group("hud")
	var cur_w := get_current_weapon()
	if hud and cur_w:
		if hud.has_method("update_weapon"):
			hud.update_weapon(cur_w.name)
		if hud.has_method("update_ammo"):
			if active_weapon_index == 3:
				hud.update_ammo_text("TACTICAL BLADE // MELEE")
			else:
				hud.update_ammo(cur_w.current_ammo, cur_w.reserve_ammo)


func take_damage(amount: int) -> void:
	take_damage_with_attacker(amount, "ENEMY", 0)


func take_damage_with_attacker(amount: int, attacker_name: String, attacker_id: int) -> void:
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		rpc("rpc_apply_damage", amount, attacker_name, attacker_id)
	else:
		_apply_damage_internal(amount, attacker_name, attacker_id)


@rpc("any_peer", "call_local", "reliable")
func rpc_apply_damage(amount: int, attacker_name: String, attacker_id: int) -> void:
	_apply_damage_internal(amount, attacker_name, attacker_id)


func _apply_damage_internal(amount: int, attacker_name: String, attacker_id: int) -> void:
	if is_dead:
		return

	current_health = clampi(current_health - amount, 0, max_health)
	_update_label()

	# Spawn 3D floating damage number
	var dmg_num = DAMAGE_NUMBER_SCENE.instantiate()
	get_tree().current_scene.add_child(dmg_num)
	dmg_num.global_position = global_position + Vector3(randf_range(-0.3, 0.3), 1.6, randf_range(-0.3, 0.3))
	dmg_num.setup(amount, amount >= 50)

	if is_local_player:
		var hud = get_tree().get_first_node_in_group("hud")
		if hud:
			if hud.has_method("update_health"):
				hud.update_health(current_health, max_health)
			if hud.has_method("show_damage_flash"):
				hud.show_damage_flash()

	if current_health <= 0:
		_die(attacker_name, attacker_id)


func _die(killer_name: String, killer_id: int) -> void:
	is_dead = true
	velocity = Vector3.ZERO
	_update_label()

	var hud = get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("notify_kill"):
		hud.notify_kill(killer_name, player_name)

	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active") and killer_id != 0:
		net.record_kill(killer_id, peer_id)

	await get_tree().create_timer(2.2).timeout
	_respawn()


func _respawn() -> void:
	global_position = spawn_position
	target_pos = spawn_position
	reset_physics_interpolation()
	current_health = max_health
	is_dead = false
	_update_label()

	if is_local_player:
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("update_health"):
			hud.update_health(current_health, max_health)


func _throw_smoke() -> void:
	if smoke_cooldown > 0.0 or is_reloading or is_switching:
		return

	smoke_cooldown = 12.0
	var throw_pos := camera.global_position + (-camera.global_transform.basis.z * 0.7)
	var throw_impulse := (-camera.global_transform.basis.z * 18.0) + (Vector3.UP * 4.5)

	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		rpc("rpc_spawn_smoke", throw_pos, throw_impulse)
	else:
		_spawn_smoke_local(throw_pos, throw_impulse)


@rpc("any_peer", "call_local", "reliable")
func rpc_spawn_smoke(pos: Vector3, impulse: Vector3) -> void:
	_spawn_smoke_local(pos, impulse)


func _spawn_smoke_local(pos: Vector3, impulse: Vector3) -> void:
	var proj = SMOKE_PROJECTILE_SCENE.instantiate()
	get_tree().current_scene.add_child(proj)
	proj.global_position = pos
	proj.apply_central_impulse(impulse)


func _inspect_weapon() -> void:
	var cur_w := get_current_weapon()
	if not cur_w or not cur_w.node or is_inspecting or is_aiming or is_reloading or is_switching:
		return

	is_inspecting = true

	# Sick knife twirl inspect trick!
	if active_weapon_index == 3 and knife_node:
		var tween := create_tween()
		tween.tween_property(knife_node, "rotation:x", knife_node.rotation.x + TAU, 0.42).set_trans(Tween.TRANS_BACK)
		tween.parallel().tween_property(knife_node, "rotation:y", knife_node.rotation.y + deg_to_rad(35.0), 0.21)
		tween.chain().tween_property(knife_node, "rotation", cur_w.default_rot, 0.18)
		await tween.finished
		is_inspecting = false
		return

	var tween := create_tween()
	tween.tween_property(cur_w.node, "rotation:z", cur_w.default_rot.z + deg_to_rad(30.0), 0.35)
	tween.parallel().tween_property(cur_w.node, "rotation:y", cur_w.default_rot.y - deg_to_rad(25.0), 0.35)
	tween.tween_interval(0.45)
	tween.tween_property(cur_w.node, "rotation", cur_w.default_rot, 0.35)
	await tween.finished
	is_inspecting = false


# ============================================================================
# Operative Customization & Weapon Skins Synchronization
# ============================================================================

func _apply_profile_customization() -> void:
	var prof := get_node_or_null("/root/ProfileManager")
	if not prof:
		_select_weapon(0)
		return

	var suit: Dictionary = prof.get_current_suit()
	var visor_col: Color = prof.get_current_visor_color()
	var skin: Dictionary = prof.get_current_weapon_skin()
	var starting_wp_idx: int = prof.current_weapon_index

	# 1. Update First-Person Weapon materials with chosen skin & visor glow
	_apply_weapon_skin_to_node(rifle_node, skin, visor_col)
	_apply_weapon_skin_to_node(pistol_node, skin, visor_col)
	_apply_weapon_skin_to_node(sniper_node, skin, visor_col)
	_apply_weapon_skin_to_node(knife_node, skin, visor_col)

	# 2. Update Third-Person Visuals
	_apply_tp_customization(suit, visor_col, skin)

	# 3. Equip the chosen weapon
	_select_weapon(clamp(starting_wp_idx, 0, weapons.size() - 1))

	# 4. If in LAN multiplayer, broadcast customization to peers
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		rpc("rpc_sync_customization", prof.get_customization_dictionary())


func _apply_weapon_skin_to_node(w_node: Node3D, skin: Dictionary, visor_col: Color) -> void:
	if not w_node: return

	var pri_mat := StandardMaterial3D.new()
	pri_mat.albedo_color = skin.get("primary_color", Color(0.14, 0.16, 0.19))
	pri_mat.metallic = skin.get("metallic", 0.72)
	pri_mat.roughness = skin.get("roughness", 0.28)

	var acc_mat := StandardMaterial3D.new()
	acc_mat.albedo_color = skin.get("accent_color", Color(0.24, 0.26, 0.30))
	acc_mat.metallic = 0.85
	acc_mat.roughness = 0.32

	var steel_mat := StandardMaterial3D.new()
	steel_mat.albedo_color = Color(0.16, 0.18, 0.21, 1.0)
	steel_mat.metallic = 0.95
	steel_mat.roughness = 0.24

	var polymer_mat := StandardMaterial3D.new()
	polymer_mat.albedo_color = Color(0.08, 0.09, 0.10, 1.0)
	polymer_mat.metallic = 0.05
	polymer_mat.roughness = 0.85

	var lens_mat := StandardMaterial3D.new()
	lens_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	lens_mat.albedo_color = Color(0.04, 0.08, 0.11, 0.70)
	lens_mat.roughness = 0.04
	lens_mat.clearcoat_enabled = true
	lens_mat.clearcoat = 1.0

	var glow_mat := StandardMaterial3D.new()
	var glow_c: Color = skin.get("glow_color", Color(0.15, 0.95, 0.45))
	glow_mat.albedo_color = glow_c
	glow_mat.emission_enabled = true
	glow_mat.emission = glow_c
	glow_mat.emission_energy_multiplier = 2.5

	for child in w_node.find_children("*", "MeshInstance3D", true, false):
		var m := child as MeshInstance3D
		var nm := m.name
		if "Lens" in nm or "Glass" in nm:
			m.material_override = lens_mat
		elif "Reticle" in nm:
			m.material_override = glow_mat
		elif "Mount" in nm or "Ring" in nm:
			m.material_override = steel_mat
		elif "Barrel" in nm or "Muzzle" in nm or "Bolt" in nm or "Chamber" in nm or "Rail" in nm or "Bipod" in nm or "Trigger" in nm:
			m.material_override = steel_mat
		elif "Grip" in nm or "Cheek" in nm or "Pad" in nm or "Handle" in nm or "Stock" in nm:
			m.material_override = polymer_mat
		elif "Accent" in nm or "Bevel" in nm or "Stripe" in nm or "Trim" in nm:
			m.material_override = acc_mat
		else:
			m.material_override = pri_mat


func _apply_tp_customization(suit: Dictionary, visor_col: Color, skin: Dictionary) -> void:
	if not visuals_3d: return

	var suit_mat := StandardMaterial3D.new()
	suit_mat.albedo_color = suit.get("suit_color", Color(0.12, 0.15, 0.20))
	suit_mat.metallic = suit.get("metallic", 0.4)
	suit_mat.roughness = suit.get("roughness", 0.5)

	var armor_mat := StandardMaterial3D.new()
	armor_mat.albedo_color = suit.get("armor_color", Color(0.2, 0.22, 0.28))
	armor_mat.metallic = clampf(suit.get("metallic", 0.4) + 0.2, 0.0, 1.0)
	armor_mat.roughness = clampf(suit.get("roughness", 0.5) - 0.15, 0.1, 1.0)

	var visor_mat := StandardMaterial3D.new()
	visor_mat.albedo_color = visor_col
	visor_mat.emission_enabled = true
	visor_mat.emission = visor_col
	visor_mat.emission_energy_multiplier = 3.5

	var torso = visuals_3d.get_node_or_null("Torso")
	if torso: torso.material_override = suit_mat
	var leg_l = visuals_3d.get_node_or_null("LegLeft")
	if leg_l: leg_l.material_override = suit_mat
	var leg_r = visuals_3d.get_node_or_null("LegRight")
	if leg_r: leg_r.material_override = suit_mat

	var chest = visuals_3d.get_node_or_null("ChestPlate")
	if chest: chest.material_override = armor_mat
	var head_m = visuals_3d.get_node_or_null("HeadMesh")
	if head_m: head_m.material_override = armor_mat

	var core = visuals_3d.get_node_or_null("ChestPlate/Core")
	if core: core.material_override = visor_mat
	var visor = visuals_3d.get_node_or_null("HeadMesh/Visor")
	if visor: visor.material_override = visor_mat

	# Third-Person Weapons
	_apply_weapon_skin_to_node(tp_rifle, skin, visor_col)
	_apply_weapon_skin_to_node(tp_pistol, skin, visor_col)
	_apply_weapon_skin_to_node(tp_sniper, skin, visor_col)
	_apply_weapon_skin_to_node(tp_knife, skin, visor_col)


@rpc("any_peer", "call_remote", "reliable")
func rpc_sync_customization(custom_dict: Dictionary) -> void:
	var suit: Dictionary = custom_dict.get("suit_data", {})
	var visor_col: Color = custom_dict.get("visor_color", Color(0.15, 0.85, 1.0))
	var skin: Dictionary = custom_dict.get("skin_data", {})
	_apply_tp_customization(suit, visor_col, skin)
