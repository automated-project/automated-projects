#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gumroadへの2Dゲームアセット（無料パック & 有料Vault）出品スクリプト
(GameVerse Audio / Assets: Gumroad Automation)

【出品内容】
1. free-game-assets ($0 / Pay what you want)
   - 名前: [FREE ASSETS] 2D Game Asset Starter Pack — Fire Magic & Spell Icons
   - ファイル: Pack01_Fire_Magic_Spells_Complete_Pack.zip
   - カバー: cover_free_game_assets.png

2. game-asset-vault ($9.99 / Pay what you want)
   - 名前: The Ultimate 2D Game Asset Vault: Sprites, UI & Environments
   - ファイル: Game_Asset_Vault_Complete_Pack.zip
   - カバー: cover_game_asset_vault.png
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
load_dotenv(BASE_DIR / ".env")

token = os.getenv("GUMROAD_ACCESS_TOKEN")
if not token:
    print("❌ GUMROAD_ACCESS_TOKEN が .env に設定されていません。", file=sys.stderr)
    sys.exit(1)

CLI_PATH = str(BASE_DIR / "bin" / "gumroad")
env = os.environ.copy()
env["GUMROAD_ACCESS_TOKEN"] = token

ASSETS_DIR = Path("/Users/base/Automated-Projects/Game-Assets/outputs/gumroad_assets")
FREE_ZIP = Path("/Users/base/Automated-Projects/Game-Assets/outputs/Pack01_Fire_Magic_Spells_20260911_160322/Pack01_Fire_Magic_Spells_Complete_Pack.zip")
VAULT_ZIP = ASSETS_DIR / "Game_Asset_Vault_Complete_Pack.zip"
FREE_COVER = ASSETS_DIR / "cover_free_game_assets.png"
VAULT_COVER = ASSETS_DIR / "cover_game_asset_vault.png"

# 1. 既存商品一覧を取得してスラッグ重複を確認
list_res = subprocess.run([CLI_PATH, "products", "list", "--json", "--no-input"], capture_output=True, text=True, env=env)
existing_products = {}
if list_res.returncode == 0:
    try:
        data = json.loads(list_res.stdout)
        for p in data.get("products", []):
            slug = p.get("custom_permalink")
            if slug:
                existing_products[slug] = p
    except Exception as e:
        print(f"注: 既存商品パースエラー: {e}")

# ==========================================
# 1. 無料アセットパック (free-game-assets)
# ==========================================
free_slug = "free-game-assets"
free_name = "[FREE ASSETS] 2D Game Asset Starter Pack — Fire Magic & Spell Icons"
free_summary = "100% free studio-quality transparent 2D spell icons for indie game developers. Drag-and-drop ready for Unity, Godot, Unreal Engine & RPG Maker."
free_desc = """<p>🔥 <strong>[FREE ASSETS] 2D Game Asset Starter Pack — Fire Magic &amp; Spell Icons</strong></p>
<p>Kickstart your indie game project with our high-impact fire magic and spell visual effects pack!</p>
<p>Each icon is handcrafted and isolated on a transparent background, ready to drag-and-drop straight into your game engine.</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Unique Hand-Crafted Fire Magic Icons</strong> (Fireball, Fire Tornado, Meteor Strike, Flaming Greatsword, Flame Shield, Phoenix Wings, Inferno Burst, Pyro Core)</p>
<p>• <strong>100% Clean Alpha Transparency PNGs</strong> (No halos, perfectly isolated)</p>
<p>• <strong>512x512 High-Resolution</strong> + Original Master Art (1024x1024)</p>
<p>• <strong>Game Engine Ready:</strong> Drag-and-drop into Unity, Godot, Unreal Engine, GameMaker, and RPG Maker.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ <strong>100% Commercial Use:</strong> Cleared for commercial games, Steam releases, mobile apps (iOS/Android), and monetized projects.</p>
<p>✅ <strong>Modify &amp; Edit:</strong> Freely crop, resize, recolor, and animate.</p>
<p>✅ <strong>No Credit Required:</strong> Attribution is completely optional.</p>
<p>❌ You may NOT resell, redistribute, or repackage these assets as standalone stock art.</p>
<hr>
<h3>👑 WANT ALL OUR CURRENT &amp; FUTURE ASSETS?</h3>
<p>Upgrade to <strong>The Ultimate 2D Game Asset Vault ($9.99)</strong> and get lifetime access to all our growing collections of sprites, UI, and icons!</p>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault">Unlock The Complete 2D Game Asset Vault here!</a></p>
"""

