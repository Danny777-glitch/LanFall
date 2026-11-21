# ============================================================================
# LobbyMenu — AAA 3D Interactive Tactical Lobby (BGMI / PUBG Style)
# ============================================================================
# Features full 3D character preview, realistic two-handed weapon carry,
# tabbed Dress & Gear closet (Suits, Visor glow, Weapons, Skins),
# drag-to-rotate operative, profile stats, and LAN matchmaking.
# ============================================================================
extends Node3D

const MAP_SCENE_PATH = "res://scenes/maps/warehouse/warehouse_map.tscn"

# 3D Node References
@onready var character_model: Node3D = $CharacterShowcase/CharacterModel
@onready var camera_3d: Camera3D = $Camera3D

# UI Node References
@onready var player_name_label: Label = $CanvasLayer/TopLeft/ProfileCard/VBox/NameHBox/NameLabel
@onready var player_level_label: Label = $CanvasLayer/TopLeft/ProfileCard/VBox/LevelLabel
@onready var gold_label: Label = $CanvasLayer/TopRight/HBox/GoldBadge/Label
@onready var rp_label: Label = $CanvasLayer/TopRight/HBox/RPBadge/Label
@onready var start_btn: Button = $CanvasLayer/BottomLeft/StartBtn
@onready var mode_label: Label = $CanvasLayer/BottomLeft/ModeCard/ModeLabel
@onready var customize_btn: Button = $CanvasLayer/BottomBar/NavHBox/CustomizeBtn
@onready var weapons_btn: Button = $CanvasLayer/BottomBar/NavHBox/WeaponsBtn
@onready var lan_btn: Button = $CanvasLayer/BottomBar/NavHBox/LanBtn
@onready var solo_btn: Button = $CanvasLayer/BottomBar/NavHBox/SoloBtn

# Drawer & Closet UI
@onready var custom_drawer: Panel = $CanvasLayer/CustomizationDrawer
@onready var close_drawer_btn: Button = $CanvasLayer/CustomizationDrawer/VBox/Header/CloseBtn
@onready var drawer_title_lbl: Label = $CanvasLayer/CustomizationDrawer/VBox/Header/Title
@onready var tab_suits_btn: Button = $CanvasLayer/CustomizationDrawer/VBox/CategoryTabBar/TabSuits
@onready var tab_visors_btn: Button = $CanvasLayer/CustomizationDrawer/VBox/CategoryTabBar/TabVisors
@onready var tab_weapons_btn: Button = $CanvasLayer/CustomizationDrawer/VBox/CategoryTabBar/TabWeapons
@onready var tab_skins_btn: Button = $CanvasLayer/CustomizationDrawer/VBox/CategoryTabBar/TabSkins
@onready var items_grid: GridContainer = $CanvasLayer/CustomizationDrawer/VBox/Scroll/ItemsGrid

# LAN Dialog
@onready var lan_dialog: Panel = $CanvasLayer/LanDialog
@onready var host_btn: Button = $CanvasLayer/LanDialog/VBox/BtnHBox/HostBtn
@onready var join_btn: Button = $CanvasLayer/LanDialog/VBox/BtnHBox/JoinBtn
@onready var close_lan_btn: Button = $CanvasLayer/LanDialog/VBox/CloseLanBtn
@onready var ip_input: LineEdit = $CanvasLayer/LanDialog/VBox/JoinHBox/IPInput
@onready var status_label: Label = $CanvasLayer/LanDialog/VBox/StatusLabel
@onready var lan_ip_label: Label = $CanvasLayer/LanDialog/VBox/LanIPLabel

# Edit Name Dialog
@onready var name_dialog: Panel = $CanvasLayer/NameDialog
@onready var edit_name_input: LineEdit = $CanvasLayer/NameDialog/VBox/NameInput
@onready var save_name_btn: Button = $CanvasLayer/NameDialog/VBox/SaveBtn
@onready var cancel_name_btn: Button = $CanvasLayer/NameDialog/VBox/CancelBtn
@onready var edit_name_btn: Button = $CanvasLayer/TopLeft/ProfileCard/VBox/EditNameBtn

# Drag to Rotate State
var is_dragging_char: bool = false
var drag_start_x: float = 0.0

# Current Inventory Category: "SUITS", "VISORS", "WEAPONS", "SKINS"
var current_inventory_tab: String = "SUITS"


