# ============================================================================
# TestMap - District 7 Match Controller (Singleplayer & LAN Multiplayer)
# ============================================================================
extends Node3D

const PLAYER_SCENE = preload("res://scenes/player/player.tscn")

const SPAWN_POINTS: Array[Dictionary] = [
	{ "pos": Vector3(-4.0, 0.05, 36.0), "rot_y": deg_to_rad(180.0), "team": 1 },   # Team 1 South Mid-Left (Covered by Warehouse South Wall)
	{ "pos": Vector3(4.0, 0.05, -36.0), "rot_y": 0.0, "team": 2 },                # Team 2 North Mid-Right (Covered by Warehouse North Wall)
	{ "pos": Vector3(-6.5, 0.05, 36.0), "rot_y": deg_to_rad(180.0), "team": 1 },  # Team 1 South West Flank
	{ "pos": Vector3(6.5, 0.05, -36.0), "rot_y": 0.0, "team": 2 },                # Team 2 North East Flank
	{ "pos": Vector3(16.5, 0.05, 36.0), "rot_y": deg_to_rad(180.0), "team": 1 },  # Team 1 South East Rail Flank
	{ "pos": Vector3(-16.5, 0.05, -36.0), "rot_y": 0.0, "team": 2 },              # Team 2 North West Pergola Flank
]

const SPAWN_PROTECTION_DURATION := 3.0

@onready var players_container: Node3D = $Players



func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _ready() -> void:
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		# In multiplayer: clear pre-placed player and spawn per-peer players
		var static_player = get_node_or_null("Player")
		if static_player:
			static_player.queue_free()

		var p_dict = net.get("players")
		if p_dict:
			for pid in p_dict.keys():
				_spawn_player(pid)

		if net.has_signal("player_connected"):
			net.player_connected.connect(_on_network_player_connected)
		if net.has_signal("player_disconnected"):
			net.player_disconnected.connect(_on_network_player_disconnected)
	else:
		# Singleplayer sandbox: pre-placed player remains active, or spawn Player 1
		print("[TestMap] Running in Solo Practice Mode.")
		if not get_node_or_null("Player") and players_container and players_container.get_child_count() == 0:
			_spawn_player(1)

	var perf := get_node_or_null("/root/PerfSettings")
	if perf:
		perf.set_in_menu(false)
		apply_quality_preset(perf.quality_preset)


func _spawn_player(peer_id: int) -> void:
	if not players_container:
		return

	var p_name := "Player_%d" % peer_id
	if players_container.has_node(p_name):
		return

	var player_inst = PLAYER_SCENE.instantiate()
	player_inst.name = p_name
	player_inst.peer_id = peer_id
	player_inst.set_multiplayer_authority(peer_id)

	# Assign spawn point based on peer index
	var spawn_idx := (peer_id - 1) % SPAWN_POINTS.size()
	var spawn_data: Dictionary = SPAWN_POINTS[spawn_idx]
	player_inst.position = spawn_data["pos"]
	player_inst.rotation.y = spawn_data["rot_y"]

	players_container.add_child(player_inst)
	print("[TestMap] Spawned player node for peer %d at %s facing %s" % [peer_id, player_inst.position, player_inst.rotation.y])

	# Spawn protection: 3 seconds of invulnerability
	if player_inst.has_method("grant_spawn_protection"):
		player_inst.grant_spawn_protection(SPAWN_PROTECTION_DURATION)
	else:
		_apply_spawn_protection(player_inst)


func _apply_spawn_protection(player: Node) -> void:
	if player.has_method("set_invulnerable"):
		player.set_invulnerable(true)
	elif "invulnerable" in player:
		player.invulnerable = true

	var timer := get_tree().create_timer(SPAWN_PROTECTION_DURATION)
	timer.timeout.connect(func():
		if is_instance_valid(player):
			if player.has_method("set_invulnerable"):
				player.set_invulnerable(false)
			elif "invulnerable" in player:
				player.invulnerable = false
			print("[TestMap] Spawn protection ended for %s" % player.name)
	)


func _on_network_player_connected(peer_id: int, _player_data: Dictionary) -> void:
	_spawn_player(peer_id)


func _on_network_player_disconnected(peer_id: int) -> void:
	var p_name := "Player_%d" % peer_id
	if players_container and players_container.has_node(p_name):
		var p_node := players_container.get_node(p_name)
		p_node.queue_free()
		print("[TestMap] Removed player node for peer %d" % peer_id)


