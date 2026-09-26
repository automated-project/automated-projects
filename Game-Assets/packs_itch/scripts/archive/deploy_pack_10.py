#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
deploy_pack_10.py
Gumroadの1日作成枠リセット後に実行する、10個目の単品パック出品スクリプト
10 // Dark Magic & Cursed Relics Pack ($0.99)
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

item = {
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

print("🚀 10個目の単品商品作成中...")
res_c = subprocess.run([
    GUMROAD_CLI, "products", "create",
    "--name", item["name"],
    "--currency", "usd",
    "--price", "0.99"
], env=env, capture_output=True, text=True)

if res_c.returncode != 0:
    print(f"❌ 作成失敗（まだ制限中の可能性があります）: {res_c.stderr}")
    sys.exit(1)

# ID取得
res_l = subprocess.run([GUMROAD_CLI, "products", "list", "--all", "--json"], env=env, capture_output=True, text=True)
target_id = None
for p in json.loads(res_l.stdout).get("products", []):
    if p.get("name") == item["name"]:
        target_id = p.get("id")
        break

if not target_id:
    print("❌ ID特定失敗")
    sys.exit(1)

# 更新 & 公開
up_cmd = [
    GUMROAD_CLI, "products", "update", target_id,
    "--name", item["name"],
    "--custom-permalink", item["slug"],
    "--currency", "usd",
    "--price", "0.99",
    "--suggested-price", "1.99",
    "--pay-what-you-want",
    "--description", item["desc"],
    "--custom-summary", item["summary"],
    "--cover-image", str(item["folder"] / "showcase_preview.png"),
    "--thumbnail", str(item["folder"] / "thumbnail_square.png"),
    "--file", str(item["folder"] / item["zip_name"]),
    "--file-name", item["zip_name"]
]
subprocess.run(up_cmd, env=env, capture_output=True)
subprocess.run([GUMROAD_CLI, "products", "publish", target_id], env=env, capture_output=True)

# Rich Content
res_view = subprocess.run([GUMROAD_CLI, "products", "view", target_id, "--json"], env=env, capture_output=True, text=True)
p_info = json.loads(res_view.stdout).get("product", {})
matched = [f for f in p_info.get("files", []) if f.get("name") == item["zip_name"]]
if matched:
    fid = matched[-1].get("id")
    rc = [{
        "id": "page_1",
        "page_id": "page_1",
        "title": item["name"],
        "description": {
            "type": "doc",
            "content": [{"type": "fileEmbed", "attrs": {"id": fid, "uid": None, "collapsed": False}}]
        }
    }]
    tmp_rc = item["folder"] / "rc_10.json"
    with open(tmp_rc, "w") as f:
        json.dump(rc, f)
    subprocess.run([GUMROAD_CLI, "products", "content", "set", target_id, str(tmp_rc), "--yes"], env=env, capture_output=True)
    if tmp_rc.exists():
        tmp_rc.unlink()

print(f"✅ 10個目の単品商品出品完了: https://gameverseaudio.gumroad.com/l/{item['slug']}")
