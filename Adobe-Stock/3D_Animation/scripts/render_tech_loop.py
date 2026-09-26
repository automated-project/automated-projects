#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
3D Tech Data Grid 4K 完全シームレスループ動画 レンダリング＆提出パッケージ作成
"""

import os
import sys
import subprocess
import csv
from pathlib import Path

BLEND_FILE = "/Users/base/Automated-Projects/Adobe-Stock/3D_Animation/blender_projects/tech_data_grid_wave_4k.blend"
OUTPUT_DIR = Path("/Users/base/Automated-Projects/Adobe-Stock/3D_Animation/renders")
FRAMES_DIR = OUTPUT_DIR / "tech_frames"
FINAL_VIDEO = OUTPUT_DIR / "tech_cyber_data_grid_4k_loop.mp4"
CSV_FILE = OUTPUT_DIR / "adobe_stock_3d_tech_submission.csv"

def render_frames():
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    print("🎬 Starting 4K 60fps Frame Rendering (EEVEE)...")
    
    cmd = [
        "/opt/homebrew/bin/blender",
        "-b", BLEND_FILE,
        "-o", str(FRAMES_DIR / "frame_####"),
        "-s", "1",
        "-e", "240",
        "-a"
    ]
    
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("❌ Blender rendering failed.")
        sys.exit(1)
    print("✅ All frames rendered successfully!")

def encode_seamless_mp4():
    print("🎥 Encoding Seamless 4K 60fps Commercial MP4 (-an)...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "60",
        "-i", str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v", "libx264",
        "-crf", "16",
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-an",
        "-movflags", "+faststart",
        str(FINAL_VIDEO)
    ]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("❌ ffmpeg encoding failed.")
        sys.exit(1)
    print(f"✅ Final Commercial Stock Video Created: {FINAL_VIDEO}")

def generate_csv_metadata():
    print("📄 Generating Adobe Stock Submission CSV Metadata...")
    headers = ["Filename", "Title", "Keywords", "Category"]
    row = [
        FINAL_VIDEO.name,
        "3D Cyber Data Grid Wave and Glowing Neural Network Nodes Seamless Loop",
        "cyberpunk, data grid, technology background, 3d wave, digital transformation, network nodes, big data, abstract background, ai tech, cloud computing, server room, 4k commercial, seamless loop, negative space, copy space",
        3
    ]
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)
    print(f"✅ Metadata CSV Saved: {CSV_FILE}")

def main():
    render_frames()
    encode_seamless_mp4()
    generate_csv_metadata()
    print("\n==================================================")
    print(f"🎉 3D動画素材（テクノロジー・DX系）の完成！")
    print(f"動画ファイル: {FINAL_VIDEO}")
    print(f"CSVメタデータ: {CSV_FILE}")
    print("==================================================")

if __name__ == "__main__":
    main()
