#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1: ジブリ風 ノスタルジックLofi 1時間完全版Mix動画レンダリングスクリプト（1曲目雷カット修正版）
- 映像: 波形なし・文字なしの静止画アート（1920x1080）
- 音響: Lofi専用ウォームマスタリング（-14 LUFS / 温かいテープEQ / 2.5sクロスフェード）
- 1曲目（Coffee_by_the_Window）: 冒頭9.8秒の雷鳴ノイズを完全カットしてフェードインスタート
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Dark_Fantasy_Channel")
AUDIO_DIR = CHANNEL_DIR / "Lofi-Mix"
BG_IMAGE = CHANNEL_DIR / "cover_art/Gemini_Generated_Image_xaosvnxaosvnxaos.jpeg"
OUT_DIR = CHANNEL_DIR / "output_videos"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUT_DIR / "temp_lofi_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUT_DIR / "1HOUR_GHIBLI_NOSTALGIC_LOFI_VOL1.mp4"
CHAPTERS_FILE = OUT_DIR / "1HOUR_GHIBLI_NOSTALGIC_LOFI_VOL1_chapters.txt"

def format_seconds(sec: float) -> str:
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m:02d}:{s:02d}"

def get_media_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def main():
    print("=== Starting 1-Hour Ghibli Nostalgic Lofi Mix Video Build (Track 1 Fixed) ===")
    
    # 1. 1920x1080 背景画像（波形・文字なし）の準備
    bg_1080p = TEMP_DIR / "bg_1080p.jpg"
    img = Image.open(BG_IMAGE).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
    img.save(bg_1080p, quality=95)
    print(f"[+] Prepared 1080p pure static background: {bg_1080p}")
    
    # 2. 音源リストの取得
    audio_files = sorted(list(AUDIO_DIR.glob("*.mp4")) + list(AUDIO_DIR.glob("*.mp3")))
    print(f"[+] Found {len(audio_files)} tracks in {AUDIO_DIR.name}")
    
    # Lofi Warm Mastering Filter Chain
    af_chain = (
        "highpass=f=35,"
        "equalizer=f=180:t=q:w=1.2:g=1.8,"
        "equalizer=f=8500:t=q:w=1.0:g=-1.8,"
        "lowpass=f=15000,"
        "loudnorm=I=-14.0:TP=-1.5:LRA=11"
    )
    
    current_time = 0.0
    chapter_lines = []
    clip_entries = []
    
    for idx, audio_path in enumerate(audio_files):
        track_title = audio_path.stem.replace("_", " ").title()
        raw_duration = get_media_duration(audio_path)
        
        # 1曲目（Coffee by the Window）は9.8秒〜開始
        start_offset = 9.8 if idx == 0 else 0.0
        duration = raw_duration - start_offset
        
        ts = format_seconds(current_time)
        chapter_lines.append(f"{ts} - {track_title}")
        
        clip_path = TEMP_DIR / f"clip_{idx:03d}.mp4"
        print(f"  [{idx+1}/{len(audio_files)}] Mastering & rendering: {track_title} (Start: {start_offset}s, Dur: {duration:.1f}s)...")
        
        cmd_clip = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(bg_1080p)
        ]
        if start_offset > 0:
            cmd_clip.extend(["-ss", f"{start_offset:.2f}"])
        cmd_clip.extend([
            "-i", str(audio_path),
            "-af", f"{af_chain},afade=t=in:ss=0:d=1.5,afade=t=out:st={duration-1.5:.2f}:d=1.5",
            "-c:v", "h264_videotoolbox", "-b:v", "2500k", "-r", "30", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "320k",
            "-shortest",
            str(clip_path)
        ])
        subprocess.run(cmd_clip, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        clip_entries.append(f"file '{clip_path.resolve()}'")
        current_time += duration
        
    # Concatリスト作成
    concat_list_file = TEMP_DIR / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        f.write("\n".join(clip_entries) + "\n")
        
    # チャプターファイル作成
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(chapter_lines) + "\n")
        
    print(f"\n[+] Concatenating all 21 tracks into full 1-hour video: {OUT_VIDEO}...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(OUT_VIDEO)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    total_mins = current_time / 60.0
    print("==================================================")
    print(f"✅ Render Complete!")
    print(f"   Output Video: {OUT_VIDEO}")
    print(f"   Duration: {format_seconds(current_time)} ({total_mins:.1f} mins)")
    print(f"   Chapters: {CHAPTERS_FILE}")
    print("==================================================")

if __name__ == "__main__":
    main()
