#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio) 24/7ライブ配信用 Ocean Waves テスト動画生成スクリプト (1曲版)
- 背景動画: 03_Coding_Synth_Channel/Ocean_waves_rolling_onto_beach_20260920063936.mp4 (シームレスループ)
- 音源: 03_Coding_Synth_Channel/raw_audio/Amber_Horizon.mp4 (Track 01: Amber Horizon / 170秒)
- ビジュアライザー: 48本 Discrete Rounded Bars (Cyan / Neon Blue + White Glow)
- UIオーバーレイ:
  - 左上: 🔴 LIVE 24/7 | AURA MELODY RADIO (ミニマム角丸バッジ)
  - 右下: 🎁 Free Download & Creator Safe (No Copyright) (ミニマム角丸バッジ)
"""

import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube")
CHANNEL_DIR = BASE_DIR / "03_Coding_Synth_Channel"
BG_VIDEO = CHANNEL_DIR / "Ocean_waves_rolling_onto_beach_20260920063936.mp4"
AUDIO_SRC = CHANNEL_DIR / "raw_audio/Amber_Horizon.mp4"
AUDIO_WAV = CHANNEL_DIR / "output_videos/temp_live_track1.wav"
OUT_MP4 = CHANNEL_DIR / "output_videos/TEST_LIVE_CH3_OCEAN_WAVES_TRACK1.mp4"
OUT_MP4.parent.mkdir(parents=True, exist_ok=True)

if not BG_VIDEO.exists():
    print(f"Error: Background video not found at {BG_VIDEO}", file=sys.stderr)
    sys.exit(1)

if not AUDIO_SRC.exists():
    print(f"Error: Audio source not found at {AUDIO_SRC}", file=sys.stderr)
    sys.exit(1)

# 1. 音源を44.1kHz 16-bit WAVに高速抽出
print(f"[+] Extracting WAV from {AUDIO_SRC.name}...")
subprocess.run([
    "ffmpeg", "-y", "-i", str(AUDIO_SRC),
    "-vn", "-ar", "44100", "-ac", "2", "-sample_fmt", "s16",
    str(AUDIO_WAV)
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

FPS = 24
WIDTH = 1920
HEIGHT = 1080

# 2. 波形ビジュアライザー パラメータ (水色・シアンネオン仕様)
NUM_BARS = 48
BAR_WIDTH = 18
BAR_GAP = 10
MAX_BAR_HEIGHT = 48
MIN_BAR_HEIGHT = 5
BOTTOM_MARGIN = 32
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

FILL_COLOR = (0, 229, 255, 230)       # 鮮やかなシアンブルー
OUTLINE_COLOR = (200, 250, 255, 220)  # ホワイト・シアン発光

# 3. 音声データの読み込み & 周波数解析準備
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
print(f"[+] Target Duration: {total_duration_sec:.1f}s ({total_video_frames} frames)")

fft_size = 4096
freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)

freq_weights = np.zeros(NUM_BARS)
for b in range(NUM_BARS):
    f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
    freq_weights[b] = (f_center / 100.0) ** 0.52 * 18.0

# 4. 背景動画のフレームリーダー（FFmpegパイプで無限ループ読み込み）
bg_proc_cmd = [
    "ffmpeg", "-stream_loop", "-1", "-i", str(BG_VIDEO),
    "-f", "image2pipe",
    "-pix_fmt", "rgba",
    "-vcodec", "rawvideo",
    "-r", str(FPS),
    "-s", f"{WIDTH}x{HEIGHT}",
    "-"
]
bg_proc = subprocess.Popen(bg_proc_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

# 5. 出力用FFmpegパイプライン（VideoToolbox ハードウェアエンコード）
out_proc_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",
    "-i", str(AUDIO_WAV),
    "-c:v", "h264_videotoolbox",
    "-b:v", "3500k",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "320k",
    "-shortest",
    str(OUT_MP4)
]
out_proc = subprocess.Popen(out_proc_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 6. フォント準備
font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
font_badge_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)

# 固定UIレイヤーを事前生成（左上バッジ ＆ 右下バッジ）
ui_static = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
ui_draw = ImageDraw.Draw(ui_static)

# [左上バッジ: 🔴 LIVE 24/7 | AURA MELODY RADIO]
badge_left_x = 40
badge_left_y = 40
badge_left_w = 460
badge_left_h = 54
ui_draw.rounded_rectangle([badge_left_x, badge_left_y, badge_left_x + badge_left_w, badge_left_y + badge_left_h], radius=27, fill=(10, 15, 25, 190), outline=(0, 229, 255, 120), width=2)
# 赤い丸
ui_draw.ellipse([badge_left_x + 18, badge_left_y + 17, badge_left_x + 38, badge_left_y + 37], fill=(255, 40, 60))
# テキスト
ui_draw.text((badge_left_x + 48, badge_left_y + 13), "LIVE 24/7", fill=(255, 255, 255), font=font_badge)
ui_draw.text((badge_left_x + 175, badge_left_y + 13), "|", fill=(100, 130, 160), font=font_badge)
ui_draw.text((badge_left_x + 195, badge_left_y + 13), "AURA MELODY RADIO", fill=(165, 243, 252), font=font_badge)

# [右下バッジ: 🎁 Free Download & Creator Safe (No Copyright)]
badge_right_w = 540
badge_right_h = 48
badge_right_x = WIDTH - badge_right_w - 40
badge_right_y = HEIGHT - badge_right_h - 36
ui_draw.rounded_rectangle([badge_right_x, badge_right_y, badge_right_x + badge_right_w, badge_right_y + badge_right_h], radius=24, fill=(10, 15, 25, 190), outline=(255, 215, 0, 100), width=1)
ui_draw.text((badge_right_x + 22, badge_right_y + 12), "🎁 Free Download & Creator Safe (No Copyright)", fill=(255, 245, 220), font=font_badge_sub)

prev_heights = np.zeros(NUM_BARS)
hanning_win = np.hanning(fft_size)
frame_bytes_size = WIDTH * HEIGHT * 4

print("[+] Rendering Live Ocean Waves Video with Cyan Visualizer...")

try:
    for f_idx in range(total_video_frames):
        # 1. 背景フレーム読み込み
        raw_frame = bg_proc.stdout.read(frame_bytes_size)
        if len(raw_frame) < frame_bytes_size:
            break
        frame = Image.frombytes("RGBA", (WIDTH, HEIGHT), raw_frame)

        # 2. 周波数解析
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
                smooth_heights[b] = max(MIN_BAR_HEIGHT, prev_heights[b] * 0.84)
        prev_heights = smooth_heights
        
        # 3. 波形描画
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 波形バー
        for b in range(NUM_BARS):
            h = int(smooth_heights[b])
            x0 = START_X + b * (BAR_WIDTH + BAR_GAP)
            x1 = x0 + BAR_WIDTH
            y1 = BASE_Y
            y0 = BASE_Y - h
            draw.rounded_rectangle([x0, y0, x1, y1], radius=5, fill=FILL_COLOR, outline=OUTLINE_COLOR, width=1)
            
        # 4. 合成（背景 ＋ 波形 ＋ 固定UI）
        frame = Image.alpha_composite(frame, overlay)
        frame = Image.alpha_composite(frame, ui_static)
        
        out_proc.stdin.write(frame.tobytes())
        
        if f_idx % 240 == 0:
            pct = (f_idx / total_video_frames) * 100.0
            print(f"  Progress: frame {f_idx}/{total_video_frames} ({pct:.1f}%)")

finally:
    bg_proc.terminate()
    out_proc.stdin.close()
    out_proc.wait()

if AUDIO_WAV.exists():
    AUDIO_WAV.unlink()

print("==================================================")
print(f"✅ Successfully rendered Test Live Ocean Waves Video!")
print(f"   Output: {OUT_MP4}")
print(f"   Size: {OUT_MP4.stat().st_size / (1024*1024):.2f} MB")
print("==================================================")
