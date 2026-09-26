# -*- coding: utf-8 -*-
"""
Ch 2 (PhonkForge Audio) Official Thumbnail Generator
- 100% Exact Official Design: Futura Medium (index=0), Top-Left (x=75, y1=70), Crimson Neon Glow (28px + 10px Gaussian Blur) + 2px Black Stroke
- Zero Pill Badges (文字枠・ピルバッジ完全排除)
# - 仕様書: .agents/rules/01_youtube_automation.md Section 4 (サムネイル確定テーブル)
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path("/Users/base/Automated-Projects/YouTube/02_Phonk_Channel")
COVER_ART = BASE_DIR / "cover_art" / "bg_underground_gym.jpeg"
OUT_DIR = BASE_DIR / "output_videos" / "thumbnails"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_TTC = "/System/Library/Fonts/Supplemental/Futura.ttc"
WIDTH, HEIGHT = 1920, 1080

def draw_spaced_text(draw, x, y, text, font, fill, spacing=3, stroke_w=0, stroke_f=None):
    curr_x = x
    for char in text:
        if stroke_w > 0:
            draw.text((curr_x, y), char, font=font, fill=fill, stroke_width=stroke_w, stroke_fill=stroke_f)
        else:
            draw.text((curr_x, y), char, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), char, font=font)
        curr_x += (bbox[2] - bbox[0]) + spacing
    return curr_x

def generate_exact_thumbnail(cover_image_path, output_path, line1="GYM PHONK", line2="HEAVY BASS", line_sub="30 MIN AGGRESSIVE WORKOUT MIX"):
    # 1. 背景リサイズ & 左上グラデーション
    base_im = Image.open(cover_image_path).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    gradient = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    for x in range(950):
        for y in range(650):
            fx, fy = 1.0 - (x / 950.0), 1.0 - (y / 650.0)
            alpha = int(180 * (fx * 0.7 + fy * 0.3) ** 1.3)
            g_draw.point((x, y), fill=(5, 5, 10, alpha))
    base_im = Image.alpha_composite(base_im, gradient)

    # 2. フォント読み込み (Futura Medium index=0)
    font_main = ImageFont.truetype(FONT_TTC, 118, index=0) # Futura Medium 118px
    font_sub = ImageFont.truetype(FONT_TTC, 36, index=0)   # Futura Medium 36px

    x, y1 = 75, 70
    y2 = y1 + 125
    y_sub = y2 + 130

    # 3. 鮮烈な真紅ネオングロー (28px + 10px Gaussian Blur)
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    for _ in range(4):
        draw_spaced_text(g_draw, x, y1, line1, font_main, (255, 10, 45, 255), spacing=4, stroke_w=8, stroke_f=(255, 10, 45, 255))
        draw_spaced_text(g_draw, x, y2, line2, font_main, (255, 10, 45, 255), spacing=4, stroke_w=8, stroke_f=(255, 10, 45, 255))
        draw_spaced_text(g_draw, x, y_sub, line_sub, font_sub, (255, 30, 60, 220), spacing=3, stroke_w=4, stroke_f=(255, 30, 60, 220))

    glow_wide = glow.filter(ImageFilter.GaussianBlur(28))
    glow_mid = glow.filter(ImageFilter.GaussianBlur(10))
    base_im = Image.alpha_composite(base_im, glow_wide)
    base_im = Image.alpha_composite(base_im, glow_mid)

    # 4. 細い黒アウトライン ＋ ピュアホワイト文字
    txt_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    draw_spaced_text(t_draw, x, y1, line1, font_main, (255, 255, 255, 255), spacing=4, stroke_w=2, stroke_f=(0, 0, 0, 255))
    draw_spaced_text(t_draw, x, y2, line2, font_main, (255, 255, 255, 255), spacing=4, stroke_w=2, stroke_f=(0, 0, 0, 255))
    draw_spaced_text(t_draw, x, y_sub, line_sub, font_sub, (255, 255, 255, 255), spacing=3, stroke_w=2, stroke_f=(0, 0, 0, 255))

    base_im = Image.alpha_composite(base_im, txt_layer)
    base_im.convert("RGB").save(output_path, quality=95)
    print(f"✅ Generated exact thumbnail: {output_path}")

def generate_all_thumbnails():
    # パターン 1: GYM PHONK // HEAVY BASS (公式採用)
    p1 = OUT_DIR / "THUMBNAIL_01_EXACT_FUTURA_GYM_PHONK.jpg"
    generate_exact_thumbnail(COVER_ART, p1, "GYM PHONK", "HEAVY BASS", "30 MIN AGGRESSIVE WORKOUT MIX")

    # パターン 2: HARDCORE // DISCIPLINE
    p2 = OUT_DIR / "THUMBNAIL_02_EXACT_FUTURA_DISCIPLINE.jpg"
    generate_exact_thumbnail(COVER_ART, p2, "HARDCORE", "DISCIPLINE", "30 MIN MOTIVATION & HEAVY BASS")

    # パターン 3: Pure Clean Art (文字なし)
    p3 = OUT_DIR / "THUMBNAIL_03_PURE_GYM_ART.jpg"
    Image.open(COVER_ART).convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).save(p3, quality=95)
    print(f"✅ Pattern 3: {p3}")

if __name__ == "__main__":
    generate_all_thumbnails()
