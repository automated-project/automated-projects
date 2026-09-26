# -*- coding: utf-8 -*-
"""
第2チャンネル（PhonkForge Audio）Anime Phonk SEO最適化スクリプト
Video ID: KfDXrQ2gmkM
- タイトルに Anime Phonk & Gym Drift を追加
- 各国語ローカライズ（ru, pt, es, ko, ja）に Anime Phonk キーワードを注入
- 検索タグに anime phonk, anime gym phonk, brazilian anime phonk 等を追加
"""
import sys
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

VIDEO_ID = "KfDXrQ2gmkM"

print(f"=== Applying Anime Phonk SEO Metadata to Video: {VIDEO_ID} on PhonkForge Audio ===")
yt = get_youtube_service("phonkforge")

# 1. 最適化タグ
TAGS = [
    "gym phonk", "anime phonk", "drift phonk", "anime gym phonk", "heavy bass",
    "workout music", "hardstyle", "brazilian phonk", "phonk 2026", "phonk mix 1 hour",
    "gym workout edm", "anime workout", "super crisp phonk", "phonkforge"
]

# 2. 既存スニペット取得
video_res = yt.videos().list(part="snippet,localizations", id=VIDEO_ID).execute()
item = video_res["items"][0]
existing_desc = item["snippet"].get("description", "")
category_id = item["snippet"].get("categoryId", "10")

# 3. 英語メインタイトル
title_en = "🔥 [1 HOUR] Heavy Bass Anime Gym Phonk & Drift EDM Mix 2026 | Super Crisp Workout Set"

# 4. 各国語ローカライズ
LOCALIZATIONS = {
    "ru": {
        "title": "🔥 [1 ЧАС] Аниме Дрифт Фонк и Тяжелый Басс Микс 2026 | Мощная Музыка для Качалки",
        "description": "Погрузитесь в абсолютную энергию с этим 1-часовым Anime Gym Phonk и Drift EDM сетом! ⚡\nТяжелый бас, агрессивный ритм и кристальное сведение для максимального пампа на тренировке.\n\n#AnimePhonk #GymPhonk #DriftPhonk #Фонк"
    },
    "pt": {
        "title": "🔥 [1 HORA] Anime Gym Phonk & Heavy Bass Drift EDM Mix 2026 | Treino Pesado",
        "description": "Sinta a energia máxima com este mix de 1 hora de Anime Gym Phonk e Drift EDM! ⚡\nGraves pesados, ritmo insano e masterização nítida para quebrar seus recordes na academia.\n\n#AnimePhonk #GymPhonk #DriftPhonk #Treino"
    },
    "es": {
        "title": "🔥 [1 HORA] Anime Gym Phonk & Heavy Bass Drift EDM Mix 2026 | Música para Entrenar",
        "description": "¡Desata tu verdadero potencial con este mix de 1 hora de Anime Gym Phonk y Drift EDM! ⚡\nBajos demoledores, ritmo agresivo y masterización cristalina para entrenar al límite.\n\n#AnimePhonk #GymPhonk #DriftPhonk #Entrenamiento"
    },
    "ko": {
        "title": "🔥 [1시간] 애니 짐 폰크 & 하이퍼 드리프트 EDM 믹스 2026 | 초고음질 헬스 노동요",
        "description": "한계를 뛰어넘는 초고음질 Anime Gym Phonk & Drift EDM 1시간 연속 믹스! ⚡\n묵직한 중저음과 압도적인 텐션으로 헬스장 PR 갱신을 위한 최고의 트랙!\n\n#애니폰크 #짐폰크 #드리프트폰크 #헬스음악 #노동요"
    },
    "ja": {
        "title": "🔥【1時間】超重低音アニメGym Phonk & ドリフトEDM公式Mix 2026 | 筋トレ・モチベ爆上げ作業用BGM",
        "description": "限界突破！1時間ノンストップ・超重低音Anime Gym Phonk & ドリフトEDM公式Mix！⚡\n脳を揺らす重低音ベースと高音質クリスプマスタリングで、筋トレ・ドライブ・作業のモチベーションを最高潮に引き上げます！\n\n#アニメフォンク #ジムフォンク #ドリフトフォンク #筋トレBGM #作業用BGM"
    }
}

update_body = {
    "id": VIDEO_ID,
    "snippet": {
        "title": title_en,
        "description": existing_desc,
        "tags": TAGS,
        "categoryId": category_id,
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    },
    "localizations": LOCALIZATIONS
}

print("Updating snippet and localizations with Anime Phonk keywords...")
res = yt.videos().update(part="snippet,localizations", body=update_body).execute()
print("✅ Successfully updated video with Anime Phonk SEO keywords!")
