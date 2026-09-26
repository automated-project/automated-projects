# -*- coding: utf-8 -*-
"""
Ch 3 全3動画（Vol. 1, Vol. 2, Vol. 3）のローカライズ（日・韓・露・葡・西）を
現地のYouTube検索需要・自然なネイティブフレーズで一括最適化するスクリプト（1回のみのAPI実行）
"""
import sys
import time
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

yt = get_youtube_service("auramelody")

# タイムスタンプテキスト
vol1_ch = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL1_chapters.txt").read_text(encoding="utf-8").strip()
vol2_ch = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL2_chapters.txt").read_text(encoding="utf-8").strip()
vol3_ch = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/1HOUR_CRYSTAL_MELODIC_EDM_VOL3_chapters.txt").read_text(encoding="utf-8").strip()

# =========================================================================
# 1. Vol. 1 (o8ygRO9KVuQ) — やる気・モチベーション・テンションUP
# =========================================================================
vol1_loc = {
    "ja": {
        "title": "【洋楽BGM】気分を上げたい時に。やる気とモチベーションが高まる爽快サウンド【1時間】",
        "description": f"✨ AuraMelody Audioへようこそ。\n心が高鳴るドラマチックな旋律と、胸に響くクリアなビートを厳選した洋楽BGMです。\n\nデスクワークや勉強、ワークアウトでモチベーションを高めたい時に最適です。\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可能）】です。\n\n🎵 トラックリスト:\n{vol1_ch}\n\n#洋楽BGM #作業用BGM #モチベーション #フリーBGM #AuraMelody"
    },
    "ko": {
        "title": "[노동요] 텐션 올리고 싶을 때 듣는 신나는 멜로딕 EDM & 팝 플레이리스트 [1시간]",
        "description": f"✨ AuraMelody Audio에 오신 것을 환영합니다.\n지친 일상에 에너지를 불어넣는 신나고 청량한 멜로딕 EDM & 팝 플레이리스트입니다.\n\n작업, 공부, 운동, 드라이브할 때 기분 전환으로 추천합니다.\n크리에이터를 위한 100% 무료 음원(Royalty-Free)입니다.\n\n🎵 트랙리스트:\n{vol1_ch}\n\n#노동요 #멜로딕EDM #신나는음악 #운동음악 #1시간 #AuraMelody"
    },
    "ru": {
        "title": "⚡ Музыка для энергии и мотивации — Бодрый и красивый Melodic EDM [1 час]",
        "description": f"✨ 1 час бодрящей и вдохновляющей электронной музыки (Melodic EDM) для спорта, работы, кодинга и отличного настроения.\n\n100% Бесплатно для создателей контента и стримов!\n\n🎵 Треклист:\n{vol1_ch}\n\n#МузыкаДляТренировок #Мотивация #MelodicEDM #МузыкаДляРаботы #AuraMelody"
    },
    "pt": {
        "title": "⚡ Música Animada para Motivação e Foco — Melodic EDM & Progressive [1 Hora]",
        "description": f"✨ 1 hora de Melodic EDM e Progressive House vibrante para dar aquele gás nos treinos, estudos e no trabalho.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol1_ch}\n\n#MusicaParaTreino #Motivacao #MelodicEDM #MusicaParaTrabalhar #AuraMelody"
    },
    "es": {
        "title": "⚡ Música para Levantar el Ánimo y Entrenar — Melodic EDM Motivacional [1 Hora]",
        "description": f"✨ 1 hora de música electrónica positiva y enérgica para motivarte al máximo en tus entrenamientos, trabajo o estudio.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol1_ch}\n\n#MusicaParaEntrenar #Motivacion #MelodicEDM #MusicaParaTrabajar #AuraMelody"
    }
}

# =========================================================================
# 2. Vol. 2 (Tamf2pVElJU) — 深い集中・勉強・プログラミング・ゾーン
# =========================================================================
vol2_loc = {
    "ja": {
        "title": "【勉強・作業用BGM】驚くほど集中できる。思考を邪魔しない透明感あふれる美メロ【1時間】",
        "description": f"✨ AuraMelody Audioへようこそ。\n澄み渡るピアノと洗練された音色が、深い没入感（ゾーン状態）へと導く集中特化のBGMです。\n\n長時間のコーディング、資格勉強、デスクワーク、読書など、周囲の雑音を遮断して作業に没頭したい時に最適です。\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可能）】です。\n\n🎵 トラックリスト:\n{vol2_ch}\n\n#集中用BGM #勉強用BGM #作業用BGM #プログラミングBGM #フリーBGM #AuraMelody"
    },
    "ko": {
        "title": "[공부/작업용] 갓생 사는 사람들을 위한 초집중 몰입 BGM • 깔끔한 멜로디 [1시간]",
        "description": f"✨ AuraMelody Audio에 오신 것을 환영합니다.\n집중력을 극한으로 끌어올려 주는 깔끔하고 세련된 감성 비트입니다.\n\n코딩, 공부, 과제, 재택근무 등 장시간 몰입이 필요할 때 듣기 좋습니다.\n크리에이터를 위한 100% 무료 음원(Royalty-Free)입니다.\n\n🎵 트랙리스트:\n{vol2_ch}\n\n#공부할때듣는음악 #집중BGM #코딩음악 #노동요 #1시간 #AuraMelody"
    },
    "ru": {
        "title": "🎧 Музыка для глубокой концентрации, работы и учебы — Чистый Melodic EDM [1 час]",
        "description": f"✨ 1 час атмосферной и чистой музыки для глубокого погружения в работу, программирование, учебу и чтение.\n\n100% Бесплатно для использования в видео и стримах!\n\n🎵 Треклист:\n{vol2_ch}\n\n#МузыкаДляУчебы #МузыкаДляРаботы #Концентрация #Кодинг #AuraMelody"
    },
    "pt": {
        "title": "🎧 Música para Estudar e Trabalhar com Foco Total — Melodic EDM Limpo [1 Hora]",
        "description": f"✨ 1 hora de batidas limpas e harmoniosas para alcançar foco total na programação, leitura e estudos diários.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol2_ch}\n\n#MusicaParaEstudar #FocoTotal #MusicaParaProgramar #Estudos #AuraMelody"
    },
    "es": {
        "title": "🎧 Música para Estudiar y Trabajar con Máxima Concentración — Melodic EDM Instrumental [1 Hora]",
        "description": f"✨ 1 hora de melodías envolventes y sonido impecable para entrar en estado de concentración absoluta mientras estudias o trabajas.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol2_ch}\n\n#MusicaParaEstudiar #ConcentracionTotal #MusicaParaTrabajar #Programacion #AuraMelody"
    }
}

