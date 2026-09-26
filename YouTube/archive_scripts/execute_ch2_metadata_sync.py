# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) の公開中動画メタデータ一括更新スクリプト
- 30分Mix (z1jIjyKqNLM)
- 1時間Gym Phonk (4aJlGEfEI84)
- 1時間Car Phonk (KfDXrQ2gmkM)
- 新曲名タイムスタンプ同期
- 正規チャンネルハンドル (@PhonkForgeAudio-s1h, @haven-chill-audio, @AuraMelody-Audio)
- 各国のYouTube検索需要・自然なネイティブ表現（直訳禁止・耐久禁止）
"""
import sys
import time
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("phonkforge")

# 1. 30分Mix (z1jIjyKqNLM)
ch_30m = """00:00 - Bonecrusher Phonk
02:51 - Iron Ascension
05:48 - Boost Pressure Max
08:45 - Asphalt Burnout 808
11:36 - Kingdom Of Shadows
14:19 - Blacktop Overdrive
17:16 - Night Drift Redline
20:10 - Concrete Chaser
23:07 - Savage Tire Grip
25:58 - Storming The Gates
28:51 - Maximum Torque RPM"""

Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel/output_videos/30MIN_HARDCORE_GYM_PHONK_MOTIVATION_chapters.txt").write_text(ch_30m, encoding="utf-8")

desc_30m = f"""⚡ 30 MIN NON-STOP HARDCORE GYM PHONK & BRUTAL WORKOUT MOTIVATION MIX
Heavy 808 Bass, Aggressive Drift Drops, and Relentless Drive to push past your absolute limits.

⏱️ TRACKLIST & TIMESTAMPS:
{ch_30m}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 WELCOME TO PHONKFORGE AUDIO
The ultimate sonic forge for gym athletes, powerlifters, and night drifters.
Engineered with heavy distortion, authentic vocal chops, and crushing 808 sub-bass tuned for pure adrenaline.

💪 Perfect for: Max Effort PRs, Heavy Sets, Late-Night Highway Drives, High-Speed Gaming.

100% Free & Royalty-Free for Creators! Feel free to use these tracks in your gym vlogs, gaming streams, and content.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎧 Sound Design: Extreme Sub-Bass Calibration (-14.0 LUFS / Seamless Equal-Power DJ Crossfade)
🎬 Visual: Underground Iron Sanctuary with Reactive Sub-Bass Pulse

