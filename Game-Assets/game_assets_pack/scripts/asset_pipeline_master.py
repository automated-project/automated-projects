#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
asset_pipeline_master.py: ゲームアセット完全自動化マスターパイプライン
仕様書: /Users/base/Automated-Projects/.agents/rules/03_asset_commerce.md

【絶対厳守仕様】
1. 合体ZIPの作成は完全禁止。各パックは独立ZIPとして生成・保持する。
2. itch.io: Butler CLIで個別チャンネルに独立push。
3. Gumroad: 全商品に必ず --currency usd と --pay-what-you-want を適用。
4. Gumroad Vaultには全パックの個別ZIPを並列で添付（合体させない）。
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("ITCH_API_KEY") or os.getenv("BUTLER_API_KEY")
token = os.getenv("GUMROAD_ACCESS_TOKEN")

if not token or not api_key:
    print("❌ 認証情報（GUMROAD_ACCESS_TOKEN または BUTLER_API_KEY）が不足しています。", file=sys.stderr)
    sys.exit(1)

BUTLER_BIN = str(BASE_DIR / "bin" / "butler")
GUMROAD_CLI = str(BASE_DIR / "bin" / "gumroad")

env_butler = os.environ.copy()
env_butler["BUTLER_API_KEY"] = api_key

env_gumroad = os.environ.copy()
env_gumroad["GUMROAD_ACCESS_TOKEN"] = token

ASSETS_BASE = Path("/Users/base/Automated-Projects/Game-Assets/outputs")

# 定義されている個別パック一覧（合体させず、常にこの個別ZIP群を扱う）
PACKS = [
    {
        "id": "pack01-fire-magic-spells",
        "zip": ASSETS_BASE / "Pack01_Fire_Magic_Spells_20260911_160322" / "Pack01_Fire_Magic_Spells_Complete_Pack.zip",
        "src_dir": ASSETS_BASE / "Pack01_Fire_Magic_Spells_20260911_160322" / "Pack01_Fire_Magic_Spells_Complete_Pack",
        "filename": "Pack01_Fire_Magic_Spells_Complete_Pack.zip"
    },
    {
        "id": "pack02-fantasy-weapons",
        "zip": ASSETS_BASE / "Pack02_Fantasy_Weapons_20260911_190148" / "Pack02_Fantasy_Weapons_Complete_Pack.zip",
        "src_dir": ASSETS_BASE / "Pack02_Fantasy_Weapons_20260911_190148",
        "filename": "Pack02_Fantasy_Weapons_Complete_Pack.zip"
    },
    {
        "id": "pack03-potions-and-ui",
        "zip": ASSETS_BASE / "Game_Asset_Vault_Build" / "Pack03_Potions_and_Cyberpunk_UI.zip",
        "src_dir": ASSETS_BASE / "Game_Asset_Vault_Build" / "Pack03_Potions_and_Cyberpunk_UI",
        "filename": "Pack03_Potions_and_Cyberpunk_UI.zip"
    }
]

FREE_STARTER_DIR = ASSETS_BASE / "Free_Starter_Pack_Selected" / "Free_2D_Game_Asset_Starter_Pack"
FREE_STARTER_ZIP = ASSETS_BASE / "Free_Starter_Pack_Selected" / "Free_2D_Game_Asset_Starter_Pack.zip"

def deploy_itch():
    print("\n🎮 [itch.io] 自動デプロイ実行中...")
    # 1. 無料スターター
    print("  -> Pushing Free Starter Pack...")
    subprocess.run([
        BUTLER_BIN, "push", str(FREE_STARTER_DIR),
        "gameverse-audio/free-game-assets:free-starter-pack"
    ], env=env_butler, check=True)

    # 2. 有料Vault（個別チャンネルへ独立push）
    for p in PACKS:
        if p["src_dir"].exists():
            print(f"  -> Pushing {p['id']} to game-asset-vault...")
            subprocess.run([
                BUTLER_BIN, "push", str(p["src_dir"]),
                f"gameverse-audio/game-asset-vault:{p['id']}"
            ], env=env_butler, check=True)

def deploy_gumroad():
    print("\n🛒 [Gumroad] 自動デプロイ実行中...")
    
    # 1. 無料スターター更新 (ID: ozQ4-e20_gROzj378uBJrA==)
    print("  -> Updating Free Starter Pack...")
    subprocess.run([
        GUMROAD_CLI, "products", "update", "ozQ4-e20_gROzj378uBJrA==",
        "--file", str(FREE_STARTER_ZIP),
        "--file-name", "Free_2D_Game_Asset_Starter_Pack.zip",
        "--currency", "usd",
        "--price", "0",
        "--suggested-price", "2.00",
        "--pay-what-you-want",
        "--yes"
    ], env=env_gumroad, check=True)

    # 2. 有料Vault更新 (ID: c07Os4dAkeUFa2VBAne4YQ==) - 個別ZIPを並列添付
    print("  -> Updating Paid Vault (attaching individual pack ZIPs)...")
    vault_cmd = [
        GUMROAD_CLI, "products", "update", "c07Os4dAkeUFa2VBAne4YQ==",
        "--currency", "usd",
        "--price", "9.99",
        "--suggested-price", "9.99",
        "--pay-what-you-want",
        "--yes"
    ]
    for p in PACKS:
        if p["zip"].exists():
            vault_cmd.extend(["--file", str(p["zip"]), "--file-name", p["filename"]])
            
    subprocess.run(vault_cmd, env=env_gumroad, check=True)

if __name__ == "__main__":
    deploy_itch()
    deploy_gumroad()
    print("\n🎉 パイプラインの自動実行が完全完了しました。")
