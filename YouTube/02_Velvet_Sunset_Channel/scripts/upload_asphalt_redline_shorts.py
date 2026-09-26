#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
第2チャンネル（PhonkForge Audio）集客用Shorts動画 アップロード＆メタデータ投入スクリプト
- Video: output_videos/SHORTS_ASPHALT_REDLINE_DROP_20S.mp4
- Track: Asphalt Redline (Peak Drop Hook 19.5s)
- Token: phonkforge (token_phonkforge.json)
"""

import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/SHORTS_ASPHALT_REDLINE_DROP_20S.mp4"

if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}", file=sys.stderr)
    sys.exit(1)

print(f"=== Starting Upload for Shorts: {VIDEO_PATH.name} on PhonkForge Audio ===")
yt = get_youtube_service("phonkforge")

TITLE_EN = "⚡ ASPHALT REDLINE — Extreme Gym Phonk Drop #Shorts #GymPhonk #DriftPhonk"

DESCRIPTION_EN = """⚡ 20s High-Octane Gym Phonk & Drift EDM Drop — "Asphalt Redline"
🎧 Full 1-Hour Aggressive Workout Mix available in Related Video!

🔥 Subscribe to @PhonkForgeAudio for daily non-stop adrenaline workout mixes!

#Shorts #GymPhonk #DriftPhonk #AggressivePhonk #WorkoutMusic #Phonk #Hardstyle #GymMotivation
"""

TAGS = [
    "shorts", "gym phonk", "drift phonk", "asphalt redline", "aggressive phonk", 
    "phonk drop", "workout motivation", "gym edm", "hardstyle phonk", "phonkforge", 
    "bass boosted", "beast mode"
]

LOCALIZATIONS = {
    "ru": {
        "title": "⚡ ASPHALT REDLINE — Мощный Дрифт Фонк Дроп #Shorts #Фонк #GymPhonk",
        "description": "⚡ Взрывной 20-секундный дроп для тренировок и ночного дрифта! Полный 1-часовой микс доступен в связанных видео.\n\n#Shorts #Фонк #GymPhonk #DriftPhonk"
    },
    "pt": {
        "title": "⚡ ASPHALT REDLINE — Drop Insano de Gym Phonk #Shorts #Phonk",
        "description": "⚡ 20s do drop mais pesado de Gym Phonk para treino pesado! Mix completo de 1 hora no vídeo relacionado.\n\n#Shorts #GymPhonk #DriftPhonk #Treino #Phonk"
    },
    "es": {
        "title": "⚡ ASPHALT REDLINE — Drop Extremo de Gym Phonk #Shorts #Phonk",
        "description": "⚡ ¡20 segundos de pura adrenalina y bajo pesado para entrenar! Mix completo de 1 hora en el video relacionado.\n\n#Shorts #GymPhonk #DriftPhonk #Entrenamiento #Phonk"
    },
    "ko": {
        "title": "⚡ 아스팔트 레드라인 — 극강 헬스 폰크 드롭 #Shorts #헬스음악 #짐폰크",
        "description": "⚡ 20초 극강의 중저음 헬스 폰크 & 드리프트 드롭! 1시간 풀버전 운동 믹스는 관련 동영상 링크에서 감상하세요.\n\n#Shorts #짐폰크 #헬스음악 #운동BGM #동기부여"
    },
    "ja": {
        "title": "⚡ ASPHALT REDLINE — 脳汁爆発Gym Phonkサビ #Shorts #筋トレBGM #Phonk",
        "description": "⚡ 脳汁が吹き飛ぶ20秒極限重低音サビ！ワークアウト＆深夜ドライブ特化。\n🎧 1時間フル公式Mixは関連動画リンクから視聴できます！\n\n#Shorts #GymPhonk #DriftPhonk #筋トレBGM #重低音"
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
comment_text = """⚡ How many reps did this drop add to your set? Drop your workout PRs below! 🏋️‍♂️⬇️

🔥 Full 1-Hour Aggressive Mix is available in the Related Video link!"""

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
