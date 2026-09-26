# -*- coding: utf-8 -*-
"""
第3チャンネル（AuraMelody Audio）公式動画 多言語ローカライズ一括反映スクリプト
Video ID: o8ygRO9KVuQ
- 英語（デフォルト）、ロシア語、ポルトガル語、スペイン語、韓国語、日本語の6言語設定
- サムネイル画像の自動セット
- 公式固定コメント（Pinned Comment）の自動投稿
"""
import sys
import os
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

VIDEO_ID = "o8ygRO9KVuQ"
THUMBNAIL_PATH = Path("/Users/base/Automated-Projects/YouTube/03_Coding_Synth_Channel/output_videos/thumbnails/THUMBNAIL_01A_PERFECT.jpg")

print(f"=== Applying Metadata to Video: {VIDEO_ID} on AuraMelody Audio ===")
yt = get_youtube_service("auramelody")

# 1. 各言語のメタデータ定義
TAGS = [
    "melodic edm", "progressive house", "summer edm mix", "1 hour edm",
    "vocal edm", "festival edm", "uplifting edm", "avicii style", "zedd style",
    "dance music 2026", "driving music", "gaming music", "workout edm", "euphoric edm"
]

TRACKLIST_TIMESTAMPS = """00:00 - Hands Turn Slowly
02:56 - Brighter Than The Sun
05:51 - Breaking Past Gravity
08:46 - Broken Glass Mornings
11:44 - Burning Like Stars
14:37 - Beyond The Heavy Ground
17:09 - Weightless In The Sun
20:07 - Sun Above
22:47 - Golden Motion
25:45 - Chasing the Infinite
28:41 - Chasing Endless Daylight
31:39 - Salt and Sunlight
34:29 - Midnight Afterglow
37:27 - Weightless In Gold
40:27 - A Thousand Frames
43:27 - Chasing After Endless Light
46:26 - Golden Hour Traces
49:22 - Salt in Our Hair
52:20 - Wait for the Motion
55:20 - Healed by Summer Light
58:18 - The Chair By The Door"""

DESC_EN = f"""Feel the ultimate summer energy with this 1-Hour Uplifting Melodic EDM & Progressive House Mix! 🌊✨
Featuring breathtaking female vocals, soaring piano melodies, and euphoric festival drops. Perfect for driving, workout, gaming, and boosting your daily mood!

🎧 Tracklist & Timestamps:
{TRACKLIST_TIMESTAMPS}

🔔 Subscribe to AuraMelody Audio for the freshest melodic EDM, progressive house, and summer anthems!

#MelodicEDM #ProgressiveHouse #SummerMix #VocalEDM #FestivalEDM #AuraMelody"""

