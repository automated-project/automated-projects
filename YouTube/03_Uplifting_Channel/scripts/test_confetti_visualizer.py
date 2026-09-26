# -*- coding: utf-8 -*-
"""
Confetti Burst & 3D Fluttering Petals Particle Engine
(3D立体回転・ヒラヒラ舞い散る紙吹雪＆ホログラムリボン演出エンジン)

- 3次元回転（X/Y軸フリップ・アスペクト比伸縮）によるリアルな紙吹雪のヒラヒラ感
- 爆発初速 ＋ 空気抵抗 ＋ 重力 ＋ 風のサイン波揺らぎシミュレーション
- カラフルなフェス風ネオンホログラム＆ゴールドリボン
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

class ConfettiPiece:
    """3D立体回転しながら舞い散る紙吹雪の1片"""
    def __init__(self, cx, cy, color):
        self.cx = cx + random.uniform(-30, 30)
        self.cy = cy + random.uniform(-30, 30)
        self.color = color  # (R, G, B)
        
        # 爆発初速 (上および外向きに弾ける)
        angle = random.uniform(-math.pi * 0.9, -math.pi * 0.1)  # 上方向中心
        speed = random.uniform(10, 28)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        
        # 紙のサイズ
        self.w = random.uniform(8, 16)
        self.h = random.uniform(14, 26)
        
        # 3D回転パラメータ
        self.rot_z = random.uniform(0, math.pi * 2)
        self.rot_x = random.uniform(0, math.pi * 2)
        self.rot_y = random.uniform(0, math.pi * 2)
        self.spin_speed_z = random.uniform(-0.15, 0.15)
        self.spin_speed_x = random.uniform(0.08, 0.25)
        self.spin_speed_y = random.uniform(0.05, 0.18)
        
        # 風の揺らぎ
        self.flutter_phase = random.uniform(0, math.pi * 2)
        self.flutter_speed = random.uniform(0.08, 0.15)
        
        self.gravity = random.uniform(0.25, 0.45)
        self.life = random.randint(60, 90)
        self.max_life = self.life

    def update(self):
        # 速度更新
        self.vx *= 0.94  # 空気抵抗
        self.vy += self.gravity  # 重力
        if self.vy > 4.5:
            self.vy = 4.5  # 終端落下速度
            
        # 風のサイン波揺らぎ
        self.flutter_phase += self.flutter_speed
        self.cx += self.vx + math.sin(self.flutter_phase) * 1.8
        self.cy += self.vy
        
        # 3D回転
        self.rot_z += self.spin_speed_z
        self.rot_x += self.spin_speed_x
        self.rot_y += self.spin_speed_y
        
        self.life -= 1

    def draw(self, draw: ImageDraw.ImageDraw):
        if self.life <= 0:
            return
        
        # フェードアウト
        alpha = int(255 * min(1.0, self.life / (self.max_life * 0.4)))
        
        # 3D回転による見かけの幅・高さ (X/Y軸のコサイン伸縮)
        scale_x = math.cos(self.rot_x)
        scale_y = math.cos(self.rot_y)
        cur_w = self.w * abs(scale_x)
        cur_h = self.h * abs(scale_y)
        
        if cur_w < 1.0 or cur_h < 1.0:
            return  # 完全に真横を向いている瞬間
            
        # 表裏で色味と明るさを変える（立体シェーディング）
        r, g, b = self.color
        if scale_x * scale_y > 0:
            fill_col = (r, g, b, alpha)
        else:
            # 裏面: 少し白っぽくハイライト
            fill_col = (min(255, r + 60), min(255, g + 60), min(255, b + 60), alpha)
            
        # 2D Z軸回転した4頂点を計算
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


class ConfettiBurst:
    """大量の紙吹雪がパッと弾ける演出イベント"""
    def __init__(self, cx, cy, count=60):
        self.pieces = []
        
        palette = [
            (255, 45, 85),    # Neon Coral Pink
            (0, 229, 255),    # Electric Cyan
            (255, 215, 0),    # Pure Gold
            (255, 149, 0),    # Vivid Orange
            (175, 82, 222),   # Royal Violet
            (52, 199, 89),    # Lime Emerald
            (255, 255, 255)   # Hologram White
        ]
        
        for _ in range(count):
            col = random.choice(palette)
            self.pieces.append(ConfettiPiece(cx, cy, col))
            
    def update(self):
        for p in self.pieces:
            p.update()
            
    def draw(self, draw: ImageDraw.ImageDraw):
        for p in self.pieces:
            p.draw(draw)
            
    @property
    def is_dead(self):
        return all(p.life <= 0 for p in self.pieces)


def render_confetti_test():
    print("🎉 Step 1: Simulating 3D Fluttering Confetti Burst Physics...")
    bg_raw = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    out_video = OUTPUT_DIR / "TEST_CONFETTI_BURST_8S.mp4"
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
    
    # 爆発タイミング（開始直後と中盤に左右・中央から次々弾ける）
    burst_schedule = [
        (10, WIDTH // 2, HEIGHT // 2 + 100),
        (35, WIDTH // 2 - 350, HEIGHT // 2 + 150),
        (45, WIDTH // 2 + 350, HEIGHT // 2 + 150),
        (100, WIDTH // 2, HEIGHT // 2),
        (130, WIDTH // 2 - 250, HEIGHT // 2 + 80),
        (140, WIDTH // 2 + 250, HEIGHT // 2 + 80),
    ]

    print("🎬 Step 2: Rendering Confetti Animation Frames...")
    preview_saved = False
    
    for f in range(total_frames):
        # スケジュールされたバーストを投入
        for bf, bx, by in burst_schedule:
            if f == bf:
                confetti_bursts.append(ConfettiBurst(bx, by, count=55))
                
        frame = bg_raw.copy()
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d_over = ImageDraw.Draw(overlay)
        
        for cb in confetti_bursts:
            cb.draw(d_over)
            cb.update()
            
        confetti_bursts = [cb for cb in confetti_bursts if not cb.is_dead]
        
        # わずかなグロー発光
        bloom = overlay.filter(ImageFilter.GaussianBlur(radius=3))
        final_frame = Image.alpha_composite(frame, bloom)
        final_frame = Image.alpha_composite(final_frame, overlay)
        
        # プレビュー保存（最も紙吹雪が舞っている瞬間）
        if f == 75 and not preview_saved:
            preview_path = OUTPUT_DIR / "preview_confetti_burst.jpg"
            final_frame.convert("RGB").save(str(preview_path), quality=95)
            preview_saved = True
            
        process.stdin.write(final_frame.tobytes())
        
    process.stdin.close()
    process.wait()
    print(f"🎉 Rendered Confetti Burst video: {out_video}")
    return out_video, OUTPUT_DIR / "preview_confetti_burst.jpg"

if __name__ == "__main__":
    render_confetti_test()
