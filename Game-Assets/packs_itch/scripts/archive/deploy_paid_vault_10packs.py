#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deploy_paid_vault_10packs.py
有料版全部盛りVault (game-asset-vault / $1.99) デプロイスクリプト

【最上位厳守事項】
1. 合体マスターZIPは絶対に作成・出品しない。
2. 01〜10の個別パック（各8枚・計80枚）を独立した個別ZIPとして配信・添付する。
3. 無料版（ポーション、宝箱・金貨、バフ、火炎魔法）との重複は完全ゼロ。
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
env_file = BASE_DIR / ".env"

env = os.environ.copy()
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v.strip("\"'\\")

token = env.get("GUMROAD_ACCESS_TOKEN")
api_key = env.get("ITCH_API_KEY") or env.get("BUTLER_API_KEY")

if not token or not api_key:
    print("❌ 認証情報（GUMROAD_ACCESS_TOKEN / BUTLER_API_KEY）が不足しています。", file=sys.stderr)
    sys.exit(1)

BUTLER_BIN = str(BASE_DIR / "bin" / "butler")
GUMROAD_CLI = str(BASE_DIR / "bin" / "gumroad")

VAULT_DIR = Path("/Users/base/Automated-Projects/Game-Assets/outputs/Paid_Vault_10Packs")

PACKS = [
    {
        "channel": "01-fantasy-weapons",
        "zip_name": "01_Fantasy_Weapons_Pack.zip",
        "folder": VAULT_DIR / "01_Fantasy_Weapons",
        "title": "01 // Fantasy Weapons Pack (8 Sprites)"
    },
    {
        "channel": "02-mythic-armor-helmets",
        "zip_name": "02_Mythic_Armor_Helmets_Pack.zip",
        "folder": VAULT_DIR / "02_Mythic_Armor_Helmets",
        "title": "02 // Mythic Armor & Helmets Pack (8 Sprites)"
    },
    {
        "channel": "03-cyberpunk-scifi-hud-ui",
        "zip_name": "03_Cyberpunk_SciFi_HUD_UI_Pack.zip",
        "folder": VAULT_DIR / "03_Cyberpunk_SciFi_HUD_UI",
        "title": "03 // Cyberpunk & Sci-Fi HUD UI Pack (8 Sprites)"
    },
    {
        "channel": "04-gemstones-crystals",
        "zip_name": "04_Gemstones_Crystals_Pack.zip",
        "folder": VAULT_DIR / "04_Gemstones_Crystals",
        "title": "04 // Gemstones & Crystals Pack (8 Sprites)"
    },
    {
        "channel": "05-spellbooks-tomes",
        "zip_name": "05_Spellbooks_Tomes_Pack.zip",
        "folder": VAULT_DIR / "05_Spellbooks_Tomes",
        "title": "05 // Spellbooks & Ancient Tomes Pack (8 Sprites)"
    },
    {
        "channel": "06-monster-creature-avatars",
        "zip_name": "06_Monster_Creature_Avatars_Pack.zip",
        "folder": VAULT_DIR / "06_Monster_Creature_Avatars",
        "title": "06 // Monster & Creature Avatars Pack (8 Sprites)"
    },
    {
        "channel": "07-survival-food-cooking",
        "zip_name": "07_Survival_Food_Cooking_Pack.zip",
        "folder": VAULT_DIR / "07_Survival_Food_Cooking",
        "title": "07 // Survival Food & Provisions Pack (8 Sprites)"
    },
    {
        "channel": "08-crafting-materials-ores",
        "zip_name": "08_Crafting_Materials_Ores_Pack.zip",
        "folder": VAULT_DIR / "08_Crafting_Materials_Ores",
        "title": "08 // Crafting Materials & Ores Pack (8 Sprites)"
    },
    {
        "channel": "09-rings-amulets-jewelry",
        "zip_name": "09_Rings_Amulets_Jewelry_Pack.zip",
        "folder": VAULT_DIR / "09_Rings_Amulets_Jewelry",
        "title": "09 // Rings, Amulets & Talismans Pack (8 Sprites)"
    },
    {
        "channel": "10-dark-magic-necromancy",
        "zip_name": "10_Dark_Magic_Necromancy_Pack.zip",
        "folder": VAULT_DIR / "10_Dark_Magic_Necromancy",
        "title": "10 // Dark Magic & Cursed Relics Pack (8 Sprites)"
    },
]

# 全ZIPの存在確認
print("🔍 ZIPファイル存在確認中...")
for p in PACKS:
    zip_file = p["folder"] / p["zip_name"]
    if not zip_file.exists():
        print(f"❌ ファイルが存在しません: {zip_file}")
        sys.exit(1)
    print(f"  ✅ {p['zip_name']} ({zip_file.stat().st_size / (1024*1024):.2f} MB)")

