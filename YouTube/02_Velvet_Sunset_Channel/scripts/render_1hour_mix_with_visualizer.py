#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PhonkForge Audio: 1-Hour Long Mix Video Renderer with Discrete Rounded Bars Visualizer
- Input: full_seamless_dj_mix.wav (Super Crisp mastered 22 tracks, DJ crossfade)
- Cover Art: Gemini_Generated_Image_gzzyqfgzzyqfgzzy.jpeg
- Output: 1HOUR_SUPER_CRISP_GYM_PHONK_VOL1_OFFICIAL.mp4
- Hardware accelerated video pipeline: PIL -> Raw YUV -> ffmpeg h264_videotoolbox
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel")
AUDIO_WAV = CHANNEL_DIR / "output_videos/temp_dj_mix_build/full_seamless_dj_mix.wav"
BG_IMAGE_PATH = CHANNEL_DIR / "cover_art/bg_highway_crimson.jpeg"
OUT_MP4 = CHANNEL_DIR / "output_videos/1HOUR_AGGRESSIVE_GYM_PHONK_VOL1_CRIMSON.mp4"

FPS = 30
WIDTH = 1920
HEIGHT = 1080

# Visualizer Parameters
NUM_BARS = 48
BAR_WIDTH = 18
BAR_GAP = 10
MAX_BAR_HEIGHT = 52
MIN_BAR_HEIGHT = 6
BOTTOM_MARGIN = 24
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

print(f"[+] Loading Audio: {AUDIO_WAV}")
with wave.open(str(AUDIO_WAV), 'rb') as wf:
    sr = wf.getframerate()
    n_channels = wf.getnchannels()
    n_frames = wf.getnframes()
    raw_bytes = wf.readframes(n_frames)
    
print(f"    Sample rate: {sr} Hz, Channels: {n_channels}, Total samples: {n_frames}")

if n_channels == 2:
    # Interleaved stereo to mono
    audio_stereo = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    audio_mono = 0.5 * (audio_stereo[0::2] + audio_stereo[1::2])
else:
    audio_mono = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0

samples_per_frame = sr // FPS
total_video_frames = len(audio_mono) // samples_per_frame
total_duration_sec = total_video_frames / FPS
print(f"[+] Total Video Frames: {total_video_frames} ({total_duration_sec/60:.2f} mins / {total_duration_sec:.1f} s)")

# Prepare Background Image
print(f"[+] Loading Background Image: {BG_IMAGE_PATH}")
bg_img = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# Frequency bin calculation (Pink noise slope compensation)
fft_size = 4096
freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)

freq_weights = np.zeros(NUM_BARS)
for b in range(NUM_BARS):
    f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
    freq_weights[b] = (f_center / 100.0) ** 0.52 * 19.0

# Start FFmpeg pipe process
print(f"[+] Starting FFmpeg process writing to: {OUT_MP4}")
cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",  # Stdin video pipe
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

print("[+] Rendering and streaming video frames to FFmpeg pipe...")

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
            
    # Dynamic Gravity Smoothing
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
        draw.rounded_rectangle([x0, y0, x1, y1], radius=5, fill=(255, 255, 255, 220), outline=(255, 255, 255, 255), width=1)
        
    frame = Image.alpha_composite(frame, overlay)
    
    # Write RGBA bytes directly to stdin
    ffmpeg_proc.stdin.write(frame.tobytes())
    
    if f_idx % 1800 == 0:
        pct = (f_idx / total_video_frames) * 100.0
        elapsed_min = (f_idx / FPS) / 60.0
        print(f"  [Frame {f_idx}/{total_video_frames}] ({pct:.1f}%) - {elapsed_min:.1f}m rendered")

print("[+] Finalizing FFmpeg stream...")
ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()

print(f"[✓] Successfully generated 1-Hour Mix Video: {OUT_MP4}")
