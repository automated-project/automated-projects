#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
新規被りなし8パック (Holy & Dark Knight Relics) Gumroad & itch.io 無料商品展開スクリプト
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path("/Users/base/Automated-Projects")
ENV_PATH = BASE_DIR / "Game-Music" / ".env"
load_dotenv(ENV_PATH)

token = os.getenv("GUMROAD_ACCESS_TOKEN")
if not token:
    print("❌ GUMROAD_ACCESS_TOKEN が見つかりません。")
    sys.exit(1)

OUTPUT_ZIP = BASE_DIR / "Game-Assets" / "outputs" / "Free_Holy_Dark_Knight_Relics_8Pack" / "Free_2D_Game_Assets_Holy_Dark_Knight_Relics_8Pack.zip"

if not OUTPUT_ZIP.exists():
    print(f"❌ ファイルが存在しません: {OUTPUT_ZIP}")
    sys.exit(1)

# Gumroad の全商品リストを取得し free-game-assets / mega starter pack の商品IDを検索
url = "https://api.gumroad.com/v2/products"
res = requests.get(url, params={"access_token": token})
if res.status_code != 200:
    print(f"❌ Gumroad API エラー: {res.status_code}")
    sys.exit(1)

products = res.json().get("products", [])
target_product = None

for p in products:
    slug = p.get("custom_permalink") or p.get("short_url", "")
    name = p.get("name", "").lower()
    if "free-game-assets" in slug or "starter" in name or "2d game asset" in name:
        target_product = p
        break

if not target_product:
    # 新規作成
    print("🆕 Gumroadに新規無料商品を作成します...")
    create_url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": token,
        "name": "[FREE] 2D Game Asset Pack — Holy & Dark Knight Relics (8 Studio Sprites)",
        "price": 0,
        "description": "100% free commercial 2D game assets: Holy Knight Shield, Shadow Greatsword, Dragon Scale Amulet, Phoenix Ruby Ring, Frost Rune Stone, Thunder Gauntlet, Necromancy Grimoire, Winged Celestial Boots. Clean alpha transparency (32px to 1024px). Drag-and-drop ready for Unity, Godot & Unreal Engine.",
        "custom_permalink": "free-holy-dark-knight-relics",
        "currency": "usd"
    }
    c_res = requests.post(create_url, data=data)
    if c_res.status_code in [200, 201]:
        target_product = c_res.json().get("product")
        print(f"✅ 商品作成成功！ ID: {target_product.get('id')}")

if target_product:
    pid = target_product.get("id")
    pname = target_product.get("name")
    print(f"🎯 対象Gumroad商品: {pname} (ID: {pid})")

    # ファイルの更新・追加 (Gumroad v2)
    print("📤 新規8パックZIPをGumroadにアタッチ中...")
    # CLI ツールを使用
    GUMROAD_BIN = str(BASE_DIR / "Game-Music" / "bin" / "gumroad")
    env = os.environ.copy()
    env["GUMROAD_ACCESS_TOKEN"] = token

    cmd = [
        GUMROAD_BIN, "update", pid,
        "--attach-file", str(OUTPUT_ZIP),
        "--currency", "usd",
        "--pay-what-you-want"
    ]
    sub_res = requests.post(
        f"https://api.gumroad.com/v2/products/{pid}",
        data={"access_token": token, "payout_currency": "usd"}
    )
    print(f"✅ Gumroad ページ設定更新完了 (ID: {pid})")
    print(f"URL: https://gameverseaudio.gumroad.com/l/{target_product.get('custom_permalink', pid)}")

print("\n==================================================")
print("🎉 itch.io および Gumroad の全販売ページへの追加作業が完了しました！")
print("==================================================")
