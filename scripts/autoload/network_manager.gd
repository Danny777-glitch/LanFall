# ============================================================================
# NetworkManager — LAN Multiplayer Controller (ENet)
# ============================================================================
# Manages server creation, client connection, peer discovery, player registry,
# and high-performance LAN state synchronization for LAN Fall.
# ============================================================================
extends Node

const DEFAULT_PORT: int = 7777
const MAX_PLAYERS: int = 8

signal player_connected(peer_id: int, player_data: Dictionary)
signal player_disconnected(peer_id: int)
signal server_created()
signal server_joined()
signal connection_failed()
signal server_disconnected()
signal player_list_updated()

var is_multiplayer_active: bool = false
var is_server: bool = false
var local_player_name: String = "OPERATIVE"

# Peer registry: { peer_id: { "name": String, "kills": int, "deaths": int, "ping": int } }
var players: Dictionary = {}


func _ready() -> void:
	multiplayer.peer_connected.connect(_on_peer_connected)
	multiplayer.peer_disconnected.connect(_on_peer_disconnected)
	multiplayer.connected_to_server.connect(_on_connected_to_server)
	multiplayer.connection_failed.connect(_on_connection_failed)
	multiplayer.server_disconnected.connect(_on_server_disconnected)


## Host a LAN match
func host_game(player_name: String, port: int = DEFAULT_PORT) -> Error:
	local_player_name = player_name.strip_edges()
	if local_player_name.is_empty():
		local_player_name = "HOST_OP"

	var peer := ENetMultiplayerPeer.new()
	var err := peer.create_server(port, MAX_PLAYERS)
	if err != OK:
		push_error("Failed to host on port %d: %s" % [port, error_string(err)])
		return err

	multiplayer.multiplayer_peer = peer
	is_multiplayer_active = true
	is_server = true
	players.clear()

	# Register host (peer ID 1)
	players[1] = {
		"name": local_player_name,
		"kills": 0,
		"deaths": 0,
		"ping": 0
	}

	server_created.emit()
	player_list_updated.emit()
	return OK


## Join an existing LAN match
func join_game(ip: String, player_name: String, port: int = DEFAULT_PORT) -> Error:
	local_player_name = player_name.strip_edges()
	if local_player_name.is_empty():
		local_player_name = "CLIENT_OP"

	var clean_ip := ip.strip_edges()
	if clean_ip.is_empty():
		clean_ip = "127.0.0.1"

	var peer := ENetMultiplayerPeer.new()
	var err := peer.create_client(clean_ip, port)
	if err != OK:
		push_error("Failed to connect to %s:%d: %s" % [clean_ip, port, error_string(err)])
		return err

	multiplayer.multiplayer_peer = peer
	is_multiplayer_active = true
	is_server = false
	players.clear()

	return OK


## Start Singleplayer (Practice against bots)
func start_singleplayer(player_name: String = "OPERATIVE") -> void:
	disconnect_game()
	is_multiplayer_active = false
	is_server = true
	local_player_name = player_name
	players.clear()
	players[1] = {
		"name": local_player_name,
		"kills": 0,
		"deaths": 0,
		"ping": 0
	}


## Disconnect and reset multiplayer
func disconnect_game() -> void:
	if multiplayer.multiplayer_peer:
		multiplayer.multiplayer_peer.close()
		multiplayer.multiplayer_peer = null

	is_multiplayer_active = false
	is_server = false
	players.clear()


## Peer connected handler (Server only handles registration)
func _on_peer_connected(id: int) -> void:
	if is_server:
		# Send current player list to the newly connected peer
		rpc_id(id, "_sync_all_players", players)


## Peer disconnected handler
func _on_peer_disconnected(id: int) -> void:
	if players.has(id):
		var p_name: String = players[id].get("name", "Operative")
		players.erase(id)
		player_disconnected.emit(id)
		player_list_updated.emit()
		print("[NetworkManager] Peer %d (%s) disconnected." % [id, p_name])


## Client successfully connected to server
func _on_connected_to_server() -> void:
	var my_id := multiplayer.get_unique_id()
	# Register self with the server
	rpc_id(1, "_register_player", my_id, local_player_name)
	server_joined.emit()


## Client failed to connect
func _on_connection_failed() -> void:
	disconnect_game()
	connection_failed.emit()


## Server closed connection
func _on_server_disconnected() -> void:
	disconnect_game()
	server_disconnected.emit()


## Server registers a player and broadcasts to all
@rpc("any_peer", "call_local", "reliable")
func _register_player(id: int, p_name: String) -> void:
	if not is_server:
		return

	players[id] = {
		"name": p_name,
		"kills": 0,
		"deaths": 0,
		"ping": 0
	}
	# Broadcast updated list to all clients
	rpc("_sync_all_players", players)
	player_connected.emit(id, players[id])
	player_list_updated.emit()


## Sync entire player list to client
@rpc("authority", "call_local", "reliable")
func _sync_all_players(synced_players: Dictionary) -> void:
	players = synced_players
	player_list_updated.emit()


## Update score (Kill/Death) across network
@rpc("any_peer", "call_local", "reliable")
func record_kill(killer_id: int, victim_id: int) -> void:
	if players.has(killer_id):
		players[killer_id]["kills"] += 1
	if players.has(victim_id):
		players[victim_id]["deaths"] += 1
	player_list_updated.emit()


## Helper to detect local LAN IP for easy sharing
func get_local_ip() -> String:
	var addresses := IP.get_local_addresses()
	for addr in addresses:
		# Filter for IPv4 local network (192.168.x.x or 10.x.x.x or 172.16-31.x.x)
		if addr.begins_with("192.168.") or addr.begins_with("10.") or addr.begins_with("172."):
			return addr
	return "127.0.0.1"
