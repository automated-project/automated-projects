import os, sys, subprocess, time, wave
import numpy as np
from pathlib import Path
from PIL import Image

# 1. 完全合格の2曲
TRACK1 = "/Users/base/Downloads/ch2-flow-mix/Neon Horizon.wav"
TRACK2 = "/Users/base/Downloads/ch2-flow-mix/Twilight Tide.wav"
IMAGE_IN = "/Users/base/Downloads/Gemini_Generated_Image_cxs9rncxs9rncxs9.jpeg"

OUT_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/output_videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUT_DIR / "temp_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_WAV = TEMP_DIR / "ch2_2tracks_natural_mix.wav"
OUT_MP4 = OUT_DIR / "CH2_VELVET_SUNSET_2TRACKS_4K_MINI3BARS.mp4"
BG_4K = TEMP_DIR / "bg_4k.png"

print("🎵 [1/3] 2曲の自然余白保持 2.5秒DJクロスフェード合成中...")

def read_wav_mono_stereo(p):
    with wave.open(p, "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        n = w.getnframes()
        raw = w.readframes(n)
        d = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if ch == 2:
            d = d.reshape(-1, 2)
        else:
            d = np.column_stack((d, d))
        return d, sr

d1, sr1 = read_wav_mono_stereo(TRACK1)
d2, sr2 = read_wav_mono_stereo(TRACK2)

# 2.5秒等エネルギー (cos/sin) クロスフェード (無音トリムなし・自然な余白維持)
crossfade_sec = 2.5
fade_samples = int(crossfade_sec * sr1)

t_in = np.linspace(0, np.pi / 2, fade_samples, endpoint=False, dtype=np.float32)
in_curve = np.sin(t_in)[:, np.newaxis]
out_curve = np.cos(t_in)[:, np.newaxis]

total_samples = len(d1) + len(d2) - fade_samples
combined = np.zeros((total_samples, 2), dtype=np.float32)

combined[:len(d1)] += d1
overlap_start = len(d1) - fade_samples
combined[overlap_start:overlap_start + fade_samples] = (
    d1[overlap_start:] * out_curve + d2[:fade_samples] * in_curve
)
combined[overlap_start + fade_samples:] = d2[fade_samples:]

# ピーク保護 (0.95)
peak = np.max(np.abs(combined))
if peak > 0.95:
    combined *= (0.95 / peak)

int16_out = (np.clip(combined, -1.0, 1.0) * 32767.0).astype(np.int16)
with wave.open(str(OUT_WAV), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(sr1)
    w.writeframes(int16_out.tobytes())

total_dur = len(int16_out) / sr1
print(f"✅ 音声結合完了: {OUT_WAV} (総尺: {total_dur/60:.2f}分 / {total_dur:.1f}秒)")

print("🎨 [2/3] 4K (3840x2160) 背景画像 Lanczosアップスケール中...")
with Image.open(IMAGE_IN) as im:
    im_rgb = im.convert("RGB")
    im_resized = im_rgb.resize((3840, 2160), Image.Resampling.LANCZOS)
    im_resized.save(str(BG_4K), "PNG")
print(f"✅ 4K背景画像準備完了: {BG_4K}")

print("🎬 [3/3] 右下隅・極小3本ネオンバー波形 ＋ 4K MP4 レンダリング開始...")

# 右下隅の極小3本ネオンバー (showfreqs で低音・中音・高音の3本のみ抽出)
# サイズ: 64x40px, 色: Sunset Orange (#FF8C32), 位置: 右下 (x=3680, y=2040)
filter_complex = (
    "[0:v]scale=3840:2160[bg];"
    "[1:a]asplit=2[a_out][a_for_bars];"
    "[a_for_bars]showfreqs=s=64x40:mode=bar:ascale=cbrt:fscale=lin:colors=0xFF8C32@0.9:win_size=1024[bars_raw];"
    "[bars_raw]format=rgba,colorchannelmixer=aa=0.85[bars_clean];"
    "[bg][bars_clean]overlay=W-w-120:H-h-100:format=auto[v_out]"
)

cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-framerate", "30", "-i", str(BG_4K),
    "-i", str(OUT_WAV),
    "-filter_complex", filter_complex,
    "-map", "[v_out]",
    "-map", "[a_out]",
    "-t", f"{total_dur:.3f}",
    "-c:v", "h264_videotoolbox", "-b:v", "9500k", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
    "-shortest", "-movflags", "+faststart",
    str(OUT_MP4)
]

t0 = time.time()
subprocess.run(cmd, check=True)
render_time = time.time() - t0
sz_mb = os.path.getsize(str(OUT_MP4)) / (1024 * 1024)

print(f"\n🎉🎉🎉 4K動画レンダリング完全完了！")
print(f"📁 出力先: {OUT_MP4}")
print(f"📊 ファイルサイズ: {sz_mb:.2f} MB")
print(f"⏱️ レンダリング時間: {render_time:.1f}秒 ({render_time/60:.2f}分)")
