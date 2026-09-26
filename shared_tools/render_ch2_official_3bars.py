#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2: Velvet Sunset Audio - Official 4K Video Renderer with Exact 3-Bar Rounded Capsule Visualizer
- 公式設計仕様に完全準拠 (NumPy FFT -> PIL Rounded Rectangle / Outer Glow -> FFmpeg Pipe)
- 3本カプセルバー (低音・中音・高音) を右下隅 (x=3660, y=2060) に小さく上品に配置
- 2曲自然余白保持 2.5秒DJクロスフェード結合
- 4K (3840x2160) Lanczosアップスケール
"""

import os
import sys
import wave
import time
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

# 1. 素材パス
TRACK1 = "/Users/base/Downloads/ch2-flow-mix/Neon Horizon.wav"
TRACK2 = "/Users/base/Downloads/ch2-flow-mix/Twilight Tide.wav"
IMAGE_IN = "/Users/base/Downloads/Gemini_Generated_Image_cxs9rncxs9rncxs9.jpeg"

OUT_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/output_videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUT_DIR / "temp_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_WAV = TEMP_DIR / "ch2_2tracks_natural_mix.wav"
OUT_MP4 = OUT_DIR / "CH2_VELVET_SUNSET_OFFICIAL_3BARS_4K.mp4"

WIDTH = 3840
HEIGHT = 2160
FPS = 30

# 2. 正式な3本丸角カプセル波形パラメータ (4K 右下隅配置)
NUM_BARS = 3
BAR_WIDTH = 14
BAR_GAP = 10
MAX_BAR_HEIGHT = 44       # 上品で控えめな最大高
MIN_BAR_HEIGHT = 6        # アイドル時も灯る最小高
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = WIDTH - TOTAL_WIDTH - 120 # 右端から120px
BASE_Y = HEIGHT - 100               # 下端から100px

# Sunset Orange ネオン発光カラー (RGBA)
BAR_COLOR = (255, 140, 50, 220)     # サンセットオレンジ本体
BAR_GLOW = (255, 180, 100, 90)      # 柔らかな光彩 (Glow)

print("🎵 [1/4] 2曲の自然余白保持 2.5秒等エネルギーDJクロスフェード合成...")

def read_wav(p):
    with wave.open(p, "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        n = w.getnframes()
        raw = w.readframes(n)
        d = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if ch == 2:
            d = d.reshape(-1, 2)
        else:
            d = np.column_stack((d, d))
        return d, sr

d1, sr1 = read_wav(TRACK1)
d2, sr2 = read_wav(TRACK2)

crossfade_sec = 2.5
fade_samples = int(crossfade_sec * sr1)

t_in = np.linspace(0, np.pi / 2, fade_samples, endpoint=False, dtype=np.float32)
in_curve = np.sin(t_in)[:, np.newaxis]
out_curve = np.cos(t_in)[:, np.newaxis]

total_samples = len(d1) + len(d2) - fade_samples
combined = np.zeros((total_samples, 2), dtype=np.float32)

combined[:len(d1)] += d1
overlap_start = len(d1) - fade_samples
combined[overlap_start:overlap_start + fade_samples] = (
    d1[overlap_start:] * out_curve + d2[:fade_samples] * in_curve
)
combined[overlap_start + fade_samples:] = d2[fade_samples:]

peak = np.max(np.abs(combined))
if peak > 0.95:
    combined *= (0.95 / peak)

int16_out = (np.clip(combined, -1.0, 1.0) * 32767.0).astype(np.int16)
with wave.open(str(OUT_WAV), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr1)
    w.writeframes(int16_out.tobytes())

total_dur = len(int16_out) / sr1
print(f"✅ 音声結合完了: {OUT_WAV} (総尺: {total_dur/60:.2f}分 / {total_dur:.1f}秒)")

print("🎨 [2/4] 4K背景画像のLanczos高品位リサイズ...")
bg_img = Image.open(IMAGE_IN).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# モノラルオーディオ (FFT解析用)
audio_mono = 0.5 * (combined[:, 0] + combined[:, 1])
samples_per_frame = sr1 // FPS
total_video_frames = int(total_dur * FPS)

# 3本バーの周波数帯域 (低音: 50-250Hz, 中音: 250-2500Hz, 高音: 2500-12000Hz)
fft_size = 4096
freq_bins = [50, 250, 2500, 12000]
freqs = np.fft.rfftfreq(fft_size, 1.0 / sr1)
freq_weights = [18.0, 26.0, 38.0] # 帯域ごとの感度補正

print("🎬 [3/4] 公式カプセル波形パイプライン (NumPy FFT -> PIL -> FFmpeg Pipe) 起動...")
cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",  # Stdin video pipe
    "-i", str(OUT_WAV),
    "-c:v", "h264_videotoolbox",
    "-b:v", "9500k",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "320k",
    "-shortest", "-movflags", "+faststart",
    str(OUT_MP4)
]

ffmpeg_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

prev_heights = np.zeros(NUM_BARS)
hanning_win = np.hanning(fft_size)

t_start = time.time()
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
            val = 0.0
        adj = np.clip(val * freq_weights[b], 0.0, 1.0)
        target_heights[b] = MIN_BAR_HEIGHT + adj * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)

    # EMA スムージング (跳ね上がり速く、減衰は滑らか)
    smooth_heights = np.where(target_heights > prev_heights,
                              target_heights * 0.75 + prev_heights * 0.25,
                              prev_heights * 0.82 + target_heights * 0.18)
    prev_heights = smooth_heights

    # フレーム描画
    frame = bg_img.copy()
    draw = ImageDraw.Draw(frame, "RGBA")

    for b in range(NUM_BARS):
        h = int(smooth_heights[b])
        bx = START_X + b * (BAR_WIDTH + BAR_GAP)
        by_top = BASE_Y - h
        by_bottom = BASE_Y

        # 柔らかなグロー外枠
        draw.rounded_rectangle(
            [bx - 3, by_top - 3, bx + BAR_WIDTH + 3, by_bottom + 3],
            radius=6,
            fill=BAR_GLOW
        )
        # ソリッドな丸角カプセルバー
        draw.rounded_rectangle(
            [bx, by_top, bx + BAR_WIDTH, by_bottom],
            radius=4,
            fill=BAR_COLOR
        )

    ffmpeg_proc.stdin.write(frame.tobytes())

    if f_idx % 600 == 0:
        pct = (f_idx / total_video_frames) * 100
        print(f"  ⏳ レンダリング進捗: {f_idx}/{total_video_frames} フレーム ({pct:.1f}%)", flush=True)

ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()

render_time = time.time() - t_start
sz_mb = os.path.getsize(str(OUT_MP4)) / (1024 * 1024)

print(f"\n🎉🎉🎉 正式仕様 4K動画レンダリング完了！")
print(f"📁 出力先: {OUT_MP4}")
print(f"📊 ファイルサイズ: {sz_mb:.2f} MB")
print(f"⏱️ レンダリング時間: {render_time:.1f}秒 ({render_time/60:.2f}分)")
