import os, wave
import numpy as np

p = "/Users/base/Downloads/ch2-flow-mix/Terrace Floor.wav"

with wave.open(p, "rb") as w:
    sr = w.getframerate()
    ch = w.getnchannels()
    n_frames = w.getnframes()
    raw = w.readframes(n_frames)
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        data = data.reshape(-1, 2)
        left = data[:, 0]
        right = data[:, 1]
    else:
        left = data
        right = data

# 2:34 から 2:42 (154.0s - 162.0s) の区間を解析
start_sec = 154.0
end_sec = 162.0
s_idx = int(start_sec * sr)
e_idx = int(end_sec * sr)

sub_l = left[s_idx:e_idx]
sub_r = right[s_idx:e_idx]

# 1. ゼロクロス周期によるピッチ・基本周波数（F0）変動検出
# 2. 短時間フーリエ変換 / 自己相関によるピッチ不安定性（ワウフラッター / ピッチグリッチ）
window_size = int(sr * 0.05) # 50ms窓
hop_size = int(sr * 0.01)    # 10msステップ

pitches = []
times = []
for i in range(0, len(sub_l) - window_size, hop_size):
    segment = sub_l[i:i+window_size]
    # 自己相関
    corr = np.correlate(segment, segment, mode='full')
    corr = corr[len(corr)//2:]
    
    # ピッチピーク検出 (50Hz - 800Hz)
    min_lag = int(sr / 800)
    max_lag = int(sr / 50)
    if max_lag < len(corr):
        peak_lag = min_lag + np.argmax(corr[min_lag:max_lag])
        freq = sr / peak_lag
        pitches.append(freq)
        times.append(start_sec + (i / sr))

pitches = np.array(pitches)
times = np.array(times)

# ピッチの急激な微分（10msでの極端な周波数ワープ）
pitch_diff = np.abs(np.diff(pitches))

print("=== Pitch & Waveform Micro-Analysis around 2:37 in Terrace Floor.wav ===")

# ピッチ急変ポイント
glitch_indices = np.where(pitch_diff > 40.0)[0]
print(f"Significant pitch jump events (>40Hz jump in 10ms): {len(glitch_indices)}")
for idx in glitch_indices:
    t = times[idx]
    m = int(t // 60)
    s = t % 60
    print(f"  👉 Pitch anomaly at {m}:{s:05.2f} ({t:.3f}s) - Jump from {pitches[idx]:.1f}Hz to {pitches[idx+1]:.1f}Hz (Delta: {pitch_diff[idx]:.1f}Hz)")

# 2:35 - 2:40 の区間クリップを保存
import subprocess
clip_path = "/tmp/inspect_terrace_floor_235_240.wav"
cmd = [
    "ffmpeg", "-y", "-ss", "154", "-to", "162",
    "-i", p, "-c", "copy", clip_path
]
subprocess.run(cmd, check=True)
print(f"Inspection clip saved to: {clip_path}")
