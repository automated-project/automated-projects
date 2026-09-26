#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 1時間Mix収録曲から未Shorts化トラック3選のレンダリングスクリプト
- 1. Asphalt_Fang_Strike.wav (1時間Mix #02)
- 2. Venom_On_Asphalt.wav (1時間Mix #03)
- 3. Grim_Asphalt_Reaper.wav (1時間Mix #04)
- 音響: マスタリング済みWAV (mastered_audio/wav/) からドロップ抽出
- 映像: 9:16 Full HD 30fps / 48本波形バー / 重低音連動パルス / Futuraネオングロー
- 出力先: output_videos/shorts/ (※YouTubeアップロードは行わない)
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
MASTERED_WAV_DIR = BASE_DIR / "mastered_audio/wav"
BG_SHORTS_DIR = BASE_DIR / "cover_art/bg_shorts"
OUT_DIR = BASE_DIR / "output_videos/shorts"
TEMP_DIR = BASE_DIR / "output_videos/temp_shorts_1hour_tracks"

OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

FPS = 30
WIDTH = 1080
HEIGHT = 1920

NUM_BARS = 48
BAR_WIDTH = 12
BAR_GAP = 6
MAX_BAR_HEIGHT = 52
MIN_BAR_HEIGHT = 6
BOTTOM_MARGIN = 340
TOTAL_WIDTH = NUM_BARS * BAR_WIDTH + (NUM_BARS - 1) * BAR_GAP
START_X = (WIDTH - TOTAL_WIDTH) // 2
BASE_Y = HEIGHT - BOTTOM_MARGIN

FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"

# 1時間Mix収録曲から未Shorts化トラック3選
SHORTS_QUEUE = [
    {
        "id": "shorts_1h_01_asphalt_fang_strike",
        "wav_name": "Asphalt_Fang_Strike.wav",
        "bg_name": "bg_power_rack.jpeg",
        "start_sec": 20.0,
        "duration_sec": 20.0,
        "text_main": "HARDCORE GYM MOTIVATION",
        "text_sub": "HEAVY BASS DROP",
        "glow_color": (255, 30, 60),  # Crimson Red
        "out_file": "SHORTS_CH2_1H_TRACK_01_ASPHALT_FANG_STRIKE.mp4"
    },
    {
        "id": "shorts_1h_02_venom_on_asphalt",
        "wav_name": "Venom_On_Asphalt.wav",
        "bg_name": "bg_dark_combat_shorts.jpeg",
        "start_sec": 22.0,
        "duration_sec": 20.0,
        "text_main": "BRUTAL BEAST MODE",
        "text_sub": "PURE ADRENALINE",
        "glow_color": (0, 220, 255),  # Electric Cyan
        "out_file": "SHORTS_CH2_1H_TRACK_02_VENOM_ON_ASPHALT.mp4"
    },
    {
        "id": "shorts_1h_03_grim_asphalt_reaper",
        "wav_name": "Grim_Asphalt_Reaper.wav",
        "bg_name": "bg_gym_shorts.jpeg",
        "start_sec": 18.0,
        "duration_sec": 20.0,
        "text_main": "EXTREME GYM PR PHONK",
        "text_sub": "MAXIMUM EFFORT",
        "glow_color": (255, 110, 20),  # Sunset Gold
        "out_file": "SHORTS_CH2_1H_TRACK_03_GRIM_ASPHALT_REAPER.mp4"
    }
]

def load_futura_font(size, index=0):
    try:
        return ImageFont.truetype(FUTURA_PATH, size, index=index)
    except Exception:
        return ImageFont.load_default()

def create_text_overlay(width, height, text_main, text_sub, glow_color):
    font_main = load_futura_font(56, index=0)  # Futura Medium
    font_sub = load_futura_font(32, index=0)

    glow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)

    y_main = 280
    y_sub = 355

    bbox_m = font_main.getbbox(text_main)
    w_m = bbox_m[2] - bbox_m[0]
    x_m = (width - w_m) // 2

    bbox_s = font_sub.getbbox(text_sub)
    w_s = bbox_s[2] - bbox_s[0]
    x_s = (width - w_s) // 2

    glow_rgb = glow_color
    glow_draw.text((x_m, y_main), text_main, font=font_main, fill=(glow_rgb[0], glow_rgb[1], glow_rgb[2], 240))
    glow_draw.text((x_s, y_sub), text_sub, font=font_sub, fill=(glow_rgb[0], glow_rgb[1], glow_rgb[2], 200))
    
    glow_blurred = glow_img.filter(ImageFilter.GaussianBlur(radius=10))

    text_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    text_overlay = Image.alpha_composite(text_overlay, glow_blurred)
    draw = ImageDraw.Draw(text_overlay)
    
    draw.text((x_m, y_main), text_main, font=font_main, fill=(255, 255, 255, 255))
    draw.text((x_s, y_sub), text_sub, font=font_sub, fill=(240, 240, 240, 230))

    return text_overlay

def render_single_shorts(item):
    print(f"\n==================================================", flush=True)
    print(f"▶ RENDERING 1-HOUR TRACK SHORTS: {item['id']}", flush=True)
    print(f"  Track: {item['wav_name']} | BG: {item['bg_name']}", flush=True)
    print(f"  Text: '{item['text_main']}' / '{item['text_sub']}'", flush=True)
    print(f"==================================================", flush=True)

    wav_path = MASTERED_WAV_DIR / item["wav_name"]
    bg_path = BG_SHORTS_DIR / item["bg_name"]
    out_path = OUT_DIR / item["out_file"]
    hook_wav = TEMP_DIR / f"hook_{item['id']}.wav"

    if not wav_path.exists():
        print(f"❌ Error: Audio file not found: {wav_path}", flush=True)
        return False
    if not bg_path.exists():
        print(f"❌ Error: Background file not found: {bg_path}", flush=True)
        return False

    with wave.open(str(wav_path), 'rb') as wf:
        sr = wf.getframerate()
        n_channels = wf.getnchannels()
        s_sample = int(item["start_sec"] * sr)
        e_sample = s_sample + int(item["duration_sec"] * sr)
        wf.setpos(s_sample)
        raw = wf.readframes(e_sample - s_sample)

    hook_audio = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_channels).copy()

    fade_samples = int(sr * 0.25)
    fo = np.linspace(1.0, 0.0, fade_samples)[:, None]
    hook_audio[-fade_samples:] = (hook_audio[-fade_samples:].astype(np.float32) * fo).astype(np.int16)

    with wave.open(str(hook_wav), 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(hook_audio.tobytes())

    duration = len(hook_audio) / sr
    audio_mono = 0.5 * (hook_audio[:, 0].astype(np.float32) + hook_audio[:, 1].astype(np.float32)) / 32768.0
    samples_per_frame = sr // FPS
    total_frames = len(audio_mono) // samples_per_frame
    print(f"[+] Audio Drop Extracted: {duration:.2f}s ({total_frames} frames)", flush=True)

    orig_bg = Image.open(bg_path).convert("RGBA")
    img_w, img_h = orig_bg.size
    target_ratio = WIDTH / HEIGHT
    cur_ratio = img_w / img_h

    if cur_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        orig_bg = orig_bg.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        orig_bg = orig_bg.crop((0, top, img_w, top + new_h))

    OVER_W = int(WIDTH * 1.06)
    OVER_H = int(HEIGHT * 1.06)
    bg_oversized = orig_bg.resize((OVER_W, OVER_H), Image.Resampling.LANCZOS)

    text_overlay = create_text_overlay(WIDTH, HEIGHT, item["text_main"], item["text_sub"], item["glow_color"])

    fft_size = 2048
    freq_bins = np.geomspace(40, 14000, NUM_BARS + 1)
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)
    freq_weights = np.zeros(NUM_BARS)
    for b in range(NUM_BARS):
        f_center = (freq_bins[b] * freq_bins[b+1]) ** 0.5
        freq_weights[b] = (f_center / 100.0) ** 0.50 * 18.0
    bass_idx = np.where((freqs >= 40) & (freqs <= 160))[0]

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(hook_wav),
        "-c:v", "h264_videotoolbox",
        "-b:v", "5000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_path)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    prev_heights = np.zeros(NUM_BARS)
    prev_pulse = 0.0
    hanning_win = np.hanning(fft_size)

    for f_idx in range(total_frames):
        start_s = f_idx * samples_per_frame
        chunk = audio_mono[start_s : start_s + fft_size]
        if len(chunk) < fft_size:
            chunk = np.pad(chunk, (0, fft_size - len(chunk)))

        windowed = chunk * hanning_win
        spectrum = np.abs(np.fft.rfft(windowed)) / (fft_size / 2)

        bass_energy = np.mean(spectrum[bass_idx]) * 15.0
        target_pulse = np.clip((bass_energy - 0.12) * 1.5, 0.0, 1.0)
        if target_pulse > prev_pulse:
            pulse = target_pulse
        else:
            pulse = prev_pulse * 0.78
        prev_pulse = pulse

        scale = 1.00 + (pulse ** 1.2) * 0.035
        cur_w = int(WIDTH * scale)
        cur_h = int(HEIGHT * scale)
        crop_x = (OVER_W - cur_w) // 2
        crop_y = (OVER_H - cur_h) // 2

        frame = bg_oversized.crop((crop_x, crop_y, crop_x + cur_w, crop_y + cur_h)).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)

        target_heights = np.zeros(NUM_BARS)
        for b in range(NUM_BARS):
            idx_range = np.where((freqs >= freq_bins[b]) & (freqs < freq_bins[b+1]))[0]
            if len(idx_range) > 0:
                val = np.mean(spectrum[idx_range])
            else:
                closest_idx = np.argmin(np.abs(freqs - (freq_bins[b] + freq_bins[b+1])/2))
                val = spectrum[closest_idx]
            adj = np.clip(val * freq_weights[b], 0.0, 1.0)
            target_heights[b] = MIN_BAR_HEIGHT + (adj ** 0.85) * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)

        smooth_heights = np.zeros(NUM_BARS)
        for b in range(NUM_BARS):
            if target_heights[b] >= prev_heights[b]:
                smooth_heights[b] = target_heights[b]
            else:
                smooth_heights[b] = max(MIN_BAR_HEIGHT, prev_heights[b] * 0.82)
        prev_heights = smooth_heights

        vis_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_vis = ImageDraw.Draw(vis_overlay)
        for b in range(NUM_BARS):
            h = int(smooth_heights[b])
            x0 = START_X + b * (BAR_WIDTH + BAR_GAP)
            x1 = x0 + BAR_WIDTH
            y1 = BASE_Y
            y0 = BASE_Y - h
            draw_vis.rounded_rectangle([x0, y0, x1, y1], radius=4, fill=(255, 255, 255, 220), outline=(255, 255, 255, 255), width=1)

        frame = Image.alpha_composite(frame, vis_overlay)
        frame = Image.alpha_composite(frame, text_overlay)

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()

    if hook_wav.exists():
        hook_wav.unlink()

    print(f"✅ Render Complete: {out_path} ({duration:.2f}s)", flush=True)
    return True

def main():
    sys.stdout.reconfigure(line_buffering=True)
    print("==================================================", flush=True)
    print("🚀 PHONK SHORTS: 1-HOUR MIX TRACKS (BATCH 3)", flush=True)
    print(f"   Output Dir: {OUT_DIR}", flush=True)
    print("==================================================", flush=True)

    success_count = 0
    for item in SHORTS_QUEUE:
        if render_single_shorts(item):
            success_count += 1

    print(f"\n🎉 Finished: {success_count}/{len(SHORTS_QUEUE)} Shorts rendered successfully!", flush=True)

if __name__ == "__main__":
    main()
