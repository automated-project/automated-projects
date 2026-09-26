#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
rebuild_and_deploy_free_multi_res.py
無料ゲームアセット5パック（計40素材）のマルチ解像度（32px〜512px + 1024px）自動生成、
ZIP再ビルド、および itch.io & Gumroad への一括デプロイ
"""

import os
import sys
import zipfile
import subprocess
from pathlib import Path
from PIL import Image

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Assets")
MUSIC_DIR = Path("/Users/base/Automated-Projects/Game-Music")
OUTPUTS_DIR = BASE_DIR / "outputs"

BUTLER_BIN = str(MUSIC_DIR / "bin" / "butler")
GUMROAD_BIN = str(MUSIC_DIR / "bin" / "gumroad")

# 認証トークンの読み込み
env = os.environ.copy()
env_path = MUSIC_DIR / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k] = v.strip("\"'")

SIZES = [
    (32, 32, "32x32"),
    (64, 64, "64x64"),
    (128, 128, "128x128"),
    (256, 256, "256x256"),
    (512, 512, "512x512"),
]

PACKS = [
    {
        "folder": OUTPUTS_DIR / "Free_Mystic_Potions",
        "trans_src": OUTPUTS_DIR / "Free_Mystic_Potions" / "Transparent_Icons",
        "orig_dir": OUTPUTS_DIR / "Free_Mystic_Potions" / "Original_Art",
        "zip_name": "Free_2D_Game_Assets_Mystic_Potions.zip",
        "channel": "mystic-potions",
        "title": "Mystic Potions & Alchemy Elixirs"
    },
    {
        "folder": OUTPUTS_DIR / "Free_Treasure_Loot",
        "trans_src": OUTPUTS_DIR / "Free_Treasure_Loot" / "Transparent_Icons",
        "orig_dir": OUTPUTS_DIR / "Free_Treasure_Loot" / "Original_Art",
        "zip_name": "Free_2D_Game_Assets_Treasure_Loot.zip",
        "channel": "treasure-loot",
        "title": "Treasure & Dungeon Loot"
    },
    {
        "folder": OUTPUTS_DIR / "Free_Status_Buffs",
        "trans_src": OUTPUTS_DIR / "Free_Status_Buffs" / "Transparent_Icons",
        "orig_dir": OUTPUTS_DIR / "Free_Status_Buffs" / "Original_Art",
        "zip_name": "Free_2D_Game_Assets_Status_Buffs.zip",
        "channel": "status-buffs",
        "title": "RPG Status & Buff Icons"
    },
    {
        "folder": OUTPUTS_DIR / "Free_Starter_Pack_Selected",
        "trans_src": OUTPUTS_DIR / "Free_Starter_Pack_Selected" / "Transparent_Icons_512px",
        "orig_dir": OUTPUTS_DIR / "Free_Starter_Pack_Selected" / "Original_Art",
        "zip_name": "Free_2D_Game_Asset_Starter_Pack.zip",
        "channel": "free-starter-pack",
        "title": "Core Starter Essentials"
    },
    {
        "folder": OUTPUTS_DIR / "Pack01_Fire_Magic_Spells_20260911_160322",
        "trans_src": OUTPUTS_DIR / "Pack01_Fire_Magic_Spells_20260911_160322" / "Transparent_Icons_512px",
        "orig_dir": OUTPUTS_DIR / "Pack01_Fire_Magic_Spells_20260911_160322" / "Original_Art",
        "zip_name": "Pack01_Fire_Magic_Spells_Complete_Pack.zip",
        "channel": "pack01-fire-magic-spells",
        "title": "Fire Magic & Spells"
    }
]

README_TEMPLATE = """============================================================
GameVerse Audio - [FREE] 2D Game Asset Pack
Title: {title}
============================================================

Thank you for downloading this free studio-grade 2D game asset pack!

📦 FOLDER STRUCTURE & RESOLUTIONS:
------------------------------------------------------------
This pack includes 5 game-ready resolutions + master artwork:

📁 Transparent_Icons/
   ├── 32x32/   -> Ideal for dense Inventory Grids & Action Hotbars
   ├── 64x64/   -> Standard RPG Inventory, Skill Trees & Crafting UI
   ├── 128x128/ -> Item Inspection Popups, Tooltips & Loot Drops
   ├── 256x256/ -> Shop Merchant UI, Equipment Dialogs & Menus
   └── 512x512/ -> High-Definition Hero Displays & Cutscenes

📁 Original_Art/ (1024x1024)
   Full high-resolution master artwork with authentic backgrounds.
   Perfect for Card Battlers, Gacha Banners, and Concept Promos.

✨ TECHNICAL SPECIFICATIONS:
------------------------------------------------------------
- Format: PNG with 100% clean Alpha Transparency (zero edge halos)
- Color Space: sRGB
- Engine Compatibility: Drag & Drop ready for Unity, Godot 4, 
  Unreal Engine 5, RPG Maker MZ/MV, GameMaker & Web Canvas.

📜 COMMERCIAL LICENSE:
------------------------------------------------------------
- 100% Royalty-Free & Commercial Use permitted.
- Cleared for PC/Steam, Console, iOS, Android, and Web Games.
- No attribution required (credit to GameVerse Audio is appreciated).
- Resale or redistribution as raw standalone asset packs is prohibited.

