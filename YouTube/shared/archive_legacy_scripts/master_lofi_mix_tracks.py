#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio): Lofi-Mix 全曲一括ウォームマスタリングスクリプト
- 対象: 01_Chill_Channel/Lofi-Mix/*.mp4
- 出力先: 01_Chill_Channel/mastered_audio/wav/lofi_mix/
- マスタリング仕様:
  * 35Hz ハイパス（不要超低域カット）
  * 180Hz +1.8dB（ピアノ・ベースの温もり）
  * 3.2kHz -1.5dB（耳障りなピーク緩和）
  * 8.5kHz -1.8dB & 15kHz ローパス（アナログテープ質感）
  * Loudness Normalization: -14.0 LUFS / True Peak -1.5dB
  * 1曲目（Coffee_by_the_Window）: 冒頭9.8秒の雷鳴ノイズを自動カット
  * 各曲末尾/冒頭のスムーズフェード
"""

import os
import subprocess
from pathlib import Path

SOURCE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel/Lofi-Mix")
OUTPUT_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel/mastered_audio/wav/lofi_mix")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def main():
    audio_files = sorted(list(SOURCE_DIR.glob("*.mp4")) + list(SOURCE_DIR.glob("*.mp3")) + list(SOURCE_DIR.glob("*.wav")))
    print(f"🎵 発見した音源: {len(audio_files)} 曲")
    print(f"📁 出力先ディレクトリ: {OUTPUT_DIR}\n")

    # Lofi Warm Mastering Filter Chain
    af_chain_base = (
        "highpass=f=35,"
        "equalizer=f=180:t=q:w=1.2:g=1.8,"
        "equalizer=f=3200:t=q:w=1.5:g=-1.5,"
        "equalizer=f=8500:t=q:w=1.0:g=-1.8,"
        "lowpass=f=15000,"
        "loudnorm=I=-14.0:TP=-1.5:LRA=11"
    )

    results = []

    for idx, src_file in enumerate(audio_files, start=1):
        filename = src_file.stem
        out_wav = OUTPUT_DIR / f"{idx:02d}_{filename}.wav"
        raw_dur = get_duration(src_file)

        # 1曲目（Coffee_by_the_Window）は雷鳴ノイズ(9.8秒)をカット
        is_first_track_noise = "Coffee_by_the_Window" in filename
        start_offset = 9.8 if is_first_track_noise else 0.0
        dur = raw_dur - start_offset

        print(f"[{idx:02d}/{len(audio_files)}] マスタリング中: {filename}")
        if is_first_track_noise:
            print(f"      ⚡ 冒頭 {start_offset}s の雷鳴ノイズを自動スキップ")

        # 音声フェード処理を追加した完全フィルター
        af_full = f"{af_chain_base},afade=t=in:ss=0:d=1.2,afade=t=out:st={dur-1.5:.2f}:d=1.5"

        cmd = ["ffmpeg", "-y"]
        if start_offset > 0:
            cmd.extend(["-ss", f"{start_offset:.2f}"])
        cmd.extend([
            "-i", str(src_file),
            "-vn",
            "-af", af_full,
            "-ar", "48000",
            "-ac", "2",
            "-c:a", "pcm_s16le",
            str(out_wav)
        ])

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ エラー発生: {filename}")
            print(res.stderr)
        else:
            final_dur = get_duration(out_wav)
            mins = int(final_dur // 60)
            secs = int(final_dur % 60)
            results.append((idx, filename, f"{mins:02d}:{secs:02d}", out_wav))
            print(f"      ✅ 完了: {out_wav.name} ({mins:02d}:{secs:02d})")

    print("\n" + "="*60)
    print(f"🎉 全 {len(results)} 曲のマスタリングが正常に完了しました！")
    print("="*60)
    for idx, title, dur_str, path in results:
        print(f"  {idx:02d}. {title.replace('_', ' ')} [{dur_str}]")
    print("="*60)

if __name__ == "__main__":
    main()
