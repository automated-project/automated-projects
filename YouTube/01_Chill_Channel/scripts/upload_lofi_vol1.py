# -*- coding: utf-8 -*-
"""
Ch 1 (GameVerse ➡️ Lofi) 第1弾 ジブリ風 勉強・作業用ノスタルジックLofi 1時間動画 アップロードスクリプト
- Video: output_videos/1HOUR_GHIBLI_NOSTALGIC_LOFI_VOL1.mp4 (60分41秒)
- Thumbnail: output_videos/thumbnails/THUMBNAIL_01_CHILL_LOFI_LARGE.jpg
- Token: gameverse (token_gameverse.json)
- SEO & Multilingual localizations & Pinned Comment
"""
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Dark_Fantasy_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/1HOUR_GHIBLI_NOSTALGIC_LOFI_VOL1.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/THUMBNAIL_01_CHILL_LOFI_LARGE.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/1HOUR_GHIBLI_NOSTALGIC_LOFI_VOL1_chapters.txt"

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

print(f"=== Starting Upload for Vol. 1 Ghibli Lofi Mix on GameVerse/Lofi Channel ===")
yt = get_youtube_service("gameverse")

TITLE_EN = "🍃 [1 HOUR] Studio Ghibli Inspired Chill Lofi — Nostalgic Beats for Study, Work & Deep Sleep"

DESCRIPTION_EN = f"""🍃 Welcome to our peaceful corner of the world — Studio Ghibli inspired nostalgic chill lofi beats for deep focus, studying, working, reading, and relaxing sleep.

Immerse yourself in 1 hour of warm acoustic guitars, soft upright piano melodies, and gentle vinyl tape textures. Designed to create a cozy, stress-free atmosphere that calms your mind.

🎵 Tracklist / Timestamps:
{chapters_text}

🎧 Sound Design & Mastering:
- Warm Tape Acoustic Mastering (-14.0 LUFS)
- Gentle 80 BPM Steady Lo-Fi Rhythms & Organic Textures

🔔 Subscribe to join our daily cozy study sessions & relaxing lofi journeys!

#Lofi #ChillLofi #GhibliLofi #StudyMusic #LofiHipHop #RelaxingBGM #SleepMusic #CozyVibes #FocusMusic #1HourLofi
"""

TAGS = [
    "lofi", "chill lofi", "ghibli lofi", "study music", "lofi hip hop", "relaxing beats",
    "sleep music", "cozy lofi", "nostalgic lofi", "work music", "reading bgm",
    "1 hour lofi", "studio ghibli lofi", "peaceful lofi", "deep focus"
]

LOCALIZATIONS = {
    "ru": {
        "title": "🍃 [1 ЧАС] Лофай в стиле Студии Гибли — Уютный Лофай для Учебы, Работы и Сна",
        "description": f"🍃 1 час спокойного и ностальгического Lo-Fi в стиле Студии Гибли для глубокой концентрации, учебы, чтения и сна.\n\n🎵 Треклист:\n{chapters_text}\n\n#Лофай #МузыкаДляУчебы #ГиблиЛофай #Lofi"
    },
    "pt": {
        "title": "🍃 [1 HORA] Lofi Inspirado no Studio Ghibli — Beats Nostálgicos para Estudar e Dormir",
        "description": f"🍃 1 hora de Lofi acústico e nostálgico inspirado no Studio Ghibli para foco profundo, estudos, trabalho e sono tranquilo.\n\n🎵 Tracklist:\n{chapters_text}\n\n#Lofi #MusicaParaEstudar #LofiGhibli #Relaxar"
    },
    "es": {
        "title": "🍃 [1 HORA] Lofi Inspirado en Studio Ghibli — Beats Nostálgicos para Estudiar y Dormir",
        "description": f"🍃 1 hora de música Lofi tranquila y nostálgica inspirada en Studio Ghibli para estudiar, trabajar, leer y descansar.\n\n🎵 Lista de canciones:\n{chapters_text}\n\n#Lofi #MusicaParaEstudiar #GhibliLofi #Relax"
    },
    "ko": {
        "title": "🍃 [1시간] 지브리 감성 칠 로파이 — 공부·집중·독서·수면을 위한 힐링 노동요",
        "description": f"🍃 1시간 연속 재생 지브리 감성 노스탤직 로파이 비트! 깊은 집중, 독서, 프로그래밍, 편안한 수면을 위한 따뜻한 아쿠스틱 사운드.\n\n🎵 트랙리스트:\n{chapters_text}\n\n#로파이 #지브리로파이 #공부할때듣는음악 #노동요 #수면음악 #1시간"
    },
    "ja": {
        "title": "🍃【1時間】ジブリ風ノスタルジック作業用Chill Lofi — 勉強・仕事・読書・睡眠用 極上ピアノ＆アコースティックBGM",
        "description": f"🍃 1時間ノンストップ！ジブリの世界観に浸る、温かいアコースティック＆ピアノの極上ノスタルジックLofi Mix。\n勉強、プログラミング、読書、カフェ作業、そして夜の睡眠導入に最適な、耳に優しい癒やしの空間をお届けします。\n\n🎵 トラックリスト:\n{chapters_text}\n\n#Lofi #ジブリ風Lofi #作業用BGM #勉強用BGM #睡眠用BGM #チルBGM #1時間耐久"
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

print("[+] Uploading 1-Hour Lofi Video (approx 1.2GB)...")
response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"    Progress: {int(status.progress() * 100)}%")

video_id = response.get("id")
print("==================================================")
print(f"✅ Lofi Video Upload Successful!")
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
comment_text = """🍃 Welcome to your daily cozy study & relaxation room. 

What are you working on or studying today? Let us know in the comments below, and feel free to share your favorite moments or timestamps! ☕📚

✨ Subscribe to join our cozy community for daily relaxing lofi sessions!"""

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
