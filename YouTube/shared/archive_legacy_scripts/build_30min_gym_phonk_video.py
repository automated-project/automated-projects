# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) 30-Minute Hardcore Gym Phonk Video Pipeline
- 音源: 現在公開中ロング動画採用曲から "マスタリング済みWAV" (02_Phonk_Channel/mastered_audio/wav/) を使用
- 接続: 無音テール自動トリミング ＋ 2.5秒 等エネルギーDJクロスフェード (Equal-Power Crossfade / 無音ギャップ完全ゼロ)
- 背景: アンダーグラウンド・ジム (bg_underground_gym.jpeg)
- 演出: マイルドBass Pulse (Scale 1.000〜1.018) ＋ 48本波形 ＋ 特大72px Futura名言 (15フレーズ / 2分ごと切替)
- 規格: 30分ジャスト (1800.0秒)
"""
import os
import sys
import wave
import shutil
import subprocess
import json
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
WAV_DIR = BASE_DIR / "mastered_audio" / "wav"
COVER_ART = BASE_DIR / "cover_art" / "bg_underground_gym.jpeg"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

TARGET_DURATION_SEC = 1800.0  # 30分00秒ジャスト
FPS = 15
WIDTH, HEIGHT = 1920, 1080
CROSSFADE_SEC = 2.5
SR = 44100

# 現在公開中ロング動画の採用曲の中から、曲順をガラリと変えて厳選したマスタリング済み11曲
ORDERED_MASTERED_TRACKS = [
    ("Crush_The_Bone.wav", "Crush The Bone"),
    ("The_Iron_Ascent.wav", "The Iron Ascent"),
    ("Redline_Pressure.wav", "Redline Pressure"),
    ("Midnight_Asphalt_Burn.wav", "Midnight Asphalt Burn"),
    ("Kingdom_Of_My_Own.wav", "Kingdom Of My Own"),
    ("Blacktop_Fury.wav", "Blacktop Fury"),
    ("Asphalt_Redline.wav", "Asphalt Redline"),
    ("Concrete_Pursuit.wav", "Concrete Pursuit"),
    ("Savage_Grip.wav", "Savage Grip"),
    ("Storming_the_Gate.wav", "Storming The Gate"),
    ("Redline_Torque.wav", "Redline Torque")
]

# 英語モチベーション名言 (全15フレーズ / 120秒ごと切替)
QUOTES = [
    {
        "sub": "HARDCORE GYM MOTIVATION",
        "main": "DISCIPLINE IS CHOOSING\nBETWEEN WHAT YOU WANT NOW\nAND WHAT YOU WANT MOST."
    },
    {
        "sub": "MINDSET OVER MUSCLE",
        "main": "PAIN IS TEMPORARY.\nPRIDE IS FOREVER."
    },
    {
        "sub": "RELENTLESS FOCUS",
        "main": "CONQUER YOURSELF\nBEFORE YOU TRY TO\nCONQUER THE WORLD."
    },
    {
        "sub": "STANDARD OF EXCELLENCE",
        "main": "WE DO NOT RISE TO OUR HOPES,\nWE FALL TO THE LEVEL\nOF OUR TRAINING."
    },
    {
        "sub": "NEVER SURRENDER",
        "main": "WHEN YOU FEEL LIKE QUITTING,\nREMEMBER WHY YOU STARTED."
    },
    {
        "sub": "UNSTOPPABLE WILL",
        "main": "THE BODY ACHIEVES\nWHAT THE MIND BELIEVES."
    },
    {
        "sub": "SEEK DISCOMFORT",
        "main": "BE UNCOMFORTABLE WITH\nBEING COMFORTABLE."
    },
    {
        "sub": "TWO PATHS",
        "main": "SUFFER THE PAIN OF DISCIPLINE\nOR SUFFER THE PAIN OF REGRET."
    },
    {
        "sub": "ZERO DISTRACTIONS",
        "main": "SILENCE THE NOISE.\nFOCUS ON THE GRIND."
    },
    {
        "sub": "FINISH THE FIGHT",
        "main": "DON'T STOP WHEN YOU'RE TIRED.\nSTOP WHEN YOU'RE DONE."
    },
    {
        "sub": "BORN IN THE SHADOWS",
        "main": "GREATNESS IS BORN IN THE DARK,\nWHERE NO ONE IS WATCHING."
    },
    {
        "sub": "INNER BATTLE",
        "main": "YOUR ONLY COMPETITION\nIS IN THE MIRROR."
    },
    {
        "sub": "CONVERT THE RAGE",
        "main": "TURN YOUR ANGER\nINTO PURE FUEL."
    },
    {
        "sub": "SWEET VICTORY",
        "main": "THE HARDER THE BATTLE,\nTHE SWEETER THE VICTORY."
    },
    {
        "sub": "NO EXCUSES",
        "main": "THE ONLY BAD WORKOUT\nIS THE ONE THAT DIDN'T HAPPEN."
    }
]

def build_seamless_mastered_audio(temp_wav_path: Path):
    """無音トリミング ＋ 2.5秒 DJクロスフェードによる完全シームレス30分音源生成"""
    print("🔊 Step 1: Synthesizing Seamless Non-Stop DJ Mix with 2.5s Crossfades...")
    
    cf_samples = int(CROSSFADE_SEC * SR)
    full_audio = None
    timestamps = []
    current_sample_count = 0
    
    for i, (fn, title) in enumerate(ORDERED_MASTERED_TRACKS):
        p = WAV_DIR / fn
        if not p.exists():
            raise FileNotFoundError(f"❌ Mastered WAV track not found: {p}")
            
        with wave.open(str(p), "rb") as wf:
            n_ch = wf.getnchannels()
            n_fr = wf.getnframes()
            raw = wf.readframes(n_fr)
            
        data = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_ch).astype(np.float32) / 32768.0
        
        # 1. 末尾の無音（-46dB以下）をトリミング
        energy = np.abs(data).mean(axis=1)
        non_silent = np.where(energy > 0.005)[0]
        if len(non_silent) > 0:
            trim_end = min(len(data), non_silent[-1] + int(0.15 * SR)) # 0.15秒余韻
            data = data[:trim_end]
            
        # 2. シームレスDJクロスフェード合成
        if full_audio is None:
            full_audio = data
            timestamps.append((0.0, title))
            current_sample_count = len(data)
            print(f"  🎵 [00:00] {title} (First Track)")
        else:
            ts_sec = (current_sample_count - cf_samples) / SR
            timestamps.append((ts_sec, title))
            m = int(ts_sec) // 60
            s = int(ts_sec) % 60
            print(f"  🎵 [{m:02d}:{s:02d}] {title} (Crossfaded {CROSSFADE_SEC}s)")
            
            prev_tail = full_audio[-cf_samples:]
            curr_head = data[:cf_samples]
            
            # 等エネルギー（Equal-Power）クロスフェード
            fade_out = np.cos(np.linspace(0, np.pi/2, cf_samples))[:, np.newaxis]
            fade_in = np.sin(np.linspace(0, np.pi/2, cf_samples))[:, np.newaxis]
            blended = prev_tail * fade_out + curr_head * fade_in
            
            full_audio = np.vstack([
                full_audio[:-cf_samples],
                blended,
                data[cf_samples:]
            ])
            current_sample_count = len(full_audio)
            
    # 30分00秒ジャスト（1800.0秒）にトリミング ＋ 末尾3秒滑らかフェードアウト
    target_samples = int(TARGET_DURATION_SEC * SR)
    if len(full_audio) > target_samples:
        full_audio = full_audio[:target_samples]
    elif len(full_audio) < target_samples:
        pad_len = target_samples - len(full_audio)
        full_audio = np.pad(full_audio, ((0, pad_len), (0, 0)))
        
    end_fade_samples = int(3.0 * SR)
    end_fade = np.linspace(1.0, 0.0, end_fade_samples)[:, np.newaxis]
    full_audio[-end_fade_samples:] *= end_fade
    
    # 16-bit PCM WAVとして保存
    int16_audio = (np.clip(full_audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(str(temp_wav_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(int16_audio.tobytes())
        
    print(f"✅ Seamless 30-min audio created! ({len(full_audio)/SR:.2f}s)")
    return timestamps

def generate_video():
    temp_dir = OUTPUT_DIR / "temp_30min_seamless"
    temp_dir.mkdir(exist_ok=True, parents=True)
    
    mastered_wav = temp_dir / "seamless_30min_mix.wav"
    output_mp4 = OUTPUT_DIR / "30MIN_HARDCORE_GYM_PHONK_MOTIVATION.mp4"
    chapters_txt = OUTPUT_DIR / "30MIN_HARDCORE_GYM_PHONK_MOTIVATION_chapters.txt"
    
    timestamps = build_seamless_mastered_audio(mastered_wav)
    
    # チャプターファイル作成
    print("📝 Step 2: Generating Chapters and Timestamps...")
    with open(chapters_txt, "w", encoding="utf-8") as f:
        f.write("⏱️ TRACKLIST & TIMESTAMPS:\n")
        for ts_sec, title in timestamps:
            m = int(ts_sec) // 60
            s = int(ts_sec) % 60
            f.write(f"{m:02d}:{s:02d} - {title}\n")
    print(f"✅ Chapters saved to: {chapters_txt}")
    
    # オーディオ動的解析 (FFT)
    print("🎵 Step 3: Analyzing sub-bass audio dynamics with FFT...")
    with wave.open(str(mastered_wav), "rb") as wf:
        n_ch = wf.getnchannels()
        n_fr = wf.getnframes()
        raw = wf.readframes(n_fr)
    audio_data = np.frombuffer(raw, dtype=np.int16).reshape(-1, n_ch)
    audio_mono = audio_data.mean(axis=1) / 32768.0
    
    total_frames = int(TARGET_DURATION_SEC * FPS)
    samples_per_frame = int(SR / FPS)
    
    num_bars = 48
    fft_size = 2048
    freq_bins = np.logspace(np.log10(3), np.log10(fft_size // 4), num_bars).astype(int)
    
    subbass_levels = np.zeros(total_frames)
    for f in range(total_frames):
        start_idx = f * samples_per_frame
        end_idx = min(start_idx + fft_size, len(audio_mono))
        chunk = audio_mono[start_idx:end_idx]
        if len(chunk) < fft_size:
            chunk = np.pad(chunk, (0, fft_size - len(chunk)))
        windowed = chunk * np.hanning(fft_size)
        spec = np.abs(np.fft.rfft(windowed))
        subbass_levels[f] = np.mean(spec[3:9])
        
    p95 = np.percentile(subbass_levels, 95)
    if p95 > 0:
        subbass_norm = np.clip(subbass_levels / p95, 0.0, 1.5)
    else:
        subbass_norm = np.zeros(total_frames)
        
    # ベース画像準備
    raw_bg = Image.open(COVER_ART).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    for y_idx in range(HEIGHT):
        if y_idx < 460:
            alpha = int(160 * (1.0 - y_idx / 460))
            d_over.line([(0, y_idx), (WIDTH, y_idx)], fill=(0, 0, 0, alpha))
        elif y_idx > 740:
            alpha = int(180 * ((y_idx - 740) / 340))
            d_over.line([(0, y_idx), (WIDTH, y_idx)], fill=(0, 0, 0, alpha))
    base_bg = Image.alpha_composite(raw_bg, overlay)
    
    font_path = "/System/Library/Fonts/Supplemental/Futura.ttc"
    font_quote = ImageFont.truetype(font_path, 72, index=2)  # Futura Bold 72px
    font_sub = ImageFont.truetype(font_path, 34, index=1)    # Futura Medium Italic 34px

    print(f"🚀 Step 4: Rendering 30-min Video with Seamless Crossfades to {output_mp4.name}...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "-",
        "-i", str(mastered_wav),
        "-c:v", "h264_videotoolbox", "-b:v", "3500k", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    bar_w = 14
    gap = 10
    total_w = num_bars * bar_w + (num_bars - 1) * gap
    start_x = (WIDTH - total_w) // 2
    base_y = 970
    
    smooth_heights = np.zeros(num_bars)
    quote_interval_frames = 120 * FPS
    fade_frames = 15
    
    for f_idx in range(total_frames):
        quote_idx = min(f_idx // quote_interval_frames, len(QUOTES) - 1)
        curr_quote = QUOTES[quote_idx]
        frame_in_quote = f_idx % quote_interval_frames
        
        if frame_in_quote < fade_frames:
            txt_alpha = frame_in_quote / fade_frames
        elif frame_in_quote > (quote_interval_frames - fade_frames):
            txt_alpha = (quote_interval_frames - frame_in_quote) / fade_frames
        else:
            txt_alpha = 1.0
            
        sb = subbass_norm[f_idx]
        pulse_scale = 1.000 + 0.018 * (sb ** 1.3)
        
        crop_w = int(WIDTH / pulse_scale)
        crop_h = int(HEIGHT / pulse_scale)
        x1 = (WIDTH - crop_w) // 2
        y1 = (HEIGHT - crop_h) // 2
        
        frame_im = base_bg.crop((x1, y1, x1 + crop_w, y1 + crop_h)).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
        draw = ImageDraw.Draw(frame_im)
        
        # 筋トレ名言テキスト描画 (2分ごと切替)
        if txt_alpha > 0.01:
            sub_text = curr_quote["sub"]
            bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
            w_sub = bbox_sub[2] - bbox_sub[0]
            x_sub = (WIDTH - w_sub) // 2
            y_sub = 150
            
            sub_glow_a = int(220 * txt_alpha)
            sub_txt_a = int(255 * txt_alpha)
            
            for offset in [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]:
                draw.text((x_sub + offset[0], y_sub + offset[1]), sub_text, font=font_sub, fill=(255, 30, 60, sub_glow_a))
            draw.text((x_sub, y_sub), sub_text, font=font_sub, fill=(255, 255, 255, sub_txt_a))
            
            lines = curr_quote["main"].split("\n")
            curr_y = 240
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font_quote)
                w = bbox[2] - bbox[0]
                x = (WIDTH - w) // 2
                
                sh_a = int(220 * txt_alpha)
                for offset in range(1, 6):
                    draw.text((x - offset, curr_y), line, font=font_quote, fill=(0, 0, 0, sh_a))
                    draw.text((x + offset, curr_y), line, font=font_quote, fill=(0, 0, 0, sh_a))
                    draw.text((x, curr_y - offset), line, font=font_quote, fill=(0, 0, 0, sh_a))
                    draw.text((x, curr_y + offset), line, font=font_quote, fill=(0, 0, 0, sh_a))
                draw.text((x, curr_y), line, font=font_quote, fill=(255, 255, 255, sub_txt_a))
                curr_y += 95

        # 48本波形描画
        start_idx = f_idx * samples_per_frame
        end_idx = min(start_idx + fft_size, len(audio_mono))
        chunk = audio_mono[start_idx:end_idx]
        if len(chunk) < fft_size:
            chunk = np.pad(chunk, (0, fft_size - len(chunk)))
        windowed = chunk * np.hanning(fft_size)
        spec = np.abs(np.fft.rfft(windowed))
        
        for b in range(num_bars):
            bin_idx = min(freq_bins[b], len(spec)-1)
            raw_val = spec[bin_idx]
            target_h = min(raw_val * 4.5 + 4.0, 110.0)
            
            if target_h > smooth_heights[b]:
                smooth_heights[b] = target_h * 0.75 + smooth_heights[b] * 0.25
            else:
                smooth_heights[b] = smooth_heights[b] * 0.82
                
            bh = smooth_heights[b]
            bx = start_x + b * (bar_w + gap)
            by = base_y - bh
            
            draw.rounded_rectangle([bx-2, by-2, bx+bar_w+2, base_y+2], radius=4, fill=(255, 255, 255, 60))
            draw.rounded_rectangle([bx, by, bx+bar_w, base_y], radius=3, fill=(255, 255, 255, 240))
            
        raw_bytes = frame_im.convert("RGB").tobytes()
        proc.stdin.write(raw_bytes)
        
        if f_idx % (FPS * 60) == 0:
            print(f"  Rendered {f_idx // (FPS * 60)} / {int(TARGET_DURATION_SEC / 60)} minutes...")
            
    proc.stdin.close()
    proc.wait()
    
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("\n🎉 Seamless 30-Minute Gym Phonk Video Rendered Successfully!")
    print(f"  Output: {output_mp4} ({output_mp4.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    generate_video()
