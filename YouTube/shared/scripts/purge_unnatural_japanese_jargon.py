# -*- coding: utf-8 -*-
"""
全チャンネル・全動画 日本語タイトル＆説明文から「Phonk」等の専門用語を完全排除し、
日本人が日常で自然に使う言葉（重低音、ドライブBGM、作業用BGM、筋トレBGM等）へ全面修正するスクリプト
"""

import sys
from pathlib import Path

sys.path.append("/Users/base/Automated-Projects/YouTube")
from shared.scripts.account_token_manager import get_youtube_service

def fix_all_japanese_titles():
    print("=== STARTING JAPANESE VOCABULARY PURGE & NATURALIZATION ===")
    
    # 1. Ch 2: PhonkForge Audio
    yt2 = get_youtube_service("phonkforge")
    print("\n▶ Fixing Ch 2 (PhonkForge Audio)...")
    
    # 本編 1時間 (4aJlGEfEI84)
    v2_long = "4aJlGEfEI84"
    res = yt2.videos().list(part="snippet,localizations", id=v2_long).execute()
    if res["items"]:
        locs = res["items"][0]["localizations"]
        locs["ja"] = {
            "title": "🔥【作業用BGM】テンション爆上げ 超重低音・夜ドライブ＆筋トレ用BGM（1時間）",
            "description": "🔥 重低音イヤホンやカーステレオ推奨。1時間ノンストップでテンションが上がる超重低音サウンド。\n夜のドライブ、筋トレ、集中して作業したい時のモチベーションアップに。"
        }
        yt2.videos().update(part="localizations", body={"id": v2_long, "localizations": locs}).execute()
        print(f"  ✓ Updated 1-hour mix {v2_long}")
        
    # Shorts
    shorts_ch2 = {
        "W7yzwdh1vdQ": {
            "title": "⚡【超重低音】テンションが上がる夜ドライブ＆筋トレ用サビまとめ #Shorts #ドライブ #筋トレ",
            "desc": "⚡ 身体の芯に響く超重低音。1時間フルバージョンは関連動画から。"
        },
        "uBwoMrx4EPU": {
            "title": "⚡【夜ドライブ用】テンション爆上げ超重低音（16秒無限ループ）#Shorts #ドライブ #筋トレ",
            "desc": "⚡ 16秒シームレスループ。1時間フルバージョンは関連動画から。"
        }
    }
    for s_id, s_data in shorts_ch2.items():
        res = yt2.videos().list(part="snippet,localizations", id=s_id).execute()
        if res["items"]:
            locs = res["items"][0]["localizations"]
            locs["ja"] = {"title": s_data["title"], "description": s_data["desc"]}
            yt2.videos().update(part="localizations", body={"id": s_id, "localizations": locs}).execute()
            print(f"  ✓ Updated Shorts {s_id}")

    # 2. Ch 1: Komorebi Chill Audio
    yt1 = get_youtube_service("gameverse")
    print("\n▶ Fixing Ch 1 (Komorebi Chill Audio)...")
    
    # 本編 Lofi (H9xAE2j0JZM)
    v1_lofi = "H9xAE2j0JZM"
    res = yt1.videos().list(part="snippet,localizations", id=v1_lofi).execute()
    if res["items"]:
        locs = res["items"][0]["localizations"]
        locs["ja"] = {
            "title": "🍃【作業用BGM】勉強・読書・睡眠用 心が落ち着く癒やしのピアノBGM（1時間）",
            "description": "🍃 1時間ノンストップ。勉強や仕事、読書、睡眠導入に最適な落ち着いたピアノとアコースティックギターの音楽です。"
        }
        yt1.videos().update(part="localizations", body={"id": v1_lofi, "localizations": locs}).execute()
        print(f"  ✓ Updated Lofi {v1_lofi}")
        
    # 誘導用動画
    ch1_promos = {
        "lnJBDZszKCE": "🔥【作業用BGM】集中力を高める超重低音BGM（50分）",
        "bFLKzlSiq4o": "🔥【短時間集中】テンションを上げる超重低音BGM（20分）"
    }
    for p_id, p_title in ch1_promos.items():
        res = yt1.videos().list(part="snippet,localizations", id=p_id).execute()
        if res["items"]:
            locs = res["items"][0]["localizations"]
            locs["ja"] = {
                "title": p_title,
                "description": "🚨 重低音・アップテンポ楽曲は専門チャンネルへ移転しました。\n🔥 超重低音チャンネル ➡️ https://www.youtube.com/@phonkforgeaudio-s1h\n✨ 爽快アップテンポ チャンネル ➡️ https://www.youtube.com/@auramelody-audio"
            }
            yt1.videos().update(part="localizations", body={"id": p_id, "localizations": locs}).execute()
            print(f"  ✓ Updated promo {p_id}")

    # 3. Ch 3: AuraMelody Audio
    yt3 = get_youtube_service("auramelody")
    print("\n▶ Fixing Ch 3 (AuraMelody Audio)...")
    
    vids_ch3 = {
        "o8ygRO9KVuQ": {
            "title": "✨【作業用BGM】気分が上がる爽快な曲・やる気と集中力を高めるアップテンポBGM（1時間）",
            "desc": "✨ 1時間ノンストップ。開放感あふれる明るいアップテンポな音楽。\n仕事や勉強、ドライブ、運動中のモチベーションアップに。"
        },
        "Tamf2pVElJU": {
            "title": "🌌【作業用BGM】深く集中したい時に聴く 疾走感のある夜の作業用BGM（1時間）",
            "desc": "🌌 1時間ノンストップ。夜の作業や勉強、パソコン作業に没頭できる心地よいスピード感の音楽。\n集中力を研ぎ澄ませたい時に。"
        }
    }
    for v_id, v_data in vids_ch3.items():
        res = yt3.videos().list(part="snippet,localizations", id=v_id).execute()
        if res["items"]:
            locs = res["items"][0]["localizations"]
            locs["ja"] = {
                "title": v_data["title"],
                "description": v_data["desc"]
            }
            yt3.videos().update(part="localizations", body={"id": v_id, "localizations": locs}).execute()
            print(f"  ✓ Updated Ch 3 {v_id}")

    # Shorts
    res = yt3.videos().list(part="snippet,localizations", id="4sDPJh25GGw").execute()
    if res["items"]:
        locs = res["items"][0]["localizations"]
        locs["ja"] = {
            "title": "✨【作業用BGM】やる気が出る爽快な曲（15秒ループ）#Shorts #作業用BGM #勉強用BGM",
            "description": "✨ 15秒シームレス無限ループ。1時間フルバージョンは関連動画から。"
        }
        yt3.videos().update(part="localizations", body={"id": "4sDPJh25GGw", "localizations": locs}).execute()
        print("  ✓ Updated Ch 3 Shorts 4sDPJh25GGw")

    print("\n==================================================")
    print("✅ ALL JAPANESE TITLES & DESCRIPTIONS COMPLETELY REFINED TO PURE NATURAL JAPANESE!")
    print("==================================================")

if __name__ == "__main__":
    fix_all_japanese_titles()
