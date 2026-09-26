#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GameVerse Audio (Account 4) ワークアウトEDMパッケージ 一括アップロードスクリプト
1. 20分ワークアウト長尺動画のアップロード & サムネイル設定 & 固定コメント投稿
2. 7曲のショート動画のアップロード & 本編への誘導リンク設定 & 固定コメント投稿
3. 台帳 (Game-Music/docs/VIDEOS_CHANNEL4.md) の自動更新
"""

import os
import sys
import json
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

TRACK_TIMESTAMPS = [
    ("0:00", "Crush The Bone", "Aggressive Gym Phonk / Hardstyle"),
    ("2:56", "The Iron Ascent", "Heavy Power Hardstyle / Bass"),
    ("5:58", "Midnight Asphalt Burn", "Brazilian Drift Phonk / Bass"),
    ("8:53", "Asphalt Redline", "High-Octane Speed Phonk"),
    ("11:52", "Asphalt Teeth", "Dark Metal Phonk / Heavy Bass"),
    ("14:51", "Kingdom Of My Own", "Epic Melodic EDM / Power Synth"),
    ("17:38", "Midnight Redline", "Phonk Hardstyle / Night Velocity")
]

SHORTS_DATA = [
    {
        "file": "short_01_Crush_The_Bone.mp4",
        "title": '[FREE BGM] "Crush The Bone" - Aggressive Phonk & Hardstyle EDM #Shorts',
        "track_name": "Crush The Bone",
        "genre": "Aggressive Gym Phonk / Hardstyle"
    },
    {
        "file": "short_02_The_Iron_Ascent.mp4",
        "title": '[FREE BGM] "The Iron Ascent" - Crushing Power Hardstyle EDM #Shorts',
        "track_name": "The Iron Ascent",
        "genre": "Heavy Power Hardstyle"
    },
    {
        "file": "short_03_Midnight_Asphalt_Burn.mp4",
        "title": '[FREE BGM] "Midnight Asphalt Burn" - Brazilian Drift Phonk EDM #Shorts',
        "track_name": "Midnight Asphalt Burn",
        "genre": "Brazilian Drift Phonk"
    },
    {
        "file": "short_04_Asphalt_Redline.mp4",
        "title": '[FREE BGM] "Asphalt Redline" - High-Octane Speed Phonk EDM #Shorts',
        "track_name": "Asphalt Redline",
        "genre": "High-Octane Speed Phonk"
    },
    {
        "file": "short_05_Asphalt_Teeth.mp4",
        "title": '[FREE BGM] "Asphalt Teeth" - Dark Metal Phonk & Heavy Bass EDM #Shorts',
        "track_name": "Asphalt Teeth",
        "genre": "Dark Metal Phonk"
    },
    {
        "file": "short_06_Kingdom_Of_My_Own.mp4",
        "title": '[FREE BGM] "Kingdom Of My Own" - Epic Power Synth EDM #Shorts',
        "track_name": "Kingdom Of My Own",
        "genre": "Epic Power Synth EDM"
    },
    {
        "file": "short_07_Midnight_Redline.mp4",
        "title": '[FREE BGM] "Midnight Redline" - Phonk Hardstyle Velocity EDM #Shorts',
        "track_name": "Midnight Redline",
        "genre": "Phonk Hardstyle"
    }
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

def upload_video_file(youtube, video_path, title, description, tags, privacy="public", publish_at=None, category_id="10"):
    status_dict = {
        "selfDeclaredMadeForKids": False
    }
    if publish_at:
        # YouTube Data API仕様: 予約投稿時はprivacyStatusを必ずprivateにする
        status_dict["privacyStatus"] = "private"
        status_dict["publishAt"] = publish_at
    else:
        status_dict["privacyStatus"] = privacy

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": status_dict
    }
    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    res = req.execute()
    return res.get("id")

def set_thumbnail(youtube, video_id, thumb_path):
    req = youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg"))
    req.execute()

def post_comment(youtube, video_id, comment_text):
    body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": comment_text
                }
            }
        }
    }
    youtube.commentThreads().insert(part="snippet", body=body).execute()

def main():
    print("==================================================")
    print("🚀 GameVerse Audio (Account 4) EDMアップロード開始")
    print("==================================================")

    youtube = get_youtube()
    ch = youtube.channels().list(mine=True, part="snippet").execute()
    channel_title = ch["items"][0]["snippet"]["title"]
    channel_id = ch["items"][0]["id"]
    print(f"接続先チャンネル: {channel_title} (ID: {channel_id})")
    assert "GameVerse" in channel_title, f"ERROR: Channel {channel_title} is not GameVerse Audio!"

    # 1. 長尺動画のアップロード
    long_video_path = OUTPUT_DIR / "workout_edm_longform_20min.mp4"
    thumb_path = OUTPUT_DIR / "workout_edm_thumbnail.jpg"

    assert long_video_path.exists(), f"ERROR: {long_video_path} does not exist!"
    assert thumb_path.exists(), f"ERROR: {thumb_path} does not exist!"

    long_title = "[20 MIN] Heavy Gym Workout EDM & Phonk BGM | Beast Mode Motivation"
    
    timestamp_lines = "\n".join([f"{ts} - {title} ({genre})" for ts, title, genre in TRACK_TIMESTAMPS])
    
    long_desc = f"""🔥 CRUSH THE BONE — Heavy Gym Workout EDM & Phonk Compilation (20-Minute Beast Mode Motivation)

Looking for unstoppable adrenaline for deadlifts, heavy bench press, and savage PR sets? This 20-minute non-stop mix delivers distorted 808s, aggressive basslines, and relentless hardstyle energy to keep you locked in the zone.

