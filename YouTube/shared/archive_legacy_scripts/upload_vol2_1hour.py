# -*- coding: utf-8 -*-
"""
第3チャンネル（AuraMelody Audio）第2弾1時間長尺Mix公式動画 アップロードスクリプト
- Video: output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL2_OFFICIAL.mp4
- Thumbnail: output_videos/thumbnails/THUMBNAIL_VOL2_PERFECT_CENTER.jpg
- Token: auramelody (token_auramelody.json)
- SEO & Multilingual localizations & Pinned Comment
"""
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Coding_Synth_Channel")
VIDEO_PATH = CHANNEL_DIR / "output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL2_OFFICIAL.mp4"
THUMBNAIL_PATH = CHANNEL_DIR / "output_videos/thumbnails/THUMBNAIL_VOL2_PERFECT_CENTER.jpg"
CHAPTERS_PATH = CHANNEL_DIR / "output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL2_chapters.txt"

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

print(f"=== Starting Upload for Vol. 2 Official 1-Hour Mix on AuraMelody Audio ===")
yt = get_youtube_service("auramelody")

TITLE_EN = "✨ [1 HOUR] Pure Uplifting Melodic EDM — Beautiful Progressive House Mix for Focus & Energy"

DESCRIPTION_EN = f"""✨ Welcome to AuraMelody Audio — Pure Uplifting Melodic EDM & Progressive House for Focus, Energy, and Good Vibes.

Immerse yourself in 1 hour of continuous, crystal-clear euphoric melodies inspired by the golden era of Avicii, Kygo, and melodic festival anthems. Perfect for deep focus, coding, studying, workout, gaming, and night drives.

🎵 Tracklist / Chapters:
{chapters_text}

🎧 Sound Design & Mastering:
- SoftBass Transparent Mastering (Enhanced Sub-Bass & Crystal Highs)
- Original High-Fidelity Audio Experience

🔥 Subscribe to @AuraMelodyAudio for non-stop uplifting melodies & festival energy!

#MelodicEDM #ProgressiveHouse #AviciiStyle #EDMMix #StudyMusic #FocusMusic #CodingBGM #SummerVibes #AuraMelody #1HourMix
"""

TAGS = [
    "melodic edm", "progressive house", "avicii style", "uplifting edm", "edm mix 2026",
    "1 hour edm mix", "study music edm", "coding music", "gaming bgm", "festival vibes",
    "summer melodic edm", "auramelody", "euphoric edm", "chill house", "edm mix 1 hour"
]

LOCALIZATIONS = {
    "ru": {
        "title": "✨ [1 ЧАС] Мелодичный EDM и Прогрессив Хаус — Микс для энергии и концентрации",
        "description": f"✨ 1 час кристально чистого Melodic EDM и Progressive House для учебы, работы, тренировок и концентрации.\n\n🎵 Треклист:\n{chapters_text}\n\n#МелодикEDM #ПрогрессивХаус #МузыкаДляУчебы #EDM"
    },
    "pt": {
        "title": "✨ [1 HORA] Pure Uplifting Melodic EDM — Mix de Progressive House para Foco e Energia",
        "description": f"✨ 1 hora de Melodic EDM e Progressive House para foco, trabalho, treino e vibe positiva.\n\n🎵 Tracklist:\n{chapters_text}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaEstudar #EDM"
    },
    "es": {
        "title": "✨ [1 HORA] Pure Uplifting Melodic EDM — Mix de Progressive House para Concentración",
        "description": f"✨ 1 hora de Melodic EDM y Progressive House para estudiar, trabajar, entrenar y concentrarse.\n\n🎵 Lista de canciones:\n{chapters_text}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaEstudiar #EDM"
    },
    "ko": {
        "title": "✨ [1시간] 퓨어 멜로딕 EDM & 프로그레시브 하우스 — 공부·집중·노동요를 위한 감성 믹스",
        "description": f"✨ 1시간 연속 재생 감성 멜로딕 EDM & 프로그레시브 하우스! 집중, 공부, 코딩, 드라이브를 위한 최고의 에너제틱 사운드.\n\n🎵 트랙리스트:\n{chapters_text}\n\n#멜로딕EDM #프로그레시브하우스 #노동요 #공부할때듣는음악 #1시간"
    },
    "ja": {
        "title": "✨ [1時間] 爽快エモーショナルMelodic EDM — 集中力・モチベーションを高める極上Progressive House作業用BGM",
        "description": f"✨ 1時間ノンストップ！ Aviciiスタイルの多幸感あふれる極上Melodic EDM & Progressive House Mix。\n作業、プログラミング、勉強、ドライブ、ワークアウトに最適な高揚感をお届けします。\n\n🎵 トラックリスト:\n{chapters_text}\n\n#メロディックEDM #プログレッシブハウス #作業用BGM #勉強用BGM #洋楽EDM #1時間耐久"
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

print("[+] Uploading 1-Hour Long Mix Video (approx 1.2GB)...")
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
comment_text = """✨ Which track gave you the most energy today? Let us know in the comments below, and feel free to share your favorite moments or timestamps! ⬇️

🔥 Subscribe to @AuraMelodyAudio for daily uplifting vibes & focus music!"""

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
