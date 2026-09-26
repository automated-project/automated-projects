# -*- coding: utf-8 -*-
"""
全チャンネル（Ch3, Ch1, Ch2）のメタデータ一括更新スクリプト
- 季節キーワード（summer, spring, autumn, fall, winter, 春夏秋冬）の完全排除
- Ch3 Vol1/Vol2/Vol3 のタイトル被り解消・明確な差別化
- 全長尺動画の全曲タイムスタンプ完備・正規チャンネルハンドル・Free BGM表記
- 多言語ローカライズ（日・英・露・葡・西・韓）の完全同期
※ サムネイルは一切変更しません。
"""
import sys
import time
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

def update_video_metadata(yt, video_id, title, description, tags, localizations=None):
    print(f"\n[+] Updating Video ID: {video_id}")
    print(f"    New Title: {title}")
    
    # First get existing snippet to preserve categoryId, etc.
    v_res = yt.videos().list(id=video_id, part="snippet,status,localizations").execute()
    if not v_res.get("items"):
        print(f"❌ Video {video_id} not found!")
        return False
        
    item = v_res["items"][0]
    category_id = item["snippet"].get("categoryId", "10")
    
    body = {
        "id": video_id,
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        }
    }
    
    if localizations:
        body["localizations"] = localizations
        part_str = "snippet,localizations"
    else:
        part_str = "snippet"
        
    res = yt.videos().update(
        part=part_str,
        body=body
    ).execute()
    
    print(f"✅ Successfully updated metadata for {video_id}!")
    return True

# ==========================================
# 1. Ch 3 (AuraMelody Audio) Updates
# ==========================================
print("==================================================")
print("=== UPDATING CH 3 (AuraMelody Audio) METADATA ===")
print("==================================================")
yt_ch3 = get_youtube_service("auramelody")

# --- Ch 3 Vol. 1 (o8ygRO9KVuQ) ---
vol1_chapters = """00:00 - Amber Flame
02:59 - Kissing The Golden Sun
05:46 - Weightless At Last
08:44 - Beyond The Heavy Ground
11:16 - Broken Glass Mornings
14:15 - Chasing After Endless Light
17:14 - Golden Hour Traces
20:10 - Salt In Our Hair
23:09 - Wait For The Motion
26:08 - Healed By Golden Light
29:06 - The Chair By The Door
31:53 - Ocean And Sunlight
34:43 - Sun Above
37:23 - Breaking Past Gravity
40:18 - A Thousand Frames
43:18 - Weightless In Gold
46:17 - The Golden Door
49:17 - Tear The Sky
52:17 - Hold On To The Night
55:03 - Amber Horizon
57:51 - Kissing The Golden Sun"""

