#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AuraMelody Audio: 14.86-Second Seamless Loop Shorts Video Renderer (Drop Lead Synth Edition)
- Background: cover_art/bg_summer_edm_shorts.jpeg (1080x1920)
- Audio: Perfect Drop Loop (82.83s - 97.69s, 129.20 BPM 8-bar drop loop with tail wrap)
- Visualizer: 48-Bar Discrete Rounded Bars (Vibrant Cyan Neon) placed in safe-zone (BOTTOM_MARGIN=340)
- Output: output_videos/SHORTS_SUMMER_MELODIC_EDM_LOOP_15S.mp4
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Coding_Synth_Channel")
TRACK1_WAV = CHANNEL_DIR / "output_videos/temp_mix_build/01_Hands_Turn_Slowly_mastered.wav"
BG_IMAGE_PATH = CHANNEL_DIR / "cover_art/bg_summer_edm_shorts.jpeg"
OUT_MP4 = CHANNEL_DIR / "output_videos/SHORTS_SUMMER_MELODIC_EDM_LOOP_15S.mp4"
TEMP_DIR = CHANNEL_DIR / "output_videos/temp_shorts"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
LOOP_WAV = TEMP_DIR / "shorts_melodic_edm_loop_15s.wav"

FPS = 30
WIDTH = 1080
HEIGHT = 1920

# Visualizer Parameters for Vertical 9:16
NUM_BARS = 48
BAR_WIDTH = 12
BAR_GAP = 6
MAX_BAR_HEIGHT = 52
MIN_BAR_HEIGHT = 6
BOTTOM_MARGIN = 340  # Safe zone above Shorts title / sound icon
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

print(f"[+] Loading Audio from: {TRACK1_WAV}")
with wave.open(str(TRACK1_WAV), 'rb') as wf:
    sr = wf.getframerate()
    n_channels = wf.getnchannels()
    raw = wf.readframes(wf.getnframes())

audio = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_channels)

# Exact Zero-cross 8-bar drop extraction (82.8301s - 97.6908s)
zero_cross_start = 3652809
exact_8bars = 655356
zero_cross_end = zero_cross_start + exact_8bars

loop_audio = audio[zero_cross_start:zero_cross_end].copy()

# Tail wrap-around (200ms) for ultra-smooth loop transition
overlap_samples = int(sr * 0.20)
tail = audio[zero_cross_end : zero_cross_end + overlap_samples].astype(np.float32)

loop_f = loop_audio.astype(np.float32)
fade_in = np.linspace(1.0, 0.0, overlap_samples)[:, None]
loop_f[:overlap_samples] += tail * fade_in

# Limit peak
max_val = np.max(np.abs(loop_f))
if max_val > 32700:
    loop_f = loop_f * (32700 / max_val)

perfect_loop = loop_f.astype(np.int16)

with wave.open(str(LOOP_WAV), 'wb') as wf:
    wf.setnchannels(n_channels)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(perfect_loop.tobytes())

duration_sec = len(perfect_loop) / sr
print(f"[+] Saved Perfect Drop Loop WAV: {LOOP_WAV} ({duration_sec:.3f}s)")

# Prepare mono audio for FFT
audio_mono = 0.5 * (perfect_loop[:, 0].astype(np.float32) + perfect_loop[:, 1].astype(np.float32)) / 32768.0

samples_per_frame = sr // FPS
total_video_frames = len(audio_mono) // samples_per_frame
print(f"[+] Total Video Frames: {total_video_frames} ({total_video_frames/FPS:.2f}s)")

# Load & Prepare Vertical Background Image
print(f"[+] Loading Background Image: {BG_IMAGE_PATH}")
bg_img = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# Frequency bin calculation (Pink noise slope compensation)
fft_size = 2048
freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)

freq_weights = np.zeros(NUM_BARS)
for b in range(NUM_BARS):
    f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
    freq_weights[b] = (f_center / 100.0) ** 0.50 * 18.0

# Start FFmpeg process
print(f"[+] Starting FFmpeg process writing to: {OUT_MP4}")
cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",  # Stdin video pipe
    "-i", str(LOOP_WAV),
    "-c:v", "h264_videotoolbox",
    "-b:v", "3000k",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(OUT_MP4)
]

ffmpeg_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

prev_heights = np.zeros(NUM_BARS)
hanning_win = np.hanning(fft_size)

print("[+] Rendering Shorts video frames...")
for f_idx in range(total_video_frames):
    start_sample = f_idx * samples_per_frame
    chunk = audio_mono[start_sample : start_sample + fft_size]
    if len(chunk) < fft_size:
        wrap_needed = fft_size - len(chunk)
        chunk = np.concatenate([chunk, audio_mono[:wrap_needed]])
        
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
        draw.rounded_rectangle([x0, y0, x1, y1], radius=4, fill=(0, 229, 255, 230), outline=(220, 250, 255, 255), width=1)
        
    frame = Image.alpha_composite(frame, overlay)
    ffmpeg_proc.stdin.write(frame.tobytes())

print("[+] Finalizing FFmpeg stream...")
ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()

print(f"[✓] Successfully generated Seamless Loop Shorts Video: {OUT_MP4}")
