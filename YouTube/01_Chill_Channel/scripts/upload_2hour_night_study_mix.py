#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio): 2時間夜間Study With Me 4K動画 YouTubeアップロードスクリプト
- 厳格ルール遵守:
  1. タイトルに「商用利用OK / FREE BGM / 耐久」等を含めない（世界観維持）
  2. メタデータからマスタリング等（-14 LUFS / Warm Tape等）の内部技術仕様を完全排除
  3. 時間帯・情景・具体的用途（3 AM, Midnight, Deep Focus, Study With Me, Sleep）を明記
  4. タイムスタンプを概要欄＆固定コメントの両方に完全自動記載
  5. アップロード完了後にローカル動画ファイル（8.3GB）を自動削除
"""

import os
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/2HOUR_MIDNIGHT_STUDY_WITH_ME_LOFI_4K.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/THUMB_01_3AM_STUDY_WITH_ME.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/2HOUR_MIDNIGHT_STUDY_WITH_ME_LOFI_4K_chapters.txt"

if not VIDEO_PATH.exists():
    print(f"❌ Error: Video not found at {VIDEO_PATH}", file=sys.stderr)
    sys.exit(1)

if not THUMBNAIL_PATH.exists():
    print(f"❌ Error: Thumbnail not found at {THUMBNAIL_PATH}", file=sys.stderr)
    sys.exit(1)

chapters_text = ""
if CHAPTERS_PATH.exists():
    with open(CHAPTERS_PATH, "r", encoding="utf-8") as f:
        chapters_text = f.read().strip()

print("==================================================")
print("🚀 Starting YouTube Upload for Ch 1 (Haven Chill Audio)")
print(f"📹 Video: {VIDEO_PATH.name}")
print(f"🖼️ Thumbnail: {THUMBNAIL_PATH.name}")
print("==================================================")

yt = get_youtube_service("chill")

TITLE_EN = "3 AM Study with Me 🌙 2 Hours Cozy Midnight Lofi & Felt Piano for Deep Focus / Sleep [4K]"

DESCRIPTION_EN = f"""🌙 Welcome to a peaceful 2-hour midnight study session. Gentle nostalgic lofi beats and warm felt piano melodies inside a quiet cozy room at 3 AM — crafted for late night study, deep focus, coding, reading, and deep sleep.

