import os, glob, wave, subprocess
import numpy as np

folder = "/Users/base/Downloads/ch2-flow-mix"
files = sorted(glob.glob(os.path.join(folder, "*.wav")))

print("=== Scanning 26 Tracks in /Users/base/Downloads/ch2-flow-mix ===")

report = []
for p in files:
    fname = os.path.basename(p)
    cmd = ["ffmpeg", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stderr
    
    lufs = -99.0
    tp = -99.0
    for line in out.split("\n"):
        if "I:" in line and "LUFS" in line:
            parts = line.split()
            try:
                lufs = float(parts[parts.index("I:") + 1])
            except: pass
        if "Peak:" in line and "dBFS" in line:
            parts = line.split()
            try:
                tp = float(parts[parts.index("Peak:") + 1])
            except: pass

    with wave.open(p, "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        n_frames = w.getnframes()
        dur = n_frames / sr
        raw = w.readframes(n_frames)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if ch == 2:
            data = data.reshape(-1, 2)
            left = data[:, 0]
            right = data[:, 1]
        else:
            left = data
            right = data

        # クリッピング検知
        clip_count = int(np.sum(np.abs(data) >= 0.999))
        
        # 突発的スパイク（プチッという急激なデジタルノイズ）
        diff_l = np.abs(np.diff(left))
        diff_r = np.abs(np.diff(right))
        spike_count = int(np.sum(diff_l > 0.6) + np.sum(diff_r > 0.6))
        
        # 末尾の不自然なぶつ切りチェック (最後の100サンプルの振幅)
        tail_amplitude = float(np.max(np.abs(data[-100:])))
        
        # 冒頭の不自然な立ち上がりチェック (最初の100サンプルの最大振幅)
        head_amplitude = float(np.max(np.abs(data[:100])))

        report.append({
            "name": fname,
            "dur": dur,
            "lufs": lufs,
            "tp": tp,
            "clip": clip_count,
            "spike": spike_count,
            "head_amp": head_amplitude,
            "tail_amp": tail_amplitude
        })

print("{:<2} | {:<26} | {:<6} | {:<6} | {:<6} | {:<5} | {:<6} | {:<8} | {:<8}".format(
    "#", "Title", "Dur", "LUFS", "Peak", "Clip", "Spikes", "HeadAmp", "TailAmp"
))
print("-" * 90)
for i, r in enumerate(report, 1):
    warn = ""
    if r["spike"] > 0: warn += "[SPIKE!] "
    if r["clip"] > 10: warn += "[CLIPPING] "
    if r["tail_amp"] > 0.1: warn += "[TAIL CUT!] "
    if r["lufs"] < -19.0 or r["lufs"] > -11.0: warn += "[LUFS ABNORMAL] "
    
    print("{:02d} | {:<26} | {:4.2f}m | {:>5.1f} | {:>5.1f} | {:>5} | {:>6} | {:>8.4f} | {:>8.4f} {}".format(
        i, r["name"][:25], r["dur"]/60.0, r["lufs"], r["tp"], r["clip"], r["spike"], r["head_amp"], r["tail_amp"], warn
    ))
