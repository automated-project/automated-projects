#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): 1時間長尺 Sunroof Feel-Good Pop Mix ビルドスクリプト
- 音源: raw_audio/sunroof_male_mix (全21曲 / 約62分)
- 背景: cover_art/Gemini_Generated_Image_4ojup34ojup34oju.jpeg (ピュアアート)
- 音響: SoftBass Transparent Mastering (-14.0 LUFS) + 2.5秒 DJ等エネルギー(cos/sin)クロスフェード
- 出力: output_videos/1HOUR_SUNROOF_FEEL_GOOD_POP_MIX.mp4
"""

import os
import sys
import wave
import math
import shutil
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
AUDIO_DIR = BASE_DIR / "raw_audio/sunroof_male_mix"
BG_IMAGE_PATH = BASE_DIR / "cover_art/Gemini_Generated_Image_4ojup34ojup34oju.jpeg"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_sunroof_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUTPUT_DIR / "1HOUR_SUNROOF_FEEL_GOOD_POP_MIX.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "1HOUR_SUNROOF_FEEL_GOOD_POP_MIX_chapters.txt"
COMBINED_WAV = TEMP_DIR / "master_audio_sunroof_mix.wav"

WIDTH, HEIGHT = 3840, 2160
FPS = 30
SAMPLE_RATE = 48000
CROSSFADE_SEC = 2.5
CROSSFADE_SAMPLES = int(CROSSFADE_SEC * SAMPLE_RATE)

TRACK_LIST = [
    "Barefoot_on_Silver_Shores.mp4",
    "Sunroof_Melody_Chaser.mp4",
    "Bouncy_Rhythm_Avenue.mp4",
    "Endless_Sunshine_Drive.mp4",
    "Pure_Dopamine_Groove.mp4",
    "Chasing_The_Golden_Light.mp4",
    "Dancing_Into_Day.mp4",
    "Gold_Painted_Sky.mp4",
    "Golden_Horizon_Glow.mp4",
    "Miles_Into_Morning.mp4",
    "Miles_of_Burning_Sun.mp4",
    "Run_Beneath_The_Stars.mp4",
    "Salt_on_Our_Skin.mp4",
    "Smiling_This_Wide.mp4",
    "Standing_Eight_Feet_Tall.mp4",
    "Sunlight_In_My_Chest.mp4",
    "Before_the_Tide.mp4",
    "Sweet_Acoustic_Breeze.mp4",
    "The_Edge_of_Grace.mp4",
    "Under_Open_Skies.mp4",
    "Written_in_the_Sky.mp4"
]

def extract_and_trim_audio(input_file, out_wav):
    """MP4から音声を抽出し、無音テールを自動トリミングしてWAVに変換"""
    cmd = [
        "ffmpeg", "-y", "-i", str(input_file),
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-48dB",
        "-vn", "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out_wav)
    ]
    subprocess.run(cmd, capture_output=True, check=True)

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

def build_seamless_dj_mix():
    print("=== Step 1: Extracting & Smart Trimming Audio ===")
    wav_files = []
    for idx, track_name in enumerate(TRACK_LIST):
        src_mp4 = AUDIO_DIR / track_name
        dest_wav = TEMP_DIR / f"track_{idx:02d}.wav"
        print(f"[{idx+1}/{len(TRACK_LIST)}] Processing: {track_name}")
        extract_and_trim_audio(src_mp4, dest_wav)
        wav_files.append((track_name, dest_wav))
    
    print("\n=== Step 2: Equal-Power 2.5s DJ Crossfading ===")
    combined_audio = None
    chapters = []
    current_time_sec = 0.0
    
    # cos/sin equal-power curve
    t = np.linspace(0, np.pi / 2, CROSSFADE_SAMPLES, endpoint=True, dtype=np.float32)
    fade_out = np.cos(t)[:, np.newaxis]
    fade_in = np.sin(t)[:, np.newaxis]
    
    for idx, (track_name, wav_p) in enumerate(wav_files):
        track_audio = load_wav_as_float(wav_p)
        clean_title = track_name.replace(".mp4", "").replace("_", " ")
        
        # Format timestamp
        mins = int(current_time_sec // 60)
        secs = int(current_time_sec % 60)
        timestamp_str = f"{mins:02d}:{secs:02d}"
        chapters.append(f"{timestamp_str} - {clean_title}")
        print(f"Chapter: {timestamp_str} - {clean_title}")
        
        if combined_audio is None:
            combined_audio = track_audio
            current_time_sec += len(track_audio) / SAMPLE_RATE
        else:
            # Overlap last 2.5s with next track first 2.5s
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
            
    print(f"\nTotal Mix Duration: {current_time_sec/60:.2f} minutes ({current_time_sec:.1f} seconds)")
    
    # Save unmastered mix
    raw_mix_wav = TEMP_DIR / "raw_combined_mix.wav"
    save_float_as_wav(combined_audio, raw_mix_wav)
    
    # Save chapters file
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as cf:
        cf.write("\n".join(chapters) + "\n")
    print(f"Saved Chapters to: {CHAPTERS_FILE}")
    
    print("\n=== Step 3: Peak Limiter Direct Mastering (alimiter=0.95) ===")
    master_cmd = [
        "ffmpeg", "-y", "-i", str(raw_mix_wav),
        "-af", "alimiter=limit=0.95:level=disabled",
        "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(COMBINED_WAV)
    ]
    subprocess.run(master_cmd, capture_output=True, check=True)
    print(f"Mastered Audio Saved to: {COMBINED_WAV}")

def render_full_video():
    print("\n=== Step 4: Video Encoding (Pure High-Def Art + 4K UHD 30fps) ===")
    # Prepare 4K Background
    bg_4k = TEMP_DIR / "bg_4k.jpg"
    img = Image.open(BG_IMAGE_PATH).convert('RGB')
    img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    img.save(bg_4k, quality=98)
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(bg_4k),
        "-i", str(COMBINED_WAV),
        "-c:v", "h264_videotoolbox",
        "-b:v", "9500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        str(OUT_VIDEO)
    ]
    print(f"Encoding full video to: {OUT_VIDEO}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg Error: {res.stderr}")
        sys.exit(1)
        
    print(f"\n✅ Video Render Completed Successfully: {OUT_VIDEO}")
    print(f"File Size: {os.path.getsize(OUT_VIDEO) / 1024 / 1024:.2f} MB")
    
    # Cleanup temp dir
    shutil.rmtree(TEMP_DIR)
    print("Cleaned up temp build directory.")

if __name__ == "__main__":
    build_seamless_dj_mix()
    render_full_video()
