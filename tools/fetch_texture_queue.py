import os
import sys
import time
from fetch_textures import fetch_polyhaven_asset
from optimize_imports import scan_and_optimize

QUEUE = [
    "brown_planks_08",
    "corrugated_iron_02",
    "dirty_concrete",
    "chipped_concrete",
    "clay_roof_tiles_02",
    "sparse_grass",
    "stony_dirt_path",
    "bark_brown_01",
    "container_side"
]

def run_queue():
    for asset_id in QUEUE:
        print(f"\n==========================================", flush=True)
        print(f"PROCESSING ASSET: {asset_id} (4k)", flush=True)
        print(f"==========================================", flush=True)
        success = False
        for attempt in range(3):
            try:
                success = fetch_polyhaven_asset(asset_id, "4k")
                if success:
                    break
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}", flush=True)
                time.sleep(2)
        if not success:
            print(f"ERROR: Failed to download {asset_id}", flush=True)
        else:
            print(f"SUCCESS: {asset_id} downloaded", flush=True)
    
    print("\nOptimizing .import files...", flush=True)
    scan_and_optimize("assets/textures/pbr_4k")
    print("ALL DONE!", flush=True)

if __name__ == "__main__":
    run_queue()
