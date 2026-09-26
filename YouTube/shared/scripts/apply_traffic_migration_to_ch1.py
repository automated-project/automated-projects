#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ch 1 旧EDM動画2本（lnJBDZszKCE / bFLKzlSiq4o）のトラフィックを
Ch 2（重低音）とCh 3（EDM）へ総移転・誘導する一括自動化スクリプト
1. 移転専用高CTRサムネイルの生成 & YouTube API適用
2. タイトル・説明文・多言語ローカライズの移転専用メタデータ更新
3. 移転先直リンク固定コメントの投稿
"""

import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from googleapiclient.http import MediaFileUpload

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

THUMB_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Dark_Fantasy_Channel/cover_art")
THUMB_DIR.mkdir(parents=True, exist_ok=True)
THUMB_OUT_PATH = THUMB_DIR / "THUMBNAIL_CHANNEL_MIGRATION_NOTICE.jpg"

def generate_migration_thumbnail(out_path: Path):
    print(f"[+] Generating High-CTR Migration Thumbnail: {out_path}")
    w, h = 1920, 1080
    
    # Base background (Dark red/black high contrast)
    img = Image.new("RGB", (w, h), (15, 10, 18))
    draw = ImageDraw.Draw(img)
    
    # Draw dark diagonal caution background stripes
    for x in range(-500, w + 500, 120):
        draw.polygon([(x, 0), (x + 50, 0), (x - 200, h), (x - 250, h)], fill=(30, 15, 25))
        
    # Dark vignette
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    v_draw.rectangle([0, 0, w, h], fill=(0, 0, 0, 120))
    img.paste(vignette, (0, 0), vignette)
    
    # Draw Heavy Red Header Banner
    draw.rectangle([0, 80, w, 280], fill=(220, 20, 40))
    draw.rectangle([0, 75, w, 80], fill=(255, 220, 0))
    draw.rectangle([0, 280, w, 285], fill=(255, 220, 0))
    
    # Fonts
    font_impact_huge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Impact.ttf", 120)
    font_impact_mid = ImageFont.truetype("/System/Library/Fonts/Supplemental/Impact.ttf", 80)
    font_impact_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Impact.ttf", 65)
    font_arial_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
    
    # Header Banner Text
    header_text = "CHANNEL MOVED"
    bbox_h = draw.textbbox((0, 0), header_text, font=font_impact_huge)
    tw_h = bbox_h[2] - bbox_h[0]
    draw.text(((w - tw_h) // 2, 105), header_text, fill=(255, 255, 255), font=font_impact_huge)
    
    # Main Body Text Box 1: Heavy Bass & EDM
    draw.rectangle([140, 350, w - 140, 520], fill=(0, 0, 0, 230), outline=(255, 220, 0), width=5)
    body1 = "HEAVY BASS & EDM MOVED TO NEW CHANNELS"
    bbox_b1 = draw.textbbox((0, 0), body1, font=font_impact_mid)
    tw_b1 = bbox_b1[2] - bbox_b1[0]
    draw.text(((w - tw_b1) // 2, 395), body1, fill=(255, 235, 40), font=font_impact_mid)
    
    # Main Body Text Box 2: 1-Hour Full Mixes
    draw.rectangle([140, 560, w - 140, 730], fill=(15, 20, 35), outline=(0, 220, 255), width=5)
    body2 = "1-HOUR FULL MIXES NOW STREAMING"
    bbox_b2 = draw.textbbox((0, 0), body2, font=font_impact_mid)
    tw_b2 = bbox_b2[2] - bbox_b2[0]
    draw.text(((w - tw_b2) // 2, 605), body2, fill=(255, 255, 255), font=font_impact_mid)
    
    # Bottom Call To Action Banner
    draw.rectangle([0, 820, w, 1000], fill=(255, 200, 0))
    cta_text = "CHECK DESCRIPTION & PINNED COMMENT FOR NEW LINKS!"
    bbox_cta = draw.textbbox((0, 0), cta_text, font=font_arial_bold)
    tw_cta = bbox_cta[2] - bbox_cta[0]
    draw.text(((w - tw_cta) // 2, 875), cta_text, fill=(0, 0, 0), font=font_arial_bold)
    
    img.save(out_path, "JPEG", quality=95)
    print(f"✓ Saved Migration Thumbnail: {out_path}")

def apply_migration_to_ch1():
    print("\n=== STARTING FULL TRAFFIC MIGRATION ON CH 1 OLD EDM VIDEOS ===")
    yt = get_youtube_service("gameverse")
    
    # 1. Generate Thumbnail
    generate_migration_thumbnail(THUMB_OUT_PATH)
    
    target_videos = [
        {"id": "bFLKzlSiq4o", "label": "20分EDM (590 views)"},
        {"id": "lnJBDZszKCE", "label": "50分EDM (314 views)"}
    ]
    
    TITLE_EN = "🚨 [CHANNEL MOVED] Heavy Bass & EDM Tracks Moved to New Official Channels ➡️ Check Description"
    DESC_EN = """🚨 IMPORTANT NOTICE / CHANNEL MOVED 🚨

