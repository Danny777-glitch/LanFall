# ============================================================================
# PauseMenu - Settings & In-Game Options
# ============================================================================
extends CanvasLayer

@onready var panel: Control = $Panel
@onready var sens_slider: HSlider = $Panel/VBox/SensBox/SensSlider
@onready var sens_val_label: Label = $Panel/VBox/SensBox/HBox/SensVal
@onready var vol_slider: HSlider = $Panel/VBox/VolBox/VolSlider
@onready var vol_val_label: Label = $Panel/VBox/VolBox/HBox/VolVal
@onready var resume_btn: Button = $Panel/VBox/ResumeBtn
@onready var restart_btn: Button = $Panel/VBox/RestartBtn
@onready var menu_btn: Button = $Panel/VBox/MenuBtn
@onready var quit_btn: Button = $Panel/VBox/QuitBtn
@onready var perf_btn: Button = $Panel/VBox/PerfBtn

var is_perf_mode: bool = true


func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	panel.visible = false

	resume_btn.pressed.connect(_on_resume_pressed)
	restart_btn.pressed.connect(_on_restart_pressed)
	menu_btn.pressed.connect(_on_menu_pressed)
	quit_btn.pressed.connect(_on_quit_pressed)
	if perf_btn:
		perf_btn.pressed.connect(_on_perf_toggle)

	sens_slider.value_changed.connect(_on_sens_changed)
	vol_slider.value_changed.connect(_on_vol_changed)

	sens_slider.value = 0.002
	vol_slider.value = 80.0
	_apply_graphics_preset(true)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause_game"):
		if panel.visible:
			resume()
		else:
			pause()


func pause() -> void:
	panel.visible = true
	var net := _get_net_mgr()
	# In multiplayer, do NOT pause tree so other players keep moving smoothly
	if not (net and net.get("is_multiplayer_active")):
		get_tree().paused = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE


func resume() -> void:
	panel.visible = false
	get_tree().paused = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


func _on_sens_changed(val: float) -> void:
	sens_val_label.text = "%.4f" % val
	for p in get_tree().get_nodes_in_group("player"):
		if "mouse_sensitivity" in p:
			p.mouse_sensitivity = val


func _on_vol_changed(val: float) -> void:
	vol_val_label.text = "%d%%" % int(val)
	var db := linear_to_db(val / 100.0) if val > 0 else -80.0
	AudioServer.set_bus_volume_db(0, db)


func _on_resume_pressed() -> void:
	resume()


func _on_restart_pressed() -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()


func _on_menu_pressed() -> void:
	get_tree().paused = false
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		net.disconnect_game()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().change_scene_to_file("res://scenes/ui/lobby_menu.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()


func _on_perf_toggle() -> void:
	is_perf_mode = not is_perf_mode
	_apply_graphics_preset(is_perf_mode)


func _apply_graphics_preset(perf: bool) -> void:
	if not perf_btn:
		return
	if perf:
		perf_btn.text = "⚡ GRAPHICS: PERFORMANCE (HIGH FPS)"
		perf_btn.add_theme_color_override("font_color", Color(0.2, 1.0, 0.5, 1.0))
	else:
		perf_btn.text = "✨ GRAPHICS: HIGH VISUALS (SSAO ON)"
		perf_btn.add_theme_color_override("font_color", Color(0.3, 0.85, 1.0, 1.0))

	var current_scene = get_tree().current_scene
	if current_scene and current_scene.has_method("apply_quality_preset"):
		current_scene.apply_quality_preset("LOW" if perf else "HIGH")
	else:
		var env_node = get_tree().root.find_child("WorldEnvironment", true, false)
		if env_node and env_node.environment:
			env_node.environment.ssao_enabled = not perf
