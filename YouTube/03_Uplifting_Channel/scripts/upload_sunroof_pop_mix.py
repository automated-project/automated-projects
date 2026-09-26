#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): 1時間長尺 Sunroof Feel-Good Pop Mix 公式動画 アップロードスクリプト
- Video: output_videos/1HOUR_SUNROOF_FEEL_GOOD_POP_MIX.mp4
- Thumbnail: output_videos/thumbnails/thumb_ch3_sunroof_02_feel_good_pop.jpg
- Token: auramelody (token_auramelody.json)
- Channel: @AuraMelody-Audio (UCldq7fhclKDAXUA1gLI0FRw)
- Full 21-Track Timestamps
- Multilingual SEO Localizations & License Declaration
"""

import os
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/1HOUR_SUNROOF_FEEL_GOOD_POP_MIX.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/thumb_ch3_sunroof_02_feel_good_pop.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/1HOUR_SUNROOF_FEEL_GOOD_POP_MIX_chapters.txt"

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

print("=== Starting Upload for 1-Hour Sunroof Feel-Good Pop Mix on AuraMelody Audio ===")
yt = get_youtube_service("auramelody")

TITLE_EN = "☀️ [1 HOUR] Feel Good Pop Dance & Acoustic Hits — Upbeat Sunshine Vibes for Work & Drive"

DESCRIPTION_EN = f"""☀️ Welcome to AuraMelody Audio — Pure Joyful & Uplifting Feel-Good Pop Dance & Acoustic Hits!

Immerse yourself in 1 hour of non-stop, feel-good acoustic pop dance and vibrant upbeat melodies. Crafted with bright acoustic guitars, cheerful horns, bouncy basslines, and positive male vocals to elevate your mood and boost dopamine. Perfect for work, driving, studying, morning motivation, and workouts.

100% Free & Royalty-Free for Creators! Feel free to use these tracks in your YouTube videos, live streams, and background projects.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 TRACKLIST & TIMESTAMPS:
{chapters_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 【FREE DOWNLOAD & CREATOR LICENSE / フリー音源利用規約】
You can freely use this track in your YouTube videos, Twitch streams, TikToks & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
✅ Commercial & Non-Commercial Use Free
📋 Required Attribution (Copy & Paste):
   Music: AuraMelody Audio
   Watch: https://www.youtube.com/@AuraMelody-Audio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎧 Sound Design & Mastering:
- SoftBass Transparent Mastering (-14.0 LUFS / Crystal Highs & Warm Lows)
- Seamless 2.5s DJ Equal-Power Crossfades
- Visuals: 1080p Pure Coastal Sunset Anime Art

━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 LOOKING FOR HEAVY BASS OR COZY LOFI?
Check out our dedicated sister channels:

🔥 Heavy Bass & Gym Phonk ➡️ @PhonkForgeAudio-s1h
https://www.youtube.com/@PhonkForgeAudio-s1h

🌿 Cozy Lofi & Study Beats ➡️ @Haven-Chill-Audio
https://www.youtube.com/@Haven-Chill-Audio
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe to @AuraMelody-Audio for regular feel-good pop dance & positive energy!

#FeelGoodPop #PopDance #AcousticPop #UpbeatMusic #WorkBGM #DriveMusic #Dopamine #AuraMelody #1HourMix #FreeBGM
"""

TAGS = [
    "feel good pop", "pop dance", "acoustic pop", "upbeat pop", "sunroof vibes",
    "1 hour pop mix", "work music", "study music", "drive music", "morning motivation",
    "auramelody", "auramelody audio", "positive music", "dopamine music", "free bgm pop"
]

LOCALIZATIONS = {
    "ru": {
        "title": "☀️ [1 ЧАС] Feel Good Pop Dance & Акустические Хиты — Для Работы и Дороги",
        "description": f"☀️ 1 час позитивной и энергичной поп-дэнс музыки с живой акустической гитарой и ярким вокалом! Идеально для работы, учебы, поездок и поднятия настроения.\n\n100% Бесплатно для создателей контента!\n\n🎵 Треклист:\n{chapters_text}\n\n#ПопМузыка #МузыкаДляРаботы #ПозитивнаяМузыка #AuraMelody"
    },
    "pt": {
        "title": "☀️ [1 HORA] Feel Good Pop Dance & Acoustic Hits — Para Trabalho e Viagem",
        "description": f"☀️ 1 hora de pop dance acústico alegre e contagiante para elevar o ânimo, trabalhar, estudar e dirigir com energia positiva.\n\n100% Grátis e Royalty-Free para criadores!\n\n🎵 Tracklist:\n{chapters_text}\n\n#PopDance #MusicaParaTrabalhar #GoodVibes #AuraMelody"
    },
    "es": {
        "title": "☀️ [1 HORA] Feel Good Pop Dance & Éxitos Acústicos — Para Trabajo y Conducir",
        "description": f"☀️ 1 hora de música pop dance alegre y acústica para motivarte, trabajar, estudiar y disfrutar del camino con buena vibra.\n\n100% Libre de regalías para creadores!\n\n🎵 Lista de canciones:\n{chapters_text}\n\n#PopDance #MusicaParaTrabajar #BuenaVibra #AuraMelody"
    },
    "ko": {
        "title": "☀️ [1시간] 청량한 팝 댄스 & 어쿠스틱 힐링 믹스 — 신나는 노동요·드라이브·텐션업",
        "description": f"☀️ 1시간 논스톱! 밝고 기분 좋은 어쿠스틱 기타와 팝 댄스 비트의 특급 힐링 믹스. 업무, 공부, 드라이브, 아침 모닝 루틴에 활력을 불어넣어 드립니다.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트:\n{chapters_text}\n\n#팝댄스 #노동요 #드라이브음악 #신나는노래 #1시간 #AuraMelody"
    },
    "ja": {
        "title": "☀️ 【作業用BGM/1時間】爽快ポップダンス＆アコースティック名曲Mix — テンションが上がるドライブ・仕事・勉強用",
        "description": f"☀️ 1時間ノンストップ！聴くだけで気分が上がる明るいアコースティックギターと爽快ポップダンスビートの特上BGM。\n仕事、勉強、ドライブ、朝のモチベーションアップに最高のポジティブサウンドをお届けします。\n\n動画や配信で使える100%フリー音源（商用利用可・クレジット表記で無料）！\n\n🎵 トラックリスト:\n{chapters_text}\n\n#作業用BGM #ポップダンス #ドライブBGM #勉強用BGM #1時間 #AuraMelody"
    }
}

body = {
    "snippet": {
        "title": TITLE_EN,
        "description": DESCRIPTION_EN,
        "tags": TAGS,
        "categoryId": "10", # Music
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

# 4. 固定コメント（Engagement Comment）の投稿
comment_text = """☀️ Thank you for tuning in to AuraMelody Audio! 
If you enjoyed these feel-good pop dance vibes, please give it a LIKE 👍 and SUBSCRIBE for weekly uplifting beats!

Which track was your favorite? Let us know in the comments below! 👇✨"""

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

print(f"\n🚀 ALL TASKS COMPLETED! Live at https://youtu.be/{video_id}")
