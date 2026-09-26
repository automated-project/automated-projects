# -*- coding: utf-8 -*-
"""
第2チャンネル（PhonkForge Audio）集客用Shorts動画 アップロード＆メタデータ投入スクリプト
- Video: output_videos/SHORTS_AGGRESSIVE_DRIFT_LOOP_16S.mp4
- Token: phonkforge (token_phonkforge.json)
- SEO & Multilingual localizations & Pinned Comment
"""
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/SHORTS_AGGRESSIVE_DRIFT_LOOP_16S.mp4"

if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}", file=sys.stderr)
    sys.exit(1)

print(f"=== Starting Upload for Shorts: {VIDEO_PATH.name} on PhonkForge Audio ===")
yt = get_youtube_service("phonkforge")

TITLE_EN = "⚡ AGGRESSIVE DRIFT PHONK (16s Seamless Loop) #Shorts #GymPhonk #DriftPhonk"

DESCRIPTION_EN = """⚡ 16s Seamless Loop - Aggressive Drift Phonk & Gym EDM.
🎧 Full 1-Hour Mix available in Related Video!

🔥 Subscribe to @PhonkForgeAudio for daily non-stop high-energy mixes!

#Shorts #GymPhonk #DriftPhonk #WorkoutMusic #Hardstyle #BassBoosted #PhonkForge #EDM #LateNightDrive
"""

TAGS = [
    "shorts", "gym phonk", "drift phonk", "aggressive phonk", "phonk loop", 
    "heavy bass", "workout motivation", "phonk 2026", "phonkforge", 
    "bass boosted", "drift edm", "hardstyle", "beast mode"
]

LOCALIZATIONS = {
    "ru": {
        "title": "⚡ АГРЕССИВНЫЙ ДРИФТ ФОНК (16с Луп) #Shorts #ДрифтФонк #Фонк",
        "description": "⚡ 16-секундный бесшовный луп агрессивного дрифт-фонка! Полный 1-часовой микс доступен в связанных видео.\n\n#Shorts #ДрифтФонк #Фонк #Качалка"
    },
    "pt": {
        "title": "⚡ AGGRESSIVE DRIFT PHONK (16s Loop) #Shorts #GymPhonk #DriftPhonk",
        "description": "⚡ Loop perfeito de 16s de Drift Phonk & Gym EDM! Mix completo de 1 hora no vídeo relacionado.\n\n#Shorts #GymPhonk #DriftPhonk #Treino"
    },
    "es": {
        "title": "⚡ AGGRESSIVE DRIFT PHONK (16s Loop) #Shorts #GymPhonk #DriftPhonk",
        "description": "⚡ ¡Loop sin fin de 16s de Drift Phonk y Gym EDM! Mix completo de 1 hora en el video relacionado.\n\n#Shorts #GymPhonk #DriftPhonk #Entrenamiento"
    },
    "ko": {
        "title": "⚡ 하이퍼 드리프트 폰크 (16초 무한루프) #Shorts #짐폰크 #드리프트폰크",
        "description": "⚡ 16초 무한 루프 드리프트 폰크 & 짐 EDM! 1시간 풀버전은 관련 동영상 링크에서 감상하세요.\n\n#Shorts #짐폰크 #드리프트폰크 #헬스음악 #노동요"
    },
    "ja": {
        "title": "⚡ 超重低音ドリフトPhonk（16秒シームレス無限ループ）#Shorts #GymPhonk #DriftPhonk",
        "description": "⚡ 16秒シームレス無限ループ！超重低音Aggressive Drift Phonk & 筋トレEDM。\n🎧 1時間フル公式Mixは関連動画リンクから視聴できます！\n\n#Shorts #ドリフトフォンク #ジムフォンク #筋トレBGM #作業用BGM"
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
comment_text = """⚡ What did you hit on this beat? PR or Night Drift? Drop below! ⬇️

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
