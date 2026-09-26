# -*- coding: utf-8 -*-
"""
第2チャンネル（PhonkForge Audio）Aggressive Drift & Late Night Gym Phonk メタデータ投入スクリプト
Video ID: 4aJlGEfEI84
Thumbnail: Option 3 (Aggressive Drift / Late Night Highway)
"""
import sys
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

VIDEO_ID = "4aJlGEfEI84"

print(f"=== Applying Aggressive Drift Phonk Metadata to Video: {VIDEO_ID} on PhonkForge Audio ===")
yt = get_youtube_service("phonkforge")

TAGS = [
    "drift phonk", "aggressive phonk", "gym phonk", "hardstyle phonk", 
    "late night drive phonk", "phonk 2026", "phonk mix 1 hour", 
    "heavy bass workout", "midnight drift", "brazilian phonk", 
    "workout edm", "phonkforge", "bass boosted", "super crisp audio",
    "beast mode workout", "gym motivation"
]

TITLE_EN = "🔥 [1 HOUR] AGGRESSIVE DRIFT PHONK & GYM EDM MIX 2026 | Late Night Highway Workout Motivation"

DESCRIPTION_EN = """⚡ [1 HOUR] AGGRESSIVE DRIFT PHONK & GYM EDM MIX 2026
Engineered for high-intensity gym workouts, heavy PR lifts, fast late-night highway drives, and unstoppable focus.
Mastered with Super Crisp Sound Engineering (Deep Sub-Bass +8.5dB & Highs +9.0dB) with zero silence gaps (Seamless DJ Crossfade).

⏱️ TRACKLIST & TIMESTAMPS:
00:00 01. Storming The Gate
02:54 02. Asphalt Bite
05:54 03. Asphalt Fang
08:46 04. Asphalt Reaper
11:35 05. Asphalt Redline
14:31 06. Asphalt Takedown
17:31 07. Asphalt Teeth
20:27 08. Asphalt Vise
23:27 09. Blacktop Fury
26:26 10. Concrete Pursuit
29:26 11. Raw Aggressive Drive
32:25 12. Crush The Bone
35:18 13. Kingdom Of My Own
38:03 14. Midnight Asphalt
41:02 15. Midnight Asphalt Burn
43:55 16. Midnight Redline
46:49 17. Redline Impact
49:47 18. Redline Pressure
52:47 19. Redline Torque
55:39 20. Savage Grip
58:32 21. Tarmac Teeth
61:30 22. The Iron Ascent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎧 Visualizer: Luminous White 48-Bar Discrete Rounded Bars
🔥 Subscribe to @PhonkForgeAudio for daily non-stop gym workout & aggressive drift mixes!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#WorkoutMusic #GymPhonk #DriftPhonk #Hardstyle #BassBoosted #BeastMode #PhonkForge #EDM #LateNightDrive
"""

LOCALIZATIONS = {
    "ru": {
        "title": "🔥 [1 ЧАС] АГРЕССИВНЫЙ ДРИФТ ФОНК 2026 | Ночной Дрифт и Музыка для Качалки",
        "description": "Погрузитесь в абсолютную агрессию и мощь с этим 1-часовым Drift Phonk & Gym EDM сетом! ⚡\nТяжелый бас, агрессивный ритм и кристальное сведение для максимального пампа на тренировке и ночного дрифта.\n\n#DriftPhonk #GymPhonk #Фонк #Тренировка #НочнойДрифт"
    },
    "pt": {
        "title": "🔥 [1 HORA] AGGRESSIVE DRIFT PHONK & GYM EDM 2026 | Treino Noturno e Automotivo",
        "description": "Sinta a energia máxima com este mix de 1 hora de Aggressive Drift Phonk e Gym EDM! ⚡\nGraves pesados, ritmo insano e masterização nítida para quebrar seus recordes na academia e acelerar na pista.\n\n#DriftPhonk #GymPhonk #TreinoPesado #Phonk2026"
    },
    "es": {
        "title": "🔥 [1 HORA] AGGRESSIVE DRIFT PHONK & GYM EDM 2026 | Motivación para Entrenar al Límite",
        "description": "¡Desata tu verdadero potencial con este mix de 1 hora de Aggressive Drift Phonk y Gym EDM! ⚡\nBajos demoledores, ritmo agresivo y masterización cristalina para entrenar al límite y conducir de noche.\n\n#DriftPhonk #GymPhonk #Entrenamiento #Phonk2026"
    },
    "ko": {
        "title": "🔥 [1시간] 하이퍼 드리프트 폰크 & 짐 EDM 믹스 2026 | 심야 드라이브 & 헬스 고음질 노동요",
        "description": "한계를 뛰어넘는 초고음질 Aggressive Drift Phonk & Gym EDM 1시간 연속 믹스! ⚡\n묵직한 중저음과 압도적인 텐션으로 헬스장 PR 갱신과 심야 드라이브를 위한 최고의 트랙!\n\n#드리프트폰크 #짐폰크 #헬스음악 #노동요 #드라이브음악"
    },
    "ja": {
        "title": "🔥【1時間】超重低音アグレッシブ・ドリフトPhonk & 筋トレEDM公式Mix 2026 | 深夜ドライブ・モチベ爆上げ作業用BGM",
        "description": "限界突破！1時間ノンストップ・超重低音Aggressive Drift Phonk & 筋トレEDM公式Mix！⚡\n脳を揺らす重低音ベースと高音質クリスプマスタリングで、筋トレ・深夜ドライブ・作業のモチベーションを最高潮に引き上げます！\n\n#ドリフトフォンク #ジムフォンク #筋トレBGM #作業用BGM #重低音"
    }
}

update_body = {
    "id": VIDEO_ID,
    "snippet": {
        "title": TITLE_EN,
        "description": DESCRIPTION_EN,
        "tags": TAGS,
        "categoryId": "10",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    },
    "localizations": LOCALIZATIONS
}

print("Updating snippet, description, tags, and localizations...")
res = yt.videos().update(part="snippet,localizations", body=update_body).execute()
print(f"✅ Successfully updated video {VIDEO_ID} with Aggressive Drift Metadata!")

# --- Post Pinned Engagement Comment ---
print("\n=== Posting Pinned Engagement Comment ===")
comment_text = """⚡ What track gave you the biggest PR or adrenaline surge in this mix? Drop your favorite timestamp below! ⬇️

🔥 Subscribe to @PhonkForgeAudio for daily non-stop high-energy Phonk & Drift EDM mixes!"""

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
    print(f"✅ Successfully posted engagement comment! (Comment ID: {c_res['id']})")
    print("👉 Please Pin this comment to the top in YouTube Studio.")
except Exception as e:
    print(f"⚠️ Note on comment posting: {e}")
    print("   (If video is set to 'private', set to 'unlisted' or 'public' to enable comments)")

