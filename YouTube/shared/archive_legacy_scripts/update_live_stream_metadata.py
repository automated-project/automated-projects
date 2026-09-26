# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio) 24/7 ライブ配信メタデータ & サムネイル更新スクリプト
"""
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

BROADCAST_ID = "bGypKuKwbow"
THUMBNAIL_PATH = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/output_videos/thumbnails/THUMBNAIL_01_PURE_UPLIFTING.jpg")

TITLE = "24/7 MELODIC EDM & PROGRESSIVE HOUSE RADIO ✨ Uplifting BGM for Coding, Gaming & Deep Focus"

DESCRIPTION = """✨ Welcome to 24/7 AuraMelody Audio Live Radio!
Your non-stop sanctuary for beautiful Melodic EDM, Uplifting Progressive House, and Summer Vibes.

🎧 Perfect for: Coding, Gaming, Studying, Driving, and Creative Flow.

━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ ABOUT AURAMELODY AUDIO
Delivering crystal-clear melodies, euphoric synth drops, and uplifting rhythms to elevate your mood and energy 24/7.
All tracks are 100% original, seamlessly mixed and mastered for pure sonic clarity.

━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 EXPLORE OUR SISTER CHANNELS:
🌿 Cozy Lofi & Pomodoro Study ➡️ @Haven-Chill-Audio
https://www.youtube.com/@Haven-Chill-Audio

🔥 Heavy Bass & Gym Phonk ➡️ @PhonkForgeAudio-s1h
https://www.youtube.com/@PhonkForgeAudio-s1h
━━━━━━━━━━━━━━━━━━━━━━━━━━

#MelodicEDM #ProgressiveHouse #LiveStream #247Radio #CodingMusic #GamingBGM #UpliftingEDM #EDMRadio
"""

TAGS = [
    "melodic edm", "progressive house", "24/7 radio", "live stream",
    "uplifting edm", "coding bgm", "gaming music", "study music",
    "deep focus", "summer edm", "auramelody audio", "作業用bgm", "ドライブbgm"
]

print("🔐 Authenticating with YouTube Data API (auramelody)...")
yt = get_youtube_service("auramelody")

# 1. videos().update によるメタデータ更新
print(f"📝 Updating video metadata for {BROADCAST_ID}...")
try:
    video_body = {
        "id": BROADCAST_ID,
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": "10",  # Music
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        }
    }
    video_res = yt.videos().update(part="snippet", body=video_body).execute()
    print("✅ Video metadata updated successfully!")
    print(f"  New Title: {video_res['snippet']['title']}")
except Exception as e:
    print(f"⚠️ Video update notice: {e}")

# 2. liveBroadcasts().update によるライブ配信メタデータ更新
print(f"📡 Updating liveBroadcasts metadata for {BROADCAST_ID}...")
try:
    broadcast_body = {
        "id": BROADCAST_ID,
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "scheduledStartTime": "2026-09-21T00:00:00Z"
        }
    }
    b_res = yt.liveBroadcasts().update(part="snippet", body=broadcast_body).execute()
    print("✅ Live Broadcast metadata updated successfully!")
except Exception as e:
    print(f"⚠️ Live broadcast update notice: {e}")

# 3. サムネイル設定
if THUMBNAIL_PATH.exists():
    print(f"🖼️ Setting Official Thumbnail: {THUMBNAIL_PATH.name}...")
    try:
        thumb_media = MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
        thumb_res = yt.thumbnails().set(videoId=BROADCAST_ID, media_body=thumb_media).execute()
        print("✅ Official Thumbnail set successfully!")
    except Exception as e:
        print(f"❌ Thumbnail update error: {e}")
else:
    print(f"❌ Thumbnail not found: {THUMBNAIL_PATH}")

print("\n🎉 Live stream metadata update completed successfully!")
print(f"🔗 URL: https://youtu.be/{BROADCAST_ID}")
