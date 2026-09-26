#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 8分〜10分 ハイエナジー Gym Phonk Mini Mix (Vol. 1)
- 音源: mastered_audio/wav/ のマスタリング済み音源のみを使用（二重マスタリング・EQ完全禁止）
- 合成: 末尾無音トリミング ＋ 2.5秒 DJ等エネルギー(cos/sin)クロスフェードのみ（原音の音質・ダイナミクスを100%完全維持）
- 演出: 48本高感度ダイナミック丸角波形（FFT正規化＋ピーク減衰スムージング） ＋ マイルド重低音パルス (1.000〜1.018) ＋ Futura Bold 英語名言
- 背景: cover_art/bg_underground_gym.jpeg
- 出力: output_videos/8MIN_HARDCORE_GYM_PHONK_VOL1.mp4
"""

import os
import sys
import wave
import shutil
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
WAV_DIR = BASE_DIR / "mastered_audio/wav"
COVER_ART = BASE_DIR / "cover_art/bg_underground_gym.jpeg"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_8min_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUTPUT_DIR / "8MIN_HARDCORE_GYM_PHONK_VOL1.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "8MIN_HARDCORE_GYM_PHONK_VOL1_chapters.txt"
COMBINED_WAV = TEMP_DIR / "master_audio_8min.wav"

WIDTH, HEIGHT = 1920, 1080
FPS = 15
SAMPLE_RATE = 44100
CROSSFADE_SEC = 2.5
CROSSFADE_SAMPLES = int(CROSSFADE_SEC * SAMPLE_RATE)

# 厳選キラーチューン3曲（Iron Ascensionは完全除外）
TRACK_LIST = [
    ("Bonecrusher_Phonk.wav", "Bonecrusher Phonk"),
    ("Asphalt_Fang_Strike.wav", "Asphalt Fang Strike"),
    ("Grim_Asphalt_Reaper.wav", "Grim Asphalt Reaper")
]

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
    }
]

def load_wav_as_float(wav_path):
    with wave.open(str(wav_path), 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
    
    if sampwidth == 2:
        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    elif sampwidth == 3:
        raw = np.frombuffer(data, dtype=np.uint8)
        audio = (raw[0::3].astype(np.int32) | (raw[1::3].astype(np.int32) << 8) | (raw[2::3].astype(np.int32) << 16))
        audio = np.where(audio >= 0x800000, audio - 0x1000000, audio).astype(np.float32) / 8388608.0
    else:
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    
    audio = audio.reshape(-1, n_channels)
    return audio

def save_float_as_wav(audio_data, out_path):
    audio_int16 = np.clip(audio_data * 32767.0, -32768.0, 32767.0).astype(np.int16)
    with wave.open(str(out_path), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())

def build_seamless_audio():
    print("=== Step 1: 2.5s DJ Crossfading 3 Mastered Tracks (No Re-Mastering) ===")
    combined_audio = None
    chapters = []
    current_time_sec = 0.0
    
    t = np.linspace(0, np.pi / 2, CROSSFADE_SAMPLES, endpoint=True, dtype=np.float32)
    fade_out = np.cos(t)[:, np.newaxis]
    fade_in = np.sin(t)[:, np.newaxis]
    
    for idx, (filename, title) in enumerate(TRACK_LIST):
        wav_path = WAV_DIR / filename
        if not wav_path.exists():
            raise FileNotFoundError(f"❌ Mastered track not found: {wav_path}")
            
        track_audio = load_wav_as_float(wav_path)
        
        # 末尾の無音（-46dB以下）をトリミング
        energy = np.abs(track_audio).mean(axis=1)
        non_silent = np.where(energy > 0.005)[0]
        if len(non_silent) > 0:
            trim_end = min(len(track_audio), non_silent[-1] + int(0.15 * SAMPLE_RATE))
            track_audio = track_audio[:trim_end]
            
        mins = int(current_time_sec // 60)
        secs = int(current_time_sec % 60)
        timestamp_str = f"{mins:02d}:{secs:02d}"
        chapters.append(f"{timestamp_str} - {title}")
        print(f"[{idx+1}/{len(TRACK_LIST)}] {timestamp_str} - {title}")
        
        if combined_audio is None:
            combined_audio = track_audio
            current_time_sec += len(track_audio) / SAMPLE_RATE
        else:
            overlap_tail = combined_audio[-CROSSFADE_SAMPLES:]
            overlap_head = track_audio[:CROSSFADE_SAMPLES]
            
            blended = overlap_tail * fade_out + overlap_head * fade_in
            combined_audio = np.vstack([
                combined_audio[:-CROSSFADE_SAMPLES],
                blended,
                track_audio[CROSSFADE_SAMPLES:]
            ])
            track_net_len = (len(track_audio) - CROSSFADE_SAMPLES) / SAMPLE_RATE
            current_time_sec += track_net_len
            
    print(f"\nTotal 8-Min Mix Duration: {current_time_sec/60:.2f} minutes ({current_time_sec:.1f} seconds)")
    
    # マスタリング済み音源の原音をそのまま出力（再イコライジング・再ラウドネス圧縮は一切行わない）
    save_float_as_wav(combined_audio, COMBINED_WAV)
    print(f"Combined Master Audio Saved to: {COMBINED_WAV}")
    
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as cf:
        cf.write("\n".join(chapters) + "\n")
    print(f"Saved Chapters to: {CHAPTERS_FILE}")

def render_8min_video():
    print("\n=== Step 2: Rendering Video with Dynamic Waveform & Bass Reactive Pulse ===")
    
    # 1. Base Image Setup
    base_bg = Image.open(COVER_ART).convert('RGB')
    base_bg = base_bg.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    font_path = "/System/Library/Fonts/Supplemental/Futura.ttc"
    font_main = ImageFont.truetype(font_path, 68, index=2) # Bold
    font_sub = ImageFont.truetype(font_path, 34, index=0)  # Medium
    
    # Load audio mono for analysis
    with wave.open(str(COMBINED_WAV), 'rb') as wf:
        n_frames = wf.getnframes()
        raw_data = wf.readframes(n_frames)
    audio_np = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
    audio_mono = audio_np.reshape(-1, 2).mean(axis=1)
    
    total_duration_sec = len(audio_mono) / SAMPLE_RATE
    total_frames = int(total_duration_sec * FPS)
    samples_per_frame = int(SAMPLE_RATE / FPS)
    
    print(f"Total Frames to render: {total_frames} ({total_duration_sec:.1f}s at {FPS}fps)")
    
    # 48本波形ビジュアライザー設定
    n_bars = 48
    bar_width = 16
    bar_gap = 10
    total_wave_width = n_bars * bar_width + (n_bars - 1) * bar_gap
    wave_start_x = (WIDTH - total_wave_width) // 2
    wave_base_y = HEIGHT - 90
    max_bar_height = 130
    min_bar_height = 6
    
    # FFT設定 (正確な正規化 ＋ 対数周波数バンド ＋ 周波数重み付け)
    fft_size = 2048
    hanning_win = np.hanning(fft_size)
    freq_bins = np.geomspace(40, 14000, n_bars + 1)
    fft_freqs = np.fft.rfftfreq(fft_size, 1.0 / SAMPLE_RATE)
    
    freq_weights = np.zeros(n_bars, dtype=np.float32)
    for b in range(n_bars):
        f_center = np.sqrt(freq_bins[b] * freq_bins[b+1])
        # 人間の聴覚特性＆ビジュアルバランスに応じた傾斜重み付け
        freq_weights[b] = ((f_center / 100.0) ** 0.48) * 14.0
        
    bass_idx = np.where((fft_freqs >= 35) & (fft_freqs <= 140))[0]
    
    # Pre-render Quote Overlays
    quote_overlays = []
    for q in QUOTES:
        glow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow_layer)
        
        sub_text = q['sub']
        main_text = q['main']
        
        # Subtext at y=180
        bbox_sub = gdraw.textbbox((0, 0), sub_text, font=font_sub)
        sub_w = bbox_sub[2] - bbox_sub[0]
        sub_x = (WIDTH - sub_w) // 2
        sub_y = 180
        gdraw.text((sub_x, sub_y), sub_text, font=font_sub, fill=(255, 10, 45, 255))
        
        # Main text at y=250
        lines = main_text.split('\n')
        line_height = 80
        start_y = 250
        for l_idx, line in enumerate(lines):
            bbox_line = gdraw.textbbox((0, 0), line, font=font_main)
            lw = bbox_line[2] - bbox_line[0]
            lx = (WIDTH - lw) // 2
            ly = start_y + l_idx * line_height
            gdraw.text((lx, ly), line, font=font_main, fill=(255, 10, 45, 180))
            
        glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(14))
        
        # Text Layer
        text_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(text_layer)
        
        # Shadow
        tdraw.text((sub_x + 3, sub_y + 3), sub_text, font=font_sub, fill=(0, 0, 0, 200))
        for l_idx, line in enumerate(lines):
            bbox_line = tdraw.textbbox((0, 0), line, font=font_main)
            lw = bbox_line[2] - bbox_line[0]
            lx = (WIDTH - lw) // 2
            ly = start_y + l_idx * line_height
            tdraw.text((lx + 4, ly + 4), line, font=font_main, fill=(0, 0, 0, 200))
            
        # Solid Text
        tdraw.text((sub_x, sub_y), sub_text, font=font_sub, fill=(255, 60, 80, 255))
        for l_idx, line in enumerate(lines):
            bbox_line = tdraw.textbbox((0, 0), line, font=font_main)
            lw = bbox_line[2] - bbox_line[0]
            lx = (WIDTH - lw) // 2
            ly = start_y + l_idx * line_height
            tdraw.text((lx, ly), line, font=font_main, fill=(255, 255, 255, 255))
            
        final_quote = Image.alpha_composite(glow_blurred, text_layer)
        quote_overlays.append(final_quote)
        
    print("Pre-rendered Quote overlays. Streaming frames to FFmpeg...")
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(COMBINED_WAV),
        "-c:v", "h264_videotoolbox",
        "-b:v", "3200k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        str(OUT_VIDEO)
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    prev_heights = np.zeros(n_bars, dtype=np.float32)
    prev_pulse = 0.0
    quote_dur_frames = total_frames // len(QUOTES)
    
    for f_idx in range(total_frames):
        if f_idx % (FPS * 30) == 0:
            print(f"  Progress: {f_idx}/{total_frames} frames ({f_idx/total_frames*100:.1f}%)")
            
        start_sample = f_idx * samples_per_frame
        chunk = audio_mono[start_sample : start_sample + fft_size]
        if len(chunk) < fft_size:
            chunk = np.pad(chunk, (0, fft_size - len(chunk)))
            
        windowed = chunk * hanning_win
        spectrum = np.abs(np.fft.rfft(windowed)) / (fft_size / 2)
        
        # 1. 重低音パルス（35Hz〜140Hz）
        bass_energy = np.mean(spectrum[bass_idx]) * 16.0
        target_pulse = np.clip((bass_energy - 0.10) * 1.5, 0.0, 1.0)
        if target_pulse > prev_pulse:
            pulse = target_pulse
        else:
            pulse = prev_pulse * 0.75
        prev_pulse = pulse
        
        pulse_scale = 1.00 + (pulse ** 1.2) * 0.018
        
        # 背景パルス
        if pulse_scale > 1.001:
            pw, ph = int(WIDTH * pulse_scale), int(HEIGHT * pulse_scale)
            frame_bg = base_bg.resize((pw, ph), Image.Resampling.BILINEAR)
            cx, cy = (pw - WIDTH) // 2, (ph - HEIGHT) // 2
            frame_img = frame_bg.crop((cx, cy, cx + WIDTH, cy + HEIGHT)).convert('RGBA')
        else:
            frame_img = base_bg.copy().convert('RGBA')
            
        # 2. 波形バーの周波数解析＆スムージング
        target_heights = np.zeros(n_bars, dtype=np.float32)
        for b in range(n_bars):
            idx_range = np.where((fft_freqs >= freq_bins[b]) & (fft_freqs < freq_bins[b+1]))[0]
            if len(idx_range) > 0:
                val = np.mean(spectrum[idx_range])
            else:
                closest_idx = np.argmin(np.abs(fft_freqs - (freq_bins[b] + freq_bins[b+1])/2))
                val = spectrum[closest_idx]
                
            adj = np.clip(val * freq_weights[b], 0.0, 1.0)
            target_heights[b] = min_bar_height + (adj ** 0.85) * (max_bar_height - min_bar_height)
            
        smooth_heights = np.zeros(n_bars, dtype=np.float32)
        for b in range(n_bars):
            if target_heights[b] >= prev_heights[b]:
                smooth_heights[b] = target_heights[b]
            else:
                smooth_heights[b] = max(min_bar_height, prev_heights[b] * 0.80)
        prev_heights = smooth_heights
        
        # 3. 波形バーの描画（半透明白＋丸角）
        wave_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        wdraw = ImageDraw.Draw(wave_layer)
        
        for b in range(n_bars):
            bh = int(smooth_heights[b])
            bx = wave_start_x + b * (bar_width + bar_gap)
            by = wave_base_y - bh
            wdraw.rounded_rectangle([bx, by, bx + bar_width, wave_base_y], radius=6, fill=(255, 255, 255, 235))
            
        frame_img = Image.alpha_composite(frame_img, wave_layer)
        
        # 4. 名言のフェードイン/アウト
        quote_idx = min(f_idx // quote_dur_frames, len(QUOTES) - 1)
        rel_frame = f_idx % quote_dur_frames
        fade_frames = FPS * 2
        
        if rel_frame < fade_frames:
            alpha = rel_frame / fade_frames
        elif rel_frame > (quote_dur_frames - fade_frames):
            alpha = (quote_dur_frames - rel_frame) / fade_frames
        else:
            alpha = 1.0
            
        if alpha > 0.01:
            q_overlay = quote_overlays[quote_idx].copy()
            r, g, b_ch, a_ch = q_overlay.split()
            a_ch = a_ch.point(lambda p: int(p * alpha))
            q_overlay.putalpha(a_ch)
            frame_img = Image.alpha_composite(frame_img, q_overlay)
            
        proc.stdin.write(frame_img.convert('RGB').tobytes())
        
    proc.stdin.close()
    proc.wait()
    print(f"\n✅ Video Render Finished: {OUT_VIDEO}")
    print(f"File Size: {os.path.getsize(OUT_VIDEO) / 1024 / 1024:.2f} MB")
    
    shutil.rmtree(TEMP_DIR)
    print("Cleaned up temp build directory.")

if __name__ == "__main__":
    build_seamless_audio()
    render_8min_video()
