#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects")
MUSIC_DIR = BASE_DIR / "Game-Music"
ASSETS_DIR = BASE_DIR / "Game-Assets"
OUTPUTS_DIR = ASSETS_DIR / "outputs"

BUTLER_BIN = str(MUSIC_DIR / "bin" / "butler")
api_key = "lIqgRvCN1y0XSzDtRX2cEcNGU0arb4LwTUT0XnJn"

paid_bgm_dir = OUTPUTS_DIR / "Paid_Bonus_Music_Loops"
paid_bgm_dir.mkdir(parents=True, exist_ok=True)

wav_sources = [
    ("Track01_Wrath_of_the_Abyss", MUSIC_DIR / "tracks/2026-09-08/Track01_Wrath_of_the_Abyss/gumroad_wrath_of_the_abyss"),
    ("Track02_Neon_Overdrive", MUSIC_DIR / "tracks/2026-09-08/Track02_Neon_Overdrive/gumroad_neon_overdrive"),
    ("Track03_Requiem_of_the_Fallen", MUSIC_DIR / "tracks/2026-09-08/Track03_Requiem_of_the_Fallen/gumroad_requiem_of_the_fallen"),
    ("Track05_God_of_Ruin", MUSIC_DIR / "tracks/2026-09-09/Track05_God_of_Ruin/gumroad_god-of-ruin"),
    ("Track06_Cyber_Nemesis", MUSIC_DIR / "tracks/2026-09-09/Track06_Cyber_Nemesis/gumroad_cyber-nemesis")
]

paid_zip = paid_bgm_dir / "Bonus_Commercial_Game_Music_and_Seamless_Loops_Collection.zip"
with zipfile.ZipFile(paid_zip, "w", zipfile.ZIP_DEFLATED) as zf:
    for track_name, wdir in wav_sources:
        if wdir.exists():
            for f in wdir.glob("*.*"):
                if f.suffix in [".wav", ".mp3", ".png", ".txt"]:
                    zf.write(f, f"Bonus_Music_Collection/{track_name}/{f.name}")

print(f"✅ 有料版用BGM＆シームレスループパック（サブフォルダ構造）準備完了: {paid_zip.name}")

env = os.environ.copy()
env["BUTLER_API_KEY"] = api_key

print("\n📤 game-asset-vault に有料BGM＆シームレスループデプロイ中...")
cmd_paid = [
    BUTLER_BIN, "push",
    str(paid_zip),
    "gameverse-audio/game-asset-vault:bonus-commercial-music-loops",
    "--userversion=1.0.0"
]
res_paid = subprocess.run(cmd_paid, env=env, capture_output=True, text=True)
print("Butler Output (Paid):", res_paid.stdout)
if res_paid.returncode == 0:
    print("✅ 有料版 Vault へのBGM特典パック並列デプロイが成功しました！")
else:
    print("Error:", res_paid.stderr)
