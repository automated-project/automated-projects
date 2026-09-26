#!/usr/bin/env python3
"""
【Adobe Stock 完全自動生成パイプライン】
世界最高峰画像AI「FLUX.1」によるクラウド生成 ＆ 高品質Lanczos 4K拡大 ＆ 出品用CSV自動追記
"""

import os
import sys
import time
import random
import urllib.parse
import urllib.request
import csv
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
MAIN_CSV = os.path.join(BASE_DIR, "adobe_stock_submission.csv")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

# Adobe Stock 黄金ルールに準拠したプロンプトリスト
PROMPTS_DATA = [
    {
        "id": "flux_marble_podium_cosmetic",
        "title": "Minimalist Carrara Marble Podium with Large Negative Space for Luxury Cosmetics",
        "keywords": "podium, pedestal, marble, carrara, minimalist, cosmetic, luxury, display, negative space, copy space, 3D render, elegant, white, clean, architectural, smooth curved form, raytracing",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A minimalist architectural installation serving as a premium cosmetics podium. Single continuous ribbon-like sculpture made of carrara marble. Sweeping smooth curved form, no complex intersections. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion. 8k resolution, highly detailed, photorealistic commercial stock photography."
    },
    {
        "id": "flux_frosted_glass_tech_banner",
        "title": "Modern Frosted Glass and Brushed Aluminum Banner with Clean Copy Space",
        "keywords": "tech banner, header, frosted glass, brushed aluminum, modern, futuristic, negative space, copy space, background, metallic, sleek, minimalist, architectural, 3D, corporate",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A modern hero image banner for a high-tech enterprise. Minimalist architectural installation featuring a sweeping smooth curved form made of frosted smoked glass and brushed aluminum. No complex intersections. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion. 8k resolution, photorealistic, commercial grade."
    },
    {
        "id": "flux_matte_plaster_ribbon_organic",
        "title": "Serene Matte White Plaster Ribbon Sculpture Background for Organic Beauty Products",
        "keywords": "plaster, sculpture, organic, beauty, background, white, matte, minimalist, podium, copy space, soft shadows, texture, spa, wellness, smooth, architectural, clean",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A serene background for organic beauty products. Single continuous ribbon-like sculpture made of matte white plaster. Sweeping smooth curved form, minimalist architectural installation. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion, elegant, clean stock photo."
    }
]

def generate_flux_image(prompt: str, target_path: str, width: int = 1344, height: int = 768):
    """FLUX.1 クラウドエンジンから画像を直接取得"""
    seed = random.randint(10000, 9999999)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&seed={seed}&nologo=true"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=90) as resp, open(target_path, "wb") as f:
        f.write(resp.read())

def upscale_lanczos_4k(input_path: str, output_path: str, scale: int = 4):
    """高品質Lanczos補間で4K（4096px以上）に拡大"""
    with Image.open(input_path) as img:
        w, h = img.size
        # 4倍拡大（1344x768 ➔ 5376x3072: 約1,650万画素）
        new_w, new_h = w * scale, h * scale
        upscaled = img.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
        upscaled.save(output_path, quality=95)

def main():
    print("==================================================")
    print("🎨 【Adobe Stock】世界最高峰 FLUX.1 自動生成パイプライン")
    print("==================================================")

    new_csv_rows = []

    for idx, item in enumerate(PROMPTS_DATA, 1):
        fid = item["id"]
        timestamp = int(time.time())
        raw_filename = f"{fid}_{timestamp}.jpg"
        upscaled_filename = f"{fid}_{timestamp}_4k.jpg"

        raw_path = os.path.join(OUTPUTS_DIR, raw_filename)
        upscaled_path = os.path.join(UPSCALED_DIR, upscaled_filename)

        print(f"\n[{idx}/{len(PROMPTS_DATA)}] 生成中: {item['title'][:45]}...")
        t0 = time.time()
        
        # 1. FLUX.1 生成
        generate_flux_image(item["prompt"], raw_path)
        print(f"   ↳ FLUX.1 生成完了 ({time.time() - t0:.1f}秒)！ outputs/{raw_filename}")

        # 2. 4Kアップスケール（Lanczos）
        t1 = time.time()
        upscale_lanczos_4k(raw_path, upscaled_path, scale=4)
        print(f"   ↳ 4K超高画質化完了 ({time.time() - t1:.1f}秒)！ outputs_upscaled/{upscaled_filename}")

        new_csv_rows.append({
            "Filename": upscaled_filename,
            "Title": item["title"],
            "Keywords": item["keywords"],
            "Category": 11
        })
        time.sleep(2) # 礼儀正しい待機

    # 3. 出品用CSVの更新
    print("\n📄 出品用CSV（adobe_stock_submission.csv）を更新しています...")
    existing_filenames = set()
    existing_rows = []
    
    if os.path.exists(MAIN_CSV):
        with open(MAIN_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing_filenames.add(r.get("Filename"))
                existing_rows.append(r)

    with open(MAIN_CSV, mode="w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["Filename", "Title", "Keywords", "Category"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing_rows + new_csv_rows)

    print(f"✅ {added} 件のメタデータを {MAIN_CSV} に追記しました！")
    print("\n==================================================")
    print("🎉 すべての処理が完璧に完了しました！")
    print(f"・元画像保存先: {OUTPUTS_DIR}")
    print(f"・4K画像保存先: {UPSCALED_DIR}")
    print(f"・出品CSV:     {MAIN_CSV}")
    print("==================================================")

if __name__ == "__main__":
    main()
