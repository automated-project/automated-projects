import numpy as np
import wave
import os

p_bad_pitch = "/Users/base/Downloads/ch2-flow-mix/Terrace Floor.wav"
p_good = "/Users/base/Downloads/ch2-flow-mix/Carmel Coastline.wav"
p_clean = "/Users/base/Downloads/ch2-flow-mix/Santa Barbara Sunset.wav"

def analyze_vocal_stability(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        n_frames = w.getnframes()
        raw = w.readframes(n_frames)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if w.getnchannels() == 2:
            data = data.reshape(-1, 2)
            mono = np.mean(data, axis=1)
        else:
            mono = data

    # 100ms窓、50msステップでスペクトル不連続性（オートチューン/ピッチ崩壊）を解析
    # ピッチの揺れではなく、高調波の位相コヒーレンス破壊（位相の瞬間的ズレ）を測定
    window_size = int(sr * 0.1) # 100ms
    hop = int(sr * 0.05)        # 50ms
    
    spectral_flux = []
    times = []
    
    prev_mag = None
    for i in range(0, len(mono) - window_size, hop):
        seg = mono[i:i+window_size] * np.hanning(window_size)
        spec = np.fft.rfft(seg)
        mag = np.abs(spec)
        
        if prev_mag is not None:
            # 50ms間でのスペクトルの急激な破壊・歪み量 (Spectral Flux)
            flux = np.sum((mag - prev_mag)**2) / len(mag)
            spectral_flux.append(flux)
            times.append(i / sr)
        prev_mag = mag

    spectral_flux = np.array(spectral_flux)
    times = np.array(times)
    
    # 異常値の検出
    mean_f = np.mean(spectral_flux)
    std_f = np.std(spectral_flux)
    outliers = np.where(spectral_flux > (mean_f + 4.0 * std_f))[0]
    
    print(f"\n--- {os.path.basename(path)} ---")
    print(f"Mean Flux: {mean_f:.4f}, Std: {std_f:.4f}, Extreme Anomalies (>4 sigma): {len(outliers)}")
    for idx in outliers:
        t = times[idx]
        print(f"  🚨 Spectral Chaos/Warp at {int(t//60)}:{t%60:05.2f} ({t:.3f}s) - Score: {spectral_flux[idx]:.4f}")

analyze_vocal_stability(p_bad_pitch)
analyze_vocal_stability(p_good)
analyze_vocal_stability(p_clean)
