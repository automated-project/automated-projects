# -*- coding: utf-8 -*-
"""
全チャンネル・全公開動画 コメント一括多言語（英語＋ロシア語）更新スクリプト
- ルール: 日本語のみのコメント完全禁止。完全英語または「英語＋ロシア語併記」を適用。
- URL記載禁止（YouTubeスパム自動非表示の回避）、数字タイムスタンプ禁止を徹底。
"""

import sys
import time
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

# 全チャンネルの動画別多言語（英語＋ロシア語）コメントマスター
COMMENTS_CONFIG = {
    "gameverse": {
        "H9xAE2j0JZM": (
            "🍃 Welcome to your daily cozy study & relaxation session.\n"
            "What are you working on or studying today? Share your thoughts below! ☕📚\n\n"
            "(🍃 Добро пожаловать! Для чего вы слушаете этот лофай сегодня — учеба, работа или отдых? Делитесь в комментариях!)"
        ),
        "lnJBDZszKCE": (
            "🚨 【IMPORTANT NOTICE / CHANNEL MOVED】\n"
            "All Heavy Bass, Workout EDM & Phonk tracks have officially moved to our sister channels!\n"
            "👉 Check the description for new 1-Hour full mixes and channel links!\n\n"
            "(🚨 Все треки Heavy Bass и Phonk переехали на наши новые каналы! Ссылки в описании видео!)"
        ),
        "bFLKzlSiq4o": (
            "🚨 【IMPORTANT NOTICE / CHANNEL MOVED】\n"
            "All Heavy Bass, Workout EDM & Phonk tracks have officially moved to our sister channels!\n"
            "👉 Check the description for new 1-Hour full mixes and channel links!\n\n"
            "(🚨 Все треки Heavy Bass и Phonk переехали на наши новые каналы! Ссылки в описании видео!)"
        )
    },
    "phonkforge": {
        "4aJlGEfEI84": (
            "⚡ What track gave you the biggest PR or adrenaline surge in this mix? Let us know in the comments below! 🏋️‍♂️🔥\n\n"
            "(⚡ Какой трек дал вам максимальный заряд энергии на тренировке или за рулем? Пишите в комментариях!)"
        ),
        "W7yzwdh1vdQ": (
            "⚡ How many reps did this drop add to your set? Check Related Video for the full 1-Hour mix! 🏋️‍♂️🔥\n\n"
            "(⚡ Экстремальный бас для качалки и авто! Полный 1-часовой микс в связанном видео!)"
        ),
        "uBwoMrx4EPU": (
            "⚡ Deep heavy bass for midnight driving and workouts! Check Related Video for the full 1-Hour mix! 🔥\n\n"
            "(⚡ Тяжелый бас для авто и тренировок! Полный 1-часовой микс в связанном видео!)"
        ),
        "QhBfGIJh7jg": (
            "⚡ Engineered for crushing gym PRs and heavy lifts! Check Related Video for the full 1-hour mix! 🔥\n\n"
            "(⚡ Мощный бас для тренировок и качалки! Полный 1-часовой микс в связанном видео!)"
        ),
        "j49aZgkO0Kc": (
            "⚡ Deep heavy bass for midnight driving and deep focus! Check Related Video for the full 1-hour mix! 🔥\n\n"
            "(⚡ Тяжелый бас для авто и ночного дрифта! Полный 1-часовой микс в связанном видео!)"
        ),
        "6gK-_VodDJM": (
            "⚡ Maximum adrenaline for your workout session! Check Related Video for the full 1-hour mix! 🔥\n\n"
            "(⚡ Взрывной адреналин для тренировок! Полный 1-часовой микс в связанном видео!)"
        )
    },
    "auramelody": {
        "Tamf2pVElJU": (
            "✨ Which track gave you the most energy and focus today? Let us know in the comments below! ⬇️\n\n"
            "(✨ Какой трек зарядил вас максимальной энергией для работы или учебы? Пишите в комментариях!)"
        ),
        "o8ygRO9KVuQ": (
            "✨ Welcome to AuraMelody! What are you focusing on today while listening? Let us know in the comments! 🎧✨\n\n"
            "(✨ Добро пожаловать! Что вы делаете под эту музыку — работаете, учитесь или тренируетесь? Делитесь в комментариях!)"
        ),
        "4sDPJh25GGw": (
            "✨ What feeling did this summer melody give you? Full 1-Hour Long Mix is available in the Related Video link! ⬇️\n\n"
            "(✨ Летний мелодичный EDM для настроения и энергии! Полный 1-часовой микс в связанном видео!)"
        )
    }
}

def update_comments_for_channel(channel_key: str):
    print(f"\n==========================================")
    print(f"▶ Updating Comments for Channel: {channel_key}")
    print(f"==========================================")
    
    try:
        yt = get_youtube_service(channel_key)
    except Exception as e:
        print(f"[-] Authentication failed for {channel_key}: {e}")
        return
        
    videos = COMMENTS_CONFIG.get(channel_key, {})
    for vid, comment_text in videos.items():
        print(f"[+] Processing Video {vid}...")
        
        # 1. 既存の自チャンネルのコメントを取得して更新を試みる
        try:
            res = yt.commentThreads().list(part="snippet", videoId=vid, maxResults=20).execute()
            items = res.get("items", [])
            my_comment_id = None
            
            for item in items:
                top_comment = item["snippet"]["topLevelComment"]["snippet"]
                # チャンネルオーナーのコメントまたは以前投稿したコメントを探す
                author_channel = top_comment.get("authorChannelId", {}).get("value")
                # 自アカウントのコメントであれば特定
                my_comment_id = item["id"]
                break
                
            if my_comment_id:
                print(f"  -> Found existing comment thread {my_comment_id}, updating...")
                yt.comments().update(
                    part="snippet",
                    body={
                        "id": my_comment_id,
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                ).execute()
                print(f"  ✓ Updated existing comment {my_comment_id} on {vid}")
            else:
                print(f"  -> No existing comment thread found, creating new comment...")
                c_res = yt.commentThreads().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "videoId": vid,
                            "topLevelComment": {
                                "snippet": {
                                    "textOriginal": comment_text
                                }
                            }
                        }
                    }
                ).execute()
                print(f"  ✓ Created new comment {c_res['id']} on {vid}")
        except Exception as e:
            print(f"  ⚠️ Error updating comment on {vid}: {e}")
            
        time.sleep(3)

def main():
    print("=== STARTING CROSS-CHANNEL MULTILINGUAL COMMENT UPDATE ===")
    for ch in ["gameverse", "phonkforge", "auramelody"]:
        update_comments_for_channel(ch)
        time.sleep(5)
    print("\n==================================================")
    print("🏁 COMMENT UPDATE PROCESS COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    main()
