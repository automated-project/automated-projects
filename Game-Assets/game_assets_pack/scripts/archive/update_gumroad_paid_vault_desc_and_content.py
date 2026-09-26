#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import subprocess
import requests
import urllib.parse
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
GUMROAD_BIN = str(BASE_DIR / "bin" / "gumroad")
PID = "c07Os4dAkeUFa2VBAne4YQ=="

env = os.environ.copy()
env_path = BASE_DIR / ".env"
token = ""
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("GUMROAD_ACCESS_TOKEN="):
                token = line.split("=", 1)[1].strip().strip("\"'")
                env["GUMROAD_ACCESS_TOKEN"] = token

if not token:
    print("❌ GUMROAD_ACCESS_TOKEN が見つかりません")
    sys.exit(1)

# 1. 説明欄HTML（開発者向けユースケース、対応/非対応、無料版導線、ゆったり余白）
new_desc_html = """<p>👑 <strong>The Ultimate 2D Game Asset Vault &mdash; 10 Genre Starter Packs (80 Handcrafted Studio Sprites)</strong></p>

<p>Designed specifically for indie game developers. Stop spending hours manually resizing and cleaning messy backgrounds &mdash; every sprite in this vault comes pre-scaled into <strong>5 game-ready resolutions + master artwork</strong> with 100% clean alpha transparency.</p>

<p><br></p>
<hr>
<p><br></p>

<h3>🎮 Game-Ready Resolutions &amp; Use Cases:</h3>

<p>Ready to drag &amp; drop straight into your game UI:</p>

<ul>
  <li><strong>32x32:</strong> Ideal for dense Inventory Grids, Action Hotbars, and Minimap Icons.</li>
<br>
  <li><strong>64x64:</strong> Standard for RPG Inventories, Skill Trees, and Crafting Recipe Slots.</li>
<br>
  <li><strong>128x128:</strong> Perfect for Item Inspection Popups, Tooltips, and Loot Drop banners.</li>
<br>
  <li><strong>256x256:</strong> Great for Shop Merchant UI, Equipment Dialogs, and Quest Menus.</li>
<br>
  <li><strong>512x512:</strong> Ultra-crisp for Hero Equipment Displays, Dialog Cutscenes, and High-DPI screens.</li>
<br>
  <li><strong>1024x1024 Master Art:</strong> Full master artwork included for Card Battlers, Gacha Banners, and Promo Art.</li>
</ul>

<p><br></p>
<hr>
<p><br></p>

<h3>⚙️ Engine &amp; Platform Compatibility:</h3>

<p><strong>✅ What You CAN Do:</strong></p>
<ul>
  <li><strong>Universal Drag &amp; Drop:</strong> 100% compatible with <strong>Unity, Godot 4, Unreal Engine 5, RPG Maker MZ/MV, GameMaker, Construct 3, and Web Canvas (Phaser / Pixi.js)</strong>.</li>
<br>
  <li><strong>Commercial Clearance:</strong> 100% royalty-free for commercial PC/Steam games, mobile apps (iOS/Android), and web games.</li>
<br>
  <li><strong>Full Creative Freedom:</strong> Freely crop, tint, recolor, combine, and animate.</li>
<br>
  <li><strong>No Mandatory Attribution:</strong> No credit required (though appreciated).</li>
</ul>

<p><br></p>

<p><strong>❌ What This Pack IS NOT (Avoid Misunderstanding):</strong></p>
<ul>
  <li><strong>NOT 3D Models:</strong> These are high-quality 2D transparent PNG graphics/textures.</li>
<br>
  <li><strong>NOT Animated Sprite Sheets:</strong> These are static item/icon sprites.</li>
<br>
  <li><strong>NOT Pixel Art:</strong> These are detailed, painted illustrated assets.</li>
</ul>

<p><br></p>
<hr>
<p><br></p>

<h3>📦 What's Inside the 10 Individual Packs (80 Unique Sprites):</h3>

<ol>
  <li><strong>01 // Fantasy Weapons Pack (8 Sprites)</strong>: Excalibur Greatsword, Molten Hammer, Thunder Battleaxe, Elven Longbow, Dragon Dagger, Shadow Scythe, Crystal Staff, Runed Halberd.</li>
<br>
  <li><strong>02 // Mythic Armor &amp; Helmets Pack (8 Sprites)</strong>: Paladin Helm, Dragon Cuirass, Shadow Hood, Spiked Pauldrons, Celestial Crown, Obsidian Greaves, Elven Gauntlets, Phoenix Shield.</li>
<br>
  <li><strong>03 // Cyberpunk &amp; Sci-Fi HUD UI Pack (8 Elements)</strong>: Holographic Radar, Biometric Monitor, Quantum Crosshair, Energy Gauge, Shield Matrix, Targeting Lock, Nano Battery, Data Compass.</li>
<br>
  <li><strong>04 // Gemstones &amp; Crystals Pack (8 Sprites)</strong>: Crimson Ruby, Celestial Sapphire, Radiant Emerald, Solar Topaz, Void Amethyst, Prismatic Diamond, Astral Quartz, Dragon Opal.</li>
<br>
  <li><strong>05 // Spellbooks &amp; Ancient Tomes Pack (8 Sprites)</strong>: Arcane Grimoire, Necronomicon Tome, Divine Scripture, Pyromancer Book, Void Grimoire, Storm Tome, Permafrost Book, Nature Herbal.</li>
<br>
  <li><strong>06 // Monster &amp; Creature Avatars Pack (8 Sprites)</strong>: Goblin Portrait, Skeleton Warrior, Abyssal Demon, Lich Necromancer, Werewolf Beast, Stone Gargoyle, Vampire Count, Toxic Slime.</li>
<br>
  <li><strong>07 // Survival Food &amp; Provisions Pack (8 Sprites)</strong>: Roasted Beast Meat, Sourdough Bread, Orchard Apple, Salmon Steak, Swiss Cheese, Forest Mushrooms, Honey Pot, Tavern Sausages.</li>
<br>
  <li><strong>08 // Crafting Materials &amp; Ores Pack (8 Sprites)</strong>: Gold Ore Nugget, Mithril Crystal, Dark Iron Ingot, Dragon Scale Hide, Fairy Dust Jar, Ancient Beast Horn, Spider Silk, Magma Coal.</li>
<br>
  <li><strong>09 // Rings, Amulets &amp; Talismans Pack (8 Sprites)</strong>: Ruby Signet Ring, Sapphire Claw Ring, Dragon Eye Amulet, Celtic Knot, Emerald Leaf Brooch, Star Necklace, Gold Torc, Skull Ring.</li>
<br>
  <li><strong>10 // Dark Magic &amp; Cursed Relics Pack (8 Sprites)</strong>: Voodoo Effigy, Bone Dagger, Soul Lantern, Occult Pentagram, Demon Finger Relic, Raven Skull, Witch Cauldron, Demon Pact Scroll.</li>
</ol>

<p><br></p>
<hr>
<p><br></p>

<h3>🎁 Want to Test Quality First? (Try Before You Buy):</h3>

<p>Want to verify our transparent PNGs, resolution scaling, and engine compatibility before buying?</p>

<p>👉 <strong><a href="https://gameverseaudio.gumroad.com/l/free-game-assets">Download our Free 2D Game Asset Mega Starter Pack ($0 / 40 Sprites)</a></strong></p>

<p><br></p>
<hr>
<p><br></p>

<h3>🎮 Check Out Our Official itch.io Store:</h3>
<p>Browse our entire catalog of indie game music &amp; assets on itch.io:</p>
<p>👉 <strong><a href="https://gameverse-audio.itch.io" target="_blank">Visit GameVerse Audio on itch.io</a></strong></p>"""

