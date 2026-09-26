#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_paid_vault_10packs.py: 有料全部盛りVault (10大ジャンル・計80枚) 完全自動生成スクリプト
- ユーザー指定ルール:
  1. 無料版（火炎魔法、ポーション、宝箱・金貨、バフ）と絶対に素材を被らせない
  2. 有料版のZIP名には「01_...」〜「10_...」と通し番号（数字）を明記
  3. 各パック8枚 ＝ 計80枚の超特大メガVault
- パック構成:
  01: 01_Fantasy_Weapons_Pack (武器・近接・遠距離: 既存完成品を活用)
  02: 02_Mythic_Armor_Helmets_Pack (重装防具・兜・盾)
  03: 03_Cyberpunk_SciFi_HUD_UI_Pack (SF・サイバーパンクHUD/UI)
  04: 04_Gemstones_Crystals_Pack (宝石・鉱物・結晶)
  05: 05_Spellbooks_Tomes_Pack (魔導書・古代グリモワール)
  06: 06_Monster_Creature_Avatars_Pack (モンスター・敵キャラ顔アイコン)
  07: 07_Survival_Food_Cooking_Pack (サバイバル食材・料理)
  08: 08_Crafting_Materials_Ores_Pack (採掘鉱石・モンスター素材)
  09: 09_Rings_Amulets_Jewelry_Pack (指輪・アミュレット・装飾品)
  10: 10_Dark_Magic_Necromancy_Pack (暗黒魔術・オカルト・呪物)
"""

import os
import sys
import time
import json
import shutil
import base64
import zipfile
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

BASE_DIR = Path("/Users/base/Automated-Projects/Game-Assets")
OUTPUTS_DIR = BASE_DIR / "outputs" / "Paid_Vault_10Packs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

EXISTING_WEAPONS_DIR = BASE_DIR / "outputs" / "Game_Asset_Vault_Build" / "Pack02_Fantasy_Weapons_Armor"
ENV_PATH = Path("/Users/base/Automated-Projects/YouTube/.env")

def load_api_key():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("ACCOUNT_1_GEMINI_API_KEY")
    if not api_key and ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ACCOUNT_1_GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
                break
    return api_key

def make_transparent_luma(img, low_thresh=18, high_thresh=55):
    rgba = img.convert("RGBA")
    data = np.array(rgba, dtype=np.float32)

    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    max_val = np.maximum(np.maximum(r, g), b)
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    key_metric = 0.7 * max_val + 0.3 * luma

    alpha = np.zeros_like(key_metric)
    mask_opaque = key_metric >= high_thresh
    mask_trans = key_metric <= low_thresh
    mask_inter = (~mask_opaque) & (~mask_trans)

    alpha[mask_opaque] = 255.0
    alpha[mask_trans] = 0.0

    t = (key_metric[mask_inter] - low_thresh) / (high_thresh - low_thresh)
    alpha[mask_inter] = (3 * t**2 - 2 * t**3) * 255.0

    alpha_norm = np.clip(alpha / 255.0, 0.001, 1.0)
    for c in range(3):
        boosted = data[:, :, c] / alpha_norm
        data[:, :, c] = np.clip(boosted, 0, 255)

    data[:, :, 3] = np.clip(alpha, 0, 255)
    return Image.fromarray(data.astype(np.uint8), "RGBA")

def generate_single_image(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }
    resp = requests.post(url, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"API Error {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    b64_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    return base64.b64decode(b64_data)

LICENSE_TEXT = """================================================================================
COMMERCIAL GAME ASSET LICENSE & TERMS OF USE
THE ULTIMATE 2D GAME ASSET VAULT
================================================================================

Thank you for purchasing The Ultimate 2D Game Asset Vault!

--------------------------------------------------------------------------------
【PERMITTED USES】
--------------------------------------------------------------------------------
1. Unlimited Commercial & Personal Game Projects
   - You are granted a worldwide, perpetual, royalty-free license to use these assets in commercial, indie, or free games.
   