print("\n--- 1. itch.io へのデプロイ開始 (Butler CLI) ---")
for p in PACKS:
    target = f"gameverse-audio/game-asset-vault:{p['channel']}"
    print(f"\n🚀 Pushing to itch.io: {target}...")
    res = subprocess.run([
        BUTLER_BIN, "push", str(p["folder"] / p["zip_name"]), target
    ], env=env, text=True)
    if res.returncode != 0:
        print(f"❌ Butler push 失敗: {target}")
    else:
        print(f"✅ Butler push 成功: {target}")

print("\n--- 2. Gumroad へのデプロイ開始 ---")
vault_id = "c07Os4dAkeUFa2VBAne4YQ=="

# 説明文の構築
vault_desc = """<p>👑 <strong>The Ultimate 2D Game Asset Vault — 10 Epic Genre Packs (80 Handcrafted Studio Sprites)</strong></p>
<p>Get instant lifetime access to the complete 10-genre studio collection of high-resolution transparent 2D sprites, icons, and UI elements. Ready to drag and drop straight into Unity, Godot, Unreal Engine, GameMaker, and RPG Maker.</p>
<p>💡 <em>Organized as 10 clean, modular genre packs — no cluttered mega-archives! Pick and extract exactly what you need.</em></p>
<hr>
<h3>📦 What's Inside the 10 Individual Packs (80 Sprites):</h3>
<ol>
  <li><strong>01 // Fantasy Weapons Pack (8 Sprites)</strong>: Excalibur Greatsword, Molten Hammer, Thunder Battleaxe, Elven Longbow, Dragon Dagger, Shadow Scythe, Crystal Staff, Runed Halberd.</li>
  <li><strong>02 // Mythic Armor &amp; Helmets Pack (8 Sprites)</strong>: Paladin Helm, Dragon Cuirass, Shadow Hood, Spiked Pauldrons, Celestial Crown, Obsidian Greaves, Elven Gauntlets, Phoenix Shield.</li>
  <li><strong>03 // Cyberpunk &amp; Sci-Fi HUD UI Pack (8 Elements)</strong>: Holographic Radar, Biometric Monitor, Quantum Crosshair, Energy Gauge, Shield Matrix, Targeting Lock, Nano Battery, Data Compass.</li>
  <li><strong>04 // Gemstones &amp; Crystals Pack (8 Sprites)</strong>: Crimson Ruby, Celestial Sapphire, Radiant Emerald, Solar Topaz, Void Amethyst, Prismatic Diamond, Astral Quartz, Dragon Opal.</li>
  <li><strong>05 // Spellbooks &amp; Ancient Tomes Pack (8 Sprites)</strong>: Arcane Grimoire, Necronomicon Tome, Divine Scripture, Pyromancer Book, Void Grimoire, Storm Tome, Permafrost Book, Nature Herbal.</li>
  <li><strong>06 // Monster &amp; Creature Avatars Pack (8 Sprites)</strong>: Goblin Portrait, Skeleton Warrior, Abyssal Demon, Lich Necromancer, Werewolf Beast, Stone Gargoyle, Vampire Count, Toxic Slime.</li>
  <li><strong>07 // Survival Food &amp; Provisions Pack (8 Sprites)</strong>: Roasted Beast Meat, Sourdough Bread, Orchard Apple, Salmon Steak, Swiss Cheese, Forest Mushrooms, Honey Pot, Tavern Sausages.</li>
  <li><strong>08 // Crafting Materials &amp; Ores Pack (8 Sprites)</strong>: Gold Ore Nugget, Mithril Crystal, Dark Iron Ingot, Dragon Scale Hide, Fairy Dust Jar, Ancient Beast Horn, Spider Silk, Magma Coal.</li>
  <li><strong>09 // Rings, Amulets &amp; Talismans Pack (8 Sprites)</strong>: Ruby Signet Ring, Sapphire Claw Ring, Dragon Eye Amulet, Celtic Knot, Emerald Leaf Brooch, Star Necklace, Gold Torc, Skull Ring.</li>
  <li><strong>10 // Dark Magic &amp; Cursed Relics Pack (8 Sprites)</strong>: Voodoo Effigy, Bone Dagger, Soul Lantern, Occult Pentagram, Demon Finger Relic, Raven Skull, Witch Cauldron, Demon Pact Scroll.</li>
</ol>
<hr>
<h3>✨ Technical Specifications:</h3>
<p>• <strong>100% Clean Alpha Transparency PNGs</strong> (Meticulously isolated, zero edge halos)</p>
<p>• <strong>512x512 High-Resolution</strong> game-ready assets + <strong>1024x1024 Master Artworks</strong> included</p>
<p>• <strong>Engine Ready:</strong> Fully tested and compatible with Unity, Godot 4, Unreal Engine 5, RPG Maker, and web canvas.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ <strong>100% Commercial Use:</strong> Cleared for commercial Steam releases, indie games, mobile apps (iOS/Android), and monetized projects.</p>
<p>✅ <strong>Modify &amp; Adapt:</strong> Freely resize, crop, recolor, combine, and animate.</p>
<p>✅ <strong>Royalty-Free &amp; No Attribution Required:</strong> Use without royalty payments or mandatory credits.</p>
<p>❌ You may NOT resell or redistribute these assets as standalone stock graphic files.</p>
"""

