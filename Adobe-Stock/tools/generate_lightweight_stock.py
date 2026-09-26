#!/usr/bin/env python3
"""
【超軽量・高画質 Adobe Stock 自動生成パイプライン】
生成: SSD-1B（1.3Bパラメータ / メモリ消費約2.5GBでM1 8GBでも超安全）
超解像: Real-ESRGAN x4plus（AIが微細テクスチャを描き足しながら4096pxへ拡大）
"""

import os
import sys
import time
import subprocess
import csv
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

# Adobe Stock 黄金ルールプロンプト（実需・商用価値重視）
PROMPTS = [
    {
        "id": "ssd_marble_podium",
        "title": "Minimalist Carrara Marble Podium with Large Negative Space for Luxury Cosmetics",
        "keywords": "podium, pedestal, marble, carrara, minimalist, cosmetic, luxury, display, negative space, copy space, 3D render, elegant, white, architectural, smooth curved form, clean, raytracing",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A minimalist architectural installation serving as a premium cosmetics podium. Single continuous ribbon-like sculpture made of carrara marble. Sweeping smooth curved form, no complex intersections. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion. 8k resolution, photorealistic commercial stock photography."
    },
    {
        "id": "ssd_dark_stone_jewelry",
        "title": "Minimalist Dark Slate Stone and Brushed Gold Pedestal for Luxury Jewelry",
        "keywords": "pedestal, podium, jewelry display, dark slate, brushed gold, brass, luxury, minimalist, negative space, copy space, 3D render, dramatic lighting, ambient occlusion, black stone, architectural",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A luxury jewelry display pedestal. Sweeping smooth curved form and minimalist architectural installation made of dark polished stone and brushed gold metal. Single continuous shape, no complex overlapping. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion. Photorealistic commercial stock photography, 8k resolution."
    }
]

def load_ssd_pipeline():
    print("🚀 [1/3] 超軽量AIモデル（SSD-1B / 1.3B）をメモリに展開しています...")
    # Apple Silicon (MPS) または CPU
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"   ↳ 実行デバイス: {device.upper()}（Apple Silicon GPU）")
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "segmind/SSD-1B",
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        use_safetensors=True,
        variant="fp16" if device == "mps" else None
    )
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to(device)
    print("✅ ロード完了！（メモリ消費は約2.5GB、8GB Macでも完全安全圏です）\n")
    return pipe

def run_ai_upscale(input_path, output_path):
    """Real-ESRGAN x4plus による AI 超解像アップスケール"""
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
    print("🎨 【SSD-1B × Real-ESRGAN】ローカル安全・高解像度パイプライン")
    print("==================================================")

    pipe = load_ssd_pipeline()
    new_rows = []

    for idx, p in enumerate(PROMPTS, 1):
        fid = p["id"]
        timestamp = int(time.time())
        raw_name = f"{fid}_{timestamp}.png"
        up_name = f"{fid}_{timestamp}_ai4k.jpg"

        raw_path = os.path.join(OUTPUTS_DIR, raw_name)
        up_path = os.path.join(UPSCALED_DIR, up_name)

        print(f"[{idx}/{len(PROMPTS)}] 生成中: {p['title'][:40]}...")
        t0 = time.time()

        # 1. SSD-1B で画像生成 (1024x576: 16:9比率)
        img = pipe(
            prompt=p["prompt"],
            negative_prompt="complex intersections, messy, blurry, low quality, artifacts, watermark, text, signature, distorted",
            width=1024,
            height=576,
            num_inference_steps=20,
            guidance_scale=7.5
        ).images[0]
        img.save(raw_path)
        print(f"   ↳ 生成完了 ({time.time() - t0:.1f}秒)！ outputs/{raw_name}")

        # 2. Real-ESRGAN による AI ディテール描き足しアップスケール（4096x2304px）
        t1 = time.time()
        print(f"   ↳ Real-ESRGAN AI超解像アップスケール中 (4096x2304px)...")
        run_ai_upscale(raw_path, up_path)
        print(f"   ↳ AIアップスケール完了 ({time.time() - t1:.1f}秒)！ outputs_upscaled/{up_name}")

        new_rows.append({
            "Filename": up_name,
            "Title": p["title"],
            "Keywords": p["keywords"],
            "Category": 11
        })
        time.sleep(2)

    # 3. CSV更新
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
        writer = csv.DictWriter(f, fieldnames=["Filename", "Title", "Keywords", "Category"], extrasaction="ignore")
        writer.writeheader()
        writer.writerows(existing_rows + new_rows)

    print(f"✅ {len(new_rows)} 件のメタデータを追記しました！")
    print("\n==================================================")
    print("🎉 すべての処理が安全・確実に完了しました！")
    print("==================================================")

if __name__ == "__main__":
    main()
