import os
import json
import urllib.request

BASE_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1"
TEXTURES_DIR = os.path.join(BASE_DIR, "assets", "textures", "pbr")
MODELS_DIR = os.path.join(BASE_DIR, "assets", "models")

os.makedirs(TEXTURES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

def download_file(url, out_path):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  [Exists] {os.path.basename(out_path)}")
        return
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    print(f"  [Downloaded] {os.path.basename(out_path)} ({os.path.getsize(out_path)} bytes)")

# -----------------------------------------------------------------------------
# 1. Download PBR Textures
# -----------------------------------------------------------------------------
TEXTURE_NAMES = [
    "container_side",
    "corrugated_iron_02",
    "brown_planks_08",
    "bark_brown_01",
    "clay_roof_tiles_02",
    "chipped_concrete",
    "dirty_concrete",
    "stony_dirt_path",
    "sparse_grass",
]

print("=== DOWNLOADING POLYHAVEN PBR TEXTURES ===")
for tex_id in TEXTURE_NAMES:
    print(f"\nProcessing texture: {tex_id}")
    try:
        data = fetch_json(f"https://api.polyhaven.com/files/{tex_id}")
        maps_to_download = [
            ("Diffuse", "diff"),
            ("nor_gl", "nor_gl"),
            ("Rough", "rough"),
        ]
        for map_key, suffix in maps_to_download:
            if map_key in data and "1k" in data[map_key] and "jpg" in data[map_key]["1k"]:
                file_info = data[map_key]["1k"]["jpg"]
                out_name = f"{tex_id}_{suffix}_1k.jpg"
                out_path = os.path.join(TEXTURES_DIR, out_name)
                download_file(file_info["url"], out_path)
            elif map_key in data and "1k" in data[map_key] and "png" in data[map_key]["1k"]:
                file_info = data[map_key]["1k"]["png"]
                out_name = f"{tex_id}_{suffix}_1k.png"
                out_path = os.path.join(TEXTURES_DIR, out_name)
                download_file(file_info["url"], out_path)
    except Exception as e:
        print(f"  Error downloading {tex_id}: {e}")

# -----------------------------------------------------------------------------
# 2. Download 3D Models (GLTF 1k)
# -----------------------------------------------------------------------------
MODEL_NAMES = [
    "wooden_military_crate",
    "old_military_crate",
    "wooden_crate_01",
    "ammo_box",
    "Barrel_01",
    "wooden_table_02",
    "hanging_industrial_lamp",
    "pine_tree_01",
    "sand_rocks_small_01",
]

print("\n=== DOWNLOADING POLYHAVEN 3D MODELS ===")
for model_id in MODEL_NAMES:
    print(f"\nProcessing model: {model_id}")
    try:
        data = fetch_json(f"https://api.polyhaven.com/files/{model_id}")
        if "gltf" not in data or "1k" not in data["gltf"]:
            print(f"  GLTF 1k not available for {model_id}")
            continue
        gltf_info = data["gltf"]["1k"]["gltf"]
        model_dir = os.path.join(MODELS_DIR, model_id)
        os.makedirs(model_dir, exist_ok=True)
        
        gltf_file = os.path.join(model_dir, f"{model_id}.gltf")
        download_file(gltf_info["url"], gltf_file)
        
        for rel_path, inc_info in gltf_info.get("include", {}).items():
            out_path = os.path.join(model_dir, rel_path)
            download_file(inc_info["url"], out_path)
    except Exception as e:
        print(f"  Error downloading model {model_id}: {e}")

print("\n=== ALL HIGH QUALITY ASSETS DOWNLOAD COMPLETED! ===")