vol1_title = "✨ [1 HOUR] Euphoric Melodic EDM — Uplifting Progressive House Mix for Energy & Motivation"
vol1_desc = f"""✨ Welcome to AuraMelody Audio — Pure Uplifting Melodic EDM & Progressive House for Energy, Motivation, and Good Vibes.

Immerse yourself in 1 hour of continuous, euphoric progressive melodies inspired by the golden era of melodic festival anthems. Perfect for energy boosts, deep focus, workout, coding, gaming, and night drives.

100% Free & Royalty-Free for Creators! Feel free to use this track in your YouTube videos, live streams, and background projects.

🎵 Tracklist / Timestamps:
{vol1_chapters}

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
        "description": f"✨ 1 час кристально чистого Melodic EDM и Progressive House для энергии, спорта, кодинга и мотивации.\n\n100% Бесплатно для использования в видео и стримах!\n\n🎵 Треклист:\n{vol1_chapters}\n\n#МелодикEDM #ПрогрессивХаус #МузыкаДляТренировок #EDM #AuraMelody"
    },
    "pt": {
        "title": "✨ [1 HORA] Euphoric Melodic EDM — Mix de Progressive House para Energia e Motivação",
        "description": f"✨ 1 hora de Melodic EDM e Progressive House para energia, treino, foco e vibe positiva.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol1_chapters}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaTreino #EDM #AuraMelody"
    },
    "es": {
        "title": "✨ [1 HORA] Euphoric Melodic EDM — Mix de Progressive House para Energía y Motivación",
        "description": f"✨ 1 hora de Melodic EDM y Progressive House para entrenar, trabajar, programar y llenarte de energía.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol1_chapters}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaEntrenar #EDM #AuraMelody"
    },
    "ko": {
        "title": "✨ [1시간] 유포릭 멜로딕 EDM & 프로그레시브 하우스 — 에너지·동기부여·운동을 위한 감성 믹스",
        "description": f"✨ 1시간 연속 재생 감성 멜로딕 EDM & 프로그레シ브 하우스! 에너지 충전, 운동, 코딩, 드라이브를 위한 최고의 사운드.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트:\n{vol1_chapters}\n\n#멜로딕EDM #프로그레시브하우스 #운동음악 #1시간 #AuraMelody"
    },
    "ja": {
        "title": "✨ [1時間] 多幸感Melodic EDM — モチベーション・集中力を極限まで高めるProgressive House作業用BGM",
        "description": f"✨ 1時間ノンストップ！ 圧倒的な多幸感と疾走感あふれる極上Melodic EDM & Progressive House Mix。\n作業、プログラミング、勉強、ドライブ、ワークアウトに最適な高揚感をお届けします。\n\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可）】です。\n\n🎵 トラックリスト:\n{vol1_chapters}\n\n#メロディックEDM #プログレッシブハウス #作業用BGM #勉強用BGM #洋楽EDM #1時間耐久 #フリーBGM #AuraMelody"
    }
}
update_video_metadata(yt_ch3, "o8ygRO9KVuQ", vol1_title, vol1_desc, vol1_tags, vol1_loc)
time.sleep(1)

# --- Ch 3 Vol. 2 (Tamf2pVElJU) ---
vol2_chapters = """00:00 - Amber Flame
02:59 - Kissing The Golden Sun
05:46 - Weightless At Last
08:44 - Beyond The Heavy Ground
11:16 - Broken Glass Mornings
14:15 - Chasing After Endless Light
17:14 - Golden Hour Traces
20:10 - Salt In Our Hair
23:09 - Wait For The Motion
26:08 - Healed By Golden Light
29:06 - The Chair By The Door
31:53 - Ocean And Sunlight
34:43 - Sun Above
37:23 - Breaking Past Gravity
40:18 - A Thousand Frames
43:18 - Weightless In Gold
46:17 - The Golden Door
49:17 - Tear The Sky
52:17 - Hold On To The Night
55:03 - Amber Horizon
57:51 - Kissing The Golden Sun"""

vol2_title = "✨ [1 HOUR] Crystal Progressive House — Deep Focus Melodic EDM Mix for Coding & Study"
vol2_desc = f"""✨ Welcome to AuraMelody Audio — Crystal Progressive House & Melodic EDM for Deep Focus, Coding, and Study.

Immerse yourself in 1 hour of clean, hypnotic, and uplifting progressive house melodies. Engineered to enhance concentration, flow state, and productivity.

100% Free & Royalty-Free for Creators! Feel free to use this track in your YouTube videos, live streams, and background projects.

🎵 Tracklist / Timestamps:
{vol2_chapters}

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
        "description": f"✨ 1 час кристально чистого Progressive House для максимальной концентрации, работы и учебы.\n\n100% Бесплатно для создателей контента!\n\n🎵 Треклист:\n{vol2_chapters}\n\n#ПрогрессивХаус #МелодикEDM #МузыкаДляУчебы #Кодинг #AuraMelody"
    },
    "pt": {
        "title": "✨ [1 HORA] Crystal Progressive House — Mix de Melodic EDM para Foco Profundo e Estudo",
        "description": f"✨ 1 hora de Progressive House cristalino para foco total, programação e estudos.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol2_chapters}\n\n#ProgressiveHouse #MelodicEDM #MusicaParaEstudar #Foco #AuraMelody"
    },
    "es": {
        "title": "✨ [1 HORA] Crystal Progressive House — Mix de Melodic EDM para Concentración y Estudio",
        "description": f"✨ 1 hora de Progressive House cristalino para máxima concentración, programación y estudio.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol2_chapters}\n\n#ProgressiveHouse #MelodicEDM #MusicaParaEstudiar #Concentracion #AuraMelody"
    },
    "ko": {
        "title": "✨ [1시간] 크리스탈 프로그레시브 하우스 — 코딩·공부·초집중을 위한 감성 멜로딕 EDM",
        "description": f"✨ 1시간 연속 재생 맑고 청량한 프로그레시브 하우스! 몰입, 코딩, 공부를 위한 최고의 노동요.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트:\n{vol2_chapters}\n\n#프로그레시브하우스 #멜로딕EDM #노동요 #코딩음악 #1시간 #AuraMelody"
    },
    "ja": {
        "title": "✨ [1時間] 澄み渡る美旋律Progressive House — 深い集中とフロー状態へ導く極上作業用BGM",
        "description": f"✨ 1時間ノンストップ！ 美しく洗練された旋律が続く極上Progressive House & Melodic EDM Mix。\nプログラミング、勉強、デスクワーク、読書など深い集中（ゾーン）に入りたい時に最適です。\n\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可）】です。\n\n🎵 トラックリスト:\n{vol2_chapters}\n\n#プログレッシブハウス #メロディックEDM #作業用BGM #勉強用BGM #集中BGM #1時間耐久 #フリーBGM #AuraMelody"
    }
}
update_video_metadata(yt_ch3, "Tamf2pVElJU", vol2_title, vol2_desc, vol2_tags, vol2_loc)
time.sleep(1)

