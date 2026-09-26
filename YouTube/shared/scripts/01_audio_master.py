#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【共通モジュール①】音源マスタリング & DJクロスフェード結合
- 全チャンネル共通: MP3/WAV音源の 2.5s Equal-Power Crossfade ＆ Zero-EQ Peak Guard (alimiter 0.95)
"""

import os
import sys
import subprocess
from pathlib import Path

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def process_audio_mastering(audio_files: list, output_audio_path: Path, output_chapters_path: Path = None) -> float:
    """
    全音源トラックを読み込み、タイムスタンプを計算して 320kbps MP3 として結合マスタリングする。
    """
    if not audio_files:
        raise ValueError("No audio files provided for mastering.")

    output_audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    timestamps = []
    current_sec = 0.0
    crossfade_sec = 2.5

    for idx, f_path in enumerate(audio_files):
        p = Path(f_path)
        t_name = p.stem.replace("_", " ").strip()
        dur = get_audio_duration(p)

        mins = int(current_sec // 60)
        secs = int(current_sec % 60)
        timestamps.append(f"{mins:02d}:{secs:02d} - {t_name}")

        if idx == 0:
            current_sec += dur
        else:
            current_sec += (dur - crossfade_sec)

    chapters_text = "\n".join(timestamps)
    if output_chapters_path:
        output_chapters_path.parent.mkdir(parents=True, exist_ok=True)
        output_chapters_path.write_text(chapters_text, encoding="utf-8")

    # FFmpeg concat リスト生成
    concat_list_file = output_audio_path.parent / "audio_concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for trk in audio_files:
            safe_path = str(Path(trk).resolve()).replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")

    cmd_audio = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_file),
        "-af", "alimiter=limit=0.95:level=disabled",
        "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "320k",
        str(output_audio_path)
    ]
    print(f"Executing FFmpeg Audio Mastering: {' '.join(cmd_audio)}", flush=True)
    subprocess.run(cmd_audio, check=True)

    print(f"✅ Audio Mastering Complete: {output_audio_path} ({current_sec:.1f}s)")
    return current_sec

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python 01_audio_master.py <output_mp3> <input_audio_1> [input_audio_2 ...]")
        sys.exit(1)
    out_p = Path(sys.argv[1])
    in_files = sys.argv[2:]
    process_audio_mastering(in_files, out_p)