# =========================================================================
# 3. Vol. 3 (EWtj0yBMsrs) — ドライブ・夕暮れ・気分転換・開放感
# =========================================================================
vol3_loc = {
    "ja": {
        "title": "【ドライブBGM】どこまでも走りたくなる。夕暮れの心地よい開放感と爽快サウンド【1時間】",
        "description": f"✨ AuraMelody Audioへようこそ。\nあたたかな夕暮れの光に包まれるような、心地よい開放感と前向きな高揚感を届けるBGMです。\n\n夕方のドライブや、気分転換をしながら進めたい作業、日々のリフレッシュタイムに寄り添います。\n動画制作や配信で自由に使える【完全フリーBGM（商用利用可能）】です。\n\n🎵 トラックリスト:\n{vol3_ch}\n\n#ドライブBGM #洋楽BGM #作業用BGM #リフレッシュ #フリーBGM #AuraMelody"
    },
    "ko": {
        "title": "[드라이브 BGM] 노을 질 때 달리기 좋은 청량하고 신나는 EDM 플레이리스트 [1시간]",
        "description": f"✨ AuraMelody Audio에 오신 것을 환영합니다.\n노을 질 때 드라이브하거나 기분 전환할 때 듣기 딱 좋은 감성 멜로딕 EDM입니다.\n\n답답한 마음을 날려주는 시원한 비트와 따뜻한 멜로디를 즐겨보세요.\n크리에이터를 위한 100% 무료 음원(Royalty-Free)입니다.\n\n🎵 트랙리스트:\n{vol3_ch}\n\n#드라이브음악 #드라이브BGM #신나는음악 #청량한음악 #1시간 #AuraMelody"
    },
    "ru": {
        "title": "🚗 Музыка в машину / Для фона — Красивый и атмосферный Melodic EDM на закате [1 час]",
        "description": f"✨ 1 час красивой и легкой электронной музыки для поездок на авто, вечернего отдыха и приятного рабочего фона.\n\n100% Бесплатно для использования в видео и стримах!\n\n🎵 Треклист:\n{vol3_ch}\n\n#МузыкаВМашину #МузыкаДляДороги #КрасиваяМузыка #Фон #AuraMelody"
    },
    "pt": {
        "title": "🚗 Música para Viagem e Estrada — Melodic EDM Perfeito para o Fim de Tarde [1 Hora]",
        "description": f"✨ 1 hora de som relaxante e empolgante para curtir na estrada, viagens ou para animar o seu fim de tarde.\n\n100% Grátis e Royalty-Free para criadores de conteúdo!\n\n🎵 Tracklist:\n{vol3_ch}\n\n#MusicaParaViagem #MusicaParaCarro #MelodicEDM #Estrada #AuraMelody"
    },
    "es": {
        "title": "🚗 Música para Manejar y Relajarse — Melodic EDM para el Atardecer [1 Hora]",
        "description": f"✨ 1 hora de música perfecta para conducir al atardecer, viajar o simplemente desconectar y disfrutar del camino.\n\n100% Libre de regalías para creadores y streamers!\n\n🎵 Lista de canciones:\n{vol3_ch}\n\n#MusicaParaManejar #MusicaParaViajar #Atardecer #Relax #AuraMelody"
    }
}

updates = [
    ("o8ygRO9KVuQ", vol1_loc, "Vol. 1"),
    ("Tamf2pVElJU", vol2_loc, "Vol. 2"),
    ("EWtj0yBMsrs", vol3_loc, "Vol. 3")
]

for vid, loc_data, label in updates:
    print(f"\n[+] Updating {label} ({vid}) with native market search localizations...")
    v_res = yt.videos().list(id=vid, part="snippet").execute()
    if v_res.get("items"):
        snippet = v_res["items"][0]["snippet"]
        body = {
            "id": vid,
            "snippet": {
                "title": snippet["title"],
                "description": snippet["description"],
                "tags": snippet.get("tags", []),
                "categoryId": snippet.get("categoryId", "10"),
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en"
            },
            "localizations": loc_data
        }
        yt.videos().update(part="snippet,localizations", body=body).execute()
        print(f"✅ Successfully updated {label} ({vid})!")
        time.sleep(1)

print("\n🎉 ALL 3 VIDEOS SUCCESSFULLY LOCALIZED TO NATIVE MARKET SEARCH DEMANDS!")