print("1. Gumroad 商品説明文を最新版に更新中...")
cmd = [GUMROAD_BIN, "products", "update", PID, "--description", new_desc_html, "--currency", "usd", "--price", "0.99", "--yes"]
res = subprocess.run(cmd, env=env, text=True, capture_output=True)
print("  Description update result:", res.stdout.strip())

# 2. 最新のマルチ解像度10ZIPを正確に特定して content.json に設定
print("\n2. 最新の10パックZIPを特定中...")
r_prod = requests.get(f"https://api.gumroad.com/v2/products/{PID}", headers={"Authorization": f"Bearer {token}"}).json()
files = r_prod.get("product", {}).get("files", [])

TARGET_PACK_NAMES = [
    "01_Fantasy_Weapons_Pack.zip",
    "02_Mythic_Armor_Helmets_Pack.zip",
    "03_Cyberpunk_SciFi_HUD_UI_Pack.zip",
    "04_Gemstones_Crystals_Pack.zip",
    "05_Spellbooks_Tomes_Pack.zip",
    "06_Monster_Creature_Avatars_Pack.zip",
    "07_Survival_Food_Cooking_Pack.zip",
    "08_Crafting_Materials_Ores_Pack.zip",
    "09_Rings_Amulets_Jewelry_Pack.zip",
    "10_Dark_Magic_Necromancy_Pack.zip",
]

