#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): トロピカル大自然 サムネイル生成スクリプト (3パターン)
- ソース画像: /Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/cover_art/tropical_thumb_base.jpg
- フォント: Futura (Electric Cyan Glow / Pure White Glow)
- 新ルール完全遵守:
  1. 商用利用・FREE BGM等の文言をサムネ・タイトルに含めない
  2. 時間帯・情景（Morning, Sunshine, Tropical Paradise）、用途（Drive, Focus, Good Mood）を明確化
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
SRC_IMG = BASE_DIR / "cover_art/Gemini_Generated_Image_avpynyavpynyavpy.jpeg"
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

def draw_ch3_thumbnail(base_img, output_path, line_main, line_sub, x=90, y=85):
    # Futura Bold / Medium
    font_main = ImageFont.truetype(FUTURA_PATH, 98, index=2)
    font_sub = ImageFont.truetype(FUTURA_PATH, 42, index=0)
    
    x_s = x + 5
    y_s = y + 120
    
    # 1. シャドウ & Electric Cyan Glow
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    
    # 黒影
    g_draw.text((x + 6, y + 8), line_main, font=font_main, fill=(0, 0, 0, 245))
    g_draw.text((x_s + 4, y_s + 6), line_sub, font=font_sub, fill=(0, 0, 0, 230))
    
    # Cyan Glow
    g_draw.text((x, y), line_main, font=font_main, fill=(0, 229, 255, 220))
    g_draw.text((x_s, y_s), line_sub, font=font_sub, fill=(0, 229, 255, 190))
    
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(14))
    result = Image.alpha_composite(base_img, glow_blurred)
    
    # 2. 前面ピュアホワイト
    txt_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    t_draw.text((x, y), line_main, font=font_main, fill=(255, 255, 255, 255))
    t_draw.text((x_s, y_s), line_sub, font=font_sub, fill=(210, 245, 255, 255))
    
    result = Image.alpha_composite(result, txt_layer)
    result.convert("RGB").save(output_path, quality=95)
    print(f"✅ Generated Thumbnail: {output_path}")

def main():
    base_bg = prepare_base_image()
    
    # パターン1: 【FEEL GOOD POP / 1 HOUR】（朝の目覚め・ポジティブ・王道）
    p1 = OUT_DIR / "THUMB_CH3_01_FEEL_GOOD_POP.jpg"
    draw_ch3_thumbnail(base_bg, p1, "FEEL GOOD POP", "1 HOUR • SUNSHINE MORNING DANCE")
    p1_art = ARTIFACTS_DIR / "thumb_ch3_01_feel_good_pop.jpg"
    Image.open(p1).save(p1_art, quality=95)
    
    # パターン2: 【SUNSHINE MORNING / 1 HOUR】（朝・晴天・ドライブ）
    p2 = OUT_DIR / "THUMB_CH3_02_SUNSHINE_MORNING.jpg"
    draw_ch3_thumbnail(base_bg, p2, "SUNSHINE MORNING", "1 HOUR • UPLIFTING TROPICAL BEATS")
    p2_art = ARTIFACTS_DIR / "thumb_ch3_02_sunshine_morning.jpg"
    Image.open(p2).save(p2_art, quality=95)
    
    # パターン3: 【TROPICAL PARADISE / 1 HOUR】（海・リゾート・モチベーション）
    p3 = OUT_DIR / "THUMB_CH3_03_TROPICAL_PARADISE.jpg"
    draw_ch3_thumbnail(base_bg, p3, "TROPICAL PARADISE", "1 HOUR • BRIGHT ACOUSTIC & POP")
    p3_art = ARTIFACTS_DIR / "thumb_ch3_03_tropical_paradise.jpg"
    Image.open(p3).save(p3_art, quality=95)
    
    # パターン4: 【Pure Clean Art】（文字なし）
    p4 = OUT_DIR / "THUMB_CH3_04_PURE_NATURE_ART.jpg"
    base_bg.convert("RGB").save(p4, quality=95)
    p4_art = ARTIFACTS_DIR / "thumb_ch3_04_pure_nature_art.jpg"
    Image.open(p4).save(p4_art, quality=95)
    
    print("\n🎉 All 4 Ch3 tropical thumbnail variations generated successfully!")

if __name__ == "__main__":
    main()
