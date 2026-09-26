# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) 日本語＆各言語タイトル 市場標準ワード修正スクリプト
- 「ウーファーが震える」等の不自然なポエム表現を完全排除
- YouTube市場で実際に数百万回検索・再生されている定番ワードに修正：
  - JA: 【超重低音】夜のドライブ用 ドリフトPhonk作業用BGM | 筋トレ・テンション爆上げ
  - KO: 【초중저음】 심야 드라이브용 드리프트 폰크 노동요 | 헬스·운동 BGM
"""

import sys
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("phonkforge")
v_id = "4aJlGEfEI84"

title_en = "🔥 [1 HOUR] Car Audio Heavy Bass — Subwoofer Drift Phonk & Night Drive Mix"
desc_en = """🔥 Welcome to PhonkForge Audio — Extreme Sub-Bass Car Music, Drift Phonk & Night Drive Anthems.

1 Hour Non-Stop Heavy Bass Car Audio Mix — Extreme Sub-Bass Drift Phonk & Aggressive Gym Workout Beats.
Engineered with Super Crisp deep sub-bass frequencies (35Hz-55Hz) specifically tuned for car subwoofers, heavy workout sets, and high-speed night drives.

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
🌿 Sister Channels:
🍃 Ghibli Nostalgic Lofi ➡️ @komorebi-chill-audio (https://www.youtube.com/@komorebi-chill-audio)
✨ Uplifting Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Subscribe to @phonkforgeaudio-s1h for daily heavy bass car audio mixes!
"""

localizations = {
    "ja": {
        "title": "🔥【超重低音】夜のドライブ用 ドリフトPhonk作業用BGM | 筋トレ・テンション爆上げ（1時間）",
        "description": "🔥 車載オーディオ・重低音イヤホン推奨。1時間ノンストップ・超重低音ドリフトPhonk。\n夜のドライブ、筋トレ、集中作業のモチベーションアップに最適なトラック集です。\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🌿 姉妹チャンネル:\n🍃 ジブリ風作業用Lofi ➡️ @komorebi-chill-audio (https://www.youtube.com/@komorebi-chill-audio)\n✨ 爽快Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    },
    "es": {
        "title": "🔥 [1 HORA] Música de Bajos Pesados para Coche — Drift Phonk para Conducir de Noche y Entrenar",
        "description": "🔥 1 hora de bajos pesados y Drift Phonk para coche y entrenamientos intensos."
    },
    "pt": {
        "title": "🔥 [1 HORA] Som Automotivo Grave Pesado — Drift Phonk para Racha e Treino",
        "description": "🔥 1 hora de subgraves pesados para som automotivo e treinos pesados."
    },
    "ru": {
        "title": "🔥 [1 ЧАС] Мощный Бас в Машину — Дрифт Фонк для Ночной Езды и Тренировок",
        "description": "🔥 1 час мощного сабвуферного баса и дрифт-фонка для поездок и качалки."
    },
    "ko": {
        "title": "🔥 [1시간] 극저음 카오디오 베이스 — 심야 드라이브용 드리프트 폰크 & 헬스 노동요",
        "description": "🔥 카오디오 및 헤드폰 전용 극저음 헤비 폰크 1시간 믹스! 심야 드라이브와 헬스장 운동에 최적화된 사운드입니다."
    }
}

yt.videos().update(
    part="snippet,localizations",
    body={
        "id": v_id,
        "snippet": {
            "title": title_en,
            "description": desc_en,
            "categoryId": "10",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
            "tags": ["car audio heavy bass", "drift phonk", "night drive music", "gym phonk", "phonkforge"]
        },
        "localizations": localizations
    }
).execute()

# Shortsの日本語タイトルも市場標準ワードに修正
shorts_updates = {
    "W7yzwdh1vdQ": {
        "ja_title": "⚡【超重低音】アグレッシブ・ドリフトPhonkドロップ #Shorts #筋トレ #ドライブ",
        "ko_title": "⚡【극저음】 심장 때리는 드리프트 폰크 드롭 #Shorts #헬스 #드라이브"
    },
    "uBwoMrx4EPU": {
        "ja_title": "⚡【夜ドライブ用】爆音ドリフトPhonk（16秒無限ループ）#Shorts #筋トレ",
        "ko_title": "⚡【심야 드라이브】 아드레날린 드리프트 폰크 (16초 루프) #Shorts"
    }
}

for s_id, s_data in shorts_updates.items():
    s_res = yt.videos().list(part="snippet,localizations", id=s_id).execute()
    if s_res["items"]:
        item = s_res["items"][0]
        locs = item.get("localizations", {})
        if "ja" in locs:
            locs["ja"]["title"] = s_data["ja_title"]
        if "ko" in locs:
            locs["ko"]["title"] = s_data["ko_title"]
        yt.videos().update(
            part="localizations",
            body={
                "id": s_id,
                "localizations": locs
            }
        ).execute()
        print(f"Updated Shorts {s_id} localization")

print("Successfully updated Ch 2 metadata with standard market vocabulary!")
