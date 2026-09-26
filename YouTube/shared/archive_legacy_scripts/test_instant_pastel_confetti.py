# -*- coding: utf-8 -*-
"""
Translucent & Instant Fast Confetti Burst (透明感・瞬間高速散布 紙吹雪エンジン)
- パステル・淡い半透明カラー (Pale Pastels & Translucent Crystal Alpha)
- 超高速初速でパッと一瞬で広がり、0.5〜0.8秒でスッと消える瞬間バースト
"""

import os
import sys
import math
import random
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import subprocess
import wave

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
AUDIO_FILE = BASE_DIR / "mastered_audio_test" / "01_Hands_Turn_Slowly_NaturalBass.wav"
BG_IMAGE_PATH = BASE_DIR / "output_videos" / "thumbnails" / "STYLE_01_PURE_ART_NO_TEXT.jpg"
OUTPUT_DIR = BASE_DIR / "output_videos" / "burst_tests"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30
TEST_DURATION_SEC = 8.0

class InstantPastelConfetti:
    """透明感のある淡い色合いで、一瞬で弾けて消える紙吹雪"""
    def __init__(self, cx, cy, color):
        self.cx = cx
        self.cy = cy
        self.color = color
        
        # 超高速初速（四方八方にパッと爆発拡散）
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(18, 42)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        
        # 小さめの紙片サイズ
        self.w = random.uniform(6, 12)
        self.h = random.uniform(10, 18)
        
        # 高速3D回転
        self.rot_z = random.uniform(0, math.pi * 2)
        self.rot_x = random.uniform(0, math.pi * 2)
        self.rot_y = random.uniform(0, math.pi * 2)
        self.spin_speed_z = random.uniform(-0.3, 0.3)
        self.spin_speed_x = random.uniform(0.2, 0.45)
        self.spin_speed_y = random.uniform(0.15, 0.35)
        
        # 短い寿命（約0.5〜0.8秒でスッと消える）
        self.life = random.randint(14, 24)
        self.max_life = self.life

    def update(self):
        self.vx *= 0.88  # 急速な空気抵抗減速
        self.vy *= 0.88
        self.cx += self.vx
        self.cy += self.vy + 0.8  # わずかな落下
        
        self.rot_z += self.spin_speed_z
        self.rot_x += self.spin_speed_x
        self.rot_y += self.spin_speed_y
        
        self.life -= 1

    def draw(self, draw: ImageDraw.ImageDraw):
        if self.life <= 0:
            return
        
        # 3次イージングによる滑らかな瞬間フェードアウト
        prog = self.life / self.max_life
        alpha = int(140 * math.pow(prog, 1.5))  # 最大アルファを140（半透明）に抑えて薄く
        
        scale_x = math.cos(self.rot_x)
        scale_y = math.cos(self.rot_y)
        cur_w = self.w * abs(scale_x)
        cur_h = self.h * abs(scale_y)
        
        if cur_w < 0.5 or cur_h < 0.5:
            return
            
        r, g, b = self.color
        fill_col = (r, g, b, alpha)
        
        cos_z = math.cos(self.rot_z)
        sin_z = math.sin(self.rot_z)
        
        hw, hh = cur_w / 2, cur_h / 2
        local_pts = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        poly_pts = []
        for lx, ly in local_pts:
            rx = lx * cos_z - ly * sin_z
            ry = lx * sin_z + ly * cos_z
            poly_pts.append((self.cx + rx, self.cy + ry))
            
        draw.polygon(poly_pts, fill=fill_col)


class InstantConfettiBurst:
    """一瞬でパッと弾ける淡い紙吹雪イベント"""
    def __init__(self, cx, cy, count=75):
        self.pieces = []
        
        # 淡いパステル・クリスタルカラー（薄い色合い）
        pastel_palette = [
            (255, 200, 220),   # Pale Rose Pink
            (190, 240, 255),   # Crystal Ice Blue
            (255, 245, 200),   # Soft Champagne Gold
            (200, 255, 230),   # Pastel Mint
            (230, 210, 255),   # Soft Lavender
            (255, 255, 255),   # Pure Crystal White
        ]
        
        for _ in range(count):
            col = random.choice(pastel_palette)
            self.pieces.append(InstantPastelConfetti(cx, cy, col))
            
    def update(self):
        for p in self.pieces:
            p.update()
            
    def draw(self, draw: ImageDraw.ImageDraw):
        for p in self.pieces:
            p.draw(draw)
            
    @property
    def is_dead(self):
        return all(p.life <= 0 for p in self.pieces)


def render_instant_pastel_confetti():
    print("✨ Step 1: Simulating Instant Pastel Translucent Confetti Bursts...")
    bg_raw = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    out_video = OUTPUT_DIR / "TEST_INSTANT_PASTEL_CONFETTI_8S.mp4"
    total_frames = int(TEST_DURATION_SEC * FPS)
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-ss", "00:00:00",
        "-t", str(TEST_DURATION_SEC),
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(out_video)
    ]
    
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    confetti_bursts = []
    
    # 複数ポイントでの瞬間バースト
    burst_schedule = [
        (15, WIDTH // 2, HEIGHT // 2),
        (35, 1580, 500),                  # 右ヘッドホン
        (55, 820, 480),                   # 左瞳周辺
        (75, WIDTH // 2 - 250, HEIGHT // 2 - 100),
        (75, WIDTH // 2 + 250, HEIGHT // 2 - 100),
        (110, WIDTH // 2, HEIGHT // 2),
        (140, 1100, 480),
        (160, WIDTH // 2, HEIGHT // 2 + 150),
    ]

    print("🎬 Step 2: Rendering Instant Confetti Frames...")
    preview_saved = False
    
    for f in range(total_frames):
        for bf, bx, by in burst_schedule:
            if f == bf:
                confetti_bursts.append(InstantConfettiBurst(bx, by, count=70))
                
        frame = bg_raw.copy()
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d_over = ImageDraw.Draw(overlay)
        
        for cb in confetti_bursts:
            cb.draw(d_over)
            cb.update()
            
        confetti_bursts = [cb for cb in confetti_bursts if not cb.is_dead]
        
        # 繊細なソフトグロー
        bloom = overlay.filter(ImageFilter.GaussianBlur(radius=2.5))
        final_frame = Image.alpha_composite(frame, bloom)
        final_frame = Image.alpha_composite(final_frame, overlay)
        
        # プレビュー保存（バースト直後の拡散した瞬間）
        if f == 79 and not preview_saved:
            preview_path = OUTPUT_DIR / "preview_instant_pastel_confetti.jpg"
            final_frame.convert("RGB").save(str(preview_path), quality=95)
            preview_saved = True
            
        process.stdin.write(final_frame.tobytes())
        
    process.stdin.close()
    process.wait()
    print(f"🎉 Rendered Instant Pastel Confetti video: {out_video}")
    return out_video, OUTPUT_DIR / "preview_instant_pastel_confetti.jpg"

if __name__ == "__main__":
    render_instant_pastel_confetti()
