# -*- coding: utf-8 -*-
"""
Ch3 AuraMelody Audio - Official Video Visual FX Engine
(真のサビタイミング完全一致版：37.0s ＆ 150.0s / 2分30秒)

【確定仕様】
1. 光（浮遊オーブ）：音響非連動。一定速度でゆったりと自然呼吸しながら漂う環境光（少数・淡色）。
2. 通常区間（平歌）：約10秒に1回、高濃度クッキリで単体（丸 or 紙吹雪）が一瞬アクセント。
3. サビ（1曲につき計2回）：
   - サビ1: 37.0秒（1番サビ）
   - サビ2: 150.0秒（2分30秒・ラスサビ）
   - 【サビ1セット】＝「丸と紙吹雪がそれぞれ独立した別々の場所で同時に弾ける」× 連続2回（0.5秒差）。
   - 滞在時間 1.5〜2.0秒、高発色（alpha 245）で優雅に舞い散る。
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
OUTPUT_VIDEO_PATH = OUTPUT_DIR / "FULL_TRACK_PERFECT_TIMING_176S.mp4"
PREVIEW_IMAGE_PATH = OUTPUT_DIR / "preview_perfect_timing_fx.jpg"

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# ==========================================
# 1. 浮遊光ボケオーブ（音響非連動・スロー環境光）
# ==========================================
class SteadyFloatingOrb:
    def __init__(self, x=None, y=None, layer="mid"):
        self.layer = layer
        self.x = x if x is not None else random.uniform(0, WIDTH)
        self.y = y if y is not None else random.uniform(0, HEIGHT + 100)
        
        if layer == "large_fg":
            self.base_radius = random.uniform(55, 90)
            self.base_alpha = random.uniform(28, 50)
            self.vy = random.uniform(-0.35, -0.15)
            self.drift_amp = random.uniform(0.8, 1.5)
        elif layer == "mid":
            self.base_radius = random.uniform(14, 26)
            self.base_alpha = random.uniform(55, 95)
            self.vy = random.uniform(-0.5, -0.22)
            self.drift_amp = random.uniform(0.5, 1.1)
        else: # "small_dust"
            self.base_radius = random.uniform(3, 6)
            self.base_alpha = random.uniform(85, 135)
            self.vy = random.uniform(-0.35, -0.18)
            self.drift_amp = random.uniform(0.3, 0.7)
            
        self.phase_x = random.uniform(0, math.pi * 2)
        self.speed_x = random.uniform(0.012, 0.025)
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.pulse_speed = random.uniform(0.02, 0.04)
        
        colors = [
            (255, 240, 200),  # Soft Gold
            (255, 220, 180),  # Pale Amber
            (210, 245, 255),  # Airy Cyan
            (255, 220, 235),  # Soft Rose
            (255, 255, 255),  # Pure White
        ]
        self.color = random.choice(colors)

    def update(self):
        self.phase_x += self.speed_x
        self.pulse_phase += self.pulse_speed
        self.x += math.sin(self.phase_x) * self.drift_amp
        self.y += self.vy
        
        if self.y < -100:
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

# ==========================================
# 2. 紙吹雪（クッキリ高濃度・独立発火）
# ==========================================
class SolidConfettiPiece:
    def __init__(self, cx, cy, is_climax=False):
        self.is_climax = is_climax
        self.cx = cx + random.uniform(-60, 60)
        self.cy = cy + random.uniform(-50, 50)
        
        angle = random.uniform(0, 2 * math.pi)
        if is_climax:
            speed = random.uniform(10.0, 28.0)
            self.gravity = random.uniform(0.12, 0.26)
            self.w = random.uniform(9, 17)
            self.h = random.uniform(14, 24)
            self.max_life = random.randint(45, 60)     # 約1.5〜2.0秒滞在
            self.base_alpha = 245                      # クッキリ高発色
            palette = [
                (255, 120, 180),  # Vivid Deep Rose
                (255, 215, 0),    # Rich Gold
                (100, 220, 255),  # Electric Cyan
                (255, 230, 80),   # Bright Sun Yellow
                (200, 140, 255),  # Vivid Violet
                (255, 160, 110),  # Bright Coral
                (255, 255, 255),  # Pure White
            ]
        else:
            speed = random.uniform(8.0, 20.0)
            self.gravity = random.uniform(0.25, 0.42)
            self.w = random.uniform(8, 14)
            self.h = random.uniform(12, 18)
            self.max_life = random.randint(16, 22)     # 約0.55〜0.75秒
            self.base_alpha = 205                      # 通常時もしっかり視認
            palette = [
                (255, 160, 195), (150, 215, 255), (255, 230, 140),
                (180, 245, 190), (220, 180, 255), (255, 255, 255)
            ]
            
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle) - random.uniform(2.5, 6.5)
        self.rot = random.uniform(0, 360)
        self.rot_speed = random.uniform(-18, 18)
        self.flutter_phase = random.uniform(0, math.pi * 2)
        self.flutter_speed = random.uniform(0.2, 0.35)
        self.life = self.max_life
        self.color = random.choice(palette)

    def update(self):
        self.cx += self.vx
        self.cy += self.vy
        self.vy += self.gravity
        damping = 0.90 if self.is_climax else 0.88
        self.vx *= damping
        self.vy *= damping
        self.rot += self.rot_speed
        self.flutter_phase += self.flutter_speed
        self.life -= 1

    def draw(self, draw: ImageDraw.ImageDraw):
        if self.life <= 0:
            return
        life_ratio = self.life / self.max_life
        alpha_factor = min(1.0, life_ratio * 1.6)
        alpha = int(self.base_alpha * alpha_factor)
        
        r, g, b = self.color
        fill_col = (r, g, b, alpha)
        
        flutter_scale = math.cos(self.flutter_phase)
        curr_w = max(2.5, abs(self.w * flutter_scale))
        curr_h = self.h
        
        rad = math.radians(self.rot)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        hw, hh = curr_w / 2.0, curr_h / 2.0
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        pts = [(self.cx + x * cos_a - y * sin_a, self.cy + x * sin_a + y * cos_a) for x, y in corners]
        draw.polygon(pts, fill=fill_col)

class SolidConfettiBurst:
    def __init__(self, cx, cy, is_climax=False):
        num_pieces = random.randint(90, 130) if is_climax else random.randint(40, 55)
        self.particles = [SolidConfettiPiece(cx, cy, is_climax) for _ in range(num_pieces)]
        self.is_dead = False

    def update(self):
        alive = False
        for p in self.particles:
            p.update()
            if p.life > 0:
                alive = True
        if not alive:
            self.is_dead = True

    def draw(self, draw: ImageDraw.ImageDraw):
        for p in self.particles:
            p.draw(draw)

# ==========================================
# 3. サークルバースト（クッキリ鮮明リング・独立発火）
# ==========================================
class SolidCircleBurst:
    def __init__(self, cx, cy, is_climax=False):
        self.cx = cx
        self.cy = cy
        self.is_climax = is_climax
        if is_climax:
            self.max_radius = random.uniform(360, 480)
            self.duration = 28   # 約0.93秒
            self.base_alpha = 245
            self.line_w = 6
        else:
            self.max_radius = random.uniform(240, 320)
            self.duration = 18   # 約0.6秒
            self.base_alpha = 205
            self.line_w = 4
            
        self.age = 0
        self.is_dead = False
        
        palette = [
            (255, 220, 100),  # Rich Gold
            (140, 230, 255),  # Vivid Cyan
            (255, 160, 210),  # Vivid Rose
            (255, 255, 255),  # Pure White
        ]
        self.color = random.choice(palette)

    def update(self):
        self.age += 1
        if self.age >= self.duration:
            self.is_dead = True

    def draw(self, draw: ImageDraw.ImageDraw):
        if self.is_dead:
            return
        p = self.age / self.duration
        ease_p = 1.0 - (1.0 - p) ** 2
        r = self.max_radius * ease_p
        alpha = int(self.base_alpha * (1.0 - p))
        
        r_c, g_c, b_c = self.color
        col = (r_c, g_c, b_c, alpha)
        
        w = max(1, int(self.line_w * (1.0 - p * 0.6)))
        draw.ellipse([self.cx - r, self.cy - r, self.cx + r, self.cy + r], outline=col, width=w)
        
        inner_r1 = max(1, r * 0.76)
        inner_alpha1 = int(alpha * 0.75)
        draw.ellipse([self.cx - inner_r1, self.cy - inner_r1, self.cx + inner_r1, self.cy + inner_r1], outline=(r_c, g_c, b_c, inner_alpha1), width=max(1, w - 1))
        
        if self.is_climax:
            inner_r2 = max(1, r * 0.50)
            inner_alpha2 = int(alpha * 0.55)
            draw.ellipse([self.cx - inner_r2, self.cy - inner_r2, self.cx + inner_r2, self.cy + inner_r2], outline=(255, 255, 255, inner_alpha2), width=2)

def main():
    print("🚀 [Step 1] Loading assets & setting exact chorus timing (37.0s & 150.0s)...")
    bg_img = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    with wave.open(str(AUDIO_FILE), 'rb') as wf:
        total_sec = wf.getnframes() / wf.getframerate()
        total_frames = int(total_sec * FPS)
        
    print(f"🎵 Audio Duration: {total_sec:.2f}s | Total Frames: {total_frames}")
    
    # サビの正確なタイミング（秒 ➔ フレーム）
    climax_seconds = [37.0, 150.0]
    climax_frames = [int(s * FPS) for s in climax_seconds]
    print(f"🎯 [Exact Chorus Timing] Chorus 1: {climax_seconds[0]}s (F{climax_frames[0]}) | Chorus 2: {climax_seconds[1]}s (F{climax_frames[1]})")
    
    # 浮遊光オーブ（音響非連動・スロー環境光：計20個）
    orbs = [SteadyFloatingOrb(layer="large_fg") for _ in range(3)]
    orbs += [SteadyFloatingOrb(layer="mid") for _ in range(7)]
    orbs += [SteadyFloatingOrb(layer="small_dust") for _ in range(10)]

    active_bursts = []
    
    # サビ演出スケジュール（サビ1セット ＝ 丸と紙吹雪が独立した別々の場所で同時に弾ける × 連続2回）
    scheduled_events = []
    for c_frame in climax_frames:
        # 第1波（t = 0秒）
        circle_cx1 = random.uniform(WIDTH * 0.20, WIDTH * 0.42)
        circle_cy1 = random.uniform(HEIGHT * 0.25, HEIGHT * 0.55)
        confetti_cx1 = random.uniform(WIDTH * 0.58, WIDTH * 0.80)
        confetti_cy1 = random.uniform(HEIGHT * 0.25, HEIGHT * 0.55)
        
        scheduled_events.append((c_frame, "circle", circle_cx1, circle_cy1, True))
        scheduled_events.append((c_frame, "confetti", confetti_cx1, confetti_cy1, True))
        
        # 第2波（t = +0.5秒後 / 15フレーム後）
        circle_cx2 = random.uniform(WIDTH * 0.55, WIDTH * 0.78)
        circle_cy2 = random.uniform(HEIGHT * 0.30, HEIGHT * 0.60)
        confetti_cx2 = random.uniform(WIDTH * 0.22, WIDTH * 0.45)
        confetti_cy2 = random.uniform(HEIGHT * 0.30, HEIGHT * 0.60)
        
        scheduled_events.append((c_frame + 15, "circle", circle_cx2, circle_cy2, True))
        scheduled_events.append((c_frame + 15, "confetti", confetti_cx2, confetti_cy2, True))
    
    # 通常時の約10秒に1回アクセント用（サビ前後5秒間は除外）
    normal_cooldown = int(9.5 * FPS)
    cooldown = 90
    effect_toggle = 0
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
    
    print(f"🎬 [Step 2] Rendering Full Track with Exact Chorus Timing to {OUTPUT_VIDEO_PATH.name}...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    for f in range(total_frames):
        cooldown -= 1
        
        # 1. 予約されたサビ演出
        current_events = [ev for ev in scheduled_events if ev[0] == f]
        for _, fx_type, cx, cy, is_clx in current_events:
            if fx_type == "circle":
                active_bursts.append(SolidCircleBurst(cx, cy, is_climax=True))
            elif fx_type == "confetti":
                active_bursts.append(SolidConfettiBurst(cx, cy, is_climax=True))
            cooldown = int(6.0 * FPS)
            
        # 2. 通常区間のアクセント（サビ前後5秒間は休止）
        if cooldown <= 0:
            is_near_climax = any(abs(f - c) < int(5.0 * FPS) for c in climax_frames)
            if not is_near_climax:
                cx = random.uniform(WIDTH * 0.25, WIDTH * 0.75)
                cy = random.uniform(HEIGHT * 0.25, HEIGHT * 0.65)
                if effect_toggle % 2 == 0:
                    active_bursts.append(SolidCircleBurst(cx, cy, is_climax=False))
                else:
                    active_bursts.append(SolidConfettiBurst(cx, cy, is_climax=False))
                effect_toggle += 1
                cooldown = normal_cooldown + random.randint(-15, 25)
                
        # 3. 浮遊光の更新
        for orb in orbs:
            orb.update()
            
        # 4. バースト演出の更新
        for b in active_bursts:
            b.update()
        active_bursts = [b for b in active_bursts if not b.is_dead]
        
        # 5. 描画合成
        frame_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_layer)
        
        for orb in orbs:
            orb.draw(draw)
            
        for b in active_bursts:
            b.draw(draw)
            
        final_frame = Image.alpha_composite(bg_img, frame_layer)
        
        # 37秒サビの第2波発火の瞬間（f = 37.0s + 18F）をプレビュー保存
        if not preview_saved and f == climax_frames[0] + 18:
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
        
    print(f"✨ [Success] Full Track Render Complete: {OUTPUT_VIDEO_PATH}")
    print(f"🖼 Preview Image Saved: {PREVIEW_IMAGE_PATH}")

if __name__ == "__main__":
    main()