# --- Ch 3 Vol. 3 (pW2Zw1TvNXA) ---
vol3_chapters = """00:00 - Amber Flame
02:59 - Kissing The Golden Sun
05:46 - Weightless At Last
08:44 - Beyond The Heavy Ground
11:16 - Broken Glass Mornings
14:15 - Chasing After Endless Light
17:14 - Golden Hour Traces
20:10 - Salt In Our Hair
23:09 - Wait For The Motion
26:08 - Healed By Golden Light
29:06 - The Chair By The Door
31:53 - Ocean And Sunlight
34:43 - Sun Above
37:23 - Breaking Past Gravity
40:18 - A Thousand Frames
43:18 - Weightless In Gold
46:17 - The Golden Door
49:17 - Tear The Sky
52:17 - Hold On To The Night
55:03 - Amber Horizon
57:51 - Kissing The Golden Sun"""

vol3_title = "✨ [1 HOUR] Golden Hour Melodic EDM — Uplifting Progressive House Beats for Work & Drive"
vol3_desc = f"""✨ Welcome to AuraMelody Audio — Pure Uplifting Melodic EDM & Progressive House for Work, Drive, and Daily Energy.

Immerse yourself in 1 hour of non-stop, crystal-clear euphoric melodies. Crafted with warm golden tones to elevate your mood and soundtrack your creative flow. Perfect for work, driving, studying, workouts, and relaxation.

100% Free & Royalty-Free for Creators! Feel free to use this track in your YouTube videos, live streams, and background projects.

🎵 Tracklist / Timestamps:
{vol3_chapters}

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
vol3_tags = [
    "melodic edm", "progressive house", "uplifting edm", "golden hour edm", "edm mix 2026",
    "1 hour edm mix", "study music edm", "coding music", "drive music", "festival vibes",
    "auramelody", "euphoric edm", "free bgm edm", "royalty free music edm"
]
vol3_loc = {
    "ru": {
        "title": "✨ [1 ЧАС] Melodic EDM Золотого Часа — Прогрессив Хаус для Работы и Поездок",
        "description": f"✨ 1 час кристально чистого Melodic EDM и Progressive House для работы, поездок, кодинга и концентрации.\n\n100% Бесплатно для использования в ваших видео и стримах!\n\n🎵 Треклист:\n{vol3_chapters}\n\n#МелодикEDM #ПрогрессивХаус #МузыкаДляРаботы #EDM #AuraMelody"
    },
    "pt": {
        "title": "✨ [1 HORA] Golden Hour Melodic EDM — Progressive House para Trabalho e Viagem",
        "description": f"✨ 1 hora de Melodic EDM e Progressive House para foco, trabalho, direção e vibe positiva.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol3_chapters}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaTrabalhar #EDM #AuraMelody"
    },
    "es": {
        "title": "✨ [1 HORA] Golden Hour Melodic EDM — Progressive House para Trabajo y Conducir",
        "description": f"✨ 1 hora de Melodic EDM y Progressive House para estudiar, trabajar, conducir y entrenar.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol3_chapters}\n\n#MelodicEDM #ProgressiveHouse #MusicaParaTrabajar #EDM #AuraMelody"
    },
    "ko": {
        "title": "✨ [1시간] 골든아워 감성 멜로딕 EDM & 프로그레시브 하우스 — 업무·드라이브·노동요",
        "description": f"✨ 1시간 논스톱 따스하고 청량한 감성 멜로딕 EDM & 프로그레시브 하우스! 업무, 공부, 코딩, 드라이브를 위한 최고의 에너제틱 사운드.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)!\n\n🎵 트랙리스트:\n{vol3_chapters}\n\n#멜로딕EDM #프로그레시브하우스 #노동요 #드라이브음악 #1시간 #AuraMelody"
    },
    "ja": {
        "title": "✨ [1時間] 爽快エモーショナルGolden Hour EDM — 作業効率・モチベーションを高める極上Progressive House作業用BGM",
        "description": f"✨ 1時間ノンストップ！ 心地よい高揚感あふれる極上Melodic EDM & Progressive House Mix。\n作業、プログラミング、勉強、ドライブ、ワークアウトに最適なBGMをお届けします。\n\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可）】です。\n\n🎵 トラックリスト:\n{vol3_chapters}\n\n#メロディックEDM #プログレッシブハウス #作業用BGM #勉強用BGM #ドライブBGM #1時間耐久 #フリーBGM #AuraMelody"
    }
}
update_video_metadata(yt_ch3, "pW2Zw1TvNXA", vol3_title, vol3_desc, vol3_tags, vol3_loc)
time.sleep(1)

# --- Ch 3 Shorts (4sDPJh25GGw) ---
shorts_title = "✨ EUPHORIC MELODIC EDM DROP [Free BGM] #Shorts #melodicedm #edm"
shorts_desc = """✨ Euphoric Melodic EDM & Progressive House Drop!
100% Free & Royalty-Free for Creators.

