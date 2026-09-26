#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_assets_api.py: Gemini APIによるゲーム素材8枚パック自動生成 ＆ 透過ZIP化ツール
- Gemini API (gemini-2.5-flash-image) を直接呼び出し
- 単体アイコン（黒背景）を1枚ずつ生成（スライス事故完全ゼロ）
- ルミナンスキーイングによる自動背景透過 ＆ 黒フチ除去
- 配布・販売用ZIPパッケージの自動生成
"""

import os
import sys
import time
import json
import base64
import zipfile
import requests
from pathlib import Path
from PIL import Image
import numpy as np

# プロジェクトルートと環境設定
ROOT_DIR = Path("/Users/base/Automated-Projects").resolve()
ENV_PATH = ROOT_DIR / "YouTube" / ".env"
OUTPUTS_DIR = ROOT_DIR / "Game-Assets" / "outputs"

def load_api_key():
    """環境変数または.envファイルからGemini APIキーを取得"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("ACCOUNT_1_GEMINI_API_KEY")
    if not api_key and ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ACCOUNT_1_GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break
    return api_key

def make_transparent_luma(img, low_thresh=20, high_thresh=60):
    """
    黒・ダーク背景を高精度に透過（ルミナンス＋カラーキーイング）
    発光エフェクトや魔法の光を半透明で残し、黒フチを除去する
    """
    rgba = img.convert("RGBA")
    data = np.array(rgba, dtype=np.float32)

    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    max_val = np.maximum(np.maximum(r, g), b)
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    key_metric = 0.7 * max_val + 0.3 * luma

    # スムーズなアルファマスク生成 (Smoothstep)
    alpha = np.zeros_like(key_metric)
    mask_opaque = key_metric >= high_thresh
    mask_trans = key_metric <= low_thresh
    mask_inter = (~mask_opaque) & (~mask_trans)

    alpha[mask_opaque] = 255.0
    alpha[mask_trans] = 0.0

    t = (key_metric[mask_inter] - low_thresh) / (high_thresh - low_thresh)
    alpha[mask_inter] = (3 * t**2 - 2 * t**3) * 255.0

    # ブラックフリンジ除去 (Unmultiply)
    alpha_norm = np.clip(alpha / 255.0, 0.001, 1.0)
    for c in range(3):
        boosted = data[:, :, c] / alpha_norm
        data[:, :, c] = np.clip(boosted, 0, 255)

    data[:, :, 3] = np.clip(alpha, 0, 255)
    return Image.fromarray(data.astype(np.uint8), "RGBA")

def generate_single_image(api_key, prompt):
    """Gemini APIを呼び出して1枚の画像を生成（Base64バイト列で取得）"""
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
        raise RuntimeError(f"Unexpected API response structure: {data}")

