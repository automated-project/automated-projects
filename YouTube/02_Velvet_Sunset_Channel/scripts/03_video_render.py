#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【Ch2 固有モジュール③】Velvet Sunset Audio 4K動画レンダリングエンジン (確定統一仕様)
- 解像度: 3840x2160 (4K UHD), 30fps, Bitrate: 9500k (H.264 / AAC 320k)
- 波形演出: 画面左下 (x=150, y=2050) BPM同期 Center-Mirrored 3-Bar Visualizer
"""

import os
import sys
import subprocess
from pathlib import Path

YOUTUBE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(YOUTUBE_ROOT))

from shared.scripts.visualizer_engine import BottomLeftBpmVisualizer

def render_ch2_video(
    thumb_path: Path,
    audio_path: Path,
    output_video_path: Path,
    bpm: float = 102.0,
    use_cloud_encoder: bool = False
) -> Path:
    output_video_path.parent.mkdir(parents=True, exist_ok=True)

    encoder = "libx264" if use_cloud_encoder or os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true" else "h264_videotoolbox"
    b_rate = "9500k"

    print(f"🎬 [Ch2 Video Render] Engine: {encoder} | 4K UHD 30fps | Audio: {audio_path.name}")
    print(f"📌 Visualizer: Bottom-Left BPM-Synced 3-Bar (x=150, y=2050, BPM={bpm})")

    # 静止画 ＋ オーディオ 4K レンダリング
    cmd_video = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(thumb_path),
        "-i", str(audio_path),
        "-c:v", encoder, "-b:v", b_rate,
        "-vf", "scale=3840:2160:flags=lanczos,format=yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-shortest",
        str(output_video_path)
    ]

    print(f"Executing: {' '.join(cmd_video)}", flush=True)
    subprocess.run(cmd_video, check=True)
    print(f"✅ Ch2 4K Video Render Complete: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    print("Ch2 Video Render Engine Standalone Mode")
