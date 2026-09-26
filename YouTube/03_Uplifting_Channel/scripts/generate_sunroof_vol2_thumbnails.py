#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio): Sunroof Pop Mix Vol. 2 公式サムネイル生成スクリプト
- 背景画像: cover_art/Gemini_Generated_Image_i4ej4zi4ej4zi4ej.jpeg (実写風イケメン4人海沿いカフェテラス)
- フォント: Futura Bold + Electric Cyan / Soft Gold Glow
- ピュアアート版、特大文字版の複数バリエーション生成
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
SRC_IMG = BASE_DIR / "cover_art/Gemini_Generated_Image_i4ej4zi4ej4zi4ej.jpeg"
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

def draw_thumbnail(base_img, output_path, line_main, line_sub=None, x=90, y=90):
    font_main = ImageFont.truetype(FUTURA_PATH, 115, index=2) # Futura Bold
    
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    
    # 影 & シアンシグナルグロー
    g_draw.text((x + 6, y + 8), line_main, font=font_main, fill=(0, 0, 0, 245))
    g_draw.text((x, y), line_main, font=font_main, fill=(0, 229, 255, 230))
    
    if line_sub:
        font_sub = ImageFont.truetype(FUTURA_PATH, 48, index=0)
        y_s = y + 135
        g_draw.text((x + 4, y_s + 6), line_sub, font=font_sub, fill=(0, 0, 0, 230))
        g_draw.text((x, y_s), line_sub, font=font_sub, fill=(255, 235, 180, 200))
        
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(16))
    result = Image.alpha_composite(base_img, glow_blurred)
    
    # 前面ピュアホワイト
    txt_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    t_draw.text((x, y), line_main, font=font_main, fill=(255, 255, 255, 255))
    
    if line_sub:
        t_draw.text((x, y_s), line_sub, font=font_sub, fill=(255, 255, 255, 255))
        
    result = Image.alpha_composite(result, txt_layer)
    result.convert("RGB").save(output_path, quality=95)
    print(f"✅ Generated Thumbnail: {output_path}")

def main():
    base_bg = prepare_base_image()
    
    # 1. 【FEEL GOOD POP / 1 HOUR MIX】
    p1 = OUT_DIR / "thumb_ch3_sunroof_vol2_feel_good.jpg"
    draw_thumbnail(base_bg, p1, "FEEL GOOD POP", "1 HOUR • SUNSHINE & ACOUSTIC HITS", x=90, y=90)
    Image.open(p1).save(ARTIFACTS_DIR / "thumb_ch3_sunroof_vol2_feel_good.jpg", quality=95)
    
    # 2. 【SUNSHINE VIBES / POP & ACOUSTIC】
    p2 = OUT_DIR / "thumb_ch3_sunroof_vol2_sunshine.jpg"
    draw_thumbnail(base_bg, p2, "SUNSHINE VIBES", "1 HOUR • UPLIFTING POP DANCE", x=90, y=90)
    Image.open(p2).save(ARTIFACTS_DIR / "thumb_ch3_sunroof_vol2_sunshine.jpg", quality=95)
    
    # 3. 【Pure Clean Art (テキストなし)】
    p3 = OUT_DIR / "thumb_ch3_sunroof_vol2_pure_art.jpg"
    base_bg.convert("RGB").save(p3, quality=95)
    Image.open(p3).save(ARTIFACTS_DIR / "thumb_ch3_sunroof_vol2_pure_art.jpg", quality=95)
    
    print("\n🎉 Ch3 Vol 2 Thumbnails Generated Successfully!")

if __name__ == "__main__":
    main()
