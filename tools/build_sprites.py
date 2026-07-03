#!/usr/bin/env python3
"""Extract frames from hero orbit clip and pack into sprite sheets for canvas scrubbing.

Usage: python3 build_sprites.py <input.mp4> <outdir> [n_frames] [cell_w] [cell_h] [cols] [rows]
Outputs: outdir/sheet_00.webp ... plus manifest.json and poster.webp
"""
import json, math, os, shutil, subprocess, sys
from PIL import Image

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        sys.exit(1)
    return r.stdout

def main():
    src = sys.argv[1]
    outdir = sys.argv[2]
    n_frames = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    cw = int(sys.argv[4]) if len(sys.argv) > 4 else 1280
    ch = int(sys.argv[5]) if len(sys.argv) > 5 else 720
    cols = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    rows = int(sys.argv[7]) if len(sys.argv) > 7 else 3

    tmp = os.path.join(outdir, "_frames")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)

    # Probe duration
    dur = float(run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 '{src}'").strip())
    fps = n_frames / dur
    # Extract exactly n_frames evenly, light sharpen to recover crispness at 720p
    run(
        f"ffmpeg -y -i '{src}' -vf \"fps={fps:.6f},scale={cw}:{ch}:flags=lanczos,unsharp=5:5:0.4:5:5:0.0\" "
        f"-frames:v {n_frames} -q:v 2 '{tmp}/f_%04d.jpg' 2>&1 | tail -1"
    )
    frames = sorted(f for f in os.listdir(tmp) if f.endswith(".jpg"))[:n_frames]
    actual = len(frames)
    per_sheet = cols * rows
    n_sheets = math.ceil(actual / per_sheet)
    print(f"duration={dur:.2f}s frames={actual} sheets={n_sheets} cell={cw}x{ch}")

    sheet_files = []
    for s in range(n_sheets):
        sheet = Image.new("RGB", (cw * cols, ch * rows), (8, 9, 8))
        for i in range(per_sheet):
            gi = s * per_sheet + i
            if gi >= actual:
                break
            im = Image.open(os.path.join(tmp, frames[gi]))
            sheet.paste(im, ((i % cols) * cw, (i // cols) * ch))
        name = f"sheet_{s:02d}.webp"
        sheet.save(os.path.join(outdir, name), "WEBP", quality=72, method=4)
        sheet_files.append(name)
        print(name, os.path.getsize(os.path.join(outdir, name)) // 1024, "KB")

    # Poster = first frame
    Image.open(os.path.join(tmp, frames[0])).save(os.path.join(outdir, "poster.webp"), "WEBP", quality=80)

    manifest = {"frames": actual, "cols": cols, "rows": rows, "fw": cw, "fh": ch, "sheets": sheet_files}
    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(manifest, f)
    total = sum(os.path.getsize(os.path.join(outdir, x)) for x in sheet_files)
    print(f"TOTAL sprite bytes: {total//1024} KB")
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
