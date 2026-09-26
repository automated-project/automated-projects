#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deploy_all_10_individual_gumroad_packs.py
Gumroadストアに「全10パックの個別単品商品（各$0.99）」を独立出品・完全更新するスクリプト

【構成 (01〜10)】
01 // Fantasy Weapons Pack
02 // Mythic Armor & Helmets Pack
03 // Cyberpunk & Sci-Fi HUD UI Pack
04 // Gemstones & Crystals Pack
05 // Spellbooks & Ancient Tomes Pack
06 // Monster & Creature Avatars Pack
07 // Survival Food & Provisions Pack
08 // Crafting Materials & Ores Pack
09 // Rings, Amulets & Talismans Pack
10 // Dark Magic & Cursed Relics Pack
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

UPGRADE_BOX = """<hr>
<h3>👑 WANT ALL 10 GENRE PACKS (80 SPRITES)?</h3>
<p>Upgrade to <strong>The Ultimate 2D Game Asset Vault ($1.99)</strong> and get lifetime access to all 10 genre packs!</p>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Complete 10-Pack Vault for just $1.99!</strong></a></p>
"""

PRODUCTS = [
    {
        "num": "01",
        "slug": "fantasy-weapons-pack",
        "name": "01 // Fantasy Weapons Pack (2D Game Assets)",
        "folder": VAULT_DIR / "01_Fantasy_Weapons",
        "zip_name": "01_Fantasy_Weapons_Pack.zip",
        "summary": "8 studio-quality transparent fantasy weapon sprites (512x512 + 1024x1024) for Unity, Godot & Unreal Engine. Commercial license included.",
        "desc": """<p>⚔️ <strong>01 // Fantasy Weapons Pack (2D Game Assets)</strong></p>
<p>Equip your heroes and monsters with 8 handcrafted, studio-quality fantasy weapons!</p>
<p>Each sprite is meticulously cut with clean alpha transparency, ready to drag and drop straight into your game engine.</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Unique Handcrafted Weapon Sprites:</strong> Excalibur Greatsword, Molten Blacksmith Hammer, Thunder Storm Battleaxe, Elven Ranger Longbow, Poison Dragon Dagger, Shadow Death Scythe, Crystal Arcane Staff, Runed Royal Halberd</p>
<p>• <strong>100% Clean Alpha Transparency:</strong> Zero halo, perfectly isolated.</p>
<p>• <strong>512x512 Game-Ready PNGs</strong> + <strong>1024x1024 Master Artworks</strong> included.</p>
<p>• <strong>Engine Ready:</strong> Unity, Godot, Unreal Engine, GameMaker, RPG Maker.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "02",
        "slug": "mythic-armor-helmets-pack",
        "name": "02 // Mythic Armor & Helmets Pack (2D Game Assets)",
        "folder": VAULT_DIR / "02_Mythic_Armor_Helmets",
        "zip_name": "02_Mythic_Armor_Helmets_Pack.zip",
        "summary": "8 studio-quality transparent armor & helmet sprites (512x512 + 1024x1024) for Unity, Godot & Unreal Engine. Commercial license included.",
        "desc": """<p>🛡️ <strong>02 // Mythic Armor &amp; Helmets Pack (2D Game Assets)</strong></p>
<p>Fortify your RPG equipment screen with 8 handcrafted mythic armor pieces and helmets!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Unique Handcrafted Armor Sprites:</strong> Paladin Golden Winged Helm, Dragon Scale Heavy Cuirass, Shadow Assassin Leather Hood, Gladiator Spiked Pauldrons, Celestial Angelic Crown, Obsidian Knight Greaves, Elven Mithril Gauntlets, Phoenix Sun Shield</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "03",
        "slug": "cyberpunk-scifi-hud-ui-pack",
        "name": "03 // Cyberpunk & Sci-Fi HUD UI Pack (2D Game Assets)",
        "folder": VAULT_DIR / "03_Cyberpunk_SciFi_HUD_UI",
        "zip_name": "03_Cyberpunk_SciFi_HUD_UI_Pack.zip",
        "summary": "8 glowing cyberpunk & futuristic HUD UI icons (512x512 + 1024x1024) with clean transparency. Commercial license included.",
        "desc": """<p>⚡ <strong>03 // Cyberpunk &amp; Sci-Fi HUD UI Pack (2D Game Assets)</strong></p>
<p>Upgrade your sci-fi interfaces and futuristic games with 8 high-tech glowing HUD UI elements!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Futuristic UI Elements:</strong> Holographic Radar Reticle, Biometric Pulse Monitor, Quantum Targeting Crosshair, Plasma Energy Level Gauge, Hexagonal Shield Matrix, Lock-On Missile Bracket, Nano Cell Power Battery, Cybernetic Data Compass</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "04",
        "slug": "gemstones-crystals-pack",
        "name": "04 // Gemstones & Crystals Pack (2D Game Assets)",
        "folder": VAULT_DIR / "04_Gemstones_Crystals",
        "zip_name": "04_Gemstones_Crystals_Pack.zip",
        "summary": "8 dazzling faceted gemstones & glowing magic crystals (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>💎 <strong>04 // Gemstones &amp; Crystals Pack (2D Game Assets)</strong></p>
<p>Add brilliance and sparkle to your inventory, loot tables, and socketing systems with 8 radiant gemstone sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Faceted Gemstones &amp; Crystals:</strong> Faceted Crimson Ruby, Celestial Azure Sapphire, Radiant Emerald Cut, Solar Topaz Geode, Void Violet Amethyst, Prismatic Brilliant Diamond, Astral Star Quartz, Dragon Eye Fire Opal</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "05",
        "slug": "spellbooks-ancient-tomes-pack",
        "name": "05 // Spellbooks & Ancient Tomes Pack (2D Game Assets)",
        "folder": VAULT_DIR / "05_Spellbooks_Tomes",
        "zip_name": "05_Spellbooks_Tomes_Pack.zip",
        "summary": "8 mystical spellbooks & enchanted grimoires (512x512 + 1024x1024) with clean transparency. Commercial license included.",
        "desc": """<p>📖 <strong>05 // Spellbooks &amp; Ancient Tomes Pack (2D Game Assets)</strong></p>
<p>Equip your wizards and sorcerers with 8 detailed, elemental and occult spellbook sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Elemental &amp; Mystic Tomes:</strong> Arcane Eye Grimoire, Eldritch Necronomicon, Divine Holy Scripture, Pyromancer Leather Tome, Void Abyssal Book, Storm Lightning Tome, Permafrost Ice Grimoire, Herbalist Nature Tome</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "06",
        "slug": "monster-creature-avatars-pack",
        "name": "06 // Monster & Creature Avatars Pack (2D Game Assets)",
        "folder": VAULT_DIR / "06_Monster_Creature_Avatars",
        "zip_name": "06_Monster_Creature_Avatars_Pack.zip",
        "summary": "8 fierce monster & creature portrait avatars (512x512 + 1024x1024) with clean transparency. Commercial license included.",
        "desc": """<p>👾 <strong>06 // Monster &amp; Creature Avatars Pack (2D Game Assets)</strong></p>
<p>Populate your dungeons and turn-based combat encounters with 8 menacing monster face portraits!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Monster &amp; Creature Portraits:</strong> Swamp Goblin Portrait, Undead Skeleton Warrior, Horned Abyssal Demon, Withered Lich Necromancer, Savage Werewolf Beast, Gothic Stone Gargoyle, Vampire Blood Count, Toxic Slime Creature</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "07",
        "slug": "survival-food-cooking-pack",
        "name": "07 // Survival Food & Provisions Pack (2D Game Assets)",
        "folder": VAULT_DIR / "07_Survival_Food_Cooking",
        "zip_name": "07_Survival_Food_Cooking_Pack.zip",
        "summary": "8 delicious survival food & tavern provision sprites (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>🍖 <strong>07 // Survival Food &amp; Provisions Pack (2D Game Assets)</strong></p>
<p>Feed your adventurers and stock your tavern menus with 8 mouthwatering food sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Survival Food Sprites:</strong> Roasted Beast Meat on Bone, Crusty Sourdough Loaf, Enchanted Orchard Apple, Grilled Salmon Steak, Aged Swiss Cheese Wedge, Wild Forest Mushrooms, Golden Honeycomb Clay Pot, Smoked Tavern Sausages</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "08",
        "slug": "crafting-materials-ores-pack",
        "name": "08 // Crafting Materials & Ores Pack (2D Game Assets)",
        "folder": VAULT_DIR / "08_Crafting_Materials_Ores",
        "zip_name": "08_Crafting_Materials_Ores_Pack.zip",
        "summary": "8 essential crafting materials, ingots & monster drops (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>⚒️ <strong>08 // Crafting Materials &amp; Ores Pack (2D Game Assets)</strong></p>
<p>Build your game's crafting economy and gathering systems with 8 high-detail resource sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Crafting Materials &amp; Ores:</strong> Raw Gold Ore Nugget, Mithril Crystal Ore, Dark Iron Ingot Stack, Dragon Scale Leather Hide, Luminous Fairy Dust Jar, Ancient Beast Horn, Giant Spider Silk Spool, Elemental Magma Coal</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "09",
        "slug": "rings-amulets-jewelry-pack",
        "name": "09 // Rings, Amulets & Talismans Pack (2D Game Assets)",
        "folder": VAULT_DIR / "09_Rings_Amulets_Jewelry",
        "zip_name": "09_Rings_Amulets_Jewelry_Pack.zip",
        "summary": "8 enchanted rings, necklaces & mystic talismans (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>💍 <strong>09 // Rings, Amulets &amp; Talismans Pack (2D Game Assets)</strong></p>
<p>Equip your accessory and relic slots with 8 intricately crafted jewelry and talisman sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Rings, Amulets &amp; Talismans:</strong> Lion Signet Ruby Ring, Dragon Claw Sapphire Ring, Dragon Eye Medallion Amulet, Celtic Trinity Knot Talisman, Elven Emerald Leaf Brooch, Star of Eternity Necklace, Dwarven Warrior Torc, Gothic Skull Knuckle Ring</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "10",
        "slug": "dark-magic-necromancy-pack",
        "name": "10 // Dark Magic & Cursed Relics Pack (2D Game Assets)",
        "folder": VAULT_DIR / "10_Dark_Magic_Necromancy",
        "zip_name": "10_Dark_Magic_Necromancy_Pack.zip",
        "summary": "8 sinister dark magic, occult & cursed relics (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>💀 <strong>10 // Dark Magic &amp; Cursed Relics Pack (2D Game Assets)</strong></p>
<p>Channel the forbidden arts with 8 dark occult relics, sacrificial blades, and cursed artifacts!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Dark Magic &amp; Cursed Relics:</strong> Cursed Voodoo Effigy, Sacrificial Bone Dagger, Trapped Soul Lantern, Occult Pentagram Scrying Orb, Mummified Demon Finger Relic, Raven Skull Occult Fetish, Bubbling Witch Cauldron, Blood Demon Pact Scroll</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    }
]

print("🔍 Gumroad既存商品一覧取得中...")
res_list = subprocess.run([GUMROAD_CLI, "products", "list", "--json"], env=env, capture_output=True, text=True)
existing_products = []
if res_list.returncode == 0:
    existing_products = json.loads(res_list.stdout).get("products", [])

for item in PRODUCTS:
    slug = item["slug"]
    name = item["name"]
    zip_path = item["folder"] / item["zip_name"]
    cover_path = item["folder"] / "showcase_preview.png"
    thumb_path = item["folder"] / "thumbnail_square.png"
    
    print(f"\n🚀 [{item['num']}/10] 商品デプロイ中: {name} ({slug})...")
    
    # 既存商品チェック
    target_id = None
    for p in existing_products:
        if p.get("custom_permalink") == slug or p.get("name") == name:
            target_id = p.get("id")
            break
    
    if not target_id:
        print("  ✨ 新規商品作成中...")
        res_create = subprocess.run([
            GUMROAD_CLI, "products", "create",
            "--name", name,
            "--currency", "usd",
            "--price", "0.99"
        ], env=env, capture_output=True, text=True)
        
        # ID再取得
        res_l2 = subprocess.run([GUMROAD_CLI, "products", "list", "--json"], env=env, capture_output=True, text=True)
        for p in json.loads(res_l2.stdout).get("products", []):
            if p.get("name") == name:
                target_id = p.get("id")
                break
    
    if target_id:
        print(f"  ⏩ 商品更新実行中 (ID: {target_id})...")
        update_cmd = [
            GUMROAD_CLI, "products", "update", target_id,
            "--name", name,
            "--custom-permalink", slug,
            "--currency", "usd",
            "--price", "0.99",
            "--suggested-price", "1.99",
            "--pay-what-you-want",
            "--description", item["desc"],
            "--custom-summary", item["summary"],
            "--cover-image", str(cover_path),
            "--thumbnail", str(thumb_path),
            "--file", str(zip_path),
            "--file-name", item["zip_name"]
        ]
        res_up = subprocess.run(update_cmd, env=env, capture_output=True, text=True)
        
        # 公開
        subprocess.run([GUMROAD_CLI, "products", "publish", target_id], env=env, capture_output=True)
        
        # Rich Content を新ZIPのみに更新
        res_view = subprocess.run([GUMROAD_CLI, "products", "view", target_id, "--json"], env=env, capture_output=True, text=True)
        if res_view.returncode == 0:
            p_info = json.loads(res_view.stdout).get("product", {})
            files = p_info.get("files", [])
            matched = [f for f in files if f.get("name") == item["zip_name"]]
            if matched:
                fid = matched[-1].get("id")
                rc = [{
                    "id": "page_1",
                    "page_id": "page_1",
                    "title": name,
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
                tmp_rc = item["folder"] / f"rc_{slug}.json"
                with open(tmp_rc, "w") as f:
                    json.dump(rc, f)
                subprocess.run([GUMROAD_CLI, "products", "content", "set", target_id, str(tmp_rc), "--yes"], env=env, capture_output=True)
                if tmp_rc.exists():
                    tmp_rc.unlink()
        
        print(f"  ✅ 出品・公開成功: https://gameverseaudio.gumroad.com/l/{slug}")
    else:
        print(f"  ❌ ID特定失敗: {slug}")

print("\n🎉 全10パックの個別単品商品（各$0.99）の出品・公開がすべて完了しました！")
