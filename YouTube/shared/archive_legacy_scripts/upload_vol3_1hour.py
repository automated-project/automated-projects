# -*- coding: utf-8 -*-
"""
第3チャンネル（AuraMelody Audio）第3弾 1時間長尺Mix公式動画 アップロード & 旧動画整理スクリプト
- Video: output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL3.mp4
- Thumbnail: output_videos/thumbnails/THUMBNAIL_CH3_VOL3_SUMMER_MELODIC.jpg
- Token: auramelody (token_auramelody.json)
- Accurate Channel Handle: @AuraMelody-Audio
- Free BGM / Royalty Free Declaration
- Full 21-Track Timestamps (New deduplicated list)
- Multilingual SEO & Engagement Comment
"""
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL3.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/THUMBNAIL_CH3_VOL3_SUMMER_MELODIC.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL3_chapters.txt"

OLD_VIDEO_ID = "pW2Zw1TvNXA" # 冒頭曲重複があった前バージョン

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

print("=== Starting Upload for Vol. 3 Rebuilt 1-Hour Mix on AuraMelody Audio ===")
yt = get_youtube_service("auramelody")

# 1. 旧動画の削除 (Delete Old Duplicate Video)
try:
    print(f"[+] Deleting previous duplicate video ID: {OLD_VIDEO_ID}...")
    yt.videos().delete(id=OLD_VIDEO_ID).execute()
    print(f"✅ Successfully deleted old video: {OLD_VIDEO_ID}")
except Exception as e:
    print(f"⚠️ Note on deleting old video: {e}")

# 2. 新規動画のアップロード
TITLE_EN = "✨ [1 HOUR] Golden Hour Melodic EDM — Uplifting Progressive House Beats for Work & Drive"

DESCRIPTION_EN = f"""✨ Welcome to AuraMelody Audio — Pure Uplifting Melodic EDM & Progressive House for Work, Drive, and Daily Energy.

Immerse yourself in 1 hour of non-stop, crystal-clear euphoric melodies. Crafted with warm golden tones to elevate your mood and soundtrack your creative flow. Perfect for work, driving, studying, workouts, and relaxation.

100% Free & Royalty-Free for Creators! Feel free to use this track in your YouTube videos, live streams, and background projects.

🎵 Tracklist / Timestamps:
{chapters_text}

🎧 Sound Design & Mastering:
- SoftBass Transparent Mastering (-14.0 LUFS / Crystal Highs & Warm Lows)
- Seamless 2.5s DJ Energy Crossfades
- Visuals: Pure Luminous Floating Bokeh Orbs

📜 License:
- 100% Free to use for videos, podcasts, and streams.
- Credit appreciated: Music by @AuraMelody-Audio (https://www.youtube.com/@AuraMelody-Audio)

🔥 Subscribe to @AuraMelody-Audio for regular uplifting melodies & festival energy!

#MelodicEDM #ProgressiveHouse #GoldenHour #EDMMix #StudyMusic #DriveMusic #WorkBGM #AuraMelody #1HourMix #FreeBGM
"""

TAGS = [
    "melodic edm", "progressive house", "uplifting edm", "golden hour edm", "edm mix 2026",
    "1 hour edm mix", "study music edm", "coding music", "drive music", "festival vibes",
    "auramelody", "euphoric edm", "free bgm edm", "royalty free music edm"
]

LOCALIZATIONS = {
    "ru": {
        "title": "✨ [1 ЧАС] Melodic EDM Золотого Часа — Прогрессив Хаус для Работы и Поездок",
        "description": f"✨ 1 час кристально чистого Melodic EDM и Progressive House для работы, поездок, кодинга и концентрации.\n\n100% Бесплатно для использования в ваших видео и стримах!\n\n🎵 Треклист:\n{chapters_text}\n\n#МелодикEDM #ПрогрессивХаус #МузыкаДляРаботы #EDM #AuraMelody"
    },
    "pt": {
        "title": "✨ [1 HORA] Golden Hour Melodic EDM — Progressive House para Trabalho e Viagem",
        "description": f"✨ 1 hora de Melodic EDM e Progressive House para foco, trabalho, direção e vibe positiva.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{chapters_text}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaTrabalhar #EDM #AuraMelody"
    },
    "es": {
        "title": "✨ [1 HORA] Golden Hour Melodic EDM — Progressive House para Trabajo y Conducir",
        "description": f"✨ 1 hora de Melodic EDM y Progressive House para estudiar, trabajar, conducir y entrenar.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{chapters_text}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaTrabajar #EDM #AuraMelody"
    },
    "ko": {
        "title": "✨ [1시간] 골든아워 감성 멜로딕 EDM & 프로그레시브 하우스 — 업무·드라이브·노동요",
        "description": f"✨ 1시간 논스톱 따스하고 청량한 감성 멜로딕 EDM & 프로그레시브 하우스! 업무, 공부, 코딩, 드라이브를 위한 최고의 에너제틱 사운드.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트:\n{chapters_text}\n\n#멜로딕EDM #프로그레시브하우스 #노동요 #드라이브음악 #1시간 #AuraMelody"
    },
    "ja": {
        "title": "✨ [1時間] 爽快エモーショナルGolden Hour EDM — 作業効率・モチベーションを高める極上Progressive House作業用BGM",
        "description": f"✨ 1時間ノンストップ！ 心地よい高揚感あふれる極上Melodic EDM & Progressive House Mix。\n作業、プログラミング、勉強、ドライブ、ワークアウトに最適なBGMをお届けします。\n\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可）】です。\n\n🎵 トラックリスト:\n{chapters_text}\n\n#メロディックEDM #プログレッシブハウス #作業用BGM #勉強用BGM #ドライブBGM #1時間耐久 #フリーBGM #AuraMelody"
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

media = MediaFileUpload(str(VIDEO_PATH), chunksize=10*1024*1024, resumable=True, mimetype="video/mp4")
request = yt.videos().insert(
    part="snippet,status,localizations",
    body=body,
    media_body=media
)

print("[+] Uploading Rebuilt 1-Hour Long Mix Video...")
response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"    Progress: {int(status.progress() * 100)}%")

video_id = response.get("id")
print("==================================================")
print(f"✅ Video Upload Successful!")
print(f"   Video ID: {video_id}")
print(f"   Watch URL: https://youtu.be/{video_id}")
print("==================================================")

# Set Thumbnail
print(f"\n[+] Setting Thumbnail: {THUMBNAIL_PATH.name}...")
time.sleep(2)
try:
    yt.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
    ).execute()
    print("✅ Custom Thumbnail set successfully!")
except Exception as e:
    print(f"⚠️ Note on thumbnail setting: {e}")

# Post Pinned Engagement Comment
print("\n[+] Posting Pinned Engagement Comment...")
time.sleep(2)
comment_text = """✨ Which track gave you the best energy today? Let us know in the comments below, and feel free to share your favorite timestamps! ⬇️

🎵 100% Free & Royalty-Free for content creators and streamers.
🔥 Subscribe to @AuraMelody-Audio for regular uplifting melodies & festival energy!"""

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
