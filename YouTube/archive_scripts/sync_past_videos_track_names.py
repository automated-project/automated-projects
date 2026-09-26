# -*- coding: utf-8 -*-
"""
Ch 3 過去動画（Vol. 1: o8ygRO9KVuQ, Vol. 2: Tamf2pVElJU）のタイムスタンプおよび概要欄・多言語ローカライズを
今回リネーム・確定した正式な新曲名に完全同期・更新するスクリプト
"""
import sys
import time
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("auramelody")

# ====================================================
# 1. Vol. 1 (o8ygRO9KVuQ) 新曲名タイムスタンプ & メタデータ
# ====================================================
vol1_new_chapters = """00:00 - Timeless Moment
02:56 - Brighter Than Starlight
05:51 - Zero Gravity Drive
08:46 - Crystal Morning Light
11:44 - Starlight Burning Bright
14:37 - Beyond The Horizon
17:09 - Sunlit Atmosphere
20:07 - High Above The Clouds
22:47 - Pure Motion Pulse
25:45 - Infinite Horizons
28:41 - Daylight Anthem
31:39 - Crystal Ocean Breeze
34:29 - Midnight Glow Pulse
37:27 - Golden Euphoria
40:27 - A Thousand Memories
43:27 - Endless Sky Radiance
46:26 - Golden Hour Echoes
49:22 - Ocean Drift Melody
52:20 - Waiting For The Rush
55:20 - Healed By Golden Light
58:18 - Echoes By The Door"""

# チャプターファイルも更新
Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL1_chapters.txt").write_text(vol1_new_chapters, encoding="utf-8")

vol1_title = "✨ [1 HOUR] Euphoric Melodic EDM — Uplifting Progressive House Mix for Energy & Motivation"
vol1_desc = f"""✨ Welcome to AuraMelody Audio — Pure Uplifting Melodic EDM & Progressive House for Energy, Motivation, and Good Vibes.

Immerse yourself in 1 hour of continuous, euphoric progressive melodies inspired by the golden era of melodic festival anthems. Perfect for energy boosts, deep focus, workout, coding, gaming, and night drives.

100% Free & Royalty-Free for Creators! Feel free to use this track in your YouTube videos, live streams, and background projects.

🎵 Tracklist / Timestamps:
{vol1_new_chapters}

🎧 Sound Design & Mastering:
- SoftBass Transparent Mastering (-14.0 LUFS / Crystal Highs & Warm Lows)
- Seamless 2.5s DJ Equal-Power Crossfades

📜 License:
- 100% Free to use for videos, podcasts, and streams.
- Credit appreciated: Music by @AuraMelody-Audio (https://www.youtube.com/@AuraMelody-Audio)

🔥 Subscribe to @AuraMelody-Audio for regular uplifting melodies & festival energy!

#MelodicEDM #ProgressiveHouse #UpliftingEDM #EDMMix #EnergyMusic #FocusMusic #CodingBGM #AuraMelody #1HourMix #FreeBGM
"""

vol1_tags = [
    "melodic edm", "progressive house", "uplifting edm", "euphoric edm", "edm mix 2026",
    "1 hour edm mix", "energy music edm", "coding music", "gaming bgm", "festival vibes",
    "auramelody", "study music", "free bgm edm", "royalty free music edm"
]

