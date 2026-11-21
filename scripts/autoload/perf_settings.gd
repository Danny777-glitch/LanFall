# ============================================================================
# PerfSettings - Frame Pacing, Power Efficiency & Visual Scalability Manager
# Autoload singleton handling display sync, FPS caps, resolution and quality
# ============================================================================
extends Node

const CONFIG_PATH: String = "user://graphics_settings.cfg"

# Available FPS caps
const FPS_CHOICES: Array[int] = [0, 60, 90, 120, 144, 165, 240]

# Core settings
var vsync_mode: int = DisplayServer.VSYNC_ENABLED
var max_fps: int = 144
var in_menu_fps: int = 60
var unfocused_fps: int = 30
var dynamic_resolution_enabled: bool = false
var render_scale: float = 1.0
var scaling_3d_mode: int = Viewport.SCALING_3D_MODE_BILINEAR
var quality_preset: String = "HIGH"
var auto_battery_saver: bool = true

# Live states
var is_on_battery: bool = false
var _is_window_focused: bool = true
var _is_in_menu: bool = false
var _configured_fps: int = 144

signal settings_changed
signal preset_changed(preset_name: String)


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_detect_monitor_defaults()
	load_settings()
	apply_all()
	_check_battery_state()


func _detect_monitor_defaults() -> void:
	var args := OS.get_cmdline_user_args()
	for a in args:
		if a.begins_with("--cap="):
			max_fps = int(a.trim_prefix("--cap="))
			_configured_fps = max_fps
			return
		elif a.begins_with("--preset="):
			quality_preset = a.trim_prefix("--preset=").to_upper()

	var all_args := OS.get_cmdline_args()
	for a in all_args:
		if a.begins_with("--cap="):
			max_fps = int(a.trim_prefix("--cap="))
			_configured_fps = max_fps
			return
		elif a.begins_with("--preset="):
			quality_preset = a.trim_prefix("--preset=").to_upper()

	var refresh: float = DisplayServer.screen_get_refresh_rate()
	if refresh > 0:
		var rounded: int = int(round(refresh))
		if rounded >= 240:
			max_fps = 240
		elif rounded >= 165:
			max_fps = 165
		elif rounded >= 144:
			max_fps = 144
		elif rounded >= 120:
			max_fps = 120
		elif rounded >= 90:
			max_fps = 90
		elif rounded >= 60:
			max_fps = 60
		else:
			max_fps = 60
	else:
		max_fps = 144
	_configured_fps = max_fps


func _notification(what: int) -> void:
	match what:
		NOTIFICATION_APPLICATION_FOCUS_OUT, NOTIFICATION_WM_WINDOW_FOCUS_OUT:
			_is_window_focused = false
			_update_effective_engine_pacing()
		NOTIFICATION_APPLICATION_FOCUS_IN, NOTIFICATION_WM_WINDOW_FOCUS_IN:
			_is_window_focused = true
			_update_effective_engine_pacing()


func set_in_menu(in_menu: bool) -> void:
	_is_in_menu = in_menu
	_update_effective_engine_pacing()


func _update_effective_engine_pacing() -> void:
	if not _is_window_focused:
		# When alt-tabbed or minimized: throttle to 30 FPS and sleep CPU
		Engine.max_fps = unfocused_fps
		OS.low_processor_usage_mode = true
	elif _is_in_menu:
		# In menus: cap at 60 FPS to prevent coil whine and wasteful wattage
		Engine.max_fps = in_menu_fps
		OS.low_processor_usage_mode = true
	else:
		OS.low_processor_usage_mode = false
		Engine.max_fps = max_fps


func set_max_fps(val: int) -> void:
	max_fps = val
	_configured_fps = val
	_update_effective_engine_pacing()
	settings_changed.emit()


func set_vsync(mode: int) -> void:
	vsync_mode = mode
	DisplayServer.window_set_vsync_mode(vsync_mode)
	settings_changed.emit()


func set_render_scale(scale_val: float) -> void:
	render_scale = clampf(scale_val, 0.5, 1.0)
	var vp = get_viewport()
	if vp:
		vp.scaling_3d_scale = render_scale
	settings_changed.emit()


func set_scaling_mode(mode: int) -> void:
	scaling_3d_mode = mode
	var vp = get_viewport()
	if vp:
		vp.scaling_3d_mode = scaling_3d_mode
	settings_changed.emit()


func set_quality_preset(preset: String) -> void:
	quality_preset = preset.to_upper()
	_apply_quality_preset_to_scene(quality_preset)
	preset_changed.emit(quality_preset)
	settings_changed.emit()


func apply_all() -> void:
	DisplayServer.window_set_vsync_mode(vsync_mode)
	_update_effective_engine_pacing()

	var vp = get_viewport()
	if vp:
		vp.scaling_3d_scale = render_scale
		vp.scaling_3d_mode = scaling_3d_mode

	_apply_quality_preset_to_scene(quality_preset)


func _apply_quality_preset_to_scene(preset: String) -> void:
	var cur = get_tree().current_scene
	if cur and cur.has_method("apply_quality_preset"):
		cur.apply_quality_preset(preset)


func _check_battery_state() -> void:
	if not auto_battery_saver:
		return
	if OS.get_name() == "Windows":
		var output: Array = []
		var exit_code := OS.execute("powershell.exe", ["-NoProfile", "-Command", "(Get-CimInstance -ClassName Win32_Battery).BatteryStatus"], output, false)
		if exit_code == 0 and output.size() > 0:
			var status_str: String = String(output[0]).strip_edges()
			# BatteryStatus: 1 = Discharging (On battery), 2 = AC Power (Plugged in)
			if status_str == "1":
				is_on_battery = true
				print("[PerfSettings] Battery discharge detected. Engaging POWER_SAVER preset.")
				set_quality_preset("POWER_SAVER")
				set_max_fps(60)
				return
	is_on_battery = false


func save_settings() -> void:
	var config := ConfigFile.new()
	config.set_value("graphics", "vsync_mode", vsync_mode)
	config.set_value("graphics", "max_fps", max_fps)
	config.set_value("graphics", "render_scale", render_scale)
	config.set_value("graphics", "scaling_3d_mode", scaling_3d_mode)
	config.set_value("graphics", "quality_preset", quality_preset)
	config.set_value("graphics", "auto_battery_saver", auto_battery_saver)
	config.save(CONFIG_PATH)


func load_settings() -> void:
	var config := ConfigFile.new()
	var err := config.load(CONFIG_PATH)
	if err == OK:
		vsync_mode = config.get_value("graphics", "vsync_mode", vsync_mode)
		max_fps = config.get_value("graphics", "max_fps", max_fps)
		_configured_fps = max_fps
		render_scale = config.get_value("graphics", "render_scale", render_scale)
		scaling_3d_mode = config.get_value("graphics", "scaling_3d_mode", scaling_3d_mode)
		quality_preset = config.get_value("graphics", "quality_preset", quality_preset)
		auto_battery_saver = config.get_value("graphics", "auto_battery_saver", auto_battery_saver)
