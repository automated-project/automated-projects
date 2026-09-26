#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG_PATH = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/cover_art/Gemini_Generated_Image_gzzyqfgzzyqfgzzy.jpeg")
OUT_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/output_videos/thumbnails")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

base_img = Image.open(BG_PATH).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)

# --- PATTERN 1A: Left-Side Vertical Stack (Far Left Dark Margin, Zero Face Overlap) ---
def make_thumb_left_vertical():
    img = base_img.copy()
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    gradient = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(560):
        alpha = int(210 * (1.0 - (x / 560.0) ** 1.3))
        g_draw.line([(x, 0), (x, 1080)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, gradient)
    
    font_large = ImageFont.truetype(FONT_IMPACT, 100)
    font_badge = ImageFont.truetype(FONT_ARIAL_BLACK, 30)
    font_sub = ImageFont.truetype(FONT_ARIAL_BLACK, 32)
    
    # 1. Top Mini Pill Badge
    draw.rounded_rectangle([50, 60, 390, 115], radius=10, fill=(220, 38, 38, 240), outline=(255, 255, 255, 220), width=2)
    draw.text((70, 72), "SUPER CRISP AUDIO", font=font_badge, fill=(255, 255, 255, 255))
    
    words = [
        ("1 HOUR", (255, 255, 255, 255)),
        ("GYM", (244, 114, 182, 255)),
        ("PHONK", (244, 114, 182, 255)),
        ("MIX", (216, 180, 254, 255))
    ]
    
    y_start = 145
    line_h = 95
    for i, (w, col) in enumerate(words):
        y = y_start + i * line_h
        draw.text((54, y + 4), w, font=font_large, fill=(0, 0, 0, 255))
        draw.text((50, y), w, font=font_large, fill=col)
        
    draw.rounded_rectangle([50, y_start + 4 * line_h + 15, 430, y_start + 4 * line_h + 70], radius=8, fill=(17, 24, 39, 230), outline=(147, 51, 234, 220), width=2)
    draw.text((68, y_start + 4 * line_h + 23), "DRIFT & HARDSTYLE", font=font_sub, fill=(216, 180, 254, 255))
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_01A_LEFT_VERTICAL.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

# --- PATTERN 1B: Left Bottom Placement (Completely below chin) ---
def make_thumb_left_bottom():
    img = base_img.copy()
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    b_grad = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(b_grad)
    for y in range(650, 1080):
        for x in range(0, 900):
            factor_y = (y - 650) / 430.0
            factor_x = 1.0 - (x / 900.0)
            alpha = int(220 * factor_y * (factor_x ** 0.8))
            bg_draw.point((x, y), fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, b_grad)
    
    font_large = ImageFont.truetype(FONT_IMPACT, 120)
    font_badge = ImageFont.truetype(FONT_ARIAL_BLACK, 32)
    font_sub = ImageFont.truetype(FONT_ARIAL_BLACK, 34)
    
    x_pos = 65
    draw.rounded_rectangle([x_pos, 700, x_pos + 380, 750], radius=10, fill=(220, 38, 38, 240), outline=(255, 255, 255, 220), width=2)
    draw.text((x_pos + 18, 708), "SUPER CRISP AUDIO", font=font_badge, fill=(255, 255, 255, 255))
    
    draw.text((x_pos + 5, 765), "1 HOUR", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, 760), "1 HOUR", font=font_large, fill=(255, 255, 255, 255))
    
    draw.text((x_pos + 5, 875), "GYM PHONK", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, 870), "GYM PHONK", font=font_large, fill=(244, 114, 182, 255))
    
    draw.rounded_rectangle([x_pos, 985, x_pos + 470, 1038], radius=8, fill=(17, 24, 39, 230), outline=(147, 51, 234, 220), width=2)
    draw.text((x_pos + 18, 992), "DRIFT & HARDSTYLE", font=font_sub, fill=(216, 180, 254, 255))
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_01B_LEFT_BOTTOM.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

make_thumb_left_vertical()
make_thumb_left_bottom()
