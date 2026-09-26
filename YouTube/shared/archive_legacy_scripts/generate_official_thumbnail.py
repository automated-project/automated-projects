#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate High CTR Official Thumbnails for PhonkForge Audio 1-Hour Mix
Fix emoji square boxes using pure text and optimized font rendering.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG_PATH = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/cover_art/Gemini_Generated_Image_gzzyqfgzzyqfgzzy.jpeg")
OUT_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/output_videos/thumbnails")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

base_img = Image.open(BG_PATH).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)

# --- PATTERN 1: Pro Neon Gym Phonk Badge (Top-Left / High Visibility) ---
def make_thumb_1():
    img = base_img.copy()
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font_large = ImageFont.truetype(FONT_IMPACT, 135)
    font_badge = ImageFont.truetype(FONT_ARIAL_BLACK, 38)
    
    # Left Gradient Shadow for extreme text contrast
    gradient = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(950):
        alpha = int(190 * (1.0 - (x / 950.0) ** 1.4))
        g_draw.line([(x, 0), (x, 1080)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, gradient)
    
    # 1. Top Mini Pill Badge "SUPER CRISP AUDIO"
    draw.rounded_rectangle([75, 75, 460, 135], radius=12, fill=(220, 38, 38, 230), outline=(255, 255, 255, 200), width=2)
    draw.text((100, 84), "SUPER CRISP AUDIO", font=font_badge, fill=(255, 255, 255, 255))
    
    # 2. Main Large Text "1 HOUR"
    x_pos = 75
    y_pos = 160
    draw.text((x_pos + 6, y_pos + 6), "1 HOUR", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, y_pos), "1 HOUR", font=font_large, fill=(255, 255, 255, 255))
    
    # 3. Main Accent Text "GYM PHONK" (Neon Pink / Magenta)
    y_pos2 = 295
    draw.text((x_pos + 6, y_pos2 + 6), "GYM PHONK", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, y_pos2), "GYM PHONK", font=font_large, fill=(244, 114, 182, 255))
    
    # 4. Subtitle "DRIFT & HARDSTYLE"
    y_pos3 = 440
    draw.rounded_rectangle([x_pos, y_pos3, x_pos + 560, y_pos3 + 70], radius=10, fill=(17, 24, 39, 220), outline=(147, 51, 234, 220), width=2)
    draw.text((x_pos + 26, y_pos3 + 12), "DRIFT & HARDSTYLE", font=ImageFont.truetype(FONT_ARIAL_BLACK, 40), fill=(216, 180, 254, 255))
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_01_PRO_NEON_BADGE.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

# --- PATTERN 2: High Visibility Corner Badges ---
def make_thumb_3():
    img = base_img.copy()
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Top Left Yellow Badge
    draw.rounded_rectangle([70, 70, 480, 150], radius=14, fill=(245, 158, 11, 240), outline=(255, 255, 255, 220), width=2)
    draw.text((95, 82), "1 HOUR MIX", font=ImageFont.truetype(FONT_ARIAL_BLACK, 50), fill=(0, 0, 0, 255))
    
    # Bottom Left Phonk Pill
    draw.rounded_rectangle([70, 880, 740, 990], radius=16, fill=(15, 23, 42, 230), outline=(236, 72, 153, 230), width=3)
    draw.text((95, 902), "GYM & DRIFT PHONK", font=ImageFont.truetype(FONT_ARIAL_BLACK, 52), fill=(255, 255, 255, 255))
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_03_CLEAN_BADGES.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

p1 = make_thumb_1()
p3 = make_thumb_3()
