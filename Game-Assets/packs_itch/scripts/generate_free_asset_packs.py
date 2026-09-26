#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_free_asset_packs.py: 無料ゲームアセット3パック自動生成スクリプト
- ユーザー指定ルール: 「pack1とか数字は書かない」
- 3パック構成 (各8枚 = 計24枚):
  1. Mystic Potions & Elixirs (ポーション・薬品)
  2. Treasure & Dungeon Loot (宝箱・戦利品)
  3. RPG Status & Buff Icons (バフ・状態異常)
- 各パックに 512px透過PNG, 原画, プレビューコラージュ, LICENSE.txt, README.txt を同封してZIP化
"""

import os
import sys
import time
import json
import base64
import zipfile
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Assets")
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

ENV_PATH = Path("/Users/base/Automated-Projects/YouTube/.env")

def load_api_key():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("ACCOUNT_1_GEMINI_API_KEY")
    if not api_key and ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ACCOUNT_1_GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break
    return api_key

def make_transparent_luma(img, low_thresh=18, high_thresh=55):
    rgba = img.convert("RGBA")
    data = np.array(rgba, dtype=np.float32)

    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    max_val = np.maximum(np.maximum(r, g), b)
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    key_metric = 0.7 * max_val + 0.3 * luma

    alpha = np.zeros_like(key_metric)
    mask_opaque = key_metric >= high_thresh
    mask_trans = key_metric <= low_thresh
    mask_inter = (~mask_opaque) & (~mask_trans)

    alpha[mask_opaque] = 255.0
    alpha[mask_trans] = 0.0

    t = (key_metric[mask_inter] - low_thresh) / (high_thresh - low_thresh)
    alpha[mask_inter] = (3 * t**2 - 2 * t**3) * 255.0

    alpha_norm = np.clip(alpha / 255.0, 0.001, 1.0)
    for c in range(3):
        boosted = data[:, :, c] / alpha_norm
        data[:, :, c] = np.clip(boosted, 0, 255)

    data[:, :, 3] = np.clip(alpha, 0, 255)
    return Image.fromarray(data.astype(np.uint8), "RGBA")

def generate_single_image(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }
    resp = requests.post(url, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"API Error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    b64_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    return base64.b64decode(b64_data)

PACK_DEFINITIONS = [
    {
        "folder_name": "Free_Mystic_Potions",
        "zip_name": "Free_2D_Game_Assets_Mystic_Potions.zip",
        "title": "Mystic Potions & Alchemy Elixirs",
        "category_title": "MYSTIC POTIONS & ELIXIRS",
        "items": [
            {
                "slug": "healing_potion_flask",
                "name": "Health Restoration Potion",
                "desc": "an ornate glass flask containing glowing ruby-red healing elixir with gentle magical bubbles and a carved brass cork"
            },
            {
                "slug": "mana_elixir_vial",
                "name": "Mana Restoration Elixir",
                "desc": "a tall crystal vial containing radiant sapphire-blue mana liquid with subtle starry glitter and an ornate silver stopper"
            },
            {
                "slug": "poison_flask",
                "name": "Toxic Venom Flask",
                "desc": "a triangular glass alchemy beaker filled with bubbling emerald-green toxic venom emitting faint acidic fumes"
            },
            {
                "slug": "golden_ambrosia",
                "name": "Golden Ambrosia Elixir",
                "desc": "a spherical ornate gold-rimmed flask filled with radiant liquid sunshine golden immortality elixir"
            },
            {
                "slug": "frost_shield_elixir",
                "name": "Frost Shield Elixir",
                "desc": "a crystalline hexagonal glass vial containing shimmering icy frost essence with floating snowflakes"
            },
            {
                "slug": "fire_blast_concoction",
                "name": "Fire Blast Concoction",
                "desc": "a round heavy ceramic bottle with glowing fiery orange explosive liquid and carved flame runes"
            },
            {
                "slug": "stamina_vitality_draught",
                "name": "Stamina Vitality Draught",
                "desc": "a cylindrical glass bottle with glowing bright amber vitality potion and leather cord wrap"
            },
            {
                "slug": "purification_holy_water",
                "name": "Purification Holy Water",
                "desc": "an elegant winged silver-capped ornate vial with pure luminous white holy water casting a sacred glow"
            }
        ]
    },
    {
        "folder_name": "Free_Treasure_Loot",
        "zip_name": "Free_2D_Game_Assets_Treasure_Loot.zip",
        "title": "Treasure & Dungeon Loot",
        "category_title": "TREASURE & DUNGEON LOOT",
        "items": [
            {
                "slug": "wooden_dungeon_chest",
                "name": "Reinforced Dungeon Chest",
                "desc": "a sturdy wooden dungeon treasure chest with iron reinforcements, corner brackets, and a heavy iron padlock"
            },
            {
                "slug": "royal_gold_chest",
                "name": "Royal Gold Treasure Chest",
                "desc": "an ornate royal golden treasure chest overflowing with sparkling red rubies, sapphires, and polished diamonds"
            },
            {
                "slug": "sinister_mimic_chest",
                "name": "Sinister Mimic Monster",
                "desc": "a wooden treasure chest revealing jagged monstrous teeth and a long purple tongue in a menacing grin"
            },
            {
                "slug": "gold_coins_pile",
                "name": "Overflowing Gold Coins",
                "desc": "a sparkling overflowing pile of ancient embossed gold and silver fantasy coins with radiant metallic highlights"
            },
            {
                "slug": "skeleton_dungeon_key",
                "name": "Antique Skeleton Key",
                "desc": "an intricate antique iron dungeon skeleton key with an ornate skull-shaped bow and engraved notches"
            },
            {
                "slug": "runic_crystal_key",
                "name": "Runic Crystal Key",
                "desc": "a mystical glowing cyan crystal dungeon key carved with ancient glowing magical runes"
            },
            {
                "slug": "ancient_spell_scroll",
                "name": "Ancient Sealed Spell Scroll",
                "desc": "a rolled ancient parchment magic spell scroll tied with a gold ribbon and an intact red wax seal"
            },
            {
                "slug": "sacred_golden_grail",
                "name": "Sacred Golden Grail Relic",
                "desc": "an ornate medieval golden chalice goblet encrusted with precious emerald gems casting divine light"
            }
        ]
    },
    {
        "folder_name": "Free_Status_Buffs",
        "zip_name": "Free_2D_Game_Assets_Status_Buffs.zip",
        "title": "RPG Status & Buff Icons",
        "category_title": "RPG STATUS & BUFF ICONS",
        "items": [
            {
                "slug": "poison_skull_debuff",
                "name": "Poison Condition",
                "desc": "a stylized graphic dripping toxic green skull symbol with venom vapors, bold RPG status icon"
            },
            {
                "slug": "burn_flame_debuff",
                "name": "Burn Condition",
                "desc": "a stylized graphic blazing crimson and orange flame fire hazard symbol, bold RPG status icon"
            },
            {
                "slug": "freeze_ice_debuff",
                "name": "Freeze Condition",
                "desc": "a stylized graphic sharp crystalline blue snowflake ice frost symbol, bold RPG status icon"
            },
            {
                "slug": "shock_lightning_debuff",
                "name": "Shock Condition",
                "desc": "a stylized graphic jagged crackling electric purple lightning bolt spark symbol, bold RPG status icon"
            },
            {
                "slug": "attack_power_buff",
                "name": "Attack Power Buff",
                "desc": "two glowing crossed steel broadswords surrounded by a radiant golden combat aura, bold RPG status icon"
            },
            {
                "slug": "defense_shield_buff",
                "name": "Defense Shield Buff",
                "desc": "a solid glowing knight tower shield with a radiant blue protective barrier aura, bold RPG status icon"
            },
            {
                "slug": "bleed_droplet_debuff",
                "name": "Bleed Condition",
                "desc": "three stylized glistening deep-red blood droplets splashing downward, bold RPG status icon"
            },
            {
                "slug": "stun_dizzy_stars",
                "name": "Stun Condition",
                "desc": "three stylized spinning glowing yellow cartoon stars indicating dizziness and stun, bold RPG status icon"
            }
        ]
    }
]

LICENSE_TEXT = """================================================================================
FREE GAME ASSET LICENSE & TERMS OF USE
================================================================================

