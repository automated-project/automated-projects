#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ch1 (Komorebi Chill Audio): 2時間（4セッション）ポモドーロ作業BGM完全自動ビルドパイプライン

【設計仕様】
1. 音源マスタリング: 集中15曲 & 休憩5曲を一括で Warm Analog EQ ＋ -14.0 LUFS にノーマライズ
2. タイムアライメント: 25分集中 ＋ 5分休憩 × 4セット ＝ きっちり 7200.0秒（120分00秒）
3. チャイム自動合成: セッション切り替え時（25分、30分、55分、60分、85分、90分、115分）にソフトベル音を自動挿入
4. 映像レンダリング: 実写風大図書館アート ＋ 72px特大Futuraタイマー ＋ プログレスバー（集中:ホワイト / 休憩:エメラルドグリーン）
5. 1080p 15fps H.264 (videotoolbox / 軽量・高品質約700MB)
6. YouTube概要欄用チャプターファイル自動生成
"""

import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
RAW_FOCUS_DIR = BASE_DIR / "raw_audio/集中"
RAW_BREAK_DIR = BASE_DIR / "raw_audio/休憩"
MASTERED_FOCUS_DIR = BASE_DIR / "mastered_audio/wav/focus"
MASTERED_BREAK_DIR = BASE_DIR / "mastered_audio/wav/break"
BG_IMAGE = BASE_DIR / "cover_art/bg_grand_library_real.jpeg"
OUT_DIR = BASE_DIR / "output_videos"
TEMP_DIR = OUT_DIR / "temp_pomodoro_2hour_build"

MASTERED_FOCUS_DIR.mkdir(parents=True, exist_ok=True)
MASTERED_BREAK_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

FULL_MIX_WAV = TEMP_DIR / "full_2hour_pomodoro_mix.wav"
OUT_VIDEO = OUT_DIR / "2HOUR_POMODORO_STUDY_WITH_ME_LIBRARY.mp4"
CHAPTERS_FILE = OUT_DIR / "2HOUR_POMODORO_STUDY_WITH_ME_LIBRARY_chapters.txt"

WIDTH = 1920
HEIGHT = 1080
FPS = 15  # 長尺動画の標準規格（軽量＆スムーズ）
FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"
SR = 48000

def generate_soft_chime(duration_sec=3.0):
    """耳に優しいチベタンベル／ソフトチャイム（3秒）を合成"""
    chime_path = TEMP_DIR / "soft_chime_3s.wav"
    t = np.linspace(0, duration_sec, int(SR * duration_sec), endpoint=False)
    
    # 基本周波数 (528Hz: 愛と奇跡の周波数 + 倍音)
    f0 = 528.0
    f1 = 1056.0
    f2 = 1584.0
    f3 = 2112.0
    
    env = np.exp(-t * 1.8) * np.sin(np.pi * np.minimum(t * 15.0, 1.0) / 2.0)
    sig = (
        0.50 * np.sin(2 * np.pi * f0 * t) +
        0.25 * np.sin(2 * np.pi * f1 * t) +
        0.15 * np.sin(2 * np.pi * f2 * t) +
        0.10 * np.sin(2 * np.pi * f3 * t)
    ) * env
    
    # ステレオ化 ＆ 微小ディレイで空間演出
    sig_l = sig
    sig_r = np.roll(sig, int(SR * 0.012))
    stereo = np.column_stack([sig_l, sig_r]) * 0.45
    stereo = np.clip(stereo * 32767, -32768, 32767).astype(np.int16)
    
    with wave.open(str(chime_path), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(stereo.tobytes())
        
    return chime_path

def master_all_tracks():
    """全20曲を一括マスタリング（Warm EQ + -14 LUFS / pcm_s16le統一）"""
    print("\n=== [1/4] MASTERING ALL 20 TRACKS ===")
    audio_filter = (
        "highpass=f=35,"
        "equalizer=f=180:width_type=q:w=1.2:g=1.8,"
        "equalizer=f=3200:width_type=q:w=1.0:g=-1.5,"
        "highshelf=f=8500:g=-2.0,"
        "lowpass=f=15000,"
        "loudnorm=I=-14.0:TP=-1.5:LRA=7.0"
    )
    
    # 集中15曲
    focus_files = sorted(RAW_FOCUS_DIR.glob("*.mp4"))
    for f in focus_files:
        out_w = MASTERED_FOCUS_DIR / f"{f.stem}.wav"
        print(f"  [+] Mastering Focus: {f.stem}")
        cmd = ["ffmpeg", "-y", "-i", str(f), "-vn", "-af", audio_filter, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(out_w)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    # 休憩5曲
    break_files = sorted(RAW_BREAK_DIR.glob("*.mp4"))
    for f in break_files:
        out_w = MASTERED_BREAK_DIR / f"{f.stem}.wav"
        print(f"  [+] Mastering Break: {f.stem}")
        cmd = ["ffmpeg", "-y", "-i", str(f), "-vn", "-af", audio_filter, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(out_w)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    print("✅ All 20 tracks mastered successfully!")

def load_wav_numpy(wav_path):
    with wave.open(str(wav_path), 'rb') as wf:
        n = wf.getnframes()
        raw = wf.readframes(n)
        width = wf.getsampwidth()
        n_ch = wf.getnchannels()
        
        if width == 2:
            return np.frombuffer(raw, dtype=np.int16).reshape(-1, n_ch).astype(np.float32)
        elif width == 3:
            # 24-bit PCM unpack
            a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
            # sign extend
            int24 = a[:, 0].astype(np.int32) | (a[:, 1].astype(np.int32) << 8) | (a[:, 2].astype(np.int32) << 16)
            int24[int24 >= 0x800000] -= 0x1000000
            return (int24.astype(np.float32) / 256.0).reshape(-1, n_ch)
        else:
            return np.frombuffer(raw, dtype=np.int16).reshape(-1, n_ch).astype(np.float32)

def crossfade_sequence(track_paths, target_duration_sec, crossfade_sec=2.5, end_fade_sec=3.0):
    """複数トラックをクロスフェードで接続し、target_duration_sec に完璧にアライメント"""
    cf_samples = int(SR * crossfade_sec)
    audio_list = [load_wav_numpy(p) for p in track_paths]
    
    combined = audio_list[0].copy()
    for nxt in audio_list[1:]:
        overlap_a = combined[-cf_samples:]
        overlap_b = nxt[:cf_samples]
        
        fade_out = np.linspace(1.0, 0.0, cf_samples)[:, None]
        fade_in = np.linspace(0.0, 1.0, cf_samples)[:, None]
        blended = (overlap_a * fade_out) + (overlap_b * fade_in)
        
        combined = np.vstack([combined[:-cf_samples], blended, nxt[cf_samples:]])
        
    target_samples = int(target_duration_sec * SR)
    if len(combined) > target_samples:
        combined = combined[:target_samples]
    elif len(combined) < target_samples:
        pad = np.zeros((target_samples - len(combined), 2), dtype=np.float32)
        combined = np.vstack([combined, pad])
        
    # 末尾フェードアウト
    fade_end_samples = int(SR * end_fade_sec)
    fo = np.linspace(1.0, 0.0, fade_end_samples)[:, None]
    combined[-fade_end_samples:] = combined[-fade_end_samples:] * fo
    
    return combined

def build_2hour_mix():
    """2時間（4セッション：25分+5分 × 4）の完璧な音声トラックを結合生成"""
    print("\n=== [2/4] BUILDING 2-HOUR AUDIO TIMELINE (120 MINS) ===")
    chime_path = generate_soft_chime()
    chime_audio = load_wav_numpy(chime_path)
    
    focus_tracks = sorted(MASTERED_FOCUS_DIR.glob("*.wav"))
    break_tracks = sorted(MASTERED_BREAK_DIR.glob("*.wav"))
    
    # 4セッション分のトラック配分
    # Focus: 1500秒 (25分), Break: 300秒 (5分)
    session_configs = [
        {"focus": focus_tracks[0:10], "break": [break_tracks[0], break_tracks[1]]},
        {"focus": focus_tracks[10:15] + focus_tracks[0:5], "break": [break_tracks[2], break_tracks[3]]},
        {"focus": focus_tracks[4:14], "break": [break_tracks[4], break_tracks[0]]},
        {"focus": [focus_tracks[14]] + focus_tracks[0:9], "break": [break_tracks[1], break_tracks[2]]}
    ]
    
    timeline_segments = []
    
    for s_idx, cfg in enumerate(session_configs):
        print(f"  [+] Processing Session {s_idx+1}/4 (Focus 25m + Break 5m)...")
        # 1. Focus 25分 (1500秒)
        focus_seg = crossfade_sequence(cfg["focus"], target_duration_sec=1500.0, crossfade_sec=2.5, end_fade_sec=3.0)
        
        # 2. Break 5分 (300秒)
        break_seg = crossfade_sequence(cfg["break"], target_duration_sec=300.0, crossfade_sec=3.0, end_fade_sec=3.0)
        
        # 3. チャイムを 25:00 の瞬間および 30:00 の瞬間にオーバーレイ
        # Focus終了時のチャイム (24分58秒〜25分01秒)
        chime_len = len(chime_audio)
        focus_seg[-chime_len:] = focus_seg[-chime_len:] + chime_audio
        
        # Break終了時のチャイム (29分58秒〜30分01秒 / ※最終セッション除く)
        if s_idx < 3:
            break_seg[-chime_len:] = break_seg[-chime_len:] + chime_audio
            
        timeline_segments.append(focus_seg)
        timeline_segments.append(break_seg)
        
    full_audio = np.vstack(timeline_segments)
    full_audio = np.clip(full_audio, -32768, 32767).astype(np.int16)
    
    with wave.open(str(FULL_MIX_WAV), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(full_audio.tobytes())
        
    total_sec = len(full_audio) / SR
    print(f"✅ Full 2-Hour Audio Generated: {FULL_MIX_WAV} ({total_sec:.2f}s = {total_sec/60:.2f} min)")
    
    # チャプターファイル生成
    chapters_text = (
        "00:00 - Session 1 (Focus 25 Min)\n"
        "25:00 - Break 1 (5 Min)\n"
        "30:00 - Session 2 (Focus 25 Min)\n"
        "55:00 - Break 2 (5 Min)\n"
        "1:00:00 - Session 3 (Focus 25 Min)\n"
        "1:25:00 - Break 3 (5 Min)\n"
        "1:30:00 - Session 4 (Focus 25 Min)\n"
        "1:55:00 - Break 4 (5 Min / Cooldown)\n"
    )
    with open(CHAPTERS_FILE, "w", encoding="utf-8") as f:
        f.write(chapters_text)
    print(f"✅ Chapters file saved: {CHAPTERS_FILE}")
    return total_sec

def load_font(size, index=4):
    try:
        return ImageFont.truetype(FUTURA_PATH, size, index=index)
    except Exception:
        try:
            return ImageFont.truetype(FUTURA_PATH, size, index=0)
        except Exception:
            return ImageFont.load_default()

def render_2hour_video(total_sec):
    """2時間ポモドーロ動画レンダリング（特大Futura 72px ＋ セッション別UI切替）"""
    print("\n=== [3/4] RENDERING 2-HOUR VIDEO (1080P 15FPS H.264) ===")
    total_frames = int(total_sec * FPS)

    # 1. Prepare Base Background Image (1920x1080)
    bg_orig = Image.open(BG_IMAGE).convert("RGBA")
    img_w, img_h = bg_orig.size
    target_ratio = WIDTH / HEIGHT
    cur_ratio = img_w / img_h

    if cur_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        bg_orig = bg_orig.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        bg_orig = bg_orig.crop((0, top, img_w, top + new_h))

    base_bg = bg_orig.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    # 2. Font (72px)
    font_large = load_font(72, index=4)

    # 3. FFmpeg Process (1080p 15fps, -b:v 650k, Hardware Accelerated)
    print(f"[+] Starting FFmpeg hardware encoder -> {OUT_VIDEO}")
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-i", str(FULL_MIX_WAV),
        "-c:v", "h264_videotoolbox",
        "-b:v", "650k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(OUT_VIDEO)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # UI Geometry parameters
    BAR_W = 800
    BAR_H = 8
    BAR_X = (WIDTH - BAR_W) // 2
    BAR_Y = 142

    SESSION_LEN_FOCUS = 1500.0  # 25分
    SESSION_LEN_BREAK = 300.0   # 5分
    CYCLE_LEN = 1800.0          # 30分

    for f_idx in range(total_frames):
        cur_sec = f_idx / FPS
        
        # 現在のセッション判定 (0〜30分周期)
        cycle_sec = cur_sec % CYCLE_LEN
        session_num = int(cur_sec // CYCLE_LEN) + 1
        
        if cycle_sec < SESSION_LEN_FOCUS:
            # 集中セッション (25分カウントダウン)
            is_focus = True
            sec_in_session = cycle_sec
            rem_sec = max(0.0, SESSION_LEN_FOCUS - sec_in_session)
            progress = sec_in_session / SESSION_LEN_FOCUS
            mode_title = f"STUDY SESSION"
            fill_color = (255, 255, 255, 245)  # ルミナスホワイト
        else:
            # 休憩セッション (5分カウントダウン)
            is_focus = False
            sec_in_session = cycle_sec - SESSION_LEN_FOCUS
            rem_sec = max(0.0, SESSION_LEN_BREAK - sec_in_session)
            progress = sec_in_session / SESSION_LEN_BREAK
            mode_title = f"BREAK TIME"
            fill_color = (80, 240, 160, 245)   # ソフトエメラルドグリーン

        # UI Overlay
        ui = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ui)

        # Top subtle gradient background
        draw.rectangle([0, 0, WIDTH, 175], fill=(0, 0, 0, 100))

        # Digital Countdown Timer
        m = int(rem_sec) // 60
        s = int(rem_sec) % 60
        timer_str = f"{m:02d}:{s:02d}"

        # 中央特大テキスト: "STUDY SESSION   25:00"
        center_text = f"{mode_title}   {timer_str}"
        bbox = font_large.getbbox(center_text)
        text_w = bbox[2] - bbox[0]
        text_x = (WIDTH - text_w) // 2
        draw.text((text_x, 42), center_text, font=font_large, fill=(255, 255, 255, 255))

        # Progress Bar Track & Fill
        fill_w = int(BAR_W * progress)
        draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + BAR_W, BAR_Y + BAR_H], radius=4, fill=(255, 255, 255, 45))
        if fill_w > 0:
            draw.rounded_rectangle([BAR_X, BAR_Y, BAR_X + fill_w, BAR_Y + BAR_H], radius=4, fill=fill_color)

        frame = Image.alpha_composite(base_bg, ui)
        proc.stdin.write(frame.tobytes())
        
        if f_idx % (FPS * 60) == 0:
            min_done = f_idx // (FPS * 60)
            print(f"    Render Progress: {min_done}/120 mins ({min_done/120*100:.1f}%)")

    proc.stdin.close()
    proc.wait()
    print(f"✅ 2-Hour Video Rendered: {OUT_VIDEO}")

def main():
    print("==================================================")
    print("🚀 CH1 2-HOUR POMODORO STUDY VIDEO BUILD PIPELINE")
    print("==================================================")
    master_all_tracks()
    total_sec = build_2hour_mix()
    render_2hour_video(total_sec)
    print("\n🎉 [4/4] 2-HOUR POMODORO VIDEO COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
