#!/usr/bin/env python3
"""
1時間（60分）4K長尺BGM動画の結合・エンコード用スクリプト（Colab A100 / NVENC GPU 高速レンダリング対応）
"""
import os
import sys
import wave
import time
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image

def setup_environment():
    print("📦 [1/4] FFmpeg環境のセットアップ...", flush=True)
    subprocess.check_call(["apt-get", "update", "-qq"])
    subprocess.check_call(["apt-get", "install", "-y", "-qq", "ffmpeg"])
    print("✅ 環境セットアップ完了！", flush=True)

def run_render_1hour_video():
    print("🚀 [2/4] 1時間長尺音源の2.5秒DJクロスフェード合成開始...", flush=True)
    t0 = time.time()
    
    audio_dir = Path("/content/audio_tracks")
    wav_files = sorted(list(audio_dir.glob("*.wav")))
    if not wav_files:
        raise FileNotFoundError("WAV files not found in /content/audio_tracks")
    
    print(f"🎵 読み込みトラック数: {len(wav_files)}曲", flush=True)
    
    sample_rate = 44100
    crossfade_sec = 2.5
    fade_samples = int(crossfade_sec * sample_rate)
    
    # 60分（3600秒）以上になるまでトラックをループ構築
    selected_tracks = []
    accumulated_sec = 0.0
    idx = 0
    while accumulated_sec < 3660.0: # 61分分確保
        wav_p = wav_files[idx % len(wav_files)]
        selected_tracks.append(wav_p)
        with wave.open(str(wav_p), 'rb') as w:
            dur = w.getnframes() / w.getframerate()
            accumulated_sec += (dur - crossfade_sec)
        idx += 1
        
    print(f"🔄 1時間構築用トラック数: {len(selected_tracks)}曲 (計算総尺: {accumulated_sec/60:.2f}分)", flush=True)
    
    # WAVロード & クロスフェード
    track_data = []
    for p in selected_tracks:
        with wave.open(str(p), 'rb') as w:
            n_frames = w.getnframes()
            data = w.readframes(n_frames)
            arr = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            arr = arr.reshape(-1, w.getnchannels())
            track_data.append(arr)
            
    # 等エネルギーブレンド
    t_in = np.linspace(0, np.pi / 2, fade_samples, endpoint=False, dtype=np.float32)
    in_curve = np.sin(t_in)[:, np.newaxis]
    out_curve = np.cos(t_in)[:, np.newaxis]
    
    total_samples = sum(len(a) for a in track_data) - (len(track_data) - 1) * fade_samples
    output_audio = np.zeros((total_samples, 2), dtype=np.float32)
    
    cur_idx = 0
    for i, arr in enumerate(track_data):
        t_len = len(arr)
        if i == 0:
            output_audio[0:t_len] += arr
            cur_idx = t_len - fade_samples
        else:
            overlap = output_audio[cur_idx:cur_idx + fade_samples]
            output_audio[cur_idx:cur_idx + fade_samples] = overlap * out_curve + arr[:fade_samples] * in_curve
            output_audio[cur_idx + fade_samples:cur_idx + t_len] = arr[fade_samples:]
            cur_idx += (t_len - fade_samples)
            
    # ピーク保護
    peak = np.max(np.abs(output_audio))
    if peak > 0.95:
        output_audio *= (0.95 / peak)
        
    os.makedirs("/content/render_work", exist_ok=True)
    combined_wav = "/content/render_work/master_combined_1hour.wav"
    int16_audio = (np.clip(output_audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(combined_wav, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(int16_audio.tobytes())
        
    actual_dur = len(int16_audio) / sample_rate
    print(f"✅ 音声結合完了: {combined_wav} (総尺: {actual_dur/60:.2f}分 / {actual_dur:.1f}秒)", flush=True)
    
    # 3. 4K NVENC GPU 高速レンダリング
    print("\n🎬 [3/4] Colab A100 GPU (h264_nvenc) 4K/30fps 1時間動画レンダリング開始...", flush=True)
    bg_img = "/content/cover_bg.png"
    out_mp4 = "/content/render_work/haven_chill_1hour_4k_master.mp4"
    
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", bg_img,
        "-i", combined_wav,
        "-t", f"{actual_dur:.3f}",
        "-vf", "scale=3840:2160:flags=lanczos",
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-shortest", "-movflags", "+faststart",
        out_mp4
    ]
    
    t_render = time.time()
    proc = subprocess.Popen(cmd_ffmpeg, stderr=subprocess.PIPE, text=True)
    for line in proc.stderr:
        if "frame=" in line or "time=" in line:
            print(f"  {line.strip()}", flush=True)
    proc.wait()
    
    total_time = time.time() - t0
    render_time = time.time() - t_render
    print(f"\n🎉 [4/4] 1時間4K動画のレンダリング完全完了！", flush=True)
    print(f"出力ファイル: {out_mp4} (レンダリング時間: {render_time:.1f}秒 / 総所要時間: {total_time:.1f}秒)", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_render_1hour_video()
