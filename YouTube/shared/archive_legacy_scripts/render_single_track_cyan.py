#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cyberpunk / Synthwave 1曲プレビュー動画生成スクリプト
水色（Cyan / Neon Blue）48本独立丸角カプセル波形ビジュアライザー
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Coding_Synth_Channel")
AUDIO_SRC_MP3 = Path("/Users/base/Automated-Projects/Store-Assets/game_music_store/tracks/2026-09-08/Track02_Neon_Overdrive/lyria_cyberpunk_track.mp3")
AUDIO_WAV = CHANNEL_DIR / "output_videos/temp_single_track.wav"
BG_IMAGE_PATH = CHANNEL_DIR / "cover_art/sample_cyber_bg.jpg"
OUT_MP4 = CHANNEL_DIR / "output_videos/CYBERPUNK_SINGLE_TRACK_CYAN_PREVIEW.mp4"
OUT_MP4.parent.mkdir(parents=True, exist_ok=True)

# 1. MP3 -> 44.1kHz 16-bit WAVに高速変換
print(f"[+] Converting {AUDIO_SRC_MP3.name} to WAV...")
subprocess.run([
    "ffmpeg", "-y", "-i", str(AUDIO_SRC_MP3),
    "-ar", "44100", "-ac", "2", "-sample_fmt", "s16",
    str(AUDIO_WAV)
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

FPS = 30
WIDTH = 1920
HEIGHT = 1080

# 2. 波形ビジュアライザーパラメータ (水色ネオン仕様)
NUM_BARS = 48
BAR_WIDTH = 18
BAR_GAP = 10
MAX_BAR_HEIGHT = 52
MIN_BAR_HEIGHT = 6
BOTTOM_MARGIN = 24
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

# 水色（Cyan / Electric Icy Blue）カラー
FILL_COLOR = (0, 229, 255, 230)      # 鮮やかな水色・ネオンシアン (RGBA)
OUTLINE_COLOR = (165, 243, 252, 200)  # 淡いアイシーブルーの輪郭光

print(f"[+] Loading Audio: {AUDIO_WAV}")
with wave.open(str(AUDIO_WAV), 'rb') as wf:
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
print(f"[+] Video length: {total_duration_sec:.1f}s ({total_video_frames} frames)")

# 3. 背景画像読み込み
bg_img = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# 4. 周波数ビン分割 & ピンクノイズスロープ補正
fft_size = 4096
freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)

freq_weights = np.zeros(NUM_BARS)
for b in range(NUM_BARS):
    f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
    freq_weights[b] = (f_center / 100.0) ** 0.52 * 19.0

# 5. FFmpegパイプライン起動 (Mac VideoToolbox)
cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",
    "-i", str(AUDIO_WAV),
    "-c:v", "h264_videotoolbox",
    "-b:v", "1500k",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(OUT_MP4)
]

ffmpeg_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

prev_heights = np.zeros(NUM_BARS)
hanning_win = np.hanning(fft_size)

print("[+] Rendering Cyberpunk Cyan Visualizer frames...")

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
        target_heights[b] = MIN_BAR_HEIGHT + (adj ** 0.85) * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)
            
    # Dynamic Gravity Smoothing (アタック即応 + 0.82減衰)
    smooth_heights = np.zeros(NUM_BARS)
    for b in range(NUM_BARS):
        if target_heights[b] >= prev_heights[b]:
            smooth_heights[b] = target_heights[b]
        else:
            smooth_heights[b] = max(MIN_BAR_HEIGHT, prev_heights[b] * 0.82)
    prev_heights = smooth_heights
    
    frame = bg_img.copy()
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for b in range(NUM_BARS):
        h = int(smooth_heights[b])
        x0 = START_X + b * (BAR_WIDTH + BAR_GAP)
        x1 = x0 + BAR_WIDTH
        y1 = BASE_Y
        y0 = BASE_Y - h
        draw.rounded_rectangle([x0, y0, x1, y1], radius=5, fill=FILL_COLOR, outline=OUTLINE_COLOR, width=1)
        
    frame = Image.alpha_composite(frame, overlay)
    ffmpeg_proc.stdin.write(frame.tobytes())
    
    if f_idx % 300 == 0:
        pct = (f_idx / total_video_frames) * 100.0
        print(f"  Frame {f_idx}/{total_video_frames} ({pct:.1f}%)")

ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()

if AUDIO_WAV.exists():
    AUDIO_WAV.unlink()

print(f"✅ Successfully rendered Cyan Preview Video: {OUT_MP4}")
