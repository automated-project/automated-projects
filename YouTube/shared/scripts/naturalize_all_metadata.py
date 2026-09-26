# -*- coding: utf-8 -*-
"""
全チャンネル・全動画 メタデータ完全自然化＆チープワード排除スクリプト
- 修正方針:
  1. 直訳・英語丸投げ（Car Audio Bass Boosted等）を完全排除し、各言語のネイティブが日常で使う自然な表現に意訳。
  2. 「2026」「公式」「Official」「最新版」等のチープなワードを全言語・全動画から完全永久排除。
"""

import sys
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

def sync_ch1_lofi(yt):
    print("▶ Syncing Ch 1: Komorebi Chill Audio...")
    
    # 1. 1Hour Lofi (H9xAE2j0JZM)
    v_id = "H9xAE2j0JZM"
    title_en = "🍃 [1 HOUR] Studio Ghibli Inspired Chill Lofi — Nostalgic Beats for Study, Work & Sleep"
    desc_en = """🍃 Welcome to Komorebi Chill Audio — Studio Ghibli inspired nostalgic chill lofi beats for deep focus, studying, working, reading, and relaxing sleep.

Immerse yourself in 1 hour of warm acoustic guitars, soft upright piano melodies, and gentle vinyl tape textures. Designed to create a cozy, stress-free atmosphere.

🎵 Tracklist:
00:00 - Coffee By The Window
02:46 - Fields Of Amber Light
05:45 - Lanterns On The River
08:39 - Late October Afternoon
11:35 - Leaving The Window Open
14:33 - Letters By The Window
17:33 - Midnight Wool Blanket
20:22 - Paper Boats On The Canal
23:17 - Paper Cranes And Rain
26:12 - Platform Five At Sunset
28:40 - Platform At Dusk
31:37 - Porchlight At Midnight
34:05 - Portrait Of Rainy Hours
37:07 - Summer Porch At Twilight
40:02 - Sunday Morning Stream
42:56 - Sunlight Through The Blinds
45:52 - The Garden At Dawn
48:45 - The Last Page Turned
51:47 - Tokyo Window Seat
54:43 - Under The Canopy
57:44 - Window Seat View

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 Looking for our Heavy Bass or Melodic EDM mixes?
🔥 Heavy Bass & Gym Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)
✨ Pure Uplifting Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe to @komorebi-chill-audio for daily cozy study sessions.
"""
    localizations = {
        "ja": {
            "title": "🍃【1時間】ジブリ風ノスタルジック作業用BGM — 勉強・仕事・読書・睡眠用 癒やしのピアノ＆アコースティックChill Lofi",
            "description": "🍃 1時間ノンストップ。ジブリの世界観を思わせる、温かいアコースティックギターとピアノのノスタルジックなLofi Mix。\n勉強や仕事、読書、カフェ作業、そして夜の睡眠導入に心地よい時間をお届けします。\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🚨 重低音・EDM楽曲をお探しの方はこちらへ移転しました:\n🔥 重低音 & 筋トレPhonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)\n✨ 爽快Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        },
        "es": {
            "title": "🍃 [1 HORA] Lofi Relajante Inspirado en Studio Ghibli — Música para Estudiar, Trabajar y Dormir",
            "description": "🍃 1 hora de música Lofi acústica y nostálgica inspirada en Studio Ghibli para máxima concentración, lectura y descanso profundo.\n\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
        },
        "pt": {
            "title": "🍃 [1 HORA] Lofi Relaxante Inspirado no Studio Ghibli — Música para Estudar, Trabalhar e Dormir",
            "description": "🍃 1 hora de Lofi acústico e nostálgico inspirado no Studio Ghibli para foco profundo, leitura e sono tranquilo.\n\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
        },
        "ru": {
            "title": "🍃 [1 ЧАС] Уютный Лофай в стиле Студии Гибли — Музыка для Учебы, Работы и Сна",
            "description": "🍃 1 час спокойного и ностальгического Lo-Fi в стиле Студии Гибли для глубокой концентрации, чтения и крепкого сна.\n\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
        },
        "ko": {
            "title": "🍃 [1시간] 지브리 감성 힐링 로파이 — 공부할 때 듣는 음악, 잔잔한 독서 & 수면 BGM",
            "description": "🍃 1시간 연속 재생 지브리 감성 칠 로파이 비트. 깊은 집중, 독서, 편안한 수면을 위한 따뜻한 피아노와 어쿠스틱 사운드입니다.\n\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
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
                "tags": ["lofi", "chill lofi", "ghibli lofi", "study music", "lofi hip hop", "sleep music", "1 hour lofi"]
            },
            "localizations": localizations
        }
    ).execute()
    print("  ✓ Ch 1 Vol 1 updated.")

    # 2. 残した2本のEDM (lnJBDZszKCE & bFLKzlSiq4o)
    promo_desc = """🚨 【IMPORTANT NOTICE / チャンネル移転のお知らせ】
All Heavy Bass, Drift Phonk & Gym EDM tracks have officially moved to our new dedicated sister channels!
🔥 Heavy Bass & Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)
✨ Pure Uplifting Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Non-Stop Heavy Gym Phonk & Hardstyle EDM Workout Motivation!
Mastered for maximum adrenaline, heavy deadlifts, PR sets, and high-speed night drives.

🔥 Subscribe to @phonkforgeaudio-s1h for daily gym mixes!
"""
    promo_loc = {
        "ja": {
            "title": "🔥【作業・筋トレ用】超重低音Phonk & ハードスタイルEDM — テンション・集中力爆上げBGM",
            "description": "🚨 重低音・EDM楽曲は専門チャンネルへ完全移転いたしました！\n🔥 重低音 & Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)\n✨ 爽快Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)"
        },
        "es": {
            "title": "🔥 Heavy Gym Phonk & Hardstyle EDM — Música Potente para Entrenar y Motivarse",
            "description": "🚨 ¡Los mixes de Heavy Bass y EDM se han mudado a nuestros nuevos canales!\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
        },
        "pt": {
            "title": "🔥 Heavy Gym Phonk & Hardstyle EDM — Treino Pesado e Foco Extremo",
            "description": "🚨 As faixas de Heavy Bass e EDM mudaram para novos canais!\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
        },
        "ru": {
            "title": "🔥 Heavy Gym Phonk & Hardstyle EDM — Мощная Музыка для Тренировок и Драйва",
            "description": "🚨 Все треки Heavy Bass и Phonk переехали на новые каналы!\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
        },
        "ko": {
            "title": "🔥 헬스장 전용 하이퍼 짐 폰크 & 하드스타일 EDM — 텐션 폭발 운동 노동요",
            "description": "🚨 모든 Phonk 및 EDM 트랙은 전용 채널로 이전되었습니다!\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio"
        }
    }
    for vid, t_en in [("lnJBDZszKCE", "🔥 [50 MIN] Heavy Gym Phonk & Hardstyle EDM — High-Energy Workout & Gaming Music"),
                      ("bFLKzlSiq4o", "🔥 [20 MIN] Heavy Gym & Gaming EDM Motivation — Aggressive Phonk & Heavy Bass")]:
        yt.videos().update(
            part="snippet,localizations",
            body={
                "id": vid,
                "snippet": {
                    "title": t_en,
                    "description": promo_desc,
                    "categoryId": "10",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en",
                    "tags": ["gym phonk", "drift phonk", "workout music", "hardstyle edm", "heavy bass"]
                },
                "localizations": promo_loc
            }
        ).execute()
        print(f"  ✓ Ch 1 Promo {vid} updated.")

