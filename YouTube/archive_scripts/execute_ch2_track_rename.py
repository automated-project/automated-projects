# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) の全音源ファイル（raw_audio, mastered_audio, extracted_audio）を一括リネーム・同期するスクリプト
"""
import shutil
from pathlib import Path

base_dir = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")

# 1. バックアップ作成
for folder in ["raw_audio", "mastered_audio", "extracted_audio"]:
    src = base_dir / folder
    dst = base_dir / f"{folder}_backup"
    if src.exists() and not dst.exists():
        shutil.copytree(src, dst)
        print(f"✅ Created backup for {folder} at {dst}")

# 2. リネームマッピング（ベース名対応）
# 旧ベース名 -> 新ベース名
stem_map = {
    "Asfalto_em_Chamas": "Flames_Of_Asphalt",
    "Asphalt_Siege": "Tokyo_Underground_Siege",
    "Blacktop_Havoc": "Tarmac_Havoc",
    "Colossal_Grid": "Titan_Grid_Protocol",
    "Concrete_Command": "Overlord_Command",
    "Concrete_Predator": "Urban_Predator",
    "Crimson_Surge": "Crimson_Overdrive",
    "Dead_Heat": "Dead_Heat_Lock",
    "Gravity_Crush": "Sub_Zero_Crush",
    "Grip_Locked_Hard": "Apex_Drift_Lock",
    "Heart_Is_A_Weapon": "Heart_Of_The_Warrior",
    "Heavy_Steel_Rain": "Heavy_Metal_Rain",
    "Iron_Clenched": "Titanium_Fist",
    "Iron_Impact": "Brutal_Kinetic_Impact",
    "Iron_Jaw_Arena": "Colosseum_Of_Iron",
    "Iron_Payload": "Heavyweight_Payload",
    "Midnight_Apex": "Neon_Apex_Drifter",
    "Midnight_Tarmac": "Midnight_Highway_Run",
    "Midnight_Velocity": "Infinite_Velocity",
    "Molten_Colossus": "Molten_Core_Rage",
    "Prism_Velocity": "Cyber_Prism_Overclock",
    "Redline_Ambition": "Unstoppable_Ambition",
    "Redline_Pursuit": "High_Speed_Pursuit",
    "Stadium_Burn": "Arena_Burnout",
    "Tarmac_Predator": "Shadow_Predator_808",
    "Tarmac_Vise": "Steel_Vise_Grip",
    "Teeth_On_The_Steel": "Blade_Against_Steel",
    "The_Iron_Crown": "Crown_Of_Defiance",
    "The_Rotating_Monolith": "Monolith_Resonance",
    "Violent_Traction": "Aggressive_Torque",
    "We_Are_The_Fire": "Ignite_The_Rage",
    "White_Knuckle_Grip": "Death_Grip_Momentum",
    
    "Asphalt_Bite": "Asphalt_Fang_Strike",
    "Asphalt_Fang": "Venom_On_Asphalt",
    "Asphalt_Reaper": "Grim_Asphalt_Reaper",
    "Asphalt_Redline": "Night_Drift_Redline",
    "Asphalt_Takedown": "Brutal_Takedown",
    "Asphalt_Teeth": "Street_Teeth",
    "Asphalt_Vise": "Hydraulic_Vise",
    "Blacktop_Fury": "Blacktop_Overdrive",
    "Concrete_Pursuit": "Concrete_Chaser",
    "Create_an_ultra_aggressive_dri": "Tokyo_Drift_Rage",
    "Crush_The_Bone": "Bonecrusher_Phonk",
    "Kingdom_Of_My_Own": "Kingdom_Of_Shadows",
    "Midnight_Asphalt": "Dark_Midnight_Cruise",
    "Midnight_Asphalt_Burn": "Asphalt_Burnout_808",
    "Midnight_Redline": "Midnight_Tachometer",
    "Redline_Impact": "Full_Throttle_Impact",
    "Redline_Pressure": "Boost_Pressure_Max",
    "Redline_Torque": "Maximum_Torque_RPM",
    "Savage_Grip": "Savage_Tire_Grip",
    "Storming_the_Gate": "Storming_The_Gates",
    "Storming_The_Gate": "Storming_The_Gates",
    "Tarmac_Teeth": "Serrated_Tarmac",
    "The_Iron_Ascent": "Iron_Ascension",
    "Asphalt_Claw": "Asphalt_Claw_Strike"
}

# 3. 各フォルダ内のファイルをリネーム
renamed_count = 0
for folder in ["raw_audio", "mastered_audio", "extracted_audio"]:
    target_dir = base_dir / folder
    if not target_dir.exists():
        continue
    for f in list(target_dir.glob("**/*")):
        if not f.is_file():
            continue
        old_stem = f.stem
        ext = f.suffix
        if old_stem in stem_map:
            new_stem = stem_map[old_stem]
            new_file = f.parent / f"{new_stem}{ext}"
            if f != new_file:
                f.rename(new_file)
                renamed_count += 1
                # print(f"Renamed ({folder}): {f.name} -> {new_file.name}")

print(f"🎉 Successfully renamed {renamed_count} files across all Ch2 audio directories!")