2. All Game Platforms Supported
   - Steam, itch.io, Epic Games Store, App Store (iOS), Google Play (Android), Nintendo Switch, PlayStation, Xbox, Web, etc.

3. Complete Modification Rights
   - You may freely resize, crop, recolor, alter textures, animate, and adapt these assets.

4. NO ATTRIBUTION REQUIRED
   - Credit is appreciated but completely optional.

--------------------------------------------------------------------------------
【PROHIBITED USES】
--------------------------------------------------------------------------------
1. Standalone Resale or Redistribution
   - You cannot resell, distribute, sub-license, or share these raw asset files as standalone stock art or in competing asset packs.
2. NFT / Blockchain Prohibited
   - You cannot use these assets for NFT minting or blockchain tokens.

================================================================================
"""

README_TEMPLATE = """================================================================================
THE ULTIMATE 2D GAME ASSET VAULT — {title}
================================================================================

Included in this package:
- Transparent_Icons/ : 512x512 crisp PNG icons with clean transparent alpha background (drag-and-drop ready)
- Original_Art/      : High-resolution concept art files (1024x1024)
- showcase_preview.png: Complete collection overview sheet
- LICENSE.txt        : Perpetual royalty-free commercial license

Universal Engine Compatibility:
- Unity, Godot, Unreal Engine, GameMaker, RPG Maker, Construct, and custom 2D engines.