latest_10_file_ids = []
for p_name in TARGET_PACK_NAMES:
    # URLまたはNameから最も新しいファイルIDを探す
    matched_candidates = []
    for f in files:
        url_decoded = urllib.parse.unquote(f.get("url") or "")
        name_str = f.get("name") or ""
        if p_name.lower() in url_decoded.lower() or p_name.lower() in name_str.lower():
            matched_candidates.append(f)
    if matched_candidates:
        # 最新のものを選択（リスト内の最新、サイズが0でないもの）
        chosen = matched_candidates[0]
        for c in matched_candidates:
            if c.get("size") and c["size"] > 0:
                chosen = c
        latest_10_file_ids.append(chosen["id"])
        print(f"  ✅ [MATCH {len(latest_10_file_ids)}/10] {p_name} -> ID: {chosen['id']} (Size: {chosen.get('size')} bytes)")
    else:
        print(f"  ❌ 未マッチ: {p_name}")

assert len(latest_10_file_ids) == 10, f"エラー: 10パック全てがマッチしませんでした (実数: {len(latest_10_file_ids)})"

# content.json の更新
content_payload = [
    {
        "id": "asset-vault-content-page",
        "title": "The Ultimate 2D Game Asset Vault: 10 Genre Starter Packs (80 Sprites)",
        "description": {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Thank you for purchasing The Ultimate 2D Game Asset Vault by GameVerse Audio! Download each of the 10 modular genre packs below. Each pack includes 5 game-ready resolutions (32x32, 64x64, 128x128, 256x256, 512x512) + 1024x1024 Master Art + 100% clean alpha transparency PNGs + Commercial License."
                        }
                    ]
                }
            ] + [
                {
                    "type": "fileEmbed",
                    "attrs": {"id": fid, "collapsed": False}
                } for fid in latest_10_file_ids
            ]
        }
    }
]

content_json_path = Path("/tmp/gumroad_asset_vault_10packs_content.json")
content_json_path.write_text(json.dumps(content_payload, indent=2), encoding="utf-8")

print("\n3. Gumroad の納品画面（content.json）へ最新10パックを適用中...")
r_set = subprocess.run([GUMROAD_BIN, "products", "content", "set", PID, str(content_json_path), "--yes"], env=env, text=True, capture_output=True)
print("  Content set result:", r_set.stdout.strip())

# バリデーション
print("\n4. 🔍 整合性バリデーション実行中...")
r_verify = subprocess.run([GUMROAD_BIN, "products", "content", "get", PID], env=env, text=True, capture_output=True)
verified_content = json.loads(r_verify.stdout)
verified_embeds = [item for p in verified_content for item in p.get("description", {}).get("content", []) if item.get("type") == "fileEmbed"]

print(f"  検証結果: 納品画面に埋め込まれたファイル数 = {len(verified_embeds)} 個")
assert len(verified_embeds) == 10, f"エラー: 埋め込みファイル数が10ではありません (実数: {len(verified_embeds)})"
print("  🎉 完璧です！Gumroadの納品画面に10パック全てが過不足なく確実に配備されました！")
