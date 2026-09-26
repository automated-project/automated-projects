#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
GUMROAD_BIN = str(BASE_DIR / "bin" / "gumroad")

env = os.environ.copy()
env_path = BASE_DIR / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("GUMROAD_ACCESS_TOKEN="):
                env["GUMROAD_ACCESS_TOKEN"] = line.split("=", 1)[1].strip().strip("\"'")

# 1. 有料アセットVault (c07Os4dAkeUFa2VBAne4YQ==) - 標準HTML（余計な空行なし）
desc_paid_assets = """<p>👑 <strong>The Ultimate 2D Game Asset Vault — 10 Genre Starter Packs (80 Handcrafted Studio Sprites)</strong></p>
<p>Designed specifically for indie game developers. Stop spending hours manually resizing and cleaning messy backgrounds — every sprite in this vault comes pre-scaled into <strong>5 game-ready resolutions + master artwork</strong> with 100% clean alpha transparency.</p>
<hr>
<h3>🎮 Game-Ready Resolutions &amp; Use Cases:</h3>
<p>Ready to drag &amp; drop straight into your game UI:</p>
<ul>
  <li><strong>32x32:</strong> Ideal for dense Inventory Grids, Action Hotbars, and Minimap Icons.</li>
  <li><strong>64x64:</strong> Standard for RPG Inventories, Skill Trees, and Crafting Recipe Slots.</li>
  <li><strong>128x128:</strong> Perfect for Item Inspection Popups, Tooltips, and Loot Drop banners.</li>
  <li><strong>256x256:</strong> Great for Shop Merchant UI, Equipment Dialogs, and Quest Menus.</li>
  <li><strong>512x512:</strong> Ultra-crisp for Hero Equipment Displays, Dialog Cutscenes, and High-DPI screens.</li>
  <li><strong>1024x1024 Master Art:</strong> Full master artwork included for Card Battlers, Gacha Banners, and Promo Art.</li>
</ul>
<hr>
<h3>⚙️ Engine &amp; Platform Compatibility:</h3>
<p><strong>✅ What You CAN Do:</strong></p>
<ul>
  <li><strong>Universal Drag &amp; Drop:</strong> 100% compatible with <strong>Unity, Godot 4, Unreal Engine 5, RPG Maker MZ/MV, GameMaker, Construct 3, and Web Canvas (Phaser / Pixi.js)</strong>.</li>
  <li><strong>Commercial Clearance:</strong> 100% royalty-free for commercial PC/Steam games, mobile apps (iOS/Android), and web games.</li>
  <li><strong>Full Creative Freedom:</strong> Freely crop, tint, recolor, combine, and animate.</li>
  <li><strong>No Mandatory Attribution:</strong> No credit required (though appreciated).</li>
</ul>
<p><strong>❌ What This Pack IS NOT:</strong></p>
<ul>
  <li><strong>NOT 3D Models:</strong> High-quality 2D transparent PNG graphics/textures.</li>
  <li><strong>NOT Animated Sprite Sheets:</strong> Static item/icon sprites.</li>
  <li><strong>NOT Pixel Art:</strong> Detailed, painted illustrated assets.</li>
</ul>
<hr>
<h3>📦 What's Inside the 10 Individual Packs (80 Unique Sprites):</h3>
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
<h3>🎁 Want to Test Quality First? (Try Before You Buy):</h3>
<p>Want to verify our transparent PNGs, resolution scaling, and engine compatibility before buying?<br>
👉 <strong><a href="https://gameverseaudio.gumroad.com/l/free-game-assets">Download our Free 2D Game Asset Mega Starter Pack ($0 / 40 Sprites)</a></strong></p>
<hr>
<h3>🎮 Check Out Our Official itch.io Store:</h3>
<p>Browse our entire catalog of indie game music &amp; assets on itch.io:<br>
👉 <strong><a href="https://gameverse-audio.itch.io" target="_blank">Visit GameVerse Audio on itch.io</a></strong></p>"""

print("1. Updating Gumroad Paid Asset Vault (c07Os4dAkeUFa2VBAne4YQ==)...")
r1 = subprocess.run([GUMROAD_BIN, "products", "update", "c07Os4dAkeUFa2VBAne4YQ==", "--description", desc_paid_assets, "--currency", "usd", "--price", "0.99", "--yes"], env=env, capture_output=True, text=True)
print("  Result:", r1.stdout.strip())

