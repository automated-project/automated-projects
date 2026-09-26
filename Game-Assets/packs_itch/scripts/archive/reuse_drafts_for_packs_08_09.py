#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
reuse_drafts_for_packs_08_09.py
未公開の下書き2枠を再利用して、Gumroadに 08 と 09 の個別パックを出品・公開するスクリプト
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

REUSE_ITEMS = [
    {
        "target_id": "RBGzqfoqGO20yHvBasOSQA==",
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
        "target_id": "auAovqpLd2JrQFOCg2zwWw==",
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
    }
]

for item in REUSE_ITEMS:
    target_id = item["target_id"]
    slug = item["slug"]
    name = item["name"]
    zip_path = item["folder"] / item["zip_name"]
    cover_path = item["folder"] / "showcase_preview.png"
    thumb_path = item["folder"] / "thumbnail_square.png"
    
    print(f"\n🚀 [{item['num']}/10] 下書き枠再利用更新中: {name} (ID: {target_id})...")
    
    update_cmd = [
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
    res_up = subprocess.run(update_cmd, env=env, capture_output=True, text=True)
    if res_up.returncode != 0:
        print(f"  ⚠️ update出力: {res_up.stderr}")
    else:
        print(f"  ✓ 基本情報・メディア更新成功")
        
    # 公開
    res_pub = subprocess.run([GUMROAD_CLI, "products", "publish", target_id], env=env, capture_output=True, text=True)
    if res_pub.returncode == 0:
        print("  ✓ 公開 (publish) 成功")
    else:
        print(f"  ⚠️ publish警告: {res_pub.stderr}")
        
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

print("\n🎉 08 と 09 の再利用出品がすべて完了しました！")
