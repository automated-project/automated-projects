#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): 1時間長尺 Vol.3 ビルドスクリプト (完全改訂版)
- 冒頭1曲目: Golden Sun Embrace（Vol. 1, Vol. 2 と完全差別化）
- 重複排除・一意化された21曲厳選トラックリスト（約60分）
- 音響: SoftBass Transparent Mastering (-14.0 LUFS) + 2.5秒 DJ等エネルギー(cos/sin)クロスフェード
- 映像: 3層立体深度 浮遊光ボケオーブ（Pure Luminous Bokeh Light Orbs）
- 背景: cover_art/Gemini_Generated_Image_8ujyyo8ujyyo8ujy.jpeg
"""

import os
import sys
import wave
import math
import random
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
AUDIO_DIR = BASE_DIR / "raw_audio/1hour-mix"
BG_IMAGE_PATH = BASE_DIR / "cover_art/Gemini_Generated_Image_8ujyyo8ujyyo8ujy.jpeg"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_vol3_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUTPUT_DIR / "1HOUR_CRYSTAL_MELODIC_EDM_VOL3.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "1HOUR_CRYSTAL_MELODIC_EDM_VOL3_chapters.txt"
COMBINED_WAV = TEMP_DIR / "master_audio_vol3.wav"
ORB_LOOP_VIDEO = TEMP_DIR / "luminous_orbs_loop_15s.mp4"

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Vol. 1, Vol. 2 と被らない新曲順・完全一意トラック（全21曲・約60分）
SELECTED_TRACKS = [
    "Golden_Sun_Embrace.mp4",
    "Endless_Sky_Radiance.mp4",
    "Beyond_The_Horizon.mp4",
    "Crystal_Ocean_Breeze.mp4",
    "Daylight_Anthem.mp4",
    "Ocean_Drift_Melody.mp4",
    "Golden_Euphoria.mp4",
    "Infinite_Horizons.mp4",
    "Gateway_To_Light.mp4",
    "Healed_By_Golden_Light.mp4",
    "Zero_Gravity_Drive.mp4",
    "High_Above_The_Clouds.mp4",
    "A_Thousand_Memories.mp4",
    "Golden_Hour_Echoes.mp4",
    "Pure_Motion_Pulse.mp4",
    "Weightless_Ascent.mp4",
    "Tear_The_Clouds.mp4",
    "Hold_The_Starlit_Night.mp4",
    "Waiting_For_The_Rush.mp4",
    "Echoes_By_The_Door.mp4",
    "Golden_Sun_Embrace.mp4" # 爽快アンコール
]

def format_timestamp(sec: float) -> str:
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    else:
        return f"{mins:02d}:{secs:02d}"

# 浮遊光ボケオーブ クラス
class SteadyFloatingOrb:
    def __init__(self, x=None, y=None, layer="mid"):
        self.layer = layer
        self.x = x if x is not None else random.uniform(0, WIDTH)
        self.y = y if y is not None else random.uniform(0, HEIGHT + 100)
        
        if layer == "large_fg":
            self.base_radius = random.uniform(60, 100)
            self.base_alpha = random.uniform(25, 45)
            self.vy = random.uniform(-0.35, -0.15)
            self.drift_amp = random.uniform(0.8, 1.5)
        elif layer == "mid":
            self.base_radius = random.uniform(16, 30)
            self.base_alpha = random.uniform(60, 100)
            self.vy = random.uniform(-0.5, -0.22)
            self.drift_amp = random.uniform(0.5, 1.1)
        else: # small_dust
            self.base_radius = random.uniform(3, 7)
            self.base_alpha = random.uniform(90, 140)
            self.vy = random.uniform(-0.35, -0.18)
            self.drift_amp = random.uniform(0.3, 0.7)
            
        self.phase_x = random.uniform(0, math.pi * 2)
        self.speed_x = random.uniform(0.012, 0.025)
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.pulse_speed = random.uniform(0.02, 0.04)
        
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

def render_orbs_loop():
    print("✨ [Step 1] Rendering 15-second seamless Floating Light Orbs visual loop...", flush=True)
    bg_img = Image.open(BG_IMAGE_PATH).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    random.seed(42)
    orbs = []
    for _ in range(4):
        orbs.append(SteadyFloatingOrb(layer="large_fg"))
    for _ in range(8):
        orbs.append(SteadyFloatingOrb(layer="mid"))
    for _ in range(12):
        orbs.append(SteadyFloatingOrb(layer="small_dust"))

    total_frames = 15 * FPS # 15s * 30fps = 450 frames
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgba",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "h264_videotoolbox",
        "-b:v", "6000k",
        "-pix_fmt", "yuv420p",
        str(ORB_LOOP_VIDEO)
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    for frame_idx in range(total_frames):
        for o in orbs:
            o.update()
            
        orb_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d = ImageDraw.Draw(orb_layer)
        for o in orbs:
            o.draw(d)
            
        blurred_layer = orb_layer.filter(ImageFilter.GaussianBlur(radius=3.0))
        comp = Image.alpha_composite(bg_img, blurred_layer)
        proc.stdin.write(comp.tobytes())
        
    proc.stdin.close()
    proc.wait()
    print(f"✅ Floating Light Orbs visual loop rendered: {ORB_LOOP_VIDEO}", flush=True)

def master_and_stitch_audio():
    print("🎧 [Step 2] Mastering and stitching 21 tracks with 2.5s DJ crossfade...", flush=True)
    sample_rate = 48000
    crossfade_sec = 2.5
    crossfade_samples = int(crossfade_sec * sample_rate)

    t = np.linspace(0, np.pi / 2, crossfade_samples, endpoint=False, dtype=np.float32)
    fade_out_curve = np.cos(t)[:, np.newaxis]
    fade_in_curve = np.sin(t)[:, np.newaxis]

    # Ch3 SoftBass Transparent Mastering filter
    af_chain = (
        "highpass=f=30,"
        "equalizer=f=60:t=q:w=1.0:g=3.0,"
        "equalizer=f=3200:t=q:w=1.2:g=1.0,"
        "equalizer=f=12000:t=q:w=1.0:g=1.5,"
        "loudnorm=I=-14.0:TP=-1.5:LRA=10"
    )

    loaded_audios = []
    total_raw_samples = 0
    chapters = []

    for idx, fname in enumerate(SELECTED_TRACKS, start=1):
        raw_path = AUDIO_DIR / fname
        if not raw_path.exists():
            print(f"❌ Audio file not found: {raw_path}")
            sys.exit(1)

        title = fname.replace(".mp4", "").replace("_", " ").title()
        temp_wav = TEMP_DIR / f"temp_{idx:02d}.wav"

        # Apply Ch3 mastering
        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_path),
            "-vn",
            "-af", af_chain,
            "-ar", str(sample_rate),
            "-ac", "2",
            "-c:a", "pcm_s16le",
            str(temp_wav)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        with wave.open(str(temp_wav), "rb") as w:
            data = w.readframes(w.getnframes())
            arr = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            arr = arr.reshape(-1, 2)
            loaded_audios.append((title, arr))
            total_raw_samples += len(arr)

        if temp_wav.exists():
            temp_wav.unlink()

    num_transitions = len(loaded_audios) - 1
    total_master_samples = total_raw_samples - (num_transitions * crossfade_samples)
    master_audio = np.zeros((total_master_samples, 2), dtype=np.float32)
    current_pos = 0

    for i, (title, audio) in enumerate(loaded_audios):
        track_len = len(audio)
        if i == 0:
            chapters.append(f"{format_timestamp(0.0)} - {title}")
            master_audio[0:track_len] = audio
            current_pos = track_len
        else:
            track_start_sec = (current_pos - crossfade_samples) / sample_rate
            chapters.append(f"{format_timestamp(track_start_sec)} - {title}")

            blend_start = current_pos - crossfade_samples
            tail = master_audio[blend_start:current_pos]
            head = audio[:crossfade_samples]
            master_audio[blend_start:current_pos] = (tail * fade_out_curve) + (head * fade_in_curve)

            rem_len = track_len - crossfade_samples
            master_audio[current_pos : current_pos + rem_len] = audio[crossfade_samples:]
            current_pos += rem_len

    total_sec = total_master_samples / sample_rate
    print(f"✅ Total 1-Hour Master Duration: {format_timestamp(total_sec)} ({total_sec/60:.1f} mins)", flush=True)

    # Save Master Audio WAV
    master_audio_int16 = (np.clip(master_audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(COMBINED_WAV), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        chunk_size = 2000000
        for offset in range(0, len(master_audio_int16), chunk_size):
            chunk = master_audio_int16[offset:offset+chunk_size]
            w.writeframes(chunk.tobytes())

    # Save Chapters
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(chapters) + "\n")
    print(f"✅ Chapters file saved: {CHAPTERS_FILE}", flush=True)
    return total_sec

def render_final_video(total_sec):
    print("🎬 [Step 3] Multiplexing floating light orbs loop with 1-hour master audio...", flush=True)
    cmd_mux = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(ORB_LOOP_VIDEO),
        "-i", str(COMBINED_WAV),
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "h264_videotoolbox",
        "-b:v", "4000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        str(OUT_VIDEO)
    ]
    subprocess.run(cmd_mux, check=True)
    
    # Clean temp WAV
    if COMBINED_WAV.exists():
        COMBINED_WAV.unlink()
    if ORB_LOOP_VIDEO.exists():
        ORB_LOOP_VIDEO.unlink()
        
    print("\n" + "="*60, flush=True)
    print(f"🎉 1-HOUR CH3 VOL.3 RE-BUILD COMPLETE!", flush=True)
    print(f"   Output Video: {OUT_VIDEO}", flush=True)
    print(f"   Duration: {format_timestamp(total_sec)} ({total_sec/60:.1f} mins)", flush=True)
    print(f"   Chapters: {CHAPTERS_FILE}", flush=True)
    print("==================================================", flush=True)

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    render_orbs_loop()
    total_sec = master_and_stitch_audio()
    render_final_video(total_sec)
