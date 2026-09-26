#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
finish_packs_08_09_10.py
未完了の 08, 09, 10 を確実に作成・更新・公開するスクリプト
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
env_file = BASE_DIR / ".env"

env = os.environ.copy()
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v.strip("\"'\\")

token = env.get("GUMROAD_ACCESS_TOKEN")
GUMROAD_CLI = str(BASE_DIR / "bin" / "gumroad")
VAULT_DIR = Path("/Users/base/Automated-Projects/Game-Assets/outputs/Paid_Vault_10Packs")

UPGRADE_BOX = """<hr>
<h3>👑 WANT ALL 10 GENRE PACKS (80 SPRITES)?</h3>
<p>Upgrade to <strong>The Ultimate 2D Game Asset Vault ($1.99)</strong> and get lifetime access to all 10 genre packs!</p>
<p>👉 <a href="https://gameverseaudio.gumroad.com/l/game-asset-vault"><strong>Unlock The Complete 10-Pack Vault for just $1.99!</strong></a></p>
"""

REMAINING = [
    {
        "num": "08",
        "slug": "crafting-materials-ores-pack",
        "name": "08 // Crafting Materials & Ores Pack (2D Game Assets)",
        "folder": VAULT_DIR / "08_Crafting_Materials_Ores",
        "zip_name": "08_Crafting_Materials_Ores_Pack.zip",
        "summary": "8 essential crafting materials, ingots & monster drops (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>⚒️ <strong>08 // Crafting Materials &amp; Ores Pack (2D Game Assets)</strong></p>
<p>Build your game's crafting economy and gathering systems with 8 high-detail resource sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Crafting Materials &amp; Ores:</strong> Raw Gold Ore Nugget, Mithril Crystal Ore, Dark Iron Ingot Stack, Dragon Scale Leather Hide, Luminous Fairy Dust Jar, Ancient Beast Horn, Giant Spider Silk Spool, Elemental Magma Coal</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "09",
        "slug": "rings-amulets-jewelry-pack",
        "name": "09 // Rings, Amulets & Talismans Pack (2D Game Assets)",
        "folder": VAULT_DIR / "09_Rings_Amulets_Jewelry",
        "zip_name": "09_Rings_Amulets_Jewelry_Pack.zip",
        "summary": "8 enchanted rings, necklaces & mystic talismans (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>💍 <strong>09 // Rings, Amulets &amp; Talismans Pack (2D Game Assets)</strong></p>
<p>Equip your accessory and relic slots with 8 intricately crafted jewelry and talisman sprites!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Rings, Amulets &amp; Talismans:</strong> Lion Signet Ruby Ring, Dragon Claw Sapphire Ring, Dragon Eye Medallion Amulet, Celtic Trinity Knot Talisman, Elven Emerald Leaf Brooch, Star of Eternity Necklace, Dwarven Warrior Torc, Gothic Skull Knuckle Ring</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    },
    {
        "num": "10",
        "slug": "dark-magic-necromancy-pack",
        "name": "10 // Dark Magic & Cursed Relics Pack (2D Game Assets)",
        "folder": VAULT_DIR / "10_Dark_Magic_Necromancy",
        "zip_name": "10_Dark_Magic_Necromancy_Pack.zip",
        "summary": "8 sinister dark magic, occult & cursed relics (512x512 + 1024x1024). Commercial license included.",
        "desc": """<p>💀 <strong>10 // Dark Magic &amp; Cursed Relics Pack (2D Game Assets)</strong></p>
<p>Channel the forbidden arts with 8 dark occult relics, sacrificial blades, and cursed artifacts!</p>
<hr>
<h3>📦 What's Included:</h3>
<p>• <strong>8 Dark Magic &amp; Cursed Relics:</strong> Cursed Voodoo Effigy, Sacrificial Bone Dagger, Trapped Soul Lantern, Occult Pentagram Scrying Orb, Mummified Demon Finger Relic, Raven Skull Occult Fetish, Bubbling Witch Cauldron, Blood Demon Pact Scroll</p>
<p>• <strong>100% Clean Alpha Transparency</strong> + <strong>512x512 &amp; 1024x1024 Masters</strong>.</p>
<hr>
<h3>📜 Commercial License Terms:</h3>
<p>✅ 100% Commercial Use | ✅ Modify &amp; Adapt | ✅ Royalty-Free (Attribution Optional)</p>
""" + UPGRADE_BOX
    }
]

