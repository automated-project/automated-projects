#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1: Haven Chill Audio - Veo Night Loop 4K Renderer with Ambient Sound Blend (Option A)
- Input Video: cover_art/Young_woman_writing_at_desk_20260923075443.mp4 (10s seamless loop)
- Input Music: mastered_audio/wav/Three_AM_Notebook.wav (Warm Tape Mastered)
- Ambient Audio: Veo native rain/pencil ambient blended subtly at -28dB (Warm tape hiss effect)
- Output: output_videos/CH1_NIGHT_VEO_LOOP_4K_TEST.mp4 (4K UHD 3840x2160, Lanczos)
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
VEO_VIDEO = BASE_DIR / "cover_art/Young_woman_writing_at_desk_20260923075443.mp4"
MUSIC_WAV = BASE_DIR / "mastered_audio/wav/Three_AM_Notebook.wav"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP4 = OUTPUT_DIR / "CH1_NIGHT_VEO_LOOP_4K_TEST.mp4"

WIDTH = 3840
HEIGHT = 2160
FPS = 24

def main():
    print("==================================================")
    print("🎬 Ch1 Veo Night Loop 4K Renderer (Ambient Blend)")
    print(f"🎥 Video Loop: {VEO_VIDEO.name}")
    print(f"🎵 Music Track: {MUSIC_WAV.name}")
    print(f"🎯 Output: {OUT_MP4.name} (4K 3840x2160 @ 24fps)")
    print("==================================================")

    # FFmpeg Filter Graph:
    # 1. Loop Video & Ambient Audio infinitely
    # 2. Scale Video to 4K using high quality Lanczos
    # 3. Blend Music (1.0) and Ambient Sound (-28dB = volume 0.04) without clipping
    filter_complex = (
        "[0:v]scale=3840:2160:flags=lanczos,fps=24[v4k];"
        "[0:a]volume=0.04,aloop=loop=-1:size=2e+09[amb];"
        "[1:a][amb]amix=inputs=2:duration=first:normalize=0[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(VEO_VIDEO),
        "-i", str(MUSIC_WAV),
        "-filter_complex", filter_complex,
        "-map", "[v4k]",
        "-map", "[aout]",
        "-c:v", "h264_videotoolbox",
        "-b:v", "9500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        str(OUT_MP4)
    ]

    print("🚀 Starting 4K Video Encoding with Hardware Acceleration...")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode != 0:
        print("❌ FFmpeg Error:")
        print(res.stderr)
        sys.exit(1)

    print(f"\n🎉 4K TEST VIDEO BUILD COMPLETE!")
    print(f"   Output File: {OUT_MP4}")
    print(f"   Size: {OUT_MP4.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
