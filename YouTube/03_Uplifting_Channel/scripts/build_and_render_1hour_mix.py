#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第3チャンネル（綺麗系Melodic EDM）1時間長尺Mix公式動画自動生成パイプライン (全21曲・60分超完全版)
- Super Crisp Vocal & Summer EDM V-Shape マスタリング
- 2.5秒DJシームレスクロスフェード結合
- 48本水色ネオン波形ビジュアライザー描画
- Mac VideoToolbox高速ハードウェアエンコード
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Coding_Synth_Channel")
RAW_AUDIO_DIR = CHANNEL_DIR / "raw_audio/1hour-mix"
BG_IMAGE_PATH = CHANNEL_DIR / "cover_art/Gemini_Generated_Image_zhebfczhebfczheb.jpeg"
TEMP_BUILD_DIR = CHANNEL_DIR / "output_videos/temp_mix_build"
OUT_DIR = CHANNEL_DIR / "output_videos"
TEMP_BUILD_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MIX_WAV = TEMP_BUILD_DIR / "full_seamless_melodic_edm_mix.wav"
FINAL_VIDEO_MP4 = OUT_DIR / "1HOUR_CRYSTAL_MELODIC_EDM_VOL1_OFFICIAL.mp4"
CHAPTERS_TXT = OUT_DIR / "1HOUR_CRYSTAL_MELODIC_EDM_VOL1_chapters.txt"

# トラック順序（Hands_Turn_Slowly / Avicii系最優先配置）
PRIORITY_ORDER = [
    "Hands_Turn_Slowly",
    "Brighter_Than_The_Sun",
    "Breaking_Past_Gravity",
    "Broken_Glass_Mornings",
    "Burning_Like_Stars",
    "Beyond_The_Heavy_Ground",
    "Weightless_In_The_Sun",
    "Sun_Above",
    "Golden_Motion",
    "Chasing_the_Infinite",
    "Chasing_Endless_Daylight",
    "Salt_and_Sunlight",
    "Midnight_Afterglow",
    "Weightless_In_Gold",
    "A_Thousand_Frames",
    "Chasing_After_Endless_Light",
    "Golden_Hour_Traces",
    "Salt_in_Our_Hair",
    "Wait_for_the_Motion",
    "Healed_by_Summer_Light",
    "The_Chair_By_The_Door"
]

print("=== STEP 1: 音声抽出 & Super Crisp Vocal & EDMマスタリング ===")
# Super Crisp Vocal & Summer EDM V-Shape EQ
EQ_FILTER = (
    "equalizer=f=50:t=q:w=1.4:g=9.5,"
    "equalizer=f=100:t=q:w=1.2:g=6.0,"
    "equalizer=f=250:t=q:w=1.0:g=-3.0,"
    "equalizer=f=3500:t=q:w=1.0:g=4.0,"
    "equalizer=f=8000:t=q:w=1.0:g=7.5,"
    "equalizer=f=12000:t=q:w=1.0:g=9.0,"
    "equalizer=f=16000:t=q:w=1.0:g=9.5,"
    "alimiter=limit=0.95"
)

