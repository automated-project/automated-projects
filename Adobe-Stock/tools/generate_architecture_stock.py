#!/usr/bin/env python3
"""
【建築・建造物バリエーション検証スクリプト】
SSD-1B（1.3B・ステップ数12に最適化で高速化） × Real-ESRGAN x4plus
建物の直線、ガラス、柱、タイルの目地など「細かい部分の破綻」を徹底検証
"""

import os
import sys
import time
import subprocess
import csv
import gc
import torch
from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
MAIN_CSV = os.path.join(BASE_DIR, "adobe_stock_submission.csv")
REALESRGAN_BIN = os.path.join(BASE_DIR, "tools", "realesrgan", "realesrgan-ncnn-vulkan")
REALESRGAN_MODELS = os.path.join(BASE_DIR, "tools", "realesrgan", "models")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

# 建築・細かい構造の検証プロンプト3選（Adobe Stock実需重視・3:7余白ルール）
PROMPTS = [
    {
        "id": "arch_minimal_concrete_hall",
        "title": "Minimalist Modern Concrete Architectural Gallery Hall with Large Negative Space",
        "keywords": "modern architecture, concrete wall, architectural hall, minimalist interior, glass window, courtyard, gallery, empty space, copy space, 3D render, ambient light, sunlight shadows, brutalist, clean lines",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A minimalist modern architectural gallery hall with smooth raw exposed concrete walls and polished concrete floor. Floor-to-ceiling glass windows on the left with clean architectural frames. Natural daylight casting geometric shadows across the interior. Sharp straight lines, no warped walls, no distorted geometry. Photorealistic architectural stock photography, 8k resolution."
    },
    {
        "id": "arch_luxury_marble_atrium",
        "title": "Luxury Minimalist Marble Entrance Atrium with Symmetrical Columns and Copy Space",
        "keywords": "luxury atrium, marble columns, architectural lobby, elegant, white marble, grand entrance, high ceiling, copy space, negative space, geometric, clean lines, interior architecture, 3D render",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A luxury architectural entrance atrium. Elegant minimalist structural columns made of white Carrara marble with clean straight fluting. Polished limestone floor with subtle seamless grid seams. Recessed linear ceiling lighting. No crooked pillars, perfectly aligned perspective, sharp architectural details. High-end commercial stock photography, 8k."
    },
    {
        "id": "arch_tech_lobby_wood_louvers",
        "title": "Modern Corporate Lobby Interior with Vertical Wooden Louvers and Clean Negative Space",
        "keywords": "corporate lobby, wooden louvers, timber acoustic slats, tech office, minimalist interior, glass facade, reception background, copy space, negative space, linear design, architectural 3D",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. Modern enterprise headquarters lobby interior. Accent wall featuring perfectly parallel vertical oak wood acoustic louvers and sleek matte black aluminum trim. Seamless polished terrazzo floor, soft diffused architectural lighting. Precise parallel lines, clean craftsmanship, no repetitive errors or wavy textures. Commercial stock photography, 8k resolution."
    }
]

def load_pipeline():
    print("🚀 [1/3] SSD-1B モデルをメモリにロードしています...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"   ↳ 実行デバイス: {device.upper()} (Apple Silicon GPU)")
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "segmind/SSD-1B",
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        use_safetensors=True,
        variant="fp16" if device == "mps" else None
    )
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to(device)
    # メモリ節約（VRAMをこまめに片付ける）
    pipe.enable_attention_slicing()
    print("✅ ロード完了！（ステップ数12で高速・美麗にチューニング済み）\n")
    return pipe

def run_ai_upscale(input_path, output_path):
    cmd = [
        REALESRGAN_BIN,
        "-i", input_path,
        "-o", output_path,
        "-s", "4",
        "-n", "realesrgan-x4plus",
        "-m", REALESRGAN_MODELS
    ]
    subprocess.run(cmd, check=True)

def main():
    print("==================================================")
    print("🏛️ 【建築・構造物ディテール検証】SSD-1B × Real-ESRGAN")
    print("==================================================")

    pipe = load_pipeline()
    new_rows = []

    for idx, p in enumerate(PROMPTS, 1):
        fid = p["id"]
        timestamp = int(time.time())
        raw_name = f"{fid}_{timestamp}.png"
        up_name = f"{fid}_{timestamp}_ai4k.jpg"

        raw_path = os.path.join(OUTPUTS_DIR, raw_name)
        up_path = os.path.join(UPSCALED_DIR, up_name)

        print(f"[{idx}/{len(PROMPTS)}] 生成中: {p['title'][:42]}...")
        t0 = time.time()

        # 1. 画像生成（ステップ数12で時間短縮＆ディテール維持）
        img = pipe(
            prompt=p["prompt"],
            negative_prompt="warped lines, crooked pillars, distorted geometry, blurry, artifacts, noisy, watermark, signature, messy, low quality, deformed structure",
            width=1024,
            height=576,
            num_inference_steps=12,
            guidance_scale=7.5
        ).images[0]
        img.save(raw_path)
        gen_time = time.time() - t0
        print(f"   ↳ 生成完了 ({gen_time:.1f}秒)！ outputs/{raw_name}")

        # 2. Real-ESRGAN AI超解像アップスケール（4096x2304px）
        t1 = time.time()
        print(f"   ↳ Real-ESRGAN による直線・ディテール再構築中 (4096x2304px)...")
        run_ai_upscale(raw_path, up_path)
        up_time = time.time() - t1
        print(f"   ↳ AIアップスケール完了 ({up_time:.1f}秒)！ outputs_upscaled/{up_name}")

        new_rows.append({
            "Filename": up_name,
            "Title": p["title"],
            "Keywords": p["keywords"],
            "Category": 11
        })

        # 3. メモリ強制解放（Macの熱・負荷をリセット）
        gc.collect()
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
        print("   ↳ メモリキャッシュ解放完了\n")
        time.sleep(3)

    # 4. CSV更新
    print("📄 出品用CSV（adobe_stock_submission.csv）を更新しています...")
    existing_filenames = set()
    existing_rows = []
    if os.path.exists(MAIN_CSV):
        with open(MAIN_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing_filenames.add(r.get("Filename"))
                existing_rows.append(r)

    with open(MAIN_CSV, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Filename", "Title", "Keywords", "Category"], extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing_rows + new_rows)

    print(f"✅ {len(new_rows)} 件のメタデータを追記しました！")
    print("==================================================")
    print("🎉 建築バリエーションの生成・AIアップスケールが完了しました！")
    print("==================================================")

if __name__ == "__main__":
    main()
