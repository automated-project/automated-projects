#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【Ch1 固有モジュール②】Haven Chill Audio サムネイル生成エンジン (新デザイン確定規格)
- スタイル: レトロ ＆ アナログ
- フォント: Courier New Bold または American Typewriter Bold
- 文字組み: 単語の頭だけ大文字 (Title Case) -> "Haven Chill"
- カラー: 高級オフホワイト (#F4F4F2 / 244, 244, 242)
- シャドウ: #000000, xy: (0,0), opacity: 50%, ぼかし: 文字高さと同等 (広範囲ソフトシャドウ)
- 配置: 画面中央ジャスト (260px基準)
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEXT_COLOR = (244, 244, 242, 255)  # 高級オフホワイト #F4F4F2

def generate_ch1_thumbnail(bg_image_path: Path, output_thumb_path: Path, font_variant: str = "courier") -> Path:
    output_thumb_path.parent.mkdir(parents=True, exist_ok=True)

    base_bg = Image.open(bg_image_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    
    font_size = 260
    if font_variant.lower() == "typewriter":
        font_path = "/System/Library/Fonts/Supplemental/AmericanTypewriter.ttc"
        font_index = 1
    else:
        font_path = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
        font_index = 0

    try:
        if font_path.endswith(".ttc"):
            font_main = ImageFont.truetype(font_path, font_size, index=font_index)
        else:
            font_main = ImageFont.truetype(font_path, font_size)
    except Exception:
        font_path = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
        font_main = ImageFont.truetype(font_path, font_size)

    text = "Haven Chill"

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
    print(f"✅ Generated Ch1 Thumbnail ({font_variant}): {output_thumb_path.name}")
    return output_thumb_path

if __name__ == "__main__":
    bg = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel/cover_art/Bioluminescent_jellyfish_study.jpeg")
    out1 = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel/cover_art/thumb_ch1_courier.jpg")
    out2 = Path("/Users/base/Automated-Projects/YouTube/01_Chill_Channel/cover_art/thumb_ch1_typewriter.jpg")
    generate_ch1_thumbnail(bg, out1, "courier")
    generate_ch1_thumbnail(bg, out2, "typewriter")
