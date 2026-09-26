import numpy as np
import wave
import struct

sample_rate = 44100
duration = 6.0
total_samples = int(sample_rate * duration)
audio = np.zeros(total_samples)

# 80枚のドミノが倒れるリズミカルで心地よい連続カタカタ音（ウッド・プラスチック打撃音）
# ペンタトニック音階（C Major Pentatonic）を上昇させながら鳴らし、音楽的快感を作る
base_notes = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99, 880.00, 1046.50]

for i in range(80):
    t_hit = (10 + i * 1.8) / 30.0 # フレームから秒へ変換
    if t_hit >= duration - 0.2:
        break
    start_idx = int(t_hit * sample_rate)
    sound_len = int(0.08 * sample_rate)
    if start_idx + sound_len > total_samples:
        sound_len = total_samples - start_idx
        
    t_s = np.linspace(0, sound_len / sample_rate, sound_len)
    
    # 旋律的ピッチ（徐々に上がっていく）
    freq = base_notes[i % len(base_notes)] * (1.0 + (i / 80.0) * 0.5)
    # 打撃クラック + クリック
    sine = np.sin(2 * np.pi * freq * t_s)
    click = np.random.normal(0, 1, sound_len) * np.exp(-t_s * 80.0)
    env = np.exp(-t_s * 45.0)
    audio[start_idx:start_idx+sound_len] += (sine * 0.5 + click * 0.5) * env * 0.35

# 最後のフィニッシュ・ゴング（5.4秒）
fin_idx = int(5.3 * sample_rate)
fin_len = int(0.7 * sample_rate)
t_fin = np.linspace(0, 0.7, fin_len)
chime = (np.sin(2 * np.pi * 1046.5 * t_fin) + 0.4 * np.sin(2 * np.pi * 1318.5 * t_fin)) * np.exp(-t_fin * 5.0) * 0.4
audio[fin_idx:fin_idx+fin_len] += chime

# 正規化
audio = audio / np.max(np.abs(audio)) * 0.9

out_wav = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets/domino_asmr.wav"
with wave.open(out_wav, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    packed_data = struct.pack(f'<{len(audio)}h', *(int(s * 32767) for s in audio))
    wf.writeframes(packed_data)

print("Generated domino ASMR soundtrack to", out_wav)
