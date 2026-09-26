#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio): 高CTR 公式サムネイル生成スクリプト
- ユーザー指示準拠: 「MINI」表記完全排除、文字サイズ特大化、HEAVY BASS / GYM MIX
- フォント: Futura.ttc (Medium/Bold) + Crimson Red Glow (255, 10, 45)
- 出力: output_videos/thumbnails/thumb_ch2_8min_gym_phonk_vol1.jpg
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
BG_PATH = BASE_DIR / "cover_art/bg_underground_gym.jpeg"
OUT_DIR = BASE_DIR / "output_videos/thumbnails"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "thumb_ch2_8min_gym_phonk_vol1.jpg"

FUTURA_TTC = "/System/Library/Fonts/Supplemental/Futura.ttc"

def generate_bold_thumbnail():
    base_img = Image.open(BG_PATH).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    
    # 左側ダークグラデーション（特大文字の視認性確保）
    gradient = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(1000):
        alpha = int(210 * (1.0 - (x / 1000.0) ** 1.3))
        g_draw.line([(x, 0), (x, 1080)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(base_img, gradient)
    
    # 特大フォント設定 (Futura Bold / Medium)
    font_sub = ImageFont.truetype(FUTURA_TTC, 46, index=0)    # Medium
    font_main1 = ImageFont.truetype(FUTURA_TTC, 140, index=2) # Bold (HEAVY BASS)
    font_main2 = ImageFont.truetype(FUTURA_TTC, 140, index=2) # Bold (GYM MIX)
    
    text_sub = "HARDCORE WORKOUT"
    text_main1 = "HEAVY BASS"
    text_main2 = "GYM MIX"
    
    x = 80
    y_sub = 80
    y_main1 = 150
    y_main2 = 300
    
    # 1. グローレイヤー (Crimson Red Glow: 255, 10, 45)
    glow_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    
    g_draw.text((x, y_sub), text_sub, font=font_sub, fill=(255, 10, 45, 255))
    g_draw.text((x, y_main1), text_main1, font=font_main1, fill=(255, 10, 45, 255))
    g_draw.text((x, y_main2), text_main2, font=font_main2, fill=(255, 10, 45, 255))
    
    glow_wide = glow_layer.filter(ImageFilter.GaussianBlur(24))
    glow_tight = glow_layer.filter(ImageFilter.GaussianBlur(8))
    
    # 2. テキストレイヤー (影 + 輪郭 + 白文字)
    text_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    
    # 漆黒ドロップシャドウ (オフセット 8px)
    t_draw.text((x + 4, y_sub + 4), text_sub, font=font_sub, fill=(0, 0, 0, 240))
    t_draw.text((x + 8, y_main1 + 8), text_main1, font=font_main1, fill=(0, 0, 0, 255))
    t_draw.text((x + 8, y_main2 + 8), text_main2, font=font_main2, fill=(0, 0, 0, 255))
    
    # 赤のアウトライン (輪郭 2px)
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx != 0 or dy != 0:
                t_draw.text((x + dx, y_sub + dy), text_sub, font=font_sub, fill=(255, 20, 50, 180))
                t_draw.text((x + dx, y_main1 + dy), text_main1, font=font_main1, fill=(255, 20, 50, 180))
                t_draw.text((x + dx, y_main2 + dy), text_main2, font=font_main2, fill=(255, 20, 50, 180))
                
    # 純白ソリッドテキスト
    t_draw.text((x, y_sub), text_sub, font=font_sub, fill=(255, 70, 90, 255))
    t_draw.text((x, y_main1), text_main1, font=font_main1, fill=(255, 255, 255, 255))
    t_draw.text((x, y_main2), text_main2, font=font_main2, fill=(255, 255, 255, 255))
    
    # 合成
    composite = Image.alpha_composite(img, glow_wide)
    composite = Image.alpha_composite(composite, glow_tight)
    composite = Image.alpha_composite(composite, text_layer)
    
    composite.convert("RGB").save(OUT_PATH, quality=95)
    print(f"✅ High-Impact Thumbnail Generated: {OUT_PATH}")

if __name__ == "__main__":
    generate_bold_thumbnail()
