# -*- coding: utf-8 -*-
"""
各トラックの冒頭・サビ等の特徴を把握するためのスクリプト
"""
import subprocess
from pathlib import Path

mix_dir = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/raw_audio/1hour-mix")
files = sorted([f for f in mix_dir.iterdir() if f.is_file() and f.suffix.lower() == ".mp4"])

for f in files:
    # Get volume stats to see loudness
    cmd = [
        "ffmpeg", "-i", str(f), "-af", "volumedetect", "-vn", "-sn", "-dn",
        "-f", "null", "/dev/null"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True).stderr
    mean_vol = ""
    max_vol = ""
    for line in res.split("\n"):
        if "mean_volume:" in line:
            mean_vol = line.strip()
        if "max_volume:" in line:
            max_vol = line.strip()
    print(f"{f.name:<32} | {mean_vol} | {max_vol}")
