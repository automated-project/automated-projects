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

GUMROAD_CLI = str(BASE_DIR / 'bin' / 'gumroad')
VAULT_DIR = Path('/Users/base/Automated-Projects/Game-Assets/outputs/Paid_Vault_10Packs')

PACKS = [
    VAULT_DIR / '01_Fantasy_Weapons' / '01_Fantasy_Weapons_Pack.zip',
    VAULT_DIR / '02_Mythic_Armor_Helmets' / '02_Mythic_Armor_Helmets_Pack.zip',
    VAULT_DIR / '03_Cyberpunk_SciFi_HUD_UI' / '03_Cyberpunk_SciFi_HUD_UI_Pack.zip',
    VAULT_DIR / '04_Gemstones_Crystals' / '04_Gemstones_Crystals_Pack.zip',
    VAULT_DIR / '05_Spellbooks_Tomes' / '05_Spellbooks_Tomes_Pack.zip',
    VAULT_DIR / '06_Monster_Creature_Avatars' / '06_Monster_Creature_Avatars_Pack.zip',
    VAULT_DIR / '07_Survival_Food_Cooking' / '07_Survival_Food_Cooking_Pack.zip',
    VAULT_DIR / '08_Crafting_Materials_Ores' / '08_Crafting_Materials_Ores_Pack.zip',
    VAULT_DIR / '09_Rings_Amulets_Jewelry' / '09_Rings_Amulets_Jewelry_Pack.zip',
    VAULT_DIR / '10_Dark_Magic_Necromancy' / '10_Dark_Magic_Necromancy_Pack.zip',
]

print('🚀 Updating Gumroad Paid Asset Vault with new multi-res packages...')
cmd = [
    GUMROAD_CLI, "products", "update", "c07Os4dAkeUFa2VBAne4YQ==",
    "--currency", "usd",
    "--price", "0.99",
    "--yes"
]
for p in PACKS:
    cmd.extend(["--file", str(p)])

res = subprocess.run(cmd, env=env, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
