#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deploy_new_free_packs.py: 新規無料ゲームアセット3パックの出品スクリプト
- ユーザー指定ルール: 「pack1とか数字は書かない」
- Gumroad: 3つの独立した無料商品（$0 / PWYW）として新規作成＆公開
- itch.io: Butler CLI を使用して free-game-assets の各専用チャンネル（数字なし）へプッシュ
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects")
ASSETS_DIR = BASE_DIR / "Game-Assets"
OUTPUTS_DIR = ASSETS_DIR / "outputs"
MUSIC_DIR = BASE_DIR / "Game-Music"
ENV_PATH = MUSIC_DIR / ".env"
GUMROAD_BIN = str(MUSIC_DIR / "bin" / "gumroad")
BUTLER_BIN = str(MUSIC_DIR / "bin" / "butler")

# 認証トークンの読み込み
env = os.environ.copy()
if ENV_PATH.exists():
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("GUMROAD_ACCESS_TOKEN="):
            env["GUMROAD_ACCESS_TOKEN"] = line.split("=", 1)[1].strip()
        elif line.startswith("BUTLER_API_KEY=") or line.startswith("ITCH_API_KEY="):
            env["BUTLER_API_KEY"] = line.split("=", 1)[1].strip()

PRODUCTS = [
    {
        "slug": "free-mystic-potions",
        "channel": "mystic-potions",
        "name": "[FREE] 2D Game Asset Pack — Mystic Potions & Alchemy Elixirs",
        "summary": "100% free studio-quality transparent 2D potion & elixir icons for indie game developers. Drag-and-drop ready for Unity, Godot, Unreal Engine & RPG Maker.",
        "folder": OUTPUTS_DIR / "Free_Mystic_Potions",
        "zip_file": OUTPUTS_DIR / "Free_Mystic_Potions" / "Free_2D_Game_Assets_Mystic_Potions.zip",
        "cover_file": OUTPUTS_DIR / "Free_Mystic_Potions" / "showcase_preview.png",
        "bullets": [
            "8 Unique Hand-Crafted Potions & Elixirs (Health, Mana, Poison, Golden Ambrosia, Frost, Fire Blast, Stamina, Holy Water)",
            "100% Clean Alpha Transparency (No halos, perfectly isolated on 512x512 canvas)",
            "Original High-Resolution Master Art (1024x1024) included",
            "Universal Engine Ready: Unity, Godot, Unreal Engine, GameMaker, and RPG Maker"
        ]
    },
    {
        "slug": "free-treasure-loot",
        "channel": "treasure-loot",
        "name": "[FREE] 2D Game Asset Pack — Treasure & Dungeon Loot",
        "summary": "100% free studio-quality transparent 2D treasure chests, keys, and loot icons for indie game developers. Commercial use allowed.",
        "folder": OUTPUTS_DIR / "Free_Treasure_Loot",
        "zip_file": OUTPUTS_DIR / "Free_Treasure_Loot" / "Free_2D_Game_Assets_Treasure_Loot.zip",
        "cover_file": OUTPUTS_DIR / "Free_Treasure_Loot" / "showcase_preview.png",
        "bullets": [
            "8 Dungeon Loot & Treasure Icons (Reinforced Wooden Chest, Royal Gold Chest, Sinister Mimic, Gold Coins Pile, Skeleton Key, Runic Key, Sealed Scroll, Golden Grail)",
            "100% Clean Alpha Transparency (512x512 transparent PNGs)",
            "Original High-Resolution Master Art (1024x1024) included",
            "Full Perpetual Commercial License: Commercial games, Steam, mobile, Web"
        ]
    },
    {
        "slug": "free-status-buffs",
        "channel": "status-buffs",
        "name": "[FREE] 2D Game Asset Pack — RPG Status & Buff Icons",
        "summary": "100% free studio-quality transparent 2D status condition, buff, and debuff icons for indie game developers.",
        "folder": OUTPUTS_DIR / "Free_Status_Buffs",
        "zip_file": OUTPUTS_DIR / "Free_Status_Buffs" / "Free_2D_Game_Assets_Status_Buffs.zip",
        "cover_file": OUTPUTS_DIR / "Free_Status_Buffs" / "showcase_preview.png",
        "bullets": [
            "8 RPG Status & Buff Icons (Poison Skull, Burn Flame, Freeze Ice, Shock Lightning, Attack Power Buff, Defense Shield Buff, Bleed Droplets, Stun Stars)",
            "100% Clean Alpha Transparency (512x512 transparent PNGs, clean borderless icons)",
            "Original High-Resolution Master Art (1024x1024) included",
            "No Credit Required: 100% royalty-free for commercial and free indie projects"
        ]
    }
]

