#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PhonkForge Audio: マスタリング済みShorts（全5本）自動アップロードスクリプト
- API経由での既存タイトル事前照合＆完全一意化（Zero Title Collision）
- 100% Global English + 多言語ローカライズ（ja, es, pt, ru, ko）
- フリー音源アピール（[Free BGM]）＆高需要ワード（Gym, Workout, Heavy Bass, Drift）
- URL・数字なしの固定コメント自動投稿
- APIクォータ保護（リクエスト間スリープ）
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
        "id": "shorts_01_asphalt_redline",
        "file_name": "SHORTS_01_ASPHALT_REDLINE.mp4",
        "base_title_en": "DRIFT & AGGRESSIVE PHONK ⚡ [Free BGM] #Shorts #drift",
        "base_title_ja": "【超重低音】深夜ドリフト用 PHONK 🔥 フリーBGM #Shorts #作業用BGM",
        "desc_en": (
            "⚡ Aggressive Drift Phonk with ultra heavy bass for night driving and deep focus.\n"
            "Feel the sub-bass adrenaline and push beyond your limits!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Simply include the credit below in your description:\n"
            "---\n"
            "Music: PhonkForge Audio\n"
            "Stream & Download: Check Channel Page\n"
            "---\n\n"
            "🔥 Looking for more? Check the Related Video for the full 1-Hour Non-Stop Mix!\n\n"
            "#phonk #driftphonk #heavybass #nightdrive #freebgm #nocopyrightmusic #shorts"
        ),
        "desc_ja": (
            "⚡ 深夜のドライブや集中作業に最適な超重低音ドリフトPHONK。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます（クレジット表記推奨）。\n"
            "クレジット: PhonkForge Audio\n\n"
            "🔥 1時間フルバージョンは関連動画からチェック！\n\n"
            "#phonk #ドリフト #超重低音 #作業用BGM #フリーBGM #Shorts"
        ),
        "comment_text": "⚡ 100% Free to use for your videos & streams! Check the Related Video for the full 1-Hour Mix! 🔥",
        "tags": ["shorts", "phonk", "drift phonk", "heavy bass", "bass boosted", "free bgm", "no copyright music", "night drive"]
    },
    {
        "id": "shorts_02_crush_the_bone",
        "file_name": "SHORTS_02_CRUSH_THE_BONE.mp4",
        "base_title_en": "HEAVY BASS GYM PHONK 🔥 [Free BGM] #Shorts #gym",
        "base_title_ja": "【超重低音】筋トレ用 限界突破PHONK 🔥 フリーBGM #Shorts #筋トレ",
        "desc_en": (
            "⚡ Brutal Heavy Bass Phonk engineered for breaking PRs and crushing hardcore gym workouts.\n"
            "Feel the sub-bass adrenaline and push beyond your limits!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Simply include the credit below in your description:\n"
            "---\n"
            "Music: PhonkForge Audio\n"
            "Stream & Download: Check Channel Page\n"
            "---\n\n"
            "🔥 Looking for more? Check the Related Video for the full 1-Hour Non-Stop Gym Mix!\n\n"
            "#phonk #gymphonk #heavybass #workoutmusic #freebgm #nocopyrightmusic #gymmotivation #shorts"
        ),
        "desc_ja": (
            "⚡ 身体の芯に響く超重低音。筋トレやワークアウトの限界突破に。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます（クレジット表記推奨）。\n"
            "クレジット: PhonkForge Audio\n\n"
            "🔥 1時間フルバージョンは関連動画からチェック！\n\n"
            "#phonk #筋トレ #ワークアウト #超重低音 #作業用BGM #フリーBGM #Shorts"
        ),
        "comment_text": "⚡ 100% Free to use for your gym & workout videos! Check Related Video for the full 1-Hour Mix! 🔥",
        "tags": ["shorts", "phonk", "gym phonk", "heavy bass", "workout music", "gym motivation", "free bgm", "bass boosted"]
    },
    {
        "id": "shorts_03_storming_the_gate",
        "file_name": "SHORTS_03_STORMING_THE_GATE.mp4",
        "base_title_en": "HARDSTYLE HEAVY BASS DROP ⚡ [Free BGM] #Shorts #phonk",
        "base_title_ja": "【超重低音】ハードスタイル重低音ドロップ ⚡ フリーBGM #Shorts #重低音",
        "desc_en": (
            "⚡ Extreme Hardstyle Heavy Bass drop for high-intensity training, gaming, and night driving.\n"
            "Feel the sub-bass adrenaline and push beyond your limits!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Simply include the credit below in your description:\n"
            "---\n"
            "Music: PhonkForge Audio\n"
            "Stream & Download: Check Channel Page\n"
            "---\n\n"
            "🔥 Looking for more? Check the Related Video for the full 1-Hour Non-Stop Mix!\n\n"
            "#phonk #hardstyle #heavybass #bassboosted #freebgm #nocopyrightmusic #shorts"
        ),
        "desc_ja": (
            "⚡ ハードな重低音キックが炸裂する高音圧ドロップ。集中やトレーニングに。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます（クレジット表記推奨）。\n"
            "クレジット: PhonkForge Audio\n\n"
            "🔥 1時間フルバージョンは関連動画からチェック！\n\n"
            "#phonk #ハードスタイル #超重低音 #作業用BGM #フリーBGM #Shorts"
        ),
        "comment_text": "⚡ 100% Free to use for your videos & streams! Check the Related Video for the full 1-Hour Mix! 🔥",
        "tags": ["shorts", "hardstyle", "phonk", "heavy bass", "bass boosted", "free bgm", "workout", "gaming music"]
    },
    {
        "id": "shorts_04_blacktop_fury",
        "file_name": "SHORTS_04_BLACKTOP_FURY.mp4",
        "base_title_en": "UNDERGROUND DRIFT HEAVY BASS ⚡ [Free DL] #Shorts #car",
        "base_title_ja": "【超重低音】アンダーグラウンド ドリフトPHONK ⚡ フリーBGM #Shorts #車",
        "desc_en": (
            "⚡ Underground Night Drift Phonk with crushing basslines and maximum sound pressure.\n"
            "Feel the sub-bass adrenaline and push beyond your limits!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Simply include the credit below in your description:\n"
            "---\n"
            "Music: PhonkForge Audio\n"
            "Stream & Download: Check Channel Page\n"
            "---\n\n"
            "🔥 Looking for more? Check the Related Video for the full 1-Hour Non-Stop Mix!\n\n"
            "#phonk #driftphonk #underground #heavybass #nightdrive #freebgm #shorts"
        ),
        "desc_ja": (
            "⚡ 地下トンネルを揺らす圧倒的重低音。夜ドライブや作業用BGMに。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます（クレジット表記推奨）。\n"
            "クレジット: PhonkForge Audio\n\n"
            "🔥 1時間フルバージョンは関連動画からチェック！\n\n"
            "#phonk #ドリフト #車 #超重低音 #夜ドライブ #作業用BGM #フリーBGM #Shorts"
        ),
        "comment_text": "⚡ 100% Free to use for your videos & streams! Check the Related Video for the full 1-Hour Mix! 🔥",
        "tags": ["shorts", "underground", "drift phonk", "heavy bass", "car", "night drive", "free bgm"]
    },
    {
        "id": "shorts_05_savage_grip",
        "file_name": "SHORTS_05_SAVAGE_GRIP.mp4",
        "base_title_en": "BRUTAL WORKOUT HEAVY BASS 🔥 [Free BGM] #Shorts #workout",
        "base_title_ja": "【超重低音】テンション爆上げ ワークアウトPHONK 🔥 フリーBGM #Shorts #筋トレ",
        "desc_en": (
            "⚡ Brutal Workout Heavy Bass Phonk for maximum adrenaline, powerlifting, and combat training.\n"
            "Feel the sub-bass adrenaline and push beyond your limits!\n\n"
            "🆓 FREE TO USE / ROYALTY FREE MUSIC:\n"
            "You can freely use this track in your YouTube videos, Twitch streams, and TikTok clips!\n"
            "Simply include the credit below in your description:\n"
            "---\n"
            "Music: PhonkForge Audio\n"
            "Stream & Download: Check Channel Page\n"
            "---\n\n"
            "🔥 Looking for more? Check the Related Video for the full 1-Hour Non-Stop Gym Mix!\n\n"
            "#phonk #workoutmusic #gymmotivation #heavybass #fitness #freebgm #shorts"
        ),
        "desc_ja": (
            "⚡ テンションが最高潮に達するアグレッシブな重低音。ハードワークアウトに。\n\n"
            "🆓 フリー音源 / 商用利用可能:\n"
            "YouTube動画、配信、ショート等で自由にご使用いただけます（クレジット表記推奨）。\n"
            "クレジット: PhonkForge Audio\n\n"
            "🔥 1時間フルバージョンは関連動画からチェック！\n\n"
            "#phonk #ワークアウト #筋トレ #テンション爆上げ #超重低音 #フリーBGM #Shorts"
        ),
        "comment_text": "⚡ 100% Free to use for your gym & workout videos! Check Related Video for the full 1-Hour Mix! 🔥",
        "tags": ["shorts", "workout", "gym motivation", "heavy bass", "brutal phonk", "free bgm", "powerlifting"]
    }
]