🎵 Tracklist & Timestamps:
{chapters_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【FREE DOWNLOAD & CREATOR LICENSE / フリー音源利用規約】
You can freely use this music in your YouTube videos, Twitch streams, TikToks & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
✅ Commercial & Non-Commercial Use Free
📋 Required Attribution (Copy & Paste):
   Music: Haven Chill Audio (@Haven-Chill-Audio)
   Watch: https://youtube.com/@haven-chill-audio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe to Haven Chill Audio for daily cozy study sessions, nostalgic lofi mixes, and relaxing midnight atmospheres.

#StudyWithMe #Lofi #CozyLofi #MidnightLofi #DeepFocus #SleepMusic #LateNightStudy #FeltPiano #LofiHipHop #RelaxingMusic
"""

TAGS = [
    "study with me", "lofi", "midnight lofi", "cozy lofi", "study music",
    "deep focus", "sleep music", "2 hours lofi", "felt piano", "late night study",
    "lofi hip hop", "relaxing music", "reading music", "coding music",
    "haven chill", "haven chill audio"
]

LOCALIZATIONS = {
    "ja": {
        "title": "深夜3時のStudy with Me 🌙 2時間 静寂のノスタルジックLofi＆温もりフェルトピアノ（作業用・勉強用・睡眠用BGM） [4K]",
        "description": f"🌙 静まり返った真夜中の部屋で過ごす、2時間のStudy with Me。温かいデスクライトと穏やかなフェルトピアノの音色に包まれる、勉強・仕事・読書・睡眠のための極上作業用BGMです。\n\n🎵 トラックリスト / タイムスタンプ:\n{chapters_text}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🎁 【フリー音源利用規約 / Creator License】\n本動画の音源はすべて商用利用・YouTube配信・動画制作の背景BGMとして完全無料でご利用いただけます（収益化動画もOK）。\n\n📋 クレジット表記例（動画概要欄等に記載）：\n音源提供: Haven Chill Audio (@Haven-Chill-Audio)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n#作業用BGM #勉強用BGM #StudyWithMe #睡眠用BGM #Lofi #深夜作業 #フェルトピアノ #チルBGM"
    },
    "ko": {
        "title": "새벽 3시 스터디 위드 미 🌙 2시간 밤샘 공부와 깊은 수면을 위한 따뜻한 로파이 피아노 노동요 [4K]",
        "description": f"🌙 조용한 한밤중의 방에서 함께하는 2시간 스터디 위드 미. 공부, 코딩, 독서 및 편안한 수면을 위한 로파이 & 감성 피아노 음악입니다.\n\n🎵 트랙리스트:\n{chapters_text}\n\n#로파이 #스터디위드미 #공부할때듣는음악 #수면음악 #노동요 #2시간"
    },
    "es": {
        "title": "3 AM Study with Me 🌙 2 Horas de Lofi Nocturno y Piano Cálido para Concentrarse y Dormir [4K]",
        "description": f"🌙 Una tranquila sesión de estudio de 2 horas a medianoche. Música lofi relajante y piano suave para estudiar, leer y dormir profundamente.\n\n🎵 Lista de canciones:\n{chapters_text}\n\n#StudyWithMe #Lofi #MusicaParaEstudiar #Dormir #Relax"
    },
    "pt": {
        "title": "3 AM Study with Me 🌙 2 Horas de Lofi Noturno e Piano Suave para Foco Profundo e Dormir [4K]",
        "description": f"🌙 Uma sessão aconchegante de 2 horas para estudos na madrugada. Lofi relaxante e piano acústico para foco, leitura e sono profundo.\n\n🎵 Tracklist:\n{chapters_text}\n\n#StudyWithMe #Lofi #MusicaParaEstudar #Dormir #Foco"
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

print("\n▶ Uploading video to YouTube (Public)...")
media = MediaFileUpload(
    str(VIDEO_PATH),
    mimetype="video/mp4",
    chunksize=10 * 1024 * 1024,
    resumable=True
)

request = yt.videos().insert(
    part="snippet,status,localizations",
    body=body,
    media_body=media
)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"  Uploaded: {int(status.progress() * 100)}%", flush=True)

video_id = response.get("id")
print(f"\n🎉 Video uploaded successfully! Video ID: {video_id}")
print(f"🔗 Video URL: https://youtu.be/{video_id}")
print(f"🔗 Studio URL: https://studio.youtube.com/video/{video_id}/edit")

# Set Custom Thumbnail
print("\n▶ Setting Custom Thumbnail...")
try:
    yt.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
    ).execute()
    print("✅ Custom thumbnail uploaded successfully!")
except Exception as e:
    print(f"⚠️ Warning: Could not set thumbnail automatically: {e}")

# Post Top Pinned Comment with Timestamps
print("\n▶ Posting Pinned Comment with Timestamps...")
comment_text = f"""🌙 Welcome to your 3 AM study session! Which track brought you the most peace tonight? Let us know in the comments. ☕✨

🎵 Quick Timestamps:
{chapters_text}
"""

try:
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
    comment_id = comment_res.get("id")
    print(f"✅ Comment posted successfully! (ID: {comment_id})")
except Exception as e:
    print(f"⚠️ Warning: Could not post comment: {e}")

# Delete local video file to save storage
print(f"\n🧹 Cleaning up local video file: {VIDEO_PATH.name}...")
try:
    if VIDEO_PATH.exists():
        VIDEO_PATH.unlink()
        print(f"✅ Successfully deleted {VIDEO_PATH.name} to free up disk space.")
except Exception as e:
    print(f"⚠️ Warning: Could not delete local video file: {e}")

print("\n==================================================")
print("🎊 UPLOAD AND CLEANUP COMPLETE!")
print(f"👉 Watch: https://youtu.be/{video_id}")
print(f"👉 Studio A/B Test Setup: https://studio.youtube.com/video/{video_id}/edit")
print("==================================================")
