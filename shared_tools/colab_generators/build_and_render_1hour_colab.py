import os
import sys
import wave
import time
import subprocess
import numpy as np
from pathlib import Path

def main():
    print("🚀 [1/3] 音声結合開始...", flush=True)
    audio_dir = Path("/content/audio_tracks")
    wav_files = sorted(list(audio_dir.glob("*.wav")))
    sample_rate = 44100
    crossfade_sec = 2.5
    fade_samples = int(crossfade_sec * sample_rate)

    selected_tracks = []
    accumulated_sec = 0.0
    idx = 0
    while accumulated_sec < 3660.0:
        wav_p = wav_files[idx % len(wav_files)]
        selected_tracks.append(wav_p)
        with wave.open(str(wav_p), 'rb') as w:
            dur = w.getnframes() / w.getframerate()
            accumulated_sec += (dur - crossfade_sec)
        idx += 1

    track_data = []
    for p in selected_tracks:
        with wave.open(str(p), 'rb') as w:
            n_frames = w.getnframes()
            data = w.readframes(n_frames)
            arr = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            arr = arr.reshape(-1, w.getnchannels())
            track_data.append(arr)

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

    peak = np.max(np.abs(output_audio))
    if peak > 0.95:
        output_audio *= (0.95 / peak)

    os.makedirs("/content/render_work", exist_ok=True)
    combined_wav = "/content/render_work/combined_1hour.wav"
    int16_audio = (np.clip(output_audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    with wave.open(combined_wav, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(int16_audio.tobytes())

    actual_dur = len(int16_audio) / sample_rate
    print(f"✅ 音声結合完了: {actual_dur/60:.2f}分 ({actual_dur:.1f}秒)", flush=True)

    print("🎬 [2/3] 1時間4K動画レンダリング中...", flush=True)
    out_mp4 = "/content/render_work/haven_chill_1hour_4k_complete.mp4"
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", "1", "-i", "/content/cover_bg.png",
        "-i", combined_wav,
        "-t", f"{actual_dur:.3f}",
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-shortest", "-movflags", "+faststart",
        out_mp4
    ]
    proc = subprocess.Popen(cmd_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        if "frame=" in line or "time=" in line:
            print(line.strip(), flush=True)
    proc.wait()

    sz_mb = os.path.getsize(out_mp4) / (1024 * 1024)
    print(f"🎉 [3/3] レンダリング完了！ 出力: {out_mp4} (サイズ: {sz_mb:.2f} MB)", flush=True)

if __name__ == "__main__":
    main()
