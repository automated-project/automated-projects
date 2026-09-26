# -*- coding: utf-8 -*-
"""
Universal Procedural Visual FX Engine (汎用プロシージャル演出エフェクトエンジン)
背景が変わっても全チャンネル（Ch1/Ch2/Ch3）で自由に使える6種類の弾けるビジュアルエフェクト集

【収録エフェクト一覧】
1. Type A: Neon Shockwave Ripple (多重ネオン波紋リング)
2. Type B: Stardust Galaxy Burst (無数の星屑・光の粉が舞い散る)
3. Type C: Cyber Hexagon Grid (近未来SF・六角形デジタルバースト)
4. Type D: Solar Flare Rays (放射状に差し込む鋭い光条フラッシュ)
5. Type E: Floating Luminous Orbs (空間をフワフワ漂い脈動する光球)
6. Type F: Heavy Bass Glitch Pulse (重低音で歪むショックウェーブ)
"""

import os
import sys
import math
import random
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import subprocess
import wave

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
AUDIO_FILE = BASE_DIR / "mastered_audio_test" / "01_Hands_Turn_Slowly_NaturalBass.wav"
BG_IMAGE_PATH = BASE_DIR / "output_videos" / "thumbnails" / "STYLE_01_PURE_ART_NO_TEXT.jpg"
OUTPUT_DIR = BASE_DIR / "output_videos" / "burst_tests"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# ==========================================
# 1. 各種パーティクル & エフェクトクラス群
# ==========================================

class ShockwaveRing:
    """Type A: 多重ネオン波紋リング"""
    def __init__(self, cx, cy, color, max_r=350, duration=20):
        self.cx, self.cy = cx, cy
        self.color = color
        self.max_r = max_r
        self.duration = duration
        self.age = 0
        self.is_dead = False

    def update(self):
        self.age += 1
        if self.age >= self.duration:
            self.is_dead = True

    def draw(self, draw: ImageDraw.ImageDraw):
        prog = self.age / self.duration
        t = 1.0 - math.pow(1.0 - prog, 3)
        r = self.max_r * t
        alpha = int(255 * (1.0 - prog))
        w = max(1, int(6 * (1.0 - prog)))
        r_c, g_c, b_c = self.color
        draw.ellipse([self.cx - r, self.cy - r, self.cx + r, self.cy + r], outline=(r_c, g_c, b_c, alpha), width=w)
        if prog > 0.12:
            r2 = r * 0.75
            draw.ellipse([self.cx - r2, self.cy - r2, self.cx + r2, self.cy + r2], outline=(255, 255, 255, int(alpha * 0.8)), width=max(1, w - 2))


class StardustParticle:
    """Type B: 星屑・光の粉"""
    def __init__(self, cx, cy, color):
        self.cx, self.cy = cx, cy
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(4, 26)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.size = random.uniform(2, 6)
        self.life = random.randint(16, 28)
        self.max_life = self.life
        self.twinkle = random.uniform(0.1, 0.3)

    def update(self):
        self.cx += self.vx
        self.cy += self.vy + 0.3  # わずかな重力で舞い落ちる
        self.vx *= 0.93
        self.vy *= 0.93
        self.life -= 1

    def draw(self, draw: ImageDraw.ImageDraw):
        if self.life <= 0:
            return
        prog = self.life / self.max_life
        twinkle_factor = 0.7 + 0.3 * math.sin(self.life * self.twinkle * 10)
        alpha = int(255 * prog * twinkle_factor)
        r, g, b = self.color
        s = self.size * prog
        draw.ellipse([self.cx - s, self.cy - s, self.cx + s, self.cy + s], fill=(r, g, b, alpha))
        draw.ellipse([self.cx - s*0.5, self.cy - s*0.5, self.cx + s*0.5, self.cy + s*0.5], fill=(255, 255, 255, alpha))


class HexagonBurst:
    """Type C: 近未来SF・デジタル六角形バースト"""
    def __init__(self, cx, cy, color, max_r=280, duration=18):
        self.cx, self.cy = cx, cy
        self.color = color
        self.max_r = max_r
        self.duration = duration
        self.age = 0
        self.rot = random.uniform(0, math.pi / 3)
        self.is_dead = False

    def update(self):
        self.age += 1
        self.rot += 0.04
        if self.age >= self.duration:
            self.is_dead = True

    def draw(self, draw: ImageDraw.ImageDraw):
        prog = self.age / self.duration
        t = 1.0 - math.pow(1.0 - prog, 3)
        r = self.max_r * t
        alpha = int(255 * (1.0 - prog))
        w = max(1, int(4 * (1.0 - prog)))
        r_c, g_c, b_c = self.color
        
        # 六角形の頂点を計算
        points = []
        for i in range(6):
            a = self.rot + i * (math.pi / 3)
            px = self.cx + r * math.cos(a)
            py = self.cy + r * math.sin(a)
            points.append((px, py))
        draw.polygon(points, outline=(r_c, g_c, b_c, alpha), width=w)
        
        # 内部の回転三角
        if prog > 0.15:
            inner_pts = []
            for i in range(3):
                a = -self.rot * 1.5 + i * (2 * math.pi / 3)
                px = self.cx + (r * 0.5) * math.cos(a)
                py = self.cy + (r * 0.5) * math.sin(a)
                inner_pts.append((px, py))
            draw.polygon(inner_pts, outline=(255, 255, 255, int(alpha * 0.7)), width=1)


