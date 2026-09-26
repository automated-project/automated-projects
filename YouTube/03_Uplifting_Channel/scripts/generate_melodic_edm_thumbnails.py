#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 3 (AuraMelody Audio) 公式サムネイル完全自動生成スクリプト
- フォント: Futura Bold (index=2) ＋ Futura Medium (index=0)
- エフェクト: Electric Cyan Glow (0, 229, 255) + ディープドロップシャドウ (GaussianBlur 8px)
- 文字枠・ピルバッジ完全排除
- 仕様書: .agents/rules/01_youtube_automation.md Section 4 (サムネイル確定テーブル)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel")
BG_PATH = BASE_DIR / "cover_art/Gemini_Generated_Image_tfs8zttfs8zttfs8.jpeg"
OUT_DIR = BASE_DIR / "output_videos/thumbnails"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1920
HEIGHT = 1080
FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"

def render_glow_left(cover_path, output_path, text_main="PURE UPLIFTING", text_sub="1 HOUR MELODIC PROGRESSIVE"):
    base_img = Image.open(cover_path).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    font_main = ImageFont.truetype(FUTURA_PATH, 86, index=2) # Futura Bold
    font_sub = ImageFont.truetype(FUTURA_PATH, 36, index=0)  # Futura Medium
    
    x_m = 80
    y_m = 65
    x_s = 82
    y_s = y_m + 98
    
    # 1. 鮮やかなシアンネオングロー
    glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_layer)
    
    for offset in range(12, 0, -2):
        alpha = int(130 * (1.0 - offset / 14.0))
        for dx, dy in [(-offset,0), (offset,0), (0,-offset), (0,offset), (-offset,-offset), (offset,offset), (-offset,offset), (offset,-offset)]:
            gdraw.text((x_m + dx, y_m + dy), text_main, font=font_main, fill=(0, 229, 255, alpha))
            
    for offset in range(6, 0, -2):
        alpha = int(100 * (1.0 - offset / 8.0))
        for dx, dy in [(-offset,0), (offset,0), (0,-offset), (0,offset)]:
            gdraw.text((x_s + dx, y_s + dy), text_sub, font=font_sub, fill=(0, 229, 255, alpha))
            
    glow_blurred = glow_layer.filter(ImageFilter.GaussianBlur(8))
    im = Image.alpha_composite(base_img, glow_blurred)
    
    # 2. ディープドロップシャドウ ＋ 前面テキスト
    txt_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(txt_layer)
    for dx, dy in [(2,2), (3,3), (1,3), (3,1)]:
        tdraw.text((x_m + dx, y_m + dy), text_main, font=font_main, fill=(5, 15, 30, 220))
        tdraw.text((x_s + dx, y_s + dy), text_sub, font=font_sub, fill=(5, 15, 30, 200))
        
    tdraw.text((x_m, y_m), text_main, font=font_main, fill=(255, 255, 255, 255))
    tdraw.text((x_s, y_s), text_sub, font=font_sub, fill=(185, 245, 255, 255))
    
    im = Image.alpha_composite(im, txt_layer)
    im.convert("RGB").save(output_path, quality=98)
    print(f"✅ Generated Ch3 Thumbnail: {output_path}")

def generate_all():
    p1 = OUT_DIR / "THUMBNAIL_01_PURE_UPLIFTING.jpg"
    render_glow_left(BG_PATH, p1, "PURE UPLIFTING", "1 HOUR MELODIC PROGRESSIVE")

if __name__ == "__main__":
    generate_all()
