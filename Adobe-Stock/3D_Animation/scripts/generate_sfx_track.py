import wave
import struct
import math
import subprocess
import os

sr = 44100
total_duration = 15.0 # 15秒
total_samples = int(sr * total_duration)

# 10ステージの切断タイミング（秒）と着地タイミング（秒）
stages = [
    (0.00, 0.75, 1.15), # 1
    (1.50, 2.25, 2.65), # 2
    (3.00, 3.75, 4.15), # 3
    (4.50, 5.25, 5.65), # 4
    (6.00, 6.75, 7.15), # 5
    (7.50, 8.25, 8.65), # 6
    (9.00, 9.75, 10.15),# 7
    (10.50, 11.25, 11.65),# 8
    (12.00, 12.75, 13.15),# 9
    (13.50, 14.25, 14.65) # 10
]

sfx_buffer = [0.0] * total_samples

for idx, (t_start, t_cut, t_land) in enumerate(stages):
    # 1. 鋭い切断音 (Slicing sound: 高周波周波数スイープ 2800Hz -> 600Hz + ノイズ)
    cut_sample = int(t_cut * sr)
    cut_len = int(0.12 * sr) # 120ms
    for i in range(cut_len):
        if cut_sample + i < total_samples:
            p = i / cut_len
            freq = 2800.0 * (1.0 - p)**1.8 + 500.0
            # サイン波 + ノイズ成分
            phase = 2.0 * math.pi * freq * (i / sr)
            env = math.exp(-p * 8.0) * math.sin(math.pi * p)
            sample_val = (0.75 * math.sin(phase) + 0.25 * ((hash(f"{idx}_{i}") % 1000)/500.0 - 1.0)) * env * 0.85
            sfx_buffer[cut_sample + i] += sample_val

    # 2. ぷるぷる着地音 (Landing Squash: 低周波80Hzサイン波 + ボヨヨン倍音)
    land_sample = int(t_land * sr)
    land_len = int(0.28 * sr) # 280ms
    for i in range(land_len):
        if land_sample + i < total_samples:
            p = i / land_len
            # ベース周波数
            f_base = 75.0 + 35.0 * math.sin(2.0 * math.pi * 9.0 * p) # 9Hzのぷるぷる揺れ
            phase_base = 2.0 * math.pi * f_base * (i / sr)
            
            # 高周波倍音 (ポヨヨン)
            f_high = 320.0 * (1.0 - p)**1.2 + 120.0
            phase_high = 2.0 * math.pi * f_high * (i / sr)
            
            env = math.exp(-p * 5.0)
            sample_val = (0.60 * math.sin(phase_base) + 0.40 * math.sin(phase_high)) * env * 0.90
            sfx_buffer[land_sample + i] += sample_val

# クリッピング防止（ノーマライズ）
max_val = max(max(abs(s) for s in sfx_buffer), 1.0)
sfx_samples_int = [int((s / max_val) * 30000.0) for s in sfx_buffer]

out_sfx_wav = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets/rhythm_sfx_15s.wav"
with wave.open(out_sfx_wav, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    raw_data = struct.pack(f"{len(sfx_samples_int)}h", *sfx_samples_int)
    wf.writeframes(raw_data)

print(f"Generated 15-second ASMR SFX track to {out_sfx_wav}")
