#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【Ch2 固有モジュール③】Velvet Sunset Audio 4K動画レンダリングエンジン
- サンセットオレンジ極細波形演出および 4K (3840x2160) Lanczos レンダリング
"""

import os
import sys
import subprocess
from pathlib import Path

def render_ch2_video(
    thumb_path: Path,
    audio_path: Path,
    output_video_path: Path,
    use_cloud_encoder: bool = False
) -> Path:
    output_video_path.parent.mkdir(parents=True, exist_ok=True)

    encoder = "libx264" if use_cloud_encoder or os.getenv("GITHUB_ACTIONS") == "true" else "h264_videotoolbox"
    b_rate = "9500k"

    print(f"🎬 [Ch2 Video Render] Engine: {encoder} | Input Audio: {audio_path.name}")

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