func _get_profile() -> Node:
	return get_node_or_null("/root/ProfileManager")


func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

	_update_profile_ui()
	_setup_network_ui()
	_setup_inventory_tabs()
	if mode_label:
		mode_label.text = "MAP: WAREHOUSE // 4v4 TDM"

	# Connect Primary Buttons
	start_btn.pressed.connect(_on_start_pressed)
	customize_btn.pressed.connect(_toggle_custom_drawer)
	weapons_btn.pressed.connect(_on_weapons_quick_toggle)
	lan_btn.pressed.connect(_toggle_lan_dialog)
	solo_btn.pressed.connect(_on_solo_warmup_pressed)
	close_drawer_btn.pressed.connect(func(): custom_drawer.visible = false)

	# Name Edit
	edit_name_btn.pressed.connect(_open_name_dialog)
	save_name_btn.pressed.connect(_save_new_name)
	cancel_name_btn.pressed.connect(func(): name_dialog.visible = false)

	# Initial Drawer & Dialog states
	custom_drawer.visible = false
	lan_dialog.visible = false
	name_dialog.visible = false

	# Listen to Profile Updates
	var prof = _get_profile()
	if prof and prof.has_signal("profile_updated"):
		prof.profile_updated.connect(_on_profile_updated)

	# Show default category tab
	_switch_inventory_tab("SUITS")

	# Refresh 3D model
	if character_model and character_model.has_method("apply_from_profile"):
		character_model.apply_from_profile()


func _unhandled_input(event: InputEvent) -> void:
	# Mouse Drag to Rotate 3D Operative
	if event is InputEventMouseButton:
		var mouse_btn := event as InputEventMouseButton
		if mouse_btn.button_index == MOUSE_BUTTON_LEFT:
			if mouse_btn.is_pressed():
				# Only drag if not clicking over active panels
				if not custom_drawer.visible and not lan_dialog.visible and not name_dialog.visible:
					is_dragging_char = true
					drag_start_x = mouse_btn.position.x
			else:
				is_dragging_char = false

	elif event is InputEventMouseMotion and is_dragging_char:
		var motion := event as InputEventMouseMotion
		var delta_x: float = motion.relative.x
		if character_model and character_model.has_method("rotate_model"):
			character_model.rotate_model(delta_x * 0.7)


func _update_profile_ui() -> void:
	var prof = _get_profile()
	if not prof:
		return

	if player_name_label:
		player_name_label.text = String(prof.player_name)
	if player_level_label:
		player_level_label.text = "Lv. %d // %s" % [int(prof.player_level), String(prof.player_title)]
	if gold_label:
		gold_label.text = str(prof.gold_coins)
	if rp_label:
		rp_label.text = "RP %d" % int(prof.rp_points)

	var wp_idx: int = clamp(int(prof.current_weapon_index), 0, prof.WEAPONS_CATALOG.size() - 1)
	var skin_idx: int = clamp(int(prof.current_weapon_skin_index), 0, prof.WEAPON_SKINS.size() - 1)
	var wp_info = prof.WEAPONS_CATALOG[wp_idx]
	var skin_info = prof.WEAPON_SKINS[skin_idx]
	if mode_label:
		mode_label.text = "HAVEN FALL // %s (%s)" % [wp_info["name"], skin_info["name"]]


func _on_profile_updated() -> void:
	_update_profile_ui()
	if character_model and character_model.has_method("apply_from_profile"):
		character_model.apply_from_profile()
	# Refresh cards in active tab
	_switch_inventory_tab(current_inventory_tab)


func _setup_inventory_tabs() -> void:
	tab_suits_btn.pressed.connect(func(): _switch_inventory_tab("SUITS"))
	tab_visors_btn.pressed.connect(func(): _switch_inventory_tab("VISORS"))
	tab_weapons_btn.pressed.connect(func(): _switch_inventory_tab("WEAPONS"))
	tab_skins_btn.pressed.connect(func(): _switch_inventory_tab("SKINS"))


