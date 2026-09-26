#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2: Velvet Sunset Audio - 10-Second Test Preview
- 波形改善仕様:
  - カラー: 洗練されたホワイト（半透明ピュアホワイト ＋ 柔らかな白グロー）
  - 形状: 細長い丸角スリムカプセル (幅: 8px, 隙間: 14px, 最大高: 96px, 最小高: 12px)
  - 伸縮方式: 「中央から上下対称に広がる（Center-Mirrored Expansion）」
  - 配置: 右下隅 (CENTER_Y = 2060, START_X = 3680)
  - 尺: 10.0秒 (動作確認用)
"""

import os
import sys
import wave
import time
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

# 素材パス
TRACK = "/Users/base/Downloads/ch2-flow-mix/Neon Horizon.wav"
IMAGE_IN = "/Users/base/Downloads/Gemini_Generated_Image_cxs9rncxs9rncxs9.jpeg"

OUT_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/output_videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP4 = OUT_DIR / "CH2_PREVIEW_WHITE_CENTER_EXPAND_10S.mp4"

WIDTH = 3840
HEIGHT = 2160
FPS = 30
TEST_DUR_SEC = 10.0
TOTAL_FRAMES = int(TEST_DUR_SEC * FPS)

# よりシャープで細身に調整した波形パラメータ
NUM_BARS = 3
BAR_WIDTH = 8            # 11px -> 8px (極細で洗練されたカプセルバー)
BAR_GAP = 14             # 18px -> 14px (細身に合わせた黄金比ギャップ)
MAX_BAR_HEIGHT = 100     # 110px -> 100px (細身に合わせたバランス)
MIN_BAR_HEIGHT = 14      # 16px -> 14px
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP

START_X = WIDTH - TOTAL_WIDTH - 150 # 右端から150px
CENTER_Y = HEIGHT - 110             # 上下に伸びる基準となる中心Y座標 (2050px)

# ピュアホワイト ＆ グローカラー
BAR_COLOR = (255, 255, 255, 240)    # 鮮明なホワイト
BAR_GLOW = (255, 255, 255, 95)      # 柔らかな光彩

# Ch2の標準BPM（約102 BPM）に合わせた周期設計
# 1拍 = 60 / 102 ≈ 0.588秒
BPM = 102.0
BEAT_DUR = 60.0 / BPM  # 秒/拍

print("🎨 [1/2] 4K背景画像の準備...")
bg_img = Image.open(IMAGE_IN).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

print("🎬 [2/2] 10秒プレビュー動画 (BPM同期・ポリリズム波形ループ) レンダリング開始...")
cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgba",
    "-r", str(FPS),
    "-i", "-",
    "-ss", "0", "-t", str(TEST_DUR_SEC),
    "-i", TRACK,
    "-c:v", "h264_videotoolbox",
    "-b:v", "9500k",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "320k",
    "-shortest", "-movflags", "+faststart",
    str(OUT_MP4)
]

proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 3本のバーそれぞれの独立した周波数比率と初期位相オフセット
# （完全バラバラに見えて、BPMに美しく乗りながら一定の周期で優雅にループする）
BAR_PARAMS = [
    {"freq_mult": 1.0, "sub_mult": 0.5, "phase": 0.0,            "sub_phase": 0.8},  # Bar 1 (低音担当風)
    {"freq_mult": 1.5, "sub_mult": 0.75, "phase": np.pi * 0.65,  "sub_phase": 2.1},  # Bar 2 (中音担当風)
    {"freq_mult": 2.0, "sub_mult": 1.25, "phase": np.pi * 1.35,  "sub_phase": 1.4},  # Bar 3 (高音担当風)
]

for f_idx in range(TOTAL_FRAMES):
    t = f_idx / FPS
    # ビート進行 (0〜2pi)
    beat_angle = (2.0 * np.pi / BEAT_DUR) * t

    frame = bg_img.copy()
    draw = ImageDraw.Draw(frame, "RGBA")

    for b in range(NUM_BARS):
        p = BAR_PARAMS[b]
        # メイン波とサブ波の合成（有機的かつBPMに同期したループモーション）
        w1 = np.sin(beat_angle * p["freq_mult"] + p["phase"])
        w2 = np.sin(beat_angle * p["sub_mult"] + p["sub_phase"])
        
        # 0.0 〜 1.0 のなめらかな振幅（イージング）
        combined = (w1 * 0.65 + w2 * 0.35 + 1.0) / 2.0
        # 少しシャープな抑揚をつける
        norm_val = combined ** 1.3

        h = MIN_BAR_HEIGHT + norm_val * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)
        half_h = h / 2.0
        bx = START_X + b * (BAR_WIDTH + BAR_GAP)
        
        # 中央 (CENTER_Y) を起点に上下に対称展開
        by_top = int(CENTER_Y - half_h)
        by_bottom = int(CENTER_Y + half_h)

        # 外枠グロー
        draw.rounded_rectangle(
            [bx - 2, by_top - 2, bx + BAR_WIDTH + 2, by_bottom + 2],
            radius=4,
            fill=BAR_GLOW
        )
        # ソリッドホワイトバー
        draw.rounded_rectangle(
            [bx, by_top, bx + BAR_WIDTH, by_bottom],
            radius=3,
            fill=BAR_COLOR
        )

    proc.stdin.write(frame.tobytes())

proc.stdin.close()
proc.wait()

print(f"🎉 10秒プレビュー動画完成: {OUT_MP4}")
