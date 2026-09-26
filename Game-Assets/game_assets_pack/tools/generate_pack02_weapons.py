#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_pack02_weapons.py: Pack 02 ファンタジー武器8種パック自動生成 ＆ 透過ZIP化ツール
- Gemini API (gemini-2.5-flash-image) により武器8種を1024x1024黒背景で個別生成
- 高精度ルミナンスキーイングによる自動透過 (512x512 & 1024x1024)
- LICENSE.txt 同梱 ＆ 完全パッケージZIP作成
- Butler CLI による itch.io (game-asset-vault:pack02-fantasy-weapons) への自動プッシュ
"""

import os
import sys
import time
import json
import base64
import zipfile
import requests
import subprocess
from pathlib import Path
from PIL import Image
import numpy as np

ROOT_DIR = Path("/Users/base/Automated-Projects").resolve()
ENV_PATH = ROOT_DIR / "YouTube" / ".env"
MUSIC_ENV_PATH = ROOT_DIR / "Game-Music" / ".env"
OUTPUTS_DIR = ROOT_DIR / "Game-Assets" / "outputs"
BUTLER_PATH = ROOT_DIR / "Game-Music" / "bin" / "butler"

def load_api_key():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("ACCOUNT_1_GEMINI_API_KEY")
    if not api_key and ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ACCOUNT_1_GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break
    return api_key

def get_itch_credentials():
    api_key = os.environ.get("ITCH_API_KEY") or os.environ.get("BUTLER_API_KEY")
    if not api_key and MUSIC_ENV_PATH.exists():
        for line in MUSIC_ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ITCH_API_KEY=") or line.startswith("BUTLER_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break
    username = os.environ.get("ITCH_USERNAME", "gameverse-audio")
    return api_key, username

def make_transparent_luma(img, low_thresh=18, high_thresh=60):
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
    try:
        b64_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
        return base64.b64decode(b64_data)
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response: {data}")

WEAPON_ITEMS = [
    {
        "name": "Holy Light Greatsword",
        "slug": "weapon_01_holy_greatsword",
        "desc": "a legendary holy radiant greatsword with a gleaming golden steel blade, sacred blue engraved runes, ornate winged crossguard, fantasy RPG game inventory icon"
    },
    {
        "name": "Frost Katana",
        "slug": "weapon_02_frost_katana",
        "desc": "an ice crystal samurai katana sword with sharp cyan frozen mist, transparent diamond ice blade, detailed silver tsuba guard, fantasy RPG game inventory icon"
    },
    {
        "name": "Thunder Battleaxe",
        "slug": "weapon_03_thunder_battleaxe",
        "desc": "a brutal double-bladed dwarven war battleaxe crackling with violent yellow electric lightning sparks, heavy dark iron steel, fantasy RPG game inventory icon"
    },
    {
        "name": "Shadow Assassin Dagger",
        "slug": "weapon_04_shadow_dagger",
        "desc": "a sinister curved rogue assassin dagger dripping with dark violet shadow smoke and eerie purple poison mist, obsidian blade, fantasy RPG game inventory icon"
    },
    {
        "name": "Archmage Crystal Staff",
        "slug": "weapon_05_crystal_staff",
        "desc": "an ancient sorcerer wooden wizard staff topped with a glowing mystical levitating ethereal cyan arcane crystal orb, fantasy RPG game inventory icon"
    },
    {
        "name": "Golden Elven Bow",
        "slug": "weapon_06_elven_bow",
        "desc": "an elegant elven composite recurve longbow made of polished golden wood with glowing emerald green magical string, fantasy RPG game inventory icon"
    },
    {
        "name": "Molten War Hammer",
        "slug": "weapon_07_molten_hammer",
        "desc": "a massive forge war hammer with cracked molten volcanic lava flowing through the steel hammerhead, glowing hot red embers, fantasy RPG game inventory icon"
    },
    {
        "name": "Radiant Paladin Shield",
        "slug": "weapon_08_paladin_shield",
        "desc": "an ornate medieval paladin kite shield with a golden lion crest, polished platinum steel, and glowing divine protection barrier, fantasy RPG game inventory icon"
    }
]

LICENSE_TEXT = """================================================================================
GAME ASSET LICENSE & TERMS OF USE
================================================================================

Thank you for downloading this game asset pack!

--------------------------------------------------------------------------------
【PERMITTED USES】
--------------------------------------------------------------------------------
1. Commercial & Non-Commercial Projects
   - You can freely use these assets in commercial, indie, or free games.
   
2. Supported Platforms
   - Steam, itch.io, App Store (iOS), Google Play (Android), Nintendo Switch, PlayStation, Xbox, PC, Web, etc.

3. Modifications Allowed
   - You may resize, crop, edit colors, add visual effects, or combine these assets with other artwork to fit your project.

4. Credit is Optional
   - Attribution/credit is appreciated but NOT required. You are welcome to use these assets without crediting the author.

--------------------------------------------------------------------------------
【PROHIBITED USES】
--------------------------------------------------------------------------------
1. Standalone Resale & Redistribution
   - You may NOT resell, redistribute, or sublicense these assets as standalone stock files, sheets, or texture packs.
2. Direct Extraction
   - You may not distribute raw asset files in an unprotected, easily extractable form.
3. NFT & Blockchain
   - Using these assets for NFTs or blockchain tokens is strictly prohibited.

