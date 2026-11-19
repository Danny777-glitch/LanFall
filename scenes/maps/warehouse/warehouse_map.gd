# ============================================================================
# TestMap - District 7 Match Controller (Singleplayer & LAN Multiplayer)
# ============================================================================
extends Node3D

const PLAYER_SCENE = preload("res://scenes/player/player.tscn")

const SPAWN_POINTS: Array[Vector3] = [
	Vector3(0.0, 1.2, 42.0),     # Team 1 South Twin Sheds Center
	Vector3(0.0, 1.2, -42.0),    # Team 2 North Twin Sheds Center
	Vector3(-5.5, 1.2, 43.0),    # Team 1 South Left Shed
	Vector3(5.5, 1.2, -43.0),    # Team 2 North Left Shed
	Vector3(5.5, 1.2, 43.0),     # Team 1 South Right Shed
	Vector3(-5.5, 1.2, -43.0),   # Team 2 North Right Shed
]

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

	players_container.add_child(player_inst)
	print("[TestMap] Spawned player node for peer %d at %s" % [peer_id, player_inst.position])


func _on_network_player_connected(peer_id: int, _player_data: Dictionary) -> void:
	_spawn_player(peer_id)


func _on_network_player_disconnected(peer_id: int) -> void:
	var p_name := "Player_%d" % peer_id
	if players_container and players_container.has_node(p_name):
		var p_node := players_container.get_node(p_name)
		p_node.queue_free()
		print("[TestMap] Removed player node for peer %d" % peer_id)
