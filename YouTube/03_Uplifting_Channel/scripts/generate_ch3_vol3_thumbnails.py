#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): Vol. 3 公式サムネイル生成スクリプト
- 背景画像: cover_art/Gemini_Generated_Image_8ujyyo8ujyyo8ujy.jpeg
- フォント: Futura (Soft Gold & Cyan Glow)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
SRC_IMG = BASE_DIR / "cover_art/Gemini_Generated_Image_8ujyyo8ujyyo8ujy.jpeg"
OUT_DIR = BASE_DIR / "output_videos/thumbnails"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR = Path("/Users/base/.gemini/antigravity/brain/155a7193-a8f4-44d7-80ea-176734dc875d")

WIDTH, HEIGHT = 1920, 1080
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

def draw_thumbnail(base_img, output_path, line_main, line_sub, x=100, y=90):
    font_main = ImageFont.truetype(FUTURA_PATH, 110, index=2) # Futura Bold
    font_sub = ImageFont.truetype(FUTURA_PATH, 48, index=0)  # Futura Medium
    
    x_s = x + 5
    y_s = y + 130
    
    # 1. シャドウ & シアン/ゴールドグロー
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.text((x + 5, y + 8), line_main, font=font_main, fill=(0, 0, 0, 245))
    g_draw.text((x, y), line_main, font=font_main, fill=(210, 245, 255, 220))
    g_draw.text((x_s + 4, y_s + 6), line_sub, font=font_sub, fill=(0, 0, 0, 230))
    g_draw.text((x_s, y_s), line_sub, font=font_sub, fill=(255, 235, 180, 200))
    
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(15))
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
    
    # パターン1: 【SUMMER MELODIC EDM / 1 HOUR】
    p1 = OUT_DIR / "THUMBNAIL_CH3_VOL3_SUMMER_MELODIC.jpg"
    draw_thumbnail(base_bg, p1, "SUMMER MELODIC EDM", "1 HOUR • UPLIFTING POP & PROGRESSIVE")
    Image.open(p1).save(ARTIFACTS_DIR / "thumb_ch3_vol3_pattern1.jpg", quality=95)
    
    # パターン2: 【GOLDEN HOUR EDM / 1 HOUR】
    p2 = OUT_DIR / "THUMBNAIL_CH3_VOL3_GOLDEN_HOUR.jpg"
    draw_thumbnail(base_bg, p2, "GOLDEN HOUR EDM", "1 HOUR • SUNSET FESTIVAL BEATS")
    Image.open(p2).save(ARTIFACTS_DIR / "thumb_ch3_vol3_pattern2.jpg", quality=95)
    
    # パターン3: 【Pure Clean Art】
    p3 = OUT_DIR / "THUMBNAIL_CH3_VOL3_PURE_ART.jpg"
    base_bg.convert("RGB").save(p3, quality=95)
    Image.open(p3).save(ARTIFACTS_DIR / "thumb_ch3_vol3_pure_art.jpg", quality=95)
    
    print("\n🎉 Ch3 Vol 3 Thumbnails Generated Successfully!")

if __name__ == "__main__":
    main()
