#!/usr/bin/env python3
"""
Z-Image Turbo 10作品一括生成 & Lanczos 4K拡大 & CSV自動追記スクリプト
"""

import os
import csv
import time
import subprocess
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
CSV_PATH = os.path.join(BASE_DIR, "adobe_stock_submission.csv")
CSV_10_PATH = os.path.join(BASE_DIR, "adobe_stock_submission_10_set.csv")
COOL_DOWN_SECONDS = 75  # 8GB M1 Macのメモリ解放・発熱抑制のための待機時間（秒）

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

# 10作品の定義（テーマ、プロンプト、メタデータ）
items = [
    {
        "filename_base": "z_image_smart_factory",
        "prompt": "Wide angle interior of an advanced smart factory and precision manufacturing facility. Clean modern industrial space with geometric steel pipelines and subtle ambient blue indicator lighting. Ample empty clean copy space on the right side for text overlay. Static framing, depth of field, dramatic cinematic industrial lighting, no text, no logos, no trademark, no people, completely empty pristine space. 8k resolution, commercial corporate stock photo.",
        "title": "Clean smart factory interior with geometric steel pipes and ambient blue lighting, industrial copy space",
        "keywords": "smart factory, industrial, manufacturing, factory interior, automation, technology, engineering, steel pipes, clean, modern, industry, copy space, background, corporate, blue lighting, empty space",
        "category": 10
    },
    {
        "filename_base": "z_image_modern_atrium",
        "prompt": "Low angle architectural view of a modern corporate building atrium. Minimalist geometric glass facade and diagonal concrete pillars with bright natural daylight streaming through. Ample clean negative space on the left for business typography. Raytraced ambient occlusion, sharp soft shadows, no text, no logos, no recognizable brands, clean architectural aesthetic, 8k resolution stock photo.",
        "title": "Modern architectural building atrium with geometric glass facade and natural daylight, corporate copy space",
        "keywords": "architecture, building, atrium, corporate, modern, glass facade, daylight, office, urban, concrete pillars, interior, minimal, clean, copy space, background, business, geometric, structure",
        "category": 2
    },
    {
        "filename_base": "z_image_automated_warehouse",
        "prompt": "A high-tech automated logistics warehouse with orderly tall steel racks and clean polished concrete floors. Perspective view with vanishing point, ample empty copy space in the upper and right sections. Soft diffused warehouse lighting with subtle amber warning tones. No text, no letters, no logos on boxes, no workers, completely clean professional infrastructure, 8k resolution.",
        "title": "High-tech automated logistics warehouse with tall steel storage racks, supply chain background with copy space",
        "keywords": "warehouse, logistics, storage, distribution, supply chain, automated warehouse, industrial, storage racks, freight, inventory, concrete floor, clean, copy space, background, commercial",
        "category": 10
    },
    {
        "filename_base": "z_image_solar_energy",
        "prompt": "Geometric aerial perspective of clean photovoltaic solar panels arranged in modern patterns under clear blue sky with soft morning directional light. High-tech clean energy infrastructure with ample open sky copy space on the top and left side. Crisp reflections, no brand logos, no text, pristine environmental corporate aesthetic, 8k resolution.",
        "title": "Photovoltaic solar panels array under clear blue sky, renewable green energy background with copy space",
        "keywords": "solar panels, green energy, renewable energy, solar power, clean energy, photovoltaic, sustainability, environment, ecology, blue sky, technology, infrastructure, copy space, background, corporate",
        "category": 5
    },
    {
        "filename_base": "z_image_data_center",
        "prompt": "Clean modern server room corridor in an enterprise data center. Symmetrical rows of black matte server racks with subtle glowing cyan and blue optical fiber cables. Dramatic linear perspective with large empty copy space on the left. Highly detailed, cool futuristic tone, no text, no branding, commercial enterprise quality, 8k resolution.",
        "title": "Enterprise data center corridor with rows of server racks and glowing cyan fiber optics, IT copy space",
        "keywords": "data center, server room, server racks, IT infrastructure, cloud computing, cybersecurity, networking, optical fiber, technology, telecommunication, internet, big data, copy space, background, futuristic",
        "category": 19
    },
    {
        "filename_base": "z_image_liquid_gold_silk",
        "prompt": "Macro shot, shallow depth of field. Smooth organic curves of flowing liquid gold fabric drapery, elegant fluid waves, volumetric warm studio lighting. Ample empty copy space on the left side, clean negative space. Rich golden palette with high specular highlights and soft shadows. Static composition, raytraced ambient occlusion, no text, textless, 8k resolution commercial stock photo.",
        "title": "Flowing liquid gold fabric drapery with rich specular highlights, luxury golden background with copy space",
        "keywords": "liquid gold, gold, golden, fabric, silk, drapery, luxury, abstract, wave, metallic, fluid, elegant, wealth, copy space, background, minimal, smooth, macro, volumetric lighting, rich",
        "category": 8
    },
    {
        "filename_base": "z_image_marble_brass_geometry",
        "prompt": "Minimalist architectural wall detail made of pure white carrara marble featuring clean brushed brass inlay lines. Dramatic soft morning sunlight casting diagonal soft-edge shadows across the surface. Ample clean negative copy space on the right side. Raytraced ambient occlusion, no text, no logos, pristine architectural material aesthetic, 8k resolution.",
        "title": "Minimalist white carrara marble wall with brushed brass inlay lines and diagonal sunlight shadows, copy space",
        "keywords": "marble, white marble, brass, gold line, wall, architectural, texture, minimal, shadow, shadow play, sunlight, luxury, interior, modern, clean, surface, copy space, background, stone",
        "category": 2
    },
    {
        "filename_base": "z_image_biotech_laboratory",
        "prompt": "Minimalist futuristic biotechnology laboratory background. Clean frosted glass partitions and polished white work surfaces with subtle emerald ambient lighting glow. Symmetrical clinical composition with ample empty negative copy space on the left. Highly sterile and sophisticated atmosphere, no text, no logos, no equipment, no people, 8k resolution commercial stock photo.",
        "title": "Futuristic biotechnology laboratory background with frosted glass and subtle emerald glow, medical copy space",
        "keywords": "biotechnology, laboratory, biotech, science, research, cleanroom, frosted glass, medical, healthcare, clinical, technology, sterile, minimal, copy space, background, modern",
        "category": 16
    },
    {
        "filename_base": "z_image_water_caustics_sandstone",
        "prompt": "Topographic macro texture of natural warm sandstone surface. Delicate water caustics light ripples and soft fluid shadows dancing across the stone. Serene zen spa atmosphere with large clean copy space on the left side. Natural earth tones, soft morning directional lighting, raytraced ambient occlusion, no text, pristine organic aesthetic, 8k resolution.",
        "title": "Natural sandstone surface texture with dancing water caustics light reflection, peaceful spa background with copy space",
        "keywords": "sandstone, stone, water caustics, water reflection, texture, natural, organic, spa, wellness, zen, earth tones, peaceful, sunlight, ripple, surface, copy space, background, minimal",
        "category": 8
    },
    {
        "filename_base": "z_image_dark_titanium_liquid",
        "prompt": "Macro shot, shallow depth of field. Smooth organic curves of dark brushed titanium and viscous obsidian oil flowing gently. Seductive deep blue and gunmetal volumetric rim lighting, deep soft shadows, ambient occlusion. Ample empty copy space on the right side, clean negative space. Static composition, no text, textless, 8k resolution, cinematic commercial stock photo.",
        "title": "Dark brushed titanium and obsidian fluid sculpture with deep blue rim lighting, futuristic background with copy space",
        "keywords": "titanium, metal, metallic, obsidian, dark, black, abstract, fluid, sculpture, curves, blue lighting, volumetric, copy space, background, minimal, smooth, macro, futuristic, elegant",
        "category": 8
    }
]

