#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【Ch3 固有モジュール②】AuraMelody Audio サムネイル生成エンジン (動的Auto-Fit確定規格)
- スタイル: クリーン ＆ モダン
- フォント: Avenir Next (Heavy/Bold) または Futura Bold
- 文字組み: ALL CAPS
- カラー: 高級オフホワイト (#F4F4F2 / 244, 244, 242)
- シャドウ: #000000, xy: (0,0), opacity: 50%, ぼかし: 文字高さと同等
- 配置: 画面中央ジャスト (文字長に応じた動的Auto-Fit: ターゲット幅 1480px / 画面幅の約77%)
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEXT_COLOR = (244, 244, 242, 255)  # 高級オフホワイト #F4F4F2
TARGET_WIDTH = 1480  # 画面幅1920pxに対し左右に適度な余白（約77%幅）を残すターゲットサイズ
MAX_FONT_SIZE = 260
MIN_FONT_SIZE = 120

def get_auto_fit_font(text: str, font_path: str, font_index: int = 0, target_width: int = TARGET_WIDTH, max_size: int = MAX_FONT_SIZE, min_size: int = MIN_FONT_SIZE):
    """
    指定テキストが target_width に収まるようフォントサイズを動的にスケール調整する
    """
    dummy = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    
    best_font = None
    best_size = max_size

    for font_size in range(max_size, min_size - 1, -2):
        try:
            if font_path.endswith(".ttc"):
                font = ImageFont.truetype(font_path, font_size, index=font_index)
            else:
                font = ImageFont.truetype(font_path, font_size)
        except Exception:
            font = ImageFont.load_default()

        bbox = d_draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= target_width or font_size == min_size:
            best_font = font
            best_size = font_size
            break

    return best_font, best_size

def generate_ch3_thumbnail(bg_image_path: Path, output_thumb_path: Path, text: str = "AURAMELODY", font_variant: str = "avenir") -> Path:
    output_thumb_path.parent.mkdir(parents=True, exist_ok=True)

    base_bg = Image.open(bg_image_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    
    if font_variant.lower() == "futura":
        font_path = "/System/Library/Fonts/Supplemental/Futura.ttc"
        font_index = 2  # Bold
    else:
        font_path = "/System/Library/Fonts/Avenir Next.ttc"
        font_index = 0  # Heavy/Bold

    font_main, calculated_size = get_auto_fit_font(text, font_path, font_index, target_width=TARGET_WIDTH)

    dummy = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox = d_draw.textbbox((0, 0), text, font=font_main)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (1920 - w) // 2
    y = (1080 - h) // 2 - 20

    # シャドウ
    shadow_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((x, y), text, font=font_main, fill=(0, 0, 0, 140))
    
    blur_radius = max(30, int(h * 0.6))
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))

    # テキスト本体
    txt_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    t_draw.text((x, y), text, font=font_main, fill=TEXT_COLOR)

    composed = Image.alpha_composite(base_bg, shadow_blurred)
    final_img = Image.alpha_composite(composed, txt_layer)

    final_img.convert("RGB").save(output_thumb_path, quality=95)
    print(f"✅ Generated Ch3 Thumbnail ({font_variant}, Auto-Fit size={calculated_size}px, width={w}px): {output_thumb_path.name}")
    return output_thumb_path

if __name__ == "__main__":
    bg = Path("/Users/base/Downloads/Rooftop_garden_with_ocean_pool_2K_20260925062535.jpg")
    out1 = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/cover_art/thumb_ch3_avenir.jpg")
    out2 = Path("/Users/base/Automated-Projects/YouTube/03_Uplifting_Channel/cover_art/thumb_ch3_futura.jpg")
    if bg.exists():
        generate_ch3_thumbnail(bg, out1, "MORNING VIBES", "avenir")
        generate_ch3_thumbnail(bg, out2, "MORNING VIBES", "futura")
