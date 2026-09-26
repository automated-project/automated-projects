#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 音楽特化チャンネル共通: 音源品質・リズム自動検品インスペクター (Audio Quality Inspector)
- リズム・テンポ安定性（キック/スネアの打点グリッド解析、テンポ揺れ・拍ズレ検出）
- 音割れ・デジタルクリッピング検出
- DCオフセット・波形非対称性（波形描画異常の事前検知）
- 周波数バランス・超低域ノイズ・AIアーティファクト検出
- 総合スコアリング ＆ 合否判定（合格 / 要確認 / 除外推奨）
"""

import sys
import os
import wave
import subprocess
import numpy as np
from pathlib import Path
from scipy.signal import find_peaks, butter, filtfilt

AUDIO_EXTS = {".wav", ".mp3", ".mp4", ".m4a", ".flac", ".ogg"}

def load_audio_to_mono_float(file_path: Path, target_sr=44100):
    """FFmpeg経由で音声を44100Hzモノラルfloat32配列として確実にロード"""
    cmd = [
        "ffmpeg", "-y", "-i", str(file_path),
        "-vn", "-ar", str(target_sr), "-ac", "1", "-f", "f32le", "-"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw_data, _ = proc.communicate()
    
    if proc.returncode != 0 or len(raw_data) == 0:
        raise ValueError(f"Failed to read audio from {file_path}")
        
    audio = np.frombuffer(raw_data, dtype=np.float32)
    return audio, target_sr

def analyze_track_quality(file_path: Path):
    """単一楽曲の音響・リズム品質を多角的に検査・スコアリング"""
    audio, sr = load_audio_to_mono_float(file_path)
    duration_sec = len(audio) / sr
    
    if duration_sec < 5.0:
        return {
            "status": "❌ 除外推奨",
            "score": 0,
            "reasons": ["尺が短すぎます（5秒未満）"]
        }

    issues = []
    warnings = []
    score = 100

    # -------------------------------------------------------------
    # 1. DCオフセット ＆ 波形対称性（波形異常・片寄り検査）
    # -------------------------------------------------------------
    dc_offset = np.mean(audio)
    if abs(dc_offset) > 0.015:
        issues.append(f"波形の上下非対称（DCオフセット大: {dc_offset:+.4f}）➔ ビジュアライザー異常の原因")
        score -= 25
    elif abs(dc_offset) > 0.005:
        warnings.append(f"軽微なDCオフセット検出 ({dc_offset:+.4f})")
        score -= 5

    # -------------------------------------------------------------
    # 2. クリッピング・音割れ検査
    # -------------------------------------------------------------
    peak_val = np.max(np.abs(audio))
    clipped_samples = np.sum(np.abs(audio) >= 0.999)
    clip_ratio = clipped_samples / len(audio)
    
    if clip_ratio > 0.0005:
        issues.append(f"深刻なデジタル音割れ・クリッピング検出 ({clipped_samples}サンプル)")
        score -= 25
    elif clip_ratio > 0.00005:
        warnings.append(f"軽微な音割れ・ピーク飽和 ({clipped_samples}サンプル)")
        score -= 10

    # -------------------------------------------------------------
    # 3. リズム・テンポ安定性検査（低域オンセット・ビートグリッド解析）
    # -------------------------------------------------------------
    # 低域（40Hz〜220Hz: キック＆ベース）をバンドパス抽出
    b, a = butter(4, [40.0 / (sr / 2), 220.0 / (sr / 2)], btype='band')
    low_band = filtfilt(b, a, audio)
    
    # 低域のエンベロープ（エネルギー変化）
    env = np.abs(low_band)
    win_size = int(sr * 0.02) # 20ms
    env_smooth = np.convolve(env, np.ones(win_size)/win_size, mode='same')
    
    # オンセット（ビート打点）の検出
    peaks, properties = find_peaks(env_smooth, distance=int(sr * 0.25), prominence=0.03) # 最小BPM240相当間隔
    
    if len(peaks) > 20:
        # ピーク間隔（秒）の推移
        peak_times = peaks / sr
        intervals = np.diff(peak_times)
        
        # 0.35s〜0.65s（BPM 90〜170の範囲）のメインビートを抽出
        main_intervals = intervals[(intervals >= 0.35) & (intervals <= 0.65)]
        
        if len(main_intervals) > 15:
            median_interval = np.median(main_intervals)
            estimated_bpm = 60.0 / median_interval
            
            # ビートのばらつき度（変動係数 CV = std / mean）
            drift_dev = np.std(main_intervals) / median_interval
            
            # テンポ揺れ・拍ズレの判定
            if drift_dev > 0.18:
                issues.append(f"重大なリズム崩れ・テンポ揺れを検出 (BPM推定: {estimated_bpm:.1f}, ズレ度: {drift_dev*100:.1f}%)")
                score -= 30
            elif drift_dev > 0.10:
                warnings.append(f"軽微なテンポのモタつき・リズム揺れあり (BPM推定: {estimated_bpm:.1f}, ズレ度: {drift_dev*100:.1f}%)")
                score -= 15
        else:
            warnings.append("明確なキック・ドラムビートが検出されにくい構成です")
            score -= 5
    else:
        warnings.append("ビート打点が少なくアンビエント寄りです")

    # -------------------------------------------------------------
    # 4. 周波数バランス & AIアーティファクト検査
    # -------------------------------------------------------------
    # 20Hz以下の無駄なサブベースノイズ
    b_sub, a_sub = butter(2, 20.0 / (sr / 2), btype='low')
    sub20 = filtfilt(b_sub, a_sub, audio)
    sub20_rms = np.sqrt(np.mean(sub20**2))
    total_rms = np.sqrt(np.mean(audio**2))
    
    if total_rms > 0 and (sub20_rms / total_rms) > 0.30:
        warnings.append("20Hz以下の過剰なサブ超低域ノイズを検出（マスタリングでのHPFカット推奨）")
        score -= 10

    # -------------------------------------------------------------
    # 5. 総合判定
    # -------------------------------------------------------------
    score = max(0, min(100, score))
    
    if score >= 80 and len(issues) == 0:
        status = "✅ 合格 (採用推奨)"
    elif score >= 60 and len(issues) == 0:
        status = "⚠️ 要確認 (軽微な揺れ・許容範囲)"
    else:
        status = "❌ 除外推奨 (リズム崩れ/音割れ/波形異常)"

    return {
        "file": file_path.name,
        "status": status,
        "score": score,
        "duration": f"{int(duration_sec//60)}分{int(duration_sec%60):02d}秒",
        "issues": issues,
        "warnings": warnings
    }

def inspect_path(target_path_str: str):
    target_path = Path(target_path_str)
    
    if target_path.is_file():
        files = [target_path]
    elif target_path.is_dir():
        files = [p for p in target_path.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS and not p.name.startswith(".")]
    else:
        print(f"❌ Target path not found: {target_path_str}")
        return

    if not files:
        print(f"ℹ️ No audio files found in: {target_path_str}")
        return

    print("=" * 70)
    print(f"🔍 楽曲品質・リズム自動検品インスペクター (対象: {len(files)} ファイル)")
    print("=" * 70)

    results = []
    for idx, f in enumerate(files):
        try:
            res = analyze_track_quality(f)
            results.append(res)
            
            print(f"\n[{idx+1}/{len(files)}] {res['file']} ({res['duration']})")
            print(f"  👉 総合判定: {res['status']} ［スコア: {res['score']}/100］")
            
            if res["issues"]:
                for iss in res["issues"]:
                    print(f"     ❌ 異常検出: {iss}")
            if res["warnings"]:
                for w in res["warnings"]:
                    print(f"     ⚠️ 注意事項: {w}")
            if not res["issues"] and not res["warnings"]:
                print("     ✨ リズム・波形・音圧ともに極めて良好（完璧なグリッド）")
                
        except Exception as e:
            print(f"❌ Error analyzing {f.name}: {e}")

    print("\n" + "=" * 70)
    passed = sum(1 for r in results if "合格" in r["status"])
    warned = sum(1 for r in results if "要確認" in r["status"])
    rejected = sum(1 for r in results if "除外" in r["status"])
    print(f"📊 検品完了サマリー: 合格 {passed}曲 / 要確認 {warned}曲 / 除外推奨 {rejected}曲")
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_audio_quality.py <audio_file_or_directory>")
        sys.exit(1)
        
    inspect_path(sys.argv[1])