print(f"\n🚀 [1/2] 無料アセット商品処理中: {free_slug}")
if free_slug in existing_products:
    prod_id = existing_products[free_slug]["id"]
    print(f"⏩ 既存商品が見つかりました (ID: {prod_id})。更新を実行します...")
    up_cmd = [
        CLI_PATH, "products", "update", prod_id,
        "--name", free_name,
        "--currency", "usd",
        "--price", "0",
        "--suggested-price", "2.00",
        "--pay-what-you-want",
        "--description", free_desc,
        "--custom-summary", free_summary,
        "--cover-image", str(FREE_COVER),
        "--thumbnail", str(FREE_COVER),
        "--file", str(FREE_ZIP),
        "--file-name", "Pack01_Fire_Magic_Spells_Complete_Pack.zip",
        "--yes"
    ]
    subprocess.run(up_cmd, env=env)
    subprocess.run([CLI_PATH, "products", "publish", prod_id, "--yes"], env=env)
    print(f"✅ 無料アセット更新＆公開完了: https://gameverseaudio.gumroad.com/l/{free_slug}")
else:
    create_cmd = [
        CLI_PATH, "products", "create",
        "--name", free_name,
        "--price", "0",
        "--currency", "usd",
        "--pay-what-you-want",
        "--suggested-price", "2.00",
        "--custom-permalink", free_slug,
        "--custom-summary", free_summary,
        "--description", free_desc,
        "--cover-image", str(FREE_COVER),
        "--thumbnail", str(FREE_COVER),
        "--file", str(FREE_ZIP),
        "--file-name", "Pack01_Fire_Magic_Spells_Complete_Pack.zip",
        "--tag", "gamedev", "--tag", "game-assets", "--tag", "pixel-art", "--tag", "sprites", "--tag", "rpg",
        "--yes"
    ]
    res = subprocess.run(create_cmd, capture_output=True, text=True, env=env)
    print("Create Output:", res.stdout)
    if res.stderr:
        print("Create Stderr:", res.stderr)
    
    # 作成された商品を公開
    list_res2 = subprocess.run([CLI_PATH, "products", "list", "--json", "--no-input"], capture_output=True, text=True, env=env)
    if list_res2.returncode == 0:
        d2 = json.loads(list_res2.stdout)
        for p in d2.get("products", []):
            if p.get("custom_permalink") == free_slug:
                pid = p.get("id")
                subprocess.run([CLI_PATH, "products", "publish", pid, "--yes"], env=env)
                print(f"✅ 無料アセット新規作成＆公開完了 (ID: {pid}): https://gameverseaudio.gumroad.com/l/{free_slug}")
                break

