# -*- coding: utf-8 -*-
"""
High-End Audio-Reactive Neon Circle Burst & Particle Engine
(高品位・音響連動 ネオンサークルバースト＆ショックウェーブエンジン)

- 多重ネオンリング急拡大 (Multi-layer Expanding Shockwave Rings)
- 中心グローフレア (Center Radial Flare Flash)
- 十字/ダイヤ型キラキラスパークル粒子 (Radial Cross/Diamond Sparkles)
- 音ハメ連動 (Audio Peak & Transient Attack Detection)
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
TEST_DURATION_SEC = 10.0

class DiamondSparkle:
    """十字・ダイヤ型に輝く光の粒子"""
    def __init__(self, cx, cy, color, speed, angle, size, life):
        self.cx = cx
        self.cy = cy
        self.color = color
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.size = size
        self.max_life = life
        self.life = life
        self.rot = random.uniform(0, math.pi)

    def update(self):
        self.cx += self.vx
        self.cy += self.vy
        self.vx *= 0.92  # 滑らかなイージング減速
        self.vy *= 0.92
        self.life -= 1
        self.rot += 0.1

    def draw(self, draw_obj: ImageDraw.ImageDraw):
        if self.life <= 0:
            return
        alpha = int(255 * (self.life / self.max_life))
        s = self.size * (0.5 + 0.5 * (self.life / self.max_life))
        
        # 十字スパークルの描画
        r, g, b = self.color
        col = (r, g, b, alpha)
        col_core = (255, 255, 255, alpha)
        
        # 水平・垂直の光芒
        draw_obj.line([(self.cx - s*2.5, self.cy), (self.cx + s*2.5, self.cy)], fill=col, width=max(1, int(s/2)))
        draw_obj.line([(self.cx, self.cy - s*2.5), (self.cx, self.cy + s*2.5)], fill=col, width=max(1, int(s/2)))
        # 中心白コア
        draw_obj.ellipse([self.cx - s, self.cy - s, self.cx + s, self.cy + s], fill=col_core)

class HighEndCircleBurst:
    """多重ネオンリング ＋ 中心フラッシュ ＋ ダイヤ粒子群"""
    def __init__(self, cx, cy, color, max_radius=320, duration_frames=22):
        self.cx = cx
        self.cy = cy
        self.color = color  # (R, G, B)
        self.max_radius = max_radius
        self.duration = duration_frames
        self.age = 0
        self.is_dead = False
        
        # 放射状スパークル粒子
        self.particles = []
        num_particles = random.randint(16, 28)
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(6, 24)
            size = random.uniform(2.5, 6.0)
            life = random.randint(14, 22)
            self.particles.append(DiamondSparkle(cx, cy, color, speed, angle, size, life))

    def update(self):
        self.age += 1
        for p in self.particles:
            p.update()
        if self.age >= self.duration and all(p.life <= 0 for p in self.particles):
            self.is_dead = True

    def draw(self, draw_obj: ImageDraw.ImageDraw):
        progress = self.age / self.duration
        r_c, g_c, b_c = self.color
        
        if progress < 1.0:
            # 3次イージング (Cubic Ease-Out)
            t = 1.0 - math.pow(1.0 - progress, 3)
            r = self.max_radius * t
            alpha = int(255 * (1.0 - progress))
            
            # 1. 中心フラッシュグロー (瞬間的な発光)
            if progress < 0.35:
                flash_alpha = int(220 * (1.0 - progress / 0.35))
                flash_r = 45 * (1.0 - progress / 0.35)
                draw_obj.ellipse([self.cx - flash_r, self.cy - flash_r, self.cx + flash_r, self.cy + flash_r], 
                                 fill=(255, 255, 255, flash_alpha))

            # 2. メインネオンリング
            line_w = max(1, int(5 * (1.0 - progress)))
            draw_obj.ellipse([self.cx - r, self.cy - r, self.cx + r, self.cy + r], 
                             outline=(r_c, g_c, b_c, alpha), width=line_w)

            # 3. 外側セカンダリリング（遅れて広がる細リング）
            if progress > 0.08:
                t2 = 1.0 - math.pow(1.0 - (progress - 0.08) / 0.92, 3)
                r2 = (self.max_radius * 0.85) * t2
                alpha2 = int(alpha * 0.75)
                draw_obj.ellipse([self.cx - r2, self.cy - r2, self.cx + r2, self.cy + r2], 
                                 outline=(255, 255, 255, alpha2), width=max(1, line_w - 1))

            # 4. サード微小リング
            if progress > 0.16:
                t3 = 1.0 - math.pow(1.0 - (progress - 0.16) / 0.84, 3)
                r3 = (self.max_radius * 0.65) * t3
                alpha3 = int(alpha * 0.5)
                draw_obj.ellipse([self.cx - r3, self.cy - r3, self.cx + r3, self.cy + r3], 
                                 outline=(r_c, g_c, b_c, alpha3), width=1)

        # スパークル粒子の描画
        for p in self.particles:
            p.draw(draw_obj)

def render_high_end_test():
    print("🎵 Step 1: Analyzing audio dynamics and beat peaks...")
    with wave.open(str(AUDIO_FILE), "rb") as wf:
        n_ch = wf.getnchannels()
        sr = wf.getframerate()
        n_fr = wf.getnframes()
        raw = wf.readframes(int(min(n_fr, TEST_DURATION_SEC * sr)))
        
    audio_data = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_ch)
    audio_mono = np.abs(audio_data.mean(axis=1) / 32768.0)
    
    total_frames = int(TEST_DURATION_SEC * FPS)
    samples_per_frame = int(sr / FPS)
    
    frame_energies = np.zeros(total_frames)
    for f in range(total_frames):
        st = f * samples_per_frame
        en = min(st + samples_per_frame, len(audio_mono))
        frame_energies[f] = np.mean(audio_mono[st:en])
        
    threshold = np.percentile(frame_energies, 68)
    burst_frames = []
    last_burst = -10
    for f in range(1, total_frames - 1):
        if frame_energies[f] > threshold and frame_energies[f] > frame_energies[f-1] * 1.12 and (f - last_burst) > 7:
            burst_frames.append(f)
            last_burst = f
            
    print(f"  Detected {len(burst_frames)} dynamic burst triggers.")

    bg_raw = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    out_video = OUTPUT_DIR / "TEST_HIGH_END_CIRCLE_BURST_10S.mp4"
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
    
    active_bursts = []
    neon_colors = [
        (0, 229, 255),    # Electric Cyan
        (255, 0, 140),    # Neon Hot Pink
        (0, 255, 190),    # Bright Emerald
        (255, 215, 0),    # Sunlight Gold
        (160, 90, 255),   # Mystic Violet
        (255, 110, 0)     # Solar Orange
    ]
    
    # 発生ポイント（ヘッドホンの光輪付近、髪先、瞳の視線先、中心など）
    focal_points = [
        (1580, 500),      # 右側ヘッドホン発光部
        (960, 540),       # 画面中央
        (820, 480),       # 左頬・瞳の周辺
        (1100, 480),      # 右頬
        (960, 300),       # 頭頂部・光の差し込み
        (700, 650),       # 左下の髪の広がり
        (1220, 650),      # 右下の髪の広がり
    ]

    print("🎬 Step 2: Rendering High-End Neon Bursts with Gaussian Bloom...")
    
    for f in range(total_frames):
        if f in burst_frames:
            cx, cy = random.choice(focal_points)
            col = random.choice(neon_colors)
            active_bursts.append(HighEndCircleBurst(
                cx, cy, col, 
                max_radius=random.randint(260, 420), 
                duration_frames=random.randint(18, 24)
            ))
            
        frame = bg_raw.copy()
        
        # エフェクト描画用透過レイヤー
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d_over = ImageDraw.Draw(overlay)
        
        for burst in active_bursts:
            burst.draw(d_over)
            burst.update()
            
        active_bursts = [b for b in active_bursts if not b.is_dead]
        
        # 2段階ネオンブルーム（強烈な発光感）
        bloom_wide = overlay.filter(ImageFilter.GaussianBlur(radius=12))
        bloom_tight = overlay.filter(ImageFilter.GaussianBlur(radius=4))
        
        final_frame = Image.alpha_composite(frame, bloom_wide)
        final_frame = Image.alpha_composite(final_frame, bloom_tight)
        final_frame = Image.alpha_composite(final_frame, overlay)
        
        # プレビュー保存（最も弾けている瞬間）
        if f == 75:
            preview_path = OUTPUT_DIR / "preview_high_end_burst.jpg"
            final_frame.convert("RGB").save(str(preview_path), quality=95)
            
        process.stdin.write(final_frame.tobytes())
        
    process.stdin.close()
    process.wait()
    print(f"🎉 High-End Burst video rendered: {out_video}")
    return out_video, OUTPUT_DIR / "preview_high_end_burst.jpg"

if __name__ == "__main__":
    render_high_end_test()