for item in REMAINING:
    slug = item["slug"]
    name = item["name"]
    zip_path = item["folder"] / item["zip_name"]
    cover_path = item["folder"] / "showcase_preview.png"
    thumb_path = item["folder"] / "thumbnail_square.png"
    
    print(f"\n🚀 [{item['num']}/10] 作成・公開開始: {name}...")
    
    # 1. 新規商品作成 (Gumroad CLI products create)
    # create 時に --json 出力させれば ID が直取れるか確認、なければ --all で探す
    res_c = subprocess.run([
        GUMROAD_CLI, "products", "create",
        "--name", name,
        "--currency", "usd",
        "--price", "0.99",
        "--json"
    ], env=env, capture_output=True, text=True)
    
    target_id = None
    if res_c.returncode == 0:
        try:
            c_data = json.loads(res_c.stdout)
            target_id = c_data.get("product", {}).get("id")
        except Exception:
            pass
            
    if not target_id:
        # --all で探す
        res_list = subprocess.run([GUMROAD_CLI, "products", "list", "--all", "--json"], env=env, capture_output=True, text=True)
        if res_list.returncode == 0:
            for p in json.loads(res_list.stdout).get("products", []):
                if p.get("name") == name or p.get("custom_permalink") == slug:
                    target_id = p.get("id")
                    break
                    
    if not target_id:
        print(f"❌ IDの取得に失敗しました: {name}")
        continue
        
    print(f"  ✓ ID取得成功: {target_id}。詳細・アセット設定中...")
    
    up_cmd = [
        GUMROAD_CLI, "products", "update", target_id,
        "--name", name,
        "--custom-permalink", slug,
        "--currency", "usd",
        "--price", "0.99",
        "--suggested-price", "1.99",
        "--pay-what-you-want",
        "--description", item["desc"],
        "--custom-summary", item["summary"],
        "--cover-image", str(cover_path),
        "--thumbnail", str(thumb_path),
        "--file", str(zip_path),
        "--file-name", item["zip_name"]
    ]
    subprocess.run(up_cmd, env=env, capture_output=True)
    
    # 公開
    subprocess.run([GUMROAD_CLI, "products", "publish", target_id], env=env, capture_output=True)
    
    # Rich Content を新ZIPのみに更新
    res_view = subprocess.run([GUMROAD_CLI, "products", "view", target_id, "--json"], env=env, capture_output=True, text=True)
    if res_view.returncode == 0:
        p_info = json.loads(res_view.stdout).get("product", {})
        files = p_info.get("files", [])
        matched = [f for f in files if f.get("name") == item["zip_name"]]
        if matched:
            fid = matched[-1].get("id")
            rc = [{
                "id": "page_1",
                "page_id": "page_1",
                "title": name,
                "description": {
                    "type": "doc",
                    "content": [
                        {
                            "type": "fileEmbed",
                            "attrs": {"id": fid, "uid": None, "collapsed": False}
                        }
                    ]
                }
            }]
            tmp_rc = item["folder"] / f"rc_{slug}.json"
            with open(tmp_rc, "w") as f:
                json.dump(rc, f)
            subprocess.run([GUMROAD_CLI, "products", "content", "set", target_id, str(tmp_rc), "--yes"], env=env, capture_output=True)
            if tmp_rc.exists():
                tmp_rc.unlink()
    
    print(f"  ✅ 出品・公開完了: https://gameverseaudio.gumroad.com/l/{slug}")

print("\n🎉 08, 09, 10 のデプロイ完了！")
