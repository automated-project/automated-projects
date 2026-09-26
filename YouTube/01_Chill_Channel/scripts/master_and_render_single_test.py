#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ch1 (Komorebi Chill Audio): 1曲テスト用 マスタリング ＆ ポモドーロタイマー動画レンダラー
1. raw_audio から高音質WAV抽出
2. Warm Analog EQ & -14.0 LUFS ラウドネスノーマライゼーション
3. 画面上部への Futura プログレスバー & カウントダウンタイマーUI描画
4. 1080p MP4動画出力
"""

import os
import sys
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
RAW_INPUT = BASE_DIR / "raw_audio/集中/A_Quiet_Corner_Table.mp4"
MASTERED_DIR = BASE_DIR / "mastered_audio/wav/focus"
OUT_DIR = BASE_DIR / "output_videos"
BG_IMAGE = BASE_DIR / "cover_art/bg_library_study.jpeg"

MASTERED_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

MASTERED_WAV = MASTERED_DIR / "A_Quiet_Corner_Table.wav"
OUT_VIDEO = OUT_DIR / "test_single_pomodoro_track.mp4"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"

def master_audio():
    """Warm Analog EQ & -14.0 LUFS ラウドネスノーマライゼーション"""
    print(f"[+] Mastering raw audio: {RAW_INPUT} -> {MASTERED_WAV}")
    
    # 2-pass/1-pass loudnorm + Warm Vintage EQ
    audio_filter = (
        "highpass=f=35,"
        "equalizer=f=180:width_type=q:w=1.2:g=1.8,"
        "equalizer=f=3200:width_type=q:w=1.0:g=-1.5,"
        "highshelf=f=8500:g=-2.0,"
        "lowpass=f=15000,"
        "loudnorm=I=-14.0:TP=-1.5:LRA=7.0"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(RAW_INPUT),
        "-vn",
        "-af", audio_filter,
        "-ar", "48000",
        "-c:a", "pcm_s24le",
        str(MASTERED_WAV)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Audio Mastered: {MASTERED_WAV}")

def get_duration(file_path):
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)],
        capture_output=True, text=True, check=True
    )
    return float(res.stdout.strip())

def load_font(size, index=4):
    try:
        return ImageFont.truetype(FUTURA_PATH, size, index=index)
    except Exception:
        try:
            return ImageFont.truetype(FUTURA_PATH, size, index=0)
        except Exception:
            return ImageFont.load_default()

def render_video():
    total_sec = get_duration(MASTERED_WAV)
    total_frames = int(total_sec * FPS)
    print(f"[+] Total Duration: {total_sec:.2f}s ({total_frames} frames)")

    # 1. Prepare Base Background Image (1920x1080)
    bg_orig = Image.open(BG_IMAGE).convert("RGBA")
    img_w, img_h = bg_orig.size
    target_ratio = WIDTH / HEIGHT
    cur_ratio = img_w / img_h

    if cur_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        bg_orig = bg_orig.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        bg_orig = bg_orig.crop((0, top, img_w, top + new_h))

    base_bg = bg_orig.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    # 2. Fonts
    font_status = load_font(26, index=4)   # Bold
    font_timer = load_font(34, index=4)    # Bold
    font_sub = load_font(20, index=1)      # Medium

    # 3. FFmpeg Process
    print(f"[+] Starting FFmpeg encoder -> {OUT_VIDEO}")
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(MASTERED_WAV),
        "-c:v", "h264_videotoolbox",
        "-b:v", "3500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        str(OUT_VIDEO)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # UI Geometry parameters (中央集約デザイン・チャンネル名完全排除)
    BAR_W = 600
    BAR_H = 6
    BAR_X = (WIDTH - BAR_W) // 2
    BAR_Y = 85

    for f_idx in range(total_frames):
        cur_sec = f_idx / FPS
        rem_sec = max(0.0, total_sec - cur_sec)

        # Build UI overlay
        ui = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ui)

        # Background subtle top gradient/card
        draw.rectangle([0, 0, WIDTH, 115], fill=(0, 0, 0, 90))

        # Digital Countdown Timer
        m = int(rem_sec) // 60
        s = int(rem_sec) % 60
        timer_str = f"{m:02d}:{s:02d}"

        # 中央ヘッダーテキスト: "STUDY SESSION  •  02:34"
        center_text = f"STUDY SESSION   {timer_str}"
        bbox = font_status.getbbox(center_text)
        text_w = bbox[2] - bbox[0]
        text_x = (WIDTH - text_w) // 2
        draw.text((text_x, 42), center_text, font=font_status, fill=(255, 255, 255, 255))

        # Progress calculation
        progress = cur_sec / total_sec
        fill_w = int(BAR_W * progress)

        # Progress Bar Track & Fill (中央)
        draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + BAR_W, BAR_Y + BAR_H], radius=3, fill=(255, 255, 255, 40))
        if fill_w > 0:
            draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + fill_w, BAR_Y + BAR_H], radius=3, fill=(255, 255, 255, 230))

        # Composite base_bg + ui
        frame = Image.alpha_composite(base_bg, ui)
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ Video Rendered: {OUT_VIDEO} ({total_sec:.2f}s)")

def main():
    print("==================================================")
    print("🚀 CH1 SINGLE TRACK MASTERING & POMODORO TEST")
    print("==================================================")
    master_audio()
    render_video()
    print("\n🎉 ALL DONE!")

if __name__ == "__main__":
    main()
