#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated-Projects 共通波形ビジュアライザー描画エンジン (Master Visualizer Engine)
- 最新確定仕様:
  - 形状: 3本極細丸角カプセルバー (幅: 8px, 隙間: 14px, 最大高: 100px, 最小高: 14px)
  - カラー: 洗練されたピュアホワイト（半透明 ＋ ソフトグロー）
  - モーション: BPM（標準102 BPM）基準のポリリズム・ループ（中央起点で上下対称に伸縮）
  - 配置: 画面右下 (START_X = WIDTH - TOTAL_WIDTH - 150, CENTER_Y = HEIGHT - 110)
"""

import numpy as np
from PIL import Image, ImageDraw

NUM_BARS = 3
BAR_WIDTH = 8
BAR_GAP = 14
MAX_BAR_HEIGHT = 100
MIN_BAR_HEIGHT = 14
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP

BAR_COLOR = (255, 255, 255, 240)    # 鮮明なホワイト
BAR_GLOW = (255, 255, 255, 95)      # 柔らかな光彩

class MinimalPolyrhythmVisualizer:
    """
    4K (3840x2160) 対応 ミニマル3本バー ビジュアライザー
    BPMベースのポリリズム・ループで上下対称に伸縮
    """
    def __init__(self, width=3840, height=2160, bpm=102.0, fps=30):
        self.width = width
        self.height = height
        self.bpm = bpm
        self.fps = fps
        self.beat_dur = 60.0 / bpm
        
        self.start_x = width - TOTAL_WIDTH - 150
        self.center_y = height - 110
        
        # 3本の独立位相 & 周波数倍率
        self.bar_params = [
            {"freq_mult": 1.0, "sub_mult": 0.5, "phase": 0.0,            "sub_phase": 0.8},
            {"freq_mult": 1.5, "sub_mult": 0.75, "phase": np.pi * 0.65,  "sub_phase": 2.1},
            {"freq_mult": 2.0, "sub_mult": 1.25, "phase": np.pi * 1.35,  "sub_phase": 1.4},
        ]

    def render_frame_overlay(self, frame_idx: int, base_frame_pil: Image.Image) -> Image.Image:
        """指定フレーム番号の波形を描画して合成"""
        t = frame_idx / self.fps
        beat_angle = (2.0 * np.pi / self.beat_dur) * t
        
        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        for b in range(NUM_BARS):
            p = self.bar_params[b]
            w1 = np.sin(beat_angle * p["freq_mult"] + p["phase"])
            w2 = np.sin(beat_angle * p["sub_mult"] + p["sub_phase"])
            
            combined = (w1 * 0.65 + w2 * 0.35 + 1.0) / 2.0
            norm_val = combined ** 1.3
            
            h = MIN_BAR_HEIGHT + norm_val * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)
            half_h = h / 2.0
            bx = self.start_x + b * (BAR_WIDTH + BAR_GAP)
            
            by_top = int(self.center_y - half_h)
            by_bottom = int(self.center_y + half_h)
            
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
            
        return Image.alpha_composite(base_frame_pil, overlay)
