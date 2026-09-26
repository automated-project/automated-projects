#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 単体音源マスタリングスクリプト (本物のSuper Crisp仕様)
- 仕様: Super Crisp Extreme Sub-Bass Mastering (過去ログ確定仕様)
  - 55Hz Extreme Sub-Bass Boost (+8.5dB, Q=1.2: 地響き808サブベース)
  - 110Hz Kick Punch (+5.5dB, Q=1.0: 胸に響くキックアタック)
  - 250Hz Mud Cut (-2.5dB, Q=1.0: 低音のモワつき濁り排除)
  - 5000Hz Presence (+4.0dB, Q=1.0: スネア・カウベルの抜け)
  - 10000Hz High Air (+9.0dB, Q=1.0: クリスプな高域煌めき)
  - 15000Hz Ultra Air (+8.5dB, Q=1.0: 突き抜けるオープン感)
  - alimiter=limit=0.95 (歪みゼロ・最大音圧 / loudnorm完全排除)
- 入力: raw_audio/ 内の未マスタリング音源 (WAV/MP3/MP4)
- 出力: mastered_audio/wav/ & mastered_audio/mp3/
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
RAW_DIR = BASE_DIR / "raw_audio"
OUT_WAV_DIR = BASE_DIR / "mastered_audio/wav"
OUT_MP3_DIR = BASE_DIR / "mastered_audio/mp3"

OUT_WAV_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP3_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".mp4", ".flac", ".ogg"}

# 波形異常が確認されている禁止トラック（恒久除外）
BANNED_STEMS = {"iron_ascension", "iron ascension"}

def master_ch2_track(src_path: Path):
    stem = src_path.stem
    if stem.lower() in BANNED_STEMS:
        print(f"⛔ Banned track ignored: {stem}")
        return None
        
    out_wav = OUT_WAV_DIR / f"{stem}.wav"
    out_mp3 = OUT_MP3_DIR / f"{stem}.mp3"
    
    print(f"🎛️ Mastering Ch2 Phonk Track (Super Crisp Extreme Bass): {src_path.name}...")
    
    # Ch 2 専用本物フィルター: 55Hz +8.5dB, 110Hz +5.5dB, 250Hz -2.5dB, 5kHz +4dB, 10kHz +9dB, 15kHz +8.5dB, alimiter=0.95 (loudnormなし)
    af_filter = (
        "equalizer=f=55:t=q:w=1.2:g=8.5,"
        "equalizer=f=110:t=q:w=1.0:g=5.5,"
        "equalizer=f=250:t=q:w=1.0:g=-2.5,"
        "equalizer=f=5000:t=q:w=1.0:g=4.0,"
        "equalizer=f=10000:t=q:w=1.0:g=9.0,"
        "equalizer=f=15000:t=q:w=1.0:g=8.5,"
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
    print("=== [Ch 2: PhonkForge Audio] Super Crisp Track Mastering Pipeline ===")
    raw_files = [p for p in RAW_DIR.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS and not p.name.startswith(".")]
    if not raw_files:
        print(f"ℹ️ No raw audio files found in {RAW_DIR}")
        return
        
    for p in raw_files:
        try:
            master_ch2_track(p)
        except Exception as e:
            print(f"❌ Failed to master {p.name}: {e}")
            
    print("\n🎉 All Ch2 Tracks Successfully Mastered (Super Crisp) into mastered_audio/wav & mp3!")

if __name__ == "__main__":
    master_all()
