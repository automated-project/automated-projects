#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): 1時間長尺 Feel-Good Pop Mix (Vol. 2) ビルドスクリプト
- 音源: mastered_audio/wav/ のみ使用 (全21曲 / 約61分)
- 背景: cover_art/Gemini_Generated_Image_i4ej4zi4ej4zi4ej.jpeg (ピュアアート / エフェクトなし)
- 音響: 事前マスタリング済音源の 2.5秒 DJ等エネルギー(cos/sin)クロスフェード合成 (二重マスタリング完全禁止)
- 出力: output_videos/1HOUR_FEEL_GOOD_POP_MIX_VOL2.mp4
"""

import os
import sys
import wave
import math
import shutil
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
AUDIO_DIR = BASE_DIR / "mastered_audio/wav"
BG_IMAGE_PATH = BASE_DIR / "cover_art/Gemini_Generated_Image_i4ej4zi4ej4zi4ej.jpeg"
OUTPUT_DIR = BASE_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_sunroof_vol2_build"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_VIDEO = OUTPUT_DIR / "1HOUR_FEEL_GOOD_POP_MIX_VOL2.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "1HOUR_FEEL_GOOD_POP_MIX_VOL2_chapters.txt"
COMBINED_WAV = TEMP_DIR / "mastered_combined_mix.wav"

WIDTH, HEIGHT = 1920, 1080
FPS = 30
SAMPLE_RATE = 44100
CROSSFADE_SEC = 2.5
CROSSFADE_SAMPLES = int(CROSSFADE_SEC * SAMPLE_RATE)

# 21曲のトラックリスト（テンポ・曲調を交互に配置し、リスナーを飽きさせない構成）
TRACK_LIST = [
    "Dancing_Into_Day.wav",           # 1. 王道サニーポップダンス (確定1曲目)
    "Saturday_Sunny_Acoustic.wav",   # 2. 軽快アコースティックカッティング
    "Funky_Good_Mood_Beat.wav",      # 3. ファンキーブラス・グルーヴ
    "Standing_Eight_Feet_Tall.wav",  # 4. 高揚感ビッグアンセム
    "Sunlit_Heaven.wav",             # 5. 口笛＆クラップ・晴天ポップ
    "Motown_Bouncy_Groove.wav",      # 6. モータウン・弾むベース
    "Roadside_Stars.wav",            # 7. クリスタルクリア・疾走感
    "Sweet_Acoustic_Breeze.wav",     # 8. 爽やかアコギブリーズ
    "Kings_of_the_Open_Sky.wav",     # 9. 壮大ボーカルアンセム
    "Caught_In_A_Morning_Smile.wav", # 10. 朝の爽やかポップ
    "Chasing_Every_Shadow.wav",      # 11. ダンサブル・シンセ＆ビート
    "Drifting_on_the_Golden_Tide.wav",# 12. チルクルーズ・スムーズ
    "Make_The_Whole_World_Shine.wav",# 13. ホーン＆アコギ・多幸感
    "Barefoot_on_Silver_Shores.wav", # 14. ビーチサイド・アコースティック
    "Heartbeat_Stereo_Anthem.wav",   # 15. 1D風アップビート
    "Carefree_Summer_Windows.wav",   # 16. サンルーフドライブ・ポップ
    "Chasing_The_Golden_Light.wav",  # 17. ゴールドアワー・メロディック
    "Chasing_Every_Cloud.wav",       # 18. 軽快ドライブボーカル
    "Written_in_the_Sky.wav",        # 19. エモーショナル・アンセム
    "Golden_Hour_Euphoria.wav",      # 20. 夕暮れユーフォリア
    "Chasing_the_Golden_Mile.wav"    # 21. 壮大フィナーレアンセム
]

def check_all_tracks_exist():
    missing = []
    for t in TRACK_LIST:
        p = AUDIO_DIR / t
        if not p.exists():
            missing.append(t)
    if missing:
        print(f"❌ Error: Missing audio files in {AUDIO_DIR}:\n" + "\n".join(missing), file=sys.stderr)
        sys.exit(1)
    print(f"✅ Verified: All {len(TRACK_LIST)} mastered tracks exist.")

def trim_silence(input_wav, out_wav):
    """無音テールを自動トリミング"""
    cmd = [
        "ffmpeg", "-y", "-i", str(input_wav),
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-48dB",
        "-vn", "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out_wav)
    ]
    subprocess.run(cmd, capture_output=True, check=True)

def load_wav_as_float(wav_path):
    with wave.open(str(wav_path), 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
    
    if sampwidth == 2:
        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    elif sampwidth == 3:
        raw = np.frombuffer(data, dtype=np.uint8)
        audio = (raw[0::3].astype(np.int32) | (raw[1::3].astype(np.int32) << 8) | (raw[2::3].astype(np.int32) << 16))
        audio = np.where(audio >= 0x800000, audio - 0x1000000, audio).astype(np.float32) / 8388608.0
    else:
        raise ValueError(f"Unsupported sample width: {sampwidth}")
    
    audio = audio.reshape(-1, n_channels)
    return audio

def save_float_as_wav(audio_data, out_path):
    audio_int16 = np.clip(audio_data * 32767.0, -32768.0, 32767.0).astype(np.int16)
    with wave.open(str(out_path), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_int16.tobytes())

def build_seamless_dj_mix():
    print("=== Step 1: Trimming Audio Tails ===")
    wav_files = []
    for idx, track_name in enumerate(TRACK_LIST):
        src_wav = AUDIO_DIR / track_name
        dest_wav = TEMP_DIR / f"track_{idx:02d}.wav"
        print(f"[{idx+1:02d}/{len(TRACK_LIST)}] Trimming: {track_name}")
        trim_silence(src_wav, dest_wav)
        wav_files.append((track_name, dest_wav))
    
    print("\n=== Step 2: Equal-Power 2.5s DJ Crossfading ===")
    combined_audio = None
    chapters = []
    current_time_sec = 0.0
    
    # cos/sin equal-power curve
    t = np.linspace(0, np.pi / 2, CROSSFADE_SAMPLES, endpoint=True, dtype=np.float32)
    fade_out = np.cos(t)[:, np.newaxis]
    fade_in = np.sin(t)[:, np.newaxis]
    
    for idx, (track_name, wav_p) in enumerate(wav_files):
        track_audio = load_wav_as_float(wav_p)
        clean_title = track_name.replace(".wav", "").replace("_", " ")
        
        mins = int(current_time_sec // 60)
        secs = int(current_time_sec % 60)
        timestamp_str = f"{mins:02d}:{secs:02d}"
        chapters.append(f"{timestamp_str} - {clean_title}")
        print(f"[{timestamp_str}] Track {idx+1:02d}: {clean_title}")
        
        if combined_audio is None:
            combined_audio = track_audio
            current_time_sec += len(track_audio) / SAMPLE_RATE
        else:
            # Overlap last 2.5s with next track first 2.5s
            overlap_tail = combined_audio[-CROSSFADE_SAMPLES:]
            overlap_head = track_audio[:CROSSFADE_SAMPLES]
            
            blended = overlap_tail * fade_out + overlap_head * fade_in
            combined_audio = np.vstack([
                combined_audio[:-CROSSFADE_SAMPLES],
                blended,
                track_audio[CROSSFADE_SAMPLES:]
            ])
            
            track_net_len = (len(track_audio) - CROSSFADE_SAMPLES) / SAMPLE_RATE
            current_time_sec += track_net_len
            
    print(f"\nTotal Mix Duration: {current_time_sec/60:.2f} minutes ({current_time_sec:.1f} seconds)")
    
    # Save combined audio directly (no double mastering)
    save_float_as_wav(combined_audio, COMBINED_WAV)
    print(f"✅ Combined Audio Saved to: {COMBINED_WAV}")
    
    # Save chapters file
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as cf:
        cf.write("\n".join(chapters) + "\n")
    print(f"✅ Saved Chapters to: {CHAPTERS_FILE}")

def render_full_video():
    print("\n=== Step 3: Video Encoding (Pure High-Def Art + 1080p 30fps) ===")
    bg_1080p = TEMP_DIR / "bg_1080p.jpg"
    img = Image.open(BG_IMAGE_PATH).convert('RGB')
    
    # 16:9 クロップ & 高画質リサイズ
    img_w, img_h = img.size
    target_ratio = WIDTH / HEIGHT
    cur_ratio = img_w / img_h
    if cur_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        img = img.crop((0, top, img_w, top + new_h))
        
    img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    img.save(bg_1080p, quality=98)
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(bg_1080p),
        "-i", str(COMBINED_WAV),
        "-c:v", "h264_videotoolbox",
        "-b:v", "3000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        str(OUT_VIDEO)
    ]
    print(f"Encoding full video to: {OUT_VIDEO}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg Error: {res.stderr}", file=sys.stderr)
        sys.exit(1)
        
    print(f"\n🎉 Video Render Completed Successfully: {OUT_VIDEO}")
    print(f"File Size: {os.path.getsize(OUT_VIDEO) / 1024 / 1024:.2f} MB")
    
    # Cleanup temp dir
    shutil.rmtree(TEMP_DIR)
    print("Cleaned up temp build directory.")

if __name__ == "__main__":
    check_all_tracks_exist()
    build_seamless_dj_mix()
    render_full_video()
