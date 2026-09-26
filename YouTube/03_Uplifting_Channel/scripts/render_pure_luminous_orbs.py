# -*- coding: utf-8 -*-
"""
Ch3 AuraMelody Audio - Official Pure Luminous Bokeh Visual Engine
(公式ビジュアル演出エンジン：洗練された3D浮遊光ボケオーブ特化レンダラー)

【確定仕様】
- 紙吹雪や記号的バーストを全廃し、最高峰のシネマティック感・透明感を誇る「浮遊光ボケオーブ（3層深度）」に一本化。
- 音響非連動、ゆったりと空間を満たす自然呼吸環境光。
- どんな曲でも完全全自動・破綻ゼロで高品質レンダリング。
"""

import os
import sys
import math
import random
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
import subprocess
import wave

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
AUDIO_FILE = BASE_DIR / "mastered_audio_test" / "01_Hands_Turn_Slowly_NaturalBass.wav"
BG_IMAGE_PATH = BASE_DIR / "output_videos" / "thumbnails" / "STYLE_01_PURE_ART_NO_TEXT.jpg"
OUTPUT_DIR = BASE_DIR / "output_videos" / "burst_tests"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_VIDEO_PATH = OUTPUT_DIR / "FULL_TRACK_PURE_LUMINOUS_ORBS_176S.mp4"
PREVIEW_IMAGE_PATH = OUTPUT_DIR / "preview_pure_luminous_orbs.jpg"

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# ==========================================
# 浮遊光ボケオーブ（3層立体深度・スロー環境光）
# ==========================================
class SteadyFloatingOrb:
    def __init__(self, x=None, y=None, layer="mid"):
        self.layer = layer
        self.x = x if x is not None else random.uniform(0, WIDTH)
        self.y = y if y is not None else random.uniform(0, HEIGHT + 100)
        
        if layer == "large_fg":
            # 画面手前の大ボケ球（映画のようなボケ感）
            self.base_radius = random.uniform(55, 95)
            self.base_alpha = random.uniform(25, 45)
            self.vy = random.uniform(-0.35, -0.15)
            self.drift_amp = random.uniform(0.8, 1.5)
        elif layer == "mid":
            # 空間を漂うメイン光球
            self.base_radius = random.uniform(14, 28)
            self.base_alpha = random.uniform(60, 100)
            self.vy = random.uniform(-0.5, -0.22)
            self.drift_amp = random.uniform(0.5, 1.1)
        else: # "small_dust"
            # 繊細な星屑粒子
            self.base_radius = random.uniform(3, 6)
            self.base_alpha = random.uniform(90, 140)
            self.vy = random.uniform(-0.35, -0.18)
            self.drift_amp = random.uniform(0.3, 0.7)
            
        self.phase_x = random.uniform(0, math.pi * 2)
        self.speed_x = random.uniform(0.012, 0.025)
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.pulse_speed = random.uniform(0.02, 0.04)
        
        # 上品なパステル光彩
        colors = [
            (255, 240, 200),  # Soft Sunlight Gold
            (255, 220, 180),  # Pale Amber
            (210, 245, 255),  # Crystal Cyan
            (255, 220, 235),  # Soft Rose
            (255, 255, 255),  # Pure Warm White
        ]
        self.color = random.choice(colors)

    def update(self):
        self.phase_x += self.speed_x
        self.pulse_phase += self.pulse_speed
        self.x += math.sin(self.phase_x) * self.drift_amp
        self.y += self.vy
        
        if self.y < -120:
            self.y = HEIGHT + random.uniform(20, 60)
            self.x = random.uniform(0, WIDTH)

    def draw(self, draw: ImageDraw.ImageDraw):
        pulse = 0.88 + 0.12 * math.sin(self.pulse_phase)
        alpha = int(np.clip(self.base_alpha * pulse, 0, 255))
        r = self.base_radius * (0.96 + 0.04 * pulse)
        r_c, g_c, b_c = self.color
        
        draw.ellipse([self.x - r, self.y - r, self.x + r, self.y + r], fill=(r_c, g_c, b_c, alpha))
        if self.layer != "large_fg":
            core_r = r * 0.35
            core_alpha = int(min(255, alpha * 1.35))
            draw.ellipse([self.x - core_r, self.y - core_r, self.x + core_r, self.y + core_r], fill=(255, 255, 255, core_alpha))

def main():
    print("🚀 [Step 1] Loading background image and audio...")
    bg_img = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    with wave.open(str(AUDIO_FILE), 'rb') as wf:
        total_sec = wf.getnframes() / wf.getframerate()
        total_frames = int(total_sec * FPS)
        
    print(f"🎵 Audio Duration: {total_sec:.2f}s | Total Frames: {total_frames}")
    
    # 3層立体深度オーブ（大: 4個, 中: 8個, 小: 12個 = 計24個の洗練された密度）
    orbs = [SteadyFloatingOrb(layer="large_fg") for _ in range(4)]
    orbs += [SteadyFloatingOrb(layer="mid") for _ in range(8)]
    orbs += [SteadyFloatingOrb(layer="small_dust") for _ in range(12)]

    preview_saved = False
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(OUTPUT_VIDEO_PATH)
    ]
    
    print(f"🎬 [Step 2] Rendering Pure Luminous Orbs Video to {OUTPUT_VIDEO_PATH.name}...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    for f in range(total_frames):
        # 1. 浮遊光の更新
        for orb in orbs:
            orb.update()
            
        # 2. 描画合成
        frame_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_layer)
        
        for orb in orbs:
            orb.draw(draw)
            
        final_frame = Image.alpha_composite(bg_img, frame_layer)
        
        # プレビュー保存（中盤の安定した1フレーム）
        if not preview_saved and f == 150:
            final_frame.convert("RGB").save(PREVIEW_IMAGE_PATH, quality=95)
            preview_saved = True
            
        proc.stdin.write(final_frame.tobytes())
        
        if f % (FPS * 15) == 0 or f == total_frames - 1:
            progress = (f + 1) / total_frames * 100
            print(f"⏳ Progress: {progress:5.1f}% ({f+1}/{total_frames} frames)")
            
    proc.stdin.close()
    proc.wait()
    
    if not preview_saved:
        final_frame.convert("RGB").save(PREVIEW_IMAGE_PATH, quality=95)
        
    print(f"✨ [Success] Pure Luminous Orbs Render Complete: {OUTPUT_VIDEO_PATH}")
    print(f"🖼 Preview Image Saved: {PREVIEW_IMAGE_PATH}")

if __name__ == "__main__":
    main()