================================================================================
Produced by GameVerse Audio & Game Assets Studio
================================================================================
"""

def main():
    api_key = load_api_key()
    if not api_key:
        print("❌ Gemini APIキーが見つかりません。")
        sys.exit(1)

    today_str = time.strftime("%Y%m%d")
    time_str = time.strftime("%H%M%S")
    pack_name = f"Pack02_Fantasy_Weapons_{today_str}_{time_str}"
    target_dir = OUTPUTS_DIR / pack_name
    target_dir.mkdir(parents=True, exist_ok=True)

    orig_dir = target_dir / "Original_Art"
    trans_512_dir = target_dir / "Transparent_Icons_512px"
    trans_1024_dir = target_dir / "Transparent_Icons_1024px"
    orig_dir.mkdir(exist_ok=True)
    trans_512_dir.mkdir(exist_ok=True)
    trans_1024_dir.mkdir(exist_ok=True)

    print("==================================================")
    print("⚔️ [Pack 02] ファンタジー武器8種パック自動生成開始")
    print(f"📁 出力先: {target_dir}")
    print("==================================================")

    for idx, item in enumerate(WEAPON_ITEMS, 1):
        num_str = f"{idx:02d}"
        slug = item["slug"]
        print(f"\n🎨 [{idx}/8] 生成中: {item['name']} ({slug})...")

        prompt = (
            f"A professional 2D video game inventory asset icon of {item['desc']}. "
            "Isolated, perfectly centered on pure solid pitch black background (#000000). "
            "Vibrant magical elemental glow, sharp crisp edges, high-contrast digital fantasy RPG game art. "
            "1:1 aspect ratio, absolutely NO text, NO letters, NO words, NO frame, NO border, NO table, NO background scene."
        )

        success = False
        for attempt in range(3):
            try:
                img_bytes = generate_single_image(api_key, prompt)
                orig_file = orig_dir / f"{slug}_{num_str}.png"
                orig_file.write_bytes(img_bytes)

                # 透過処理
                img = Image.open(orig_file)
                trans_img = make_transparent_luma(img, low_thresh=18, high_thresh=55)

                # 1024px 透過保存
                trans_1024_file = trans_1024_dir / f"{slug}_icon_{num_str}_1024px.png"
                trans_img.save(trans_1024_file, "PNG")

                # 512px 正方形センタリング
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
                    icon_512_file = trans_512_dir / f"{slug}_icon_{num_str}_512px.png"
                    canvas.save(icon_512_file, "PNG")
                else:
                    icon_512_file = trans_512_dir / f"{slug}_icon_{num_str}_512px.png"
                    trans_img.resize((512, 512), Image.Resampling.LANCZOS).save(icon_512_file, "PNG")

                print(f"  ✨ [完了] 透過PNG保存 ➔ {icon_512_file.name}")
                success = True
                break
            except Exception as e:
                print(f"  ⚠️ リトライ ({attempt + 1}/3): {e}")
                time.sleep(3)

        if not success:
            print(f"  ❌ [{idx}] 生成失敗: {item['name']}")

        time.sleep(1.5)

    # LICENSE.txt
    lic_file = target_dir / "LICENSE.txt"
    lic_file.write_text(LICENSE_TEXT, encoding="utf-8")

    # ZIP作成
    zip_path = target_dir / "Pack02_Fantasy_Weapons_Complete_Pack.zip"
    print(f"\n📦 配布用ZIPパッケージ作成中: {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(lic_file, "LICENSE.txt")
        for f in sorted(trans_512_dir.glob("*.png")):
            zf.write(f, f"Transparent_Icons_512px/{f.name}")
        for f in sorted(trans_1024_dir.glob("*.png")):
            zf.write(f, f"Transparent_Icons_1024px/{f.name}")
        for f in sorted(orig_dir.glob("*.png")):
            zf.write(f, f"Original_Art_Master/{f.name}")

    print(f"✅ ZIPパッケージ作成完了: {zip_path} ({zip_path.stat().st_size / (1024*1024):.2f} MB)")

    # Butler CLI で itch.io の game-asset-vault へ自動プッシュ
    itch_key, itch_user = get_itch_credentials()
    if itch_key:
        print("\n🚀 itch.io Butler CLI 自動プッシュ開始...")
        target = f"{itch_user}/game-asset-vault:pack02-fantasy-weapons"
        butler_cmd = str(BUTLER_PATH) if BUTLER_PATH.exists() else "butler"
        b_env = os.environ.copy()
        b_env["BUTLER_API_KEY"] = itch_key

        push_cmd = [
            butler_cmd, "push", str(zip_path), target,
            "--userversion=1.0.0"
        ]
        try:
            b_res = subprocess.run(push_cmd, env=b_env, check=True, capture_output=True, text=True)
            print(f"✅ itch.io Vault (game-asset-vault:pack02-fantasy-weapons) へのプッシュ完了！")
            print(b_res.stdout)
        except Exception as be:
            print(f"❌ Butler プッシュエラー: {be}")
    else:
        print("⚠️ ITCH_API_KEY が見つからないためButlerプッシュをスキップしました。")

    print("\n==================================================")
    print("🎉 Pack 02 ファンタジー武器パック生成 ＆ itch.io 配信完了！")
    print("==================================================")

if __name__ == "__main__":
    main()
