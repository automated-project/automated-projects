#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI音源分離 (Demucs) ＋ AIピッチ解析 (CREPE) による完全自動・高精度欠陥インスペクター
- 1本の完成曲を vocals / other / drums / bass に分離
- vocals: CREPEによるピッチ追跡（ドラムや和音ノイズなしでオートチューン崩壊を完全検知）
- other/vocals: ドラムを排除したトラックで真のクリック・音飛びを検知
"""

import os
import sys
import glob
import wave
import torch
import torchcrepe
import soundfile as sf
import numpy as np
import demucs.separate
from pathlib import Path

BASE_DIR = "/Users/base/Downloads/ch2-flow-mix"
SEP_DIR = "/Users/base/Downloads/ch2-flow-mix/ai_separated"
os.makedirs(SEP_DIR, exist_ok=True)

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"🚀 AI音源分離＆ピッチ検査エンジン起動 (Device: {device})\n")

files = sorted(glob.glob(os.path.join(BASE_DIR, "*.wav")))
# ai_separatedやdefective_tracks除外
files = [f for f in files if not os.path.basename(f).startswith(".") and "ai_separated" not in f and "defective" not in f]

print(f"📁 スキャン対象: {len(files)} 曲\n")

results = []

for idx, f in enumerate(files, 1):
    fname = os.path.basename(f)
    track_name = os.path.splitext(fname)[0]
    track_out_dir = os.path.join(SEP_DIR, "htdemucs", track_name)
    
    print(f"[{idx:02d}/{len(files):02d}] 🧠 AI解析中: {fname} ...", flush=True)
    
    # 1. Demucs による4トラック分離
    if not os.path.exists(track_out_dir):
        print(f"   ➔ [Step 1] Demucs 音源分離中...", flush=True)
        demucs.separate.main(["-n", "htdemucs", "-d", device, f, "-o", SEP_DIR])
        
    vocal_path = os.path.join(track_out_dir, "vocals.wav")
    other_path = os.path.join(track_out_dir, "other.wav")
    
    defects = []
    
    # 2. ボーカルトラックの CREPE AI ピッチ解析
    if os.path.exists(vocal_path):
        v_audio, sr = sf.read(vocal_path)
        if len(v_audio.shape) > 1:
            v_mono = np.mean(v_audio, axis=1)
        else:
            v_mono = v_audio
            
        v_tensor = torch.from_numpy(v_mono).unsqueeze(0).float().to(device)
        hop_length = int(sr / 100) # 10ms
        
        # 65Hz〜750Hz のボーカル帯域でピッチ推定
        pitch, periodicity = torchcrepe.predict(
            v_tensor, sr, hop_length=hop_length,
            fmin=65, fmax=750, model='tiny',
            device=device, batch_size=2048, return_periodicity=True
        )
        pitch = pitch.squeeze().cpu().numpy()
        periodicity = periodicity.squeeze().cpu().numpy()
        confidence = periodicity
        
        times = np.arange(len(pitch)) * (hop_length / sr)
        vocal_glitches = []
        for i in range(1, len(pitch)):
            # 確信度が高い歌声区間でのみ、10msで40Hz以上のカクッとした急変を検知
            if confidence[i] > 0.70 and confidence[i-1] > 0.70:
                p_diff = abs(pitch[i] - pitch[i-1])
                if p_diff > 40.0:
                    t = times[i]
                    if not vocal_glitches or (t - vocal_glitches[-1]) > 0.5:
                        vocal_glitches.append(t)
                        
        if len(vocal_glitches) >= 2:
            locs = ", ".join([f"{int(t//60)}:{t%60:05.2f}" for t in vocal_glitches[:3]])
            defects.append(f"ボーカルピッチ崩壊 ({len(vocal_glitches)}箇所: {locs})")

    # 3. 伴奏トラック（ドラムなし）の孤立スパイク検知
    if os.path.exists(other_path):
        o_audio, sr = sf.read(other_path)
        if len(o_audio.shape) > 1:
            o_mono = np.mean(o_audio, axis=1)
        else:
            o_mono = o_audio
            
        dl = np.abs(np.diff(o_mono))
        win = 50
        margin = int(sr * 0.5)
        isolated_clicks = []
        for i in range(margin, len(dl) - margin - win, win // 2):
            chunk = dl[i:i+win]
            mean_d = np.mean(chunk)
            max_d = np.max(chunk)
            if mean_d > 0 and (max_d / mean_d) > 6.0 and max_d > 0.18:
                t = i / sr
                if not isolated_clicks or (t - isolated_clicks[-1]) > 0.5:
                    isolated_clicks.append(t)
                    
        if len(isolated_clicks) > 0:
            locs = ", ".join([f"{int(t//60)}:{t%60:05.2f}" for t in isolated_clicks[:3]])
            defects.append(f"伴奏音飛び/クリック ({len(isolated_clicks)}箇所: {locs})")

    status = "❌ FAIL" if defects else "✅ PASS"
    details = "; ".join(defects) if defects else "Clean (No defects)"
    print(f"   ➔ 結果: {status} | {details}\n", flush=True)
    results.append({"name": fname, "status": status, "defects": details})

print("=" * 85)
print("📊 【AI音源分離＋CREPEピッチ解析 最終検査レポート】")
print("=" * 85)
for r in results:
    print(f"{r['status']:<8} | {r['name'][:28]:<28} | {r['defects']}")