Thank you for downloading this free game asset pack!

--------------------------------------------------------------------------------
【PERMITTED USES】
--------------------------------------------------------------------------------
1. Commercial & Non-Commercial Projects
   - You can freely use these assets in any commercial, indie, game jam, or free games.
   
2. Supported Platforms
   - Steam, itch.io, App Store (iOS), Google Play (Android), Nintendo Switch, PlayStation, Xbox, Web, etc.

3. Engine Compatibility
   - Fully compatible with Unity, Godot, Unreal Engine, GameMaker, RPG Maker, and custom engines.

4. Modifications Allowed
   - You may resize, crop, recolor, add visual effects, or combine these assets with other artwork.

5. Credit is Optional
   - Attribution/credit is appreciated but NOT required. You are 100% free to use these assets without crediting.

--------------------------------------------------------------------------------
【PROHIBITED USES】
--------------------------------------------------------------------------------
1. No Standalone Redistribution or Resale
   - You cannot resell, redistribute, sub-license, or share these raw asset files as standalone stock.
   
2. No NFT / Blockchain Usage
   - You cannot use these assets for NFT minting or blockchain-based tokens.

================================================================================
"""

README_TEXT = """================================================================================
FREE GAME ASSETS — QUICK START GUIDE
================================================================================

Included in this package:
- Transparent_Icons/ : 512x512 crisp PNG icons with clean transparent alpha background (drag-and-drop ready)
- Original_Art/      : High-resolution concept art files
- showcase_preview.png: Complete collection overview sheet
- LICENSE.txt        : Perpetual royalty-free commercial license

