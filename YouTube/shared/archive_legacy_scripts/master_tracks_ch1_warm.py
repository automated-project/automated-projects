#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio): 単体音源マスタリングスクリプト (本物のWarm Tape仕様)
- 仕様: Warm Tape Acoustic (過去ログ確定仕様)
  - 35Hz High-Pass Filter（不要な超低域ノイズカット）
  - 180Hz Warmth (+1.8dB, Q=1.2: ピアノ/ウッドベースの温もり)
  - 8500Hz High Roll-off (-1.8dB, Q=1.0: 耳障りな高域シャリつき抑制)
  - 15000Hz Low-Pass Filter (アナログテープの優しい質感)
  - alimiter=limit=0.95 (歪みゼロ・ダイレクト出力 / loudnorm完全排除)
- 入力: raw_audio/ 内の未マスタリング音源 (WAV/MP3/MP4)
- 出力: mastered_audio/wav/ & mastered_audio/mp3/
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
RAW_DIR = BASE_DIR / "raw_audio"
OUT_WAV_DIR = BASE_DIR / "mastered_audio/wav"
OUT_MP3_DIR = BASE_DIR / "mastered_audio/mp3"

OUT_WAV_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP3_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".mp4", ".flac", ".ogg"}

def master_ch1_track(src_path: Path):
    stem = src_path.stem
    out_wav = OUT_WAV_DIR / f"{stem}.wav"
    out_mp3 = OUT_MP3_DIR / f"{stem}.mp3"
    
    print(f"🎛️ Mastering Ch1 Lofi Track (Warm Tape): {src_path.name}...")
    
    # Ch 1 専用本物フィルター: 35Hz HPF + 180Hz +1.8dB + 8.5kHz -1.8dB + 15kHz LPF + alimiter=0.95 (loudnormなし)
    af_filter = (
        "highpass=f=35,"
        "equalizer=f=180:t=q:w=1.2:g=1.8,"
        "equalizer=f=8500:t=q:w=1.0:g=-1.8,"
        "lowpass=f=15000,"
        "alimiter=limit=0.95"
    )
    
    cmd_wav = [
        "ffmpeg", "-y", "-i", str(src_path),
        "-vn", "-af", af_filter,
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
        str(out_wav)
    ]
    subprocess.run(cmd_wav, capture_output=True, check=True)
    
    cmd_mp3 = [
        "ffmpeg", "-y", "-i", str(out_wav),
        "-vn", "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "320k",
        str(out_mp3)
    ]
    subprocess.run(cmd_mp3, capture_output=True, check=True)
    
    print(f"✅ Saved Mastered WAV: {out_wav.name}")
    print(f"✅ Saved Mastered MP3: {out_mp3.name}")
    return out_wav

def master_all():
    print("=== [Ch 1: Haven Chill Audio] Warm Tape Track Mastering Pipeline ===")
    raw_files = [p for p in RAW_DIR.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS and not p.name.startswith(".")]
    if not raw_files:
        print(f"ℹ️ No raw audio files found in {RAW_DIR}")
        return
        
    for p in raw_files:
        try:
            master_ch1_track(p)
        except Exception as e:
            print(f"❌ Failed to master {p.name}: {e}")
            
    print("\n🎉 All Ch1 Tracks Successfully Mastered (Warm Tape) into mastered_audio/wav & mp3!")

if __name__ == "__main__":
    master_all()
