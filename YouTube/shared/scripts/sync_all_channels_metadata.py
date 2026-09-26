# -*- coding: utf-8 -*-
"""
全チャンネル・全公開動画 メタデータ一括同期スクリプト（tracks_master.json 辞書駆動型）
- 単一のマスターJSON（shared/metadata/tracks_master.json）からトラック名・タイムスタンプ・Vault URLを動的生成
- フリー音源ライセンス ＆ 24bit WAV Creator Vault導線
- 多言語SEOローカライズ（英語、ロシア語[EDM系特化]、日本語、スペイン語、ポルトガル語、韓国語）
"""

import json
import sys
import time
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

MASTER_PATH = Path("/Users/base/Automated-Projects/YouTube/shared/metadata/tracks_master.json")

def load_master_data():
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_tracklist_string(tracks: list) -> str:
    lines = []
    for t in tracks:
        lines.append(f"{t['time']} - {t['title']}")
    return "\n".join(lines)

def sync_gameverse(yt, master_data):
    print("\n==========================================")
    print("▶ Syncing Ch 1: Komorebi Chill Audio")
    print("==========================================")
    
    ch_info = master_data["channels"]["gameverse"]
    vault_url = ch_info["gumroad_vault"]
    vol1_info = ch_info["albums"]["vol1"]
    vid_lofi = vol1_info["video_id"]
    tracklist_str = build_tracklist_string(vol1_info["tracks"])
    
    print(f"[+] Updating Vol. 1 Lofi video ({vid_lofi})...")
    
    title_en = "🍃 [1 HOUR] Studio Ghibli Inspired Chill Lofi — Nostalgic Beats for Study, Work & Deep Sleep"
    desc_en = f"""🍃 Welcome to Komorebi Chill Audio — Studio Ghibli inspired nostalgic chill lofi beats for deep focus, studying, working, reading, and relaxing sleep.

Immerse yourself in 1 hour of warm acoustic guitars, soft upright piano melodies, and gentle vinyl tape textures. Designed to create a cozy, stress-free atmosphere.

⏱️ Tracklist & Timestamps:
{tracklist_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【FREE DOWNLOAD & CREATOR LICENSE】
You can freely use these lofi tracks in your YouTube videos, Twitch streams, podcasts & background music!

✅ Stream-Safe & Content ID Free (No copyright strikes)
📋 Required Attribution (Copy & Paste):
   Music: Komorebi Chill Audio
   Watch: https://youtu.be/{vid_lofi}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 【LOOKING FOR OUR HEAVY BASS / EDM TRACKS?】
All Heavy Bass, Gym Phonk, and Melodic EDM tracks have officially moved to our sister channels:
🔥 Extreme Heavy Bass & Gym Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)
✨ Pure Uplifting Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe to @komorebi-chill-audio for daily cozy lofi study sessions!

#Lofi #ChillLofi #GhibliLofi #StudyMusic #LofiHipHop #RelaxingBGM #SleepMusic #NoCopyrightMusic #RoyaltyFreeBGM #StreamSafe #1HourLofi
"""
    localizations_lofi = {
        "ja": {
            "title": "🍃【1時間】ジブリ風ノスタルジック作業用Chill Lofi — 勉強・仕事・読書・睡眠用 極上ピアノ＆アコースティックBGM",
            "description": "🍃 1時間ノンストップ！ジブリの世界観に浸る、温かいアコースティック＆ピアノの極上ノスタルジックLofi Mix。\n勉強、プログラミング、読書、カフェ作業、睡眠導入に最適な癒やしの空間をお届けします。\n\n🎁【無料ダウンロード＆配信向けフリー音源ライセンス】\nYouTube動画やTwitch配信のBGMとして無料利用可能（要クレジット表記）。\n\n#Lofi #ジブリ風Lofi #作業用BGM #勉強用BGM #睡眠用BGM #著作権フリーBGM #配信BGM #1時間"
        },
        "es": {
            "title": "🍃 [1 HORA] Lofi Inspirado en Studio Ghibli — Beats Nostálgicos para Estudiar y Dormir",
            "description": "🍃 1 hora de música Lofi tranquila y nostálgica inspirada en Studio Ghibli para estudiar, trabajar y descansar.\n\n#Lofi #GhibliLofi #MusicaParaEstudiar #NoCopyrightMusic"
        },
        "pt": {
            "title": "🍃 [1 HORA] Lofi Inspirado no Studio Ghibli — Beats Nostálgicos para Estudar e Dormir",
            "description": "🍃 1 hora de Lofi acústico e nostálgico inspirado no Studio Ghibli para foco profundo, estudos e sono tranquilo.\n\n#Lofi #LofiGhibli #MusicaParaEstudar #SemCopyright"
        },
        "ko": {
            "title": "🍃 [1시간] 지브리 감성 칠 로파이 — 공부·집중·독서·수면을 위한 힐링 노동요",
            "description": "🍃 1시간 연속 재생 지브리 감성 노스탤직 로파이 비트! 깊은 집중, 독서, 수면을 위한 따뜻한 어쿠스틱 사운드.\n\n#로파이 #지브리로파이 #공부할때듣는음악 #수면음악 #저작권프리BGM"
        }
    }
    
    yt.videos().update(
        part="snippet,localizations",
        body={
            "id": vid_lofi,
            "snippet": {
                "title": title_en,
                "description": desc_en,
                "categoryId": "10",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
                "tags": ["lofi", "chill lofi", "ghibli lofi", "study music", "lofi hip hop", "sleep music", "1 hour lofi", "no copyright music", "royalty free lofi", "stream safe bgm", "free download lofi"]
            },
            "localizations": localizations_lofi
        }
    ).execute()
    print(f"  ✓ Updated {vid_lofi}")
    time.sleep(3)

    # 2. 残した2本の長尺EDM (lnJBDZszKCE & bFLKzlSiq4o)
    promo_desc_50 = """🚨 【IMPORTANT NOTICE】
Heavy Bass, Drift Phonk & Gym EDM tracks have officially moved to our new dedicated sister channels:
🔥 Heavy Bass & Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)
✨ Pure Uplifting Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 50 MIN Non-Stop Heavy Gym Phonk & Hardstyle EDM Workout Motivation!
Mastered for maximum adrenaline, heavy deadlifts, PR sets, and high-speed night drives.

🔥 Subscribe to @phonkforgeaudio-s1h for daily gym mixes!
#WorkoutMusic #GymPhonk #DriftPhonk #Hardstyle #BassBoosted #NoCopyrightMusic
"""
    localizations_50 = {
        "ja": {
            "title": "🔥【50分】超重低音Gym Phonk & ハードスタイルEDM | 筋トレ・モチベ爆上げ作業用BGM",
            "description": "🚨 重低音・EDM楽曲は専門チャンネルへ完全移転いたしました！\n🔥 重低音 & Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)\n✨ 爽快Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n#筋トレBGM #ジムフォンク #ドリフトPhonk #EDM"
        },
        "es": {
            "title": "🔥 [50 MIN] Heavy Gym Phonk & Hardstyle EDM Mix | Motivación para Entrenar",
            "description": "🚨 ¡Los mixes de Heavy Bass y EDM se han mudado a nuestros nuevos canales!\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio\n\n#GymPhonk #DriftPhonk #Entrenamiento"
        },
        "pt": {
            "title": "🔥 [50 MIN] Heavy Gym Phonk & Hardstyle EDM Mix | Treino Pesado",
            "description": "🚨 As faixas de Heavy Bass e EDM mudaram para novos canais!\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio\n\n#GymPhonk #DriftPhonk #Treino"
        },
        "ru": {
            "title": "🔥 [50 МИН] Heavy Gym Phonk & Hardstyle EDM — Музыка для Тренировок и Качалки",
            "description": "🚨 Все треки Heavy Bass, Drift Phonk и EDM переехали на наши специализированные каналы!\n🔥 Heavy Bass & Gym Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)\n✨ Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n#GymPhonk #DriftPhonk #Фонк #МузыкаДляТренировок #Басы"
        },
        "ko": {
            "title": "🔥 [50분] 헬스장 전용 하이퍼 짐 폰크 & 하드스타일 EDM 믹스 | 헬스 노동요",
            "description": "🚨 모든 Phonk 및 EDM 트랙은 전용 채널로 이전되었습니다!\n🔥 Heavy Bass ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ Melodic EDM ➡️ https://www.youtube.com/@auramelody-audio\n\n#짐폰크 #드리프트폰크 #헬스음악"
        }
    }

    for v_id, v_title in [("lnJBDZszKCE", "🔥 [50 MIN WORK BGM] Heavy Gym Phonk & Hardstyle EDM Motivation | High-Energy Workout & Gaming Music"),
                          ("bFLKzlSiq4o", "🔥 [20 MIN WORK BGM] Heavy Gym & Gaming EDM Motivation | Aggressive Phonk & Bass (Work & Workout BGM)")]:
        yt.videos().update(
            part="snippet,localizations",
            body={
                "id": v_id,
                "snippet": {
                    "title": v_title,
                    "description": promo_desc_50,
                    "categoryId": "10",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en",
                    "tags": ["gym phonk", "drift phonk", "workout music", "hardstyle edm", "heavy bass", "музыка для тренировок", "фонк", "no copyright music"]
                },
                "localizations": localizations_50
            }
        ).execute()
        print(f"  ✓ Updated promo metadata on {v_id}")
        time.sleep(3)