mastered_tracks = []
for idx, name in enumerate(PRIORITY_ORDER, 1):
    src_file = RAW_AUDIO_DIR / f"{name}.mp4"
    if not src_file.exists():
        src_file = RAW_AUDIO_DIR / f"{name}.mp3"
    if not src_file.exists():
        print(f"Warning: {src_file} not found, skipping...")
        continue
    
    out_wav = TEMP_BUILD_DIR / f"{idx:02d}_{name}_mastered.wav"
    print(f"  [{idx:02d}/{len(PRIORITY_ORDER)}] Mastering: {name}...")
    cmd = [
        "ffmpeg", "-y", "-i", str(src_file),
        "-vn", "-af", EQ_FILTER,
        "-ar", "44100", "-ac", "2", "-sample_fmt", "s16",
        str(out_wav)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    mastered_tracks.append((name, out_wav))

print(f"\n=== STEP 2: DJクロスフェード結合 (全{len(mastered_tracks)}曲) ===")
CROSSFADE_SEC = 2.5
crossfade_samples = int(CROSSFADE_SEC * 44100)

full_audio_list = []
chapters = []
current_samples = 0

for i, (title, wav_path) in enumerate(mastered_tracks):
    with wave.open(str(wav_path), 'rb') as wf:
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
        audio = audio.reshape(-1, 2)
    
    sec = current_samples / 44100.0
    m = int(sec // 60)
    s = int(sec % 60)
    display_title = title.replace("_", " ")
    chapters.append(f"{m:02d}:{s:02d} - {display_title}")
    
    if i == 0:
        full_audio_list.append(audio)
        current_samples += len(audio)
    else:
        prev_tail = full_audio_list[-1][-crossfade_samples:]
        curr_head = audio[:crossfade_samples]
        
        fade_out = np.linspace(1.0, 0.0, crossfade_samples).reshape(-1, 1)
        fade_in = np.linspace(0.0, 1.0, crossfade_samples).reshape(-1, 1)
        
        crossfaded = (prev_tail * fade_out) + (curr_head * fade_in)
        
        full_audio_list[-1] = full_audio_list[-1][:-crossfade_samples]
        full_audio_list.append(crossfaded)
        full_audio_list.append(audio[crossfade_samples:])
        
        current_samples += (len(audio) - crossfade_samples)

final_stereo = np.vstack(full_audio_list)
max_val = np.max(np.abs(final_stereo))
if max_val > 32767:
    final_stereo = (final_stereo / max_val) * 32760
final_int16 = final_stereo.astype(np.int16)

with wave.open(str(FINAL_MIX_WAV), 'wb') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(final_int16.tobytes())

total_duration = len(final_int16) / 44100.0
print(f"✅ Full Mix WAV Ready: {total_duration/60:.2f} mins ({total_duration:.1f} sec)")

with open(CHAPTERS_TXT, "w", encoding="utf-8") as f:
    f.write("\n".join(chapters) + "\n")
print(f"✅ Chapters saved to: {CHAPTERS_TXT}")

print("\n=== STEP 3: 水色波形ビジュアライザー動画レンダリング ===")
FPS = 30
WIDTH = 1920
HEIGHT = 1080

NUM_BARS = 48
BAR_WIDTH = 18
BAR_GAP = 10
MAX_BAR_HEIGHT = 52
MIN_BAR_HEIGHT = 6
BOTTOM_MARGIN = 24
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

FILL_COLOR = (0, 229, 255, 230)      # 水色ネオンシアン (RGBA)
OUTLINE_COLOR = (165, 243, 252, 200)  # 淡いアイシーブルー輪郭

audio_mono = 0.5 * (final_int16[:, 0].astype(np.float32) + final_int16[:, 1].astype(np.float32)) / 32768.0

samples_per_frame = 44100 // FPS
total_video_frames = len(audio_mono) // samples_per_frame
print(f"Total Video Frames: {total_video_frames} ({total_duration/60:.2f} mins)")

bg_img = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

fft_size = 4096
freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
freqs = np.fft.rfftfreq(fft_size, 1.0 / 44100)

freq_weights = np.zeros(NUM_BARS)
for b in range(NUM_BARS):
    f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
    freq_weights[b] = (f_center / 100.0) ** 0.52 * 19.0

cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",
    "-i", str(FINAL_MIX_WAV),
    "-c:v", "h264_videotoolbox",
    "-b:v", "1500k",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(FINAL_VIDEO_MP4)
]

ffmpeg_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

prev_heights = np.zeros(NUM_BARS)
hanning_win = np.hanning(fft_size)

print("[+] Rendering Video Stream to FFmpeg...")

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
    
    if f_idx % 1800 == 0:
        pct = (f_idx / total_video_frames) * 100.0
        print(f"  Frame {f_idx}/{total_video_frames} ({pct:.1f}%) - {(f_idx/FPS)/60:.1f}m rendered")

ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()

print(f"\n🎉 1-Hour Melodic EDM Video Created Successfully: {FINAL_VIDEO_MP4}")