func _switch_inventory_tab(tab_name: String) -> void:
	current_inventory_tab = tab_name
	var prof = _get_profile()
	if not prof or not items_grid:
		return

	# Highlight active category tab button
	tab_suits_btn.modulate = Color(1.2, 1.2, 0.4) if tab_name == "SUITS" else Color.WHITE
	tab_visors_btn.modulate = Color(1.2, 1.2, 0.4) if tab_name == "VISORS" else Color.WHITE
	tab_weapons_btn.modulate = Color(1.2, 1.2, 0.4) if tab_name == "WEAPONS" else Color.WHITE
	tab_skins_btn.modulate = Color(1.2, 1.2, 0.4) if tab_name == "SKINS" else Color.WHITE

	# Clear previous cards
	for child in items_grid.get_children():
		child.queue_free()

	match tab_name:
		"SUITS":
			drawer_title_lbl.text = "🥋 OPERATIVE COMBAT OUTFITS"
			for i in range(prof.OPERATIVE_SUITS.size()):
				var suit: Dictionary = prof.OPERATIVE_SUITS[i]
				var is_active: bool = (i == int(prof.current_suit_index))
				var card := _create_gear_card(
					suit.get("icon", "🥋"),
					suit.get("name", "SUIT"),
					suit.get("rarity", "EPIC"),
					is_active,
					suit.get("suit_color", Color.CYAN)
				)
				card.pressed.connect(func():
					prof.set_suit(i)
				)
				items_grid.add_child(card)

		"VISORS":
			drawer_title_lbl.text = "⚡ VISOR & RADIANITE GLOW"
			for i in range(prof.VISOR_GLOW_COLORS.size()):
				var v: Dictionary = prof.VISOR_GLOW_COLORS[i]
				var is_active: bool = (i == int(prof.current_visor_index))
				var card := _create_gear_card(
					v.get("icon", "⚡"),
					v.get("name", "VISOR"),
					"GLOW",
					is_active,
					v.get("color", Color.CYAN)
				)
				card.pressed.connect(func():
					prof.set_visor(i)
				)
				items_grid.add_child(card)

		"WEAPONS":
			drawer_title_lbl.text = "🔫 DISPLAY WEAPON LOADOUT"
			for i in range(prof.WEAPONS_CATALOG.size()):
				var wp: Dictionary = prof.WEAPONS_CATALOG[i]
				var is_active: bool = (i == int(prof.current_weapon_index))
				var card := _create_gear_card(
					wp.get("icon", "🔫"),
					wp.get("name", "WEAPON"),
					wp.get("slot", "PRIMARY"),
					is_active,
					Color(0.2, 0.85, 1.0)
				)
				card.pressed.connect(func():
					prof.set_weapon(i)
				)
				items_grid.add_child(card)

		"SKINS":
			drawer_title_lbl.text = "🎨 WEAPON SKINS LOCKER"
			for i in range(prof.WEAPON_SKINS.size()):
				var sk: Dictionary = prof.WEAPON_SKINS[i]
				var is_active: bool = (i == int(prof.current_weapon_skin_index))
				var card := _create_gear_card(
					sk.get("icon", "✨"),
					sk.get("name", "SKIN"),
					sk.get("rarity", "LEGENDARY"),
					is_active,
					sk.get("glow_color", Color.GOLD)
				)
				card.pressed.connect(func():
					prof.set_weapon_skin(i)
				)
				items_grid.add_child(card)


func _create_gear_card(icon: String, title: String, rarity: String, is_equipped: bool, accent_color: Color) -> Button:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(185, 96)
	btn.alignment = HORIZONTAL_ALIGNMENT_CENTER

	var card_panel := StyleBoxFlat.new()
	if is_equipped:
		card_panel.bg_color = Color(0.18, 0.16, 0.08, 0.95)
		card_panel.border_color = Color(1.0, 0.82, 0.15, 1.0) # Glowing Gold border
		card_panel.set_border_width_all(2)
		card_panel.shadow_color = Color(1.0, 0.75, 0.1, 0.5)
		card_panel.shadow_size = 6
	else:
		card_panel.bg_color = Color(0.09, 0.11, 0.16, 0.88)
		card_panel.border_color = accent_color * 0.7
		card_panel.set_border_width_all(1)

	card_panel.set_corner_radius_all(8)
	btn.add_theme_stylebox_override("normal", card_panel)
	btn.add_theme_stylebox_override("hover", card_panel)
	btn.add_theme_stylebox_override("pressed", card_panel)

	var status_text := " [✓ EQUIPPED]" if is_equipped else ""
	btn.text = "%s\n%s\n[%s]%s" % [icon, title, rarity, status_text]
	btn.add_theme_font_size_override("font_size", 11)

	if is_equipped:
		btn.add_theme_color_override("font_color", Color(1.0, 0.9, 0.4))
	else:
		btn.add_theme_color_override("font_color", Color(0.85, 0.9, 0.95))

	return btn