# 2. 無料アセットパック (ozQ4-e20_gROzj378uBJrA==) - 標準HTML
desc_free_assets = """<p>🎁 <strong>[FREE] 2D Game Asset Mega Starter Pack — 5 Complete Packs (40 Handcrafted Studio Sprites)</strong></p>
<p>Kickstart your indie game project with our massive, studio-grade starter collection. No more wasting time manually resizing or cleaning jagged edges — every sprite comes pre-scaled into <strong>5 game-ready resolutions + full 1024px master art</strong> with 100% clean alpha transparency.</p>
<hr>
<h3>👑 WANT ALL 10 EXPANDED GENRE PACKS (80 UNIQUE SPRITES)?</h3>
<p>Upgrade to <strong><a href="https://gameverseaudio.gumroad.com/l/game-asset-vault">The Ultimate 2D Game Asset Vault (99¢)</a></strong> to unlock the complete studio library: Weapons, Mythic Armor, Sci-Fi HUD UI, Gemstones, Spellbooks, Monster Avatars, Food, Ores, Jewelry &amp; Dark Magic!</p>
<p>👉 <strong><a href="https://gameverseaudio.gumroad.com/l/game-asset-vault">Unlock The Complete 10-Pack Vault for just 99¢!</a></strong></p>
<hr>
<h3>🎮 Game-Ready Resolutions &amp; Use Cases:</h3>
<p>Ready to drag &amp; drop straight into your game UI:</p>
<ul>
  <li><strong>32x32:</strong> Ideal for dense Inventory Grids, Action Hotbars, and Minimap Icons.</li>
  <li><strong>64x64:</strong> Standard for RPG Inventories, Skill Trees, and Crafting Recipe Slots.</li>
  <li><strong>128x128:</strong> Perfect for Item Inspection Popups, Tooltips, and Loot Drop banners.</li>
  <li><strong>256x256:</strong> Great for Shop Merchant UI, Equipment Dialogs, and Quest Menus.</li>
  <li><strong>512x512:</strong> Ultra-crisp for Hero Equipment Displays, Dialog Cutscenes, and High-DPI screens.</li>
  <li><strong>1024x1024 Master Art:</strong> Full master artwork included for Card Battlers, Gacha Banners, and Promo Art.</li>
</ul>
<hr>
<h3>⚙️ Engine &amp; Platform Compatibility:</h3>
<p><strong>✅ What You CAN Do:</strong></p>
<ul>
  <li><strong>Universal Drag &amp; Drop:</strong> 100% compatible with <strong>Unity, Godot 4, Unreal Engine 5, RPG Maker MZ/MV, GameMaker, Construct 3, and Web Canvas (Phaser / Pixi.js)</strong>.</li>
  <li><strong>Commercial Clearance:</strong> 100% royalty-free for commercial PC/Steam games, mobile apps (iOS/Android), and web games.</li>
  <li><strong>Full Creative Freedom:</strong> Freely crop, tint, recolor, combine, and animate.</li>
  <li><strong>No Mandatory Attribution:</strong> No credit required (though appreciated).</li>
</ul>
<p><strong>❌ What This Pack IS NOT:</strong></p>
<ul>
  <li><strong>NOT 3D Models:</strong> High-quality 2D transparent PNG graphics/textures.</li>
  <li><strong>NOT Animated Sprite Sheets:</strong> Static item/icon sprites.</li>
  <li><strong>NOT Pixel Art:</strong> Detailed, painted illustrated assets.</li>
</ul>
<hr>
<h3>📦 What's Inside This Free Download (5 Packs / 40 Sprites):</h3>
<ol>
  <li><strong>Mystic Potions &amp; Alchemy Elixirs (8 Sprites)</strong>: Healing Potion, Mana Elixir, Stamina Vitality, Poison Flask, Fire Blast Concoction, Frost Shield, Golden Ambrosia, Holy Water.</li>
  <li><strong>Treasure &amp; Dungeon Loot (8 Sprites)</strong>: Reinforced Wooden Chest, Royal Gold Chest, Sinister Mimic, Gold Coins Pile, Skeleton Key, Runic Key, Sealed Scroll, Golden Grail.</li>
  <li><strong>RPG Status &amp; Buff Icons (8 Sprites)</strong>: Holy Shield Aura, Flaming Berserk, Speed Haste, Lightning Charge, Poison Debuff, Bleed Damage, Frozen Ice Trap, Silence Curse.</li>
  <li><strong>Fire Magic &amp; Spells (8 Sprites)</strong>: Pyro Fireball, Fire Tornado, Meteor Strike, Flaming Greatsword, Flame Guard Shield, Phoenix Wings, Inferno Burst, Pyro Core.</li>
  <li><strong>Core Starter Essentials (8 Sprites)</strong>: Fantasy Broadsword, Tower Shield, Iron Helmet, Red Health Potion, Blue Mana Vial, Wooden Chest, Gold Coin, Magic Scroll.</li>
</ol>
<hr>
<h3>🎮 Check Out Our Official itch.io Store:</h3>
<p>Browse our entire catalog of game audio &amp; assets on itch.io:<br>
👉 <strong><a href="https://gameverse-audio.itch.io" target="_blank">Visit GameVerse Audio on itch.io</a></strong></p>"""

print("2. Updating Gumroad Free Assets (ozQ4-e20_gROzj378uBJrA==)...")
r2 = subprocess.run([GUMROAD_BIN, "products", "update", "ozQ4-e20_gROzj378uBJrA==", "--description", desc_free_assets, "--currency", "usd", "--price", "0", "--yes"], env=env, capture_output=True, text=True)
print("  Result:", r2.stdout.strip())