## Quality presets for Forward+ graphics scalability (Low, Medium, High, Ultra)
func apply_quality_preset(preset: String) -> void:
	var env_node: WorldEnvironment = get_node_or_null("WorldEnvironment")
	var sun_node: DirectionalLight3D = get_node_or_null("Sun")
	if not env_node or not env_node.environment:
		return
	var env: Environment = env_node.environment

	match preset.to_upper():
		"POWER_SAVER":
			# Maximum Battery / Cool Whisper Fan Preset (Cap 60 FPS, Low Power)
			env.sdfgi_enabled = false
			env.ssil_enabled = false
			env.ssao_enabled = true
			env.ssao_radius = 1.0
			env.ssao_intensity = 1.2
			env.ssr_enabled = false
			env.volumetric_fog_enabled = false
			env.glow_enabled = false
			if sun_node:
				sun_node.directional_shadow_blend_splits = false
				sun_node.shadow_blur = 1.0
				sun_node.directional_shadow_max_distance = 55.0
			print("[Graphics] Applied preset: POWER_SAVER (Cool & Silent)")

		"LOW":
			# High FPS / Integrated GPU / Low VRAM (~1.0 GB)
			env.sdfgi_enabled = false
			env.ssil_enabled = false
			env.ssao_enabled = false
			env.ssr_enabled = false
			env.volumetric_fog_enabled = false
			env.glow_enabled = false
			if sun_node:
				sun_node.directional_shadow_blend_splits = false
				sun_node.shadow_blur = 1.0
				sun_node.directional_shadow_max_distance = 60.0
			print("[Graphics] Applied preset: LOW (Performance Mode)")

		"MEDIUM":
			# Balanced / Older discrete GPUs (~1.5-2.0 GB VRAM)
			env.sdfgi_enabled = false
			env.ssil_enabled = false
			env.ssao_enabled = true
			env.ssao_radius = 1.2
			env.ssao_intensity = 1.4
			env.ssr_enabled = false
			env.volumetric_fog_enabled = false
			env.glow_enabled = true
			env.glow_intensity = 0.15
			if sun_node:
				sun_node.directional_shadow_blend_splits = true
				sun_node.shadow_blur = 1.2
				sun_node.directional_shadow_max_distance = 75.0
			print("[Graphics] Applied preset: MEDIUM (Balanced)")

		"HIGH":
			# Recommended Default for RTX 3050 6GB (~2.5-3.2 GB VRAM, 300+ FPS)
			env.sdfgi_enabled = true
			env.sdfgi_cascades = 4
			env.sdfgi_min_cell_size = 0.25
			env.sdfgi_bounce_feedback = 0.45
			env.ssil_enabled = true
			env.ssil_radius = 5.0
			env.ssil_intensity = 0.8
			env.ssao_enabled = true
			env.ssao_radius = 1.5
			env.ssao_intensity = 1.8
			env.ssr_enabled = true
			env.ssr_max_steps = 32
			env.volumetric_fog_enabled = true
			env.volumetric_fog_density = 0.008
			env.glow_enabled = true
			env.glow_intensity = 0.25
			if sun_node:
				sun_node.directional_shadow_blend_splits = true
				sun_node.shadow_blur = 1.4
				sun_node.directional_shadow_max_distance = 90.0
			print("[Graphics] Applied preset: HIGH (RTX 3050 Target)")

		"ULTRA":
			# Maximum Visual Fidelity (stays safely under 4.0 GB VRAM ceiling)
			env.sdfgi_enabled = true
			env.sdfgi_cascades = 6
			env.sdfgi_min_cell_size = 0.20
			env.sdfgi_bounce_feedback = 0.55
			env.ssil_enabled = true
			env.ssil_radius = 6.0
			env.ssil_intensity = 1.2
			env.ssao_enabled = true
			env.ssao_radius = 1.8
			env.ssao_intensity = 2.4
			env.ssr_enabled = true
			env.ssr_max_steps = 64
			env.volumetric_fog_enabled = true
			env.volumetric_fog_density = 0.012
			env.glow_enabled = true
			env.glow_intensity = 0.35
			if sun_node:
				sun_node.directional_shadow_blend_splits = true
				sun_node.shadow_blur = 1.6
				sun_node.directional_shadow_max_distance = 100.0
			print("[Graphics] Applied preset: ULTRA (Max Fidelity)")
