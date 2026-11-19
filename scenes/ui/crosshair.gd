# ============================================================================
# Crosshair — Custom drawn FPS crosshair with Hitmarker
# ============================================================================
extends Control

@export var crosshair_color := Color(1.0, 1.0, 1.0, 0.85)
@export var line_length := 8.0
@export var line_thickness := 2.0
@export var gap := 4.0
@export var dot_radius := 1.5
@export var show_outline := true
@export var outline_color := Color(0.0, 0.0, 0.0, 0.5)

# Hitmarker settings
@export var hitmarker_color := Color(1.0, 0.25, 0.25, 1.0)
@export var hitmarker_size := 7.0
@export var hitmarker_gap := 5.0
@export var hitmarker_duration := 0.18

var hitmarker_timer: float = 0.0


func _process(delta: float) -> void:
	if hitmarker_timer > 0.0:
		hitmarker_timer -= delta
		queue_redraw()


func show_hitmarker() -> void:
	hitmarker_timer = hitmarker_duration
	queue_redraw()


func _draw() -> void:
	var center := size / 2.0

	# 1. Base Crosshair
	if show_outline:
		var out_thick := line_thickness + 2.0
		_draw_cross(center, outline_color, out_thick)
		if dot_radius > 0.0:
			draw_circle(center, dot_radius + 1.0, outline_color)

	_draw_cross(center, crosshair_color, line_thickness)

	if dot_radius > 0.0:
		draw_circle(center, dot_radius, crosshair_color)

	# 2. Hitmarker (Diagonal X)
	if hitmarker_timer > 0.0:
		var alpha := clampf(hitmarker_timer / hitmarker_duration, 0.0, 1.0)
		var col := Color(hitmarker_color.r, hitmarker_color.g, hitmarker_color.b, alpha)
		var g := hitmarker_gap
		var s := hitmarker_size

		# Top-Left, Top-Right, Bottom-Left, Bottom-Right
		draw_line(center + Vector2(-g, -g), center + Vector2(-g - s, -g - s), col, 2.5)
		draw_line(center + Vector2(g, -g), center + Vector2(g + s, -g - s), col, 2.5)
		draw_line(center + Vector2(-g, g), center + Vector2(-g - s, g + s), col, 2.5)
		draw_line(center + Vector2(g, g), center + Vector2(g + s, g + s), col, 2.5)


func _draw_cross(center: Vector2, color: Color, thickness: float) -> void:
	draw_line(center + Vector2(0, -gap), center + Vector2(0, -gap - line_length), color, thickness)
	draw_line(center + Vector2(0, gap), center + Vector2(0, gap + line_length), color, thickness)
	draw_line(center + Vector2(-gap, 0), center + Vector2(-gap - line_length, 0), color, thickness)
	draw_line(center + Vector2(gap, 0), center + Vector2(gap + line_length, 0), color, thickness)
