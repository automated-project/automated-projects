# -*- coding: utf-8 -*-
"""
Ch 2 の全54ファイルの曲名・長さ・カテゴリを詳細出力するスクリプト
"""
import subprocess
from pathlib import Path

raw_dir = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel/raw_audio")
files = sorted([f for f in raw_dir.glob("**/*") if f.is_file() and f.suffix.lower() == ".mp4"])

print(f"{'#':<3} | {'Path':<40} | {'Duration'}")
print("-" * 60)

for i, f in enumerate(files, 1):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(f)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    dur_sec = float(res) if res else 0.0
    mins = int(dur_sec // 60)
    secs = int(dur_sec % 60)
    rel = str(f.relative_to(raw_dir))
    print(f"{i:<3} | {rel:<40} | {mins:02d}:{secs:02d} ({dur_sec:.1f}s)")
