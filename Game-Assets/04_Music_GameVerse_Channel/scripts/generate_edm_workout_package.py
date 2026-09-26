#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create_workout_edm_package.py
-------------------------------------------------------------------------------
20分 Workout Gym EDM & Phonk BGM 超軽量・高品質ロング動画 & ショート動画生成スクリプト
【昨日の決定仕様に完全準拠】
1. レイアウト: 候補2（ソフト・アンビエントブラー）
   - 背景: 各曲の元画像を1920x1080にリサイズ + GaussianBlur(50) + 80%暗黒オーバーレイ
   - 中央: 元画像（1080x1080）をアスペクト比維持のまま配置
2. テロップ・文字: 一切なし（絵そのものの世界観を100%活かしたシンプルな仕上がり）
3. 映像方式: 「各曲の高品質音声 + 静止画1枚（15fps, h264_videotoolbox）」で極小サイズ・爆速化
4. 結合方式: ffmpeg concat による無劣化・超高速結合
5. 音楽フェード: 冒頭1.5sフェードイン、末尾1.5sフェードアウトでシームレス接続
6. 1曲目 & サムネイル: Crush_The_Bone
-------------------------------------------------------------------------------
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from PIL import Image, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube")
EDM_DIR = BASE_DIR / "edm-bgm"
OUTPUT_DIR = BASE_DIR / "output_edm"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

TEMP_BUILD_DIR = OUTPUT_DIR / "temp_workout_build"
TEMP_BUILD_DIR.mkdir(exist_ok=True, parents=True)

FINAL_LONG_MP4 = OUTPUT_DIR / "workout_edm_longform_20min.mp4"
CHAPTERS_FILE = OUTPUT_DIR / "workout_edm_chapters.txt"
THUMBNAIL_FILE = OUTPUT_DIR / "workout_edm_thumbnail.jpg"

# 1曲目は必ず Crush_The_Bone
TRACKS = [
    {"file": EDM_DIR / "Crush_The_Bone.mp4", "title": "Crush The Bone", "genre": "Aggressive Gym Phonk / Hardstyle"},
    {"file": EDM_DIR / "The_Iron_Ascent.mp4", "title": "The Iron Ascent", "genre": "Heavy Power Hardstyle"},
    {"file": EDM_DIR / "Midnight_Asphalt_Burn.mp4", "title": "Midnight Asphalt Burn", "genre": "Brazilian Drift Phonk"},
    {"file": EDM_DIR / "Asphalt_Redline.mp4", "title": "Asphalt Redline", "genre": "High-Octane Speed Phonk"},
    {"file": EDM_DIR / "Asphalt_Teeth.mp4", "title": "Asphalt Teeth", "genre": "Dark Metal Phonk"},
    {"file": EDM_DIR / "Kingdom_Of_My_Own.mp4", "title": "Kingdom Of My Own", "genre": "Epic Power Synth EDM"},
    {"file": EDM_DIR / "Midnight_Redline.mp4", "title": "Midnight Redline", "genre": "Phonk Hardstyle"}
]

def format_seconds(sec: float) -> str:
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m}:{s:02d}"

def get_media_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def extract_raw_art(mp4_path: Path, out_path: Path):
    cmd = ["ffmpeg", "-y", "-ss", "00:00:02", "-i", str(mp4_path), "-frames:v", "1", str(out_path)]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_long_ambient_frame(art_path: Path, out_path: Path):
    """
    【決定仕様 レイアウト候補2: ソフト・アンビエントブラー】
    - 背景: 元画像を1920x1080にリサイズ + GaussianBlur(50) + 80%暗黒オーバーレイ
    - 中央: 元画像（1080x1080）をアスペクト比維持のまま配置
    - テロップ・文字: 一切なし
    """
    orig = Image.open(art_path).convert("RGBA")
    
    # 1. 背景作成
    bg = orig.resize((1920, 1080), Image.Resampling.BICUBIC)
    bg = bg.filter(ImageFilter.GaussianBlur(50))
    dark_overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, int(255 * 0.80)))
    bg = Image.alpha_composite(bg, dark_overlay)
    
    # 2. 中央配置 (1080x1080)
    center_img = orig.resize((1080, 1080), Image.Resampling.LANCZOS)
    x_pos = (1920 - 1080) // 2
    bg.paste(center_img, (x_pos, 0), center_img)
    
    bg.convert("RGB").save(out_path, quality=95)

