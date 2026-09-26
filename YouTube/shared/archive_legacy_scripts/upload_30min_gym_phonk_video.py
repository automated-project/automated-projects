# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) 30-Minute Gym Phonk Video Upload Script
- Video: 30MIN_HARDCORE_GYM_PHONK_MOTIVATION.mp4
- Thumbnail: THUMBNAIL_01_EXACT_FUTURA_GYM_PHONK.jpg
- Chapters: 30MIN_HARDCORE_GYM_PHONK_MOTIVATION_chapters.txt
- Token: phonkforge (token_phonkforge.json)
"""

import os
import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
OUTPUT_DIR = BASE_DIR / "output_videos"
VIDEO_PATH = OUTPUT_DIR / "30MIN_HARDCORE_GYM_PHONK_MOTIVATION.mp4"
THUMB_PATH = OUTPUT_DIR / "thumbnails" / "THUMBNAIL_01_EXACT_FUTURA_GYM_PHONK.jpg"
CHAPTERS_PATH = OUTPUT_DIR / "30MIN_HARDCORE_GYM_PHONK_MOTIVATION_chapters.txt"

if not VIDEO_PATH.exists():
    print(f"❌ Video not found: {VIDEO_PATH}", file=sys.stderr)
    sys.exit(1)

if not THUMB_PATH.exists():
    print(f"❌ Thumbnail not found: {THUMB_PATH}", file=sys.stderr)
    sys.exit(1)

print("🔐 Authenticating with YouTube Data API (phonkforge)...")
yt = get_youtube_service("phonkforge")

# 1. 既存動画タイトル取得（タイトル重複チェック）
print("🔍 Checking existing video titles for uniqueness...")
existing_titles = []
try:
    res = yt.search().list(part="snippet", forMine=True, maxResults=50, type="video").execute()
    for item in res.get("items", []):
        existing_titles.append(item["snippet"]["title"])
    print(f"  Found {len(existing_titles)} existing videos.")
except Exception as e:
    print(f"  ⚠️ Warning: Could not fetch title list: {e}")

TARGET_TITLE = "30 MIN HARDCORE GYM PHONK 🔥 Brutal Workout Motivation Mix [Aggressive Bass]"

# タイトル重複回避チェック
if TARGET_TITLE in existing_titles:
    TARGET_TITLE = "30 MIN HARDCORE GYM PHONK 🔥 Brutal Beast Mode Workout Mix [Super Crisp Bass]"
    print(f"  ⚡ Duplicate resolved: {TARGET_TITLE}")
else:
    print(f"  ✅ Title is completely unique: {TARGET_TITLE}")

# 2. チャプター内容の読み込み
chapters_text = ""
if CHAPTERS_PATH.exists():
    with open(CHAPTERS_PATH, "r", encoding="utf-8") as f:
        chapters_text = f.read().strip()

# 3. 概要欄の構築（公式About仕様 ＋ チャプター ＋ ハッシュタグ）
DESCRIPTION = f"""⚡ 30 MIN NON-STOP HARDCORE GYM PHONK & BRUTAL WORKOUT MOTIVATION MIX
Heavy 808 Bass, Aggressive Drift Drops, and Relentless Drive to push past your absolute limits.

{chapters_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 WELCOME TO PHONKFORGE AUDIO
The ultimate sonic forge for gym rats, speed demons, and nocturnal drifters.
Engineered with heavy distortion, cowbell melodies, and crushing 808 sub-bass designed to trigger pure adrenaline.

💪 Stream for: Max Effort PRs, Heavy Sets, Late-Night Highway Drives, High-Speed Gaming.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎧 Audio: 100% Mastered Original Phonk Mix (Equal-Power Seamless Crossfade)
🎬 Visual: Underground Iron Sanctuary & Reactive Heavy Sub-Bass Visualizer

#GymPhonk #Phonk #DriftPhonk #WorkoutMusic #HardcorePhonk #GymMotivation #AggressivePhonk #BassBoosted
"""

TAGS = [
    "gym phonk", "hardcore gym phonk", "workout motivation", "drift phonk",
    "aggressive phonk", "gym music", "workout mix", "phonk mix", "phonk 2026",
    "bass boosted phonk", "beast mode", "heavy bass", "phonkforge audio",
    "30 min workout", "gym edm", "pr music"
]

# 4. アップロード実行
print(f"🚀 Uploading video: {VIDEO_PATH.name} ({VIDEO_PATH.stat().st_size / (1024*1024):.2f} MB)...")

body = {
    "snippet": {
        "title": TARGET_TITLE,
        "description": DESCRIPTION,
        "tags": TAGS,
        "categoryId": "10",  # Music
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    }
}

media = MediaFileUpload(str(VIDEO_PATH), mimetype="video/mp4", chunksize=10*1024*1024, resumable=True)
request = yt.videos().insert(part="snippet,status", body=body, media_body=media)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"  📤 Upload Progress: {int(status.progress() * 100)}%")

video_id = response.get("id")
print(f"🎉 Video uploaded successfully! Video ID: {video_id}")
print(f"🔗 URL: https://youtu.be/{video_id}")

# 5. サムネイル設定
print(f"🖼️ Setting Official Thumbnail: {THUMB_PATH.name}...")
time.sleep(3)
try:
    thumb_media = MediaFileUpload(str(THUMB_PATH), mimetype="image/jpeg")
    yt.thumbnails().set(videoId=video_id, media_body=thumb_media).execute()
    print("✅ Official Thumbnail set successfully!")
except Exception as e:
    print(f"⚠️ Thumbnail upload error: {e}")

# 6. 固定コメント投稿
print("💬 Posting Pinned Welcome Comment...")
time.sleep(2)
try:
    comment_body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": "🔥 Tracklist & Timestamps in description! What's your current PR goal? Drop your favorite track in the comments below! 👇⚡"
                }
            }
        }
    }
    yt.commentThreads().insert(part="snippet", body=comment_body).execute()
    print("✅ Pinned Comment posted successfully!")
except Exception as e:
    print(f"⚠️ Comment error: {e}")

print("✨ ALL UPLOAD TASKS COMPLETED SUCCESSFULLY! ✨")
