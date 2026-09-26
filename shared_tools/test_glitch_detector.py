import numpy as np
import wave
import os

p_bad_jump = "/Users/base/Downloads/ch2-flow-mix/Take My Jacket (1).wav"
p_bad_pitch = "/Users/base/Downloads/ch2-flow-mix/Terrace Floor.wav"
p_good = "/Users/base/Downloads/ch2-flow-mix/Carmel Coastline.wav"

def analyze_track_physics(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        n_frames = w.getnframes()
        raw = w.readframes(n_frames)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if w.getnchannels() == 2:
            data = data.reshape(-1, 2)
            mono = np.mean(data, axis=1)
        else:
            mono = data

    # 1. 不連続ジャンプ (2階微分 / 加速度の急激な破綻)
    # スネアやキックは連続した高周波波形だが、音飛びは1サンプルだけ逆位相や孤立ジャンプする
    diff1 = np.diff(mono)
    diff2 = np.diff(diff1)
    
    # 孤立したスパイク点（前後は滑らかだが1点だけ突き抜けている）
    isolated_spikes = []
    for i in range(1, len(diff1)-1):
        if abs(diff1[i]) > 0.25 and abs(diff1[i-1]) < 0.08 and abs(diff1[i+1]) < 0.08:
            isolated_spikes.append((i/sr, abs(diff1[i])))

    print(f"\n--- {os.path.basename(path)} ---")
    print(f"Isolated Glitch Spikes: {len(isolated_spikes)}")
    for t, mag in isolated_spikes[:5]:
        print(f"  ⚡ Glitch Jump at {int(t//60)}:{t%60:05.2f} ({t:.3f}s) - Magnitude: {mag:.4f}")

analyze_track_physics(p_bad_jump)
analyze_track_physics(p_bad_pitch)
analyze_track_physics(p_good)
