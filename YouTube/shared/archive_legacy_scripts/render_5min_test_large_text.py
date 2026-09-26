#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ch1 (Komorebi Chill Audio): 5分間テスト用 大文字タイマー ＆ ポモドーロ動画レンダラー
1. 2曲の集中音源をマスタリング（Warm EQ & -14 LUFS）
2. 2.5秒クロスフェード結合 ＋ 300秒（5分00秒）ジャスト着地（ラスト3秒フェードアウト）
3. 画面上部中央に特大Futuraテキスト（約72px）＋ プログレスバーを描画
4. 1080p 30fps MP4動画出力
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
RAW_DIR = BASE_DIR / "raw_audio/集中"
MASTERED_DIR = BASE_DIR / "mastered_audio/wav/focus"
OUT_DIR = BASE_DIR / "output_videos"
BG_IMAGE = BASE_DIR / "cover_art/bg_library_study.jpeg"
TEMP_DIR = BASE_DIR / "output_videos/temp_pomodoro_test"

MASTERED_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

TARGET_SEC = 300.0  # 5分00秒
WIDTH = 1920
HEIGHT = 1080
FPS = 30
FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"

TRACKS = [
    RAW_DIR / "A_Quiet_Corner_Table.mp4",
    RAW_DIR / "After_Hours_Window.mp4"
]

OUT_WAV = TEMP_DIR / "5min_study_session_mastered.wav"
OUT_VIDEO = OUT_DIR / "test_5min_pomodoro_large_text.mp4"

