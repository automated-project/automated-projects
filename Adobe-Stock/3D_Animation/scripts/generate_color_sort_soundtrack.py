import numpy as np
import wave
import struct

sample_rate = 44100
duration = 8.0
total_samples = int(sample_rate * duration)
audio = np.zeros(total_samples)

# 1. 落下時・渦巻きの環境音（ソフトな摩擦・ローリングノイズ）
np.random.seed(42)
white_noise = np.random.normal(0, 1, total_samples)
# ローパスフィルター代わりの平滑化
b, a = [0.05], [1, -0.95]
rolling_noise = np.convolve(white_noise, np.ones(50)/50, mode='same')
# エンベロープ（0.5秒〜6.5秒にかけて盛り上がる）
t = np.linspace(0, duration, total_samples)
roll_env = np.clip(np.sin(t / duration * np.pi), 0, 1) ** 1.5
audio += rolling_noise * roll_env * 0.12

# 2. カラーソート・シリンダー吸い込みメロディ音（木琴・マリンバ風のパーカッシブな音階）
# 4色に対応するペンタトニック音階（C5: 523.25, E5: 659.25, G5: 783.99, A5: 880.00, C6: 1046.50）
notes = [523.25, 659.25, 783.99, 880.00, 1046.50]

def add_marimba_pluck(freq, start_time, volume=0.35):
    start_idx = int(start_time * sample_rate)
    sound_len = int(0.35 * sample_rate)
    if start_idx + sound_len > total_samples:
        sound_len = total_samples - start_idx
    
    t_pluck = np.linspace(0, sound_len / sample_rate, sound_len)
    # 基本波 + 倍音
    sine1 = np.sin(2 * np.pi * freq * t_pluck)
    sine2 = 0.3 * np.sin(2 * np.pi * freq * 2.0 * t_pluck)
    sine3 = 0.15 * np.sin(2 * np.pi * freq * 3.0 * t_pluck)
    
    # 指数関数的減衰（コツンというアタック）
    env = np.exp(-t_pluck * 16.0)
    audio[start_idx:start_idx+sound_len] += (sine1 + sine2 + sine3) * env * volume

# 1.5秒から6.8秒にかけて次々と吸い込まれるポップ音・メロディ
current_time = 1.6
note_idx = 0
while current_time < 6.8:
    add_marimba_pluck(notes[note_idx % len(notes)], current_time, volume=0.28)
    current_time += np.random.uniform(0.08, 0.18)
    note_idx += 1

# 3. 完璧なフィニッシュ・チャイム（6.8秒：コード一斉鳴らし）
for f in [523.25, 659.25, 783.99, 1046.50]:
    add_marimba_pluck(f, 6.85, volume=0.2)

# 正規化（クリッピング防止）
max_val = np.max(np.abs(audio))
if max_val > 0:
    audio = audio / max_val * 0.9

# WAV書き出し
out_wav = "/Users/base/Automated-Projects/YouTube/02_3D_Animation/audio_assets/color_sorter_asmr.wav"
with wave.open(out_wav, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    packed_data = struct.pack(f'<{len(audio)}h', *(int(s * 32767) for s in audio))
    wf.writeframes(packed_data)

print("Generated ASMR soundscape to", out_wav)