def make_description(p):
    bullet_html = "".join([f"<li><strong>{b}</strong></li>" for b in p["bullets"]])
    return f"""<p>🎁 <strong>{p['name']}</strong></p>
<p>{p['summary']}</p>
<hr>
<h3>📦 What's Inside:</h3>
<ul>{bullet_html}</ul>
<hr>
<h3>📜 Perpetual Commercial License:</h3>
<ul>
  <li>✅ <strong>100% Commercial Use:</strong> Cleared for Steam, itch.io, iOS, Android, consoles, and web games.</li>
  <li>✅ <strong>Full Modification Rights:</strong> Freely crop, resize, recolor, and animate.</li>
  <li>✅ <strong>NO ATTRIBUTION REQUIRED:</strong> Credit is appreciated but completely optional.</li>
  <li>❌ Standalone resale, redistribution, or sharing of the raw asset files is prohibited.</li>
</ul>
<hr>
<h3>👑 WANT ALL OUR ASSETS &amp; FUTURE EXPANSIONS?</h3>
<p>Get lifetime access to our entire expanding library of sprites, UI, and icons for just $1.99!</p>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Ultimate 2D Game Asset Vault ($1.99)</strong></a></p>
<p>👉 <a href="https://gameverse-audio.itch.io/game-asset-vault" target="_blank"><strong>View The Vault on itch.io ($1.99)</strong></a></p>
"""

def deploy_gumroad():
    print("==================================================")
    print("🚀 [Gumroad] 新規無料アセット 3商品の出品開始")
    print("==================================================")

    # 既存商品チェック
    list_res = subprocess.run([GUMROAD_BIN, "products", "list", "--json", "--no-input"], env=env, capture_output=True, text=True)
    existing_slugs = {}
    if list_res.returncode == 0:
        data = json.loads(list_res.stdout)
        for prod in data.get("products", []):
            slug = prod.get("custom_permalink")
            if slug:
                existing_slugs[slug] = prod.get("id")

    for idx, p in enumerate(PRODUCTS, 1):
        slug = p["slug"]
        print(f"\n[{idx}/3] 🛍️ Gumroad 処理中: {p['name']} (slug: {slug})")
        desc = make_description(p)

        if slug in existing_slugs:
            pid = existing_slugs[slug]
            print(f"  ⏩ 既存商品更新中 (ID: {pid})...")
            up_cmd = [
                GUMROAD_BIN, "products", "update", pid,
                "--name", p["name"],
                "--currency", "usd",
                "--price", "0",
                "--suggested-price", "1.00",
                "--pay-what-you-want",
                "--description", desc,
                "--custom-summary", p["summary"],
                "--cover-image", str(p["cover_file"]),
                "--thumbnail", str(p["cover_file"]),
                "--file", str(p["zip_file"]),
                "--file-name", p["zip_file"].name,
                "--yes"
            ]
            res = subprocess.run(up_cmd, env=env, capture_output=True, text=True)
            subprocess.run([GUMROAD_BIN, "products", "publish", pid, "--yes"], env=env)
            print(f"  ✅ 更新＆公開完了: https://gameverseaudio.gumroad.com/l/{slug}")
        else:
            print(f"  ✨ 新規商品作成中...")
            create_cmd = [
                GUMROAD_BIN, "products", "create",
                "--name", p["name"],
                "--price", "0",
                "--currency", "usd",
                "--pay-what-you-want",
                "--suggested-price", "1.00",
                "--custom-permalink", slug,
                "--custom-summary", p["summary"],
                "--description", desc,
                "--cover-image", str(p["cover_file"]),
                "--thumbnail", str(p["cover_file"]),
                "--file", str(p["zip_file"]),
                "--file-name", p["zip_file"].name,
                "--tag", "gamedev", "--tag", "game-assets", "--tag", "rpg", "--tag", "2d", "--tag", "sprites",
                "--yes"
            ]
            res = subprocess.run(create_cmd, env=env, capture_output=True, text=True)
            print("  Create Output:", res.stdout[:200])

            # 公開処理
            list_res2 = subprocess.run([GUMROAD_BIN, "products", "list", "--json", "--no-input"], env=env, capture_output=True, text=True)
            if list_res2.returncode == 0:
                d2 = json.loads(list_res2.stdout)
                for prod in d2.get("products", []):
                    if prod.get("custom_permalink") == slug:
                        pid = prod.get("id")
                        subprocess.run([GUMROAD_BIN, "products", "publish", pid, "--yes"], env=env)
                        print(f"  ✅ 公開完了: https://gameverseaudio.gumroad.com/l/{slug}")
                        break

def deploy_itch():
    print("\n==================================================")
    print("🎮 [itch.io] free-game-assets へのプッシュ開始 (Butler CLI)")
    print("==================================================")

    for idx, p in enumerate(PRODUCTS, 1):
        target = f"gameverse-audio/free-game-assets:{p['channel']}"
        print(f"\n[{idx}/3] 📤 itch.io プッシュ中: {p['zip_file'].name} -> {target}")
        push_cmd = [
            BUTLER_BIN, "push",
            str(p["zip_file"]),
            target,
            "--userversion", "1.0.0"
        ]
        res = subprocess.run(push_cmd, env=env, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  ✅ itch.io プッシュ成功: {target}")
        else:
            print(f"  ⚠️ Butler エラー:\n{res.stderr}")

    print("\n🔗 itch.io 無料配布ページ: https://gameverse-audio.itch.io/free-game-assets")

if __name__ == "__main__":
    deploy_gumroad()
    deploy_itch()
