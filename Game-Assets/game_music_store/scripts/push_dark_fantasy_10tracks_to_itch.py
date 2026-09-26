#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
push_dark_fantasy_10tracks_to_itch.py
Gumroadと完全一致する「ダークファンタジー有料専用10曲」を itch.io にプッシュ
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
BUTLER_BIN = str(BASE_DIR / "bin" / "butler")

env = os.environ.copy()
env_path = BASE_DIR / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k] = v.strip("\"'")

TRACKS = [
    {
        "channel": "god-of-ruin",
        "zip": BASE_DIR / "tracks/2026-09-09/Track05_God_of_Ruin/gumroad_god-of-ruin/God_of_Ruin_Commercial_Audio_Pack.zip",
        "title": "God of Ruin"
    },
    {
        "channel": "the-iron-ticking",
        "zip": BASE_DIR / "output/gumroad_the-iron-ticking/The_Iron_Ticking_Commercial_Audio_Pack.zip",
        "title": "The Iron Ticking"
    },
    {
        "channel": "summa-dies-advenit",
        "zip": BASE_DIR / "output/gumroad_summa-dies-advenit/Summa_Dies_Advenit_Commercial_Audio_Pack.zip",
        "title": "Summa Dies Advenit"
    },
    {
        "channel": "beneath-the-weeping-boughs",
        "zip": BASE_DIR / "output/gumroad_beneath-the-weeping-boughs/Beneath_the_Weeping_Boughs_Commercial_Audio_Pack.zip",
        "title": "Beneath the Weeping Boughs"
    },
    {
        "channel": "crown-of-iron",
        "zip": BASE_DIR / "output/gumroad_crown-of-iron/Crown_of_Iron_Commercial_Audio_Pack.zip",
        "title": "Crown of Iron"
    },
    {
        "channel": "crown-of-cinders",
        "zip": BASE_DIR / "output/gumroad_crown-of-cinders/Crown_of_Cinders_Commercial_Audio_Pack.zip",
        "title": "Crown of Cinders"
    },
    {
        "channel": "crown-of-bleeding-iron",
        "zip": BASE_DIR / "output/gumroad_crown-of-bleeding-iron/Crown_of_Bleeding_Iron_Commercial_Audio_Pack.zip",
        "title": "Crown of Bleeding Iron"
    },
    {
        "channel": "bloodline-of-the-eclipse",
        "zip": BASE_DIR / "output/gumroad_bloodline-of-the-eclipse/Bloodline_of_the_Eclipse_Commercial_Audio_Pack.zip",
        "title": "Bloodline of the Eclipse"
    },
    {
        "channel": "hammer-of-the-fallen",
        "zip": BASE_DIR / "output/gumroad_hammer-of-the-fallen/Hammer_of_the_Fallen_Commercial_Audio_Pack.zip",
        "title": "Hammer of the Fallen"
    },
    {
        "channel": "hammer-of-the-stone-king",
        "zip": BASE_DIR / "output/gumroad_hammer-of-the-stone-king/Hammer_of_the_Stone_King_Commercial_Audio_Pack.zip",
        "title": "Hammer of the Stone King"
    },
]

print("============================================================")
print("⚔️ Epic Dark Fantasy 10 Tracks ➔ itch.io Butler Sync")
print("Target: gameverse-audio/dark-fantasy-boss-battle-pack")
print("============================================================")

for t in TRACKS:
    zip_path = t["zip"]
    if not zip_path.exists():
        print(f"❌ ファイルが存在しません: {zip_path}")
        continue
    target = f"gameverse-audio/dark-fantasy-boss-battle-pack:{t['channel']}"
    print(f"\n🚀 Pushing {t['title']} to {target}...")
    res = subprocess.run([BUTLER_BIN, "push", str(zip_path), target], env=env, text=True, capture_output=True)
    if res.returncode == 0:
        print(f"  ✅ {t['channel']}: Success")
    else:
        print(f"  ❌ {t['channel']}: Failed ({res.stderr.strip()})")

print("\n🎉 全10曲のitch.ioデプロイが完了しました！")
