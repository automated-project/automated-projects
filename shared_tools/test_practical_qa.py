#!/usr/bin/env python3
import os, glob, wave, numpy as np

def inspect_practical(file_path):
    fname = os.path.basename(file_path)
    with wave.open(file_path, "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        n_frames = w.getnframes()
        dur = n_frames / sr
        raw = w.readframes(n_frames)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if ch == 2:
            data = data.reshape(-1, 2)
            mono = np.mean(data, axis=1)
            left = data[:, 0]
            right = data[:, 1]
        else:
            mono = data
            left = data
            right = data

    defects = []

    # 1. 物理クリッピング・巨大ジャンプ (>0.90)
    dl = np.abs(np.diff(left))
    dr = np.abs(np.diff(right))
    hard_jumps = np.where((dl > 0.90) | (dr > 0.90))[0]
    if len(hard_jumps) > 0:
        loc_str = ", ".join([f"{int((j/sr)//60)}:{(j/sr)%60:05.2f}" for j in hard_jumps[:2]])
        defects.append(f"Hard Discontinuity (>0.90) at {loc_str}")

    # 2. ドロップアウト (>=10ms無音)
    zeros_l = (left == 0.0)
    zero_runs = np.diff(np.where(np.concatenate(([zeros_l[0]], zeros_l[:-1] != zeros_l[1:], [True])))[0])[::2]
    if len(zero_runs) > 0 and np.max(zero_runs) >= int(sr * 0.01):
        defects.append("Audio Dropout (>=10ms silence)")

    # 3. 極小音量
    rms = np.sqrt(np.mean(mono**2))
    approx_lufs = 20 * np.log10(rms + 1e-9) - 3.0
    if approx_lufs < -22.0:
        defects.append(f"Severely Low Volume (~{approx_lufs:.1f} LUFS)")

    # 4. ピッチ崩壊
    window_size = int(sr * 0.05)
    hop_size = int(sr * 0.02)
    pitches = []
    for i in range(0, len(mono) - window_size, hop_size):
        seg = mono[i:i+window_size]
        corr = np.correlate(seg, seg, mode="full")
        corr = corr[len(corr)//2:]
        min_lag = int(sr / 600)
        max_lag = int(sr / 70)
        if max_lag < len(corr) and np.max(corr[min_lag:max_lag]) > 0.4 * corr[0]:
            peak_lag = min_lag + np.argmax(corr[min_lag:max_lag])
            pitches.append(sr / peak_lag)
        else:
            pitches.append(0)
    pitches = np.array(pitches)
    p_diff = np.abs(np.diff(pitches))
    severe_warps = np.where((p_diff > 75.0) & (pitches[:-1] > 0) & (pitches[1:] > 0))[0]
    if len(severe_warps) >= 20:
        defects.append(f"Severe Pitch Warping ({len(severe_warps)} chaotic events)")

    return {
        "fname": fname,
        "duration": dur,
        "passed": len(defects) == 0,
        "defects": defects
    }

if __name__ == "__main__":
    files = sorted(glob.glob("/Users/base/Downloads/ch2-flow-mix/*.wav"))
    header = f"No | Track Name                   | Dur   | Status   | Defect Details"
    print(header)
    print("-" * len(header))
    passed = 0
    failed = 0
    for idx, f in enumerate(files, 1):
        res = inspect_practical(f)
        if res["passed"]:
            passed += 1
            st = "✅ PASS"
            df = "Clean"
        else:
            failed += 1
            st = "❌ FAIL"
            df = "; ".join(res["defects"])
        print(f"{idx:02d} | {res['fname'][:28]:<28} | {res['duration']/60:4.2f}m | {st:<8} | {df}")

    print("=" * len(header))
    print(f"📊 実用基準での結果: 合格 {passed}曲 / 欠陥検知 {failed}曲")
