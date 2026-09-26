#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Flow 2大欠陥（音飛び＆ピッチ崩壊）確定インスペクター
- ユーザー指定の2曲を完全に捕捉し、全26曲を厳密に選別・隔離する
  ① Take My Jacket (1) 2:26型 孤立クリック音飛び (突発比率 Ratio >= 4.5 & Max >= 0.30)
  ② Terrace Floor 2:37型 ピッチ急変・オートチューン乱れ (20msでの非音楽的F0急変 >= 3箇所)
"""

import os
import sys
import glob
import shutil
import wave
import numpy as np

def inspect_track(p):
    fname = os.path.basename(p)
    with wave.open(p, "rb") as w:
        sr = w.getframerate()
        n = w.getnframes()
        dur = n / sr
        data = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        if w.getnchannels() == 2:
            left = data[0::2]
            right = data[1::2]
        else:
            left = data
            right = data
        mono = 0.5 * (left + right)

    defects = []
    margin = int(sr * 0.5)

    # ① 音飛び検知（Take My Jacket (1) 2:26を包含）
    dl = np.abs(np.diff(left))
    dr = np.abs(np.diff(right))
    win = 50
    glitches = []
    for i in range(margin, len(dl) - margin - win, win // 2):
        chunk_l = dl[i:i+win]
        mean_l = np.mean(chunk_l)
        max_l = np.max(chunk_l)
        if mean_l > 0 and (max_l / mean_l) >= 4.5 and max_l >= 0.30:
            glitches.append(i / sr)
        else:
            chunk_r = dr[i:i+win]
            mean_r = np.mean(chunk_r)
            max_r = np.max(chunk_r)
            if mean_r > 0 and (max_r / mean_r) >= 4.5 and max_r >= 0.30:
                glitches.append(i / sr)

    clean_glitches = []
    for g in glitches:
        if not clean_glitches or (g - clean_glitches[-1]) > 0.5:
            clean_glitches.append(g)

    if len(clean_glitches) > 0:
        locs = ", ".join([f"{int(t//60)}:{t%60:05.2f}" for t in clean_glitches[:3]])
        defects.append(f"音飛び/クリック ({len(clean_glitches)}箇所: {locs})")

    # ② ピッチ異常検知（Terrace Floor 2:37を包含）
    win_p = int(sr * 0.05)
    hop_p = int(sr * 0.02)
    p_anomalies = []
    prev_f0 = None
    for i in range(margin, len(mono) - margin - win_p, hop_p):
        seg = mono[i:i+win_p]
        if np.max(np.abs(seg)) > 0.08:
            corr = np.correlate(seg, seg, mode="full")
            corr = corr[len(corr)//2:]
            min_l, max_l = int(sr/500), int(sr/80)
            if max_l < len(corr) and np.max(corr[min_l:max_l]) > 0.50 * corr[0]:
                f0 = sr / (min_l + np.argmax(corr[min_l:max_l]))
                if prev_f0 and abs(f0 - prev_f0) > 60.0:
                    t = i / sr
                    if not p_anomalies or (t - p_anomalies[-1]) > 1.0:
                        p_anomalies.append(t)
                prev_f0 = f0
            else:
                prev_f0 = None

    if len(p_anomalies) >= 3:
        locs = ", ".join([f"{int(t//60)}:{t%60:05.2f}" for t in p_anomalies[:3]])
        defects.append(f"ピッチ崩壊 ({len(p_anomalies)}箇所: {locs})")

    return {
        "file": p,
        "name": fname,
        "duration": dur,
        "passed": len(defects) == 0,
        "defects": defects
    }

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/base/Downloads/ch2-flow-mix"
    isolate = "--isolate" in sys.argv
    files = sorted([f for f in glob.glob(os.path.join(target_dir, "*.wav")) if not os.path.basename(f).startswith(".") and "defective_tracks" not in f])
    
    defect_dir = os.path.join(target_dir, "defective_tracks")
    if isolate:
        os.makedirs(defect_dir, exist_ok=True)
        
    passed_list = []
    failed_list = []
    
    header = f"No | Track Name                   | Dur   | Status   | Defect Details"
    print(f"🔍 [2大欠陥スキャン] Take My Jacket型・Terrace Floor型 確定選別 (全{len(files)}曲)\n")
    print(header)
    print("-" * 85)
    for idx, f in enumerate(files, 1):
        res = inspect_track(f)
        if res["passed"]:
            passed_list.append(res)
            st = "✅ PASS"
            df = "Clean"
        else:
            failed_list.append(res)
            st = "❌ FAIL"
            df = "; ".join(res["defects"])
            if isolate:
                dest = os.path.join(defect_dir, os.path.basename(f))
                shutil.move(f, dest)
                df += f" -> [Moved to {os.path.basename(defect_dir)}]"
        print(f"{idx:02d} | {res['name'][:28]:<28} | {res['duration']/60:4.2f}m | {st:<8} | {df}")
        
    print("=" * 85)
    print(f"📊 最終選別結果: 合格 {len(passed_list)}曲 / 欠陥検知 {len(failed_list)}曲")
    if isolate:
        print(f"📁 欠陥のある {len(failed_list)}曲 を {defect_dir} へ安全に隔離しました。")
