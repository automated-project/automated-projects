#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1: Haven Chill Audio - Single Track 4K Video Renderer with Mini Subtle Visualizer
- Background: ch1_bg_new (4K UHD)
- Audio: mastered_audio/wav/Three_AM_Notebook.wav
- Visualizer: Mini subtle rounded bars (Very discreet, minimalist, warm amber-white glow)
- Hardware acceleration: NumPy FFT -> PIL -> Raw RGBA -> FFmpeg h264_videotoolbox
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
BG_PATH = BASE_DIR / "ch1_bg_new/Gemini_Generated_Image_p8bhisp8bhisp8bh.jpeg"
AUDIO_PATH = BASE_DIR / "mastered_audio/wav/Three_AM_Notebook.wav"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP4 = OUTPUT_DIR / "CH1_NEW_BG_SINGLE_TRACK_4K_MINI_VISUALIZER.mp4"

WIDTH = 3840
HEIGHT = 2160
FPS = 30

# Mini Subtle Visualizer Parameters (4K 最適化 ミニマル仕様)
NUM_BARS = 36
BAR_WIDTH = 12
BAR_GAP = 8
MAX_BAR_HEIGHT = 36      # 控えめで上品な最大高
MIN_BAR_HEIGHT = 4       # アイドル時も微かに光る最小高
BOTTOM_MARGIN = 48       # 画面最下部からの余白
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

BAR_COLOR = (255, 245, 230, 210)       # 暖かみのある半透明アンバーホワイト
BAR_GLOW = (255, 230, 190, 80)        # 柔らかな光彩

def main():
    print("==================================================")
    print("🎬 Ch1 4K Single Track Renderer (Mini Visualizer)")
    print(f"🖼️ Background: {BG_PATH.name}")
    print(f"🎵 Audio: {AUDIO_PATH.name}")
    print(f"🎯 Output: {OUT_MP4.name} (4K 3840x2160 @ 30fps)")
    print("==================================================")

    # 1. Load Audio
    with wave.open(str(AUDIO_PATH), 'rb') as wf:
        sr = wf.getframerate()
        n_channels = wf.getnchannels()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)

    if n_channels == 2:
        audio_stereo = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        audio_mono = 0.5 * (audio_stereo[0::2] + audio_stereo[1::2])
    else:
        audio_mono = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    samples_per_frame = sr // FPS
    total_video_frames = len(audio_mono) // samples_per_frame
    total_duration_sec = total_video_frames / FPS
    print(f"📊 Duration: {total_duration_sec/60:.2f} mins ({total_duration_sec:.1f} s), Frames: {total_video_frames}")

    # 2. Prepare 4K Background Image
    print("🖼️ Preparing 4K background image...")
    bg_img = Image.open(BG_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    # 3. Frequency bin calculation
    fft_size = 4096
    freq_bins = np.geomspace(40, 12000, NUM_BARS + 1)
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)

    freq_weights = np.zeros(NUM_BARS)
    for b in range(NUM_BARS):
        f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
        freq_weights[b] = (f_center / 100.0) ** 0.45 * 14.0

    # 4. Start FFmpeg Pipe
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",  # Stdin video stream
        "-i", str(AUDIO_PATH),
        "-c:v", "h264_videotoolbox",
        "-b:v", "9500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        str(OUT_MP4)
    ]

    ffmpeg_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    prev_heights = np.zeros(NUM_BARS)
    hanning_win = np.hanning(fft_size)

    print("🚀 Rendering frames with Mini Visualizer...")

    for f_idx in range(total_video_frames):
        start_sample = f_idx * samples_per_frame
        chunk = audio_mono[start_sample : start_sample + fft_size]
        if len(chunk) < fft_size:
            chunk = np.pad(chunk, (0, fft_size - len(chunk)))

        windowed = chunk * hanning_win
        spectrum = np.abs(np.fft.rfft(windowed)) / (fft_size / 2)

        target_heights = np.zeros(NUM_BARS)
        for b in range(NUM_BARS):
            idx_range = np.where((freqs >= freq_bins[b]) & (freqs < freq_bins[b+1]))[0]
            if len(idx_range) > 0:
                val = np.mean(spectrum[idx_range])
            else:
                closest_idx = np.argmin(np.abs(freqs - (freq_bins[b] + freq_bins[b+1])/2))
                val = spectrum[closest_idx]

            adj = np.clip(val * freq_weights[b], 0.0, 1.0)
            target_heights[b] = MIN_BAR_HEIGHT + adj * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)

        # Smooth Decay (EMA)
        smooth_heights = np.where(target_heights > prev_heights,
                                  target_heights * 0.75 + prev_heights * 0.25,
                                  prev_heights * 0.82 + target_heights * 0.18)
        prev_heights = smooth_heights

        # Draw frame
        frame = bg_img.copy()
        draw = ImageDraw.Draw(frame, "RGBA")

        for b in range(NUM_BARS):
            h = int(smooth_heights[b])
            bx = START_X + b * (BAR_WIDTH + BAR_GAP)
            by_top = BASE_Y - h
            by_bottom = BASE_Y

            # Subtle Outer Glow
            draw.rounded_rectangle(
                [bx - 2, by_top - 2, bx + BAR_WIDTH + 2, by_bottom + 2],
                radius=4,
                fill=BAR_GLOW
            )
            # Solid Core Bar
            draw.rounded_rectangle(
                [bx, by_top, bx + BAR_WIDTH, by_bottom],
                radius=3,
                fill=BAR_COLOR
            )

        ffmpeg_proc.stdin.write(frame.tobytes())

        if f_idx % 300 == 0:
            print(f"  ⏳ Progress: {f_idx}/{total_video_frames} frames ({(f_idx/total_video_frames)*100:.1f}%)", flush=True)

    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()

    print(f"\n🎉 4K VIDEO RENDER COMPLETE: {OUT_MP4}")
    print(f"   Size: {OUT_MP4.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