# ==========================================
# 2. 有料全部盛りVault (game-asset-vault)
# ==========================================
vault_slug = "game-asset-vault"
vault_name = "The Ultimate 2D Game Asset Vault: Sprites, UI & Environments"
vault_summary = "Studio-quality 2D sprites, icons, UI, and environments for indie game developers. Lifetime access to all current and future packs. Commercial use allowed."
vault_desc = """<p>👑 <strong>The Ultimate 2D Game Asset Vault: Sprites, UI &amp; Environments</strong></p>
<p>Get instant access to our entire premium library of transparent 2D game assets, designed specifically for indie game developers, solo creators, and game studios.</p>
<p><strong>Pay once ($9.99) and receive lifetime access</strong> to all current asset collections, plus every future pack we publish to this vault at no extra charge!</p>
<hr>
<h3>✨ What's Inside The Vault:</h3>
<p>• <strong>Complete Thematic Sprite &amp; Icon Packs:</strong> Spells, weapons, items, armor, UI buttons, loot, skill trees, and environmental props.</p>
<p>• <strong>100% Transparent Alpha PNGs:</strong> Master sheets + individually cropped icons (512x512 and 1024x1024 ultra-sharp resolution).</p>
<p>• <strong>Engine Ready:</strong> Fully optimized for drag-and-drop into Unity, Godot, Unreal Engine, GameMaker, RPG Maker, and web engines.</p>
<p>• <strong>Continuous Free Updates:</strong> New asset packs are automatically added to this vault as they are released.</p>
<hr>
<h3>📜 Perpetual Commercial License:</h3>
<p>✅ <strong>Unlimited Commercial Projects:</strong> Use in unlimited commercial games (Steam, itch.io, Epic Games, App Store, Google Play, consoles).</p>
<p>✅ <strong>Full Modification Rights:</strong> Freely crop, recolor, upscale, downscale, or modify any asset.</p>
<p>✅ <strong>NO ATTRIBUTION REQUIRED:</strong> Attribution is appreciated but never mandatory.</p>
<p>❌ Standalone resale, redistribution, or sharing of raw asset files is strictly prohibited.</p>
<hr>
<p>Ready to bring your game world to life? Download the Vault today and build without limits!</p>
"""

print(f"\n🚀 [2/2] 有料Vault商品処理中: {vault_slug}")
if vault_slug in existing_products:
    prod_id = existing_products[vault_slug]["id"]
    print(f"⏩ 既存商品が見つかりました (ID: {prod_id})。更新を実行します...")
    up_cmd = [
        CLI_PATH, "products", "update", prod_id,
        "--name", vault_name,
        "--currency", "usd",
        "--price", "9.99",
        "--suggested-price", "9.99",
        "--pay-what-you-want",
        "--description", vault_desc,
        "--custom-summary", vault_summary,
        "--cover-image", str(VAULT_COVER),
        "--thumbnail", str(VAULT_COVER),
        "--file", str(VAULT_ZIP),
        "--file-name", "Game_Asset_Vault_Complete_Pack.zip",
        "--yes"
    ]
    subprocess.run(up_cmd, env=env)
    subprocess.run([CLI_PATH, "products", "publish", prod_id, "--yes"], env=env)
    print(f"✅ 有料Vault更新＆公開完了: https://gameverseaudio.gumroad.com/l/{vault_slug}")
else:
    create_cmd = [
        CLI_PATH, "products", "create",
        "--name", vault_name,
        "--price", "9.99",
        "--currency", "usd",
        "--pay-what-you-want",
        "--suggested-price", "9.99",
        "--custom-permalink", vault_slug,
        "--custom-summary", vault_summary,
        "--description", vault_desc,
        "--cover-image", str(VAULT_COVER),
        "--thumbnail", str(VAULT_COVER),
        "--file", str(VAULT_ZIP),
        "--file-name", "Game_Asset_Vault_Complete_Pack.zip",
        "--tag", "gamedev", "--tag", "game-assets", "--tag", "sprites", "--tag", "rpg", "--tag", "unity",
        "--yes"
    ]
    res = subprocess.run(create_cmd, capture_output=True, text=True, env=env)
    print("Create Output:", res.stdout)
    if res.stderr:
        print("Create Stderr:", res.stderr)
    
    list_res2 = subprocess.run([CLI_PATH, "products", "list", "--json", "--no-input"], capture_output=True, text=True, env=env)
    if list_res2.returncode == 0:
        d2 = json.loads(list_res2.stdout)
        for p in d2.get("products", []):
            if p.get("custom_permalink") == vault_slug:
                pid = p.get("id")
                subprocess.run([CLI_PATH, "products", "publish", pid, "--yes"], env=env)
                print(f"✅ 有料Vault新規作成＆公開完了 (ID: {pid}): https://gameverseaudio.gumroad.com/l/{vault_slug}")
                break

print("\n🎉 Gumroadへのゲームアセット出品・更新処理が完了しました！")