👑 WANT ALL 10 EXPANDED GENRE PACKS (80+ SPRITES)?
------------------------------------------------------------
Unlock Weapons, Mythic Armor, Sci-Fi HUD, Crystals, Spellbooks,
Monsters, Survival Food, Ores, Jewelry & Dark Magic!
👉 https://gameverse-audio.itch.io/game-asset-vault

Designed with passion by GameVerse Audio.
============================================================
"""

def process_pack(p):
    folder = p["folder"]
    print(f"\n🚀 Processing {p['title']}...")

    src_dir = p["trans_src"]
    orig_dir = p["orig_dir"]
    
    # ソースPNG収集
    source_pngs = sorted([f for f in src_dir.iterdir() if f.is_file() and f.suffix.lower() == ".png"])
    if not source_pngs and (folder / "Transparent_Icons" / "512x512").exists():
        source_pngs = sorted([f for f in (folder / "Transparent_Icons" / "512x512").iterdir() if f.is_file() and f.suffix.lower() == ".png"])

    if not source_pngs:
        print(f"  ❌ ソースPNGが見つかりません: {src_dir}")
        return None

    print(f"  📸 Found {len(source_pngs)} source sprites.")

    target_base = folder / "Transparent_Icons"
    target_base.mkdir(parents=True, exist_ok=True)

    for w, h, size_name in SIZES:
        size_dir = target_base / size_name
        size_dir.mkdir(parents=True, exist_ok=True)

        for src in source_pngs:
            stem = src.stem
            for _, _, s_name in SIZES:
                if stem.endswith(f"_{s_name}"):
                    stem = stem[:-len(f"_{s_name}")]
            if stem.endswith("_512px"):
                stem = stem[:-6]
            if stem.endswith("_icon"):
                pass

            dst_name = f"{stem}_{size_name}.png"
            dst_path = size_dir / dst_name

            with Image.open(src) as img:
                img_resized = img.resize((w, h), Image.Resampling.LANCZOS)
                img_resized.save(dst_path, format="PNG", optimize=True)

    print(f"  ✅ All {len(SIZES)} resolutions generated.")

    # README & LICENSE
    readme_path = folder / "README.txt"
    readme_path.write_text(README_TEMPLATE.format(title=p["title"]), encoding="utf-8")
    
    license_path = folder / "LICENSE.txt"
    if not license_path.exists():
        license_path.write_text("""100% Royalty-Free Commercial License
GameVerse Audio permits unlimited personal and commercial use in indie games, mobile apps, and videos.
No attribution required. Standalone resale of raw asset files is prohibited.
""", encoding="utf-8")

    # ZIP 再ビルド
    zip_path = folder / p["zip_name"]
    print(f"  📦 Rebuilding ZIP: {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(license_path, arcname="LICENSE.txt")
        zf.write(readme_path, arcname="README.txt")
        preview = folder / "showcase_preview.png"
        if preview.exists():
            zf.write(preview, arcname="showcase_preview.png")

        for w, h, size_name in SIZES:
            s_dir = target_base / size_name
            for f in sorted(s_dir.glob("*.png")):
                zf.write(f, arcname=f"Transparent_Icons/{size_name}/{f.name}")

        if orig_dir.exists():
            for f in sorted(orig_dir.glob("*.png")):
                zf.write(f, arcname=f"Original_Art/{f.name}")

    mb_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"  🎉 Completed: {zip_path.name} ({mb_size:.2f} MB)")
    return zip_path

def main():
    print("============================================================")
    print("🎁 GameVerse Audio - Free Packs Multi-Resolution Batch System")
    print("Resolutions: 32x32, 64x64, 128x128, 256x256, 512x512 (+ 1024px Art)")
    print("============================================================")

    rebuilt_zips = []
    for p in PACKS:
        z = process_pack(p)
        if z:
            rebuilt_zips.append((p, z))

    print("\n" + "=" * 60)
    print(f"✨ 全5パック中 {len(rebuilt_zips)} パックのマルチ解像度ZIP再ビルド完了")
    print("=" * 60)

    # 1. itch.io へのデプロイ
    print("\n🚀 [1/2] itch.io (free-game-assets) への Butler プッシュ開始...")
    for p, z in rebuilt_zips:
        target = f"gameverse-audio/free-game-assets:{p['channel']}"
        res = subprocess.run([BUTLER_BIN, "push", str(z), target], env=env, text=True, capture_output=True)
        if res.returncode == 0:
            print(f"  ✅ itch.io ({p['channel']}): Success")
        else:
            print(f"  ❌ itch.io ({p['channel']}): Failed ({res.stderr.strip()})")

    # 2. Gumroad へのデプロイ
    print("\n🚀 [2/2] Gumroad (free-game-assets) へのデプロイ開始...")
    gumroad_cmd = [
        GUMROAD_BIN, "products", "update", "ozQ4-e20_gROzj378uBJrA==",
        "--currency", "usd",
        "--price", "0",
        "--yes"
    ]
    for p, z in rebuilt_zips:
        gumroad_cmd.extend(["--file", str(z)])

    res_gum = subprocess.run(gumroad_cmd, env=env, text=True, capture_output=True)
    if res_gum.returncode == 0:
        print("  ✅ Gumroad: Success")
        print(res_gum.stdout.strip())
    else:
        print("  ❌ Gumroad: Failed")
        print(res_gum.stderr.strip())

    print("\n🎉 全ての無料版マルチ解像度デプロイが完了しました！")

if __name__ == "__main__":
    main()