def generate_short_ambient_frame(art_path: Path, out_path: Path):
    """
    ショート動画用（9:16 / 1080x1920）アンビエントブラーフレーム
    - 背景: 1080x1920にリサイズ + GaussianBlur(50) + 75%暗黒オーバーレイ
    - 中央: 元画像（1080x1080）を配置
    - テロップ・文字: 一切なし（シンプル＆アートワークの世界観重視）
    """
    orig = Image.open(art_path).convert("RGBA")
    
    bg = orig.resize((1080, 1920), Image.Resampling.BICUBIC)
    bg = bg.filter(ImageFilter.GaussianBlur(50))
    dark_overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, int(255 * 0.75)))
    bg = Image.alpha_composite(bg, dark_overlay)
    
    center_img = orig.resize((1080, 1080), Image.Resampling.LANCZOS)
    y_pos = (1920 - 1080) // 2
    bg.paste(center_img, (0, y_pos), center_img)
    
    bg.convert("RGB").save(out_path, quality=95)

def build_long_clip(idx: int, t_info: dict, out_clip: Path) -> float:
    src_mp4 = t_info["file"]
    art_jpg = TEMP_BUILD_DIR / f"raw_art_{idx:02d}.jpg"
    extract_raw_art(src_mp4, art_jpg)
    
    still_jpg = TEMP_BUILD_DIR / f"long_frame_{idx:02d}.jpg"
    generate_long_ambient_frame(art_jpg, still_jpg)
    
    dur = get_media_duration(src_mp4)
    
    # 決定仕様: 15fps, h264_videotoolbox (超低ビットレート・爆速), 音声フェードイン・フェードアウト
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", "15", "-i", str(still_jpg),
        "-i", str(src_mp4),
        "-filter_complex",
        f"[1:a]afade=t=in:ss=0:d=1.5,afade=t=out:st={dur - 1.5:.2f}:d=1.5[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "h264_videotoolbox", "-b:v", "500k", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.2f}",
        str(out_clip)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if art_jpg.exists(): art_jpg.unlink()
    if still_jpg.exists(): still_jpg.unlink()
    return dur

def build_short_clip(idx: int, t_info: dict, out_clip: Path):
    src_mp4 = t_info["file"]
    art_jpg = TEMP_BUILD_DIR / f"short_art_{idx:02d}.jpg"
    extract_raw_art(src_mp4, art_jpg)
    
    still_jpg = TEMP_BUILD_DIR / f"short_frame_{idx:02d}.jpg"
    generate_short_ambient_frame(art_jpg, still_jpg)
    
    # 45秒のShorts切り出し (冒頭10秒〜55秒の最も熱いパート)
    cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:10",
        "-loop", "1", "-framerate", "15", "-i", str(still_jpg),
        "-ss", "00:00:10",
        "-i", str(src_mp4),
        "-filter_complex",
        "[1:a]afade=t=in:ss=0:d=1.0,afade=t=out:st=43.5:d=1.5[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "h264_videotoolbox", "-b:v", "800k", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "45.0",
        str(out_clip)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if art_jpg.exists(): art_jpg.unlink()
    if still_jpg.exists(): still_jpg.unlink()

