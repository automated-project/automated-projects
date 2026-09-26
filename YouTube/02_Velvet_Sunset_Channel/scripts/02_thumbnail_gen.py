#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【Ch2 固有モジュール②】Velvet Sunset Audio サムネイル生成エンジン
- SignPainter 260px Glow 中央配置（サブタイトル完全排除）規格
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_ch2_thumbnail(bg_image_path: Path, output_thumb_path: Path, spec: dict) -> Path:
    output_thumb_path.parent.mkdir(parents=True, exist_ok=True)

    base_bg = Image.open(bg_image_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    
    font_path = spec.get("font_path", "/System/Library/Fonts/Supplemental/SignPainter.ttc")
    font_size = spec.get("font_size_main", 260)
    font_index = spec.get("font_index", 0)
    glow_color = tuple(spec.get("glow_color", [255, 140, 50]))
    text_color = tuple(spec.get("text_color", [255, 255, 255]))

    try:
        font_main = ImageFont.truetype(font_path, font_size, index=font_index)
    except Exception:
        font_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 150)

    # テキスト設定（Ch2 は Velvet Sunset 表示）
    main_text = "Velvet Sunset"

    dummy = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox = d_draw.textbbox((0, 0), main_text, font=font_main)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (1920 - w) // 2
    y = (1080 - h) // 2 - 20

    glow = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.text((x + 8, y + 10), main_text, font=font_main, fill=(0, 0, 0, 245))
    g_draw.text((x, y), main_text, font=font_main, fill=(*glow_color, 230))
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(18))

    composed = Image.alpha_composite(base_bg, glow_blurred)

    txt_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    t_draw.text((x, y), main_text, font=font_main, fill=(*text_color, 255))
    final_img = Image.alpha_composite(composed, txt_layer)

    final_img.convert("RGB").save(output_thumb_path, quality=95)
    print(f"✅ Generated Ch2 Thumbnail: {output_thumb_path}")
    return output_thumb_path

if __name__ == "__main__":
    print("Ch2 Thumbnail Generator Standalone Mode")
