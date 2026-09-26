#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2: Velvet Sunset Audio (@Velvet-Sunset-Audio)
専用マスタリングスクリプト: Smooth Groove R&B Mastering

処理仕様:
- 【完全排除】loudnorm フィルタ（過圧縮・音量バラつき防止）
- 【EQ設計】
  - 60Hz +3.0dB (タイトなキックのアタックと量感)
  - 200Hz +1.5dB (ベースラインとエレピの温かい中低域)
  - 2.5kHz +2.0dB (ボーカルとスネアのクリアな抜け)
  - 10kHz +3.5dB (洗練されたAir感とハイハットの煌めき)
- 【ピーク制限】alimiter=limit=0.95:level=disabled (歪み完全防止)
- 出力先: mastered_audio/wav/ および mastered_audio/mp3/
"""

import os
import subprocess
import glob
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw_audio"
MASTERED_WAV_DIR = BASE_DIR / "mastered_audio" / "wav"
MASTERED_MP3_DIR = BASE_DIR / "mastered_audio" / "mp3"

def setup_dirs():
    MASTERED_WAV_DIR.mkdir(parents=True, exist_ok=True)
    MASTERED_MP3_DIR.mkdir(parents=True, exist_ok=True)

def master_track(input_path: Path):
    track_name = input_path.stem
    output_wav = MASTERED_WAV_DIR / f"{track_name}.wav"
    output_mp3 = MASTERED_MP3_DIR / f"{track_name}.mp3"

    print(f"🎵 [Ch2: Velvet Sunset] マスタリング開始: {input_path.name}")

    # EQ フィルター構成 (Smooth Groove R&B)
    eq_filters = [
        "equalizer=f=60:width_type=h:width=40:g=3.0",    # タイトなキック
        "equalizer=f=200:width_type=h:width=100:g=1.5",  # ベース＆エレピの厚み
        "equalizer=f=2500:width_type=h:width=1200:g=2.0",# ボーカル＆スネアの抜け
        "equalizer=f=10000:width_type=h:width=4000:g=3.5",# Air感・ハイハット
        "alimiter=limit=0.95:level=disabled"             # ピークリミッター
    ]
    filter_chain = ",".join(eq_filters)

    # 1. 高品位 WAV 出力 (24bit / 48kHz)
    cmd_wav = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-af", filter_chain,
        "-c:a", "pcm_s24le", "-ar", "48000",
        str(output_wav)
    ]
    subprocess.run(cmd_wav, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. 配信用 320kbps MP3 出力
    cmd_mp3 = [
        "ffmpeg", "-y", "-i", str(output_wav),
        "-c:a", "libmp3lame", "-b:a", "320k",
        str(output_mp3)
    ]
    subprocess.run(cmd_mp3, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"  ✅ 完了: {output_wav.name} & {output_mp3.name}")

def main():
    setup_dirs()
    raw_files = sorted(list(RAW_DIR.glob("*.wav")) + list(RAW_DIR.glob("*.mp3")) + list(RAW_DIR.glob("*.m4a")))
    
    if not raw_files:
        print(f"⚠️ {RAW_DIR} にマスタリング対象の音源ファイルがありません。")
        return

    print(f"=== Ch2 (Velvet Sunset Audio) マスタリング実行 (対象: {len(raw_files)}曲) ===")
    for raw_file in raw_files:
        master_track(raw_file)
    print("=== 全曲マスタリング完了 ===")

if __name__ == "__main__":
    main()
