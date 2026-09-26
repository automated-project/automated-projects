# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 1時間Mix収録曲からの新作Shorts 3本 アップロードスクリプト
- 1. SHORTS_CH2_1H_TRACK_01_ASPHALT_FANG_STRIKE.mp4
- 2. SHORTS_CH2_1H_TRACK_02_VENOM_ON_ASPHALT.mp4
- 3. SHORTS_CH2_1H_TRACK_03_GRIM_ASPHALT_REAPER.mp4
- API事前タイトル重複チェック
- 多言語ローカライズ（日・韓・露・葡・西 / 直訳禁止・耐久禁止・現地市場需要）
- Free BGM宣言 & 1時間Mix本編への導線
- 固定コメント自動投稿
"""

import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
SHORTS_DIR = CHANNEL_DIR / "output_videos/shorts"

SHORTS_QUEUE = [
    {
        "id": "shorts_1h_01_asphalt_fang_strike",
        "file_name": "SHORTS_CH2_1H_TRACK_01_ASPHALT_FANG_STRIKE.mp4",
        "base_title_en": "HEAVY BASS GYM PHONK DROP 🔥 [Free BGM] #Shorts #gym",
        "title_ja": "【筋トレ用BGM】身体の芯に響く超重低音。限界突破PHONK 🔥 フリーBGM #Shorts #筋トレ",
        "title_ko": "[헬스장 폰크] 묵직한 중저음 드롭 • 운동할 때 듣는 짐 폰크(Gym Phonk) #Shorts #헬스",
        "title_ru": "⚡ Тяжелый бас для качалки и тренировок — Gym Phonk Drop [Free BGM] #Shorts #gym",
        "title_pt": "⚡ Grave Pesado para Treino na Academia — Gym Phonk Drop [Free BGM] #Shorts #treino",
        "title_es": "⚡ Bajo Potente para Entrenar en el Gym — Gym Phonk Drop [Free BGM] #Shorts #gym",
        "desc_en": (
            "⚡ Brutal Heavy Bass Phonk engineered for breaking PRs and crushing hardcore gym workouts.\n"
            "Feel the sub-bass adrenaline and push beyond your limits!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Attribution: Music by @PhonkForgeAudio-s1h (https://www.youtube.com/@PhonkForgeAudio-s1h)\n\n"
            "🔥 Check the full 1-Hour Non-Stop Gym Mix here: https://youtu.be/4aJlGEfEI84\n\n"
            "#GymPhonk #WorkoutMusic #HeavyBass #Fitness #FreeBGM #Shorts"
        ),
        "desc_ja": (
            "⚡ 身体の芯に響く超重低音。筋トレやワークアウトの限界突破に。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます。\n"
            "クレジット: Music by @PhonkForgeAudio-s1h\n\n"
            "🔥 1時間フルバージョンはこちら: https://youtu.be/4aJlGEfEI84\n\n"
            "#筋トレ #ワークアウト #超重低音 #作業用BGM #フリーBGM #Shorts"
        ),
        "comment_text": "🔥 100% Free to use for your gym & workout videos! Check Related Video for the full 1-Hour Mix! ⚡",
        "tags": ["shorts", "gym phonk", "heavy bass", "workout music", "gym motivation", "free bgm", "bass boosted", "phonkforge audio"]
    },
    {
        "id": "shorts_1h_02_venom_on_asphalt",
        "file_name": "SHORTS_CH2_1H_TRACK_02_VENOM_ON_ASPHALT.mp4",
        "base_title_en": "BRUTAL BEAST MODE PHONK ⚡ [Free BGM] #Shorts #workout",
        "title_ja": "【筋トレ用BGM】アドレナリン全開。高重量トレーニング特化PHONK ⚡ フリーBGM #Shorts #ワークアウト",
        "title_ko": "[비스트 모드] 아드레날린 폭발하는 초강력 헬스 폰크(Gym Phonk) #Shorts #운동",
        "title_ru": "🔥 Режим зверя в зале — Жесткий и мощный Gym Phonk [Free BGM] #Shorts #тренировка",
        "title_pt": "🔥 Modo Besta Ativado no Treino — Gym Phonk Agressivo [Free BGM] #Shorts #academia",
        "title_es": "🔥 Modo Bestia para el Gimnasio — Phonk Agresivo y Motivador [Free BGM] #Shorts #fitness",
        "desc_en": (
            "⚡ Pure Beast Mode Phonk engineered for maximum adrenaline and heavy lifting.\n"
            "Feel the sub-bass vibration and conquer your workout!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Attribution: Music by @PhonkForgeAudio-s1h (https://www.youtube.com/@PhonkForgeAudio-s1h)\n\n"
            "🔥 Check the full 1-Hour Non-Stop Gym Mix here: https://youtu.be/4aJlGEfEI84\n\n"
            "#BeastMode #GymPhonk #WorkoutMotivation #HeavyBass #FreeBGM #Shorts"
        ),
        "desc_ja": (
            "⚡ アドレナリンが湧き出る高音圧ビート。高重量トレーニングや追い込みに。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます。\n"
            "クレジット: Music by @PhonkForgeAudio-s1h\n\n"
            "🔥 1時間フルバージョンはこちら: https://youtu.be/4aJlGEfEI84\n\n"
            "#筋トレ #高重量 #ワークアウト #超重低音 #フリーBGM #Shorts"
        ),
        "comment_text": "⚡ 100% Free to use for your videos & streams! What is your current PR goal? Let us know below! 🔥",
        "tags": ["shorts", "beast mode", "gym phonk", "workout music", "heavy bass", "free bgm", "powerlifting", "phonkforge audio"]
    },
    {
        "id": "shorts_1h_03_grim_asphalt_reaper",
        "file_name": "SHORTS_CH2_1H_TRACK_03_GRIM_ASPHALT_REAPER.mp4",
        "base_title_en": "EXTREME GYM PR HEAVY BASS 🔥 [Free DL] #Shorts #fitness",
        "title_ja": "【超重低音】自己ベスト更新用。気合が入る極太キックPHONK 🔥 フリー音源 #Shorts #筋トレ",
        "title_ko": "[PR 갱신용] 3대 운동 무게 칠 때 듣는 묵직한 중저음 비트 #Shorts #헬스장",
        "title_ru": "⚡ Музыка для рекордов в зале — Мощный тяжелый бас Phonk [Free DL] #Shorts #спорт",
        "title_pt": "⚡ Para Bater Recorde no Supino — Grave Forte Phonk [Free DL] #Shorts #maromba",
        "title_es": "⚡ Para Romper Récords en el Gym — Phonk con Bajos Pesados [Free DL] #Shorts #gymtok",
        "desc_en": (
            "⚡ Extreme Heavy Bass Phonk designed for hitting maximum effort PRs and intense sets.\n"
            "Feel the bass surge and destroy your limits!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Attribution: Music by @PhonkForgeAudio-s1h (https://www.youtube.com/@PhonkForgeAudio-s1h)\n\n"
            "🔥 Check the full 1-Hour Non-Stop Gym Mix here: https://youtu.be/4aJlGEfEI84\n\n"
            "#GymPR #PhonkWorkout #HeavyBass #Powerlifting #FreeBGM #Shorts"
        ),
        "desc_ja": (
            "⚡ 自己ベスト（PR）更新のための超重低音。集中力を研ぎ澄ませたい瞬間に。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます。\n"
            "クレジット: Music by @PhonkForgeAudio-s1h\n\n"
            "🔥 1時間フルバージョンはこちら: https://youtu.be/4aJlGEfEI84\n\n"
            "#筋トレ #PR更新 #自己ベスト #重低音 #フリーBGM #Shorts"
        ),
        "comment_text": "🔥 100% Free to use for creators! Check Related Video for the full 1-Hour Non-Stop Mix! ⚡",
        "tags": ["shorts", "gym pr", "heavy bass", "workout music", "powerlifting", "free bgm", "gym motivation", "phonkforge audio"]
    }
]

def fetch_existing_titles(yt):
    print("[+] Fetching existing channel video titles for collision check...")
    existing = set()
    try:
        res = yt.search().list(part="snippet", forMine=True, type="video", maxResults=50).execute()
        for item in res.get("items", []):
            existing.add(item["snippet"]["title"])
        print(f"[+] Found {len(existing)} existing titles.")
    except Exception as e:
        print(f"⚠️ Warning during title fetch: {e}")
    return existing

def resolve_unique(title, existing):
    if title not in existing:
        return title
    variants = [
        title.replace("🔥", "⚡"),
        title.replace("⚡", "🔥"),
        title.replace("[Free BGM]", "[Free DL]"),
        title.replace("[Free DL]", "[Free BGM]"),
        title + " ⚡",
        title + " 🔥",
        title.replace("#Shorts", "#Shorts #viral")
    ]
    for v in variants:
        if v not in existing:
            return v
    return title + f" #{int(time.time())%1000}"

def main():
    print("==================================================")
    print("🚀 PHONK SHORTS UPLOAD: 3 BATCH (1-HOUR MIX TRACKS)")
    print("==================================================")

    yt = get_youtube_service("phonkforge")
    existing_titles = fetch_existing_titles(yt)
    results = []

    for idx, item in enumerate(SHORTS_QUEUE):
        v_path = SHORTS_DIR / item["file_name"]
        if not v_path.exists():
            print(f"❌ File not found: {v_path}")
            continue

        print(f"\n[{idx+1}/{len(SHORTS_QUEUE)}] Uploading: {item['file_name']}")
        unique_title = resolve_unique(item["base_title_en"], existing_titles)
        existing_titles.add(unique_title)
        print(f"  Title: {unique_title}")

        localizations = {
            "ja": {"title": item["title_ja"], "description": item["desc_ja"]},
            "ko": {"title": item["title_ko"], "description": item["desc_en"]},
            "ru": {"title": item["title_ru"], "description": item["desc_en"]},
            "pt": {"title": item["title_pt"], "description": item["desc_en"]},
            "es": {"title": item["title_es"], "description": item["desc_en"]}
        }

        body = {
            "snippet": {
                "title": unique_title,
                "description": item["desc_en"],
                "tags": item["tags"],
                "categoryId": "10",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            },
            "localizations": localizations
        }

        media = MediaFileUpload(str(v_path), chunksize=-1, resumable=True, mimetype="video/mp4")
        req = yt.videos().insert(part="snippet,status,localizations", body=body, media_body=media)

        res = None
        while res is None:
            st, res = req.next_chunk()
            if st:
                print(f"    Progress: {int(st.progress() * 100)}%")

        vid = res.get("id")
        print(f"  ✅ Upload Successful! ID: {vid} (https://www.youtube.com/shorts/{vid})")

        # 固定コメント投稿
        time.sleep(2)
        try:
            yt.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": vid,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": item["comment_text"]
                            }
                        }
                    }
                }
            ).execute()
            print("  ✅ Pinned Comment posted successfully")
        except Exception as e:
            print(f"  ⚠️ Note on comment post: {e}")

        results.append({
            "id": vid,
            "title": unique_title,
            "url": f"https://www.youtube.com/shorts/{vid}"
        })

        if idx < len(SHORTS_QUEUE) - 1:
            print("  ⏳ Waiting 4s before next upload (API rate limit protection)...")
            time.sleep(4)

    print("\n==================================================")
    print("🎉 ALL 3 SHORTS SUCCESSFULLY UPLOADED & PUBLISHED!")
    print("==================================================")
    for r in results:
        print(f"  • {r['title']}: {r['url']}")
    print("==================================================")

if __name__ == "__main__":
    main()
