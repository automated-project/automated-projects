import numpy as np
import wave
import struct

sample_rate = 44100
duration = 4.0 # 4.0秒の極短・ループ向けショート
total_samples = int(sample_rate * duration)
audio = np.zeros(total_samples)

# 1. 落下時の微小な風切り音（0.3秒〜0.8秒）
t_w = np.linspace(0, 0.5, int(0.5 * sample_rate))
whoosh = np.sin(2 * np.pi * 120 * t_w) * np.sin(t_w / 0.5 * np.pi) * 0.15
audio[int(0.3 * sample_rate):int(0.3 * sample_rate) + len(whoosh)] += whoosh

# 2. ワイヤー切断音（0.9秒：スパッ！という超高周波スライス音）
t_s = np.linspace(0, 0.25, int(0.25 * sample_rate))
# 高周波スイープ + ホワイトノイズ・スライス
slice_sound = np.sin(2 * np.pi * (3200 - 1500 * t_s) * t_s) * np.exp(-t_s * 25.0) * 0.6
slice_noise = np.random.normal(0, 1, len(t_s)) * np.exp(-t_s * 35.0) * 0.35
audio[int(0.9 * sample_rate):int(0.9 * sample_rate) + len(t_s)] += (slice_sound + slice_noise)

# 3. サイコロゼリーの着地・ぷるぷるボヨヨン音（1.4秒〜2.2秒）
t_j = np.linspace(0, 0.8, int(0.8 * sample_rate))
# 弾力のあるサブベース・ウォブル（ぷるんっ）
jelly_wobble = np.sin(2 * np.pi * (180 + 40 * np.sin(2 * np.pi * 12.0 * t_j)) * t_j) * np.exp(-t_j * 6.0) * 0.55
# 湿ったペチャッという表面音
wet_click = np.random.normal(0, 1, len(t_j)) * np.exp(-t_j * 40.0) * 0.25
audio[int(1.4 * sample_rate):int(1.4 * sample_rate) + len(t_j)] += (jelly_wobble + wet_click)

# 正規化
audio = audio / np.max(np.abs(audio)) * 0.92

out_wav = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets/jelly_slice_sound.wav"
with wave.open(out_wav, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    packed_data = struct.pack(f'<{len(audio)}h', *(int(s * 32767) for s in audio))
    wf.writeframes(packed_data)

print("Generated Jelly Slice ASMR sound to", out_wav)
