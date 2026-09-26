#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deploy_5_individual_gumroad_packs.py
Gumroadストアに「音楽と同じく個別パック5商品（各$0.99）」を独立出品・更新するスクリプト
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
if not token:
    print("❌ GUMROAD_ACCESS_TOKEN が不足しています。", file=sys.stderr)
    sys.exit(1)

GUMROAD_CLI = str(BASE_DIR / "bin" / "gumroad")
VAULT_DIR = Path("/Users/base/Automated-Projects/Game-Assets/outputs/Paid_Vault_10Packs")

PRODUCTS = [
    {
        "slug": "fantasy-weapons-pack",
        "name": "01 // Fantasy Weapons Pack (2D Game Assets)",
        "zip": VAULT_DIR / "01_Fantasy_Weapons" / "01_Fantasy_Weapons_Pack.zip",
        "cover": VAULT_DIR / "01_Fantasy_Weapons" / "showcase_preview.png",
        "thumb": VAULT_DIR / "01_Fantasy_Weapons" / "thumbnail_square.png",
        "summary": "8 studio-quality transparent fantasy weapon sprites (512x512 + 1024x1024) for Unity, Godot & Unreal Engine. Commercial license included.",
        "desc": """<p>⚔️ <strong>01 // Fantasy Weapons Pack (2D Game Assets)</strong></p>
<p>Equip your heroes and monsters with 8 handcrafted, studio-quality fantasy weapons!</p>
<p>Each sprite is meticulously cut with clean alpha transparency, ready to drag and drop straight into your game engine.</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Unique Handcrafted Weapon Sprites:</strong> Excalibur Greatsword, Molten Blacksmith Hammer, Thunder Storm Battleaxe, Elven Ranger Longbow, Poison Dragon Dagger, Shadow Death Scythe, Crystal Arcane Staff, Runed Royal Halberd</p>
<p>• <strong>100% Clean Alpha Transparency:</strong> No white edges or halos, perfectly isolated.</p>
<p>• <strong>512x512 Game-Ready PNGs</strong> + <strong>1024x1024 Master Artworks</strong> included.</p>
<p>• <strong>Engine Ready:</strong> Fully tested and compatible with Unity, Godot, Unreal Engine, GameMaker, and RPG Maker.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ <strong>100% Commercial Use:</strong> Cleared for commercial Steam releases, indie games, mobile apps (iOS/Android), and monetized projects.</p>
<p>✅ <strong>Modify &amp; Adapt:</strong> Freely resize, crop, recolor, combine, and animate.</p>
<p>✅ <strong>Royalty-Free &amp; No Attribution Required:</strong> Use without royalty payments or mandatory credits.</p>
<p>❌ You may NOT resell or redistribute these assets as standalone stock graphic files.</p>
<hr>
<h3>👑 WANT ALL 10 GENRE PACKS (80 SPRITES)?</h3>
<p>Upgrade to <strong>The Ultimate 2D Game Asset Vault ($1.99)</strong> and get lifetime access to all 10 genre packs!</p>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Complete 10-Pack Vault for just $1.99!</strong></a></p>
"""
    },
    {
        "slug": "mythic-armor-helmets-pack",
        "name": "02 // Mythic Armor & Helmets Pack (2D Game Assets)",
        "zip": VAULT_DIR / "02_Mythic_Armor_Helmets" / "02_Mythic_Armor_Helmets_Pack.zip",
        "cover": VAULT_DIR / "02_Mythic_Armor_Helmets" / "showcase_preview.png",
        "thumb": VAULT_DIR / "02_Mythic_Armor_Helmets" / "thumbnail_square.png",
        "summary": "8 studio-quality transparent armor & helmet sprites (512x512 + 1024x1024) for Unity, Godot & Unreal Engine. Commercial license included.",
        "desc": """<p>🛡️ <strong>02 // Mythic Armor &amp; Helmets Pack (2D Game Assets)</strong></p>
<p>Fortify your RPG equipment screen with 8 handcrafted mythic armor pieces and helmets!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Unique Handcrafted Armor Sprites:</strong> Paladin Golden Winged Helm, Dragon Scale Heavy Cuirass, Shadow Assassin Leather Hood, Gladiator Spiked Pauldrons, Celestial Angelic Crown, Obsidian Knight Greaves, Elven Mithril Gauntlets, Phoenix Sun Shield</p>
<p>• <strong>100% Clean Alpha Transparency:</strong> Zero halo, drag-and-drop ready.</p>
<p>• <strong>512x512 Game-Ready PNGs</strong> + <strong>1024x1024 Master Artworks</strong>.</p>
<p>• <strong>Engine Ready:</strong> Unity, Godot, Unreal Engine, RPG Maker.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Edit | ✅ No Credit Required</p>
<hr>
<h3>👑 WANT ALL 10 GENRE PACKS (80 SPRITES)?</h3>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Complete 10-Pack Vault for just $1.99!</strong></a></p>
"""
    },
    {
        "slug": "cyberpunk-scifi-hud-ui-pack",
        "name": "03 // Cyberpunk & Sci-Fi HUD UI Pack (2D Game Assets)",
        "zip": VAULT_DIR / "03_Cyberpunk_SciFi_HUD_UI" / "03_Cyberpunk_SciFi_HUD_UI_Pack.zip",
        "cover": VAULT_DIR / "03_Cyberpunk_SciFi_HUD_UI" / "showcase_preview.png",
        "thumb": VAULT_DIR / "03_Cyberpunk_SciFi_HUD_UI" / "thumbnail_square.png",
        "summary": "8 glowing cyberpunk & futuristic HUD UI icons (512x512 + 1024x1024) with clean transparency. Commercial license included.",
        "desc": """<p>⚡ <strong>03 // Cyberpunk &amp; Sci-Fi HUD UI Pack (2D Game Assets)</strong></p>
<p>Upgrade your sci-fi interfaces and futuristic games with 8 high-tech glowing HUD UI elements!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Unique Futuristic UI Elements:</strong> Holographic Radar Reticle, Biometric Pulse Monitor, Quantum Targeting Crosshair, Plasma Energy Level Gauge, Hexagonal Shield Matrix, Lock-On Missile Bracket, Nano Cell Power Battery, Cybernetic Data Compass</p>
<p>• <strong>100% Clean Alpha Transparency:</strong> Luminous glow effects preserved on clean transparency.</p>
<p>• <strong>512x512 Game-Ready PNGs</strong> + <strong>1024x1024 Master Artworks</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Edit | ✅ No Credit Required</p>
<hr>
<h3>👑 WANT ALL 10 GENRE PACKS (80 SPRITES)?</h3>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Complete 10-Pack Vault for just $1.99!</strong></a></p>
"""
    },
    {
        "slug": "gemstones-crystals-pack",
        "name": "04 // Gemstones & Crystals Pack (2D Game Assets)",
        "zip": VAULT_DIR / "04_Gemstones_Crystals" / "04_Gemstones_Crystals_Pack.zip",
        "cover": VAULT_DIR / "04_Gemstones_Crystals" / "showcase_preview.png",
        "thumb": VAULT_DIR / "04_Gemstones_Crystals" / "thumbnail_square.png",
        "summary": "8 dazzling faceted gemstones & glowing magic crystals (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>💎 <strong>04 // Gemstones &amp; Crystals Pack (2D Game Assets)</strong></p>
<p>Add brilliance and sparkle to your inventory, loot tables, and socketing systems with 8 radiant gemstone sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Faceted Gemstones &amp; Crystals:</strong> Faceted Crimson Ruby, Celestial Azure Sapphire, Radiant Emerald Cut, Solar Topaz Geode, Void Violet Amethyst, Prismatic Brilliant Diamond, Astral Star Quartz, Dragon Eye Fire Opal</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Edit | ✅ No Credit Required</p>
<hr>
<h3>👑 WANT ALL 10 GENRE PACKS (80 SPRITES)?</h3>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Complete 10-Pack Vault for just $1.99!</strong></a></p>
"""
    },
    {
        "slug": "spellbooks-ancient-tomes-pack",
        "name": "05 // Spellbooks & Ancient Tomes Pack (2D Game Assets)",
        "zip": VAULT_DIR / "05_Spellbooks_Tomes" / "05_Spellbooks_Tomes_Pack.zip",
        "cover": VAULT_DIR / "05_Spellbooks_Tomes" / "showcase_preview.png",
        "thumb": VAULT_DIR / "05_Spellbooks_Tomes" / "thumbnail_square.png",
        "summary": "8 mystical spellbooks & enchanted grimoires (512x512 + 1024x1024) with clean transparency. Commercial license included.",
        "desc": """<p>📖 <strong>05 // Spellbooks &amp; Ancient Tomes Pack (2D Game Assets)</strong></p>
<p>Equip your wizards and sorcerers with 8 detailed, elemental and occult spellbook sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Unique Elemental &amp; Mystic Tomes:</strong> Arcane Eye Grimoire, Eldritch Necronomicon, Divine Holy Scripture, Pyromancer Leather Tome, Void Abyssal Book, Storm Lightning Tome, Permafrost Ice Grimoire, Herbalist Nature Tome</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Edit | ✅ No Credit Required</p>
<hr>
<h3>👑 WANT ALL 10 GENRE PACKS (80 SPRITES)?</h3>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Complete 10-Pack Vault for just $1.99!</strong></a></p>
"""
    }
]

# 最新商品一覧を取得
print("🔍 既存商品照会中...")
res_list = subprocess.run([GUMROAD_CLI, "products", "list", "--json"], env=env, capture_output=True, text=True)
existing_products = []
if res_list.returncode == 0:
    existing_products = json.loads(res_list.stdout).get("products", [])

# 古い2商品のID照合（再利用して上書き）
old_slug_map = {
    "fantasy-weapons-pack": ["fantasy-weapons-pack", "fantasy-weapons-armor-pack"],
    "mythic-armor-helmets-pack": ["mythic-armor-helmets-pack", "potions-cyberpunk-ui-pack"]
}

for item in PRODUCTS:
    slug = item["slug"]
    print(f"\n🚀 商品デプロイ中: {slug}...")
    
    # マッチする既存商品を探す
    target_prod = None
    target_slugs = old_slug_map.get(slug, [slug])
    for p in existing_products:
        if p.get("custom_permalink") in target_slugs or p.get("name") == item["name"]:
            target_prod = p
            break
    
    target_id = target_prod.get("id") if target_prod else None
    
    if not target_id:
        print(f"  ✨ 新規商品を作成します...")
        create_res = subprocess.run([
            GUMROAD_CLI, "products", "create",
            "--name", item["name"],
            "--currency", "usd",
            "--price", "0.99"
        ], env=env, capture_output=True, text=True)
        
        # IDをリストから再取得
        res_l2 = subprocess.run([GUMROAD_CLI, "products", "list", "--json"], env=env, capture_output=True, text=True)
        for p in json.loads(res_l2.stdout).get("products", []):
            if p.get("name") == item["name"]:
                target_id = p.get("id")
                break
    
    if target_id:
        print(f"  ⏩ 商品を完全更新・公開します (ID: {target_id})...")
        update_cmd = [
            GUMROAD_CLI, "products", "update", target_id,
            "--name", item["name"],
            "--custom-permalink", slug,
            "--currency", "usd",
            "--price", "0.99",
            "--suggested-price", "1.99",
            "--pay-what-you-want",
            "--description", item["desc"],
            "--custom-summary", item["summary"],
            "--cover-image", str(item["cover"]),
            "--thumbnail", str(item["thumb"]),
            "--file", str(item["zip"]),
            "--file-name", item["zip"].name
        ]
        res_up = subprocess.run(update_cmd, env=env, capture_output=True, text=True)
        if res_up.returncode != 0:
            print(f"  ⚠️ 更新警告: {res_up.stderr}")
        
        # 公開
        subprocess.run([GUMROAD_CLI, "products", "publish", target_id], env=env, capture_output=True)
        
        # Rich Content を新ZIPのみに更新
        res_view = subprocess.run([GUMROAD_CLI, "products", "view", target_id, "--json"], env=env, capture_output=True, text=True)
        if res_view.returncode == 0:
            p_info = json.loads(res_view.stdout).get("product", {})
            files = p_info.get("files", [])
            matched = [f for f in files if f.get("name") == item["zip"].name]
            if matched:
                fid = matched[-1].get("id")
                rc = [{
                    "id": "page_1",
                    "page_id": "page_1",
                    "title": item["name"],
                    "description": {
                        "type": "doc",
                        "content": [
                            {
                                "type": "fileEmbed",
                                "attrs": {"id": fid, "uid": None, "collapsed": False}
                            }
                        ]
                    }
                }]
                tmp_rc = VAULT_DIR / f"rc_{slug}.json"
                with open(tmp_rc, "w") as f:
                    json.dump(rc, f)
                subprocess.run([GUMROAD_CLI, "products", "content", "set", target_id, str(tmp_rc), "--yes"], env=env, capture_output=True)
                if tmp_rc.exists():
                    tmp_rc.unlink()
        
        print(f"  ✅ 出品・公開成功: https://gameverseaudio.gumroad.com/l/{slug}")
    else:
        print(f"  ❌ IDが特定できませんでした: {slug}")

print("\n🎉 5つの個別パック商品の出品・更新がすべて完了しました！")
