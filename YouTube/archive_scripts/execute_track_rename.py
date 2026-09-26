# -*- coding: utf-8 -*-
"""
03_Uplifting_Channel/raw_audio/1hour-mix の音源ファイル名および曲名の完全一意化・重複排除・リネーム実行スクリプト
"""
import shutil
from pathlib import Path

mix_dir = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/raw_audio/1hour-mix")
backup_dir = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/raw_audio/1hour-mix_backup")

# 1. 念のためバックアップを作成
if not backup_dir.exists():
    shutil.copytree(mix_dir, backup_dir)
    print(f"✅ Created backup at {backup_dir}")

# 2. リネームマッピング定義（曲名の被り・類似・季節ワードを完全に解消し、洗練されたユニークな曲名へ）
rename_map = {
    # Amber_Flame は Amber_Horizon と同一曲のため、Amber_Flame を Amber_Horizon_Duplicate.mp4 に退避・除外
    "Amber_Flame.mp4": "_ARCHIVE_Amber_Flame_Duplicate_of_Amber_Horizon.mp4",
    "Amber_Horizon.mp4": "Amber_Horizon.mp4", # そのまま保持
    
    # 季節ワード排除 & 類似曲名の差別化
    "Healed_by_Summer_Light.mp4": "Healed_By_Golden_Light.mp4",
    
    # Chasing シリーズの差別化
    "Chasing_After_Endless_Light.mp4": "Endless_Sky_Radiance.mp4",
    "Chasing_Endless_Daylight.mp4": "Daylight_Anthem.mp4",
    "Chasing_the_Infinite.mp4": "Infinite_Horizons.mp4",
    
    # Weightless シリーズの差別化
    "Weightless_In_Gold.mp4": "Golden_Euphoria.mp4",
    "Weightless_In_The_Sun.mp4": "Sunlit_Atmosphere.mp4",
    "Weightless_at_Last.mp4": "Weightless_Ascent.mp4",
    
    # Salt シリーズの差別化
    "Salt_and_Sunlight.mp4": "Crystal_Ocean_Breeze.mp4",
    "Salt_in_Our_Hair.mp4": "Ocean_Drift_Melody.mp4",
    
    # Golden / Sun シリーズの差別化
    "Kissing_the_Golden_Sun.mp4": "Golden_Sun_Embrace.mp4",
    "Sun_Above.mp4": "High_Above_The_Clouds.mp4",
    "The_Golden_Door.mp4": "Gateway_To_Light.mp4",
    "Golden_Hour_Traces.mp4": "Golden_Hour_Echoes.mp4",
    "Golden_Motion.mp4": "Pure_Motion_Pulse.mp4",
    "Brighter_Than_The_Sun.mp4": "Brighter_Than_Starlight.mp4",
    
    # Morning / Star / Gravity / Frame シリーズの明確化
    "Broken_Glass_Mornings.mp4": "Crystal_Morning_Light.mp4",
    "Burning_Like_Stars.mp4": "Starlight_Burning_Bright.mp4",
    "Beyond_The_Heavy_Ground.mp4": "Beyond_The_Horizon.mp4",
    "Breaking_Past_Gravity.mp4": "Zero_Gravity_Drive.mp4",
    "Hands_Turn_Slowly.mp4": "Timeless_Moment.mp4",
    "Hold_on_to_the_Night.mp4": "Hold_The_Starlit_Night.mp4",
    "Midnight_Afterglow.mp4": "Midnight_Glow_Pulse.mp4",
    "Tear_the_Sky.mp4": "Tear_The_Clouds.mp4",
    "The_Chair_By_The_Door.mp4": "Echoes_By_The_Door.mp4",
    "Wait_for_the_Motion.mp4": "Waiting_For_The_Rush.mp4",
    "A_Thousand_Frames.mp4": "A_Thousand_Memories.mp4"
}

print("\n=== Executing Track Renaming ===")
for old_name, new_name in rename_map.items():
    old_file = mix_dir / old_name
    new_file = mix_dir / new_name
    if old_file.exists():
        if old_name != new_name:
            old_file.rename(new_file)
            print(f"Renamed: {old_name:<35} -> {new_name}")
    else:
        if new_file.exists():
            print(f"Already Renamed: {new_name}")
        else:
            print(f"⚠️ File not found: {old_name}")

print("\n=== Current Active Audio Files in 1hour-mix ===")
active_files = sorted([f for f in mix_dir.iterdir() if f.is_file() and not f.name.startswith("_") and f.suffix == ".mp4"])
for i, f in enumerate(active_files, 1):
    print(f"[{i:02d}] {f.name}")

print(f"\nTotal Active Unique Tracks: {len(active_files)}")
