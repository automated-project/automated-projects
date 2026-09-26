import os, wave, glob
import numpy as np

folder = "/Users/base/Downloads/ch2-flow-mix"

target_files = [
    "Malibu Dusk.wav", "Amber Horizon.wav", "Pacific Gold.wav", 
    "Roll On.wav", "Sunset Boulevard Groove.wav", "Venice Coast Line.wav",
    "Terrace Floor.wav", "Slip Away.wav"
]

print("=== Detailed Defect Inspection ===")

for fname in target_files:
    p = os.path.join(folder, fname)
    if not os.path.exists(p): continue
    
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

        print(f"\n--- 🔍 {fname} ---")
        print(f"Sample Rate: {sr} Hz, Duration: {n_frames/sr:.2f}s ({n_frames/sr/60:.2f}m)")
        
        # 冒頭の飛び出し（DCオフセットやプチ音）
        print(f"Start 50ms max amplitude: {np.max(np.abs(data[:int(sr*0.05)])):.4f}")
        
        # スパイク（急激な変化）の発生タイムスタンプ
        diff = np.abs(np.diff(left))
        spike_indices = np.where(diff > 0.5)[0]
        if len(spike_indices) > 0:
            print(f"⚠️ Spikes found ({len(spike_indices)} locations):")
            for idx in spike_indices[:10]:
                sec = idx / sr
                print(f"   at {sec/60:.2f}m ({sec:.3f}s) - Jump magnitude: {diff[idx]:.4f}")
        else:
            print("✅ No harsh click spikes")
            
        # 音量 RMS の時間変化（急激な音量落ち込みや無音区間がないか）
        chunk_size = int(sr * 0.5) # 0.5秒ごと
        rms_curve = [np.sqrt(np.mean(data[i:i+chunk_size]**2)) for i in range(0, len(data), chunk_size)]
        min_rms = min(rms_curve[10:-10]) if len(rms_curve) > 20 else 0
        max_rms = max(rms_curve)
        print(f"RMS Dynamic Range: Min {min_rms:.4f}, Max {max_rms:.4f}")
