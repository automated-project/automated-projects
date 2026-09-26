#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PhonkForge Audio: 3本連続Shorts動画ジェネレーター
- 秒数固定を撤廃し、楽曲ごとのピークドロップ（最も盛り上がる区間）をフレーズ単位で自然に切り出し
- 3つの独自背景（地下ジム、サイバー雨路地、ダークコンバット）を完全適用
- 48本独立丸角バー（純白・ルミナスホワイト）波形ビジュアライザー（Shorts UI安全領域対応）
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel")
WAV_DIR = CHANNEL_DIR / "extracted_audio/wav"
COVER_DIR = CHANNEL_DIR / "cover_art"
OUT_DIR = CHANNEL_DIR / "output_videos"
TEMP_DIR = OUT_DIR / "temp_shorts"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

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

SHORTS_SPECS = [
    {
        "id": "01_gym",
        "track_name": "Heavy_Steel_Rain.wav",
        "bg_name": "bg_gym_shorts.jpeg",
        "start_sec": 73.115,
        "end_sec": 94.000,
        "out_file": "SHORTS_01_HEAVY_STEEL_GYM.mp4",
        "title_ja": "⚡【超重低音】筋トレ用 限界突破ドロップ #Shorts #筋トレ #作業用BGM",
        "title_en": "⚡ Heavy Steel Drop | Extreme Bass Gym Motivation #Shorts #Gym"
    },
    {
        "id": "02_cyberpunk_rain",
        "track_name": "Midnight_Velocity.wav",
        "bg_name": "bg_cyberpunk_rain_shorts.jpeg",
        "start_sec": 64.334,
        "end_sec": 88.000,
        "out_file": "SHORTS_02_MIDNIGHT_VELOCITY_RAIN.mp4",
        "title_ja": "⚡【超重低音】深夜の集中・ゾーン突入ドロップ #Shorts #夜作業 #作業用BGM",
        "title_en": "⚡ Midnight Rain Drop | Cyber Heavy Bass #Shorts #Focus"
    },
    {
        "id": "03_dark_combat",
        "track_name": "Concrete_Predator.wav",
        "bg_name": "bg_dark_combat_shorts.jpeg",
        "start_sec": 64.084,
        "end_sec": 88.000,
        "out_file": "SHORTS_03_CONCRETE_PREDATOR_COMBAT.mp4",
        "title_ja": "⚡【超重低音】テンション爆上げ アグレッシブドロップ #Shorts #ワークアウト #重低音",
        "title_en": "⚡ Predator Strike Drop | Raw Aggressive Bass #Shorts #Workout"
    }
]

def render_shorts_video(spec):
    print(f"\n==================================================")
    print(f"▶ RENDERING SHORTS: {spec['id']} ({spec['track_name']})")
    print(f"==================================================")
    
    track_path = WAV_DIR / spec["track_name"]
    bg_path = COVER_DIR / spec["bg_name"]
    out_path = OUT_DIR / spec["out_file"]
    hook_wav = TEMP_DIR / f"hook_{spec['id']}.wav"
    
    # 1. Load Audio and extract exact drop phrase
    print(f"[+] Loading Audio: {track_path}")
    with wave.open(str(track_path), 'rb') as wf:
        sr = wf.getframerate()
        n_channels = wf.getnchannels()
        raw = wf.readframes(wf.getnframes())
    
    audio = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_channels)
    s_idx = int(spec["start_sec"] * sr)
    e_idx = int(spec["end_sec"] * sr)
    hook_audio = audio[s_idx:e_idx].copy()
    
    # Natural clean ending fade (last 0.25s)
    fade_out_samples = int(sr * 0.25)
    fo = np.linspace(1.0, 0.0, fade_out_samples)[:, None]
    hook_audio[-fade_out_samples:] = (hook_audio[-fade_out_samples:].astype(np.float32) * fo).astype(np.int16)
    
    with wave.open(str(hook_wav), 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(hook_audio.tobytes())
        
    duration_sec = len(hook_audio) / sr
    print(f"[+] Saved Drop Phrase WAV: {hook_wav} ({duration_sec:.2f}s)")
    
    # Mono audio for FFT
    audio_mono = 0.5 * (hook_audio[:, 0].astype(np.float32) + hook_audio[:, 1].astype(np.float32)) / 32768.0
    samples_per_frame = sr // FPS
    total_video_frames = len(audio_mono) // samples_per_frame
    print(f"[+] Total Frames: {total_video_frames} ({total_video_frames/FPS:.2f}s)")
    
    # 2. Prepare Background Image (Crop/Resize to 1080x1920)
    print(f"[+] Loading Background Image: {bg_path}")
    orig_bg = Image.open(bg_path).convert("RGBA")
    
    # Center crop / resize to 9:16
    img_w, img_h = orig_bg.size
    target_ratio = WIDTH / HEIGHT
    current_ratio = img_w / img_h
    
    if current_ratio > target_ratio:
        # Image is wider -> crop width
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        orig_bg = orig_bg.crop((left, 0, left + new_w, img_h))
    else:
        # Image is taller -> crop height
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        orig_bg = orig_bg.crop((0, top, img_w, top + new_h))
        
    bg_img = orig_bg.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    # 3. Frequency bin calculation
    fft_size = 2048
    freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)
    
    freq_weights = np.zeros(NUM_BARS)
    for b in range(NUM_BARS):
        f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
        freq_weights[b] = (f_center / 100.0) ** 0.50 * 18.0
        
    # 4. Start FFmpeg process
    print(f"[+] Starting FFmpeg hardware encoder for: {out_path}")
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",  # Stdin video pipe
        "-i", str(hook_wav),
        "-c:v", "h264_videotoolbox",
        "-b:v", "3500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_path)
    ]
    
    ffmpeg_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    prev_heights = np.zeros(NUM_BARS)
    hanning_win = np.hanning(fft_size)
    
    # Base background base copy
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
                
        # Gravity Smoothing
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
            draw.rounded_rectangle([x0, y0, x1, y1], radius=4, fill=(255, 255, 255, 220), outline=(255, 255, 255, 255), width=1)
            
        frame = Image.alpha_composite(frame, overlay)
        ffmpeg_proc.stdin.write(frame.tobytes())
        
    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()
    print(f"✅ Generated: {out_path} ({duration_sec:.2f}s)")

def main():
    print("=== STARTING BATCH RENDERING OF 3 DIVERSE SHORTS ===")
    for spec in SHORTS_SPECS:
        render_shorts_video(spec)
    print("\n🎉 ALL 3 SHORTS VIDEOS RENDERED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
