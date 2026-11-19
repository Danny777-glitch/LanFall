# ============================================================================
# ProfileManager — Player Customization & Profile State Autoload
# ============================================================================
# Manages Operative suits, visor glow colors, weapon loadouts, skins,
# and player identity (BGMI / PUBG / Valorant style).
# ============================================================================
extends Node

signal profile_updated

const SAVE_PATH = "user://profile_data.json"

# -- Player Identity --
var player_name: String = "SMxTHUG"
var player_level: int = 35
var player_title: String = "CONQUEROR // ELITE"
var gold_coins: int = 6289
var rp_points: int = 35

# -- Customization Selection Indices --
var current_suit_index: int = 0
var current_visor_index: int = 0
var current_weapon_index: int = 0 # 0: AR, 1: Pistol, 2: Sniper, 3: Knife
var current_weapon_skin_index: int = 0

# -- Preset Operative Suits --
const OPERATIVE_SUITS: Array[Dictionary] = [
	{
		"name": "SPECTRE BLACK-OPS",
		"icon": "🥷",
		"rarity": "LEGENDARY",
		"desc": "Tactical matte carbon weave with military stealth plates.",
		"suit_color": Color(0.12, 0.15, 0.20, 1.0),
		"armor_color": Color(0.18, 0.20, 0.25, 1.0),
		"default_visor": Color(0.15, 0.85, 1.0, 1.0), # Cyan
		"metallic": 0.5,
		"roughness": 0.45
	},
	{
		"name": "VIPER BIO-TOXIN",
		"icon": "🐍",
		"rarity": "EPIC",
		"desc": "Acid-resistant reinforced polymer with venomous trim.",
		"suit_color": Color(0.08, 0.16, 0.10, 1.0),
		"armor_color": Color(0.12, 0.26, 0.15, 1.0),
		"default_visor": Color(0.25, 1.0, 0.35, 1.0), # Emerald Green
		"metallic": 0.4,
		"roughness": 0.4
	},
	{
		"name": "CYBERPUNK NEON",
		"icon": "⚡",
		"rarity": "MYTHIC",
		"desc": "Ultra-light carbon exoskeleton with hyper-pink radiant core.",
		"suit_color": Color(0.10, 0.08, 0.16, 1.0),
		"armor_color": Color(0.22, 0.12, 0.30, 1.0),
		"default_visor": Color(1.0, 0.15, 0.85, 1.0), # Neon Magenta
		"metallic": 0.65,
		"roughness": 0.35
	},
	{
		"name": "PRIME GOLD ELITE",
		"icon": "👑",
		"rarity": "ULTIMATE",
		"desc": "Ceramic white royal plating forged with 24K polished gold alloy.",
		"suit_color": Color(0.92, 0.92, 0.95, 1.0),
		"armor_color": Color(0.85, 0.68, 0.22, 1.0),
		"default_visor": Color(1.0, 0.82, 0.25, 1.0), # Solar Gold
		"metallic": 0.85,
		"roughness": 0.22
	},
	{
		"name": "ARCTIC VANGUARD",
		"icon": "❄️",
		"rarity": "EPIC",
		"desc": "Polar weather tactical composite with ice-blue visor glare.",
		"suit_color": Color(0.85, 0.90, 0.95, 1.0),
		"armor_color": Color(0.45, 0.55, 0.65, 1.0),
		"default_visor": Color(0.40, 0.85, 1.0, 1.0), # Frost Ice
		"metallic": 0.45,
		"roughness": 0.5
	},
	{
		"name": "CRIMSON HAZARD",
		"icon": "🌋",
		"rarity": "MYTHIC",
		"desc": "Heavy molten hazard plates designed for front-line breach.",
		"suit_color": Color(0.25, 0.08, 0.08, 1.0),
		"armor_color": Color(0.55, 0.12, 0.12, 1.0),
		"default_visor": Color(1.0, 0.30, 0.10, 1.0), # Molten Orange
		"metallic": 0.6,
		"roughness": 0.38
	}
]

# -- Visor & Core Glow Colors --
const VISOR_GLOW_COLORS: Array[Dictionary] = [
	{ "name": "RADIANITE CYAN", "color": Color(0.15, 0.90, 1.0, 1.0), "icon": "💠" },
	{ "name": "VENOM EMERALD",  "color": Color(0.20, 1.0, 0.40, 1.0), "icon": "🟢" },
	{ "name": "NEON MAGENTA",   "color": Color(1.0, 0.15, 0.85, 1.0), "icon": "🟣" },
	{ "name": "SOLAR GOLD",     "color": Color(1.0, 0.82, 0.20, 1.0), "icon": "🟡" },
	{ "name": "CRIMSON FLAME",  "color": Color(1.0, 0.22, 0.18, 1.0), "icon": "🔴" },
	{ "name": "ARCTIC FROST",   "color": Color(0.55, 0.88, 1.0, 1.0), "icon": "⚪" },
	{ "name": "VOID PURPLE",    "color": Color(0.75, 0.25, 1.0, 1.0), "icon": "🔮" }
]

# -- Weapon Names --
const WEAPONS_CATALOG: Array[Dictionary] = [
	{ "name": "VANGUARD AR",      "slot": "SLOT 1 - RIFLE",  "icon": "🔫", "desc": "30-round automatic assault rifle with holo-sight." },
	{ "name": "PHANTOM PISTOL",   "slot": "SLOT 2 - PISTOL", "icon": "🎯", "desc": "High precision tactical sidearm with tritium sights." },
	{ "name": "OPERATOR SNIPER",  "slot": "SLOT 3 - SNIPER", "icon": "🔭", "desc": "Heavy bolt-action precision marksman rifle." },
	{ "name": "TACTICAL BLADE",   "slot": "SLOT 4 - MELEE",  "icon": "🗡️", "desc": "High-speed tactical knife with inspect spin [F]." }
]

