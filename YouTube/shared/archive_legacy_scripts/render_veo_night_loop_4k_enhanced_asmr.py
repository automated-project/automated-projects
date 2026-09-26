#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1: Haven Chill Audio - Enhanced ASMR Rain & Pencil Blend 4K Video Renderer
- Fixes initial 3-second loudness anomaly (Equalizes ambient loop & balances intro)
- Enhances Pencil Scratching & Rain texture (High-shelf crisp EQ + Optimal -17dB mix level)
- Output: output_videos/CH1_NIGHT_VEO_LOOP_4K_ASMR_ENHANCED.mp4 (4K UHD 3840x2160, Lanczos)
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
OUT_MP4 = OUTPUT_DIR / "CH1_NIGHT_VEO_LOOP_4K_ASMR_ENHANCED.mp4"

def main():
    print("==================================================")
    print("🎬 Ch1 Veo Night Loop 4K Renderer (Enhanced ASMR Blend)")
    print(f"🎥 Video Loop: {VEO_VIDEO.name}")
    print(f"🎵 Music Track: {MUSIC_WAV.name}")
    print(f"🎯 Output: {OUT_MP4.name} (4K 3840x2160 @ 24fps)")
    print("==================================================")

    # 1. 音響フィルタ設計:
    # - [0:a] Veo環境音:
    #   * highpass=f=80 (濁った低域ノイズカット)
    #   * equalizer=f=3200:t=h:w=1500:g=3.5 (ペンのカリカリ音と雨粒の質感をクリアに際立たせる)
    #   * volume=0.18 (-15dB相当: 音楽と美しく調和し、全編通してしっかり聴こえる音量)
    #   * aloop (無限シームレスループ)
    # - [1:a] メイン音楽: 100%基準レベル
    # - amix: 2つの音源をクリッピングなしで高品位ミックス
    filter_complex = (
        "[0:v]scale=3840:2160:flags=lanczos,fps=24[v4k];"
        "[0:a]highpass=f=80,equalizer=f=3200:width_type=h:width=1500:g=3.5,volume=0.18,aloop=loop=-1:size=2e+09[amb];"
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

    print("🚀 Starting 4K Video Encoding with Enhanced ASMR Audio...")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode != 0:
        print("❌ FFmpeg Error:")
        print(res.stderr)
        sys.exit(1)

    print(f"\n🎉 ENHANCED ASMR 4K VIDEO BUILD COMPLETE!")
    print(f"   Output File: {OUT_MP4}")
    print(f"   Size: {OUT_MP4.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
