# ============================================================================
# HUD - Heads-Up Display with Combat, Scope, Kill Feed & Scoreboard
# ============================================================================
extends CanvasLayer

@onready var health_label: Label = $UI/HealthLabel
@onready var score_label: Label = $UI/ScoreLabel
@onready var ability_label: Label = $UI/AbilityLabel
@onready var weapon_label: Label = $UI/WeaponLabel
@onready var ammo_label: Label = $UI/AmmoLabel
@onready var crosshair: Control = $UI/Crosshair
@onready var scope_overlay: Control = $UI/ScopeOverlay
@onready var damage_flash: ColorRect = $UI/DamageFlash
@onready var smoke_blind: ColorRect = $UI/SmokeBlind
@onready var kill_banner: Label = $UI/KillBanner
@onready var scoreboard: Panel = $UI/Scoreboard
@onready var scoreboard_list: VBoxContainer = $UI/Scoreboard/VBox/PlayerList
@onready var kill_feed_container: VBoxContainer = $UI/KillFeed
@onready var hit_sound: AudioStreamPlayer = $HitSound
@onready var kill_sound: AudioStreamPlayer = $KillSound

var kill_count: int = 0
var damage_tween: Tween = null
var banner_tween: Tween = null
var smoke_tween: Tween = null
var fps_label: Label = null
var _fps_timer: float = 0.0


func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _ready() -> void:
	add_to_group("hud")
	_setup_fps_counter()
	update_health(100)
	update_weapon("VANGUARD AR [1]")
	update_ammo(30, 90)
	update_score(0)
	set_scope_overlay(false)
	if scoreboard:
		scoreboard.visible = false

	var net := _get_net_mgr()
	if net and net.has_signal("player_list_updated"):
		net.player_list_updated.connect(_update_scoreboard)


func _setup_fps_counter() -> void:
	fps_label = Label.new()
	fps_label.name = "FPSCounter"
	fps_label.anchors_preset = Control.PRESET_TOP_RIGHT
	fps_label.anchor_left = 1.0
	fps_label.anchor_right = 1.0
	fps_label.offset_left = -175.0
	fps_label.offset_top = 16.0
	fps_label.offset_right = -20.0
	fps_label.offset_bottom = 44.0
	fps_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	fps_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	fps_label.add_theme_font_size_override("font_size", 15)
	fps_label.add_theme_color_override("font_color", Color(0.2, 1.0, 0.5, 0.95))
	var ui_node = get_node_or_null("UI")
	if ui_node:
		ui_node.add_child(fps_label)
	else:
		add_child(fps_label)


var _frame_count: int = 0
var _accum_time: float = 0.0

func _process(delta: float) -> void:
	_frame_count += 1
	_accum_time += delta
	if _accum_time >= 0.25:
		var current_fps := int(round(float(_frame_count) / _accum_time))
		var ms := (_accum_time / maxf(float(_frame_count), 1.0)) * 1000.0
		_frame_count = 0
		_accum_time = 0.0
		if fps_label and is_instance_valid(fps_label):
			fps_label.text = "FPS: %d (%.1f ms)" % [current_fps, ms]
			if current_fps >= 90:
				fps_label.add_theme_color_override("font_color", Color(0.2, 1.0, 0.5, 0.95))
			elif current_fps >= 55:
				fps_label.add_theme_color_override("font_color", Color(1.0, 0.85, 0.2, 0.95))
			else:
				fps_label.add_theme_color_override("font_color", Color(1.0, 0.25, 0.25, 0.95))


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action("scoreboard"):
		if scoreboard:
			scoreboard.visible = event.is_pressed()
			if scoreboard.visible:
				_update_scoreboard()


func update_health(value: int, max_value: int = 100) -> void:
	health_label.text = "HP: %d / %d" % [value, max_value]
	var ratio := float(value) / float(max_value)
	if ratio > 0.6:
		health_label.add_theme_color_override("font_color", Color(0.4, 1.0, 0.4, 0.95))
	elif ratio > 0.3:
		health_label.add_theme_color_override("font_color", Color(1.0, 0.8, 0.2, 0.95))
	else:
		health_label.add_theme_color_override("font_color", Color(1.0, 0.25, 0.25, 0.95))


func show_damage_flash() -> void:
	if not damage_flash:
		return
	if damage_tween:
		damage_tween.kill()

	damage_flash.color = Color(0.85, 0.12, 0.12, 0.35)
	damage_tween = create_tween()
	damage_tween.tween_property(damage_flash, "color:a", 0.0, 0.35)


func set_scope_overlay(is_scoped: bool) -> void:
	if scope_overlay:
		scope_overlay.visible = is_scoped
	if crosshair:
		crosshair.visible = not is_scoped


func set_smoke_blind(inside: bool) -> void:
	if not smoke_blind:
		return
	if smoke_tween:
		smoke_tween.kill()
	smoke_tween = create_tween()
	var target_alpha := 0.88 if inside else 0.0
	smoke_tween.tween_property(smoke_blind, "color:a", target_alpha, 0.25)


func update_ability(text: String, is_ready: bool = true) -> void:
	if ability_label:
		ability_label.text = text
		if is_ready:
			ability_label.add_theme_color_override("font_color", Color(0.2, 0.85, 1.0, 0.95))
		else:
			ability_label.add_theme_color_override("font_color", Color(0.65, 0.65, 0.7, 0.75))


