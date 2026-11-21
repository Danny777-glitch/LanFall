import os
import sys
import json
import subprocess

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def curl_download(url, dest_path):
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"  Already exists ({os.path.getsize(dest_path)} bytes): {os.path.basename(dest_path)}", flush=True)
        return True
    
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    print(f"  Downloading: {url} -> {os.path.basename(dest_path)}", flush=True)
    
    cmd = [
        "curl.exe", "-L", "-C", "-",
        "--retry", "5",
        "--retry-delay", "2",
        "--speed-limit", "1000",
        "--speed-time", "15",
        "-A", USER_AGENT,
        url,
        "-o", os.path.abspath(dest_path)
    ]
    try:
        ret = subprocess.run(cmd, check=True)
        size = os.path.getsize(dest_path)
        print(f"  Done ({size} bytes): {os.path.basename(dest_path)}", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  FAILED curl on {url}", flush=True)
        return False

def curl_json(url):
    cmd = ["curl.exe", "-s", "-L", "--retry", "3", "-A", USER_AGENT, url]
    ret = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(ret.stdout)

def fetch_polyhaven_asset(asset_id, res="4k", target_dir=None):
    if target_dir is None:
        target_dir = os.path.join("assets/textures/pbr_4k", asset_id)
    os.makedirs(target_dir, exist_ok=True)
    
    api_url = f"https://api.polyhaven.com/files/{asset_id}"
    try:
        data = curl_json(api_url)
    except Exception as e:
        print(f"Failed to query API for {asset_id}: {e}", flush=True)
        return False

    # Check if HDRI
    if "hdri" in data:
        hdri_info = data["hdri"].get(res, {}).get("hdr") or data["hdri"].get("4k", {}).get("hdr")
        if hdri_info:
            dest = os.path.join(target_dir, f"{asset_id}_{res}.hdr")
            curl_download(hdri_info["url"], dest)
            return True

    # Texture maps: Diffuse, nor_gl, arm (fallback to Rough, AO)
    maps_to_get = ["Diffuse", "nor_gl"]
    if "arm" in data:
        maps_to_get.append("arm")
    else:
        if "Rough" in data:
            maps_to_get.append("Rough")
        if "AO" in data:
            maps_to_get.append("AO")

    for map_key in maps_to_get:
        if map_key in data:
            formats = data[map_key].get(res, {})
            fmt = "jpg" if "jpg" in formats else ("png" if "png" in formats else None)
            if fmt:
                info = formats[fmt]
                url = info["url"]
                dest_file = os.path.join(target_dir, f"{asset_id}_{map_key.lower()}_{res}.{fmt}")
                curl_download(url, dest_file)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asset_name = sys.argv[1]
        res = sys.argv[2] if len(sys.argv) > 2 else "4k"
        print(f"Fetching {asset_name} ({res})...", flush=True)
        fetch_polyhaven_asset(asset_name, res)
    else:
        print("Usage: fetch_textures.py <asset_id> [resolution]", flush=True)
