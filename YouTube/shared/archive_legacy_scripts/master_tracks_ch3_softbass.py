#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): 単体音源マスタリングスクリプト (本物のSoftBass仕様)
- 仕様: SoftBass & Crystal Air (過去ログ確定仕様 / Step 595「① SoftBass」)
  - 50Hz Sub-Bass Tight (+4.0dB, Q=1.2: 過度な圧迫感を抑えたタイトな低域)
  - 100Hz Kick Punch (+2.5dB, Q=1.0: 軽快なキックの抜け)
  - 250Hz Mud Cut (-2.0dB, Q=1.0: ボーカル帯域の被りをクリーン化)
  - 3500Hz Vocal Presence (+4.0dB, Q=1.0: 男性/女性ボーカルの艶と明瞭度)
  - 8000Hz Air (+7.5dB, Q=1.0: アコギのカッティングとシンセの煌めき)
  - 12000Hz Sparkle (+9.0dB, Q=1.0: クリスタルな高域の抜け)
  - 16000Hz Ultra Air (+9.5dB, Q=1.0: 突き抜けるオープンな多幸感)
  - alimiter=limit=0.95 (歪みゼロ・最大音圧 / loudnorm完全排除)
- 入力: raw_audio/ 内の未マスタリング音源 (WAV/MP3/MP4)
- 出力: mastered_audio/wav/ & mastered_audio/mp3/
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
RAW_DIR = BASE_DIR / "raw_audio"
OUT_WAV_DIR = BASE_DIR / "mastered_audio/wav"
OUT_MP3_DIR = BASE_DIR / "mastered_audio/mp3"

OUT_WAV_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP3_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".mp4", ".flac", ".ogg"}

def master_ch3_track(src_path: Path):
    stem = src_path.stem
    out_wav = OUT_WAV_DIR / f"{stem}.wav"
    out_mp3 = OUT_MP3_DIR / f"{stem}.mp3"
    
    print(f"🎛️ Mastering Ch3 Melodic Track (SoftBass & Crystal Air): {src_path.name}...")
    
    # Ch 3 専用本物フィルター: 50Hz +4dB, 100Hz +2.5dB, 250Hz -2dB, 3.5kHz +4dB, 8kHz +7.5dB, 12kHz +9dB, 16kHz +9.5dB, alimiter=0.95 (loudnormなし)
    af_filter = (
        "equalizer=f=50:t=q:w=1.2:g=4.0,"
        "equalizer=f=100:t=q:w=1.0:g=2.5,"
        "equalizer=f=250:t=q:w=1.0:g=-2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=4.0,"
        "equalizer=f=8000:t=q:w=1.0:g=7.5,"
        "equalizer=f=12000:t=q:w=1.0:g=9.0,"
        "equalizer=f=16000:t=q:w=1.0:g=9.5,"
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
    print("=== [Ch 3: AuraMelody Audio] SoftBass Track Mastering Pipeline ===")
    raw_files = [p for p in RAW_DIR.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS and not p.name.startswith(".")]
    if not raw_files:
        print(f"ℹ️ No raw audio files found in {RAW_DIR}")
        return
        
    for p in raw_files:
        try:
            master_ch3_track(p)
        except Exception as e:
            print(f"❌ Failed to master {p.name}: {e}")
            
    print("\n🎉 All Ch3 Tracks Successfully Mastered (SoftBass) into mastered_audio/wav & mp3!")

if __name__ == "__main__":
    master_all()