🔥 Subscribe to @PhonkForgeAudio-s1h for daily hardcore workout phonk!
#GymPhonk #WorkoutMusic #GymMotivation #HardcorePhonk #DriftPhonk #HeavyBass #PhonkForge #30MinMix #FreeBGM
"""

loc_30m = {
    "ja": {
        "title": "【筋トレ用BGM】限界突破。モチベーションとアドレナリンを引き出す重低音Phonk【30分】",
        "description": f"⚡ 限界を超えるためのハードコア・ワークアウトBGM！\n筋トレ（PR更新、追い込み）、深夜ドライブ、気合を入れたい作業に最適な重低音Phonk Mixです。\n\n動画制作や配信で自由に使える【フリーBGM（商用利用可能）】です。\n\n⏱️ トラックリスト:\n{ch_30m}\n\n#筋トレBGM #ワークアウトBGM #重低音 #モチベーション #フリーBGM #PhonkForge"
    },
    "ko": {
        "title": "[헬스/운동 BGM] 3대 500 찍는 사람들을 위한 초강력 중저음 폰크(Phonk) 플레이리스트 [30분]",
        "description": f"⚡ 운동할 때 아드레날린 폭발하는 묵직한 헬스장 폰크(Gym Phonk) 플레이리스트입니다.\n\n3대 운동 PR 갱신, 고중량 세트, 빡센 운동할 때 강력 추천합니다.\n크리에이터를 위한 100% 무료 음원(Royalty-Free)입니다.\n\n⏱️ 트랙리스트:\n{ch_30m}\n\n#헬스음악 #운동BGM #헬스장노동요 #중저음 #30분 #PhonkForge"
    },
    "ru": {
        "title": "⚡ Музыка для тренировок и качалки — Жесткий Gym Phonk с мощным басом [30 минут]",
        "description": f"⚡ 30 минут мощнейшего Gym Phonk для качалки, тяжелых подходов и максимальной мотивации.\n\n100% Бесплатно для использования в видео и стримах!\n\n⏱️ Треклист:\n{ch_30m}\n\n#МузыкаДляТренировок #GymPhonk #Качалка #МощныйБас #PhonkForge"
    },
    "pt": {
        "title": "⚡ Música para Treino Pesado na Academia — Gym Phonk com Grave Extremo [30 Min]",
        "description": f"⚡ 30 minutos de Gym Phonk agressivo para bater recordes na academia e treinar no limite.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n⏱️ Tracklist:\n{ch_30m}\n\n#MusicaParaTreino #GymPhonk #Academia #GraveForte #PhonkForge"
    },
    "es": {
        "title": "⚡ Música para Entrenar Pesado en el Gym — Phonk Agresivo con Bajo Potente [30 Min]",
        "description": f"⚡ 30 minutos de Phonk agresivo y motivacional para entrenar pesado en el gimnasio y romper tus récords.\n\n100% Libre de regalías para creadores y streamers!\n\n⏱️ Lista de canciones:\n{ch_30m}\n\n#MusicaParaEntrenar #GymPhonk #MotivacionGym #BajosPotentes #PhonkForge"
    }
}

print("[+] Updating 30-min Gym Phonk (z1jIjyKqNLM)...")
yt.videos().update(
    part="snippet,localizations",
    body={
        "id": "z1jIjyKqNLM",
        "snippet": {
            "title": "30 MIN HARDCORE GYM PHONK 🔥 Brutal Workout Motivation Mix [Aggressive Bass]",
            "description": desc_30m,
            "tags": ["gym phonk", "workout motivation", "drift phonk", "hardcore phonk", "gym music", "heavy bass", "phonkforge audio", "30 min workout", "free bgm"],
            "categoryId": "10",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "localizations": loc_30m
    }
).execute()
print("✅ Successfully updated z1jIjyKqNLM!")
time.sleep(1)


# 2. 1時間 Gym Phonk (4aJlGEfEI84) & 1時間 Car Phonk (KfDXrQ2gmkM)
ch_1h = """00:00 - Storming The Gates
02:54 - Asphalt Fang Strike
05:54 - Venom On Asphalt
08:46 - Grim Asphalt Reaper
11:35 - Night Drift Redline
14:31 - Brutal Takedown
17:31 - Street Teeth
20:27 - Hydraulic Vise
23:27 - Blacktop Overdrive
26:26 - Concrete Chaser
29:26 - Tokyo Drift Rage
32:25 - Bonecrusher Phonk
35:18 - Kingdom Of Shadows
38:03 - Dark Midnight Cruise
41:02 - Asphalt Burnout 808
43:55 - Midnight Tachometer
46:49 - Full Throttle Impact
49:47 - Boost Pressure Max
52:47 - Maximum Torque RPM
55:39 - Savage Tire Grip
58:32 - Serrated Tarmac
61:30 - Iron Ascension"""

desc_1h_gym = f"""⚡ Welcome to PhonkForge Audio — Aggressive Gym Phonk, Heavy Workout Motivation & Extreme Bass Anthems.

1 Hour Non-Stop Aggressive Gym Phonk Mix — Engineered for High-Intensity Weightlifting, Extreme PR Sets, Bodybuilding & Hardcore Workout Motivation.
Mastered with Super Crisp deep sub-bass frequencies (35Hz-55Hz) specifically tuned to push past your limits during heavy gym sessions, intense training, and powerlifting.

⏱️ TRACKLIST & TIMESTAMPS:
{ch_1h}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【FREE DOWNLOAD & CREATOR LICENSE】
You can freely use these Phonk tracks in your YouTube videos, TikToks, Shorts, Gym Vlogs & Gaming Montages!

