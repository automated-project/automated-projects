#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio): 2時間超 Study With Me 完全シームレスLofi Mix YouTubeアップロードスクリプト
- Video: 01_Chill_Channel/output_videos/2HOUR_COZY_LOFI_STUDY_MIX.mp4 (02:02:44)
- Thumbnail: 01_Chill_Channel/output_videos/thumbnails/THUMBNAIL_01_STUDY_WITH_ME.jpg
- License: 100% FREE BGM / Royalty-Free (商用・配信利用フリー) アピール
- SEO: 多言語ローカライズ (JA, KO, ES, PT, RU) & 固定コメント自動投稿
"""

import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/2HOUR_COZY_LOFI_STUDY_MIX.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/THUMBNAIL_01_STUDY_WITH_ME.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/2HOUR_COZY_LOFI_STUDY_MIX_chapters.txt"

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

TITLE_EN = "[2 HOURS] Study With Me ☕ Cozy Lofi & Warm Piano Beats for Deep Focus, Work & Relaxing [FREE BGM]"

DESCRIPTION_EN = f"""☕ Welcome to a peaceful 2-hour cozy study session — soothing nostalgic lofi hip hop and warm felt piano melodies for deep focus, studying, working, reading, and stress relief.

✨ 100% FREE BGM & ROYALTY-FREE MUSIC ✨
All music in this video is completely free to use in your own YouTube videos, live streams, podcasts, and creative projects (monetization allowed)!

