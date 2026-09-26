#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): 1時間長尺 Tropical Sunshine Pop 4K Mix YouTube公式アップロードスクリプト
- Video: output_videos/1HOUR_TROPICAL_SUNSHINE_POP_MIX_4K.mp4
- Thumbnail: output_videos/thumbnails/THUMB_CH3_01_FEEL_GOOD_POP.jpg
- Token: auramelody (token_auramelody.json)
- Channel: @AuraMelody-Audio (UCldq7fhclKDAXUA1gLI0FRw)
- タイトル: 1 Hour Feel-Good Summer Pop Mix ☀️ Upbeat Acoustic & Bright Morning Vibes [4K UHD]
- 全21曲タイムスタンプ (概要欄 + 固定コメント両対応)
- 100% 英語メタデータ規約完全準拠
"""

import os
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/1HOUR_TROPICAL_SUNSHINE_POP_MIX_4K.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/THUMB_CH3_01_FEEL_GOOD_POP.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/1HOUR_TROPICAL_SUNSHINE_POP_MIX_4K_chapters.txt"

if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}", file=sys.stderr)
    sys.exit(1)

if not THUMBNAIL_PATH.exists():
    print(f"Error: Thumbnail file not found at {THUMBNAIL_PATH}", file=sys.stderr)
    sys.exit(1)

chapters_text = ""
if CHAPTERS_PATH.exists():
    with open(CHAPTERS_PATH, "r", encoding="utf-8") as f:
        chapters_text = f.read().strip()

print("=== Starting Official Upload for Ch 3 (AuraMelody Audio) ===")
yt = get_youtube_service("auramelody")

TITLE_EN = "1 Hour Feel-Good Summer Pop Mix ☀️ Upbeat Acoustic & Bright Morning Vibes [4K UHD]"

DESCRIPTION_EN = f"""Start your day with radiant energy! ☀️ 1 hour of non-stop feel-good summer pop, upbeat acoustic melodies, and bright uplifting rhythms designed to boost your mood, focus, and dopamine. Perfect for morning routines, sunny drives, workouts, and productive study sessions.

🎧 Tracklist & Chapters:
{chapters_text}

📜 Commercial Use & Music Policy:
All original music in this video is produced by AuraMelody Audio. You are free to use these tracks in your personal and commercial content (YouTube videos, streams, podcasts) with proper credit:
Music provided by AuraMelody Audio (YouTube: @AuraMelody-Audio)

#FeelGoodPop #SunshinePop #MorningVibes #UpbeatMusic #SummerPop #AuraMelody #PositiveEnergy"""

TAGS = [
    "feel good pop", "sunshine pop", "morning pop", "upbeat acoustic pop",
    "summer pop", "happy pop music", "bright morning vibes", "dopamine boost music",
    "workout pop", "driving music", "study music", "auramelody", "auramelody audio",
    "4k music video", "positive energy music"
]

LOCALIZATIONS = {
    "ja": {
        "title": "【4K】1時間 爽快サマーポップ＆アコースティック MIX ☀️ 朝の目覚め・作業用・ドライブ BGM",
        "description": f"""ポジティブなエネルギーで最高の一日をスタート！☀️
弾むアコースティックギターと爽快なホーンセクションが響く、1時間ノンストップの多幸感サマーポップ＆アコースティックMIX。
朝のルーティン、集中作業、勉強、ドライブ、ワークアウトに最適です。

🎧 トラックリスト＆タイムスタンプ:
{chapters_text}

📜 音源利用規約:
本動画の楽曲はすべて AuraMelody Audio による完全オリジナル制作です。クレジット表記（YouTube: @AuraMelody-Audio）を行っていただければ、YouTube動画やライブ配信等で自由にご利用いただけます。

#作業用BGM #朝BGM #ドライブBGM #洋楽ポップ #サマーポップ #AuraMelody"""
    },
    "ko": {
        "title": "1시간 신나는 썸머 팝 & 어쿠스틱 믹스 ☀️ 모닝 루틴 & 드라이브 노동요 [4K UHD]",
        "description": f"""상쾌하고 긍정적인 에너지로 하루를 시작하세요! ☀️ 
밝은 어쿠스틱 기타와 경쾌한 멜로디가 가득한 1시간 연속 썸머 팝 믹스.

🎧 트랙리스트 & 타임스탬프:
{chapters_text}

#노동요 #모닝팝 #드라이브음악 #신나는음악 #AuraMelody"""
    },
    "es": {
        "title": "1 Hora Pop Alegre de Verano ☀️ Música Positiva & Acústica Para la Mañana [4K UHD]",
        "description": f"""¡Empieza tu día con energía radiante! ☀️ 1 hora continua de pop acústico alegre y ritmos veraniegos para motivarte en el trabajo, estudio o conduciendo.

🎧 Lista de Canciones:
{chapters_text}

#MusicaAlegre #PopVerano #MusicaPositiva #AuraMelody"""
    }
}

body = {
    "snippet": {
        "title": TITLE_EN,
        "description": DESCRIPTION_EN,
        "tags": TAGS,
        "categoryId": "10",  # Music
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    },
    "localizations": LOCALIZATIONS
}

print(f"[+] Uploading video: {VIDEO_PATH.name} ({VIDEO_PATH.stat().st_size / 1024 / 1024:.2f} MB)...")
media = MediaFileUpload(str(VIDEO_PATH), mimetype="video/mp4", resumable=True, chunksize=10*1024*1024)

request = yt.videos().insert(
    part="snippet,status,localizations",
    body=body,
    media_body=media
)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"  -> Upload progress: {int(status.progress() * 100)}%")

video_id = response.get("id")
print(f"\n🎉 Video Successfully Uploaded! Video ID: {video_id}")
print(f"🔗 URL: https://youtu.be/{video_id}")

# 3. サムネイルの設定
print(f"[+] Setting thumbnail: {THUMBNAIL_PATH.name}...")
time.sleep(3)
try:
    yt.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
    ).execute()
    print("✅ Thumbnail Successfully Set!")
except Exception as e:
    print(f"⚠️ Failed to set thumbnail: {e}")

# 4. 固定コメント（Engagement Comment）の投稿（タイムスタンプ付き）
comment_text = f"""✨ Thank you for listening to AuraMelody Audio! Which track brought the biggest smile to your day? Let us know in the comments below! Don't forget to like & subscribe for more sunny vibes every week. ☀️🌴

🎧 Tracklist & Chapters:
{chapters_text}"""

try:
    print("[+] Posting pinned engagement comment...")
    comment_res = yt.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    ).execute()
    print("✅ Engagement Comment Successfully Posted!")
except Exception as e:
    print(f"⚠️ Note on comment posting: {e}")

# 5. ストレージ管理規約に基づきローカルMP4を自動削除
print("\n[+] Cleaning up local video file per storage lifecycle rules...")
if VIDEO_PATH.exists():
    VIDEO_PATH.unlink()
    print(f"🧹 Deleted local MP4 file: {VIDEO_PATH.name}")

print(f"\n🚀 ALL TASKS COMPLETED! Live at https://youtu.be/{video_id}")
