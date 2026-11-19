# ============================================================================
# WarehouseYard - Competitive 4v4 TDM Arena Controller
# ============================================================================
# Compact 60m x 60m symmetrical close-quarters tactical arena.
# Supports Solo practice (with target dummies & bots) and 8-Player LAN matches.
# ============================================================================
extends Node3D

const PLAYER_SCENE = preload("res://scenes/player/player.tscn")

const SPAWN_POINTS: Array[Vector3] = [
	Vector3(-5.0, 1.2, 26.0),    # Team South (Spawn 1)
	Vector3(5.0, 1.2, -26.0),    # Team North (Spawn 1)
	Vector3(-1.8, 1.2, 26.0),    # Team South (Spawn 2)
	Vector3(1.8, 1.2, -26.0),    # Team North (Spawn 2)
	Vector3(1.8, 1.2, 26.0),     # Team South (Spawn 3)
	Vector3(-1.8, 1.2, -26.0),   # Team North (Spawn 3)
	Vector3(5.0, 1.2, 26.0),     # Team South (Spawn 4)
	Vector3(-5.0, 1.2, -26.0),   # Team North (Spawn 4)
]

@onready var players_container: Node3D = $Players
@onready var world_env: WorldEnvironment = $WorldEnvironment
@onready var sun_light: DirectionalLight3D = $Sun


func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _ready() -> void:
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		# Multiplayer: clean any static player and spawn per-peer instances
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
		# Singleplayer sandbox: spawn local player at spawn point 0
		print("[WarehouseYard] Running in Solo Practice Mode.")
		if not get_node_or_null("Player") and players_container and players_container.get_child_count() == 0:
			_spawn_player(1)


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
	player_inst.position = SPAWN_POINTS[spawn_idx]
	
	# Face towards center of map
	if player_inst.position.z > 0:
		player_inst.rotation.y = deg_to_rad(180) # Facing North
	else:
		player_inst.rotation.y = deg_to_rad(0)   # Facing South

	players_container.add_child(player_inst)
	print("[WarehouseYard] Spawned operative for peer %d at %s" % [peer_id, player_inst.position])


func _on_network_player_connected(peer_id: int, _player_data: Dictionary) -> void:
	_spawn_player(peer_id)


func _on_network_player_disconnected(peer_id: int) -> void:
	var p_name := "Player_%d" % peer_id
	if players_container and players_container.has_node(p_name):
		var p_node := players_container.get_node(p_name)
		p_node.queue_free()
		print("[WarehouseYard] Removed operative node for peer %d" % peer_id)


## Quality presets for weaker laptops
func apply_quality_preset(preset: String) -> void:
	if not world_env or not world_env.environment:
		return
	var env: Environment = world_env.environment
	match preset.to_upper():
		"LOW":
			env.ssao_enabled = false
			env.ssr_enabled = false
			env.glow_enabled = false
			env.fog_enabled = false
			if sun_light:
				sun_light.shadow_enabled = true
				sun_light.directional_shadow_max_distance = 45.0
		"MEDIUM":
			env.ssao_enabled = true
			env.ssr_enabled = false
			env.glow_enabled = true
			env.fog_enabled = true
			if sun_light:
				sun_light.shadow_enabled = true
				sun_light.directional_shadow_max_distance = 65.0
		"HIGH":
			env.ssao_enabled = true
			env.ssr_enabled = true
			env.glow_enabled = true
			env.fog_enabled = true
			if sun_light:
				sun_light.shadow_enabled = true
				sun_light.directional_shadow_max_distance = 75.0
