# -*- coding: utf-8 -*-
"""
第3チャンネル（AuraMelody Audio）集客用Shorts動画 アップロード＆メタデータ投入スクリプト
- Video: output_videos/SHORTS_SUMMER_MELODIC_EDM_LOOP_15S.mp4
- Token: auramelody (token_auramelody.json)
- SEO & Multilingual localizations & Pinned Comment
"""
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/SHORTS_SUMMER_MELODIC_EDM_LOOP_15S.mp4"

if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}", file=sys.stderr)
    sys.exit(1)

print(f"=== Starting Upload for Shorts: {VIDEO_PATH.name} on AuraMelody Audio ===")
yt = get_youtube_service("auramelody")

TITLE_EN = "✨ SUMMER MELODIC EDM (15s Seamless Loop) #Shorts #MelodicEDM #SummerVibes"

DESCRIPTION_EN = """✨ 15s Seamless Loop - Golden Hour Summer Melodic EDM & Progressive House (Avicii / Kygo Style).
🎧 Full 1-Hour Mix available in Related Video!

🔥 Subscribe to @AuraMelodyAudio for daily non-stop uplifting summer mixes!

#Shorts #MelodicEDM #SummerVibes #ProgressiveHouse #EDM #ChillHouse #AuraMelody #FestivalVibes
"""

TAGS = [
    "shorts", "melodic edm", "summer edm", "progressive house", "avicii style", 
    "kygo style", "summer vibes", "edm loop", "golden hour", "auramelody", 
    "festival music", "uplifting edm", "chill house"
]

LOCALIZATIONS = {
    "ru": {
        "title": "✨ ЛЕТНИЙ МЕЛОДИЧНЫЙ EDM (15с Луп) #Shorts #EDM #Лето",
        "description": "✨ 15-секундный бесшовный луп солнечного Melodic EDM и Progressive House! Полный 1-часовой микс доступен в связанных видео.\n\n#Shorts #МелодикEDM #Лето #EDM"
    },
    "pt": {
        "title": "✨ SUMMER MELODIC EDM (15s Loop) #Shorts #MelodicEDM #Vibes",
        "description": "✨ Loop perfeito de 15s de Summer Melodic EDM e Progressive House! Mix completo de 1 hora no vídeo relacionado.\n\n#Shorts #MelodicEDM #Verao #EDM"
    },
    "es": {
        "title": "✨ SUMMER MELODIC EDM (15s Loop) #Shorts #MelodicEDM #Verano",
        "description": "✨ ¡Loop sin fin de 15s de Summer Melodic EDM y Progressive House! Mix completo de 1 hora en el video relacionado.\n\n#Shorts #MelodicEDM #Verano #EDM"
    },
    "ko": {
        "title": "✨ 썸머 멜로딕 EDM (15초 무한루프) #Shorts #멜로딕EDM #여름노래",
        "description": "✨ 15초 무한 루프 썸머 멜로딕 EDM & 프로그레시브 하우스! 1시간 풀버전은 관련 동영상 링크에서 감상하세요.\n\n#Shorts #멜로딕EDM #감성EDM #노동요 #여름노래"
    },
    "ja": {
        "title": "✨ 爽快サマーMelodic EDM（15秒シームレス無限ループ）#Shorts #MelodicEDM #作業用BGM",
        "description": "✨ 15秒シームレス無限ループ！爽快エモーショナルSummer Melodic EDM & Progressive House。\n🎧 1時間フル公式Mixは関連動画リンクから視聴できます！\n\n#Shorts #メロディックEDM #サマーEDM #作業用BGM #洋楽EDM"
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

media = MediaFileUpload(str(VIDEO_PATH), chunksize=-1, resumable=True, mimetype="video/mp4")
request = yt.videos().insert(
    part="snippet,status,localizations",
    body=body,
    media_body=media
)

print("[+] Uploading Shorts video...")
response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"    Progress: {int(status.progress() * 100)}%")

video_id = response.get("id")
print("==================================================")
print(f"✅ Shorts Upload Successful!")
print(f"   Video ID: {video_id}")
print(f"   Shorts URL: https://www.youtube.com/shorts/{video_id}")
print(f"   Standard URL: https://youtu.be/{video_id}")
print("==================================================")

# Post Pinned Engagement Comment
print("\n[+] Posting Pinned Engagement Comment...")
time.sleep(2)
comment_text = """✨ What feeling did this summer melody give you? Drop your favorite vibes below! ⬇️

🔥 Full 1-Hour Long Mix is available in the Related Video link!"""

try:
    c_res = yt.commentThreads().insert(
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
    print(f"✅ Engagement Comment posted successfully! (ID: {c_res['id']})")
except Exception as e:
    print(f"⚠️ Note on comment posting: {e}")
