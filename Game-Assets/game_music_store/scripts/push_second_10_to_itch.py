#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Music")
BUTLER_BIN = str(BASE_DIR / "bin" / "butler")
OUTPUT_DIR = BASE_DIR / "output"

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
    ("steps-of-a-forgotten-god", OUTPUT_DIR / "gumroad_steps-of-a-forgotten-god/Steps of a Forgotten God_Commercial_Audio_Pack.zip"),
    ("the-titans-heavy-march", OUTPUT_DIR / "gumroad_the-titans-heavy-march/The Titan's Heavy March_Commercial_Audio_Pack.zip"),
    ("iron-kneeling-in-the-dark", OUTPUT_DIR / "gumroad_iron-kneeling-in-the-dark/Iron Kneeling in the Dark_Commercial_Audio_Pack.zip"),
    ("hammer-against-the-gate", OUTPUT_DIR / "gumroad_hammer-against-the-gate/Hammer Against the Gate_Commercial_Audio_Pack.zip"),
    ("cold-iron-march", OUTPUT_DIR / "gumroad_cold-iron-march/Cold Iron March_Commercial_Audio_Pack.zip"),
    ("the-sovereigns-last-breath", OUTPUT_DIR / "gumroad_the-sovereigns-last-breath/The Sovereign's Last Breath_Commercial_Audio_Pack.zip"),
    ("throne-of-ash", OUTPUT_DIR / "gumroad_throne-of-ash/Throne of Ash_Commercial_Audio_Pack.zip"),
    ("the-weight-of-iron", OUTPUT_DIR / "gumroad_the-weight-of-iron/The Weight of Iron_Commercial_Audio_Pack.zip"),
    ("steps-of-the-frost-titan", OUTPUT_DIR / "gumroad_steps-of-the-frost-titan/Steps of the Frost Titan_Commercial_Audio_Pack.zip"),
    ("the-last-siege-of-kings", OUTPUT_DIR / "gumroad_the-last-siege-of-kings/The Last Siege of Kings_Commercial_Audio_Pack.zip"),
]

print("🚀 Pushing newly built 10 tracks to itch.io (gameverse-audio/dark-fantasy-boss-battle-pack)...")
for channel, zip_path in TRACKS:
    if not zip_path.exists():
        print(f"❌ ファイルが存在しません: {zip_path}")
        sys.exit(1)
    target = f"gameverse-audio/dark-fantasy-boss-battle-pack:{channel}"
    res = subprocess.run([BUTLER_BIN, "push", str(zip_path), target], env=env, text=True, capture_output=True)
    if res.returncode == 0:
        print(f"  ✅ {channel}: Success")
    else:
        print(f"  ❌ {channel}: Failed ({res.stderr.strip()})")
print("🎉 itch.io deployment of 10 tracks finished.")