# -- Weapon Skins --
const WEAPON_SKINS: Array[Dictionary] = [
	{
		"name": "TACTICAL SPEC-OPS",
		"icon": "🔫",
		"rarity": "STANDARD",
		"desc": "Standard military matte black with gunmetal accents.",
		"primary_color": Color(0.14, 0.16, 0.19, 1.0),
		"accent_color": Color(0.28, 0.30, 0.35, 1.0),
		"glow_color": Color(0.2, 0.9, 1.0, 1.0),
		"metallic": 0.7,
		"roughness": 0.35
	},
	{
		"name": "PRIME GOLD",
		"icon": "✨",
		"rarity": "ULTIMATE",
		"desc": "Polished pure 24K gold body with ivory white trims.",
		"primary_color": Color(0.88, 0.72, 0.22, 1.0),
		"accent_color": Color(0.95, 0.95, 0.98, 1.0),
		"glow_color": Color(1.0, 0.85, 0.3, 1.0),
		"metallic": 0.92,
		"roughness": 0.18
	},
	{
		"name": "RADIANITE GLITCH",
		"icon": "💠",
		"rarity": "EPIC",
		"desc": "Cybernetic teal energy body with high-emission lines.",
		"primary_color": Color(0.08, 0.18, 0.22, 1.0),
		"accent_color": Color(0.15, 0.88, 0.95, 1.0),
		"glow_color": Color(0.15, 0.95, 0.90, 1.0),
		"metallic": 0.6,
		"roughness": 0.3
	},
	{
		"name": "CRIMSON FURY",
		"icon": "🔥",
		"rarity": "LEGENDARY",
		"desc": "Tactical matte carbon chassis forged with anodized crimson alloy accents.",
		"primary_color": Color(0.13, 0.14, 0.17, 1.0),
		"accent_color": Color(0.82, 0.14, 0.18, 1.0),
		"glow_color": Color(1.0, 0.32, 0.12, 1.0),
		"metallic": 0.72,
		"roughness": 0.28
	},
	{
		"name": "GLACIAL FROST",
		"icon": "🧊",
		"rarity": "EPIC",
		"desc": "Frozen diamond crystal sheen with pale frost accents.",
		"primary_color": Color(0.65, 0.80, 0.92, 1.0),
		"accent_color": Color(0.90, 0.95, 1.0, 1.0),
		"glow_color": Color(0.50, 0.85, 1.0, 1.0),
		"metallic": 0.8,
		"roughness": 0.2
	}
]


func _ready() -> void:
	load_profile()


func get_current_suit() -> Dictionary:
	return OPERATIVE_SUITS[clamp(current_suit_index, 0, OPERATIVE_SUITS.size() - 1)]


func get_current_visor_color() -> Color:
	var visor_entry := VISOR_GLOW_COLORS[clamp(current_visor_index, 0, VISOR_GLOW_COLORS.size() - 1)]
	return visor_entry["color"]


func get_current_weapon_skin() -> Dictionary:
	return WEAPON_SKINS[clamp(current_weapon_skin_index, 0, WEAPON_SKINS.size() - 1)]


func get_customization_dictionary() -> Dictionary:
	return {
		"name": player_name,
		"suit_index": current_suit_index,
		"visor_index": current_visor_index,
		"weapon_index": current_weapon_index,
		"weapon_skin_index": current_weapon_skin_index,
		"suit_data": get_current_suit(),
		"visor_color": get_current_visor_color(),
		"skin_data": get_current_weapon_skin()
	}


func set_suit(index: int) -> void:
	current_suit_index = clamp(index, 0, OPERATIVE_SUITS.size() - 1)
	profile_updated.emit()
	save_profile()


func set_visor(index: int) -> void:
	current_visor_index = clamp(index, 0, VISOR_GLOW_COLORS.size() - 1)
	profile_updated.emit()
	save_profile()


func set_weapon(index: int) -> void:
	current_weapon_index = clamp(index, 0, WEAPONS_CATALOG.size() - 1)
	profile_updated.emit()
	save_profile()


func set_weapon_skin(index: int) -> void:
	current_weapon_skin_index = clamp(index, 0, WEAPON_SKINS.size() - 1)
	profile_updated.emit()
	save_profile()


func set_player_name(new_name: String) -> void:
	var clean := new_name.strip_edges()
	if not clean.is_empty():
		player_name = clean
		profile_updated.emit()
		save_profile()


func save_profile() -> void:
	var data := {
		"player_name": player_name,
		"player_level": player_level,
		"gold_coins": gold_coins,
		"rp_points": rp_points,
		"current_suit_index": current_suit_index,
		"current_visor_index": current_visor_index,
		"current_weapon_index": current_weapon_index,
		"current_weapon_skin_index": current_weapon_skin_index
	}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(data, "\t"))
		f.close()


func load_profile() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not f:
		return
	var text := f.get_as_text()
	f.close()

	var json := JSON.new()
	if json.parse(text) == OK and json.data is Dictionary:
		var d: Dictionary = json.data
		if d.has("player_name"):
			player_name = d["player_name"]
		if d.has("player_level"):
			player_level = int(d["player_level"])
		if d.has("current_suit_index"):
			current_suit_index = int(d["current_suit_index"])
		if d.has("current_visor_index"):
			current_visor_index = int(d["current_visor_index"])
		if d.has("current_weapon_index"):
			current_weapon_index = int(d["current_weapon_index"])
		if d.has("current_weapon_skin_index"):
			current_weapon_skin_index = int(d["current_weapon_skin_index"])