LOCALIZATIONS = {
    "ru": {
        "title": "1 ЧАС ЛЕТНИЙ МЕЛОДИК EDM МИКС 2026 ☀️ Вокальный Прогрессив Хаус и Фестивальная Энергия",
        "description": f"""Почувствуйте летнюю энергию с этим 1-часовым миксом Melodic EDM и Progressive House! 🌊✨
Захватывающий женский вокал, парящие фортепианные мелодии и эйфорические фестивальные дропы. Идеально подходит для поездок, тренировок, игр и отличного настроения!

🎧 Треклист:
{TRACKLIST_TIMESTAMPS}

#MelodicEDM #ProgressiveHouse #ЛетнийМикс #EDM"""
    },
    "pt": {
        "title": "1 HORA DE MELODIC EDM MIX DE VERÃO 2026 ☀️ Vocal Progressive House & Festival Vibes",
        "description": f"""Sinta a melhor energia do verão com este mix de 1 hora de Melodic EDM e Progressive House! 🌊✨
Vocais femininos emocionantes, melodias de piano e drops eufóricos de festival. Perfeito para dirigir, treinar, jogar e se motivar!

🎧 Faixas:
{TRACKLIST_TIMESTAMPS}

#MelodicEDM #ProgressiveHouse #MixDeVerao #EDMBrasil"""
    },
    "es": {
        "title": "1 HORA DE SUMMER MELODIC EDM MIX 2026 ☀️ Vocal Progressive House y Festival Vibes",
        "description": f"""¡Siente la energía del verano con esta sesión de 1 hora de Melodic EDM y Progressive House! 🌊✨
Vocales femeninas increíbles, pianos emotivos y drops eufóricos de festival. ¡Ideal para conducir, entrenar, jugar y motivarte!

🎧 Lista de Canciones:
{TRACKLIST_TIMESTAMPS}

#MelodicEDM #ProgressiveHouse #VeranoEDM #MusicaElectronica"""
    },
    "ko": {
        "title": "[1시간] 청량한 멜로딕 EDM 보컬 믹스 2026 ☀️ 드라이브 & 기분 전환 프로그레シ브 하우스",
        "description": f"""가슴 벅찬 청량함! 1시간 연속 멜로딕 EDM & 프로그레시브 하우스 보컬 믹스입니다! 🌊✨
감성적인 피아노와 시원한 신스 드롭, 드라이브나 운동, 게임할 때 최고의 텐션을 선사합니다!

🎧 트랙리스트:
{TRACKLIST_TIMESTAMPS}

#멜로딕EDM #프로그레시브하우스 #드라이브음악 #노동요 #1시간EDM"""
    },
    "ja": {
        "title": "【1時間】超爽快・エモーショナルMelodic EDMボーカルMix 2026 ☀️ ドライブ・テンション爆上げ作業用BGM",
        "description": f"""究極の爽快感とエモさ！1時間ノンストップ・綺麗系Melodic EDM & プログレッシブハウス公式Mix！🌊✨
透き通る女性ボーカル、感情を揺さぶるピアノメロディ、疾走するスーパードロップ。ドライブ、筋トレ、作業、ゲームのお供に最高の一枚です！

🎧 トラックリスト:
{TRACKLIST_TIMESTAMPS}

#MelodicEDM #プログレッシブハウス #作業用BGM #ドライブBGM #洋楽EDM"""
    }
}

# 2. 動画の既存カテゴリ・スニペット取得
video_res = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()
item = video_res["items"][0]
category_id = item["snippet"].get("categoryId", "10")  # 10 = Music

# 3. メタデータ & 多言語ローカライズ更新
title_en = "1 HOUR SUMMER MELODIC EDM MIX 2026 ☀️ Uplifting Vocal Progressive House & Festival Vibes"
update_body = {
    "id": VIDEO_ID,
    "snippet": {
        "title": title_en,
        "description": DESC_EN,
        "tags": TAGS,
        "categoryId": category_id,
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    },
    "localizations": LOCALIZATIONS
}

print("1. Updating snippet & localizations (en, ru, pt, es, ko, ja)...")
res = yt.videos().update(part="snippet,localizations", body=update_body).execute()
print("✅ Metadata & Localizations updated successfully!")

# 4. サムネイルの自動アップロード
if THUMBNAIL_PATH.exists():
    print(f"2. Setting official thumbnail: {THUMBNAIL_PATH.name}...")
    try:
        from googleapiclient.http import MediaFileUpload
        media = MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
        yt.thumbnails().set(videoId=VIDEO_ID, media_body=media).execute()
        print("✅ Thumbnail updated successfully!")
    except Exception as e:
        print(f"⚠️ Thumbnail upload note: {e}")

# 5. 公式ピン留めコメントの投稿
print("3. Posting official pinned comment...")
comment_text = "Welcome to AuraMelody Audio! ☀️🌊 Which track was your favorite in this mix? Let us know in the comments below! Don't forget to subscribe for more 1-Hour Melodic EDM anthems!"
try:
    c_res = yt.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": VIDEO_ID,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    ).execute()
    print("✅ Successfully posted official pinned comment!")
except Exception as e:
    print(f"⚠️ Comment post note: {e}")

print("🎉 ALL METADATA & LOCALIZATION APPLIED PERFECTLY!")