def sync_ch2_phonk(yt):
    print("▶ Syncing Ch 2: PhonkForge Audio...")
    
    # 1. 1Hour Car Audio Mix (4aJlGEfEI84)
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
            "title": "🔥【1時間】ウーファーが震える超重低音 — 深夜ドライブ＆筋トレ用 爆音ドリフトPhonk作業用BGM",
            "description": "🔥 車載ウーファーや重低音ヘッドホン専用。1時間ノンストップで脳と身体を揺らす極上重低音Drift Phonk。\n深夜のドライブや筋トレ、集中作業のテンションを一気に限界まで引き上げます。\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🌿 姉妹チャンネル:\n🍃 ジブリ風作業用Lofi ➡️ @komorebi-chill-audio (https://www.youtube.com/@komorebi-chill-audio)\n✨ 爽快Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        },
        "es": {
            "title": "🔥 [1 HORA] Bajos Pesados para Coche — Drift Phonk Extremo para Conducir de Noche y Entrenar",
            "description": "🔥 1 hora de bajos demoledores para subwoofer y coche. Drift Phonk agresivo para máxima adrenalina al volante y en el gimnasio."
        },
        "pt": {
            "title": "🔥 [1 HORA] Grave Pesado para Som Automotivo — Drift Phonk Insano para Racha e Treino",
            "description": "🔥 1 hora de subgraves pesados para som automotivo e subwoofers. Drift Phonk potente para treinos e direção noturna."
        },
        "ru": {
            "title": "🔥 [1 ЧАС] Экстремальный Бас в Авто — Тяжелый Дрифт Фонк для Сабвуфера и Качалки",
            "description": "🔥 1 час мощного сабвуферного баса и агрессивного дрифт-фонка для ночных поездок и тренировок."
        },
        "ko": {
            "title": "🔥 [1시간] 우퍼를 울리는 극저음 카오디오 — 심장 뛰는 드리프트 폰크 & 드라이브 노동요",
            "description": "🔥 카오디오 서브우퍼 및 헤드폰 전용 극저음 헤비 폰크 믹스! 드라이브와 헬스장에서 심장을 울리는 타격감을 선사합니다."
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
                "tags": ["car audio heavy bass", "subwoofer test", "drift phonk", "night drive music", "gym phonk", "phonkforge"]
            },
            "localizations": localizations
        }
    ).execute()
    print("  ✓ Ch 2 Vol 1 updated.")

    # 2. Shorts
    shorts_loc = {
        "W7yzwdh1vdQ": {
            "title_en": "⚡ ASPHALT REDLINE — Extreme Sub-Bass Drift Phonk Drop #Shorts #GymPhonk #DriftPhonk",
            "loc": {
                "ja": {"title": "⚡ 脳を揺らす超重低音ドリフトPhonkドロップ #Shorts #筋トレ #ドライブ", "description": "⚡ 身体の芯を震わせる超重低音！1時間フルMixは関連動画から視聴できます。"},
                "es": {"title": "⚡ Drop de Bajos Pesados para Coche #Shorts #DriftPhonk", "description": "⚡ Drift Phonk potente. Mix completo de 1 hora en video relacionado."},
                "pt": {"title": "⚡ Drop Insano de Grave Automotivo #Shorts #DriftPhonk", "description": "⚡ Subgraves insanos! Mix de 1 hora no vídeo relacionado."},
                "ru": {"title": "⚡ Мощнейший Бас Дроп Фонк #Shorts #Фонк", "description": "⚡ Экстремальный бас! Полный 1-часовой микс в связанном видео."},
                "ko": {"title": "⚡ 심장 폭격 극저음 드리프트 폰크 드롭 #Shorts #헬스", "description": "⚡ 우퍼 전용 극저음 드롭! 1시간 풀버전은 관련 영상에서 감상하세요."}
            }
        },
        "uBwoMrx4EPU": {
            "title_en": "⚡ AGGRESSIVE DRIFT PHONK (16s Seamless Loop) #Shorts #GymPhonk #DriftPhonk",
            "loc": {
                "ja": {"title": "⚡ 疾走ドリフトPhonk（16秒シームレス無限ループ）#Shorts #ドライブ #筋トレ", "description": "⚡ 16秒シームレスループ！1時間フルMixは関連動画から視聴できます。"},
                "es": {"title": "⚡ Drift Phonk Agresivo (Loop de 16s) #Shorts #DriftPhonk", "description": "⚡ Loop perfecto de Drift Phonk! Mix de 1 hora en video relacionado."},
                "pt": {"title": "⚡ Drift Phonk Pesado (Loop de 16s) #Shorts #DriftPhonk", "description": "⚡ Loop contínuo de 16s! Mix de 1 hora no vídeo relacionado."},
                "ru": {"title": "⚡ Агрессивный Дрифт Фонк (16с Луп) #Shorts #Фонк", "description": "⚡ Бесшовный луп фонка! Полный микс в связанном видео."},
                "ko": {"title": "⚡ 아드레날린 폭발 드리프트 폰크 (16초 무한루프) #Shorts", "description": "⚡ 16초 무한루프 폰크! 1시간 풀버전은 관련 영상에서 감상하세요."}
            }
        }
    }
    for s_id, data in shorts_loc.items():
        yt.videos().update(
            part="snippet,localizations",
            body={
                "id": s_id,
                "snippet": {
                    "title": data["title_en"],
                    "description": "⚡ High-Speed Drift Phonk & Extreme Gym Drop.\n🎧 Full 1-Hour Mix available in Related Video!\n\n🔥 Subscribe to @phonkforgeaudio-s1h for daily heavy bass drops!",
                    "categoryId": "10",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en",
                    "tags": ["shorts", "gym phonk", "drift phonk", "heavy bass", "phonkforge"]
                },
                "localizations": data["loc"]
            }
        ).execute()
        print(f"  ✓ Ch 2 Shorts {s_id} updated.")

