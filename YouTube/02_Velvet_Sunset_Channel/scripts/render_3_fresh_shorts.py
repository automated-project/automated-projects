#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 完全未採用トラック3選によるShorts動画レンダリングスクリプト
- 過去の公開動画（30M, 1H, 全Shorts 10本）と1曲も被らない完全未採用トラックのみを使用
- 1. Titanium_Fist.mp4 (旧 Iron_Clenched)
- 2. Colosseum_Of_Iron.mp4 (旧 Iron_Jaw_Arena)
- 3. Apex_Drift_Lock.mp4 (旧 Grip_Locked_Hard)
- 音響: Extreme Sub-Bass Calibration (-14.0 LUFS / 55Hz+8.5dB / 80Hz+2.5dB / 10kHz+1.5dB)
- 映像: 9:16 Full HD 30fps, 48本波形バー, 重低音連動パルス, Futuraネオングロー
- 出力: output_videos/shorts/ (※YouTubeアップロードは行わない)
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
RAW_AUDIO_DIR = BASE_DIR / "raw_audio"
BG_SHORTS_DIR = BASE_DIR / "cover_art/bg_shorts"
OUT_DIR = BASE_DIR / "output_videos/shorts"
TEMP_DIR = BASE_DIR / "output_videos/temp_shorts_fresh"

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

# 完全未採用トラック3曲のキュー
SHORTS_QUEUE = [
    {
        "id": "shorts_fresh_01_titanium_fist",
        "raw_file": "Titanium_Fist.mp4",
        "bg_name": "bg_power_rack.jpeg",
        "start_sec": 20.0,
        "duration_sec": 20.0,
        "text_main": "HARDCORE GYM MOTIVATION",
        "text_sub": "TITANIUM POWER DROP",
        "glow_color": (255, 30, 60),  # Crimson Red
        "out_file": "SHORTS_CH2_FRESH_01_TITANIUM_FIST.mp4"
    },
    {
        "id": "shorts_fresh_02_colosseum_of_iron",
        "raw_file": "Colosseum_Of_Iron.mp4",
        "bg_name": "bg_dark_combat_shorts.jpeg",
        "start_sec": 22.0,
        "duration_sec": 20.0,
        "text_main": "BRUTAL BEAST MODE",
        "text_sub": "UNLEASH THE RAGE",
        "glow_color": (0, 220, 255),  # Electric Cyan
        "out_file": "SHORTS_CH2_FRESH_02_COLOSSEUM_OF_IRON.mp4"
    },
    {
        "id": "shorts_fresh_03_apex_drift_lock",
        "raw_file": "Apex_Drift_Lock.mp4",
        "bg_name": "bg_gym_shorts.jpeg",
        "start_sec": 18.0,
        "duration_sec": 20.0,
        "text_main": "EXTREME GYM PR PHONK",
        "text_sub": "MAXIMUM ADRENALINE",
        "glow_color": (255, 120, 20),  # Sunset Gold
        "out_file": "SHORTS_CH2_FRESH_03_APEX_DRIFT_LOCK.mp4"
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
    print(f"▶ RENDERING FRESH SHORTS: {item['id']}", flush=True)
    print(f"  Track: {item['raw_file']} | BG: {item['bg_name']}", flush=True)
    print(f"  Text: '{item['text_main']}' / '{item['text_sub']}'", flush=True)
    print(f"==================================================", flush=True)

    raw_path = RAW_AUDIO_DIR / item["raw_file"]
    bg_path = BG_SHORTS_DIR / item["bg_name"]
    out_path = OUT_DIR / item["out_file"]
    hook_wav = TEMP_DIR / f"hook_{item['id']}.wav"

    if not raw_path.exists():
        print(f"❌ Error: Audio file not found: {raw_path}", flush=True)
        return False
    if not bg_path.exists():
        print(f"❌ Error: Background file not found: {bg_path}", flush=True)
        return False

    # 1. Super Crisp Phonk Mastering & ドロップ切り出し
    # Ch2 仕様: 35Hzローカット, 55Hz+8.5dB, 80Hz+2.5dB, 10kHz+1.5dB, -14.0 LUFS
    af_chain = (
        "highpass=f=35,"
        "equalizer=f=55:t=q:w=1.2:g=8.5,"
        "equalizer=f=80:t=q:w=1.5:g=2.5,"
        "equalizer=f=3200:t=q:w=1.2:g=-1.0,"
        "equalizer=f=10000:t=q:w=1.0:g=1.5,"
        "loudnorm=I=-14.0:TP=-1.5:LRA=7"
    )

    temp_master_wav = TEMP_DIR / f"mastered_{item['id']}.wav"
    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(raw_path),
        "-vn",
        "-af", af_chain,
        "-ar", "44100",
        "-ac", "2",
        "-c:a", "pcm_s16le",
        str(temp_master_wav)
    ]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # ドロップ切り出し
    with wave.open(str(temp_master_wav), 'rb') as wf:
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

    if temp_master_wav.exists():
        temp_master_wav.unlink()

    duration = len(hook_audio) / sr
    audio_mono = 0.5 * (hook_audio[:, 0].astype(np.float32) + hook_audio[:, 1].astype(np.float32)) / 32768.0
    samples_per_frame = sr // FPS
    total_frames = len(audio_mono) // samples_per_frame
    print(f"[+] Audio Drop Mastered & Extracted: {duration:.2f}s ({total_frames} frames)", flush=True)

    # 2. 背景画像準備（9:16 クロップ ＆ 6%オーバーサイズ）
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

    # 3. テキストオーバーレイ生成
    text_overlay = create_text_overlay(WIDTH, HEIGHT, item["text_main"], item["text_sub"], item["glow_color"])

    # 4. FFT周波数設定
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
    print("🚀 PHONK SHORTS FRESH BATCH (Zero Duplicate with Published Videos)")
    print(f"   Output Dir: {OUT_DIR}")
    print("==================================================", flush=True)

    success_count = 0
    for item in SHORTS_QUEUE:
        if render_single_shorts(item):
            success_count += 1

    print(f"\n🎉 Finished: {success_count}/{len(SHORTS_QUEUE)} Fresh Shorts rendered successfully!", flush=True)

if __name__ == "__main__":
    main()