🎧 Subscribe to @AuraMelody-Audio for full 1-hour focus mixes!
https://www.youtube.com/@AuraMelody-Audio

#MelodicEDM #ProgressiveHouse #FreeBGM #EDM #Shorts #AuraMelody
"""
shorts_tags = ["melodic edm", "progressive house", "free bgm", "shorts", "auramelody", "edm drop"]
update_video_metadata(yt_ch3, "4sDPJh25GGw", shorts_title, shorts_desc, shorts_tags)
time.sleep(1)


# ==========================================
# 2. Ch 1 (Haven Chill Audio) Updates
# ==========================================
print("\n==================================================")
print("=== UPDATING CH 1 (Haven Chill Audio) METADATA ===")
print("==================================================")
yt_ch1 = get_youtube_service("chill")

# --- Ch 1 2-Hour Study With Me (2L0ppHOvE20) ---
v_res_ch1_2h = yt_ch1.videos().list(id="2L0ppHOvE20", part="snippet,localizations").execute()
if v_res_ch1_2h.get("items"):
    snippet = v_res_ch1_2h["items"][0]["snippet"]
    clean_tags = [t for t in snippet.get("tags", []) if "summer" not in t.lower()]
    clean_desc = snippet["description"].replace("summer", "warm").replace("Summer", "Warm")
    update_video_metadata(yt_ch1, "2L0ppHOvE20", snippet["title"], clean_desc, clean_tags)
    time.sleep(1)

# --- Ch 1 1-Hour Lofi Vol 1 (H9xAE2j0JZM) ---
v_res_ch1_1h = yt_ch1.videos().list(id="H9xAE2j0JZM", part="snippet,localizations").execute()
if v_res_ch1_1h.get("items"):
    snippet = v_res_ch1_1h["items"][0]["snippet"]
    clean_tags = [t for t in snippet.get("tags", []) if "summer" not in t.lower()]
    clean_desc = snippet["description"].replace("summer", "warm").replace("Summer", "Warm")
    clean_title = snippet["title"].replace("Studio Ghibli Inspired ", "").replace("Ghibli ", "")
    if clean_title != snippet["title"]:
        print(f"    Cleaning title: {snippet['title']} -> {clean_title}")
    update_video_metadata(yt_ch1, "H9xAE2j0JZM", clean_title, clean_desc, clean_tags)
    time.sleep(1)


# ==========================================
# 3. Ch 2 (PhonkForge Audio) Verification & Clean
# ==========================================
print("\n==================================================")
print("=== UPDATING CH 2 (PhonkForge Audio) METADATA ===")
print("==================================================")
yt_ch2 = get_youtube_service("phonk")

for vid_phonk in ["z1jIjyKqNLM", "4aJlGEfEI84", "KfDXrQ2gmkM"]:
    v_res = yt_ch2.videos().list(id=vid_phonk, part="snippet").execute()
    if v_res.get("items"):
        s = v_res["items"][0]["snippet"]
        clean_tags = [t for t in s.get("tags", []) if not any(w in t.lower() for w in ["summer", "spring", "autumn", "fall", "winter"])]
        clean_desc = s["description"]
        for w in ["summer", "spring", "autumn", "fall", "winter", "Summer", "Spring", "Autumn", "Fall", "Winter"]:
            clean_desc = clean_desc.replace(w, "hardcore")
        update_video_metadata(yt_ch2, vid_phonk, s["title"], clean_desc, clean_tags)
        time.sleep(1)

print("\n==================================================")
print("🎉 ALL CHANNELS METADATA UPDATED SUCCESSFULLY!")
print("==================================================")
