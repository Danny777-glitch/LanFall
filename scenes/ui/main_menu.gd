# ============================================================================
# MainMenu - Tactical Lobby & Matchmaking UI
# ============================================================================
extends Control

const MAP_SCENE_PATH = "res://scenes/maps/warehouse/warehouse_map.tscn"

@onready var name_input: LineEdit = $Panel/VBox/NameBox/NameInput
@onready var solo_btn: Button = $Panel/VBox/SoloBtn
@onready var host_btn: Button = $Panel/VBox/HostBtn
@onready var ip_input: LineEdit = $Panel/VBox/JoinBox/HBox/IPInput
@onready var join_btn: Button = $Panel/VBox/JoinBox/HBox/JoinBtn
@onready var status_label: Label = $Panel/VBox/StatusLabel
@onready var lan_ip_label: Label = $Panel/VBox/LanIPLabel


func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

	# Populate defaults
	var default_names := ["PHOENIX", "JETT", "SOVA", "OMEN", "REYNA", "CYPHER"]
	name_input.text = default_names[randi() % default_names.size()]
	ip_input.text = "127.0.0.1"

	var net := _get_net_mgr()
	var local_ip: String = net.get_local_ip() if net and net.has_method("get_local_ip") else "127.0.0.1"
	lan_ip_label.text = "YOUR LAN IP: %s (PORT: 7777)" % local_ip
	status_label.text = "STANDBY // READY TO DEPLOY"

	solo_btn.pressed.connect(_on_solo_pressed)
	host_btn.pressed.connect(_on_host_pressed)
	join_btn.pressed.connect(_on_join_pressed)

	if net:
		if net.has_signal("server_created"):
			net.server_created.connect(_on_server_created)
		if net.has_signal("server_joined"):
			net.server_joined.connect(_on_server_joined)
		if net.has_signal("connection_failed"):
			net.connection_failed.connect(_on_connection_failed)


func _on_solo_pressed() -> void:
	status_label.text = "STARTING PRACTICE RANGE..."
	status_label.modulate = Color(0.2, 1.0, 0.5)
	var net := _get_net_mgr()
	if net and net.has_method("start_singleplayer"):
		net.start_singleplayer(name_input.text)
	get_tree().change_scene_to_file(MAP_SCENE_PATH)


func _on_host_pressed() -> void:
	status_label.text = "INITIALIZING LAN SERVER..."
	status_label.modulate = Color(0.2, 0.85, 1.0)
	var net := _get_net_mgr()
	if net and net.has_method("host_game"):
		var err: Error = net.host_game(name_input.text, 7777)
		if err == OK:
			status_label.text = "HOST CREATED! LOADING HAVEN FALL..."
			get_tree().change_scene_to_file(MAP_SCENE_PATH)
		else:
			status_label.text = "ERROR HOSTING: %s" % error_string(err)
			status_label.modulate = Color(1.0, 0.3, 0.3)
	else:
		get_tree().change_scene_to_file(MAP_SCENE_PATH)


func _on_join_pressed() -> void:
	var target_ip := ip_input.text.strip_edges()
	if target_ip.is_empty():
		target_ip = "127.0.0.1"

	status_label.text = "CONNECTING TO %s:7777..." % target_ip
	status_label.modulate = Color(1.0, 0.85, 0.3)
	join_btn.disabled = true

	var net := _get_net_mgr()
	if net and net.has_method("join_game"):
		var err: Error = net.join_game(target_ip, name_input.text, 7777)
		if err != OK:
			status_label.text = "FAILED TO CONNECT: %s" % error_string(err)
			status_label.modulate = Color(1.0, 0.3, 0.3)
			join_btn.disabled = false
	else:
		status_label.text = "NETWORK MANAGER NOT AVAILABLE"
		join_btn.disabled = false


func _on_server_created() -> void:
	pass


func _on_server_joined() -> void:
	status_label.text = "CONNECTED! DEPLOYING INTO MATCH..."
	status_label.modulate = Color(0.2, 1.0, 0.5)
	get_tree().change_scene_to_file(MAP_SCENE_PATH)


func _on_connection_failed() -> void:
	status_label.text = "CONNECTION FAILED / SERVER UNREACHABLE"
	status_label.modulate = Color(1.0, 0.3, 0.3)
	join_btn.disabled = false