def run_pack_pipeline(pack_id, pack_title, items):
    """8枚パックの生成・透過・ZIP化パイプライン"""
    api_key = load_api_key()
    if not api_key:
        print("❌ Gemini APIキーが見つかりません。")
        return

    today_str = time.strftime("%Y%m%d")
    time_str = time.strftime("%H%M%S")
    pack_dir_name = f"{pack_id}_{today_str}_{time_str}"
    target_dir = OUTPUTS_DIR / pack_dir_name
    target_dir.mkdir(parents=True, exist_ok=True)

    orig_dir = target_dir / "Original_Art"
    trans_dir = target_dir / "Transparent_Icons_512px"
    orig_dir.mkdir(exist_ok=True)
    trans_dir.mkdir(exist_ok=True)

    print("==================================================")
    print(f"🔥 [Game Assets API] 8枚パック生成開始: {pack_title}")
    print(f"📁 保存先フォルダ: {target_dir.name}")
    print("==================================================")

    created_files = []

    for idx, item in enumerate(items, 1):
        num_str = f"{idx:02d}"
        file_slug = item["slug"]
        print(f"\n🎨 [{idx}/{len(items)}] 生成中: {item['name']} ({file_slug})...")

        prompt = (
            f"A professional 2D video game inventory asset icon of {item['desc']}. "
            "Isolated, perfectly centered on pure solid pitch black background (#000000). "
            "Vibrant magical fiery glow, sharp crisp edges, high-contrast digital fantasy RPG game art. "
            "1:1 aspect ratio, absolutely NO text, NO letters, NO words, NO frame, NO border, NO table, NO background scene."
        )

        success = False
        for attempt in range(3):
            try:
                img_bytes = generate_single_image(api_key, prompt)
                orig_file = orig_dir / f"{file_slug}_{num_str}.png"
                orig_file.write_bytes(img_bytes)

                # 画像の読み込みと透過処理
                img = Image.open(orig_file)
                trans_img = make_transparent_luma(img, low_thresh=18, high_thresh=55)

                # 512x512の正方形アイコンにリサイズ＆センタリング
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
                    icon_file = trans_dir / f"{file_slug}_icon_{num_str}_512px.png"
                    canvas.save(icon_file, "PNG")
                else:
                    icon_file = trans_dir / f"{file_slug}_icon_{num_str}_512px.png"
                    trans_img.resize((512, 512), Image.Resampling.LANCZOS).save(icon_file, "PNG")

                print(f"  ✨ [完了]: 透過PNG保存 ➔ {icon_file.name}")
                created_files.append((orig_file, icon_file))
                success = True
                break
            except Exception as e:
                print(f"  ⚠️ リトライ ({attempt + 1}/3): {e}")
                time.sleep(3)

        if not success:
            print(f"  ❌ [{idx}] 生成に失敗しました: {item['name']}")

        time.sleep(1)

    # LICENSE.txt (英語のみの商用ゲームアセット利用規約) を自動生成
    license_text = """================================================================================
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
1. No Redistribution or Resale
   - You cannot resell, redistribute, sub-license, or share these raw asset files (as images, textures, or asset packs).
   
2. No NFT / Blockchain Usage
   - You cannot use these assets for NFT minting, crypto projects, or blockchain-based tokens.

--------------------------------------------------------------------------------
【DISCLAIMER】
--------------------------------------------------------------------------------
The assets are provided "as is", without warranty of any kind. The author shall not be liable for any claims, damages, or liabilities arising from the use of these assets.
================================================================================
"""
    license_file = target_dir / "LICENSE.txt"
    license_file.write_text(license_text, encoding="utf-8")

    # 配布用ZIPの生成
    zip_path = target_dir / f"{pack_id}_Complete_Pack.zip"
    print(f"\n📦 配布用ZIPを圧縮中: {zip_path.name} ...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # ライセンス規約
        zf.write(license_file, arcname="LICENSE.txt")
        # 透過アイコン
        for f in trans_dir.glob("*.png"):
            zf.write(f, arcname=f"Transparent_Icons/{f.name}")
        # 原画
        for f in orig_dir.glob("*.png"):
            zf.write(f, arcname=f"Original_Art/{f.name}")

    print("\n==================================================")
    print(f"🎉 【8枚パック生成完了】全素材が完成しました！")
    print(f"👉 保存場所: {target_dir}")
    print(f"🎁 配布ZIP: {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")
    print("==================================================")

    # itch.io (game-asset-vault) への自動アップロード (Butler CLI)
    channel_slug = pack_id.lower().replace("_", "-")
    upload_to_itch(zip_path, channel_slug)

def upload_to_itch(zip_path, channel_slug):
    """Butler CLI を使用して itch.io の game-asset-vault にZIPを自動プッシュ"""
    import subprocess
    music_env = ROOT_DIR / "Game-Music" / ".env"
    api_key = os.getenv("ITCH_API_KEY") or os.getenv("BUTLER_API_KEY")
    if not api_key and music_env.exists():
        for line in music_env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ITCH_API_KEY=") or line.startswith("BUTLER_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break

    if not api_key:
        print("⚠️ itch.io APIキーが見つからないため、アップロードをスキップしました。")
        return False

    butler_bin = ROOT_DIR / "Game-Music" / "bin" / "butler"
    butler_cmd = str(butler_bin) if butler_bin.exists() else "butler"
    target = f"gameverse-audio/game-asset-vault:{channel_slug}"
    env = os.environ.copy()
    env["BUTLER_API_KEY"] = api_key

    print(f"\n🎮 [itch.io] 自動Butlerプッシュ開始 ➔ {target}")
    try:
        res = subprocess.run([butler_cmd, "push", str(zip_path), target, "--userversion=1.0.0"],
                             env=env, check=True, text=True, capture_output=True)
        print("✅ itch.io への自動アップロードが完了しました！")
        print(f"🔗 プロジェクトURL: https://gameverse-audio.itch.io/game-asset-vault")
        return True
    except Exception as e:
        print(f"⚠️ itch.io アップロードエラー: {e}")
        return False

if __name__ == "__main__":
    fire_magic_items = [
        {
            "slug": "fire_01_fireball",
            "name": "火球・ファイアボール",
            "desc": "a flaming fireball projectile hurtling through the air, trailing bright orange embers and fiery plasma sparks"
        },
        {
            "slug": "fire_02_firestorm",
            "name": "火炎竜巻・ファイアストーム",
            "desc": "a swirling fire tornado vortex of roaring orange flames and intense blazing updraft"
        },
        {
            "slug": "fire_03_meteor_strike",
            "name": "隕石召喚・メテオストライク",
            "desc": "a massive burning molten meteor falling from above, glowing red-hot with smoking fiery crater shards"
        },
        {
            "slug": "fire_04_flame_sword",
            "name": "火炎の剣・フレイムブレード",
            "desc": "an ancient steel runic broadsword completely engulfed in fierce holy orange flames and glowing heat"
        },
        {
            "slug": "fire_05_flame_shield",
            "name": "炎の盾・パイロシールド",
            "desc": "a magical shield ward made of blazing golden-orange firewall energy with interlocking protective flame crests"
        },
        {
            "slug": "fire_06_phoenix_wings",
            "name": "鳳凰の翼・フェニックスウィング",
            "desc": "a pair of majestic ethereal phoenix bird wings made of pure blazing orange and golden flame feathers"
        },
        {
            "slug": "fire_07_inferno_burst",
            "name": "地獄の業火・インフェルノバースト",
            "desc": "a violent inferno explosion shockwave erupting outwards with glowing magma cracks and fire blast waves"
        },
        {
            "slug": "fire_08_pyro_core",
            "name": "火炎の核・パイロオーブ",
            "desc": "a glowing crystal sphere core containing a turbulent miniature sun with solar flare coronal loops"
        }
    ]

    run_pack_pipeline("Pack01_Fire_Magic_Spells", "炎と火炎の魔法スキル 8種パック", fire_magic_items)
