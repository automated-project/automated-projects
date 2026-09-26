# -*- coding: utf-8 -*-
"""
Compare Amber_Flame and Amber_Horizon audio waveforms & spectral content
"""
import subprocess
import wave
import numpy as np

for fname in ["Amber_Flame.mp4", "Amber_Horizon.mp4"]:
    fpath = f"/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/raw_audio/1hour-mix/{fname}"
    cmd = ["ffmpeg", "-y", "-i", fpath, "-vn", "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", f"/tmp/{fname}.wav"]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

with wave.open("/tmp/Amber_Flame.mp4.wav", "rb") as w1, wave.open("/tmp/Amber_Horizon.mp4.wav", "rb") as w2:
    d1 = np.frombuffer(w1.readframes(w1.getnframes()), dtype=np.int16).astype(np.float32)
    d2 = np.frombuffer(w2.readframes(w2.getnframes()), dtype=np.int16).astype(np.float32)

print(f"Amber_Flame length: {len(d1)/44100:.2f}s, RMS: {np.sqrt(np.mean(d1**2)):.2f}")
print(f"Amber_Horizon length: {len(d2)/44100:.2f}s, RMS: {np.sqrt(np.mean(d2**2)):.2f}")

# Cross-correlate on segment
min_len = min(len(d1), len(d2))
corr = np.corrcoef(d1[:min_len], d2[:min_len])[0, 1]
print(f"Direct Segment Correlation: {corr:.4f}")

# Envelope correlation
env1 = np.abs(d1)[:min_len:1000]
env2 = np.abs(d2)[:min_len:1000]
print(f"Envelope Correlation: {np.corrcoef(env1, env2)[0,1]:.4f}")