func add_kill(victim_name: String = "BOT") -> void:
	kill_count += 1
	update_score(kill_count)
	show_kill_banner(victim_name)
	notify_kill("YOU", victim_name)


func notify_kill(killer: String, victim: String) -> void:
	var net := _get_net_mgr()
	var local_name: String = net.get("local_player_name") if net else "OPERATIVE"

	# Add to top-right kill feed
	if kill_feed_container:
		var item := Label.new()
		item.text = "%s 💥 %s" % [killer, victim]
		item.add_theme_font_size_override("font_size", 14)
		if killer == local_name or killer == "YOU":
			item.add_theme_color_override("font_color", Color(0.3, 1.0, 0.5))
		else:
			item.add_theme_color_override("font_color", Color(1.0, 0.35, 0.3))
		kill_feed_container.add_child(item)

		var tween := item.create_tween()
		tween.tween_interval(3.5)
		tween.tween_property(item, "modulate:a", 0.0, 0.5)
		tween.tween_callback(item.queue_free)

	# If local player got the kill, show big banner
	if killer == local_name:
		show_kill_banner(victim)


func update_score(count: int) -> void:
	if score_label:
		var net := _get_net_mgr()
		if net and net.get("is_multiplayer_active"):
			var p_count: int = net.get("players").size() if net.get("players") else 1
			score_label.text = "LAN MATCH // %d OPERATIVES" % p_count
		else:
			score_label.text = "TARGETS ELIMINATED: %d" % count


func show_kill_banner(victim_name: String) -> void:
	if not kill_banner:
		return
	if kill_sound:
		kill_sound.pitch_scale = randf_range(1.28, 1.38)
		kill_sound.play()

	if banner_tween:
		banner_tween.kill()

	kill_banner.text = "💀 ELIMINATED %s!" % victim_name
	kill_banner.visible = true
	kill_banner.scale = Vector2(1.2, 1.2)
	kill_banner.modulate.a = 1.0

	banner_tween = create_tween().set_parallel(true)
	banner_tween.tween_property(kill_banner, "scale", Vector2.ONE, 0.15).set_trans(Tween.TRANS_BACK)
	banner_tween.chain().tween_interval(1.2)
	banner_tween.chain().tween_property(kill_banner, "modulate:a", 0.0, 0.3)
	await banner_tween.finished
	if is_instance_valid(kill_banner):
		kill_banner.visible = false


func update_weapon(weapon_name: String) -> void:
	if weapon_label:
		weapon_label.text = weapon_name


func update_ammo(current: int, reserve: int) -> void:
	ammo_label.text = "%d / %d" % [current, reserve]


func update_ammo_text(text: String) -> void:
	if ammo_label:
		ammo_label.text = text


func show_hitmarker() -> void:
	if crosshair and crosshair.has_method("show_hitmarker"):
		crosshair.show_hitmarker()
	if hit_sound:
		hit_sound.pitch_scale = randf_range(0.97, 1.03)
		hit_sound.play()


func _update_scoreboard() -> void:
	if not scoreboard_list:
		return

	for child in scoreboard_list.get_children():
		child.queue_free()

	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active") and net.get("players"):
		var p_dict: Dictionary = net.get("players")
		for pid in p_dict.keys():
			var p_data: Dictionary = p_dict[pid]
			var row := HBoxContainer.new()
			var p_name_lbl := Label.new()
			p_name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			p_name_lbl.text = p_data.get("name", "OPERATIVE")
			if pid == multiplayer.get_unique_id():
				p_name_lbl.text += " (YOU)"
				p_name_lbl.add_theme_color_override("font_color", Color(0.2, 1.0, 0.5))
			else:
				p_name_lbl.add_theme_color_override("font_color", Color(0.85, 0.9, 1.0))

			var kills_lbl := Label.new()
			kills_lbl.custom_minimum_size = Vector2(80, 0)
			kills_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			kills_lbl.text = str(p_data.get("kills", 0))

			var deaths_lbl := Label.new()
			deaths_lbl.custom_minimum_size = Vector2(80, 0)
			deaths_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			deaths_lbl.text = str(p_data.get("deaths", 0))

			var ping_lbl := Label.new()
			ping_lbl.custom_minimum_size = Vector2(80, 0)
			ping_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			ping_lbl.text = "LAN"
			ping_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 1.0))

			row.add_child(p_name_lbl)
			row.add_child(kills_lbl)
			row.add_child(deaths_lbl)
			row.add_child(ping_lbl)
			scoreboard_list.add_child(row)
	else:
		var row := HBoxContainer.new()
		var p_name_lbl := Label.new()
		p_name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var local_name: String = net.get("local_player_name") if net else "OPERATIVE"
		p_name_lbl.text = "%s (YOU)" % local_name
		p_name_lbl.add_theme_color_override("font_color", Color(0.2, 1.0, 0.5))

		var kills_lbl := Label.new()
		kills_lbl.custom_minimum_size = Vector2(80, 0)
		kills_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		kills_lbl.text = str(kill_count)

		var deaths_lbl := Label.new()
		deaths_lbl.custom_minimum_size = Vector2(80, 0)
		deaths_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		deaths_lbl.text = "0"

		var ping_lbl := Label.new()
		ping_lbl.custom_minimum_size = Vector2(80, 0)
		ping_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		ping_lbl.text = "SOLO"
		ping_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 1.0))

		row.add_child(p_name_lbl)
		row.add_child(kills_lbl)
		row.add_child(deaths_lbl)
		row.add_child(ping_lbl)
		scoreboard_list.add_child(row)
