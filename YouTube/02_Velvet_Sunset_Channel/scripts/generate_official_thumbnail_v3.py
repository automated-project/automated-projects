#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate High CTR Official Thumbnails - Refined & Balanced Layouts
Eliminates text overflowing badges, matches color palette of the image (Neon Violet/Cyan/Pink glow).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG_PATH = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/cover_art/Gemini_Generated_Image_gzzyqfgzzyqfgzzy.jpeg")
OUT_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/output_videos/thumbnails")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

base_img = Image.open(BG_PATH).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)

def draw_pill_badge(draw, text, font, center_x, center_y, bg_color, text_color, border_color=None, pad_x=24, pad_y=12, radius=12):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x0 = center_x - tw // 2 - pad_x
    x1 = center_x + tw // 2 + pad_x
    y0 = center_y - th // 2 - pad_y
    y1 = center_y + th // 2 + pad_y
    
    if border_color:
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg_color, outline=border_color, width=2)
    else:
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg_color)
        
    draw.text((center_x - tw // 2, center_y - th // 2 - bbox[1] + (th - (bbox[3]-bbox[1]))//2), text, font=font, fill=text_color)
    return (x0, y0, x1, y1)

# --- PATTERN 1: Left Vertical Balanced (Perfect Margins & Palette Matched) ---
def make_thumb_left_vertical_fixed():
    img = base_img.copy()
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Smooth left shadow that blends with the dark background
    gradient = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(620):
        alpha = int(210 * (1.0 - (x / 620.0) ** 1.4))
        g_draw.line([(x, 0), (x, 1080)], fill=(5, 5, 12, alpha))
    img = Image.alpha_composite(img, gradient)
    
    font_large = ImageFont.truetype(FONT_IMPACT, 110)
    font_badge = ImageFont.truetype(FONT_ARIAL_BLACK, 28)
    font_sub = ImageFont.truetype(FONT_ARIAL_BLACK, 30)
    
    # 1. Top Pill Badge (Auto padded, Cyan/Purple theme to match neon lights)
    draw_pill_badge(draw, "SUPER CRISP AUDIO", font_badge, center_x=220, center_y=110, 
                    bg_color=(225, 29, 72, 235), text_color=(255, 255, 255, 255), 
                    border_color=(254, 205, 211, 220), pad_x=24, pad_y=10, radius=12)
    
    # 2. Main Large Text Vertically Stacked (x=60)
    x_pos = 65
    y_start = 170
    line_h = 100
    
    lines = [
        ("1 HOUR", (255, 255, 255, 255)),
        ("GYM", (244, 114, 182, 255)),
        ("PHONK", (244, 114, 182, 255)),
        ("MIX", (192, 132, 252, 255))
    ]
    
    for i, (text, col) in enumerate(lines):
        y = y_start + i * line_h
        # Glow / Shadow
        draw.text((x_pos + 4, y + 4), text, font=font_large, fill=(0, 0, 0, 255))
        draw.text((x_pos, y), text, font=font_large, fill=col)
        
    # 3. Bottom Subtitle Badge (Auto padded)
    draw_pill_badge(draw, "DRIFT & HARDSTYLE", font_sub, center_x=225, center_y=615, 
                    bg_color=(15, 23, 42, 230), text_color=(216, 180, 254, 255), 
                    border_color=(168, 85, 247, 200), pad_x=26, pad_y=12, radius=10)
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_01A_PERFECT.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

# --- PATTERN 2: Left-Bottom Floating Stack (Under chin, 100% clear of face) ---
def make_thumb_left_bottom_fixed():
    img = base_img.copy()
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Dark corner blend
    b_grad = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(b_grad)
    for y in range(600, 1080):
        for x in range(0, 950):
            factor_y = (y - 600) / 480.0
            factor_x = 1.0 - (x / 950.0)
            alpha = int(220 * factor_y * (factor_x ** 0.8))
            bg_draw.point((x, y), fill=(5, 5, 12, alpha))
    img = Image.alpha_composite(img, b_grad)
    
    font_large = ImageFont.truetype(FONT_IMPACT, 125)
    font_badge = ImageFont.truetype(FONT_ARIAL_BLACK, 28)
    font_sub = ImageFont.truetype(FONT_ARIAL_BLACK, 30)
    
    x_pos = 75
    # 1. Top Badge
    draw_pill_badge(draw, "SUPER CRISP AUDIO", font_badge, center_x=x_pos + 160, center_y=690, 
                    bg_color=(225, 29, 72, 235), text_color=(255, 255, 255, 255), 
                    border_color=(254, 205, 211, 220), pad_x=22, pad_y=10, radius=10)
    
    # 2. Main text
    draw.text((x_pos + 5, 745), "1 HOUR", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, 740), "1 HOUR", font=font_large, fill=(255, 255, 255, 255))
    
    draw.text((x_pos + 5, 860), "GYM PHONK", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, 855), "GYM PHONK", font=font_large, fill=(244, 114, 182, 255))
    
    # 3. Sub Badge
    draw_pill_badge(draw, "DRIFT & HARDSTYLE", font_sub, center_x=x_pos + 200, center_y=995, 
                    bg_color=(15, 23, 42, 230), text_color=(216, 180, 254, 255), 
                    border_color=(168, 85, 247, 200), pad_x=24, pad_y=12, radius=10)
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_01B_PERFECT.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

p1 = make_thumb_left_vertical_fixed()
p2 = make_thumb_left_bottom_fixed()

print("[✓] Regenerated perfect thumbnails:")
print("  1:", p1)
print("  2:", p2)
