#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
1素材＝1枚個別のAPI生成・アルファ透過・マルチ解像度化・ZIPパッケージング完全自動化スクリプト
仕様: /Users/base/Automated-Projects/.agents/rules/03_asset_commerce.md
"""

import os
import sys
import time
import json
import base64
import zipfile
import requests
import numpy as np
from pathlib import Path
from PIL import Image, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Assets")
ENV_PATH = Path("/Users/base/Antigravity-Automation-Projects/Game-Music/.env")

api_key = None
if ENV_PATH.exists():
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if "GEMINI_API_KEY" in line:
            api_key = line.split("=", 1)[1].strip()
            break

if not api_key:
    print("❌ GEMINI_API_KEY が見つかりません。")
    sys.exit(1)

OUTPUT_BASE = BASE_DIR / "outputs" / "Free_Holy_Dark_Knight_Relics_8Pack"
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

# 旧重複スターターパックの削除
old_pack_dir = BASE_DIR / "outputs" / "Free_Starter_Pack_Selected"
if old_pack_dir.exists():
    import shutil
    shutil.rmtree(old_pack_dir)
    print("🗑️ 旧スターターパック (Free_Starter_Pack_Selected) を全削除しました。")

# 1素材＝1枚でAPI個別生成する8つのアセット定義
ASSET_ITEMS = [
    {
        "slug": "01_holy_knight_shield",
        "name": "Holy Knight Shield",
        "prompt": "Strictly centered 2D flat game asset icon of an ornate golden holy knight shield with a glowing sun emblem, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    },
    {
        "slug": "02_dark_shadow_sword",
        "name": "Dark Shadow Greatsword",
        "prompt": "Strictly centered 2D flat game asset icon of a dark purple void shadow greatsword with glowing violet runes, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    },
    {
        "slug": "03_dragon_scale_amulet",
        "name": "Dragon Scale Amulet",
        "prompt": "Strictly centered 2D flat game asset icon of an emerald dragon scale protective amulet with a silver chain, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    },
    {
        "slug": "04_phoenix_ruby_ring",
        "name": "Phoenix Ruby Ring",
        "prompt": "Strictly centered 2D flat game asset icon of a crimson phoenix wing ring with a large glowing red ruby gem, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    },
    {
        "slug": "05_frost_rune_stone",
        "name": "Frost Rune Stone",
        "prompt": "Strictly centered 2D flat game asset icon of a crystalline blue frost rune stone with glowing icy runes, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    },
    {
        "slug": "06_thunder_gauntlet",
        "name": "Thunder Strike Gauntlet",
        "prompt": "Strictly centered 2D flat game asset icon of an armored plate gauntlet crackling with electric purple lightning bolts, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    },
    {
        "slug": "07_necromancy_grimoire",
        "name": "Necromancy Grimoire",
        "prompt": "Strictly centered 2D flat game asset icon of an ornate dark leather grimoire book with a glowing silver skull centerpiece, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    },
    {
        "slug": "08_winged_celestial_boots",
        "name": "Winged Celestial Boots",
        "prompt": "Strictly centered 2D flat game asset icon of a pair of silver armored boots with glowing white feather wings, isolated on pure solid black background (#000000). Sharp crisp vector game art style, vibrant edge glow. Absolutely NO text, NO words, NO letters, NO borders, NO watermark. Single 2D transparent-ready sprite."
    }
]

def make_transparent_luma(img, low_thresh=20, high_thresh=60):
    """単体画像からの高精度ルミナンスキーイング背景透過"""
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

def generate_image_api(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }
    res = requests.post(url, json=payload, timeout=60)
    if res.status_code != 200:
        raise RuntimeError(f"API Error {res.status_code}: {res.text[:300]}")
    data = res.json()
    b64_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    return base64.b64decode(b64_data)

def main():
    print("==================================================")
    print("🚀 1素材＝1枚個別API生成 ＆ パッケージング全自動パイプライン")
    print(f"対象枚数: {len(ASSET_ITEMS)} 枚")
    print("==================================================")

    res_dirs = {
        32: OUTPUT_BASE / "Transparent_Icons_32px",
        64: OUTPUT_BASE / "Transparent_Icons_64px",
        128: OUTPUT_BASE / "Transparent_Icons_128px",
        256: OUTPUT_BASE / "Transparent_Icons_256px",
        512: OUTPUT_BASE / "Transparent_Icons_512px",
        1024: OUTPUT_BASE / "Transparent_Icons_1024px"
    }
    for d in res_dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    orig_dir = OUTPUT_BASE / "Original_Art"
    orig_dir.mkdir(parents=True, exist_ok=True)

    for idx, item in enumerate(ASSET_ITEMS, 1):
        slug = item["slug"]
        name = item["name"]
        print(f"\n[{idx}/{len(ASSET_ITEMS)}] 🎨 個別API生成中: {name} ({slug})...")
        
        try:
            img_bytes = generate_image_api(item["prompt"])
            orig_path = orig_dir / f"{slug}.png"
            with open(orig_path, "wb") as f:
                f.write(img_bytes)
            
            with Image.open(orig_path) as raw_img:
                raw_img = raw_img.convert("RGB")
                trans_img = make_transparent_luma(raw_img)

                # 各解像度への高画質変換
                for sz, out_d in res_dirs.items():
                    resized = trans_img.resize((sz, sz), Image.Resampling.LANCZOS)
                    resized.save(out_d / f"{slug}_{sz}px.png", "PNG")

            print(f"  ✅ 透過・マルチ解像度変換完了")
            time.sleep(2)
        except Exception as e:
            print(f"❌ エラー ({slug}): {e}", file=sys.stderr)

    # ライセンスファイル＆README
    with open(OUTPUT_BASE / "LICENSE.txt", "w", encoding="utf-8") as f:
        f.write("Free Commercial License - GameVerse Assets\nCredit appreciated: GameVerse Audio (https://gameverse-audio.itch.io)\n")

    # ZIP化
    zip_path = OUTPUT_BASE / "Free_2D_Game_Assets_Holy_Dark_Knight_Relics_8Pack.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(OUTPUT_BASE):
            for file in files:
                if file.endswith(".zip"):
                    continue
                fp = Path(root) / file
                arcname = fp.relative_to(OUTPUT_BASE)
                zf.write(fp, arcname)

    print("\n==================================================")
    print(f"🎉 全8素材の個別生成・パッケージング完了！")
    print(f"ZIP保存先: {zip_path}")
    print(f"サイズ: {zip_path.stat().st_size / (1024*1024):.2f} MB")
    print("==================================================")

if __name__ == "__main__":
    main()
