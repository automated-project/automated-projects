# -*- coding: utf-8 -*-
"""
Ch 2 (Phonk / Gym EDM) の全54曲に対する一意で差別化された新曲名マッピングの定義と検証スクリプト
"""
from pathlib import Path

# 全54トラックの旧名 -> 新名マッピング
rename_map = {
    # --- 1. raw_audio (ルート32曲) ---
    "Asfalto_em_Chamas.mp4": "Flames_Of_Asphalt.mp4",
    "Asphalt_Siege.mp4": "Tokyo_Underground_Siege.mp4",
    "Blacktop_Havoc.mp4": "Tarmac_Havoc.mp4",
    "Colossal_Grid.mp4": "Titan_Grid_Protocol.mp4",
    "Concrete_Command.mp4": "Overlord_Command.mp4",
    "Concrete_Predator.mp4": "Urban_Predator.mp4",
    "Crimson_Surge.mp4": "Crimson_Overdrive.mp4",
    "Dead_Heat.mp4": "Dead_Heat_Lock.mp4",
    "Gravity_Crush.mp4": "Sub_Zero_Crush.mp4",
    "Grip_Locked_Hard.mp4": "Apex_Drift_Lock.mp4",
    "Heart_Is_A_Weapon.mp4": "Heart_Of_The_Warrior.mp4",
    "Heavy_Steel_Rain.mp4": "Heavy_Metal_Rain.mp4",
    "Iron_Clenched.mp4": "Titanium_Fist.mp4",
    "Iron_Impact.mp4": "Brutal_Kinetic_Impact.mp4",
    "Iron_Jaw_Arena.mp4": "Colosseum_Of_Iron.mp4",
    "Iron_Payload.mp4": "Heavyweight_Payload.mp4",
    "Midnight_Apex.mp4": "Neon_Apex_Drifter.mp4",
    "Midnight_Tarmac.mp4": "Midnight_Highway_Run.mp4",
    "Midnight_Velocity.mp4": "Infinite_Velocity.mp4",
    "Molten_Colossus.mp4": "Molten_Core_Rage.mp4",
    "Prism_Velocity.mp4": "Cyber_Prism_Overclock.mp4",
    "Redline_Ambition.mp4": "Unstoppable_Ambition.mp4",
    "Redline_Pursuit.mp4": "High_Speed_Pursuit.mp4",
    "Stadium_Burn.mp4": "Arena_Burnout.mp4",
    "Tarmac_Predator.mp4": "Shadow_Predator_808.mp4",
    "Tarmac_Vise.mp4": "Steel_Vise_Grip.mp4",
    "Teeth_On_The_Steel.mp4": "Blade_Against_Steel.mp4",
    "The_Iron_Crown.mp4": "Crown_Of_Defiance.mp4",
    "The_Rotating_Monolith.mp4": "Monolith_Resonance.mp4",
    "Violent_Traction.mp4": "Aggressive_Torque.mp4",
    "We_Are_The_Fire.mp4": "Ignite_The_Rage.mp4",
    "White_Knuckle_Grip.mp4": "Death_Grip_Momentum.mp4",

    # --- 2. best-edm (サブフォルダ22曲) ---
    "best-edm/Asphalt_Bite.mp4": "best-edm/Asphalt_Fang_Strike.mp4",
    "best-edm/Asphalt_Fang.mp4": "best-edm/Venom_On_Asphalt.mp4",
    "best-edm/Asphalt_Reaper.mp4": "best-edm/Grim_Asphalt_Reaper.mp4",
    "best-edm/Asphalt_Redline.mp4": "best-edm/Night_Drift_Redline.mp4",
    "best-edm/Asphalt_Takedown.mp4": "best-edm/Brutal_Takedown.mp4",
    "best-edm/Asphalt_Teeth.mp4": "best-edm/Street_Teeth.mp4",
    "best-edm/Asphalt_Vise.mp4": "best-edm/Hydraulic_Vise.mp4",
    "best-edm/Blacktop_Fury.mp4": "best-edm/Blacktop_Overdrive.mp4",
    "best-edm/Concrete_Pursuit.mp4": "best-edm/Concrete_Chaser.mp4",
    "best-edm/Create_an_ultra_aggressive_dri.mp4": "best-edm/Tokyo_Drift_Rage.mp4",
    "best-edm/Crush_The_Bone.mp4": "best-edm/Bonecrusher_Phonk.mp4",
    "best-edm/Kingdom_Of_My_Own.mp4": "best-edm/Kingdom_Of_Shadows.mp4",
    "best-edm/Midnight_Asphalt.mp4": "best-edm/Dark_Midnight_Cruise.mp4",
    "best-edm/Midnight_Asphalt_Burn.mp4": "best-edm/Asphalt_Burnout_808.mp4",
    "best-edm/Midnight_Redline.mp4": "best-edm/Midnight_Tachometer.mp4",
    "best-edm/Redline_Impact.mp4": "best-edm/Full_Throttle_Impact.mp4",
    "best-edm/Redline_Pressure.mp4": "best-edm/Boost_Pressure_Max.mp4",
    "best-edm/Redline_Torque.mp4": "best-edm/Maximum_Torque_RPM.mp4",
    "best-edm/Savage_Grip.mp4": "best-edm/Savage_Tire_Grip.mp4",
    "best-edm/Storming_the_Gate.mp4": "best-edm/Storming_The_Gates.mp4",
    "best-edm/Tarmac_Teeth.mp4": "best-edm/Serrated_Tarmac.mp4",
    "best-edm/The_Iron_Ascent.mp4": "best-edm/Iron_Ascension.mp4"
}

# 1. 一意性の検証
all_new_names = [Path(v).name for v in rename_map.values()]
assert len(all_new_names) == len(set(all_new_names)), f"Duplicates in new names: {len(all_new_names)} vs {len(set(all_new_names))}"
print(f"✅ Verified: All {len(all_new_names)} new track names are 100% UNIQUE!")

# 2. 表示
print("\n" + "="*80)
print(f"{'#':<3} | {'Original File Name':<38} -> {'New Unique Track Name'}")
print("="*80)
for i, (old_p, new_p) in enumerate(rename_map.items(), 1):
    print(f"[{i:02d}] {old_p:<38} -> {new_p}")