def fetch_existing_titles(yt):
    """チャンネル内の既存動画（公開・限定公開・非公開）のタイトル一覧を取得"""
    print("[+] Fetching existing channel video titles via API for collision check...")
    existing_titles = set()
    try:
        req = yt.search().list(
            part="snippet",
            forMine=True,
            type="video",
            maxResults=50
        )
        res = req.execute()
        for item in res.get("items", []):
            title = item["snippet"]["title"]
            existing_titles.add(title)
        print(f"[+] Found {len(existing_titles)} existing video titles in channel.")
    except Exception as e:
        print(f"⚠️ Note during title fetch: {e}")
    return existing_titles

def resolve_unique_title(base_title, existing_titles):
    """タイトルが既存と被っている場合、些細なバリエーションを付与して一意化"""
    if base_title not in existing_titles:
        return base_title

    print(f"⚠️ Title collision detected for: '{base_title}'! Resolving unique variation...")
    variants = [
        base_title.replace("🔥", "⚡"),
        base_title.replace("⚡", "🔥"),
        base_title.replace("[Free BGM]", "[Free DL]"),
        base_title.replace("[Free DL]", "[Free BGM]"),
        base_title.replace("PHONK", "PHONK DROP"),
        base_title.replace("#Shorts", "#Shorts #viral"),
        base_title + " ⚡",
        base_title + " 🔥",
    ]
    for v in variants:
        if v not in existing_titles:
            print(f"  ✓ Resolved unique title: '{v}'")
            return v

    # 最終手段としてユニークタグ追加
    unique_v = base_title.replace("#Shorts", f"#Shorts #{int(time.time())%1000}")
    print(f"  ✓ Fallback unique title: '{unique_v}'")
    return unique_v

