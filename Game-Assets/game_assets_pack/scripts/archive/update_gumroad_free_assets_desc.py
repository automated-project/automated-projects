#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import subprocess
import requests
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
GUMROAD_BIN = str(BASE_DIR / "bin" / "gumroad")
PID = "ozQ4-e20_gROzj378uBJrA=="

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

new_desc_html = """<p>🎁 <strong>[FREE] 2D Game Asset Mega Starter Pack &mdash; 5 Complete Packs (40 Handcrafted Studio Sprites)</strong></p>

<p>Kickstart your indie game project with our massive, studio-grade starter collection. No more wasting time manually resizing or cleaning jagged edges &mdash; every sprite comes pre-scaled into <strong>5 game-ready resolutions + full 1024px master art</strong> with 100% clean alpha transparency.</p>

<p><br></p>
<hr>
<p><br></p>

<h3>👑 WANT ALL 10 EXPANDED GENRE PACKS (80 UNIQUE SPRITES)?</h3>

<p>Upgrade to <strong><a href="https://gameverseaudio.gumroad.com/l/game-asset-vault">The Ultimate 2D Game Asset Vault (99¢)</a></strong> to unlock the complete studio library: Weapons, Mythic Armor, Sci-Fi HUD UI, Gemstones, Spellbooks, Monster Avatars, Food, Ores, Jewelry &amp; Dark Magic!</p>

<p>👉 <strong><a href="https://gameverseaudio.gumroad.com/l/game-asset-vault">Unlock The Complete 10-Pack Vault for just 99¢!</a></strong></p>

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

<h3>📦 What's Inside This Free Download (5 Packs / 40 Sprites):</h3>

<ol>
  <li><strong>Mystic Potions &amp; Alchemy Elixirs (8 Sprites)</strong>: Healing Potion, Mana Elixir, Stamina Vitality, Poison Flask, Fire Blast Concoction, Frost Shield, Golden Ambrosia, Holy Water.</li>
<br>
  <li><strong>Treasure &amp; Dungeon Loot (8 Sprites)</strong>: Reinforced Wooden Chest, Royal Gold Chest, Sinister Mimic, Gold Coins Pile, Skeleton Key, Runic Key, Sealed Scroll, Golden Grail.</li>
<br>
  <li><strong>RPG Status &amp; Buff Icons (8 Sprites)</strong>: Holy Shield Aura, Flaming Berserk, Speed Haste, Lightning Charge, Poison Debuff, Bleed Damage, Frozen Ice Trap, Silence Curse.</li>
<br>
  <li><strong>Fire Magic &amp; Spells (8 Sprites)</strong>: Pyro Fireball, Fire Tornado, Meteor Strike, Flaming Greatsword, Flame Guard Shield, Phoenix Wings, Inferno Burst, Pyro Core.</li>
<br>
  <li><strong>Core Starter Essentials (8 Sprites)</strong>: Fantasy Broadsword, Tower Shield, Iron Helmet, Red Health Potion, Blue Mana Vial, Wooden Chest, Gold Coin, Magic Scroll.</li>
</ol>

<p><br></p>
<hr>
<p><br></p>

<h3>🎮 Check Out Our Official itch.io Store:</h3>
<p>Browse our entire catalog of game audio &amp; assets on itch.io:</p>
<p>👉 <strong><a href="https://gameverse-audio.itch.io" target="_blank">Visit GameVerse Audio on itch.io</a></strong></p>"""

print("1. Gumroad 無料版商品説明文を最新版に更新中...")
cmd = [GUMROAD_BIN, "products", "update", PID, "--description", new_desc_html, "--currency", "usd", "--price", "0", "--yes"]
res = subprocess.run(cmd, env=env, text=True, capture_output=True)
print("  Description update result:", res.stdout.strip())
