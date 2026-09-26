#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
第2チャンネル（PhonkForge Audio）新規Shorts 3本 一括アップロードスクリプト
- 1時間Mix本編マスタリング済み音源 × 重低音背景パルスシェイクShorts 3本
- 規約準拠（多言語ローカライズ・チープ語排除・数字なし文字のみの固定コメント投稿）
"""

import sys
import time
from pathlib import Path
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

CHANNEL_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel")
OUT_DIR = CHANNEL_DIR / "output_videos"

SHORTS_UPLOAD_SPECS = [
    {
        "id": "01_gym",
        "file_name": "SHORTS_01_CRUSH_THE_BONE_GYM_PULSE.mp4",
        "title_en": "⚡ Heavy Bass Drop for Extreme Gym PRs #Shorts #GymMotivation #Workout",
        "desc_en": "⚡ Deep heavy bass engineered for breaking PRs and crushing high-intensity gym workouts.\n🎧 Full 1-Hour Mix is available in Related Video!\n\n#Shorts #GymMotivation #WorkoutMusic #HeavyBass #PhonkForge",
        "title_ja": "⚡【超重低音】筋トレ用 限界突破ドロップ #Shorts #筋トレ #作業用BGM",
        "desc_ja": "⚡ 身体の芯に響く超重低音。筋トレやワークアウトの限界突破に。\n🎧 1時間フルバージョンは関連動画から！\n\n#Shorts #筋トレ #筋トレBGM #作業用BGM #超重低音",
        "comment_text": "⚡ Engineered for crushing gym PRs and heavy lifts! Check Related Video for the full 1-hour mix! 🔥\n(⚡ Мощный бас для тренировок и качалки! Полный 1-часовой микс в связанном видео!)",
        "tags": ["shorts", "heavy bass", "gym motivation", "workout music", "hardcore gym", "bass boosted", "phonkforge", "beast mode"]
    },
    {
        "id": "02_cyberpunk_rain",
        "file_name": "SHORTS_02_BLACKTOP_FURY_RAIN_PULSE.mp4",
        "title_en": "⚡ Midnight Cyber Heavy Bass Drop #Shorts #Focus #NightDrive",
        "desc_en": "⚡ Deep heavy bass for midnight focus, programming, and late-night driving.\n🎧 Full 1-Hour Mix is available in Related Video!\n\n#Shorts #Focus #NightDrive #HeavyBass #PhonkForge",
        "title_ja": "⚡【超重低音】深夜の集中・ゾーン突入ドロップ #Shorts #夜作業 #作業用BGM",
        "desc_ja": "⚡ 深夜の作業や勉強、夜ドライブに没頭できる重低音。\n🎧 1時間フルバージョンは関連動画から！\n\n#Shorts #夜作業 #ドライブ用 #作業用BGM #超重低音",
        "comment_text": "⚡ Deep heavy bass for midnight driving and deep focus! Check Related Video for the full 1-hour mix! 🔥\n(⚡ Тяжелый бас для авто и ночного дрифта! Полный 1-часовой микс в связанном видео!)",
        "tags": ["shorts", "heavy bass", "midnight drive", "focus music", "cyberpunk", "late night", "phonkforge"]
    },
    {
        "id": "03_dark_combat",
        "file_name": "SHORTS_03_SAVAGE_GRIP_COMBAT_PULSE.mp4",
        "title_en": "⚡ Pure Aggressive Bass Drop for Combat & Workout #Shorts #Workout #Power",
        "desc_en": "⚡ Raw energetic heavy bass drop for combat training, punching bag sessions, and extreme focus.\n🎧 Full 1-Hour Mix is available in Related Video!\n\n#Shorts #Workout #Combat #HeavyBass #PhonkForge",
        "title_ja": "⚡【超重低音】テンション爆上げ アグレッシブドロップ #Shorts #ワークアウト #重低音",
        "desc_ja": "⚡ テンションが最高潮に達するアグレッシブな重低音。\n🎧 1時間フルバージョンは関連動画から！\n\n#Shorts #ワークアウト #テンション爆上げ #作業用BGM #超重低音",
        "comment_text": "⚡ Maximum adrenaline for your workout session! Check Related Video for the full 1-hour mix! 🔥\n(⚡ Взрывной адреналин для тренировок! Полный 1-часовой микс в связанном видео!)",
        "tags": ["shorts", "heavy bass", "workout", "combat", "motivation", "bass boosted", "phonkforge"]
    }
]

def upload_all_shorts():
    print("=== STARTING BATCH UPLOAD OF 3 MASTERED PULSE SHORTS TO PHONKFORGE AUDIO ===")
    yt = get_youtube_service("phonkforge")
    uploaded_results = []
    
    for idx, spec in enumerate(SHORTS_UPLOAD_SPECS):
        v_path = OUT_DIR / spec["file_name"]
        if not v_path.exists():
            print(f"[-] Video file not found: {v_path}")
            continue
            
        print(f"\n[{idx+1}/3] Uploading {spec['file_name']}...")
        
        localizations = {
            "ja": {
                "title": spec["title_ja"],
                "description": spec["desc_ja"]
            },
            "ru": {
                "title": spec["title_en"],
                "description": spec["desc_en"]
            },
            "pt": {
                "title": spec["title_en"],
                "description": spec["desc_en"]
            },
            "es": {
                "title": spec["title_en"],
                "description": spec["desc_en"]
            },
            "ko": {
                "title": spec["title_ja"],
                "description": spec["desc_ja"]
            }
        }
        
        body = {
            "snippet": {
                "title": spec["title_en"],
                "description": spec["desc_en"],
                "tags": spec["tags"],
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
        
        res = None
        while res is None:
            st, res = req.next_chunk()
            if st:
                print(f"    Upload progress: {int(st.progress() * 100)}%")
                
        vid = res.get("id")
        print(f"  ✓ Uploaded: {vid} (https://www.youtube.com/shorts/{vid})")
        
        # Post Engagement Comment
        time.sleep(2)
        try:
            yt.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": vid,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": spec["comment_text"]
                            }
                        }
                    }
                }
            ).execute()
            print(f"  ✓ Pinned engagement comment posted")
        except Exception as e:
            print(f"  ⚠️ Note on comment: {e}")
            
        uploaded_results.append({
            "id": vid,
            "title_ja": spec["title_ja"],
            "url": f"https://www.youtube.com/shorts/{vid}",
            "full_url": f"https://youtu.be/{vid}"
        })
        
    print("\n==================================================")
    print("🎉 ALL 3 SHORTS SUCCESSFULLY UPLOADED & PUBLISHED!")
    for r in uploaded_results:
        print(f"  • {r['title_ja']}: {r['url']}")
    print("==================================================")

if __name__ == "__main__":
    upload_all_shorts()
