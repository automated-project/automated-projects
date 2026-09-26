#!/usr/bin/env python3
import os, subprocess, sys
from pathlib import Path

BASE_DIR = Path('/Users/base/Automated-Projects/Game-Music')
env_file = BASE_DIR / '.env'
env = os.environ.copy()
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k] = v.strip('"\'')

BUTLER_BIN = str(BASE_DIR / 'bin' / 'butler')
VAULT_DIR = Path('/Users/base/Automated-Projects/Game-Assets/outputs/Paid_Vault_10Packs')

PACKS = [
    ('01-fantasy-weapons', '01_Fantasy_Weapons/01_Fantasy_Weapons_Pack.zip'),
    ('02-mythic-armor-helmets', '02_Mythic_Armor_Helmets/02_Mythic_Armor_Helmets_Pack.zip'),
    ('03-cyberpunk-scifi-hud-ui', '03_Cyberpunk_SciFi_HUD_UI/03_Cyberpunk_SciFi_HUD_UI_Pack.zip'),
    ('04-gemstones-crystals', '04_Gemstones_Crystals/04_Gemstones_Crystals_Pack.zip'),
    ('05-spellbooks-tomes', '05_Spellbooks_Tomes/05_Spellbooks_Tomes_Pack.zip'),
    ('06-monster-creature-avatars', '06_Monster_Creature_Avatars/06_Monster_Creature_Avatars_Pack.zip'),
    ('07-survival-food-cooking', '07_Survival_Food_Cooking/07_Survival_Food_Cooking_Pack.zip'),
    ('08-crafting-materials-ores', '08_Crafting_Materials_Ores/08_Crafting_Materials_Ores_Pack.zip'),
    ('09-rings-amulets-jewelry', '09_Rings_Amulets_Jewelry/09_Rings_Amulets_Jewelry_Pack.zip'),
    ('10-dark-magic-necromancy', '10_Dark_Magic_Necromancy/10_Dark_Magic_Necromancy_Pack.zip'),
]

print('🚀 Pushing updated multi-resolution packages to itch.io...')
for channel, rel_path in PACKS:
    target = f'gameverse-audio/game-asset-vault:{channel}'
    zip_file = VAULT_DIR / rel_path
    res = subprocess.run([BUTLER_BIN, 'push', str(zip_file), target], env=env, text=True, capture_output=True)
    if res.returncode == 0:
        print(f'  ✅ {channel}: Success')
    else:
        print(f'  ❌ {channel}: Failed ({res.stderr.strip()})')
print('🎉 itch.io deployment finished.')
