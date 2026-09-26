import numpy as np
import wave
import struct

sample_rate = 44100
duration = 6.0 # 6秒のショート動画
total_samples = int(sample_rate * duration)
audio = np.zeros(total_samples)

# 1. ボール発射・スイング時の風切り音（0.5秒〜1.2秒）
t = np.linspace(0, duration, total_samples)
whoosh_idx = int(0.5 * sample_rate)
whoosh_len = int(0.8 * sample_rate)
t_w = np.linspace(0, 0.8, whoosh_len)
whoosh = np.sin(2 * np.pi * (80 + 180 * t_w) * t_w) * np.sin(t_w / 0.8 * np.pi) * 0.35
audio[whoosh_idx:whoosh_idx+whoosh_len] += whoosh

# 2. 激突音（1.3秒：ドォォン！という重低音インパクト）
hit_idx = int(1.3 * sample_rate)
hit_len = int(1.5 * sample_rate)
t_h = np.linspace(0, 1.5, hit_len)
# サブベース + ノイズクラッシュ
impact_sub = np.sin(2 * np.pi * 55 * np.exp(-t_h * 3.0) * t_h) * np.exp(-t_h * 2.5) * 0.8
noise_burst = np.random.normal(0, 1, hit_len) * np.exp(-t_h * 8.0) * 0.4
audio[hit_idx:hit_idx+hit_len] += (impact_sub + noise_burst)

# 3. ブロック散乱・カラカラ音（1.4秒〜5.5秒）
np.random.seed(101)
debris_times = np.sort(np.random.uniform(1.35, 5.2, 45))
for dt in debris_times:
    d_idx = int(dt * sample_rate)
    d_len = int(0.12 * sample_rate)
    if d_idx + d_len > total_samples:
        d_len = total_samples - d_idx
    t_d = np.linspace(0, d_len / sample_rate, d_len)
    freq = np.random.uniform(400, 1600)
    clack = np.sin(2 * np.pi * freq * t_d) * np.exp(-t_d * 35.0) * np.random.uniform(0.15, 0.35)
    audio[d_idx:d_idx+d_len] += clack

# 4. フィニッシュ・シグナル音（5.5秒）
fin_idx = int(5.4 * sample_rate)
fin_len = int(0.5 * sample_rate)
t_f = np.linspace(0, 0.5, fin_len)
bell = np.sin(2 * np.pi * 880 * t_f) * np.exp(-t_f * 6.0) * 0.3
audio[fin_idx:fin_idx+fin_len] += bell

# 正規化
audio = audio / np.max(np.abs(audio)) * 0.92

out_wav = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets/smash_tower_sound.wav"
with wave.open(out_wav, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    packed_data = struct.pack(f'<{len(audio)}h', *(int(s * 32767) for s in audio))
    wf.writeframes(packed_data)

print("Generated smash sound to", out_wav)