vault_summary = "10 genre packs (80 studio sprites) with clean transparency. Weapons, Armor, Sci-Fi HUD, Crystals, Spellbooks, Monsters, Food, Ores, Jewelry, Dark Magic. 100% commercial use."

# Gumroadに各ZIPファイルをアップロード
print("\n📦 Gumroad商品更新 & 10パックZIP添付中...")
update_cmd = [
    GUMROAD_CLI, "products", "update", vault_id,
    "--name", "The Ultimate 2D Game Asset Vault: 10 Genre Starter Packs (80 Studio Sprites)",
    "--currency", "usd",
    "--price", "1.99",
    "--suggested-price", "4.99",
    "--pay-what-you-want",
    "--description", vault_desc,
    "--custom-summary", vault_summary,
]

for p in PACKS:
    zip_path = p["folder"] / p["zip_name"]
    update_cmd.extend([
        "--file", str(zip_path),
        "--file-name", p["zip_name"],
        "--file-description", p["title"]
    ])

print("⏳ アップロード実行中 (10ファイル)...")
res_up = subprocess.run(update_cmd, env=env, capture_output=True, text=True)
if res_up.returncode != 0:
    print(f"❌ Gumroad update 失敗: {res_up.stderr}")
else:
    print("✅ Gumroad update 成功！")

# 最新の商品情報とファイル一覧を取得
print("\n🔍 Gumroad最新商品情報取得中...")
res_view = subprocess.run([GUMROAD_CLI, "products", "view", vault_id, "--json"], env=env, capture_output=True, text=True)
if res_view.returncode == 0:
    prod_data = json.loads(res_view.stdout).get("product", {})
    files = prod_data.get("files", [])
    print(f"現在の登録ファイル数: {len(files)}")
    
    # 01〜10 のファイルIDを抽出
    new_file_ids = []
    for p in PACKS:
        matched = [f for f in files if f.get("name") == p["zip_name"]]
        if matched:
            latest = matched[-1]
            new_file_ids.append((p["zip_name"], latest.get("id")))
            print(f"  ✓ {p['zip_name']} -> ID: {latest.get('id')}")
        else:
            print(f"  ⚠️ 見つかりません: {p['zip_name']}")
    
    # rich_content を再構築（新10ファイルのみを表示対象にする）
    if len(new_file_ids) == 10:
        print("\n📝 購入者ダウンロード画面 (Rich Content) を新10ファイルのみに再構成中...")
        rich_content = [
            {
                "id": "7iMOzts_p7IMRAt9RxJ3dg==",
                "page_id": "7iMOzts_p7IMRAt9RxJ3dg==",
                "title": "Download Your 10 Asset Packs",
                "description": {
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Thank you for purchasing The Ultimate 2D Game Asset Vault! Download your 10 modular genre packs below:"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
        
        for name, fid in new_file_ids:
            rich_content[0]["description"]["content"].append({
                "type": "fileEmbed",
                "attrs": {
                    "id": fid,
                    "uid": None,
                    "collapsed": False
                }
            })
        
        content_json_path = VAULT_DIR / "rich_content_10packs.json"
        with open(content_json_path, "w", encoding="utf-8") as f:
            json.dump(rich_content, f, indent=2, ensure_ascii=False)
        
        res_rc = subprocess.run([
            GUMROAD_CLI, "products", "content", "set", vault_id, str(content_json_path), "--yes"
        ], env=env, capture_output=True, text=True)
        if res_rc.returncode == 0:
            print("✅ 購入者ダウンロード画面 (Rich Content) の更新完了！古いファイルは非表示になりました。")
        else:
            print(f"⚠️ Rich Content 更新失敗: {res_rc.stderr}")

print("\n🎉 デプロイ完了！")