class SunburstRay:
    """Type D: 放射状ライトレイ（光条フラッシュ）"""
    def __init__(self, cx, cy, color, num_rays=16, max_len=450, duration=15):
        self.cx, self.cy = cx, cy
        self.color = color
        self.num_rays = num_rays
        self.max_len = max_len
        self.duration = duration
        self.age = 0
        self.base_angle = random.uniform(0, math.pi)
        self.is_dead = False

    def update(self):
        self.age += 1
        self.base_angle += 0.06
        if self.age >= self.duration:
            self.is_dead = True

    def draw(self, draw: ImageDraw.ImageDraw):
        prog = self.age / self.duration
        t = 1.0 - math.pow(1.0 - prog, 2)
        l = self.max_len * t
        alpha = int(255 * (1.0 - prog))
        r_c, g_c, b_c = self.color
        
        for i in range(self.num_rays):
            a = self.base_angle + i * (2 * math.pi / self.num_rays)
            p1x = self.cx + (l * 0.15) * math.cos(a)
            p1y = self.cy + (l * 0.15) * math.sin(a)
            p2x = self.cx + l * math.cos(a)
            p2y = self.cy + l * math.sin(a)
            draw.line([(p1x, p1y), (p2x, p2y)], fill=(r_c, g_c, b_c, alpha), width=2)
            
        # 中心フラッシュ
        draw.ellipse([self.cx - 30*t, self.cy - 30*t, self.cx + 30*t, self.cy + 30*t], fill=(255, 255, 255, int(alpha * 0.9)))


class FloatingOrb:
    """Type E: 浮遊する光のオーブ（蛍の光）"""
    def __init__(self, cx, cy, color):
        self.cx = cx + random.uniform(-100, 100)
        self.cy = cy + random.uniform(-100, 100)
        self.color = color
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-2.5, -0.5)
        self.size = random.uniform(8, 20)
        self.life = random.randint(30, 50)
        self.max_life = self.life
        self.is_dead = False

    def update(self):
        self.cx += self.vx
        self.cy += self.vy
        self.life -= 1
        if self.life <= 0:
            self.is_dead = True

    def draw(self, draw: ImageDraw.ImageDraw):
        prog = self.life / self.max_life
        alpha = int(180 * math.sin(prog * math.pi))  # 滑らかなフェードイン＆アウト
        r, g, b = self.color
        s = self.size * (0.8 + 0.2 * math.sin(self.life * 0.3))
        draw.ellipse([self.cx - s, self.cy - s, self.cx + s, self.cy + s], fill=(r, g, b, alpha))
        draw.ellipse([self.cx - s*0.4, self.cy - s*0.4, self.cx + s*0.4, self.cy + s*0.4], fill=(255, 255, 255, alpha))

# ==========================================
# 2. ショーケース動画 ＆ カタログ生成
# ==========================================

def render_showcase_video():
    print("🎨 Rendering Multi-Style Visual FX Showcase (6 Dynamic Types)...")
    
    bg_raw = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    out_video = OUTPUT_DIR / "FX_CATALOG_SHOWCASE_12S.mp4"
    
    total_frames = 12 * FPS  # 12秒（2秒ごとにエフェクトタイプが切り替わる）
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-ss", "00:00:00",
        "-t", "12.0",
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
    
    fx_list = []
    
    color_palette = [
        (0, 229, 255),   # Cyan
        (255, 0, 128),   # Pink
        (255, 215, 0),   # Gold
        (0, 255, 180),   # Emerald
        (170, 90, 255)   # Purple
    ]
    
    centers = [(960, 540), (1580, 500), (820, 480), (1100, 480)]
    
    preview_frames = {}

    for f in range(total_frames):
        mode = (f // (2 * FPS)) % 6  # 2秒ごとにモード切り替え
        
        # 10フレームごとにエフェクトトリガー
        if f % 10 == 0:
            cx, cy = random.choice(centers)
            col = random.choice(color_palette)
            
            if mode == 0:  # Type A: Neon Shockwave
                fx_list.append(ShockwaveRing(cx, cy, col))
            elif mode == 1:  # Type B: Stardust Galaxy
                for _ in range(35):
                    fx_list.append(StardustParticle(cx, cy, col))
            elif mode == 2:  # Type C: Cyber Hexagon
                fx_list.append(HexagonBurst(cx, cy, col))
            elif mode == 3:  # Type D: Solar Rays
                fx_list.append(SunburstRay(cx, cy, col))
            elif mode == 4:  # Type E: Floating Orbs
                for _ in range(6):
                    fx_list.append(FloatingOrb(cx, cy, col))
            elif mode == 5:  # Type F: All Combined (全部盛りスーパーバースト)
                fx_list.append(ShockwaveRing(cx, cy, col))
                fx_list.append(HexagonBurst(cx, cy, (255, 255, 255)))
                for _ in range(25):
                    fx_list.append(StardustParticle(cx, cy, col))
                fx_list.append(SunburstRay(cx, cy, col, num_rays=12))

        frame = bg_raw.copy()
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d_over = ImageDraw.Draw(overlay)
        
        for fx in fx_list:
            fx.draw(d_over)
            fx.update()
            
        fx_list = [fx for fx in fx_list if not getattr(fx, 'is_dead', False) and getattr(fx, 'life', 1) > 0]
        
        bloom = overlay.filter(ImageFilter.GaussianBlur(radius=8))
        final_frame = Image.alpha_composite(frame, bloom)
        final_frame = Image.alpha_composite(final_frame, overlay)
        
        # 各モードの代表フレームを保存
        if f in [30, 90, 150, 210, 270, 330]:
            p_name = f"catalog_mode_{mode}.jpg"
            final_frame.convert("RGB").save(str(OUTPUT_DIR / p_name), quality=95)
            preview_frames[mode] = OUTPUT_DIR / p_name
            
        process.stdin.write(final_frame.tobytes())
        
    process.stdin.close()
    process.wait()
    print(f"🎉 Showcase video generated: {out_video}")
    return out_video, preview_frames

if __name__ == "__main__":
    render_showcase_video()