def master_and_combine_5min_audio():
    """2曲をマスタリングし、クロスフェードで結合してジャスト300秒（5分00秒）に整形"""
    print("=== [1/2] MASTERING & COMBINING 5-MINUTE AUDIO ===")
    
    # 1. 各曲をWAV抽出 & マスタリング
    temp_wavs = []
    audio_filter = (
        "highpass=f=35,"
        "equalizer=f=180:width_type=q:w=1.2:g=1.8,"
        "equalizer=f=3200:width_type=q:w=1.0:g=-1.5,"
        "highshelf=f=8500:g=-2.0,"
        "lowpass=f=15000,"
        "loudnorm=I=-14.0:TP=-1.5:LRA=7.0"
    )
    
    for idx, raw_f in enumerate(TRACKS):
        tmp_w = TEMP_DIR / f"temp_track_{idx}.wav"
        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_f),
            "-vn",
            "-af", audio_filter,
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "pcm_s16le",
            str(tmp_w)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        temp_wavs.append(tmp_w)

    # 2. Pythonで読み込み & クロスフェード結合
    sr = 48000
    audio_segments = []
    for tmp_w in temp_wavs:
        with wave.open(str(tmp_w), 'rb') as wf:
            n_frames = wf.getnframes()
            raw = wf.readframes(n_frames)
            data = np.frombuffer(raw, dtype=np.int16).reshape(-1, 2).astype(np.float32)
            audio_segments.append(data)

    # クロスフェード結合 (2.5秒オーバーラップ)
    cf_samples = int(sr * 2.5)
    combined = audio_segments[0].copy()

    for nxt in audio_segments[1:]:
        overlap_a = combined[-cf_samples:]
        overlap_b = nxt[:cf_samples]
        
        # フェードカーブ
        fade_out = np.linspace(1.0, 0.0, cf_samples)[:, None]
        fade_in = np.linspace(0.0, 1.0, cf_samples)[:, None]
        
        blended = (overlap_a * fade_out) + (overlap_b * fade_in)
        combined = np.vstack([combined[:-cf_samples], blended, nxt[cf_samples:]])

    # 3. ジャスト300秒にトリミング & 末尾3秒自然フェードアウト
    target_samples = int(TARGET_SEC * sr)
    if len(combined) > target_samples:
        combined = combined[:target_samples]
    elif len(combined) < target_samples:
        pad = np.zeros((target_samples - len(combined), 2), dtype=np.float32)
        combined = np.vstack([combined, pad])

    # ラスト3秒のフェードアウト
    fade_end_samples = int(sr * 3.0)
    fo_curve = np.linspace(1.0, 0.0, fade_end_samples)[:, None]
    combined[-fade_end_samples:] = combined[-fade_end_samples:] * fo_curve

    out_data = np.clip(combined, -32768, 32767).astype(np.int16)

    with wave.open(str(OUT_WAV), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(out_data.tobytes())

    print(f"✅ Combined 5-Minute Audio Mastered: {OUT_WAV} ({len(out_data)/sr:.2f}s)")

def load_font(size, index=4):
    try:
        return ImageFont.truetype(FUTURA_PATH, size, index=index)
    except Exception:
        try:
            return ImageFont.truetype(FUTURA_PATH, size, index=0)
        except Exception:
            return ImageFont.load_default()

def render_5min_video():
    """特大文字（72px）＋ プログレスバー 5分間動画レンダリング"""
    print("\n=== [2/2] RENDERING 5-MINUTE VIDEO (LARGE TEXT) ===")
    total_sec = TARGET_SEC
    total_frames = int(total_sec * FPS)

    # 1. Prepare Base Background Image (1920x1080)
    bg_orig = Image.open(BG_IMAGE).convert("RGBA")
    img_w, img_h = bg_orig.size
    target_ratio = WIDTH / HEIGHT
    cur_ratio = img_w / img_h

    if cur_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        bg_orig = bg_orig.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        bg_orig = bg_orig.crop((0, top, img_w, top + new_h))

    base_bg = bg_orig.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    # 2. Fonts (4倍特大サイズ: 72px)
    font_large = load_font(72, index=4)  # Futura Bold

    # 3. FFmpeg Process
    print(f"[+] Starting FFmpeg encoder -> {OUT_VIDEO}")
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(OUT_WAV),
        "-c:v", "h264_videotoolbox",
        "-b:v", "4000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        str(OUT_VIDEO)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # UI Geometry parameters (特大文字・中央集約・プログレスバー)
    BAR_W = 800
    BAR_H = 8
    BAR_X = (WIDTH - BAR_W) // 2
    BAR_Y = 142

    for f_idx in range(total_frames):
        cur_sec = f_idx / FPS
        rem_sec = max(0.0, total_sec - cur_sec)

        # Build UI overlay
        ui = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ui)

        # Background subtle top gradient
        draw.rectangle([0, 0, WIDTH, 175], fill=(0, 0, 0, 100))

        # Digital Countdown Timer
        m = int(rem_sec) // 60
        s = int(rem_sec) % 60
        timer_str = f"{m:02d}:{s:02d}"

        # 中央特大テキスト: "STUDY SESSION   05:00"
        center_text = f"STUDY SESSION   {timer_str}"
        bbox = font_large.getbbox(center_text)
        text_w = bbox[2] - bbox[0]
        text_x = (WIDTH - text_w) // 2
        draw.text((text_x, 42), center_text, font=font_large, fill=(255, 255, 255, 255))

        # Progress calculation
        progress = cur_sec / total_sec
        fill_w = int(BAR_W * progress)

        # Progress Bar Track & Fill (中央)
        draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + BAR_W, BAR_Y + BAR_H], radius=4, fill=(255, 255, 255, 45))
        if fill_w > 0:
            draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + fill_w, BAR_Y + BAR_H], radius=4, fill=(255, 255, 255, 240))

        # Composite base_bg + ui
        frame = Image.alpha_composite(base_bg, ui)
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()
    print(f"✅ 5-Minute Video Rendered: {OUT_VIDEO} ({total_sec:.2f}s)")

def main():
    print("==================================================")
    print("🚀 CH1 5-MINUTE POMODORO TEST (LARGE TEXT 72PX)")
    print("==================================================")
    master_and_combine_5min_audio()
    render_5min_video()
    print("\n🎉 5-MINUTE VIDEO COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
