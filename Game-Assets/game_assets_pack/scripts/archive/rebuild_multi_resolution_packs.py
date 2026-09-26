#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
rebuild_multi_resolution_packs.py
ゲーム開発者向けマルチ解像度（32x32, 64x64, 128x128, 256x256, 512x512, 1024x1024）自動生成＆ZIP再ビルド
"""

import os
import sys
import zipfile
from pathlib import Path
from PIL import Image

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Assets")
VAULT_DIR = BASE_DIR / "outputs" / "Paid_Vault_10Packs"

SIZES = [
    (32, 32, "32x32"),
    (64, 64, "64x64"),
    (128, 128, "128x128"),
    (256, 256, "256x256"),
    (512, 512, "512x512"),
]

PACKS = [
    {"folder": "01_Fantasy_Weapons", "zip": "01_Fantasy_Weapons_Pack.zip", "title": "Fantasy Weapons"},
    {"folder": "02_Mythic_Armor_Helmets", "zip": "02_Mythic_Armor_Helmets_Pack.zip", "title": "Mythic Armor & Helmets"},
    {"folder": "03_Cyberpunk_SciFi_HUD_UI", "zip": "03_Cyberpunk_SciFi_HUD_UI_Pack.zip", "title": "Cyberpunk & Sci-Fi HUD UI"},
    {"folder": "04_Gemstones_Crystals", "zip": "04_Gemstones_Crystals_Pack.zip", "title": "Gemstones & Crystals"},
    {"folder": "05_Spellbooks_Tomes", "zip": "05_Spellbooks_Tomes_Pack.zip", "title": "Spellbooks & Ancient Tomes"},
    {"folder": "06_Monster_Creature_Avatars", "zip": "06_Monster_Creature_Avatars_Pack.zip", "title": "Monster & Creature Avatars"},
    {"folder": "07_Survival_Food_Cooking", "zip": "07_Survival_Food_Cooking_Pack.zip", "title": "Survival Food & Cooking"},
    {"folder": "08_Crafting_Materials_Ores", "zip": "08_Crafting_Materials_Ores_Pack.zip", "title": "Crafting Materials & Ores"},
    {"folder": "09_Rings_Amulets_Jewelry", "zip": "09_Rings_Amulets_Jewelry_Pack.zip", "title": "Rings, Amulets & Jewelry"},
    {"folder": "10_Dark_Magic_Necromancy", "zip": "10_Dark_Magic_Necromancy_Pack.zip", "title": "Dark Magic & Necromancy"},
]

README_TEMPLATE = """============================================================
GameVerse Audio - 2D Game Asset Pack
Title: {title}
============================================================

Thank you for downloading this studio-grade 2D game asset pack!

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

Designed with passion by GameVerse Audio.
Store: https://gameverse-audio.itch.io
============================================================
"""

def process_pack(p_info):
    folder = VAULT_DIR / p_info["folder"]
    print(f"\n🚀 Processing {p_info['title']} ({folder.name})...")

    trans_base = folder / "Transparent_Icons"
    orig_dir = folder / "Original_Art"
    
    # 既存の直下PNG（ファイルのみ）をソースとして収集
    source_pngs = sorted([f for f in trans_base.iterdir() if f.is_file() and f.suffix.lower() == ".png"])
    
    # すでに 512x512/ がある場合（Pack 01等）のフォールバック
    if not source_pngs and (trans_base / "512x512").exists():
        source_pngs = sorted([f for f in (trans_base / "512x512").iterdir() if f.is_file() and f.suffix.lower() == ".png"])
    
    if not source_pngs:
        print(f"  ❌ ソースPNGが見つかりません: {trans_base}")
        return False

    print(f"  📸 Found {len(source_pngs)} source sprites.")

    # サイズ別フォルダ作成＆リサイズ
    for w, h, size_name in SIZES:
        target_dir = trans_base / size_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for src_path in source_pngs:
            stem = src_path.stem
            # 末尾のサイズサフィックスがあれば除去
            for _, _, s_name in SIZES:
                if stem.endswith(f"_{s_name}"):
                    stem = stem[:-len(f"_{s_name}")]
            if stem.endswith("_512px"):
                stem = stem[:-6]
            
            dst_name = f"{stem}_{size_name}.png"
            dst_path = target_dir / dst_name
            
            with Image.open(src_path) as img:
                img_resized = img.resize((w, h), Image.Resampling.LANCZOS)
                img_resized.save(dst_path, format="PNG", optimize=True)

    print(f"  ✅ All {len(SIZES)} resolutions generated.")

    # 直下の古い *.png を整理（フォルダ外にあるもののみ削除）
    for old_f in list(trans_base.iterdir()):
        if old_f.is_file() and old_f.suffix.lower() == ".png":
            old_f.unlink()

    # README.txt 更新
    readme_path = folder / "README.txt"
    readme_path.write_text(README_TEMPLATE.format(title=p_info["title"]), encoding="utf-8")

    # ZIP 再ビルド
    zip_path = folder / p_info["zip"]
    print(f"  📦 Rebuilding ZIP: {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(folder / "LICENSE.txt", arcname="LICENSE.txt")
        zf.write(folder / "README.txt", arcname="README.txt")
        if (folder / "showcase_preview.png").exists():
            zf.write(folder / "showcase_preview.png", arcname="showcase_preview.png")
        
        # Transparent_Icons 各解像度
        for w, h, size_name in SIZES:
            s_dir = trans_base / size_name
            for f in sorted(s_dir.glob("*.png")):
                zf.write(f, arcname=f"Transparent_Icons/{size_name}/{f.name}")
        
        # Original_Art (1024px)
        if orig_dir.exists():
            for f in sorted(orig_dir.glob("*.png")):
                zf.write(f, arcname=f"Original_Art/{f.name}")

    mb_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"  🎉 Completed: {zip_path.name} ({mb_size:.2f} MB)")
    return True

def main():
    print("============================================================")
    print("🎮 GameVerse Audio - Multi-Resolution Asset Batch Generator")
    print("Resolutions: 32x32, 64x64, 128x128, 256x256, 512x512 (+ 1024px Art)")
    print("============================================================")

    success_count = 0
    for p in PACKS:
        if process_pack(p):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"✨ 全10パック中 {success_count} パックのマルチ解像度ZIP再ビルドが完了しました！")
    print("=" * 60)

if __name__ == "__main__":
    main()