⏱️ TRACKLIST & TIMESTAMPS:
{timestamp_lines}

💎 100% ROYALTY-FREE & COMMERCIAL RIGHTS:
All tracks in this mix are free to use in your monetized YouTube videos, Twitch streams, fitness edits, and game projects!
- Credit: "Music: GameVerse Audio"
- No copyright strikes ever.

📥 DOWNLOAD THE FULL UNCOMPRESSED WAV MASTERS:
👉 https://gameverse-audio.itch.io/game-music-vault
👉 https://gameverseaudio.gumroad.com

🔔 Subscribe to GameVerse Audio for weekly royalty-free gym motivation, dark synthwave, and aggressive gaming soundtracks!

#WorkoutMusic #GymPhonk #GymEDM #WorkoutMotivation #Hardstyle #BeastMode #RoyaltyFreeMusic #GameVerseAudio #CrushTheBone"""

    long_tags = [
        "Workout Music", "Gym Phonk", "Gym EDM", "Workout Motivation", 
        "Crush The Bone", "Hardstyle", "Brazilian Drift Phonk", "Beast Mode",
        "Fitness Music", "Deadlift Motivation", "Royalty Free Gym Music", "GameVerse Audio"
    ]

    print("\n--------------------------------------------------")
    print("🎬 STEP 1: 20分長尺ワークアウト動画をアップロード中...")
    print(f"ファイル: {long_video_path.name}")
    print("--------------------------------------------------")
    long_video_id = upload_video_file(youtube, long_video_path, long_title, long_desc, long_tags)
    print(f"✅ 長尺動画アップロード成功！ ID: {long_video_id}")
    print(f"URL: https://youtu.be/{long_video_id}")

    # サムネイル設定
    print("サムネイルを設定中...")
    try:
        set_thumbnail(youtube, long_video_id, thumb_path)
        print("✅ サムネイル設定完了！")
    except Exception as e:
        print(f"注: サムネイル設定エラー: {e}")

    # 固定コメント
    itch_url = "https://gameverse-audio.itch.io/game-music-vault"
    gumroad_url = "https://gameverseaudio.gumroad.com"

    long_comment = (
        "🔥 Full 20-Minute Beast Mode BGM Mix! Which track gave you the biggest rush? Drop your favorite below! 👇\n\n"
        f"📥 DOWNLOAD LOSSLESS AUDIO MASTERS & COMMERCIAL LICENSE:\n"
        f"🎮 itch.io Vault: {itch_url}\n"
        f"💎 Gumroad: {gumroad_url}\n\n"
        "⚡ 100% Royalty-Free for your YouTube videos, Twitch streams & game projects! (Credit: 'GameVerse Audio')"
    )
    try:
        post_comment(youtube, long_video_id, long_comment)
        print("✅ 長尺動画へのコメント投稿完了！")
    except Exception as e:
        print(f"注: コメント投稿エラー: {e}")

    # 2. 7本のShorts動画をアップロード
    print("\n--------------------------------------------------")
    print("📱 STEP 2: 7曲のShorts動画をアップロード中...")
    print("--------------------------------------------------")
    shorts_results = []
    for idx, s in enumerate(SHORTS_DATA):
        short_file = OUTPUT_DIR / s["file"]
        short_title = s["title"]
        track_name = s["track_name"]
        genre = s["genre"]

        short_desc = f"""⚡ {track_name} — {genre} (High-Energy EDM BGM)

Need high-octane energy for your game, stream, or video?

🎧 WATCH THE FULL 20-MINUTE BGM MIX:
👉 https://youtu.be/{long_video_id}

📥 DOWNLOAD THE FULL UNCOMPRESSED WAV MASTERS:
👉 {itch_url}
👉 {gumroad_url}

💎 100% ROYALTY-FREE:
Free to use in monetized videos and streams with credit: "Music: GameVerse Audio"

#Shorts #EDM #GymPhonk #Hardstyle #BeastMode #GameVerseAudio #{track_name.replace(' ', '')}"""

        short_tags = [
            "EDM", "Gym Phonk", "Shorts", "Hardstyle", 
            "BeastMode", "Fitness", "GameVerse Audio", track_name
        ]

        print(f"[{idx+1}/7] アップロード中: {s['file']}...")
        short_id = upload_video_file(youtube, short_file, short_title, short_desc, short_tags)
        print(f"  ✅ Shortsアップロード成功！ ID: {short_id} (https://www.youtube.com/shorts/{short_id})")

        # Shortsへのコメント投稿
        short_comment = (
            f"🔥 Watch the Full 20-Minute Continuous BGM Mix:\n"
            f"👉 https://youtu.be/{long_video_id}\n\n"
            f"📥 DOWNLOAD LOSSLESS AUDIO MASTERS & LICENSE:\n"
            f"🎮 itch.io Vault: {itch_url}\n"
            f"💎 Gumroad: {gumroad_url}\n\n"
            f"⚡ 100% Royalty-Free for your videos & game projects!"
        )
        try:
            post_comment(youtube, short_id, short_comment)
        except Exception as e:
            pass

        shorts_results.append({
            "track": track_name,
            "id": short_id,
            "url": f"https://www.youtube.com/shorts/{short_id}"
        })
        time.sleep(2)

    print("\n==================================================")
    print("🎉 すべてのアップロードが完了しました！")
    print(f"本編長尺URL: https://youtu.be/{long_video_id}")
    for sr in shorts_results:
        print(f"- {sr['track']}: {sr['url']}")
    print("==================================================")

if __name__ == "__main__":
    main()
