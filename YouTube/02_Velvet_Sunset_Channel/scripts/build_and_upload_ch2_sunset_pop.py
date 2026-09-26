#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (Velvet Sunset Audio) 初回長尺動画 自動ビルド ＆ YouTube非公開投稿スクリプト
- 音源: 02_Velvet_Sunset_Channel/raw_audio/ch2_drive_mp3
- サムネイル: 02_Velvet_Sunset_Channel/cover_art/thumb_03_golden_hour.jpg
- ルール: Zero-EQ, 2.5s DJ Crossfade, 4K, SignPainter 260px Glow, Non-Public Upload
"""

import os
import sys
import glob
import json
import shutil
import subprocess
from pathlib import Path

YOUTUBE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(YOUTUBE_ROOT))

from shared.scripts.account_token_manager import get_youtube_service
from googleapiclient.http import MediaFileUpload

CHANNEL_DIR = YOUTUBE_ROOT / "02_Velvet_Sunset_Channel"
RAW_AUDIO_DIR = CHANNEL_DIR / "raw_audio" / "ch2_drive_mp3"
THUMBNAIL_SRC = CHANNEL_DIR / "cover_art" / "thumb_03_golden_hour.jpg"
OUTPUT_DIR = CHANNEL_DIR / "output_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_AUDIO_PATH = OUTPUT_DIR / "ch2_sunset_pop_master_audio.wav"
FINAL_VIDEO_PATH = OUTPUT_DIR / "ch2_sunset_pop_4k_master.mp4"
FINAL_THUMB_PATH = OUTPUT_DIR / "ch2_sunset_pop_thumbnail.jpg"

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def main():
    print("=== [1/5] 音源ファイル一覧の確認 ===")
    audio_files = sorted(glob.glob(str(RAW_AUDIO_DIR / "*.mp3")))
    if not audio_files:
        raise FileNotFoundError(f"音源が見つかりません: {RAW_AUDIO_DIR}")
    print(f"✅ 取得音源数: {len(audio_files)} 曲")

    tracks = []
    timestamps = []
    current_sec = 0.0
    crossfade_sec = 2.5

    for idx, f in enumerate(audio_files):
        t_name = Path(f).stem
        dur = get_audio_duration(f)

        mins = int(current_sec // 60)
        secs = int(current_sec % 60)
        timestamps.append(f"{mins:02d}:{secs:02d} - {t_name}")

        tracks.append({"path": f, "title": t_name, "duration": dur})
        if idx == 0:
            current_sec += dur
        else:
            current_sec += (dur - crossfade_sec)

    print("=== [2/5] 2.5秒 DJクロスフェード & Zero-EQ マスタリング (FFmpeg Direct) ===")
    # FFmpeg concat filter 構築
    filter_inputs = ""
    for idx in range(len(tracks)):
        filter_inputs += f"[{idx}:a]"

    filter_complex = ""
    if len(tracks) == 1:
        filter_complex = "[0:a]afade=t=out:st=" + str(tracks[0]['duration'] - 3.0) + ":d=3[aout]"
    else:
        # acrossfade 接続
        curr_label = "0:a"
        for i in range(1, len(tracks)):
            next_label = f"{i}:a"
            out_label = f"a{i}" if i < len(tracks) - 1 else "afin"
            filter_complex += f"[{curr_label}][{next_label}]acrossfade=d=2.5:c1=tri:c2=tri[{out_label}];"
            curr_label = out_label

        total_duration = current_sec
        fade_start = max(0, total_duration - 3.0)
        filter_complex += f"[afin]afade=t=out:st={fade_start:.2f}:d=3,alimiter=limit=0.95:level=disabled[aout]"

    cmd_ffmpeg_audio = ["ffmpeg", "-y"]
    for trk in tracks:
        cmd_ffmpeg_audio.extend(["-i", trk["path"]])

    cmd_ffmpeg_audio.extend([
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-ar", "44100", "-c:a", "pcm_s16le",
        str(FINAL_AUDIO_PATH)
    ])

    print("FFmpeg 音響合成処理を実行中...")
    subprocess.run(cmd_ffmpeg_audio, check=True)
    print(f"✅ 音声マスター出力完了: {FINAL_AUDIO_PATH}")

    print("=== [3/5] サムネイル確認 ===")
    if not THUMBNAIL_SRC.exists():
        raise FileNotFoundError(f"サムネイル画像が見つかりません: {THUMBNAIL_SRC}")
    shutil.copy(THUMBNAIL_SRC, FINAL_THUMB_PATH)
    print(f"✅ サムネイル準備完了: {FINAL_THUMB_PATH}")

    print("=== [4/5] 4K H.264 ビデオレンダリング ===")
    cmd_video = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(FINAL_THUMB_PATH),
        "-i", str(FINAL_AUDIO_PATH),
        "-c:v", "h264_videotoolbox", "-b:v", "9500k",
        "-vf", "scale=3840:2160:flags=lanczos,format=yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-shortest",
        str(FINAL_VIDEO_PATH)
    ]
    print("4K動画をエンコード中 (h264_videotoolbox)...")
    subprocess.run(cmd_video, check=True)
    print(f"✅ 動画レンダリング完了: {FINAL_VIDEO_PATH}")

    print("=== [5/5] YouTube Data API 自動非公開（private）投稿 ===")
    video_title = "Sunset Pop & Modern R&B Chill Grooves 🌅 Velvet Sunset Audio"
    time_stamp_str = "\n".join(timestamps)

    description = f"""Smooth Sunset Pop & Modern R&B Selection for Driving, Evening Chill, and Sunset Lounging.

🎵 TRACKLIST:
{time_stamp_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【CREATOR LICENSE & USAGE】
You can freely use this track in your YouTube videos, Twitch streams, TikToks & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
✅ Commercial & Non-Commercial Use Free
📋 Required Attribution (Copy & Paste):
   Music: Velvet Sunset Audio
   Watch: https://youtu.be/VelvetSunset
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    tags = ["sunset pop", "modern r&b", "neo soul", "pop r&b", "sunset groove", "evening chill", "velvet sunset audio", "smooth r&b", "driving pop"]

    yt = get_youtube_service("phonkforge")

    body = {
        'snippet': {
            'title': video_title,
            'description': description,
            'tags': tags,
            'categoryId': '10',
            'defaultLanguage': 'en',
            'defaultAudioLanguage': 'en'
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(str(FINAL_VIDEO_PATH), chunksize=-1, resumable=True, mimetype='video/mp4')
    request = yt.videos().insert(part=','.join(body.keys()), body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f" Uploading progress: {int(status.progress() * 100)}%", flush=True)

    video_id = response['id']
    print(f"🎉 YouTubeアップロード成功! Video ID: {video_id}")
    print(f"URL: https://youtu.be/{video_id}")

    print("🖼️ サムネイル画像をアップロード中...")
    yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(FINAL_THUMB_PATH))).execute()
    print("✅ サムネイル設定完了！")

if __name__ == "__main__":
    main()