✅ Stream-Safe & Content ID Free (No copyright strikes)
📋 Required Attribution (Copy & Paste):
   Music: @PhonkForgeAudio-s1h
   Watch: https://youtu.be/4aJlGEfEI84
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌿 Sister Channels:
🌿 Cozy Lofi & Study ➡️ @haven-chill-audio (https://www.youtube.com/@haven-chill-audio)
✨ Uplifting Melodic EDM ➡️ @AuraMelody-Audio (https://www.youtube.com/@AuraMelody-Audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Subscribe to @PhonkForgeAudio-s1h for daily aggressive gym phonk & heavy workout mixes!
#GymPhonk #WorkoutMusic #GymMotivation #PhonkWorkout #FitnessMotivation #HeavyBass #DriftPhonk #PhonkForge #1HourMix #GymBeats
"""

loc_1h_gym = {
    "ja": {
        "title": "【筋トレ用BGM】極限の追い込み。圧倒的アドレナリンが湧き出るノンストップ重低音Phonk【1時間】",
        "description": f"⚡ 1時間ノンストップ！ 高重量トレーニング・限界突破のための極上Gym Phonk Mix。\n重低音サブベースが筋トレや集中作業のモチベーションを最高潮に引き上げます。\n\n動画制作や配信で自由に使える【フリーBGM（商用利用可能）】です。\n\n⏱️ トラックリスト:\n{ch_1h}\n\n#筋トレBGM #ワークアウトBGM #重低音 #モチベーション #フリーBGM #PhonkForge"
    },
    "ko": {
        "title": "[헬스장 노동요] 최고 기록 갱신용 초강력 비트 • 아드레날린 폭발 짐 폰크(Gym Phonk) [1시간]",
        "description": f"⚡ 1시간 연속 재생 헬스장 빡운동 BGM! 무게 칠 때 듣기 좋은 초강력 짐 폰크(Gym Phonk) 모음입니다.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)입니다.\n\n⏱️ 트랙리스트:\n{ch_1h}\n\n#헬스음악 #헬스장노동요 #운동할때듣는음악 #중저음 #1시간 #PhonkForge"
    },
    "ru": {
        "title": "🔥 Мощная музыка для зала и тяжелых тренировок — Жесткий Gym Phonk [1 час]",
        "description": f"⚡ 1 час непрерывного мощного Gym Phonk для тренировок в зале, жима и максимального фокуса.\n\n100% Бесплатно для использования в видео и стримах!\n\n⏱️ Треклист:\n{ch_1h}\n\n#МузыкаДляЗала #GymPhonk #ТяжелыйТренинг #МощныйБас #PhonkForge"
    },
    "pt": {
        "title": "🔥 Música para Academia e Treino Pesado — Gym Phonk com Sub-Bass Brutal [1 Hora]",
        "description": f"⚡ 1 hora de Gym Phonk sem parar para manter o foco e o ritmo nos treinos mais pesados da academia.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n⏱️ Tracklist:\n{ch_1h}\n\n#MusicaParaAcademia #TreinoPesado #GymPhonk #GravePesado #PhonkForge"
    },
    "es": {
        "title": "🔥 Música Motivacional para el Gym y Levantamiento de Pesas — Gym Phonk Agresivo [1 Hora]",
        "description": f"⚡ 1 hora de Gym Phonk imparable para entrenar duro, levantar más peso y mantener la motivación arriba.\n\n100% Libre de regalías para creadores y streamers!\n\n⏱️ Lista de canciones:\n{ch_1h}\n\n#MusicaParaElGym #GymPhonk #LevantamientoDePesas #Motivacion #PhonkForge"
    }
}

print("[+] Updating 1-hour Gym Phonk (4aJlGEfEI84)...")
yt.videos().update(
    part="snippet,localizations",
    body={
        "id": "4aJlGEfEI84",
        "snippet": {
            "title": "⚡ [1 HOUR] AGGRESSIVE GYM PHONK — Heavy Bass Drift Phonk & Workout Motivation Mix",
            "description": desc_1h_gym,
            "tags": ["gym phonk", "workout music", "gym motivation", "drift phonk", "heavy bass", "phonkforge audio", "1 hour edm mix", "free bgm"],
            "categoryId": "10",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "localizations": loc_1h_gym
    }
).execute()
print("✅ Successfully updated 4aJlGEfEI84!")
time.sleep(1)


# 3. 1時間 Car Phonk (KfDXrQ2gmkM)
desc_1h_car = f"""🔥 Welcome to PhonkForge Audio — Extreme Sub-Bass Car Music, Drift Phonk & Night Drive Anthems.

1 Hour Non-Stop Heavy Bass Car Audio Mix — Extreme Sub-Bass Drift Phonk & Aggressive Gym Workout Beats.
Engineered with Super Crisp deep sub-bass frequencies (35Hz-55Hz) specifically tuned for car subwoofers, extreme bass tests, heavy workout sets, and high-speed night drives.

⏱️ TRACKLIST & TIMESTAMPS:
{ch_1h}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【FREE DOWNLOAD & CREATOR LICENSE】
You can freely use these Phonk tracks in your YouTube videos, TikToks, Shorts, Car Vlogs & Gaming Montages!

✅ Stream-Safe & Content ID Free (No copyright strikes)
📋 Required Attribution (Copy & Paste):
   Music: @PhonkForgeAudio-s1h
   Watch: https://youtu.be/KfDXrQ2gmkM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌿 Sister Channels:
🌿 Cozy Lofi & Study ➡️ @haven-chill-audio (https://www.youtube.com/@haven-chill-audio)
✨ Uplifting Melodic EDM ➡️ @AuraMelody-Audio (https://www.youtube.com/@AuraMelody-Audio)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Subscribe to @PhonkForgeAudio-s1h for daily aggressive drift phonk & heavy bass mixes!
#CarMusic #BassBoosted #HeavyBass #DeepBass #DriftPhonk #GymPhonk #NightDrive #PhonkForge #SubwooferTest #1HourMix #FreeBGM
"""

loc_1h_car = {
    "ja": {
        "title": "【深夜ドライブBGM】車内を揺らす極上の重低音。夜のハイウェイを疾走するDrift Phonk【1時間】",
        "description": f"🔥 1時間ノンストップ！ サブウーファーを鳴らし切る極太重低音Drift Phonk Mix。\n夜のドライブ、高速道路クルージング、車内音響テストに最適です。\n\n動画制作や配信で自由に使える【フリーBGM（商用利用可能）】です。\n\n⏱️ トラックリスト:\n{ch_1h}\n\n#ドライブBGM #重低音 #ウーファー #ナイトドライブ #フリーBGM #PhonkForge"
    },
    "ko": {
        "title": "[야간 드라이브 BGM] 우퍼 찢어지는 묵직한 중저음 비트 • 심야 질주 폰크(Drift Phonk) [1시간]",
        "description": f"🔥 1시간 연속 재생 카오디오 특화 묵직한 중저음 비트! 심야 드라이브나 기분 전환할 때 듣기 좋은 드리프트 폰크입니다.\n\n크리에이터를 위한 100% 무료 음원(Royalty-Free)입니다.\n\n⏱️ 트랙리스트:\n{ch_1h}\n\n#드라이브음악 #카오디오 #중저음 #우퍼테스트 #심야드라이브 #1시간 #PhonkForge"
    },
    "ru": {
        "title": "🚗 Музыка в машину для ночной езды и басов — Жесткий Drift Phonk [1 час]",
        "description": f"🔥 1 час жесткого Drift Phonk с мощнейшими саб-басами для поездок по ночному городу и проверки автозвука.\n\n100% Бесплатно для использования в видео и стримах!\n\n⏱️ Треклист:\n{ch_1h}\n\n#МузыкаВМашину #НочнойДрайв #Автозвук #DriftPhonk #PhonkForge"
    },
    "pt": {
        "title": "🚗 Música para Carro e Drift Noturno — Grave Forte para Subwoofer [1 Hora]",
        "description": f"🔥 1 hora de Drift Phonk com graves profundos, perfeito para testar o som do carro ou curtir um rolê noturno.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n⏱️ Tracklist:\n{ch_1h}\n\n#MusicaParaCarro #SomAutomotivo #DriftPhonk #GraveForte #PhonkForge"
    },
    "es": {
        "title": "🚗 Música para Conducir de Noche y Drift — Bajos Pesados para el Coche [1 Hora]",
        "description": f"🔥 1 hora de Drift Phonk con subgraves brutales para disfrutar en la carretera o probar los altavoces de tu coche.\n\n100% Libre de regalías para creadores y streamers!\n\n⏱️ Lista de canciones:\n{ch_1h}\n\n#MusicaParaElCoche #BajosPesados #DriftPhonk #ManejarDeNoche #PhonkForge"
    }
}

print("[+] Updating 1-hour Car Phonk (KfDXrQ2gmkM)...")
yt.videos().update(
    part="snippet,localizations",
    body={
        "id": "KfDXrQ2gmkM",
        "snippet": {
            "title": "🔥 [1 HOUR] Car Audio Bass Boosted — Heavy Drift Phonk & Night Drive Mix",
            "description": desc_1h_car,
            "tags": ["car music", "bass boosted", "heavy bass", "drift phonk", "night drive", "phonkforge audio", "1 hour edm mix", "subwoofer test", "free bgm"],
            "categoryId": "10",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "localizations": loc_1h_car
    }
).execute()
print("✅ Successfully updated KfDXrQ2gmkM!")

print("\n🎉 ALL CH 2 PUBLISHED VIDEOS METADATA UPDATED SUCCESSFULLY!")