def sync_ch3_melodic(yt):
    print("▶ Syncing Ch 3: AuraMelody Audio...")
    
    # 1. Vol 1 & Vol 2
    vids_edm = [
        ("Tamf2pVElJU", "✨ [1 HOUR] Pure Uplifting Melodic EDM — Beautiful Progressive House Mix for Focus & Energy"),
        ("o8ygRO9KVuQ", "✨ [1 HOUR] Pure Uplifting Melodic EDM — Beautiful Progressive House Mix for Energy & Focus")
    ]
    loc_edm = {
        "ja": {
            "title": "✨【1時間】爽快エモーショナルMelodic EDM — モチベーションと集中力を高める極上作業用BGM",
            "description": "✨ 1時間ノンストップ。AviciiやKygoを思わせる、美しく多幸感に満ちたメロディックEDM＆プログレッシブハウス。\nプログラミング、勉強、ドライブ、ワークアウトに心地よい高揚感をお届けします。\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🌿 姉妹チャンネル:\n🍃 ジブリ風作業用Lofi ➡️ @komorebi-chill-audio (https://www.youtube.com/@komorebi-chill-audio)\n🔥 超重低音 & Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        },
        "es": {
            "title": "✨ [1 HORA] Melodic EDM y Progressive House — Sesión Motivadora para Estudiar y Trabajar",
            "description": "✨ 1 hora de Melodic EDM y Progressive House con melodías inspiradoras para mantener la energía y el enfoque."
        },
        "pt": {
            "title": "✨ [1 HORA] Melodic EDM e Progressive House — Mix Energético para Foco e Treino",
            "description": "✨ 1 hora de Melodic EDM e Progressive House com vibrações positivas para estudar, trabalhar e treinar."
        },
        "ru": {
            "title": "✨ [1 ЧАС] Мелодичный Прогрессив Хаус — Вдохновляющий Микс для Работы и Фокуса",
            "description": "✨ 1 час красивого Melodic EDM и Progressive House для продуктивной работы, учебы и отличного настроения."
        },
        "ko": {
            "title": "✨ [1시간] 청량하고 감성적인 멜로딕 EDM — 코딩·공부·드라이브를 위한 기분 좋은 노동요",
            "description": "✨ 1시간 연속 재생 감성 멜로딕 프로그레시브 하우스. 집중력과 활력을 불어넣는 세련된 사운드트랙입니다."
        }
    }
    for v_id, t_en in vids_edm:
        desc_en = f"""✨ Welcome to AuraMelody Audio — Pure Uplifting Melodic EDM & Progressive House for Focus, Energy, and Good Vibes.

Immerse yourself in 1 hour of continuous, crystal-clear euphoric melodies inspired by the golden era of Avicii, Kygo, and melodic festival anthems. Perfect for deep focus, coding, studying, workout, gaming, and night drives.

🎧 Sound Design & Mastering:
- SoftBass Transparent Mastering (Enhanced Sub-Bass & Crystal Highs)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌿 Sister Channels:
🍃 Ghibli Nostalgic Lofi ➡️ @komorebi-chill-audio (https://www.youtube.com/@komorebi-chill-audio)
🔥 Extreme Heavy Bass & Gym Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Subscribe to @auramelody-audio for daily uplifting melodies & good vibes!
"""
        yt.videos().update(
            part="snippet,localizations",
            body={
                "id": v_id,
                "snippet": {
                    "title": t_en,
                    "description": desc_en,
                    "categoryId": "10",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en",
                    "tags": ["melodic edm", "progressive house", "avicii style", "uplifting edm", "1 hour edm mix", "auramelody"]
                },
                "localizations": loc_edm
            }
        ).execute()
        print(f"  ✓ Ch 3 {v_id} updated.")

    # 2. Shorts
    s_loc = {
        "ja": {
            "title": "✨ 爽快サマーMelodic EDM（15秒シームレス無限ループ）#Shorts #作業用BGM #EDM",
            "description": "✨ 15秒シームレス無限ループ！1時間フルMixは関連動画から視聴できます。"
        },
        "es": {"title": "✨ Melodic EDM Vibras de Verano (Loop de 15s) #Shorts #EDM", "description": "✨ Loop continuo de 15s. Mix de 1 hora en video relacionado."},
        "pt": {"title": "✨ Melodic EDM Vibe Positiva (Loop de 15s) #Shorts #EDM", "description": "✨ Loop de 15s perfeito! Mix completo de 1 hora no vídeo relacionado."},
        "ru": {"title": "✨ Летний Мелодичный EDM (15с Луп) #Shorts #EDM", "description": "✨ 15-секундный бесшовный луп! Полный 1-часовой микс в связанном видео."},
        "ko": {"title": "✨ 청량 감성 멜로딕 EDM (15초 무한루프) #Shorts #노동요", "description": "✨ 15초 무한루프 멜로딕 EDM! 1시간 풀버전은 관련 영상에서 감상하세요."}
    }
    yt.videos().update(
        part="snippet,localizations",
        body={
            "id": "4sDPJh25GGw",
            "snippet": {
                "title": "✨ SUMMER MELODIC EDM (15s Seamless Loop) #Shorts #MelodicEDM #SummerVibes",
                "description": "✨ 15s Seamless Loop - Summer Melodic EDM & Progressive House.\n🎧 Full 1-Hour Mix available in Related Video!\n\n🔥 Subscribe to @auramelody-audio for daily uplifting mixes!",
                "categoryId": "10",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
                "tags": ["shorts", "melodic edm", "summer edm", "progressive house", "auramelody"]
            },
            "localizations": s_loc
        }
    ).execute()
    print("  ✓ Ch 3 Shorts updated.")

def main():
    print("=== STARTING FULL NATURAL LOCALIZATION & CLEANUP ===")
    yt_ch1 = get_youtube_service("gameverse")
    sync_ch1_lofi(yt_ch1)
    
    yt_ch2 = get_youtube_service("phonkforge")
    sync_ch2_phonk(yt_ch2)
    
    yt_ch3 = get_youtube_service("auramelody")
    sync_ch3_melodic(yt_ch3)
    
    print("\n==================================================")
    print("✅ ALL VIDEOS FULLY NATURALIZED AND CLEANED VIA API!")
    print("==================================================")

if __name__ == "__main__":
    main()
