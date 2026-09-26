#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
itch.io 全楽曲一括デプロイスクリプト
(Butler CLI を使用して既存の全楽曲パッケージを itch.io に一括アップロード)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

from itch_client import push_build, verify_credentials, ITCH_USERNAME

PRODUCTS = [
    {
        "title": "Wrath of the Abyss",
        "slug": "wrath-of-the-abyss",
        "zip": BASE_DIR / "tracks/2026-09-08/Track01_Wrath_of_the_Abyss/Wrath_of_the_Abyss_Commercial_Audio_Pack.zip"
    },
    {
        "title": "Neon Overdrive",
        "slug": "neon-overdrive",
        "zip": BASE_DIR / "tracks/2026-09-08/Track02_Neon_Overdrive/Neon_Overdrive_Commercial_Audio_Pack.zip"
    },
    {
        "title": "Requiem of the Fallen",
        "slug": "requiem-of-the-fallen",
        "zip": BASE_DIR / "tracks/2026-09-08/Track03_Requiem_of_the_Fallen/Requiem_of_the_Fallen_Commercial_Audio_Pack.zip"
    },
    {
        "title": "Solaris 1984",
        "slug": "solaris-1984",
        "zip": BASE_DIR / "tracks/2026-09-09/Track04_Solaris_1984/gumroad_solaris-1984/Solaris_1984_Commercial_Audio_Pack.zip"
    },
    {
        "title": "God of Ruin",
        "slug": "god-of-ruin",
        "zip": BASE_DIR / "tracks/2026-09-09/Track05_God_of_Ruin/gumroad_god-of-ruin/God_of_Ruin_Commercial_Audio_Pack.zip"
    },
    {
        "title": "Cyber Nemesis",
        "slug": "cyber-nemesis",
        "zip": BASE_DIR / "tracks/2026-09-09/Track06_Cyber_Nemesis/gumroad_cyber-nemesis/Cyber_Nemesis_Commercial_Audio_Pack.zip"
    }
]

def main():
    print("=======================================================")
    print("🎮 GameVerse Audio ➔ itch.io 一括デプロイシステム")
    print(f"対象アカウント: {ITCH_USERNAME}")
    print("=======================================================")

    user = verify_credentials()
    if not user:
        print("❌ itch.io 認証に失敗しました。.env の ITCH_API_KEY を確認してください。")
        sys.exit(1)

    print(f"✅ 認証確認: {user.get('username')}\n")

    success_count = 0
    fail_count = 0

    for p in PRODUCTS:
        print(f"-------------------------------------------------------")
        print(f"🎵 処理中: {p['title']} (スラッグ: {p['slug']})")
        if not p["zip"].exists():
            print(f"⚠️ ZIPファイルが見つかりません: {p['zip']}")
            fail_count += 1
            continue

        ok = push_build(p["zip"], channel=p["slug"], project_slug="game-music-vault")
        if ok:
            success_count += 1
        else:
            fail_count += 1

    print("\n=======================================================")
    print(f"🏁 一括デプロイ処理終了")
    print(f"成功: {success_count} 件 / 失敗: {fail_count} 件")
    print("=======================================================")

if __name__ == "__main__":
    main()