# メインCSVの既存データ確認
existing_filenames = set()
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                existing_filenames.add(row[0])

# 10枚専用CSVの初期化（未作成ならヘッダー書き込み）
if not os.path.exists(CSV_10_PATH):
    with open(CSV_10_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Title", "Keywords", "Category", "Releases"])

existing_10_filenames = set()
with open(CSV_10_PATH, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            existing_10_filenames.add(row[0])

for idx, item in enumerate(items, 1):
    base_name = item["filename_base"]
    raw_png = os.path.join(OUTPUT_DIR, f"{base_name}.png")
    lanczos_png = os.path.join(UPSCALED_DIR, f"{base_name}_lanczos.png")
    csv_filename = f"{base_name}_lanczos.png"

    print(f"\n==========================================")
    print(f"[{idx}/10] Processing: {base_name}")
    print(f"==========================================")

    generated_now = False

    # 1. Z-Image Turbo で画像生成（未生成の場合のみ）
    if not os.path.exists(raw_png):
        print(f"Step 1: Generating image with Z-Image Turbo...")
        cmd = [
            "mflux-generate-z-image-turbo",
            "-q", "4",
            "--steps", "8",
            "--width", "1024",
            "--height", "576",
            "--low-ram",
            "--prompt", item["prompt"],
            "--output", raw_png
        ]
        start_t = time.time()
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"Error generating {base_name}, skipping.")
            continue
        print(f"Generated raw image in {time.time() - start_t:.1f}s")
        generated_now = True
    else:
        print(f"Raw image already exists: {raw_png}")

    # 2. 高品質Lanczos補間で4096x2304へアップスケール
    if not os.path.exists(lanczos_png):
        print(f"Step 2: Upscaling with Lanczos to 4096x2304...")
        img = Image.open(raw_png)
        upscaled = img.resize((4096, 2304), Image.Resampling.LANCZOS)
        upscaled.save(lanczos_png, format="PNG", compress_level=1)
        print(f"Saved: {lanczos_png} ({os.path.getsize(lanczos_png)/(1024*1024):.2f} MB)")
    else:
        print(f"Lanczos image already exists: {lanczos_png}")

    # 3. メインCSVファイルに追記（未登録の場合のみ）
    if csv_filename not in existing_filenames:
        print(f"Step 3: Appending to main CSV ({CSV_PATH})...")
        with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                csv_filename,
                item["title"],
                item["keywords"],
                item["category"],
                ""
            ])
        existing_filenames.add(csv_filename)
        print(f"Appended {csv_filename} to main CSV")

    # 4. 10枚専用CSVファイルに追記（未登録の場合のみ）
    if csv_filename not in existing_10_filenames:
        print(f"Step 4: Appending to 10-set CSV ({CSV_10_PATH})...")
        with open(CSV_10_PATH, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                csv_filename,
                item["title"],
                item["keywords"],
                item["category"],
                ""
            ])
        existing_10_filenames.add(csv_filename)
        print(f"Appended {csv_filename} to 10-set CSV")

    # 5. 1枚生成ごとのスリープ（冷却 & メモリ解放インターバル）
    if generated_now and idx < len(items):
        print(f"\n[Cooling Down] Sleeping for {COOL_DOWN_SECONDS} seconds to release GPU memory & cool down M1 chip...")
        time.sleep(COOL_DOWN_SECONDS)
        print("[Cooling Down] Ready for next image.")

print("\n==========================================")
print("All 10 items generated, upscaled, and registered to both CSVs!")
print(f"Main CSV: {CSV_PATH}")
print(f"10-Set CSV: {CSV_10_PATH}")
print("==========================================")
