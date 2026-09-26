#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【共通モジュール】BPM同期 Center-Mirrored 3-Bar Visualizer Engine
- 仕様: 3本の細長丸角カプセルバー (幅:8px, 隙間:14px, 最大高:100px) が画面左下で中心Y座標から上下対称に伸縮
- 配置: 画面左下 (START_X = 150, CENTER_Y = 2050)
- BPM同期: 引数 bpm に基づき、優雅にアニメーション表示
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

class BottomLeftBpmVisualizer:
    def __init__(
        self,
        width: int = 3840,
        height: int = 2160,
        bpm: float = 102.0,
        num_bars: int = 3,
        bar_width: int = 8,
        bar_gap: int = 14,
        max_height: int = 100,
        min_height: int = 14,
        start_x: int = 150,           # 【確定指示】画面左下配置
        center_y: int = 2050,         # 【確定指示】画面左下基準Y
        glow_color: tuple = (255, 255, 255, 120),
        bar_color: tuple = (255, 255, 255, 240)
    ):
        self.width = width
        self.height = height
        self.bpm = bpm
        self.beat_dur = 60.0 / bpm
        self.num_bars = num_bars
        self.bar_width = bar_width
        self.bar_gap = bar_gap
        self.max_height = max_height
        self.min_height = min_height
        self.start_x = start_x
        self.center_y = center_y
        self.glow_color = glow_color
        self.bar_color = bar_color

        self.bar_params = [
            {"freq_mult": 1.0, "sub_mult": 0.5, "phase": 0.0, "sub_phase": 0.8},
            {"freq_mult": 1.5, "sub_mult": 0.75, "phase": math.pi * 0.65, "sub_phase": 2.1},
            {"freq_mult": 2.0, "sub_mult": 1.25, "phase": math.pi * 1.35, "sub_phase": 1.4},
        ]

    def render_frame(self, base_img: Image.Image, frame_idx: int, fps: int = 30) -> Image.Image:
        """
        与えられたフレーム画像に、画面左下でBPMに同期して上下伸縮する3本バーを描画して返す。
        """
        t = frame_idx / fps
        beat_angle = (2.0 * math.pi / self.beat_dur) * t

        frame = base_img.copy()
        draw = ImageDraw.Draw(frame, "RGBA")

        for b in range(self.num_bars):
            p = self.bar_params[b]
            w1 = math.sin(beat_angle * p["freq_mult"] + p["phase"])
            w2 = math.cos(beat_angle * p["sub_mult"] + p["sub_phase"])
            norm_val = (w1 * 0.6 + w2 * 0.4 + 1.0) / 2.0
            norm_val = max(0.0, min(1.0, norm_val))

            current_h = self.min_height + norm_val * (self.max_height - self.min_height)
            half_h = current_h / 2.0

            x0 = self.start_x + b * (self.bar_width + self.bar_gap)
            x1 = x0 + self.bar_width
            y0 = self.center_y - half_h
            y1 = self.center_y + half_h
            radius = self.bar_width / 2.0

            # グロー描画
            draw.rounded_rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], radius=radius + 1, fill=self.glow_color)
            # 本体バー描画
            draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=self.bar_color)

        return frame

if __name__ == "__main__":
    print("BottomLeftBpmVisualizer Engine Loaded Successfully")