def sync_phonkforge(yt, master_data):
    print("\n==========================================")
    print("▶ Syncing Ch 2: PhonkForge Audio")
    print("==========================================")
    
    ch_info = master_data["channels"]["phonkforge"]
    vol1_info = ch_info["albums"]["vol1"]
    v_long = vol1_info["video_id"]
    tracklist_str = build_tracklist_string(vol1_info["tracks"])
    
    # 1. 1時間長尺 (4aJlGEfEI84) - 100% GYM PHONK & WORKOUT MOTIVATION
    title_en = "⚡ [1 HOUR] AGGRESSIVE GYM PHONK — Heavy Bass Drift Phonk & Workout Motivation Mix"
    desc_en = f"""⚡ Welcome to PhonkForge Audio — Aggressive Gym Phonk, Heavy Workout Motivation & Extreme Bass Anthems.

1 Hour Non-Stop Aggressive Gym Phonk Mix — Engineered for High-Intensity Weightlifting, Extreme PR Sets, Bodybuilding & Hardcore Workout Motivation.
Mastered with Super Crisp deep sub-bass frequencies (35Hz-55Hz) specifically tuned to push past your limits during heavy gym sessions, intense training, and powerlifting.

⏱️ TRACKLIST & TIMESTAMPS:
{tracklist_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【FREE DOWNLOAD & CREATOR LICENSE】
You can freely use these Phonk tracks in your YouTube videos, TikToks, Shorts, Gym Vlogs & Gaming Montages!

✅ Stream-Safe & Content ID Free (No copyright strikes)
📋 Required Attribution (Copy & Paste):
   Music: PhonkForge Audio
   Watch: https://youtu.be/{v_long}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌿 Sister Channels:
🍃 Ghibli Nostalgic Lofi ➡️ @komorebi-chill-audio (https://www.youtube.com/@komorebi-chill-audio)
✨ Uplifting Melodic EDM ➡️ @auramelody-audio (https://www.youtube.com/@auramelody-audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Subscribe to @phonkforgeaudio-s1h for daily aggressive gym phonk & heavy workout mixes!
#GymPhonk #WorkoutMusic #GymMotivation #PhonkWorkout #FitnessMotivation #HeavyBass #DriftPhonk #PhonkForge #1HourMix #GymBeats
"""
    localizations_long = {
        "ja": {
            "title": "⚡【1時間】超重低音AGGRESSIVE GYM PHONK — 筋トレ・限界突破ワークアウト公式Mix",
            "description": "⚡ ジム・筋トレ・限界突破専用！1時間ノンストップ・超重低音Aggressive Gym Phonk公式Mix！🔥\n身体の芯を震わせるサブベースと高音質マスタリングで、ベンチプレスやスクワット、高強度トレーニングのモチベーションを爆発させます！\n\n🎁【無料ダウンロード＆商用フリーライセンス】\nYouTubeやTikTokで無料利用可能（要クレジット表記）。\n\n#筋トレBGM #ジムフォンク #重低音 #ワークアウト #ドリフトPhonk #著作権フリーBGM"
        },
        "es": {
            "title": "⚡ [1 HORA] AGGRESSIVE GYM PHONK — Heavy Bass Drift Phonk & Motivación para Entrenar",
            "description": "⚡ ¡1 hora de Gym Phonk agresivo y bajos pesados para entrenar duro en el gimnasio, pesas y cardio intenso!\n\n#GymPhonk #Entrenamiento #DriftPhonk #NoCopyrightMusic"
        },
        "pt": {
            "title": "⚡ [1 HORA] AGGRESSIVE GYM PHONK — Heavy Bass Drift Phonk & Treino Pesado",
            "description": "⚡ 1 hora de Gym Phonk pesado e agressivo para musculação pesada, treinos intensos e motivação extrema!\n\n#GymPhonk #TreinoPesado #DriftPhonk #SemCopyright"
        },
        "ru": {
            "title": "⚡ [1 ЧАС] AGGRESSIVE GYM PHONK — Тяжелый Фонк для Качалки, Тренировок и Дрифта",
            "description": "⚡ 1 час экстремального и тяжелого Gym Phonk для качалки, пауэрлифтинга, жестких тренировок и ночного дрифта!\n\n#GymPhonk #ФонкДляКачалки #МузыкаДляТренировок #Фонк #БасыВМашину #CarMusic"
        },
        "ko": {
            "title": "⚡ [1시간] 익스트림 짐 폰크 — 헬스장 3대 운동 전용 헤비 베이스 노동요",
            "description": "⚡ 헬스장 고중량 웨이트 및 극강의 집중을 위한 1시간 논스톱 어그레시브 짐 폰크 믹스!\n\n#짐폰크 #헬스음악 #웨이트트레이닝 #드리프트폰크 #1시간"
        }
    }
    
    yt.videos().update(
        part="snippet,localizations",
        body={
            "id": v_long,
            "snippet": {
                "title": title_en,
                "description": desc_en,
                "categoryId": "10",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
                "tags": ["gym phonk", "workout music", "gym motivation", "phonk workout", "fitness motivation", "heavy bass", "drift phonk", "phonkforge", "музыка для тренировок", "фонк для качалки", "фонк", "no copyright phonk", "free download phonk"]
            },
            "localizations": localizations_long
        }
    ).execute()
    print(f"  ✓ Updated {v_long}")


    # 2. Shorts動画群
    shorts_list = [
        ("W7yzwdh1vdQ", "⚡ TOKYO OVERDRIVE — Extreme Gym Phonk Drop #Shorts #GymPhonk #DriftPhonk", "⚡ TOKYO OVERDRIVE — Мощный Дрифт Фонк Дроп (Басы в Машину) #Shorts #Фонк #МузыкаВМашину"),
        ("uBwoMrx4EPU", "⚡ AGGRESSIVE DRIFT PHONK (16s Seamless Loop) #Shorts #GymPhonk #DriftPhonk", "⚡ AGGRESSIVE DRIFT PHONK (16s Seamless Loop) #Shorts #Фонк #МузыкаВМашину"),
        ("QhBfGIJh7jg", "⚡ CRUSH THE BONE — Aggressive Gym Phonk Drop #Shorts #GymPhonk #DriftPhonk", "⚡ CRUSH THE BONE — Тяжелый Дрифт Фонк для Качалки #Shorts #Фонк #МузыкаВМашину"),
        ("j49aZgkO0Kc", "⚡ BLACKTOP FURY — Cyber Drift Phonk Drop #Shorts #GymPhonk #DriftPhonk", "⚡ BLACKTOP FURY — Дрифт Фонк и Басы в Машину #Shorts #Фонк #МузыкаВМашину"),
        ("6gK-_VodDJM", "⚡ SAVAGE GRIP — Hardcore Gym Phonk Drop #Shorts #GymPhonk #DriftPhonk", "⚡ SAVAGE GRIP — Мощный Фонк для Тренировок #Shorts #Фонк #МузыкаДляТренировок")
    ]
    
    for s_id, s_title, ru_title in shorts_list:
        s_desc = f"""⚡ High-Speed Drift Phonk & Extreme Gym Drop.
🎧 Full 1-Hour Mix available in Related Video!

🎁 Free Creator Download: {vault_url}
🔥 Subscribe to @phonkforgeaudio-s1h for daily heavy bass drops!
#Shorts #GymPhonk #DriftPhonk #BassBoosted #NoCopyrightPhonk #PhonkForge
"""
        s_loc = {
            "ja": {
                "title": "⚡ 激熱ドリフトPhonkドロップ（超重低音）#Shorts #GymPhonk #筋トレBGM",
                "description": "⚡ 脳を揺らす超重低音ドリフトPhonk！\n🎧 1時間フル公式Mixは関連動画リンクから視聴できます！\n\n#Shorts #ドリフトPhonk #筋トレBGM"
            },
            "es": {"title": f"{s_title.split('—')[0]}— Drop de Gym Phonk #Shorts #DriftPhonk", "description": "⚡ ¡Bajos pesados y Drift Phonk agresivo! Mix de 1 hora en video relacionado."},
            "pt": {"title": f"{s_title.split('—')[0]}— Drop Pesado de Gym Phonk #Shorts #DriftPhonk", "description": "⚡ Graves insanos e Drift Phonk! Mix completo de 1 hora no vídeo relacionado."},
            "ru": {"title": ru_title, "description": "⚡ Экстремальный бас и мощный дрифт фонк для авто и качалки!\n🎧 Полный 1-часовой микс доступен в связанном видео.\n\n#Shorts #Фонк #МузыкаВМашину #Басы #МузыкаДляТренировок"},
            "ko": {"title": "⚡ 익스트림 짐 폰크 드롭 #Shorts #짐폰크", "description": "⚡ 심장을 울리는 극저음 드리프트 폰크! 1시간 풀버전은 관련 영상에서 감상하세요."}
        }
        yt.videos().update(
            part="snippet,localizations",
            body={
                "id": s_id,
                "snippet": {
                    "title": s_title,
                    "description": s_desc,
                    "categoryId": "10",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en",
                    "tags": ["shorts", "gym phonk", "drift phonk", "heavy bass", "phonkforge", "фонк", "музыка в машину", "музыка для тренировок", "no copyright phonk"]
                },
                "localizations": s_loc
            }
        ).execute()
        print(f"  ✓ Updated Shorts {s_id}")
        time.sleep(3)

