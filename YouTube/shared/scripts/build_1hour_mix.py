#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
build_1hour_mix.py
-------------------------------------------------------------------------------
各チャンネル共通の「1 Hour Seamless Mix 動画 & タイムスタンプ自動生成スクリプト」

【動作仕様】
1. 指定チャンネルの raw_audio/ 内にある全楽曲（mp4/mp3）を自動検出（主観選別なしですべて投入）。
2. 各楽曲のカバーアートを抽出し、決定仕様の「ソフト・アンビエントブラー（16:9）」フレームを生成。
3. 高速かつ極小ファイルサイズ（h264_videotoolbox / 15fps）で各曲クリップをエンコード。
4. ffmpeg concat で無劣化結合し、1時間前後の超軽量ロング動画を出力。
5. 概要欄にそのまま貼れるタイムスタンプ付きトラックリスト（チャプター）を自動出力。
-------------------------------------------------------------------------------
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageFilter

def format_seconds(sec: float) -> str:
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m}:{s:02d}"

def get_media_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def extract_raw_art(media_path: Path, out_path: Path):
    cmd = ["ffmpeg", "-y", "-ss", "00:00:02", "-i", str(media_path), "-frames:v", "1", str(out_path)]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_ambient_frame(art_path: Path, out_path: Path):
    """
    決定仕様：ソフト・アンビエントブラー
    - 背景: 元画像を1920x1080に拡大 + GaussianBlur(50) + 80%暗黒オーバーレイ
    - 中央: 元画像（1080x1080）をアスペクト比維持で配置
    """
    raw_img = Image.open(art_path).convert("RGBA")
    
    bg_img = raw_img.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(50))
    dark_overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, int(255 * 0.8)))
    bg_img = Image.alpha_composite(bg_img, dark_overlay)
    
    fg_size = 1080
    fg_img = raw_img.resize((fg_size, fg_size), Image.Resampling.LANCZOS)
    
    x_offset = (1920 - fg_size) // 2
    y_offset = (1080 - fg_size) // 2
    
    bg_img.paste(fg_img, (x_offset, y_offset), fg_img)
    bg_img.convert("RGB").save(out_path, "JPEG", quality=95)

def build_channel_mix(channel_dir: Path, output_name: str = "1hour_mix"):
    raw_dir = channel_dir / "raw_audio"
    out_dir = channel_dir / "output_videos"
    out_dir.mkdir(exist_ok=True, parents=True)
    temp_dir = out_dir / "temp_build"
    temp_dir.mkdir(exist_ok=True, parents=True)
    
    audio_files = sorted(list(raw_dir.glob("*.mp4")) + list(raw_dir.glob("*.mp3")))
    if not audio_files:
        print(f"[-] No audio files found in {raw_dir}")
        return
        
    print(f"[+] Found {len(audio_files)} tracks in {channel_dir.name}")
    
    concat_list_file = temp_dir / "concat_list.txt"
    chapters_file = out_dir / f"{output_name}_chapters.txt"
    final_video = out_dir / f"{output_name}.mp4"
    
    current_time = 0.0
    chapter_lines = []
    concat_entries = []
    
    for idx, media_path in enumerate(audio_files):
        track_title = media_path.stem.replace("_", " ").title()
        duration = get_media_duration(media_path)
        
        ts = format_seconds(current_time)
        chapter_lines.append(f"{ts} - {track_title}")
        
        art_jpg = temp_dir / f"art_{idx:03d}.jpg"
        frame_jpg = temp_dir / f"frame_{idx:03d}.jpg"
        clip_mp4 = temp_dir / f"clip_{idx:03d}.mp4"
        
        extract_raw_art(media_path, art_jpg)
        generate_ambient_frame(art_jpg, frame_jpg)
        
        # 15fps, videotoolbox hardware acceleration
        cmd_clip = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(frame_jpg),
            "-i", str(media_path),
            "-c:v", "h264_videotoolbox", "-b:v", "2000k", "-r", "15", "-pix_fmt", "yuv420p",
            "-af", f"afade=t=in:ss=0:d=1.5,afade=t=out:st={duration-1.5:.2f}:d=1.5",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(clip_mp4)
        ]
        subprocess.run(cmd_clip, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        concat_entries.append(f"file '{clip_mp4.resolve()}'")
        current_time += duration
        print(f"  [{idx+1}/{len(audio_files)}] Rendered: {track_title} ({duration:.1f}s)")
        
    # Write concat list
    with open(concat_list_file, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_entries) + "\n")
        
    # Write chapters
    with open(chapters_file, "w", encoding="utf-8") as f:
        f.write("\n".join(chapter_lines) + "\n")
        
    print(f"[+] Concatenating into final 1-hour video: {final_video}")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(final_video)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[✓] Complete! Total duration: {format_seconds(current_time)}")
    print(f"[✓] Video: {final_video}")
    print(f"[✓] Chapters: {chapters_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build 1-Hour Mix Video for YouTube Channel")
    parser.add_argument("--channel", required=True, help="Path to channel directory (e.g. YouTube/01_Dark_Fantasy_Channel)")
    parser.add_argument("--name", default="1hour_mix", help="Output filename prefix")
    args = parser.parse_args()
    
    build_channel_mix(Path(args.channel), args.name)
