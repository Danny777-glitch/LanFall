# ============================================================================
# Minimap — Tactical 3D HUD Radar System
# ============================================================================
# Renders a Valorant / BGMI style top-down tactical radar display:
# - Concentric tactical scan rings & crosshairs
# - Dynamic rotating North [N] compass indicator
# - Center Player arrow showing orientation
# - Site markers [A] and [B] clamped to radar boundary
# - Target dummies & LAN players blips
# ============================================================================
extends Control

@export var radar_radius: float = 78.0
@export var world_scale: float = 1.6 # World meters to radar pixels (78px = ~48m range)
@export var show_grid: bool = true

var player_node: Node3D = null
var pulse_time: float = 0.0
var redraw_timer: float = 0.0
const REDRAW_INTERVAL: float = 0.033 # 30 FPS redraw throttle

var cached_dummies: Array = []
var dummy_cache_timer: float = 0.0

# Strategic Site Locations
const SITES: Array[Dictionary] = [
	{ "name": "A", "pos": Vector2(35.0, 28.0), "color": Color(0.2, 0.88, 1.0) },
	{ "name": "B", "pos": Vector2(-38.0, 28.0), "color": Color(1.0, 0.72, 0.2) },
	{ "name": "MID", "pos": Vector2(0.0, -18.0), "color": Color(0.8, 0.8, 0.9) }
]


func _ready() -> void:
	custom_minimum_size = Vector2(radar_radius * 2 + 16, radar_radius * 2 + 16)


func _process(delta: float) -> void:
	pulse_time += delta * 2.0

	dummy_cache_timer += delta
	if dummy_cache_timer >= 0.5:
		dummy_cache_timer = 0.0
		cached_dummies = get_tree().get_nodes_in_group("targets")

	redraw_timer += delta
	if redraw_timer >= REDRAW_INTERVAL:
		redraw_timer = 0.0
		if not player_node or not is_instance_valid(player_node):
			_find_player()
		queue_redraw()


func _find_player() -> void:
	# Local player lookup
	var players = get_tree().get_nodes_in_group("players")
	if players.size() > 0:
		player_node = players[0]
	else:
		# Fallback: check map root
		var p = get_tree().root.find_child("Player", true, false)
		if p and p is Node3D:
			player_node = p


func _draw() -> void:
	var center: Vector2 = size * 0.5
	var r: float = radar_radius

	# 1. Dark Glass Radar Background
	draw_circle(center, r, Color(0.05, 0.07, 0.12, 0.88))
	draw_arc(center, r, 0, TAU, 48, Color(0.2, 0.85, 1.0, 0.9), 2.0)
	draw_arc(center, r * 0.55, 0, TAU, 32, Color(0.2, 0.85, 1.0, 0.3), 1.0)

	# 2. Crosshairs
	draw_line(center - Vector2(r, 0), center + Vector2(r, 0), Color(0.2, 0.85, 1.0, 0.22), 1.0)
	draw_line(center - Vector2(0, r), center + Vector2(0, r), Color(0.2, 0.85, 1.0, 0.22), 1.0)

	# If no player found yet, just draw center point
	if not player_node:
		draw_circle(center, 4, Color(0.2, 1.0, 0.5))
		return

	var p_pos_3d: Vector3 = player_node.global_position
	var p_pos: Vector2 = Vector2(p_pos_3d.x, p_pos_3d.z)
	var p_rot: float = player_node.rotation.y

	# 3. Rotating North Marker [N]
	var north_angle: float = -p_rot - PI * 0.5
	var north_dir: Vector2 = Vector2(cos(north_angle), sin(north_angle))
	var north_pos: Vector2 = center + (north_dir * (r - 10))
	draw_string(ThemeDB.fallback_font, north_pos + Vector2(-4, 4), "N", HORIZONTAL_ALIGNMENT_CENTER, -1, 10, Color(1.0, 0.35, 0.35, 0.9))

	# 4. Draw Strategic Sites [A] and [B]
	for site in SITES:
		var site_pos: Vector2 = site.get("pos", Vector2.ZERO)
		var rel: Vector2 = site_pos - p_pos
		# Rotate relative to player view
		var rot_rel: Vector2 = rel.rotated(-p_rot)
		var map_pos: Vector2 = rot_rel * world_scale

		# Clamp to perimeter if out of range
		var dist: float = map_pos.length()
		var clamped: bool = false
		if dist > (r - 14):
			map_pos = map_pos.normalized() * (r - 14)
			clamped = true

		var draw_pt: Vector2 = center + map_pos
		var col: Color = site.get("color", Color.WHITE)
		if clamped:
			col.a = 0.65

		# Draw site badge ring & letter
		draw_circle(draw_pt, 7, Color(0.08, 0.1, 0.16, 0.9))
		draw_arc(draw_pt, 7, 0, TAU, 16, col, 1.5)
		draw_string(ThemeDB.fallback_font, draw_pt + Vector2(-3, 3.5), String(site.get("name", "")), HORIZONTAL_ALIGNMENT_CENTER, -1, 9, col)

	# 5. Draw Target Dummies as Amber/Red blips
	for dummy in cached_dummies:
		if not is_instance_valid(dummy) or not (dummy is Node3D):
			continue
		var d_node := dummy as Node3D
		var d_pos: Vector2 = Vector2(d_node.global_position.x, d_node.global_position.z)
		var rel_d: Vector2 = (d_pos - p_pos).rotated(-p_rot) * world_scale
		if rel_d.length() <= (r - 6):
			var pt: Vector2 = center + rel_d
			draw_circle(pt, 3.5, Color(1.0, 0.3, 0.3, 0.95))
			draw_arc(pt, 5.0, 0, TAU, 12, Color(1.0, 0.7, 0.2, 0.6), 1.0)

	# 6. Center Player Arrow
	var arrow_pts: PackedVector2Array = [
		center + Vector2(0, -9),
		center + Vector2(-6, 6),
		center + Vector2(0, 3),
		center + Vector2(6, 6)
	]
	draw_colored_polygon(arrow_pts, Color(0.15, 0.95, 1.0, 1.0))

	# Player pulse scan ring
	var scan_r: float = fmod(pulse_time * 24.0, r)
	draw_arc(center, scan_r, 0, TAU, 24, Color(0.15, 0.95, 1.0, max(0.0, 1.0 - (scan_r / r))), 1.0)
