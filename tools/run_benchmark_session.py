import os
import sys
import time
import subprocess
import argparse
import pandas as pd # or plain csv if pandas is not available

def run_session(name, duration=90, cap=0, preset="HIGH", is_release=False):
    os.makedirs("docs/perf", exist_ok=True)
    engine_csv = f"docs/perf/{name}_engine.csv"
    gpu_csv = f"docs/perf/{name}_gpu.csv"
    merged_csv = f"docs/perf/{name}.csv"

    # 1. Start nvidia-smi in background
    smi_cmd = [
        "nvidia-smi",
        "--query-gpu=power.draw,utilization.gpu,temperature.gpu,clocks.gr,clocks.mem",
        "--format=csv,noheader,nounits",
        "-l", "1"
    ]
    gpu_file = open(gpu_csv, "w", encoding="utf-8")
    gpu_file.write("power_watts,utilization_pct,temp_c,clock_gpu_mhz,clock_mem_mhz\n")
    gpu_file.flush()
    
    print(f"\n[Bench] Starting nvidia-smi monitoring -> {gpu_csv}", flush=True)
    gpu_proc = subprocess.Popen(smi_cmd, stdout=gpu_file, stderr=subprocess.PIPE, text=True)

    # Allow nvidia-smi to spin up
    time.sleep(1.0)

    # 2. Choose Godot binary
    godot_bin = r"C:\Users\danie\Downloads\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe"
    if is_release and os.path.exists("builds/LanFall_console.exe"):
        godot_bin = os.path.abspath("builds/LanFall_console.exe")
        print(f"[Bench] Running STANDALONE RELEASE build: {godot_bin}", flush=True)
    else:
        print(f"[Bench] Running Godot Runtime: {godot_bin}", flush=True)

    godot_cmd = [
        godot_bin,
        "--script", "res://tools/perf_log.gd",
        "--",
        f"--out={engine_csv}",
        f"--duration={duration}",
        f"--cap={cap}",
        f"--preset={preset}"
    ]

    print(f"[Bench] Launching benchmark (Duration: {duration}s, Cap: {cap}, Preset: {preset})...", flush=True)
    t_start = time.time()
    godot_proc = subprocess.run(godot_cmd)
    t_end = time.time()

    # 3. Terminate nvidia-smi
    gpu_proc.terminate()
    try:
        gpu_proc.wait(timeout=3)
    except:
        gpu_proc.kill()
    gpu_file.close()

    print(f"[Bench] Benchmark finished in {t_end - t_start:.1f}s. Processing metrics...", flush=True)

    # 4. Parse and Merge CSVs
    engine_rows = []
    if os.path.exists(engine_csv):
        with open(engine_csv, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
            header = lines[0].split(",")
            for l in lines[1:]:
                parts = l.split(",")
                if len(parts) == len(header):
                    row = {header[i]: parts[i] for i in range(len(header))}
                    engine_rows.append(row)

    gpu_rows = []
    if os.path.exists(gpu_csv):
        with open(gpu_csv, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
            header = lines[0].split(",")
            for l in lines[1:]:
                parts = [p.strip() for p in l.split(",")]
                if len(parts) >= len(header):
                    try:
                        row = {
                            "power_watts": float(parts[0]),
                            "utilization_pct": float(parts[1]),
                            "temp_c": float(parts[2]),
                            "clock_gpu_mhz": float(parts[3]),
                            "clock_mem_mhz": float(parts[4])
                        }
                        gpu_rows.append(row)
                    except ValueError:
                        pass

    # Merge by row index
    n_samples = min(len(engine_rows), len(gpu_rows))
    merged_rows = []
    for i in range(n_samples):
        er = engine_rows[i]
        gr = gpu_rows[i]
        merged_row = {**er, **gr}
        merged_rows.append(merged_row)

    # Save merged CSV
    if merged_rows:
        keys = list(merged_rows[0].keys())
        with open(merged_csv, "w", encoding="utf-8") as f:
            f.write(",".join(keys) + "\n")
            for r in merged_rows:
                f.write(",".join(str(r[k]) for k in keys) + "\n")

    # 5. Compute Statistics
    if merged_rows:
        fps_list = [float(r["fps"]) for r in merged_rows]
        ms_list = [float(r["frame_time_ms"]) for r in merged_rows]
        watts_list = [float(r["power_watts"]) for r in merged_rows]
        util_list = [float(r["utilization_pct"]) for r in merged_rows]
        temp_list = [float(r["temp_c"]) for r in merged_rows]
        vram_list = [float(r["vram_mb"]) for r in merged_rows]
        dc_list = [int(r["draw_calls"]) for r in merged_rows]

        avg_fps = sum(fps_list) / len(fps_list)
        min_fps = min(fps_list)
        max_fps = max(fps_list)

        avg_ms = sum(ms_list) / len(ms_list)
        avg_watts = sum(watts_list) / len(watts_list)
        peak_watts = max(watts_list)

        avg_util = sum(util_list) / len(util_list)
        peak_util = max(util_list)

        avg_temp = sum(temp_list) / len(temp_list)
        peak_temp = max(temp_list)

        avg_vram = sum(vram_list) / len(vram_list)
        avg_dc = sum(dc_list) / len(dc_list)

        summary = f"""
===========================================================================
  BENCHMARK SUMMARY: {name.upper()} (Cap: {cap} FPS | Duration: {duration}s | Preset: {preset})
===========================================================================
  Average Power Draw:     {avg_watts:6.1f} W   (Peak: {peak_watts:6.1f} W)
  Average GPU Load:       {avg_util:6.1f} %   (Peak: {peak_util:6.1f} %)
  Average Temperature:    {avg_temp:6.1f} °C  (Peak: {peak_temp:6.1f} °C)
  Average Frame Rate:     {avg_fps:6.1f} FPS (Min: {min_fps:5.1f}, Max: {max_fps:5.1f})
  Average Frame Time:     {avg_ms:6.2f} ms
  Average VRAM Memory:    {avg_vram:6.1f} MB
  Average Draw Calls:     {avg_dc:6.0f} DC
===========================================================================
Merged data written to: {merged_csv}
"""
        print(summary, flush=True)

        # Write summary file
        with open(f"docs/perf/{name}_summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
            
        return {
            "name": name,
            "avg_watts": avg_watts,
            "peak_watts": peak_watts,
            "avg_util": avg_util,
            "peak_util": peak_util,
            "avg_temp": avg_temp,
            "avg_fps": avg_fps,
            "avg_ms": avg_ms,
            "avg_vram": avg_vram,
            "avg_dc": avg_dc
        }
    else:
        print("[Bench] Warning: No rows collected!")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="baseline", help="Session name")
    parser.add_argument("--duration", type=int, default=90, help="Duration in seconds")
    parser.add_argument("--cap", type=int, default=0, help="Frame cap (0=uncapped)")
    parser.add_argument("--preset", default="HIGH", help="Quality preset (LOW/MEDIUM/HIGH/ULTRA)")
    parser.add_argument("--release", action="store_true", help="Use release standalone binary")
    args = parser.parse_args()

    run_session(args.name, duration=args.duration, cap=args.cap, preset=args.preset, is_release=args.release)