--------------------------------------------------------------------------------
👑 LOOKING FOR MORE GAME ASSETS & SOUNDTRACKS?
--------------------------------------------------------------------------------
Need weapons, armor, inventory items, and full orchestral/synthwave game soundtracks?
Check out our complete master vaults for indie game developers:

👉 itch.io Store: https://gameverse-audio.itch.io
👉 Gumroad Store: https://gameverseaudio.gumroad.com

Thank you for supporting indie game development!
================================================================================
"""

def create_showcase_image(icons, title_text, out_path):
    """8枚のアイコンを4x2の綺麗なグリッドプレビュー画像として生成"""
    cw, ch = 1200, 700
    canvas = Image.new("RGBA", (cw, ch), (15, 20, 30, 255))
    draw = ImageDraw.Draw(canvas)

    # 背景グリッド線
    for gx in range(0, cw, 40):
        draw.line([(gx, 0), (gx, ch)], fill=(26, 36, 54, 100), width=1)
    for gy in range(0, ch, 40):
        draw.line([(0, gy), (cw, gy)], fill=(26, 36, 54, 100), width=1)

    # 上部タイトル
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf", 36)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 18, index=2)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((cw // 2, 45), title_text, font=font_title, fill=(255, 255, 255), anchor="mm")
    draw.text((cw // 2, 85), "FREE 2D GAME ASSET PACK  •  512x512 TRANSPARENT PNG  •  COMMERCIAL USE ALLOWED", font=font_sub, fill=(148, 163, 184), anchor="mm")

    # 4x2 グリッド配置 (各220x220)
    slot_size = 200
    start_x = (cw - (4 * slot_size + 3 * 30)) // 2
    start_y = 130

    for idx, icon_path in enumerate(icons[:8]):
        col = idx % 4
        row = idx // 4
        x = start_x + col * (slot_size + 30)
        y = start_y + row * (slot_size + 30)

        # スロット背景枠
        draw.rounded_rectangle([x, y, x + slot_size, y + slot_size], radius=16, fill=(22, 30, 46, 220), outline=(59, 130, 246, 120), width=2)

        if icon_path.exists():
            ic = Image.open(icon_path).convert("RGBA").resize((slot_size - 30, slot_size - 30), Image.Resampling.LANCZOS)
            canvas.paste(ic, (x + 15, y + 15), ic)

    canvas.save(out_path, "PNG")

def process_pack(pack, api_key):
    folder_name = pack["folder_name"]
    zip_name = pack["zip_name"]
    title = pack["title"]
    items = pack["items"]

    target_dir = OUTPUTS_DIR / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    orig_dir = target_dir / "Original_Art"
    trans_dir = target_dir / "Transparent_Icons"
    orig_dir.mkdir(exist_ok=True)
    trans_dir.mkdir(exist_ok=True)

    print("\n" + "=" * 60)
    print(f"📦 パック生成開始: {title}")
    print(f"📁 フォルダ: {target_dir.name} (数字なし)")
    print("=" * 60)

    icon_paths = []

    for idx, item in enumerate(items, 1):
        slug = item["slug"]
        orig_file = orig_dir / f"{slug}.png"
        icon_file = trans_dir / f"{slug}.png"
        icon_paths.append(icon_file)

        if orig_file.exists() and icon_file.exists():
            print(f"  ⏭️ [{idx}/{len(items)}] 既存スキップ: {slug}")
            continue

        print(f"  🎨 [{idx}/{len(items)}] 生成中: {item['name']} ({slug})...")
        prompt = (
            f"A professional 2D video game inventory asset icon of {item['desc']}. "
            "Isolated, perfectly centered on pure solid pitch black background (#000000). "
            "Sharp crisp edges, vibrant saturated glow, studio quality digital fantasy RPG game art. "
            "1:1 aspect ratio, absolutely NO text, NO letters, NO words, NO label, NO frame, NO border, NO table, NO background scene."
        )

        for attempt in range(3):
            try:
                img_bytes = generate_single_image(api_key, prompt)
                orig_file.write_bytes(img_bytes)

                # 透過処理
                img = Image.open(orig_file)
                trans_img = make_transparent_luma(img, low_thresh=18, high_thresh=55)

                bbox = trans_img.getbbox()
                if bbox:
                    cropped = trans_img.crop(bbox)
                    iw, ih = cropped.size
                    max_dim = max(iw, ih)
                    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
                    scale = (512 * 0.88) / max_dim
                    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
                    resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
                    px = (512 - nw) // 2
                    py = (512 - nh) // 2
                    canvas.paste(resized, (px, py), resized)
                    canvas.save(icon_file, "PNG")
                else:
                    trans_img.resize((512, 512), Image.Resampling.LANCZOS).save(icon_file, "PNG")

                print(f"    ✨ 透過完了: {icon_file.name}")
                break
            except Exception as e:
                print(f"    ⚠️ リトライ ({attempt + 1}/3): {e}")
                time.sleep(3)

        time.sleep(1)

    # プレビュー画像
    preview_file = target_dir / "showcase_preview.png"
    create_showcase_image(icon_paths, pack["category_title"], preview_file)
    print(f"  🖼️ プレビュー画像生成完了: {preview_file.name}")

    # ライセンス & README
    (target_dir / "LICENSE.txt").write_text(LICENSE_TEXT, encoding="utf-8")
    (target_dir / "README.txt").write_text(README_TEXT, encoding="utf-8")

    # 配布用ZIP
    zip_path = target_dir / zip_name
    print(f"  📦 ZIP圧縮中: {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(target_dir / "LICENSE.txt", arcname="LICENSE.txt")
        zf.write(target_dir / "README.txt", arcname="README.txt")
        zf.write(preview_file, arcname="showcase_preview.png")
        for f in trans_dir.glob("*.png"):
            zf.write(f, arcname=f"Transparent_Icons/{f.name}")
        for f in orig_dir.glob("*.png"):
            zf.write(f, arcname=f"Original_Art/{f.name}")

    print(f"  ✅ パック完成: {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return zip_path

def main():
    api_key = load_api_key()
    if not api_key:
        print("❌ Gemini APIキーが見つかりません。")
        sys.exit(1)

    print("==================================================")
    print("🚀 無料ゲームアセット 3パック生成開始")
    print("※ ユーザー指定ルール: pack1等の数字表記は一切使用しない")
    print("==================================================")

    created_zips = []
    for pack in PACK_DEFINITIONS:
        zp = process_pack(pack, api_key)
        created_zips.append(zp)

    print("\n" + "=" * 60)
    print("🎉 全3パック（計24枚）の無料アセット生成がすべて完了しました！")
    for zp in created_zips:
        print(f"🎁 {zp.name} -> {zp}")
    print("=" * 60)

if __name__ == "__main__":
    main()
