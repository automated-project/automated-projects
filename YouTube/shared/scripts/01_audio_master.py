#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【共通モジュール①】音源マスタリング & DJクロスフェード結合 (確定統一仕様)
- 全チャンネル共通: 
  - イコライザー(EQ)完全OFF (Zero-EQ原音尊重)
  - LUFS(loudnorm)過度な音圧圧縮の完全不使用・排除
  - ピーク保護: alimiter=limit=0.95:level=disabled のみ適用
  - 曲間: 2.5秒 Equal-Power Crossfade
  - 末尾処理: フェードアウトなし
  - 保存形式: MP3 320kbps 最高品質
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
    全音源トラックを読み込み、タイムスタンプを計算して 2.5s クロスフェード＋Zero-EQ ピーク保護(alimiter 0.95)
    を適用し、末尾フェードアウトなしで MP3 320kbps マスターを出力する。
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

    # FFmpeg concat & crossfade / Peak Limiter (No end fade-out)
    filter_complex = ""
    if len(audio_files) == 1:
        filter_complex = "[0:a]alimiter=limit=0.95:level=disabled[aout]"
    else:
        curr = "0:a"
        for i in range(1, len(audio_files)):
            nxt = f"{i}:a"
            out_lbl = f"a{i}" if i < len(audio_files) - 1 else "afin"
            filter_complex += f"[{curr}][{nxt}]acrossfade=d=2.5:c1=tri:c2=tri[{out_lbl}];"
            curr = out_lbl
        # 末尾 afade を完全除去し、alimiter のみ適用
        filter_complex += f"[afin]alimiter=limit=0.95:level=disabled[aout]"

    cmd_audio = ["ffmpeg", "-y"]
    for trk in audio_files:
        cmd_audio.extend(["-i", str(Path(trk).resolve())])

    cmd_audio.extend([
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "320k",
        str(output_audio_path)
    ])

    print(f"Executing FFmpeg Audio Mastering (Zero-EQ / No Fade-out): {' '.join(cmd_audio)}", flush=True)
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