vol1_loc = {
    "ru": {
        "title": "✨ [1 ЧАС] Эйфоричный Melodic EDM — Энергичный Progressive House Микс для Мотивации",
        "description": f"✨ 1 час кристально чистого Melodic EDM и Progressive House для энергии, спорта, кодинга и мотивации.\n\n100% Бесплатно для использования в видео и стримах!\n\n🎵 Треклист:\n{vol1_new_chapters}\n\n#МелодикEDM #ПрогрессивХаус #МузыкаДляТренировок #EDM #AuraMelody"
    },
    "pt": {
        "title": "✨ [1 HORA] Euphoric Melodic EDM — Mix de Progressive House para Energia e Motivação",
        "description": f"✨ 1 hora de Melodic EDM e Progressive House para energia, treino, foco e vibe positiva.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol1_new_chapters}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaTreino #EDM #AuraMelody"
    },
    "es": {
        "title": "✨ [1 HORA] Euphoric Melodic EDM — Mix de Progressive House para Energía y Motivación",
        "description": f"✨ 1 hora de Melodic EDM y Progressive House para entrenar, trabajar, programar y llenarte de energía.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol1_new_chapters}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaEntrenar #EDM #AuraMelody"
    },
    "ko": {
        "title": "✨ [1시간] 유포릭 멜로딕 EDM & 프로그레시브 하우스 — 에너지·동기부여·운동을 위한 감성 믹스",
        "description": f"✨ 1시간 연속 재생 감성 멜로딕 EDM & 프로그레시브 하우스! 에너지 충전, 운동, 코딩, 드라이브를 위한 최고의 사운드.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트:\n{vol1_new_chapters}\n\n#멜로딕EDM #프로그레시브하우스 #운동음악 #1시간 #AuraMelody"
    },
    "ja": {
        "title": "✨ [1時間] 多幸感Melodic EDM — モチベーション・集中力を極限まで高めるProgressive House作業用BGM",
        "description": f"✨ 1時間ノンストップ！ 圧倒的な多幸感と疾走感あふれる極上Melodic EDM & Progressive House Mix。\n作業、プログラミング、勉強、ドライブ、ワークアウトに最適な高揚感をお届けします。\n\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可）】です。\n\n🎵 トラックリスト:\n{vol1_new_chapters}\n\n#メロディックEDM #プログレッシブハウス #作業用BGM #勉強用BGM #洋楽EDM #1時間耐久 #フリーBGM #AuraMelody"
    }
}

