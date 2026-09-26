#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 1 (Haven Chill Audio / Komorebi Chill Audio) 公式サムネイル完全自動生成スクリプト
- フォント: Futura Medium (index=0)
- エフェクト: Warm Amber Glow (255, 235, 180) + ドロップシャドウ (GaussianBlur 15px)
- 文字枠・ピルバッジ完全排除
# - 仕様書: .agents/rules/01_youtube_automation.md Section 4 (サムネイル確定テーブル)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel")
BG_PATH = BASE_DIR / "cover_art/bg_grand_library_real.jpeg"
OUT_DIR = BASE_DIR / "output_videos/thumbnails"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1920
HEIGHT = 1080
FUTURA_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"

def prepare_base_image():
    img = Image.open(BG_PATH).convert("RGBA")
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

def draw_lofi_thumbnail(base_img, output_path, line_main="STUDY WITH ME", line_sub="2 HOURS • COZY LIBRARY LOFI"):
    font_main = ImageFont.truetype(FUTURA_PATH, 105, index=0)
    font_sub = ImageFont.truetype(FUTURA_PATH, 52, index=0)
    
    x, y = 100, 100
    x_s, y_s = 105, 225
    
    # 1. シャドウ & アンバーグロー
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.text((x + 4, y + 6), line_main, font=font_main, fill=(0, 0, 0, 240))
    g_draw.text((x, y), line_main, font=font_main, fill=(255, 235, 180, 200))
    g_draw.text((x_s + 3, y_s + 4), line_sub, font=font_sub, fill=(0, 0, 0, 220))
    g_draw.text((x_s, y_s), line_sub, font=font_sub, fill=(255, 235, 180, 180))
    
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(15))
    result = Image.alpha_composite(base_img, glow_blurred)
    
    # 2. 前面ピュアホワイト
    txt_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    t_draw.text((x, y), line_main, font=font_main, fill=(255, 255, 255, 255))
    t_draw.text((x_s, y_s), line_sub, font=font_sub, fill=(255, 255, 255, 255))
    
    result = Image.alpha_composite(result, txt_layer)
    result.convert("RGB").save(output_path, quality=95)
    print(f"✅ Generated Ch1 Thumbnail: {output_path}")

def generate_all():
    base_bg = prepare_base_image()
    
    # パターン1: 【Pure Clean Art】（文字なし）
    p1 = OUT_DIR / "THUMBNAIL_01_PURE_CLEAN_ART.jpg"
    base_bg.convert("RGB").save(p1, quality=95)
    print(f"✅ Pattern 1: {p1}")
    
    # パターン2: 【STUDY WITH ME / 2 HOURS】
    p2 = OUT_DIR / "THUMBNAIL_02_STUDY_WITH_ME.jpg"
    draw_lofi_thumbnail(base_bg, p2, "STUDY WITH ME", "2 HOURS • COZY LIBRARY LOFI")
    
    # パターン3: 【POMODORO 25/5 / 2 HOURS FOCUS】
    p3 = OUT_DIR / "THUMBNAIL_03_POMODORO_25_5.jpg"
    draw_lofi_thumbnail(base_bg, p3, "POMODORO 25/5", "2 HOURS FOCUS • STUDY SESSION")

if __name__ == "__main__":
    generate_all()
