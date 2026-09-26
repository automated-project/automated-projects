import os, wave
import numpy as np

p = "/Users/base/Downloads/ch2-flow-mix/Take My Jacket (1).wav"

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

# 2:24 から 2:28 (144.0s - 148.0s) の区間を高解像度解析
start_sec = 143.0
end_sec = 149.0
s_idx = int(start_sec * sr)
e_idx = int(end_sec * sr)

sub_l = left[s_idx:e_idx]
sub_r = right[s_idx:e_idx]

# 1. 微分値（サンプルの瞬間的ジャンプ / クリック）
diff_l = np.abs(np.diff(sub_l))
diff_r = np.abs(np.diff(sub_r))

# 2. ゼロサンプルの連続（完全な欠落・ドロップアウト）
zeros_l = (np.abs(sub_l) == 0)
zeros_r = (np.abs(sub_r) == 0)

# 3. リズム・ビートの不連続性（エネルギーの瞬間的断絶）
chunk = int(sr * 0.01) # 10msごと
energy = [np.sum(sub_l[i:i+chunk]**2) for i in range(0, len(sub_l), chunk)]

print("=== Analyzing 2:23 - 2:29 in Take My Jacket (1).wav ===")
print(f"Sample Rate: {sr} Hz")

# ジャンプ箇所の検出
jumps = np.where((diff_l > 0.3) | (diff_r > 0.3))[0]
print(f"Abrupt jumps (>0.3) found: {len(jumps)}")
for j in jumps:
    exact_sec = start_sec + (j / sr)
    m = int(exact_sec // 60)
    s = exact_sec % 60
    print(f"  👉 Jump at {m}:{s:05.2f} ({exact_sec:.3f}s) - L jump: {diff_l[j]:.4f}, R jump: {diff_r[j]:.4f}")

# ゼロ区間の検出
consec_zeros = 0
for i, z in enumerate(zeros_l):
    if z:
        consec_zeros += 1
    else:
        if consec_zeros > 5:
            exact_sec = start_sec + ((i - consec_zeros) / sr)
            print(f"  ⚠️ Drop-out (Silence) of {consec_zeros} samples at {exact_sec:.3f}s")
        consec_zeros = 0

# 2:24 - 2:28 の波形をクリップ保存して確認用に出力
import subprocess
clip_path = "/tmp/inspect_take_my_jacket_224_228.wav"
cmd = [
    "ffmpeg", "-y", "-ss", "143", "-to", "149",
    "-i", p, "-c", "copy", clip_path
]
subprocess.run(cmd, check=True)
print(f"Inspection clip saved to: {clip_path}")
