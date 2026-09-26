# -*- coding: utf-8 -*-
"""
Floating Luminous Bokeh Orbs & Ambient Light Particle Engine
(空間をフワフワ漂い呼吸する光の丸・ボケオーブ演出エンジン)

- 大・中・小の多層深度ボケ（Foreground Large Bokeh + Midground Glowing Orbs + Background Floating Dust）
- サイン波浮遊シミュレーション（滑らかな上昇 ＆ 左右のふんわり揺らぎ）
- 呼吸するパルス発光 ＋ 音響連動グロー（Audio-Reactive Luminance）
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

class FloatingBokehOrb:
    """空間をフワフワと浮遊し、呼吸するように光る丸いオーブ"""
    def __init__(self, x=None, y=None, layer="mid"):
        self.layer = layer  # "large_fg", "mid", "small_dust"
        self.x = x if x is not None else random.uniform(0, WIDTH)
        self.y = y if y is not None else random.uniform(0, HEIGHT + 100)
        
        if layer == "large_fg":
            # 画面手前の大きな淡いボケ球
            self.base_radius = random.uniform(50, 110)
            self.base_alpha = random.uniform(35, 75)
            self.vy = random.uniform(-0.6, -0.2)
            self.drift_amp = random.uniform(1.2, 2.5)
        elif layer == "mid":
            # 空間を漂うメインの光球
            self.base_radius = random.uniform(16, 38)
            self.base_alpha = random.uniform(90, 160)
            self.vy = random.uniform(-1.2, -0.5)
            self.drift_amp = random.uniform(0.8, 1.8)
        else: # "small_dust"
            # キラキラ漂う微細な光の粉
            self.base_radius = random.uniform(3, 8)
            self.base_alpha = random.uniform(120, 200)
            self.vy = random.uniform(-0.8, -0.3)
            self.drift_amp = random.uniform(0.5, 1.2)
            
        # 揺らぎの位相と速度
        self.phase_x = random.uniform(0, math.pi * 2)
        self.speed_x = random.uniform(0.02, 0.05)
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.pulse_speed = random.uniform(0.04, 0.08)
        
        # 温かみのある光彩カラー（ゴールド、琥珀、淡いシアン、サンセットローズ、ピュアホワイト）
        colors = [
            (255, 235, 175),  # Warm Sunlight Gold
            (255, 210, 140),  # Sunset Amber
            (190, 245, 255),  # Crystal Cyan
            (255, 205, 225),  # Soft Rose
            (255, 255, 255),  # Pure Warm White
        ]
        self.color = random.choice(colors)

    def update(self, audio_energy_boost: float = 1.0):
        # 上昇と左右のふんわり揺らぎ
        self.phase_x += self.speed_x
        self.pulse_phase += self.pulse_speed
        
        self.x += math.sin(self.phase_x) * self.drift_amp
        self.y += self.vy
        
        # 画面上部から消えたら下から再出現
        if self.y < -120:
            self.y = HEIGHT + random.uniform(20, 80)
            self.x = random.uniform(0, WIDTH)

    def draw(self, draw: ImageDraw.ImageDraw, audio_boost: float = 1.0):
        # 呼吸するパルス発光 ＋ 音響連動
        pulse = 0.75 + 0.25 * math.sin(self.pulse_phase)
        alpha = int(np.clip(self.base_alpha * pulse * audio_boost, 0, 255))
        r = self.base_radius * (0.9 + 0.1 * pulse)
        
        r_c, g_c, b_c = self.color
        
        # 光球の外側グロー
        draw.ellipse([self.x - r, self.y - r, self.x + r, self.y + r], fill=(r_c, g_c, b_c, alpha))
        
        # 中心の明るいコア（中型・小型オーブのみ）
        if self.layer != "large_fg":
            core_r = r * 0.4
            core_alpha = int(min(255, alpha * 1.4))
            draw.ellipse([self.x - core_r, self.y - core_r, self.x + core_r, self.y + core_r], 
                         fill=(255, 255, 255, core_alpha))


def render_floating_orbs_video():
    print("✨ Step 1: Initializing Multi-Depth Floating Light Orbs & Audio Dynamics...")
    
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
        
    p95 = np.percentile(frame_energies, 95)
    if p95 > 0:
        norm_energies = np.clip(frame_energies / p95, 0.0, 1.5)
    else:
        norm_energies = np.zeros(total_frames)

    # オーブ群の生成（計70個の多層オーブ）
    orbs = []
    # 1. 画面手前の大ボケ球 (8個)
    for _ in range(8):
        orbs.append(FloatingBokehOrb(layer="large_fg"))
    # 2. 中型メイン光球 (28個)
    for _ in range(28):
        orbs.append(FloatingBokehOrb(layer="mid"))
    # 3. 背景微細光粉 (34個)
    for _ in range(34):
        orbs.append(FloatingBokehOrb(layer="small_dust"))

    bg_raw = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    out_video = OUTPUT_DIR / "TEST_FLOATING_LIGHT_ORBS_10S.mp4"
    
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
    print("🎬 Step 2: Rendering Floating Light Orbs with Soft Gaussian Bloom...")
    preview_saved = False
    
    for f in range(total_frames):
        audio_boost = 1.0 + 0.35 * norm_energies[f]
        
        # エフェクトレイヤー
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d_over = ImageDraw.Draw(overlay)
        
        for orb in orbs:
            orb.update(audio_boost)
            orb.draw(d_over, audio_boost)
            
        frame = bg_raw.copy()
        
        # 多層ソフトブルーム（光球が美しくにじむ）
        bloom_soft = overlay.filter(ImageFilter.GaussianBlur(radius=10))
        bloom_sharp = overlay.filter(ImageFilter.GaussianBlur(radius=3))
        
        final_frame = Image.alpha_composite(frame, bloom_soft)
        final_frame = Image.alpha_composite(final_frame, bloom_sharp)
        final_frame = Image.alpha_composite(final_frame, overlay)
        
        # プレビュー保存
        if f == 80 and not preview_saved:
            preview_path = OUTPUT_DIR / "preview_floating_light_orbs.jpg"
            final_frame.convert("RGB").save(str(preview_path), quality=95)
            preview_saved = True
            
        process.stdin.write(final_frame.tobytes())
        
    process.stdin.close()
    process.wait()
    print(f"🎉 Rendered Floating Light Orbs video: {out_video}")
    return out_video, OUTPUT_DIR / "preview_floating_light_orbs.jpg"

if __name__ == "__main__":
    render_floating_orbs_video()