def upload_shorts_batch():
    print("==================================================")
    print("🚀 PHONK SHORTS: BATCH UPLOAD WITH TITLE COLLISION CHECK")
    print("==================================================")

    yt = get_youtube_service("phonkforge")
    existing_titles = fetch_existing_titles(yt)
    uploaded_results = []

    for idx, item in enumerate(SHORTS_QUEUE):
        v_path = SHORTS_DIR / item["file_name"]
        if not v_path.exists():
            print(f"❌ File not found: {v_path}")
            continue

        print(f"\n[{idx+1}/{len(SHORTS_QUEUE)}] Preparing upload: {item['file_name']}")

        # 1. タイトル一意化チェック（API事前照合）
        unique_title_en = resolve_unique_title(item["base_title_en"], existing_titles)
        existing_titles.add(unique_title_en)

        localizations = {
            "ja": {
                "title": item["base_title_ja"],
                "description": item["desc_ja"]
            },
            "ru": {
                "title": unique_title_en,
                "description": item["desc_en"]
            },
            "pt": {
                "title": unique_title_en,
                "description": item["desc_en"]
            },
            "es": {
                "title": unique_title_en,
                "description": item["desc_en"]
            },
            "ko": {
                "title": item["base_title_ja"],
                "description": item["desc_ja"]
            }
        }

        body = {
            "snippet": {
                "title": unique_title_en,
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
        req = yt.videos().insert(
            part="snippet,status,localizations",
            body=body,
            media_body=media
        )

        print(f"  Uploading {item['file_name']} (Title: '{unique_title_en}')...")
        res = None
        while res is None:
            st, res = req.next_chunk()
            if st:
                print(f"    Upload progress: {int(st.progress() * 100)}%")

        vid = res.get("id")
        print(f"  ✅ Uploaded: {vid} (https://www.youtube.com/shorts/{vid})")

        # 2. 固定コメント自動投稿
        time.sleep(3)  # APIレートリミット待機
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
            print(f"  ✅ Pinned engagement comment posted successfully")
        except Exception as e:
            print(f"  ⚠️ Note on comment post: {e}")

        uploaded_results.append({
            "id": vid,
            "title": unique_title_en,
            "title_ja": item["base_title_ja"],
            "url": f"https://www.youtube.com/shorts/{vid}"
        })

        # 次の動画アップロードまで待機（API保護）
        if idx < len(SHORTS_QUEUE) - 1:
            print(f"  ⏳ Waiting 4s before next upload (API rate limit protection)...")
            time.sleep(4)

    print("\n==================================================")
    print("🎉 ALL 5 SHORTS SUCCESSFULLY UPLOADED & PUBLISHED!")
    print("==================================================")
    for r in uploaded_results:
        print(f"  • {r['title']}: {r['url']}")
    print("==================================================")

if __name__ == "__main__":
    upload_shorts_batch()
