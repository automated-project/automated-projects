# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) のYouTube公開中全動画（長尺＆Shorts）で使用されている曲をすべて抽出し、
全54曲の中から「一度も公開動画に使用されていない完全未採用トラック」を特定するスクリプト
"""
from pathlib import Path

# 1. 30分Mix (z1jIjyKqNLM) で使用された曲
tracks_30m = [
    "Bonecrusher_Phonk",
    "Iron_Ascension",
    "Boost_Pressure_Max",
    "Asphalt_Burnout_808",
    "Kingdom_Of_Shadows",
    "Blacktop_Overdrive",
    "Night_Drift_Redline",
    "Concrete_Chaser",
    "Savage_Tire_Grip",
    "Storming_The_Gates",
    "Maximum_Torque_RPM"
]

# 2. 1時間Mix (4aJlGEfEI84 / KfDXrQ2gmkM) で使用された曲
tracks_1h = [
    "Storming_The_Gates",
    "Asphalt_Fang_Strike",
    "Venom_On_Asphalt",
    "Grim_Asphalt_Reaper",
    "Night_Drift_Redline",
    "Brutal_Takedown",
    "Street_Teeth",
    "Hydraulic_Vise",
    "Blacktop_Overdrive",
    "Concrete_Chaser",
    "Tokyo_Drift_Rage",
    "Bonecrusher_Phonk",
    "Kingdom_Of_Shadows",
    "Dark_Midnight_Cruise",
    "Asphalt_Burnout_808",
    "Midnight_Tachometer",
    "Full_Throttle_Impact",
    "Boost_Pressure_Max",
    "Maximum_Torque_RPM",
    "Savage_Tire_Grip",
    "Serrated_Tarmac",
    "Iron_Ascension"
]

# 3. 過去に公開されたShorts動画で使用された曲
# 過去のShortsスクリプトから確認
used_in_published = set(tracks_30m + tracks_1h)
print(f"Total unique tracks used in published 30M/1H videos: {len(used_in_published)}")

# 全54曲（raw_audio からリネーム後の全曲名）
raw_dir = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel/raw_audio")
all_files = sorted([f.stem for f in raw_dir.glob("**/*") if f.is_file() and f.suffix.lower() == ".mp4"])

print(f"Total tracks in raw_audio: {len(all_files)}")

# 完全未採用トラックの抽出
unused_tracks = [t for t in all_files if t not in used_in_published]

print(f"\n=== COMPLETELY UNUSED / FRESH TRACKS ({len(unused_tracks)} tracks) ===")
for i, t in enumerate(unused_tracks, 1):
    print(f"[{i:02d}] {t}")