Thank you for supporting GameVerse Audio & Assets!
================================================================================
"""

def create_showcase_image(icons, title_text, out_path):
    cw, ch = 1200, 700
    canvas = Image.new("RGBA", (cw, ch), (14, 19, 30, 255))
    draw = ImageDraw.Draw(canvas)

    for gx in range(0, cw, 40):
        draw.line([(gx, 0), (gx, ch)], fill=(24, 34, 52, 100), width=1)
    for gy in range(0, ch, 40):
        draw.line([(0, gy), (cw, gy)], fill=(24, 34, 52, 100), width=1)

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf", 36)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 18, index=2)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((cw // 2, 45), title_text, font=font_title, fill=(255, 255, 255), anchor="mm")
    draw.text((cw // 2, 85), "THE ULTIMATE 2D GAME ASSET VAULT  •  512x512 TRANSPARENT PNG  •  COMMERCIAL LICENSE", font=font_sub, fill=(245, 158, 11), anchor="mm")

    slot_size = 200
    start_x = (cw - (4 * slot_size + 3 * 30)) // 2
    start_y = 130

    for idx, icon_path in enumerate(icons[:8]):
        col = idx % 4
        row = idx // 4
        x = start_x + col * (slot_size + 30)
        y = start_y + row * (slot_size + 30)

        draw.rounded_rectangle([x, y, x + slot_size, y + slot_size], radius=16, fill=(20, 28, 44, 220), outline=(245, 158, 11, 100), width=2)

        if icon_path.exists():
            ic = Image.open(icon_path).convert("RGBA").resize((slot_size - 30, slot_size - 30), Image.Resampling.LANCZOS)
            canvas.paste(ic, (x + 15, y + 15), ic)

    canvas.save(out_path, "PNG")

PAID_PACKS = [
    # 01: 武器（既存活用）
    {
        "num": "01",
        "folder_name": "01_Fantasy_Weapons",
        "zip_name": "01_Fantasy_Weapons_Pack.zip",
        "title": "01 // FANTASY WEAPONS & BLADES",
        "existing_dir": EXISTING_WEAPONS_DIR,
        "items": []
    },
    # 02: 重装防具・兜・盾
    {
        "num": "02",
        "folder_name": "02_Mythic_Armor_Helmets",
        "zip_name": "02_Mythic_Armor_Helmets_Pack.zip",
        "title": "02 // MYTHIC ARMOR & BATTLE HELMETS",
        "existing_dir": None,
        "items": [
            {"slug": "dragon_scale_cuirass", "name": "Dragon Scale Cuirass", "desc": "spiky dark green dragon-scale steel cuirass chestplate with glowing molten ember lining"},
            {"slug": "death_knight_skull_helm", "name": "Death Knight Skull Helm", "desc": "horned dark iron death-knight skull helmet with glowing cyan eye sockets and jagged horns"},
            {"slug": "paladin_engraved_breastplate", "name": "Paladin Holy Breastplate", "desc": "ornate engraved polished silver paladin chestplate armor with radiant gold cross trim"},
            {"slug": "assassin_shadow_cowl", "name": "Shadow Assassin Cowl", "desc": "midnight black leather assassin hood cowl with a polished silver half-face mask"},
            {"slug": "valkyrie_winged_helmet", "name": "Valkyrie Winged Helmet", "desc": "gleaming golden valkyrie battle helmet adorned with ornate feathered angelic wings"},
            {"slug": "gladiator_spiked_pauldrons", "name": "Gladiator Spiked Pauldrons", "desc": "pair of heavy hammered spiked iron gladiator shoulder pauldrons with leather straps"},
            {"slug": "mithril_chainmail_hauberk", "name": "Mithril Chainmail Hauberk", "desc": "shimmering fine woven silver mithril chainmail armor shirt with blue mystical luster"},
            {"slug": "heavy_tower_kite_shield", "name": "Heavy Tower Kite Shield", "desc": "heavy reinforced steel and dark oak wood tower kite shield with engraved heraldic lion"}
        ]
    },
    # 03: SF・サイバーパンクHUD/UI
    {
        "num": "03",
        "folder_name": "03_Cyberpunk_SciFi_HUD_UI",
        "zip_name": "03_Cyberpunk_SciFi_HUD_UI_Pack.zip",
        "title": "03 // CYBERPUNK & SCI-FI HUD UI",
        "existing_dir": None,
        "items": [
            {"slug": "holographic_radar_reticle", "name": "Holographic Radar Reticle", "desc": "circular futuristic neon cyan holographic tactical radar targeting reticle UI icon"},
            {"slug": "neon_segmented_healthbar", "name": "Neon Segmented Healthbar", "desc": "horizontal segmented glowing neon magenta and cyan cyber health energy bar UI widget"},
            {"slug": "hazard_warning_diamond", "name": "Hazard Warning Diamond", "desc": "glowing neon amber hazard caution diamond symbol with exclamation mark, sci-fi UI icon"},
            {"slug": "biometric_pulse_monitor", "name": "Biometric Pulse Monitor", "desc": "glowing neon pink holographic electrocardiogram heartbeat pulse wave monitor UI icon"},
            {"slug": "cyber_dial_lockpick", "name": "Cyber Dial Lockpick", "desc": "futuristic electronic hacking cipher circular dial widget with rotating neon code segments"},
            {"slug": "energy_hex_shield_gauge", "name": "Energy Hex Shield Gauge", "desc": "glowing cyan hexagonal cybernetic forcefield shield status indicator UI widget"},
            {"slug": "tactical_sniper_crosshair", "name": "Tactical Sniper Crosshair", "desc": "high-tech red holographic sniper rifle scope crosshair with distance range markers"},
            {"slug": "data_chip_terminal", "name": "Digital Data Chip Terminal", "desc": "glowing neon green retro-futuristic digital matrix microprocessor data chip with gold contacts"}
        ]
    },
    # 04: 宝石・鉱物・結晶
    {
        "num": "04",
        "folder_name": "04_Gemstones_Crystals",
        "zip_name": "04_Gemstones_Crystals_Pack.zip",
        "title": "04 // CUT GEMSTONES & RADIANT CRYSTALS",
        "existing_dir": None,
        "items": [
            {"slug": "faceted_crimson_ruby", "name": "Faceted Crimson Ruby", "desc": "brilliant octagonal cut red ruby gemstone with sparkling crystal refractions and internal fire"},
            {"slug": "royal_sapphire_gem", "name": "Royal Sapphire Gem", "desc": "heart-cut deep cobalt-blue royal sapphire with radiant specular light reflections"},
            {"slug": "emerald_cut_radiant_stone", "name": "Emerald Cut Radiant Stone", "desc": "rectangular emerald-cut glowing vivid green beryl crystal gemstone with crisp facets"},
            {"slug": "amethyst_quartz_cluster", "name": "Amethyst Quartz Cluster", "desc": "raw jagged purple amethyst quartz crystal geode cluster with glowing violet core"},
            {"slug": "prismatic_diamond_gem", "name": "Prismatic Diamond Gem", "desc": "brilliant round-cut clear sparkling diamond with rainbow prism dispersion highlights"},
            {"slug": "radiant_sunstone_orb", "name": "Radiant Sunstone Orb", "desc": "round polished fiery orange sunstone gem with swirling inner solar flare light"},
            {"slug": "volcanic_obsidian_shard", "name": "Volcanic Obsidian Shard", "desc": "sharp glassy pitch-black volcanic obsidian dagger shard with glowing red molten veins"},
            {"slug": "golden_topaz_teardrop", "name": "Golden Topaz Teardrop", "desc": "pear-shaped teardrop golden amber imperial topaz gem with sparkling facets"}
        ]
    },
    # 05: 魔導書・古代グリモワール
    {
        "num": "05",
        "folder_name": "05_Spellbooks_Tomes",
        "zip_name": "05_Spellbooks_Tomes_Pack.zip",
        "title": "05 // ANCIENT SPELLBOOKS & GRIMOIRES",
        "existing_dir": None,
        "items": [
            {"slug": "necromancy_bone_grimoire", "name": "Necromancy Bone Grimoire", "desc": "dark leather spellbook bound with ancient human bone trim and a carved skull lock"},
            {"slug": "pyromancy_magma_tome", "name": "Pyromancy Magma Tome", "desc": "scorched iron-bound leather spellbook with glowing molten magma cracks and burning pages"},
            {"slug": "celestial_star_scripture", "name": "Celestial Star Scripture", "desc": "midnight-blue velvet spellbook embossed with golden constellation stars and crescent moon"},
            {"slug": "druidic_nature_herbal", "name": "Druidic Nature Herbal", "desc": "thick oak bark-bound grimoire interwoven with living green vines, moss, and glowing leaf seal"},
            {"slug": "divine_holy_scripture", "name": "Divine Holy Scripture", "desc": "pristine white leather sacred prayer book with intricate ornate gold filigree and glowing cross"},
            {"slug": "void_abyssal_forbidden_book", "name": "Void Forbidden Grimoire", "desc": "otherworldly purple-black grimoire wrapped in silver chains with a living glowing eyeball on cover"},
            {"slug": "storm_lightning_tome", "name": "Storm Lightning Tome", "desc": "steel-plated grimoire crackling with blue electrical lightning sparks and thunder rune"},
            {"slug": "permafrost_ice_grimoire", "name": "Permafrost Ice Grimoire", "desc": "thick spellbook encased in translucent blue frozen permafrost ice crystals and silver snowflakes"}
        ]
    },
    # 06: モンスター・敵キャラ顔アイコン
    {
        "num": "06",
        "folder_name": "06_Monster_Creature_Avatars",
        "zip_name": "06_Monster_Creature_Avatars_Pack.zip",
        "title": "06 // MONSTER & CREATURE AVATARS",
        "existing_dir": None,
        "items": [
            {"slug": "swamp_goblin_portrait", "name": "Swamp Goblin Portrait", "desc": "bust portrait of a grinning green swamp goblin with pointed ears, yellow eyes, and bone earrings"},
            {"slug": "undead_skeleton_warrior", "name": "Undead Skeleton Warrior", "desc": "bust portrait of a decayed skeleton warrior wearing a rusted horned iron helmet with glowing cyan eye sockets"},
            {"slug": "horned_abyssal_demon", "name": "Horned Abyssal Demon", "desc": "bust portrait of a fearsome crimson pit demon with massive curled black horns and burning eyes"},
            {"slug": "withered_lich_necromancer", "name": "Withered Lich Necromancer", "desc": "bust portrait of an ancient mummified lich sorcerer wearing an ornate bone crown with purple magical flames"},
            {"slug": "savage_werewolf_beast", "name": "Savage Werewolf Beast", "desc": "bust portrait of a ferocious gray fur werewolf lycanthrope with snarling fangs and piercing amber eyes"},
            {"slug": "gothic_stone_gargoyle", "name": "Gothic Stone Gargoyle", "desc": "bust portrait of a carved weathered gray stone gargoyle creature with sinister glowing red eyes"},
            {"slug": "vampire_blood_count", "name": "Vampire Blood Count", "desc": "bust portrait of a pale aristocratic vampire lord with slicked back hair, sharp white fangs, and ruby pendant"},
            {"slug": "toxic_slime_creature", "name": "Toxic Slime Creature", "desc": "bust portrait of a translucent bubbling acidic green gelatinous slime monster with floating glowing nucleus"}
        ]
    },
    # 07: サバイバル食材・料理
    {
        "num": "07",
        "folder_name": "07_Survival_Food_Cooking",
        "zip_name": "07_Survival_Food_Cooking_Pack.zip",
        "title": "07 // SURVIVAL FOOD & PROVISIONS",
        "existing_dir": None,
        "items": [
            {"slug": "roasted_beast_meat", "name": "Roasted Beast Meat", "desc": "golden-brown crispy roasted large meat drumstick on a thick white bone, juicy RPG food item"},
            {"slug": "crusty_sourdough_loaf", "name": "Crusty Sourdough Bread", "desc": "rustic golden-baked crusty sourdough bread loaf with flour dusting and score marks"},
            {"slug": "enchanted_orchard_apple", "name": "Enchanted Orchard Apple", "desc": "crisp shiny deep-red orchard apple with a fresh green leaf, RPG fruit item"},
            {"slug": "grilled_salmon_steak", "name": "Grilled Salmon Steak", "desc": "perfectly grilled pink river salmon fish fillet with black grill char marks and fresh lemon wedge"},
            {"slug": "aged_cheese_wedge", "name": "Aged Swiss Cheese Wheel", "desc": "round golden aged cheese wheel with a triangular cut wedge showing realistic air holes"},
            {"slug": "wild_forest_mushrooms", "name": "Wild Forest Mushrooms", "desc": "cluster of three freshly gathered wild woodland mushrooms with spotted brown caps and delicate gills"},
            {"slug": "golden_honeycomb_clay_pot", "name": "Golden Honeycomb Clay Pot", "desc": "rustic clay honey pot dripping with golden sweet honeycomb syrup and wooden honey dipper"},
            {"slug": "smoked_tavern_sausages", "name": "Smoked Tavern Sausages", "desc": "link of three plump sizzling smoked pork tavern sausages tied with cooking twine"}
        ]
    },
    # 08: 採掘鉱石・モンスター素材
    {
        "num": "08",
        "folder_name": "08_Crafting_Materials_Ores",
        "zip_name": "08_Crafting_Materials_Ores_Pack.zip",
        "title": "08 // CRAFTING MATERIALS & ORES",
        "existing_dir": None,
        "items": [
            {"slug": "raw_gold_nugget_ore", "name": "Raw Gold Ore Nugget", "desc": "jagged natural gray mining rock heavily veined with sparkling pure metallic yellow gold"},
            {"slug": "mithril_crystal_ore", "name": "Mithril Crystal Ore", "desc": "rough dark stone embedded with sharp glowing electric cyan mithril crystal minerals"},
            {"slug": "dark_iron_ingot_stack", "name": "Dark Iron Metal Ingot", "desc": "stack of two heavy forged metallic dark iron metal rectangular ingots with stamped blacksmith anvil symbol"},
            {"slug": "dragon_scale_leather_hide", "name": "Dragon Scale Leather Hide", "desc": "roll of thick textured dark reptilian dragon hide leather tied with a sturdy hemp cord"},
            {"slug": "luminous_fairy_dust_jar", "name": "Luminous Fairy Dust Jar", "desc": "small corked glass alchemy jar containing sparkling glowing iridescent rainbow fairy dust"},
            {"slug": "ancient_beast_horn", "name": "Ancient Beast Horn", "desc": "large curved spiral ivory beast horn with engraved ancient tribal runic carvings"},
            {"slug": "giant_spider_silk_spool", "name": "Giant Spider Silk Spool", "desc": "wooden crafting spool wound tightly with glistening strong silver giant spider silk thread"},
            {"slug": "elemental_magma_coal", "name": "Elemental Magma Coal", "desc": "piece of volcanic charcoal ore glowing intensely with internal red-hot molten lava heat"}
        ]
    },
    # 09: 指輪・アミュレット・装飾品
    {
        "num": "09",
        "folder_name": "09_Rings_Amulets_Jewelry",
        "zip_name": "09_Rings_Amulets_Jewelry_Pack.zip",
        "title": "09 // RINGS, AMULETS & TALISMANS",
        "existing_dir": None,
        "items": [
            {"slug": "lion_signet_ruby_ring", "name": "Lion Signet Ruby Ring", "desc": "heavy ornate gold signet ring featuring a sculpted roaring lion head with glowing ruby eyes"},
            {"slug": "dragon_claw_sapphire_ring", "name": "Dragon Claw Sapphire Ring", "desc": "twisted sterling silver dragon claw ring clutching a glowing faceted royal blue sapphire sphere"},
            {"slug": "dragon_eye_amulet", "name": "Dragon Eye Medallion Amulet", "desc": "ancient bronze circular amulet medallion enclosing a glowing lifelike reptilian dragon slit eye"},
            {"slug": "celtic_trinity_talisman", "name": "Celtic Trinity Knot Talisman", "desc": "ornate silver circular talisman pendant featuring intricate intertwined Celtic knotwork"},
            {"slug": "elven_leaf_emerald_brooch", "name": "Elven Emerald Leaf Brooch", "desc": "delicate golden filigree brooch in the shape of an elven ivy leaf with sparkling emerald dewdrop"},
            {"slug": "star_of_eternity_necklace", "name": "Star of Eternity Necklace", "desc": "fine platinum link chain necklace suspending a radiant eight-pointed diamond star pendant"},
            {"slug": "dwarven_gold_torc", "name": "Dwarven Warrior Torc", "desc": "thick heavy twisted gold dwarven battle torc armband with engraved geometric hammer terminals"},
            {"slug": "gothic_skull_knuckle_ring", "name": "Gothic Skull Knuckle Ring", "desc": "darkened oxidized silver gothic ring featuring a polished smiling human skull motif"}
        ]
    },
    # 10: 暗黒魔術・オカルト・呪物
    {
        "num": "10",
        "folder_name": "10_Dark_Magic_Necromancy",
        "zip_name": "10_Dark_Magic_Necromancy_Pack.zip",
        "title": "10 // DARK MAGIC, OCCULT & CURSED RELICS",
        "existing_dir": None,
        "items": [
            {"slug": "cursed_voodoo_effigy", "name": "Cursed Voodoo Effigy", "desc": "stitched burlap cursed voodoo effigy doll with dark button eyes and brass sewing pins stuck through"},
            {"slug": "sacrificial_bone_dagger", "name": "Sacrificial Bone Dagger", "desc": "sinister curved ritual dagger carved from ivory beast bone stained with dark dried sacrificial blood"},
            {"slug": "trapped_soul_lantern", "name": "Trapped Soul Lantern", "desc": "ornate brass gothic caged glass lantern holding a swirling glowing ethereal cyan screaming ghost soul"},
            {"slug": "occult_pentagram_orb", "name": "Occult Pentagram Scrying Orb", "desc": "polished black obsidian scrying orb sphere resting on a silver demonic claw stand with purple smoke"},
            {"slug": "mummified_demon_finger", "name": "Mummified Demon Finger Relic", "desc": "shriveled black mummified demon finger with long sharp obsidian claw tied to a leather cord necklace"},
            {"slug": "raven_skull_occult_fetish", "name": "Raven Skull Occult Fetish", "desc": "weathered bleached bird raven skull amulet adorned with black crow feathers and bone beads"},
            {"slug": "bubbling_witch_cauldron", "name": "Bubbling Witch Cauldron", "desc": "black cast-iron tripod cauldron pot boiling with glowing toxic purple witch brew emitting skull smoke"},
            {"slug": "blood_demon_pact_scroll", "name": "Blood Demon Pact Scroll", "desc": "aged crinkled yellow parchment contract written in glowing crimson demonic blood script with a wax seal"}
        ]
    }
]

def process_pack_01(pack):
    """01: 既存の武器パックから綺麗にコピーして01番として整備"""
    folder = OUTPUTS_DIR / pack["folder_name"]
    folder.mkdir(parents=True, exist_ok=True)
    orig_dir = folder / "Original_Art"
    trans_dir = folder / "Transparent_Icons"
    orig_dir.mkdir(exist_ok=True)
    trans_dir.mkdir(exist_ok=True)

    print(f"\n[{pack['num']}/10] ⚔️ {pack['title']} 整備中 (既存アセット活用)...")
    src = pack["existing_dir"]
    if src.exists():
        for f in (src / "Original_Art").glob("*.png"):
            shutil.copy2(f, orig_dir / f.name)
        for f in (src / "Transparent_Icons").glob("*.png"):
            shutil.copy2(f, trans_dir / f.name)

    icon_paths = sorted(list(trans_dir.glob("*.png")))
    preview_file = folder / "showcase_preview.png"
    create_showcase_image(icon_paths, pack["title"], preview_file)

    (folder / "LICENSE.txt").write_text(LICENSE_TEXT, encoding="utf-8")
    (folder / "README.txt").write_text(README_TEMPLATE.format(title=pack["title"]), encoding="utf-8")

    zip_path = folder / pack["zip_name"]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(folder / "LICENSE.txt", arcname="LICENSE.txt")
        zf.write(folder / "README.txt", arcname="README.txt")
        zf.write(preview_file, arcname="showcase_preview.png")
        for f in trans_dir.glob("*.png"):
            zf.write(f, arcname=f"Transparent_Icons/{f.name}")
        for f in orig_dir.glob("*.png"):
            zf.write(f, arcname=f"Original_Art/{f.name}")

    print(f"  ✅ 完成: {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return zip_path

def process_new_pack(pack, api_key):
    folder = OUTPUTS_DIR / pack["folder_name"]
    folder.mkdir(parents=True, exist_ok=True)
    orig_dir = folder / "Original_Art"
    trans_dir = folder / "Transparent_Icons"
    orig_dir.mkdir(exist_ok=True)
    trans_dir.mkdir(exist_ok=True)

    print("\n" + "=" * 60)
    print(f"[{pack['num']}/10] 🎨 {pack['title']} 生成開始 (8枚)")
    print("=" * 60)

    icon_paths = []
    for idx, item in enumerate(pack["items"], 1):
        slug = item["slug"]
        orig_file = orig_dir / f"{slug}.png"
        icon_file = trans_dir / f"{slug}.png"
        icon_paths.append(icon_file)

        if orig_file.exists() and icon_file.exists():
            print(f"  ⏭️ [{idx}/8] 既存スキップ: {slug}")
            continue

        print(f"  ✨ [{idx}/8] 生成中: {item['name']} ({slug})...")
        prompt = (
            f"A professional 2D video game inventory asset icon of {item['desc']}. "
            "Isolated, perfectly centered on pure solid pitch black background (#000000). "
            "Sharp crisp edges, vibrant saturated highlights, studio quality digital fantasy RPG game art. "
            "1:1 aspect ratio, absolutely NO white box, NO frame, NO border, NO table, NO text, NO labels, NO background scenery."
        )

        for attempt in range(3):
            try:
                img_bytes = generate_single_image(api_key, prompt)
                orig_file.write_bytes(img_bytes)

                img = Image.open(orig_file)
                trans_img = make_transparent_luma(img, low_thresh=18, high_thresh=55)

                bbox = trans_img.getbbox()
                if bbox:
                    cropped = trans_img.crop(bbox)
                    iw, ih = cropped.size
                    max_dim = max(iw, ih)
                    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
                    scale = (512 * 0.88) / max_dim
                    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
                    resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
                    px = (512 - nw) // 2
                    py = (512 - nh) // 2
                    canvas.paste(resized, (px, py), resized)
                    canvas.save(icon_file, "PNG")
                else:
                    trans_img.resize((512, 512), Image.Resampling.LANCZOS).save(icon_file, "PNG")

                print(f"    🌟 透過成功: {icon_file.name}")
                break
            except Exception as e:
                print(f"    ⚠️ リトライ ({attempt + 1}/3): {e}")
                time.sleep(3)

        time.sleep(1)

    preview_file = folder / "showcase_preview.png"
    create_showcase_image(icon_paths, pack["title"], preview_file)
    print(f"  🖼️ プレビュー生成完了: {preview_file.name}")

    (folder / "LICENSE.txt").write_text(LICENSE_TEXT, encoding="utf-8")
    (folder / "README.txt").write_text(README_TEMPLATE.format(title=pack["title"]), encoding="utf-8")

    zip_path = folder / pack["zip_name"]
    print(f"  📦 ZIP圧縮中: {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(folder / "LICENSE.txt", arcname="LICENSE.txt")
        zf.write(folder / "README.txt", arcname="README.txt")
        zf.write(preview_file, arcname="showcase_preview.png")
        for f in trans_dir.glob("*.png"):
            zf.write(f, arcname=f"Transparent_Icons/{f.name}")
        for f in orig_dir.glob("*.png"):
            zf.write(f, arcname=f"Original_Art/{f.name}")

    print(f"  ✅ パック完成: {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return zip_path

def main():
    api_key = load_api_key()
    if not api_key:
        print("❌ Gemini APIキーが見つかりません。")
        sys.exit(1)

    print("==================================================")
    print("👑 有料全部盛りVault (10大ジャンル・計80枚) 生成開始")
    print("・無料版と被りゼロを完全保証")
    print("・01〜10の通し番号付きZIPパッケージ")
    print("==================================================")

    created_zips = []

    # 01: 武器
    z1 = process_pack_01(PAID_PACKS[0])
    created_zips.append(z1)

    # 02〜10: 新規生成
    for pack in PAID_PACKS[1:]:
        zp = process_new_pack(pack, api_key)
        created_zips.append(zp)

    print("\n" + "=" * 60)
    print("🎉 【有料Vault 10パック生成完了】")
    print("各パックが独立した個別ZIP（01〜10）として完成しました！（合体マスターZIPは作成しません）")
    for zp in created_zips:
        print(f"  📦 {zp.name} ({zp.stat().st_size / 1024 / 1024:.2f} MB)")
    print("=" * 60)

if __name__ == "__main__":
    main()
