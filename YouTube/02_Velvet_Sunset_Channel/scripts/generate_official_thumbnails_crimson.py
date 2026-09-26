#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate High CTR Thumbnails using bg_highway_crimson.jpeg
- Matches the Dark Cyberpunk / Crimson Neon Highway aesthetic
- Outputs 3 distinct variations (Clean Art, Bold Gym Phonk, Aggressive Drift)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG_PATH = Path("/Users/base/Automated-Projects/YouTube/02_Gym_Phonk_Channel/cover_art/bg_highway_crimson.jpeg")
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

# --- Option A: Clean Art (Pure 1920x1080 Wallpaper) ---
def make_thumb_clean():
    out_path = OUT_DIR / "THUMBNAIL_01_CLEAN_ART.jpg"
    base_img.convert("RGB").save(out_path, quality=95)
    return out_path

# --- Option B: Left Bold Cyberpunk Stack (GYM PHONK) ---
def make_thumb_gym_phonk():
    img = base_img.copy()
    
    # Left dark gradient for text readability
    gradient = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(750):
        alpha = int(220 * (1.0 - (x / 750.0) ** 1.3))
        g_draw.line([(x, 0), (x, 1080)], fill=(3, 6, 12, alpha))
    img = Image.alpha_composite(img, gradient)
    
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font_large = ImageFont.truetype(FONT_IMPACT, 120)
    font_badge = ImageFont.truetype(FONT_ARIAL_BLACK, 28)
    font_sub = ImageFont.truetype(FONT_ARIAL_BLACK, 32)
    
    # 1. Top Badge (Crimson Red / Blood Red)
    draw_pill_badge(draw, "EXTREME BASS", font_badge, center_x=220, center_y=140, 
                    bg_color=(220, 20, 60, 240), text_color=(255, 255, 255, 255), 
                    border_color=(255, 100, 120, 220), pad_x=24, pad_y=10, radius=12)
    
    # 2. Main Large Text
    x_pos = 75
    y_start = 210
    line_h = 110
    
    lines = [
        ("1 HOUR", (255, 255, 255, 255)),
        ("GYM", (255, 45, 85, 255)),     # Crimson Neon Red
        ("PHONK", (255, 45, 85, 255)),
        ("MIX", (240, 240, 255, 255))
    ]
    
    for i, (text, col) in enumerate(lines):
        y = y_start + i * line_h
        # Heavy drop shadow
        draw.text((x_pos + 6, y + 6), text, font=font_large, fill=(0, 0, 0, 255))
        draw.text((x_pos, y), text, font=font_large, fill=col)
        
    # 3. Bottom Subtitle Badge
    draw_pill_badge(draw, "DRIFT & WORKOUT MOTIVATION", font_sub, center_x=310, center_y=710, 
                    bg_color=(10, 15, 26, 230), text_color=(255, 255, 255, 255), 
                    border_color=(255, 45, 85, 200), pad_x=26, pad_y=12, radius=10)
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_02_GYM_PHONK_CRIMSON.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

# --- Option C: Aggressive Drift Phonk (Late Night Highway) ---
def make_thumb_drift_phonk():
    img = base_img.copy()
    
    # Corner dark gradient
    gradient = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(800):
        alpha = int(230 * (1.0 - (x / 800.0) ** 1.2))
        g_draw.line([(x, 0), (x, 1080)], fill=(2, 4, 10, alpha))
    img = Image.alpha_composite(img, gradient)
    
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font_large = ImageFont.truetype(FONT_IMPACT, 125)
    font_badge = ImageFont.truetype(FONT_ARIAL_BLACK, 28)
    font_sub = ImageFont.truetype(FONT_ARIAL_BLACK, 32)
    
    # 1. Top Badge
    draw_pill_badge(draw, "SUPER CRISP AUDIO", font_badge, center_x=240, center_y=140, 
                    bg_color=(15, 23, 42, 240), text_color=(255, 255, 255, 255), 
                    border_color=(147, 51, 234, 220), pad_x=24, pad_y=10, radius=12)
    
    # 2. Main Large Text
    x_pos = 75
    y_start = 210
    
    # Line 1: 1 HOUR
    draw.text((x_pos + 6, y_start + 6), "1 HOUR", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, y_start), "1 HOUR", font=font_large, fill=(255, 255, 255, 255))
    
    # Line 2: AGGRESSIVE
    draw.text((x_pos + 6, y_start + 115 + 6), "AGGRESSIVE", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, y_start + 115), "AGGRESSIVE", font=font_large, fill=(255, 45, 85, 255))
    
    # Line 3: DRIFT PHONK
    draw.text((x_pos + 6, y_start + 230 + 6), "DRIFT PHONK", font=font_large, fill=(0, 0, 0, 255))
    draw.text((x_pos, y_start + 230), "DRIFT PHONK", font=font_large, fill=(255, 255, 255, 255))
    
    # 3. Bottom Subtitle Badge
    draw_pill_badge(draw, "LATE NIGHT HIGHWAY DRIVE", font_sub, center_x=300, center_y=610, 
                    bg_color=(220, 20, 60, 235), text_color=(255, 255, 255, 255), 
                    border_color=(255, 120, 140, 220), pad_x=26, pad_y=12, radius=10)
    
    img = Image.alpha_composite(img, overlay)
    out_path = OUT_DIR / "THUMBNAIL_03_AGGRESSIVE_DRIFT.jpg"
    img.convert("RGB").save(out_path, quality=95)
    return out_path

if __name__ == "__main__":
    t1 = make_thumb_clean()
    t2 = make_thumb_gym_phonk()
    t3 = make_thumb_drift_phonk()
    print("[✓] Successfully generated thumbnails:")
    print("  1 (Clean Art):", t1)
    print("  2 (Gym Phonk Crimson):", t2)
    print("  3 (Aggressive Drift):", t3)
