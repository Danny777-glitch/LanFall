import os
import json
import urllib.request

BASE_DIR = r"c:\Users\danie\Documents\my_projects\lan-fall-phase1"
TEXTURES_DIR = os.path.join(BASE_DIR, "assets", "textures", "pbr")
MODELS_DIR = os.path.join(BASE_DIR, "assets", "models")
ROOT_TEX_DIR = os.path.join(BASE_DIR, "assets", "textures")

os.makedirs(TEXTURES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
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

# 1. HDRI Overcast Sky
try:
    print("Checking farmland_overcast HDRI...")
    hdri_data = fetch_json("https://api.polyhaven.com/files/farmland_overcast")
    if "hdri" in hdri_data and "1k" in hdri_data["hdri"] and "hdr" in hdri_data["hdri"]["1k"]:
        url = hdri_data["hdri"]["1k"]["hdr"]["url"]
        out_path = os.path.join(ROOT_TEX_DIR, "farmland_overcast_1k.hdr")
        download_file(url, out_path)
except Exception as e:
    print("Error downloading HDRI:", e)

# 2. Textures
TEXTURES = ["asphalt_02"]
for tex_id in TEXTURES:
    print(f"Processing texture: {tex_id}")
    try:
        data = fetch_json(f"https://api.polyhaven.com/files/{tex_id}")
        maps_to_download = [("Diffuse", "diff"), ("nor_gl", "nor_gl"), ("Rough", "rough")]
        for map_key, suffix in maps_to_download:
            for ext in ["jpg", "png"]:
                if map_key in data and "1k" in data[map_key] and ext in data[map_key]["1k"]:
                    file_info = data[map_key]["1k"][ext]
                    out_name = f"{tex_id}_{suffix}_1k.{ext}"
                    out_path = os.path.join(TEXTURES_DIR, out_name)
                    download_file(file_info["url"], out_path)
                    break
    except Exception as e:
        print(f"Error downloading {tex_id}:", e)

# 3. Models: concrete_road_barrier, fir_tree_01
MODELS = ["concrete_road_barrier", "fir_tree_01"]
for model_id in MODELS:
    print(f"Processing model: {model_id}")
    try:
        data = fetch_json(f"https://api.polyhaven.com/files/{model_id}")
        if "gltf" in data and "1k" in data["gltf"]:
            gltf_info = data["gltf"]["1k"]["gltf"]
            model_dir = os.path.join(MODELS_DIR, model_id)
            os.makedirs(model_dir, exist_ok=True)
            gltf_file = os.path.join(model_dir, f"{model_id}.gltf")
            download_file(gltf_info["url"], gltf_file)
            for rel_path, inc_info in gltf_info.get("include", {}).items():
                out_path = os.path.join(model_dir, rel_path)
                download_file(inc_info["url"], out_path)
    except Exception as e:
        print(f"Error downloading {model_id}:", e)

print("Finished downloading PBR assets.")
