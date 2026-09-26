#!/usr/bin/env python3
import os, glob, wave, numpy as np

def inspect_pure_human_hearing(file_path):
    fname = os.path.basename(file_path)
    with wave.open(file_path, "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        n_frames = w.getnframes()
        dur = n_frames / sr
        raw = w.readframes(n_frames)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if ch == 2:
            left = data[0::2]
            right = data[1::2]
        else:
            left = data
            right = data

    defects = []

    # 1. クリッピング・極端な物理ジャンプ (1.0を超えるクリップや 0.90超の瞬時断絶)
    dl = np.abs(np.diff(left))
    dr = np.abs(np.diff(right))
    hard_jumps = np.where((dl > 0.90) | (dr > 0.90))[0]
    if len(hard_jumps) > 0:
        loc_str = ", ".join([f"{int((j/sr)//60)}:{(j/sr)%60:05.2f}" for j in hard_jumps[:2]])
        defects.append(f"Hard Discontinuity (>0.90) at {loc_str}")

    # 2. 演奏途中の不自然な無音（曲の最初と最後の無音を除いた、途中で100ms以上完全無音になるドロップアウト）
    mid_start = int(sr * 2.0)
    mid_end = int(len(left) - sr * 2.0)
    mid_l = left[mid_start:mid_end]
    zeros_l = (mid_l == 0.0)
    zero_runs = np.diff(np.where(np.concatenate(([zeros_l[0]], zeros_l[:-1] != zeros_l[1:], [True])))[0])[::2]
    # 100ms以上のドロップアウト (sr * 0.1)
    if len(zero_runs) > 0 and np.max(zero_runs) >= int(sr * 0.10):
        defects.append("Mid-track Drop-out (Silence >= 100ms)")

    # 3. 極端な音量破綻（曲全体がほとんど聞こえない -25 LUFS以下）
    rms = np.sqrt(np.mean(left**2))
    approx_lufs = 20 * np.log10(rms + 1e-9) - 3.0
    if approx_lufs < -26.0:
        defects.append(f"Too Quiet (~{approx_lufs:.1f} LUFS)")

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
        res = inspect_pure_human_hearing(f)
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
    print(f"📊 人間の耳基準でのスキャン結果: 合格 {passed}曲 / 致命的欠陥 {failed}曲")