def main():
    start_time = time.time()
    print("==================================================", flush=True)
    print("🔥 20分 Workout Gym EDM & Phonk (決定仕様完全準拠)", flush=True)
    print("   ・レイアウト: 候補2（ソフト・アンビエントブラー）", flush=True)
    print("   ・テロップ: 一切なし（シンプル＆アートワーク重視）", flush=True)
    print("   ・方式: 音声 + 静止画1枚（15fps, h264_videotoolbox）", flush=True)
    print("   ・結合方式: ffmpeg concat 無劣化超高速結合", flush=True)
    print("   ・1曲目: Crush The Bone", flush=True)
    print("==================================================", flush=True)

    # 1. サムネイル作成 (Crush_The_Bone ベースのアンビエントフレーム)
    print("\n📸 サムネイル生成中 (Crush The Bone)...", flush=True)
    crush_art = TEMP_BUILD_DIR / "crush_thumb_art.jpg"
    extract_raw_art(TRACKS[0]["file"], crush_art)
    generate_long_ambient_frame(crush_art, THUMBNAIL_FILE)
    if crush_art.exists(): crush_art.unlink()
    print(f"✅ サムネイル作成完了: {THUMBNAIL_FILE}", flush=True)

    # 2. ショート動画7本生成
    print("\n📱 7曲のShorts動画生成開始 (9:16 / 45s)...", flush=True)
    for idx, track in enumerate(TRACKS, 1):
        stem = track["file"].stem
        out_short = OUTPUT_DIR / f"short_{idx:02d}_{stem}.mp4"
        build_short_clip(idx, track, out_short)
        print(f"  [{idx}/7] ✅ Shorts完了: {out_short.name}", flush=True)

    # 3. 長尺クリップ7本生成
    print("\n🎬 20分長尺クリップ生成開始 (16:9)...", flush=True)
    current_sec = 0.0
    chapter_lines = []
    concat_lines = []

    for idx, track in enumerate(TRACKS, 1):
        clip_path = TEMP_BUILD_DIR / f"clip_{idx:02d}.mp4"
        time_str = format_seconds(current_sec)
        ch_line = f"{time_str} {idx:02d}. {track['title']} ({track['genre']})"
        chapter_lines.append(ch_line)

        dur = build_long_clip(idx, track, clip_path)
        concat_lines.append(f"file '{clip_path.resolve()}'")
        current_sec += dur
        print(f"  [{idx}/7] ✅ パート完了: {track['title']} ({dur:.1f}s)", flush=True)

    total_time_str = format_seconds(current_sec)
    print(f"\n✨ 全7曲クリップ生成完了！ 総再生時間: {total_time_str} ({current_sec/60:.1f}分)", flush=True)

    # 4. チャプター目次保存
    chapters_content = f"""[20 MIN] Heavy Gym Workout EDM & Phonk Mix | Beast Mode Motivation

⚡ TRACKLIST & TIMESTAMPS:
""" + "\n".join(chapter_lines) + f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏋️‍♂️ WORKOUT MOTIVATION & GYM FOCUS:
An intense 20-minute compilation of aggressive gym phonk, crushing hardstyle, and relentless basslines designed for heavy deadlifts, bench press, and savage PR sets.

All tracks produced by GameVerse Audio.
100% Royalty-Free for your YouTube fitness edits, Twitch streams, and game projects!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#WorkoutMusic #GymPhonk #GymEDM #Hardstyle #BeastMode #WorkoutMotivation #GameVerseAudio
"""
    CHAPTERS_FILE.write_text(chapters_content, encoding="utf-8")

    # 5. concat 無劣化超高速結合
    concat_list_file = TEMP_BUILD_DIR / "concat_list.txt"
    concat_list_file.write_text("\n".join(concat_lines), encoding="utf-8")

    print(f"\n🔗 全7曲を無劣化結合中...", flush=True)
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(FINAL_LONG_MP4)
    ]
    subprocess.run(concat_cmd, check=True)

    # クリーンアップ
    for p in TEMP_BUILD_DIR.glob("*.mp4"):
        p.unlink()
    if concat_list_file.exists():
        concat_list_file.unlink()

    elapsed = time.time() - start_time
    print("\n==================================================", flush=True)
    print(f"🎉 すべての生成処理が完了しました！(所要時間: {elapsed:.1f}秒)", flush=True)
    print(f"長尺動画: {FINAL_LONG_MP4} ({total_time_str})", flush=True)
    print(f"サムネイル: {THUMBNAIL_FILE}", flush=True)
    print("==================================================", flush=True)

if __name__ == "__main__":
    main()
