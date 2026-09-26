# -*- coding: utf-8 -*-
"""
1hour-mix の全28ファイルのメタデータ・長さ・特徴・曲名を精査するスクリプト
"""
import subprocess
import json
from pathlib import Path

mix_dir = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/raw_audio/1hour-mix")
files = sorted([f for f in mix_dir.iterdir() if f.is_file() and f.suffix.lower() == ".mp4"])

print(f"{'#':<3} | {'Filename':<35} | {'Size':<8} | {'Duration'}")
print("-" * 65)

for i, f in enumerate(files, 1):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(f)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    dur_sec = float(res) if res else 0.0
    mins = int(dur_sec // 60)
    secs = int(dur_sec % 60)
    size_mb = f.stat().st_size / (1024 * 1024)
    print(f"{i:<3} | {f.name:<35} | {size_mb:>6.2f}MB | {mins:02d}:{secs:02d} ({dur_sec:.1f}s)")
