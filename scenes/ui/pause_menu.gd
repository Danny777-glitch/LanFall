# ============================================================================
# PauseMenu - Settings & In-Game Options
# ============================================================================
extends CanvasLayer

@onready var panel: Control = $Panel
@onready var sens_slider: HSlider = $Panel/VBox/SensBox/SensSlider
@onready var sens_val_label: Label = $Panel/VBox/SensBox/HBox/SensVal
@onready var vol_slider: HSlider = $Panel/VBox/VolBox/VolSlider
@onready var vol_val_label: Label = $Panel/VBox/VolBox/HBox/VolVal

@onready var vsync_btn: Button = $Panel/VBox/GraphicsBox/VSyncBtn
@onready var fps_cap_btn: Button = $Panel/VBox/GraphicsBox/FpsCapBtn
@onready var preset_btn: Button = $Panel/VBox/GraphicsBox/PresetBtn
@onready var scale_slider: HSlider = $Panel/VBox/GraphicsBox/ScaleBox/ScaleSlider
@onready var scale_val_label: Label = $Panel/VBox/GraphicsBox/ScaleBox/HBox/ScaleVal

@onready var resume_btn: Button = $Panel/VBox/ResumeBtn
@onready var restart_btn: Button = $Panel/VBox/RestartBtn
@onready var menu_btn: Button = $Panel/VBox/MenuBtn
@onready var quit_btn: Button = $Panel/VBox/QuitBtn

const FPS_OPTIONS: Array[int] = [60, 90, 120, 144, 165, 240, 0]
const PRESET_OPTIONS: Array[String] = ["POWER_SAVER", "LOW", "MEDIUM", "HIGH", "ULTRA"]


func _get_net_mgr() -> Node:
	return get_node_or_null("/root/NetworkManager")


func _get_perf() -> Node:
	return get_node_or_null("/root/PerfSettings")


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	panel.visible = false

	resume_btn.pressed.connect(_on_resume_pressed)
	restart_btn.pressed.connect(_on_restart_pressed)
	menu_btn.pressed.connect(_on_menu_pressed)
	quit_btn.pressed.connect(_on_quit_pressed)

	if vsync_btn:
		vsync_btn.pressed.connect(_on_vsync_toggle)
	if fps_cap_btn:
		fps_cap_btn.pressed.connect(_on_fps_cap_cycle)
	if preset_btn:
		preset_btn.pressed.connect(_on_preset_cycle)
	if scale_slider:
		scale_slider.value_changed.connect(_on_scale_changed)

	sens_slider.value_changed.connect(_on_sens_changed)
	vol_slider.value_changed.connect(_on_vol_changed)

	sens_slider.value = 0.002
	vol_slider.value = 80.0

	_refresh_ui_from_perf()


func _refresh_ui_from_perf() -> void:
	var perf := _get_perf()
	if not perf:
		return
	if vsync_btn:
		var vsync_on: bool = (perf.vsync_mode != DisplayServer.VSYNC_DISABLED)
		vsync_btn.text = "⚡ VSYNC: %s" % ("ENABLED (TEAR-FREE)" if vsync_on else "DISABLED (FAST)")
		vsync_btn.add_theme_color_override("font_color", Color(0.2, 1.0, 0.5, 1.0) if vsync_on else Color(0.9, 0.6, 0.2, 1.0))
	if fps_cap_btn:
		fps_cap_btn.text = "🎯 MAX FPS: %s" % ("UNLIMITED" if perf.max_fps == 0 else ("%d FPS" % perf.max_fps))
	if preset_btn:
		preset_btn.text = "✨ PRESET: %s" % perf.quality_preset
	if scale_slider:
		scale_slider.value = perf.render_scale * 100.0
		if scale_val_label:
			scale_val_label.text = "%d%%" % int(perf.render_scale * 100.0)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause_game"):
		if panel.visible:
			resume()
		else:
			pause()


func pause() -> void:
	panel.visible = true
	var perf := _get_perf()
	if perf:
		perf.set_in_menu(true)
	var net := _get_net_mgr()
	# In multiplayer, do NOT pause tree so other players keep moving smoothly
	if not (net and net.get("is_multiplayer_active")):
		get_tree().paused = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_refresh_ui_from_perf()


func resume() -> void:
	panel.visible = false
	get_tree().paused = false
	var perf := _get_perf()
	if perf:
		perf.set_in_menu(false)
		perf.save_settings()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


func _on_vsync_toggle() -> void:
	var perf := _get_perf()
	if perf:
		var new_mode: int = DisplayServer.VSYNC_DISABLED if perf.vsync_mode == DisplayServer.VSYNC_ENABLED else DisplayServer.VSYNC_ENABLED
		perf.set_vsync(new_mode)
		_refresh_ui_from_perf()


func _on_fps_cap_cycle() -> void:
	var perf := _get_perf()
	if perf:
		var cur_fps: int = perf.max_fps
		var idx: int = FPS_OPTIONS.find(cur_fps)
		if idx == -1:
			idx = 0
		else:
			idx = (idx + 1) % FPS_OPTIONS.size()
		perf.set_max_fps(FPS_OPTIONS[idx])
		_refresh_ui_from_perf()


func _on_preset_cycle() -> void:
	var perf := _get_perf()
	if perf:
		var cur_preset: String = perf.quality_preset
		var idx: int = PRESET_OPTIONS.find(cur_preset)
		if idx == -1:
			idx = 0
		else:
			idx = (idx + 1) % PRESET_OPTIONS.size()
		perf.set_quality_preset(PRESET_OPTIONS[idx])
		_refresh_ui_from_perf()


func _on_scale_changed(val: float) -> void:
	if scale_val_label:
		scale_val_label.text = "%d%%" % int(val)
	var perf := _get_perf()
	if perf:
		perf.set_render_scale(val / 100.0)


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
	var perf := _get_perf()
	if perf:
		perf.set_in_menu(false)
	get_tree().reload_current_scene()


func _on_menu_pressed() -> void:
	get_tree().paused = false
	var perf := _get_perf()
	if perf:
		perf.set_in_menu(true)
		perf.save_settings()
	var net := _get_net_mgr()
	if net and net.get("is_multiplayer_active"):
		net.disconnect_game()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().change_scene_to_file("res://scenes/ui/lobby_menu.tscn")


func _on_quit_pressed() -> void:
	var perf := _get_perf()
	if perf:
		perf.save_settings()
	get_tree().quit()