# 3. 有料音楽特化パック (A6uhIWQK6_nkuWy74xOKYQ==) - 標準HTML
desc_music_pack = """<h3>⚔️ Epic Dark Fantasy &amp; Gothic Boss Battle Music Pack (20 Studio Tracks)</h3>
<p>An imposing, cinematic collection of <strong>20 complete dark fantasy and gothic orchestral battle tracks</strong> produced by GameVerse Audio. Specifically engineered for indie game developers (Souls-like, dark RPG, grimdark action, D&amp;D campaigns) and cinematic content creators.</p>
<p><em>🔒 100% Paid Exclusive Content — Zero overlap with our free promotional samplers.</em></p>
<hr>
<h4>🎧 Complete Tracklist (20 Studio Master Tracks):</h4>
<ol>
  <li><strong>God of Ruin</strong> — Epic Dark Fantasy Colossal Boss Battle</li>
  <li><strong>The Iron Ticking</strong> — Sinister Clockwork Industrial Evil Theme</li>
  <li><strong>Summa Dies Advenit</strong> — Apocalyptic Latin Choral Boss Theme</li>
  <li><strong>Beneath the Weeping Boughs</strong> — Atmospheric Dark Fantasy Combat</li>
  <li><strong>Crown of Iron</strong> — Brutal Industrial Dark Fantasy Combat</li>
  <li><strong>Crown of Cinders</strong> — Modern Gothic Symphony Boss Battle</li>
  <li><strong>Crown of Bleeding Iron</strong> — Epic Gothic Orchestral Boss Battle</li>
  <li><strong>Bloodline of the Eclipse</strong> — Epic Gothic Orchestral Boss Battle</li>
  <li><strong>Hammer of the Fallen</strong> — Dark Fantasy Epic Titan Battle</li>
  <li><strong>Hammer of the Stone King</strong> — Gothic Orchestral Titan Battle</li>
  <li><strong>Steps of a Forgotten God</strong> — Dark Fantasy Orchestral Boss Battle</li>
  <li><strong>The Titan's Heavy March</strong> — Epic Dark Fantasy Colossal Theme</li>
  <li><strong>Iron Kneeling in the Dark</strong> — Cinematic Dark Fantasy Combat</li>
  <li><strong>Hammer Against the Gate</strong> — Dark Industrial Titan Battle</li>
  <li><strong>Cold Iron March</strong> — Cinematic Dark Fantasy Battle</li>
  <li><strong>The Sovereign's Last Breath</strong> — Cinematic Orchestral Dark Fantasy</li>
  <li><strong>Throne of Ash</strong> — Epic Orchestral Dark Fantasy Battle</li>
  <li><strong>The Weight of Iron</strong> — Cinematic Dark Fantasy Boss Theme</li>
  <li><strong>Steps of the Frost Titan</strong> — Orchestral Dark Fantasy Titan Battle</li>
  <li><strong>The Last Siege of Kings</strong> — Modern Gothic Symphony Boss Battle</li>
</ol>
<hr>
<h4>💎 Commercial License &amp; Engine Compatibility:</h4>
<ul>
  <li><strong>100% Royalty-Free &amp; Commercial Use:</strong> Deploy in commercial Steam games, console releases, Kickstarter projects, YouTube videos, and Twitch streams. No copyright strikes, ever.</li>
  <li><strong>Game Engine Ready:</strong> Drag-and-drop ready for Unity, Unreal Engine 5, Godot 4, RPG Maker, and GameMaker Studio.</li>
  <li><strong>Lossless Master Quality:</strong> Pristine 24-bit / 44.1kHz audio with full dynamic range, tailored for high-stakes boss battles and atmospheric dungeon exploration.</li>
  <li><strong>No Mandatory Attribution:</strong> No credit required (though appreciated).</li>
</ul>
<hr>
<h4>🎁 Want to Test Studio Quality First? (Try Before You Buy):</h4>
<p>Want to check our mix quality, lossless master files, and seamless game loops before purchasing?<br>
👉 <strong><a href="https://gameverseaudio.gumroad.com/l/free-sample-pack">Download Free Game Music Starter Pack ($0)</a></strong></p>
<hr>
<h4>🎮 Check Out Our Official itch.io Store:</h4>
<p>Browse our entire catalog of game audio &amp; assets on itch.io:<br>
👉 <strong><a href="https://gameverse-audio.itch.io" target="_blank">Visit GameVerse Audio on itch.io</a></strong></p>"""

print("3. Updating Gumroad Music Pack (A6uhIWQK6_nkuWy74xOKYQ==)...")
r3 = subprocess.run([GUMROAD_BIN, "products", "update", "A6uhIWQK6_nkuWy74xOKYQ==", "--description", desc_music_pack, "--currency", "usd", "--price", "4.99", "--yes"], env=env, capture_output=True, text=True)
print("  Result:", r3.stdout.strip())
print("\n🎉 Gumroad 全商品の余計な余白（空行）を排除し、自然な標準レイアウトに更新完了しました！")
