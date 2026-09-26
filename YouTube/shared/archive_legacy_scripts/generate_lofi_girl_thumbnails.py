#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio): 勉強する女の子サムネイル生成スクリプト (4パターン)
- ソース画像: /Users/base/Automated-Projects/YouTube/01_Chill_Channel/cover_art/ghibli_lofi_girl_study.jpg_20260922021249.jpeg
- フォント: Futura (Warm Amber Glow + Subtle Shadow)
- 文字枠・商標（Anime/Ghibli）完全排除
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
SRC_IMG = BASE_DIR / "cover_art/ghibli_lofi_girl_study.jpg_20260922021249.jpeg"
OUT_DIR = BASE_DIR / "output_videos/thumbnails"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR = Path("/Users/base/.gemini/antigravity/brain/155a7193-a8f4-44d7-80ea-176734dc875d")

WIDTH = 1920
HEIGHT = 1080
FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"

def prepare_base_image():
    img = Image.open(SRC_IMG).convert("RGBA")
    img_w, img_h = img.size
    target_ratio = WIDTH / HEIGHT
    cur_ratio = img_w / img_h

    if cur_ratio > target_ratio:
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, img_h))
    else:
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 2
        img = img.crop((0, top, img_w, top + new_h))

    return img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

def draw_lofi_thumbnail(base_img, output_path, line_main, line_sub, x=100, y=90):
    # Futura Medium / Bold
    font_main = ImageFont.truetype(FUTURA_PATH, 110, index=0)
    font_sub = ImageFont.truetype(FUTURA_PATH, 48, index=0)
    
    x_s = x + 5
    y_s = y + 130
    
    # 1. シャドウ & アンバーグロー
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.text((x + 5, y + 8), line_main, font=font_main, fill=(0, 0, 0, 245))
    g_draw.text((x, y), line_main, font=font_main, fill=(255, 235, 180, 220))
    g_draw.text((x_s + 4, y_s + 6), line_sub, font=font_sub, fill=(0, 0, 0, 230))
    g_draw.text((x_s, y_s), line_sub, font=font_sub, fill=(255, 235, 180, 190))
    
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(14))
    result = Image.alpha_composite(base_img, glow_blurred)
    
    # 2. 前面ピュアホワイト
    txt_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    t_draw.text((x, y), line_main, font=font_main, fill=(255, 255, 255, 255))
    t_draw.text((x_s, y_s), line_sub, font=font_sub, fill=(255, 255, 255, 255))
    
    result = Image.alpha_composite(result, txt_layer)
    result.convert("RGB").save(output_path, quality=95)
    print(f"✅ Generated Thumbnail: {output_path}")

def main():
    base_bg = prepare_base_image()
    
    # パターン1: 【STUDY WITH ME / 2 HOURS】（王道・高CTR）
    p1 = OUT_DIR / "THUMBNAIL_01_STUDY_WITH_ME.jpg"
    draw_lofi_thumbnail(base_bg, p1, "STUDY WITH ME", "2 HOURS • COZY LOFI & WARM PIANO")
    p1_art = ARTIFACTS_DIR / "thumb_01_study_with_me.jpg"
    base_bg_copy = Image.open(p1)
    base_bg_copy.save(p1_art, quality=95)
    
    # パターン2: 【DEEP FOCUS / 2 HOURS】（集中・作業用）
    p2 = OUT_DIR / "THUMBNAIL_02_DEEP_FOCUS.jpg"
    draw_lofi_thumbnail(base_bg, p2, "DEEP FOCUS", "2 HOURS • NOSTALGIC LOFI BEATS")
    p2_art = ARTIFACTS_DIR / "thumb_02_deep_focus.jpg"
    Image.open(p2).save(p2_art, quality=95)
    
    # パターン3: 【COZY DESK / 2 HOURS】（チル・リラックス）
    p3 = OUT_DIR / "THUMBNAIL_03_COZY_DESK.jpg"
    draw_lofi_thumbnail(base_bg, p3, "COZY DESK", "2 HOURS • RELAXING LOFI / STUDY")
    p3_art = ARTIFACTS_DIR / "thumb_03_cozy_desk.jpg"
    Image.open(p3).save(p3_art, quality=95)
    
    # パターン4: 【Pure Clean Art】（文字なし）
    p4 = OUT_DIR / "THUMBNAIL_04_PURE_CLEAN_ART.jpg"
    base_bg.convert("RGB").save(p4, quality=95)
    p4_art = ARTIFACTS_DIR / "thumb_04_pure_clean_art.jpg"
    Image.open(p4).save(p4_art, quality=95)
    
    print("\n🎉 All 4 thumbnail variations generated successfully!")

if __name__ == "__main__":
    main()