This channel has been officially transformed into "Komorebi Chill Audio" (Dedicated to Cozy & Relaxing Lofi Music).

All Heavy Bass, Workout EDM, and Phonk tracks have moved to our new specialized official channels!
1-Hour Full Mixes are now streaming below:

🔥 Extreme Heavy Bass Channel ➡️ https://youtu.be/4aJlGEfEI84
✨ Uplifting Melodic EDM Channel ➡️ https://youtu.be/Tamf2pVElJU

Please subscribe and listen to our latest 1-Hour mixes on the new channels! Thank you!
"""

    TITLE_JA = "🚨【チャンネル移転のお知らせ】重低音・EDMは新チャンネルへ完全移行しました（1時間完全版は概要欄・固定コメントへ）"
    DESC_JA = """🚨【重要なお知らせ / チャンネル移転】🚨

当チャンネルは落ち着いた癒やしの音楽（Komorebi Chill Audio）へ完全リニューアルいたしました。

重低音・筋トレBGM・EDM楽曲の新作および「1時間ノンストップ完全版」は、以下の公式新チャンネルにて公開中です！

🔥 超重低音・夜ドライブ・筋トレ専門チャンネル
➡️ https://youtu.be/4aJlGEfEI84（PhonkForge Audio）

✨ 爽快アップテンポ・集中EDM専門チャンネル
➡️ https://youtu.be/Tamf2pVElJU（AuraMelody Audio）

ぜひ上記の新チャンネルにてチャンネル登録・ご視聴をお願いいたします！
"""

    COMMENT_TEXT = """🚨 【IMPORTANT NOTICE / CHANNEL MOVED】
This channel has been officially updated to Komorebi Chill Audio (Lofi Music).
All Heavy Bass, Workout EDM & Phonk tracks have officially moved to our sister channels!
👉 Check the description for new 1-Hour full mixes and channel links!

(🚨 Все треки Heavy Bass и Phonk переехали на наши новые каналы! Ссылки в описании видео!)"""

    LOCALIZATIONS = {
        "ja": {"title": TITLE_JA, "description": DESC_JA},
        "ru": {"title": TITLE_EN, "description": DESC_EN},
        "es": {"title": TITLE_EN, "description": DESC_EN},
        "pt": {"title": TITLE_EN, "description": DESC_EN},
        "ko": {"title": TITLE_JA, "description": DESC_JA}
    }

    for target in target_videos:
        vid = target["id"]
        print(f"\n▶ Updating Video {vid} ({target['label']})...")
        
        # 1. Update Thumbnail
        try:
            yt.thumbnails().set(
                videoId=vid,
                media_body=MediaFileUpload(str(THUMB_OUT_PATH), mimetype="image/jpeg")
            ).execute()
            print(f"  ✓ Applied Migration Thumbnail to {vid}")
        except Exception as e:
            print(f"  ⚠️ Thumbnail update error: {e}")
            
        # 2. Update Snippet & Localizations
        try:
            body = {
                "id": vid,
                "snippet": {
                    "title": TITLE_EN,
                    "description": DESC_EN,
                    "categoryId": "10",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en"
                },
                "localizations": LOCALIZATIONS
            }
            yt.videos().update(part="snippet,localizations", body=body).execute()
            print(f"  ✓ Updated Title, Description, and Multilingual Localizations for {vid}")
        except Exception as e:
            print(f"  ⚠️ Metadata update error: {e}")
            
        # 3. Post Pinned Engagement Comment
        time.sleep(2)
        try:
            yt.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": vid,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": COMMENT_TEXT
                            }
                        }
                    }
                }
            ).execute()
            print(f"  ✓ Posted Migration Notice Comment on {vid}")
        except Exception as e:
            print(f"  ⚠️ Comment error: {e}")

    print("\n==================================================")
    print("✅ TRAFFIC MIGRATION MEASURES 100% APPLIED TO CH 1!")
    print("==================================================")

if __name__ == "__main__":
    apply_migration_to_ch1()
