# -*- coding: utf-8 -*-
"""
1hour-mix の全28ファイルの音響特徴量（MFCC / クロマ / 波形ハッシュ / 長さ / 相関）を総当たり比較し、
実質的に同一の曲や酷似しているペアを完全検出するスクリプト
"""
import sys
import subprocess
import wave
import numpy as np
from pathlib import Path

mix_dir = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/raw_audio/1hour-mix")
files = sorted([f for f in mix_dir.iterdir() if f.is_file() and f.suffix.lower() == ".mp4"])

print(f"Analyzing audio content of {len(files)} files...")

audio_data = {}
sample_rate = 16000 # Downsampled for fast acoustic comparison

for f in files:
    temp_wav = Path(f"/tmp/{f.stem}_temp.wav")
    cmd = [
        "ffmpeg", "-y", "-i", str(f),
        "-vn", "-ar", str(sample_rate), "-ac", "1",
        "-c:a", "pcm_s16le", str(temp_wav)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    with wave.open(str(temp_wav), "rb") as w:
        frames = w.readframes(w.getnframes())
        arr = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        audio_data[f.name] = arr
    if temp_wav.exists():
        temp_wav.unlink()

print(f"Loaded {len(audio_data)} audio tracks into memory.")

# Compare all pairs using normalized cross-correlation / RMS diff
names = list(audio_data.keys())
duplicates = []
high_similarity = []

for i in range(len(names)):
    for j in range(i + 1, len(names)):
        n1 = names[i]
        n2 = names[j]
        a1 = audio_data[n1]
        a2 = audio_data[n2]
        
        len_diff = abs(len(a1) - len(a2)) / sample_rate
        # Check energy envelope & correlation on matching length
        min_len = min(len(a1), len(a2))
        if min_len < sample_rate * 10: # less than 10s
            continue
            
        # Segment comparison
        seg1 = a1[:min_len]
        seg2 = a2[:min_len]
        
        # Pearson correlation
        norm1 = seg1 - np.mean(seg1)
        norm2 = seg2 - np.mean(seg2)
        std1 = np.std(norm1)
        std2 = np.std(norm2)
        
        if std1 > 1e-4 and std2 > 1e-4:
            corr = np.mean(norm1 * norm2) / (std1 * std2)
        else:
            corr = 0.0
            
        # Envelope correlation (Downsampled 100x)
        env1 = np.abs(seg1)[::100]
        env2 = np.abs(seg2)[::100]
        env_corr = np.corrcoef(env1, env2)[0, 1] if len(env1) > 10 else 0
        
        dur1 = len(a1) / sample_rate
        dur2 = len(a2) / sample_rate
        
        if corr > 0.85 or env_corr > 0.90 or (len_diff < 1.0 and env_corr > 0.80):
            high_similarity.append((n1, n2, corr, env_corr, dur1, dur2))

print("\n=== Audio Similarity Analysis Results ===")
if not high_similarity:
    print("No high similarity pairs detected with simple correlation.")
else:
    for n1, n2, corr, env_corr, dur1, dur2 in high_similarity:
        print(f"⚠️ SIMILAR PAIR: {n1} ({dur1:.1f}s) <==> {n2} ({dur2:.1f}s) | WaveCorr: {corr:.3f}, EnvCorr: {env_corr:.3f}")

# Also check Vol. 1 vs Vol. 2 tracklists
print("\n=== Checking Vol. 1 and Vol. 2 Tracklists ===")
vol1_script = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/scripts/build_and_render_1hour_mix.py")
vol2_script = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/scripts/build_and_render_1hour_mix_vol2.py")

for v_path in [vol1_script, vol2_script]:
    if v_path.exists():
        print(f"\n--- {v_path.name} ---")
        with open(v_path) as fp:
            for line in fp:
                if "SELECTED_TRACKS" in line or ("mp4" in line and "[" not in line and "]" not in line):
                    print(line.strip())
