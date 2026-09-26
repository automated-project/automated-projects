#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【Ch2 固有モジュール②】Velvet Sunset Audio サムネイル生成エンジン (新デザイン確定規格)
- スタイル: シネマティック ＆ リュクス
- フォント: Didot Bold または Bodoni 72 Bold
- 文字組み: ALL CAPS + かなり広い文字間隔 (V  E  L  V  E  T    S  U  N  S  E  T)
- カラー: 高級オフホワイト (#F4F4F2 / 244, 244, 242)
- シャドウ: #000000, xy: (0,0), opacity: 50%, ぼかし: 文字高さと同等 (広範囲ソフトシャドウ)
- 配置: 画面中央ジャスト (260px基準)
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEXT_COLOR = (244, 244, 242, 255)  # 高級オフホワイト #F4F4F2

def generate_ch2_thumbnail(bg_image_path: Path, output_thumb_path: Path, font_variant: str = "didot") -> Path:
    output_thumb_path.parent.mkdir(parents=True, exist_ok=True)

    base_bg = Image.open(bg_image_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    
    font_size = 260
    if font_variant.lower() == "bodoni":
        font_path = "/System/Library/Fonts/Supplemental/Bodoni 72.ttc"
        font_index = 1
    else:
        font_path = "/System/Library/Fonts/Supplemental/Didot.ttc"
        font_index = 1

    try:
        font_main = ImageFont.truetype(font_path, font_size, index=font_index)
    except Exception:
        font_path = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
        font_main = ImageFont.truetype(font_path, font_size)

    text = "VELVET SUNSET"

    dummy = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox = d_draw.textbbox((0, 0), text, font=font_main)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (1920 - w) // 2
    y = (1080 - h) // 2 - 20

    # 1. 広範囲中心ソフトシャドウ (#000000, xy:0, opacity: 50%, blur: 文字高さと同等)
    shadow_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((x, y), text, font=font_main, fill=(0, 0, 0, 140))  # ~55% 不透明度
    
    blur_radius = max(30, int(h * 0.7))  # 文字高さに合わせた超広範囲ソフトぼかし
    shadow_blurred = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))

    # 2. テキスト本体レイヤー
    txt_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(txt_layer)
    t_draw.text((x, y), text, font=font_main, fill=TEXT_COLOR)

    # 3. 合成
    composed = Image.alpha_composite(base_bg, shadow_blurred)
    final_img = Image.alpha_composite(composed, txt_layer)

    final_img.convert("RGB").save(output_thumb_path, quality=95)
    print(f"✅ Generated Ch2 Thumbnail ({font_variant}): {output_thumb_path.name}")
    return output_thumb_path

if __name__ == "__main__":
    bg = Path("/Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/cover_art/Gemini_Generated_Image_cxs9rncxs9rncxs9.jpeg")
    out1 = Path("/Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/cover_art/thumb_ch2_didot.jpg")
    out2 = Path("/Users/base/Automated-Projects/YouTube/02_Velvet_Sunset_Channel/cover_art/thumb_ch2_bodoni.jpg")
    generate_ch2_thumbnail(bg, out1, "didot")
    generate_ch2_thumbnail(bg, out2, "bodoni")
