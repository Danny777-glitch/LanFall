# ============================================================================
# GameInput — Autoload
# ============================================================================
# Registers all game input actions on startup.
# This avoids the need to manually configure the Input Map in Project Settings.
# Add new actions here as the game grows.
# ============================================================================
extends Node


func _ready() -> void:
	# ── Movement ──
	_add_key_action("move_forward", KEY_W)
	_add_key_action("move_backward", KEY_S)
	_add_key_action("move_left", KEY_A)
	_add_key_action("move_right", KEY_D)
	_add_key_action("jump", KEY_SPACE)
	_add_key_action("sprint", KEY_SHIFT)
	_add_key_action("crouch", KEY_CTRL)

	# ── Combat ──
	_add_mouse_action("shoot", MOUSE_BUTTON_LEFT)
	_add_mouse_action("aim", MOUSE_BUTTON_RIGHT)
	_add_key_action("reload", KEY_R)
	_add_key_action("ability_e", KEY_E)
	_add_key_action("inspect", KEY_F)

	# ── Weapon Slots ──
	_add_key_action("weapon_1", KEY_1)
	_add_key_action("weapon_2", KEY_2)
	_add_key_action("weapon_3", KEY_3)
	_add_key_action("weapon_4", KEY_4)
	_add_key_action("melee_v", KEY_V)
	_add_mouse_action("next_weapon", MOUSE_BUTTON_WHEEL_UP)
	_add_mouse_action("prev_weapon", MOUSE_BUTTON_WHEEL_DOWN)

	# ── UI ──
	_add_key_action("scoreboard", KEY_TAB)
	_add_key_action("pause_game", KEY_ESCAPE)


## Register a keyboard action if it doesn't already exist.
func _add_key_action(action_name: String, keycode: Key) -> void:
	if InputMap.has_action(action_name):
		return
	InputMap.add_action(action_name)
	var event := InputEventKey.new()
	event.physical_keycode = keycode
	InputMap.action_add_event(action_name, event)


## Register a mouse button action if it doesn't already exist.
func _add_mouse_action(action_name: String, button: MouseButton) -> void:
	if InputMap.has_action(action_name):
		return
	InputMap.add_action(action_name)
	var event := InputEventMouseButton.new()
	event.button_index = button
	InputMap.action_add_event(action_name, event)
