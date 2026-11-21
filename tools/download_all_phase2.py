import os
import sys
import time
from fetch_textures import fetch_polyhaven_asset
from optimize_imports import scan_and_optimize

TEXTURE_LIST = [
    ("dirty_concrete", "4k"),
    ("chipped_concrete", "4k"),
    ("clay_roof_tiles_02", "4k"),
    ("container_side", "4k"),
    ("bark_brown_01", "4k"),
    ("sparse_grass", "2k"),
    ("stony_dirt_path", "2k"),
]

def main():
    for asset_id, res in TEXTURE_LIST:
        print(f"\n==========================================", flush=True)
        print(f"FETCHING {asset_id} ({res})", flush=True)
        print(f"==========================================", flush=True)
        for attempt in range(3):
            try:
                ok = fetch_polyhaven_asset(asset_id, res)
                if ok:
                    print(f"SUCCESS: {asset_id} ({res})", flush=True)
                    break
            except Exception as e:
                print(f"Error {e}, retrying in 2s...", flush=True)
                time.sleep(2)
    
    print("\nOptimizing texture import files...", flush=True)
    scan_and_optimize("assets/textures/pbr_4k")
    print("DONE WITH BATCH!", flush=True)

if __name__ == "__main__":
    main()