📝 How to credit in your description:
Music: Haven Chill Audio (https://youtube.com/@havenchillaudio)

🎵 Tracklist & Timestamps (2 Hours Seamless Flow):
{chapters_text}

🎧 Sound Design & Mastering:
- Warm Tape Acoustic EQ (-14.0 LUFS YouTube Standard)
- Seamless 2.5s DJ Equal-Power Crossfades (Zero Silence / Pure Focus)

🔔 Subscribe for daily cozy study sessions, warm lofi mixes, and relaxing music journeys!

#StudyWithMe #Lofi #CozyLofi #StudyMusic #FreeBGM #RoyaltyFreeMusic #DeepFocus #2HoursLofi #RelaxingBGM #LofiHipHop
"""

TAGS = [
    "study with me", "lofi", "chill lofi", "free bgm", "royalty free music",
    "study music", "deep focus", "2 hours lofi", "cozy lofi", "work music",
    "reading bgm", "relaxing beats", "lofi hip hop", "copyright free music",
    "sleep music", "piano lofi", "warm lofi"
]

LOCALIZATIONS = {
    "ja": {
        "title": "【作業用BGM・完全無料】2時間 Study With Me ☕ 集中できる極上Lofi & 温もりピアノ（商用・配信利用OK / Free BGM）",
        "description": f"☕ 勉強・仕事・読書・プログラミング・睡眠に最適な、2時間超ノンストップの極上Lofi & 温もりピアノ作業用BGMです。\n\n✨【完全無料・フリーBGM】✨\n本動画の音源はすべて商用利用・YouTube配信・動画制作の背景BGMとして完全無料でご利用いただけます（収益化動画もOK）！\n\n📝 クレジット表記例（動画概要欄等に記載）：\n音源提供: Haven Chill Audio (https://youtube.com/@havenchillaudio)\n\n🎵 トラックリスト / タイムスタンプ:\n{chapters_text}\n\n#作業用BGM #勉強用BGM #StudyWithMe #フリーBGM #Lofi #2時間耐久 #睡眠用BGM #チルBGM"
    },
    "ko": {
        "title": "☕ [2시간] 스터디 위드 미 — 깊은 집중과 공부를 위한 따뜻한 로파이 피아노 노동요 [무료 BGM]",
        "description": f"☕ 2시간 연속 재생 스터디 위드 미 로파이 & 감성 피아노 비트!\n\n✨ 100% 무료 음원 / 상업적 이용 가능 BGM ✨\n유튜브 영상 제작, 스트리밍, 과제 등에 무료로 사용하실 수 있습니다.\n\n🎵 트랙리스트:\n{chapters_text}\n\n#로파이 #스터디위드미 #무료BGM #공부할때듣는음악 #노동요 #2시간"
    },
    "es": {
        "title": "☕ [2 HORAS] Study With Me — Lofi Acogedor y Piano Cálido para Concentrarse y Estudiar [FREE BGM]",
        "description": f"☕ 2 horas de relajante música Lo-Fi y piano suave para estudiar, trabajar y descansar.\n\n✨ MÚSICA 100% LIBRE DE DERECHOS / FREE BGM ✨\n\n🎵 Lista de canciones:\n{chapters_text}\n\n#StudyWithMe #Lofi #MusicaParaEstudiar #FreeBGM #Relax"
    },
    "pt": {
        "title": "☕ [2 HORAS] Study With Me — Lofi Aconchegante e Piano para Foco e Estudo [Música Sem Copyright]",
        "description": f"☕ 2 horas de lofi nostálgico e piano relaxante para estudos, trabalho e foco profundo.\n\n✨ 100% MÚSICA GRATUITA E SEM COPYRIGHT ✨\n\n🎵 Tracklist:\n{chapters_text}\n\n#StudyWithMe #Lofi #MusicaParaEstudar #FreeBGM"
    },
    "ru": {
        "title": "☕ [2 ЧАСА] Study With Me — Уютный Лофай и Теплое Пианино для Учебы и Работы [Бесплатная Музыка]",
        "description": f"☕ 2 часа спокойного лофай-бита и нежного пианино для продуктивной учебы и глубокой концентрации.\n\n✨ 100% БЕСПЛАТНАЯ МУЗЫКА БЕЗ АВТОРСКИХ ПРАВ ✨\n\n🎵 Треклист:\n{chapters_text}\n\n#Лофай #МузыкаДляУчебы #StudyWithMe #Lofi"
    }
}

body = {
    "snippet": {
        "title": TITLE_EN,
        "description": DESCRIPTION_EN,
        "tags": TAGS,
        "categoryId": "10",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    },
    "localizations": LOCALIZATIONS
}

print("📤 Uploading video file...")
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
        print(f"   Uploading: {int(status.progress() * 100)}%")

video_id = response["id"]
video_url = f"https://youtu.be/{video_id}"
print(f"✅ Video Uploaded Successfully! Video ID: {video_id}")
print(f"🔗 Video URL: {video_url}")

# Set Thumbnail
print(f"🖼️ Setting custom thumbnail from {THUMBNAIL_PATH}...")
try:
    thumb_media = MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
    yt.thumbnails().set(videoId=video_id, media_body=thumb_media).execute()
    print("✅ Thumbnail set successfully!")
except Exception as e:
    print(f"⚠️ Thumbnail upload note: {e}")

# Post Pinned Comment
print("💬 Posting pinned comment...")
pinned_comment_text = f"""☕ Welcome to your cozy study session! How is your day going?
Drop a comment below with what you're working on today 📖✨

✨ 100% FREE BGM & ROYALTY-FREE ✨
Feel free to use all tracks in this video for your own YouTube videos, live streams, and content creation (monetization allowed)! Just credit: "Music by Haven Chill Audio".

🎵 Quick Timestamps:
00:00 - Fields of Amber Light
02:56 - A Quiet Corner Table
16:24 - After the Long Tide (Break 1)
36:12 - Glass Cathedral (Break 2)
55:28 - Rain Upon Copper (Break 3)
01:14:15 - Where The River Stops (Break 4)
01:33:59 - Where the Water Rests (Break 5)

Enjoy your stay and have a wonderful, productive session! 🌿"""

try:
    comment_res = yt.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": pinned_comment_text
                    }
                }
            }
        }
    ).execute()
    print("✅ Pinned comment posted successfully!")
except Exception as e:
    print(f"⚠️ Comment note: {e}")

print("\n" + "="*60)
print("🎉 ALL DONE! YouTube Video is Live:")
print(f"   URL: {video_url}")
print(f"   Title: {TITLE_EN}")
print(f"   License: 100% FREE BGM / Commercial Monetization OK")
print("==================================================")