def sync_auramelody(yt, master_data):
    print("\n==========================================")
    print("▶ Syncing Ch 3: AuraMelody Audio")
    print("==========================================")
    
    ch_info = master_data["channels"]["auramelody"]
    vol2_info = ch_info["albums"]["vol2"]
    tracklist_str = build_tracklist_string(vol2_info["tracks"])
    
    vids_edm = [
        ("Tamf2pVElJU", "✨ [1 HOUR] Pure Uplifting Melodic EDM — Beautiful Progressive House Mix for Focus & Energy"),
        ("o8ygRO9KVuQ", "✨ [1 HOUR] Pure Uplifting Melodic EDM — Beautiful Progressive House Mix for Energy & Focus")
    ]
    
    for v_id, v_title in vids_edm:
        desc_en = f"""✨ Welcome to AuraMelody Audio — Pure Uplifting Melodic EDM & Progressive House for Focus, Energy, and Good Vibes.

Immerse yourself in 1 hour of continuous, crystal-clear euphoric melodies inspired by the golden era of Avicii, Kygo, and melodic festival anthems. Perfect for deep focus, coding, studying, workout, gaming, and night drives.

⏱️ Tracklist & Timestamps:
{tracklist_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【FREE DOWNLOAD & CREATOR LICENSE】
You can freely use these Melodic EDM tracks in your YouTube videos, Twitch streams, Vlogs, Travel videos & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
📋 Required Attribution (Copy & Paste):
   Music: AuraMelody Audio
   Watch: https://youtu.be/{v_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌿 Sister Channels:
🍃 Ghibli Nostalgic Lofi ➡️ @komorebi-chill-audio (https://www.youtube.com/@komorebi-chill-audio)
🔥 Extreme Heavy Bass & Gym Phonk ➡️ @phonkforgeaudio-s1h (https://www.youtube.com/@phonkforgeaudio-s1h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Subscribe to @auramelody-audio for daily uplifting melodies & festival energy!

#MelodicEDM #ProgressiveHouse #AviciiStyle #EDMMix #StudyMusic #FocusMusic #CodingBGM #NoCopyrightMusic #RoyaltyFreeEDM #AuraMelody #1HourMix
"""
        loc_edm = {
            "ja": {
                "title": "✨ [1時間] 爽快エモーショナルMelodic EDM — 集中力・モチベーションを高める極上Progressive House作業用BGM",
                "description": "✨ 1時間ノンストップ！ Aviciiスタイルの多幸感あふれる極上Melodic EDM & Progressive House Mix。\n作業、プログラミング、勉強、ドライブ、ワークアウトに最適な高揚感をお届けします。\n\n🎁【無料ダウンロード＆商用フリーライセンス】\nYouTube動画やVlogで無料利用可能（要クレジット表記）。\n\n#メロディックEDM #プログレッシブハウス #作業用BGM #勉強用BGM #著作権フリーBGM #1時間"
            },
            "es": {
                "title": "✨ [1 HORA] Pure Uplifting Melodic EDM — Mix de Progressive House para Concentración",
                "description": "✨ 1 hora de Melodic EDM y Progressive House para estudiar, trabajar, entrenar y concentrarse.\n\n#MelodicEDM #ProgressiveHouse #MusicaParaEstudiar #NoCopyrightMusic"
            },
            "pt": {
                "title": "✨ [1 HORA] Pure Uplifting Melodic EDM — Mix de Progressive House para Foco e Energia",
                "description": "✨ 1 hora de Melodic EDM e Progressive House para foco, trabalho, treino e vibe positiva.\n\n#MelodicEDM #ProgressiveHouse #MusicaParaEstudar #SemCopyright"
            },
            "ru": {
                "title": "✨ [1 ЧАС] Мелодичный EDM и Клубная Музыка — Красивый Прогрессив Хаус для Энергии и Работы",
                "description": "✨ 1 час кристально чистого Melodic EDM и Progressive House (в стиле Avicii) для учебы, работы, кодинга, поездок на авто и тренировок!\n\n#МелодичныйEDM #КлубнаяМузыка #ЭлектроннаяМузыка #МузыкаДляУчебы #МузыкаБезАП #EDM"
            },
            "ko": {
                "title": "✨ [1시간] 퓨어 멜로딕 EDM & 프로그레시브 하우스 — 공부·집중·노동요를 위한 감성 믹스",
                "description": "✨ 1시간 연속 재생 감성 멜로딕 EDM & 프로그레시브 하우스! 집중, 공부, 코딩, 드라이브를 위한 최고의 에너제틱 사운드.\n\n#멜로딕EDM #프로그레시브하우스 #노동요 #공부할때듣는음악 #저작권프리음악"
            }
        }
        
        yt.videos().update(
            part="snippet,localizations",
            body={
                "id": v_id,
                "snippet": {
                    "title": v_title,
                    "description": desc_en,
                    "categoryId": "10",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en",
                    "tags": ["melodic edm", "progressive house", "avicii style", "uplifting edm", "1 hour edm mix", "auramelody", "мелодичный edm", "клубная музыка", "музыка без авторских прав", "no copyright edm", "royalty free edm", "free download edm"]
                },
                "localizations": loc_edm
            }
        ).execute()
        print(f"  ✓ Updated {v_id}")
        time.sleep(3)

    # 2. Shorts (4sDPJh25GGw)
    s_id = "4sDPJh25GGw"
    s_title = "✨ SUMMER MELODIC EDM (15s Seamless Loop) #Shorts #MelodicEDM #SummerVibes"
    s_desc = f"""✨ 15s Seamless Loop - Summer Melodic EDM & Progressive House (Avicii / Kygo Style).
🎧 Full 1-Hour Mix available in Related Video!

🎁 Free Creator Download: {vault_url}
🔥 Subscribe to @auramelody-audio for daily uplifting mixes!
#Shorts #MelodicEDM #ProgressiveHouse #EDM #NoCopyrightEDM #AuraMelody
"""
    s_loc = {
        "ja": {
            "title": "✨ 爽快サマーMelodic EDM（15秒シームレス無限ループ）#Shorts #MelodicEDM #作業用BGM",
            "description": "✨ 15秒シームレス無限ループ！爽快エモーショナルSummer Melodic EDM & Progressive House。\n🎧 1時間フル公式Mixは関連動画リンクから視聴できます！\n\n#Shorts #メロディックEDM #サマーEDM #作業用BGM"
        },
        "es": {"title": "✨ SUMMER MELODIC EDM (15s Loop) #Shorts #MelodicEDM #Verano", "description": "✨ ¡Loop sin fin de 15s de Summer Melodic EDM! Mix completo en video relacionado."},
        "pt": {"title": "✨ SUMMER MELODIC EDM (15s Loop) #Shorts #MelodicEDM #Vibes", "description": "✨ Loop perfeito de 15s de Melodic EDM! Mix completo no vídeo relacionado."},
        "ru": {"title": "✨ ЛЕТНИЙ МЕЛОДИЧНЫЙ EDM (15с Луп) #Shorts #КлубнаяМузыка #EDM", "description": "✨ 15-секундный бесшовный луп Melodic EDM & Progressive House!\n🎧 Полный 1-часовой микс доступен в связанном видео.\n\n#Shorts #МелодичныйEDM #КлубнаяМузыка #EDM"},
        "ko": {"title": "✨ 썸머 멜로딕 EDM (15초 무한루프) #Shorts #멜로딕EDM #여름노래", "description": "✨ 15초 무한 루프 썸머 멜로딕 EDM! 1시간 풀버전은 관련 영상에서 감상하세요."}
    }
    yt.videos().update(
        part="snippet,localizations",
        body={
            "id": s_id,
            "snippet": {
                "title": s_title,
                "description": s_desc,
                "categoryId": "10",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
                "tags": ["shorts", "melodic edm", "summer edm", "progressive house", "auramelody", "клубная музыка", "no copyright music"]
            },
            "localizations": s_loc
        }
    ).execute()
    print(f"  ✓ Updated Shorts {s_id}")
    time.sleep(3)

def main():
    print("=== STARTING CROSS-CHANNEL METADATA & LOCALIZATION SYNC (DATABASE DRIVEN) ===")
    master_data = load_master_data()
    
    # 1. Ch 1: Komorebi Chill Audio
    try:
        yt_gameverse = get_youtube_service("gameverse")
        sync_gameverse(yt_gameverse, master_data)
    except Exception as e:
        print(f"[-] Error syncing Ch 1 (gameverse): {e}")
    
    # 2. Ch 2: PhonkForge Audio
    try:
        yt_phonkforge = get_youtube_service("phonkforge")
        sync_phonkforge(yt_phonkforge, master_data)
    except Exception as e:
        print(f"[-] Error syncing Ch 2 (phonkforge): {e}")
    
    # 3. Ch 3: AuraMelody Audio
    try:
        yt_auramelody = get_youtube_service("auramelody")
        sync_auramelody(yt_auramelody, master_data)
    except Exception as e:
        print(f"[-] Error syncing Ch 3 (auramelody): {e}")
    
    print("\n==================================================")
    print("🏁 CROSS-CHANNEL METADATA SYNC BATCH FINISHED")
    print("==================================================")

if __name__ == "__main__":
    main()