func _toggle_custom_drawer() -> void:
	custom_drawer.visible = not custom_drawer.visible
	if custom_drawer.visible:
		lan_dialog.visible = false
		name_dialog.visible = false
		_switch_inventory_tab(current_inventory_tab)


func _on_weapons_quick_toggle() -> void:
	var prof = _get_profile()
	if not prof:
		return
	var next_wp: int = (int(prof.current_weapon_index) + 1) % prof.WEAPONS_CATALOG.size()
	prof.set_weapon(next_wp)


func _toggle_lan_dialog() -> void:
	lan_dialog.visible = not lan_dialog.visible
	if lan_dialog.visible:
		custom_drawer.visible = false
		name_dialog.visible = false


func _open_name_dialog() -> void:
	var prof = _get_profile()
	if prof and edit_name_input:
		edit_name_input.text = String(prof.player_name)
	if name_dialog:
		name_dialog.visible = true
	if edit_name_input:
		edit_name_input.grab_focus()


func _save_new_name() -> void:
	var prof = _get_profile()
	if prof and edit_name_input and not edit_name_input.text.strip_edges().is_empty():
		prof.set_player_name(edit_name_input.text.strip_edges())
	if name_dialog:
		name_dialog.visible = false


func _setup_network_ui() -> void:
	var net := _get_net_mgr()
	var local_ip: String = net.get_local_ip() if net and net.has_method("get_local_ip") else "127.0.0.1"
	lan_ip_label.text = "YOUR LAN IP: %s (PORT: 7777)" % local_ip
	ip_input.text = "127.0.0.1"
	status_label.text = "HOST OR JOIN A LOCAL LAN ARENA"

	host_btn.pressed.connect(_on_host_pressed)
	join_btn.pressed.connect(_on_join_pressed)
	close_lan_btn.pressed.connect(func(): lan_dialog.visible = false)


func _on_start_pressed() -> void:
	var prof = _get_profile()
	var net = _get_net_mgr()
	var p_name: String = String(prof.player_name) if prof else "SMxTHUG"

	if net and net.has_method("start_singleplayer"):
		net.start_singleplayer(p_name)

	get_tree().change_scene_to_file(MAP_SCENE_PATH)


func _on_solo_warmup_pressed() -> void:
	_on_start_pressed()


func _on_host_pressed() -> void:
	var prof = _get_profile()
	var net = _get_net_mgr()
	var p_name: String = String(prof.player_name) if prof else "HOST_OP"

	status_label.text = "INITIALIZING LAN MATCH..."
	status_label.modulate = Color(0.2, 0.85, 1.0)

	if net and net.has_method("host_game"):
		var err: Error = net.host_game(p_name, 7777)
		if err == OK:
			status_label.text = "HOST READY! LAUNCHING MAP..."
			get_tree().change_scene_to_file(MAP_SCENE_PATH)
		else:
			status_label.text = "ERROR HOSTING: %s" % error_string(err)
			status_label.modulate = Color(1.0, 0.3, 0.3)
	else:
		get_tree().change_scene_to_file(MAP_SCENE_PATH)


func _on_join_pressed() -> void:
	var target_ip: String = ip_input.text.strip_edges()
	if target_ip.is_empty():
		target_ip = "127.0.0.1"

	var prof = _get_profile()
	var net = _get_net_mgr()
	var p_name: String = String(prof.player_name) if prof else "CLIENT_OP"

	status_label.text = "CONNECTING TO %s:7777..." % target_ip
	status_label.modulate = Color(1.0, 0.85, 0.3)
	join_btn.disabled = true

	if net and net.has_method("join_game"):
		var err: Error = net.join_game(target_ip, p_name, 7777)
		if err != OK:
			status_label.text = "CONNECTION FAILED: %s" % error_string(err)
			status_label.modulate = Color(1.0, 0.3, 0.3)
			join_btn.disabled = false
		else:
			net.server_joined.connect(func():
				get_tree().change_scene_to_file(MAP_SCENE_PATH)
			)
	else:
		get_tree().change_scene_to_file(MAP_SCENE_PATH)