print("[+] Updating Vol. 1 (o8ygRO9KVuQ) with synchronized new track names...")
yt.videos().update(
    part="snippet,localizations",
    body={
        "id": "o8ygRO9KVuQ",
        "snippet": {
            "title": vol1_title,
            "description": vol1_desc,
            "tags": vol1_tags,
            "categoryId": "10",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "localizations": vol1_loc
    }
).execute()
print("✅ Successfully updated Vol. 1!")
time.sleep(2)


# ====================================================
# 2. Vol. 2 (Tamf2pVElJU) 新曲名タイムスタンプ & メタデータ
# ====================================================
vol2_new_chapters = """00:00 - Amber Horizon
03:02 - Hold The Starlit Night
05:49 - Tear The Clouds
08:36 - Gateway To Light
11:35 - Weightless Ascent
14:35 - Timeless Moment
17:33 - Brighter Than Starlight
20:27 - Zero Gravity Drive
23:22 - Crystal Morning Light
26:17 - Starlight Burning Bright
29:15 - Sunlit Atmosphere
32:08 - Pure Motion Pulse
35:06 - Infinite Horizons
37:45 - Daylight Anthem
40:44 - Midnight Glow Pulse
43:40 - Golden Euphoria
46:38 - Endless Sky Radiance
49:36 - Ocean Drift Melody
52:35 - Crystal Ocean Breeze
55:34 - Golden Hour Echoes
58:31 - Healed By Golden Light"""

# チャプターファイルも更新
Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL2_chapters.txt").write_text(vol2_new_chapters, encoding="utf-8")

vol2_title = "✨ [1 HOUR] Crystal Progressive House — Deep Focus Melodic EDM Mix for Coding & Study"
vol2_desc = f"""✨ Welcome to AuraMelody Audio — Crystal Progressive House & Melodic EDM for Deep Focus, Coding, and Study.

Immerse yourself in 1 hour of clean, hypnotic, and uplifting progressive house melodies. Engineered to enhance concentration, flow state, and productivity.

100% Free & Royalty-Free for Creators! Feel free to use this track in your YouTube videos, live streams, and background projects.

🎵 Tracklist / Timestamps:
{vol2_new_chapters}

🎧 Sound Design & Mastering:
- SoftBass Transparent Mastering (-14.0 LUFS / Crystal Highs & Warm Lows)
- Seamless 2.5s DJ Equal-Power Crossfades

📜 License:
- 100% Free to use for videos, podcasts, and streams.
- Credit appreciated: Music by @AuraMelody-Audio (https://www.youtube.com/@AuraMelody-Audio)

🔥 Subscribe to @AuraMelody-Audio for regular uplifting melodies & festival energy!

#ProgressiveHouse #MelodicEDM #DeepFocus #CodingBGM #StudyMusic #WorkBGM #AuraMelody #1HourMix #FreeBGM
"""

vol2_tags = [
    "progressive house", "melodic edm", "deep focus edm", "coding music", "study music edm",
    "1 hour edm mix", "focus bgm", "crystal edm", "flow state music", "auramelody",
    "free bgm edm", "royalty free music"
]

vol2_loc = {
    "ru": {
        "title": "✨ [1 ЧАС] Кристальный Progressive House — Глубокий Фокус и Melodic EDM для Кодинга и Учебы",
        "description": f"✨ 1 час кристально чистого Progressive House для максимальной концентрации, работы и учебы.\n\n100% Бесплатно для создателей контента!\n\n🎵 Треклист:\n{vol2_new_chapters}\n\n#ПрогрессивХаус #МелодикEDM #МузыкаДляУчебы #Кодинг #AuraMelody"
    },
    "pt": {
        "title": "✨ [1 HORA] Crystal Progressive House — Mix de Melodic EDM para Foco Profundo e Estudo",
        "description": f"✨ 1 hora de Progressive House cristalino para foco total, programação e estudos.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol2_new_chapters}\n\n#ProgressiveHouse #MelodicEDM #MusicaParaEstudar #Foco #AuraMelody"
    },
    "es": {
        "title": "✨ [1 HORA] Crystal Progressive House — Mix de Melodic EDM para Concentración y Estudio",
        "description": f"✨ 1 hora de Progressive House cristalino para máxima concentración, programación y estudio.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol2_new_chapters}\n\n#ProgressiveHouse #MelodicEDM #MusicaParaEstudiar #Concentracion #AuraMelody"
    },
    "ko": {
        "title": "✨ [1시간] 크리스탈 프로그레시브 하우스 — 코딩·공부·초집중을 위한 감성 멜로딕 EDM",
        "description": f"✨ 1시간 연속 재생 맑고 청량한 프로그레시브 하우스! 몰입, 코딩, 공부를 위한 최고의 노동요.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트:\n{vol2_new_chapters}\n\n#프로그레시브하우스 #멜로딕EDM #노동요 #코딩음악 #1시간 #AuraMelody"
    },
    "ja": {
        "title": "✨ [1時間] 澄み渡る美旋律Progressive House — 深い集中とフロー状態へ導く極上作業用BGM",
        "description": f"✨ 1時間ノンストップ！ 美しく洗練された旋律が続く極上Progressive House & Melodic EDM Mix。\nプログラミング、勉強、デスクワーク、読書など深い集中（ゾーン）に入りたい時に最適です。\n\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可）】です。\n\n🎵 トラックリスト:\n{vol2_new_chapters}\n\n#プログレッシブハウス #メロディックEDM #作業用BGM #勉強用BGM #集中BGM #1時間耐久 #フリーBGM #AuraMelody"
    }
}

print("[+] Updating Vol. 2 (Tamf2pVElJU) with synchronized new track names...")
yt.videos().update(
    part="snippet,localizations",
    body={
        "id": "Tamf2pVElJU",
        "snippet": {
            "title": vol2_title,
            "description": vol2_desc,
            "tags": vol2_tags,
            "categoryId": "10",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "localizations": vol2_loc
    }
).execute()
print("✅ Successfully updated Vol. 2!")

print("\n🎉 ALL PAST VIDEOS SYNCHRONIZED WITH NEW TRACK NAMES!")
