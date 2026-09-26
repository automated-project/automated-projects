#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EDM長尺動画 再予約投稿スクリプト
1. 旧動画 (zcatpNWshKw: 再生数0) の削除
2. 新規アップロード & 予約投稿 (今夜 20:00 JST / 11:00 UTC / EDT 07:00 朝ピーク直撃)
3. サムネイル設定
4. 各Shorts動画 (7本) のコメント欄の長尺URL更新
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube")
OUTPUT_DIR = BASE_DIR / "output_edm"
ENV_PATH = Path("/Users/base/Automated-Projects/Game-Music/.env")

load_dotenv(ENV_PATH)

CLIENT_ID = os.getenv("ACCOUNT_4_YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("ACCOUNT_4_YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("ACCOUNT_4_YOUTUBE_REFRESH_TOKEN")

OLD_VIDEO_ID = "zcatpNWshKw"

# 予約投稿日時: 日本時間 2026年9月13日 20:00 (JST) = UTC 2026-09-13 11:00:00
# 米国東部時間 (EDT) 朝 07:00 のモーニングピーク
PUBLISH_AT = "2026-09-13T11:00:00Z"

TRACK_TIMESTAMPS = [
    ("0:00", "Crush The Bone", "Aggressive Gym Phonk / Hardstyle"),
    ("2:56", "The Iron Ascent", "Heavy Power Hardstyle / Bass"),
    ("5:58", "Midnight Asphalt Burn", "Brazilian Drift Phonk / Bass"),
    ("8:53", "Asphalt Redline", "High-Octane Speed Phonk"),
    ("11:52", "Asphalt Teeth", "Dark Metal Phonk / Heavy Bass"),
    ("14:51", "Kingdom Of My Own", "Epic Melodic EDM / Power Synth"),
    ("17:38", "Midnight Redline", "Phonk Hardstyle / Night Velocity")
]

SHORTS_IDS = [
    "LyGR33vwVkg", "vm9JiXysQlY", "3s0FSsTcakQ", 
    "pcb5BYb4jkQ", "KUsaXidkYpI", "O29AkKy3Lp4", "3aoqyLJ13VU"
]

def get_youtube():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return build("youtube", "v3", credentials=creds)

def main():
    youtube = get_youtube()

    # 1. 旧動画の削除
    print(f"🗑️ 旧動画 ({OLD_VIDEO_ID}) を削除中...")
    try:
        youtube.videos().delete(id=OLD_VIDEO_ID).execute()
        print(f"✅ 旧動画 ({OLD_VIDEO_ID}) の削除完了")
    except Exception as e:
        print(f"注: 旧動画削除エラー (既にない可能性): {e}")

    # 2. 新規動画のアップロード & 予約投稿
    long_video_path = OUTPUT_DIR / "workout_edm_longform_20min.mp4"
    thumb_path = OUTPUT_DIR / "workout_edm_thumbnail.jpg"

    new_title = "[20 MIN WORK BGM] Heavy Gym & Gaming EDM Motivation | Aggressive Phonk & Bass (Work & Workout BGM)"

    timestamp_lines = "\n".join([f"{ts} 0{idx+1}. {title} ({genre})" for idx, (ts, title, genre) in enumerate(TRACK_TIMESTAMPS)])

    itch_url = "https://gameverse-audio.itch.io/game-music-vault"
    gumroad_url = "https://gameverseaudio.gumroad.com"

    new_desc = f"""🔥 Heavy Gym & Gaming EDM Compilation (20-Minute High-Energy Work & Workout BGM)

An unstoppable 20-minute continuous mix of aggressive phonk, heavy hardstyle, and distorted basslines. Perfect for deadlifts, PR sets, high-speed gaming, intense coding, and deep focus sessions.

⏱️ TRACKLIST & TIMESTAMPS:
{timestamp_lines}

📥 DOWNLOAD FULL UNCOMPRESSED LOSSLESS MASTERS & LICENSE:
👉 itch.io Vault (All Tracks): {itch_url}
👉 Gumroad Store: {gumroad_url}

💎 100% ROYALTY-FREE & COMMERCIAL USE:
All tracks produced by GameVerse Audio. Free to use in your monetized YouTube videos, Twitch streams, fitness edits, and game projects!
- Credit: "Music: GameVerse Audio"
- No copyright strikes ever.

🔔 Subscribe to GameVerse Audio for weekly high-energy gaming & workout soundtracks!

#WorkoutMusic #GymPhonk #GymEDM #WorkoutMotivation #Hardstyle #BeastMode #GamingMusic #WorkBGM #RoyaltyFreeMusic #GameVerseAudio"""

    tags = [
        "Workout Music", "Gym Phonk", "Gym EDM", "Gaming Music", "Work BGM",
        "Workout Motivation", "Hardstyle", "Brazilian Drift Phonk", "Beast Mode",
        "Fitness Music", "Deadlift Motivation", "Royalty Free Gym Music", "GameVerse Audio"
    ]

    print(f"\n🚀 新規長尺動画をアップロード & 予約投稿中...")
    print(f"公開予定時刻: {PUBLISH_AT} (日本時間 今夜 20:00 JST / 米国東部朝 07:00 EDT)")
    print(f"タイトル: {new_title}")

    body = {
        "snippet": {
            "title": new_title,
            "description": new_desc,
            "tags": tags,
            "categoryId": "10"
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": PUBLISH_AT,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(str(long_video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    res = req.execute()
    new_video_id = res.get("id")
    new_url = f"https://youtu.be/{new_video_id}"
    print(f"✅ アップロード＆予約投稿設定完了！ ID: {new_video_id}")
    print(f"URL: {new_url}")

    # 3. サムネイル設定
    print("🖼️ サムネイルを設定中...")
    try:
        req = youtube.thumbnails().set(videoId=new_video_id, media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg"))
        req.execute()
        print("✅ サムネイル設定完了！")
    except Exception as e:
        print(f"注: サムネイル設定エラー: {e}")

    # 4. 各Shorts動画 (7本) のコメント欄のURLを新動画に更新
    print("\n📱 Shorts動画 (7本) のコメント欄の長尺URLを更新中...")
    shorts_comment = f"""🔥 Watch the Full 20-Minute Continuous BGM Mix (Premiere Tonight 8PM JST / 7AM EDT):
👉 {new_url}

📥 DOWNLOAD LOSSLESS AUDIO MASTERS & LICENSE:
🎮 itch.io Vault: {itch_url}
💎 Gumroad: {gumroad_url}

⚡ 100% Royalty-Free for your videos & game projects!"""

    for vid in SHORTS_IDS:
        try:
            c_res = youtube.commentThreads().list(part="snippet", videoId=vid).execute()
            items = c_res.get("items", [])
            if items:
                cid = items[0]["snippet"]["topLevelComment"]["id"]
                youtube.comments().update(
                    part="snippet",
                    body={"id": cid, "snippet": {"textOriginal": shorts_comment}}
                ).execute()
                print(f"  ✅ Shorts {vid} のコメント更新完了")
        except Exception as e:
            print(f"  注: Shorts {vid} コメント更新エラー: {e}")

    print("\n==================================================")
    print("🎉 再予約投稿 & 連携更新がすべて完了しました！")
    print(f"新・長尺動画URL: {new_url}")
    print(f"公開日時: 2026-09-13 20:00 JST (EDT 07:00 モーニングピーク)")
    print("==================================================")

if __name__ == "__main__":
    main()
