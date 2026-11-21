import os
import subprocess
import time

FOLDERS = [
    "stony_dirt_path",
    "dirty_concrete",
    "asphalt_02",
    "container_side",
    "bark_brown_01",
    "clay_roof_tiles_02",
    "chipped_concrete",
    "brown_planks_08",
    "corrugated_iron_02",
]

def run(cmd):
    print(f">> {cmd}", flush=True)
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {res.stderr}", flush=True)
    else:
        print(res.stdout, flush=True)
    return res.returncode == 0

def main():
    p = "assets/textures/pbr_4k"
    for folder in FOLDERS:
        full_path = os.path.join(p, folder)
        if not os.path.exists(full_path):
            continue
        
        # Check if folder has uncommitted changes
        status_res = subprocess.run(f"git status --porcelain {full_path}", shell=True, capture_output=True, text=True)
        if not status_res.stdout.strip():
            print(f"Skipping {folder}: already committed.", flush=True)
            continue
        
        print(f"\n==========================================", flush=True)
        print(f"COMMITTING & PUSHING: {folder}", flush=True)
        print(f"==========================================", flush=True)
        
        if not run(f'git add "{full_path}"'):
            continue
        if not run(f'git commit -m "assets(pbr): add {folder} PBR textures"'):
            continue
        
        # Push with retry
        for attempt in range(3):
            print(f"Pushing {folder} (attempt {attempt+1})...", flush=True)
            if run("git push origin main"):
                print(f"SUCCESS: Pushed {folder}!", flush=True)
                break
            print("Push failed, waiting 5s to retry...", flush=True)
            time.sleep(5)
            
    print("\nALL TEXTURE BATCHES COMMITTED AND PUSHED!", flush=True)

if __name__ == "__main__":
    main()
