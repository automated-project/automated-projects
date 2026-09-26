#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する 最高峰高画質・フォトリアリズム画像生成スクリプト
モデル: Playground v2.5 (1024px Aesthetic / EDMScheduler)
"""
import os
import time
import subprocess
import sys

def setup_environment():
    print("📦 [1/4] 必要なライブラリのインストール...", flush=True)
    pkgs = [
        "torch",
        "diffusers",
        "transformers",
        "accelerate",
        "sentencepiece",
        "protobuf"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + pkgs)

def run_generation():
    import torch
    from diffusers import DiffusionPipeline
    from PIL import Image

    print("🚀 [2/4] 最高峰モデル Playground v2.5 (1024px Aesthetic) のロード (A100 GPU / fp16)...", flush=True)
    t0 = time.time()
    
    pipe = DiffusionPipeline.from_pretrained(
        "playgroundai/playground-v2.5-1024px-aesthetic",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    pipe.to("cuda")
    print(f"✅ モデルロード完了 ({time.time() - t0:.2f}秒)", flush=True)

    # 出力ディレクトリ
    output_dir = "/content/hq_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # 妥協なき高精細プロンプトリスト (YouTube 3大チャンネル確定コンセプト)
    test_prompts = [
        {
            "id": "ch1_haven_chill_hq",
            "title": "Ch1: Haven Chill (Study Room x Giant Moon)",
            "prompt": "Masterpiece, 8k resolution, ultra-photorealistic, highly detailed. A dimly lit cozy vintage study room with richly textured mahogany bookshelves, warm amber glow from an antique brass desk lamp illuminating an open leather-bound book and a steaming cup of tea. Through a large condensation-fogged window, a stunning hyper-detailed gigantic glowing crescent moon illuminates a distant dark indigo city skyline under a starry night. Cinematic lighting, soft shadows, peaceful solitude, octane render aesthetic, 16:9 widescreen.",
            "guidance_scale": 3.0,
            "steps": 30
        },
        {
            "id": "ch2_velvet_sunset_hq",
            "title": "Ch2: Velvet Sunset (Sunset City Intersection x Transparent Road)",
            "prompt": "Masterpiece, 8k resolution, photorealistic architectural photography. A bustling modern metropolitan downtown avenue during a dramatic amber and deep violet golden hour sunset. The entire asphalt road has seamlessly transformed into crystal-clear glass, revealing a breathtaking glowing nebula and deep cosmic abyss beneath the city streets. Warm orange streetlights, long dramatic sunset reflections on glass skyscrapers, sleek vehicles gliding smoothly, high dynamic range, 16:9.",
            "guidance_scale": 3.0,
            "steps": 30
        },
        {
            "id": "ch3_auramelody_hq",
            "title": "Ch3: AuraMelody (Urban Cafe Terrace x Ocean Shoreline)",
            "prompt": "Masterpiece, 8k resolution, breathtakingly crisp morning sunlight. An elegant coastal cafe terrace with white stone architecture, polished teakwood tables, lush hanging bougainvillea flowers in pastel pink and white. Directly meeting the edge of the polished marble terrace floor, crystalline turquoise ocean waves break gently onto fine white sand under a vast radiant morning sky. Gentle sea breeze, glistening water highlights, uplifting atmosphere, Hasselblad medium format look, 16:9.",
            "guidance_scale": 3.0,
            "steps": 30
        }
    ]

    print("\n🎨 [3/4] 最高画質レンダリング開始 (30 Steps / EDMScheduler / 1344x768)...", flush=True)
    generated_files = []

    for idx, item in enumerate(test_prompts, 1):
        print(f"\n--- [{idx}/{len(test_prompts)}] 高品質レンダリング中: {item['title']} ---", flush=True)
        start_gen = time.time()
        
        # 16:9 ワイド高精細解像度 (1344x768)
        image = pipe(
            prompt=item["prompt"],
            guidance_scale=item["guidance_scale"],
            num_inference_steps=item["steps"],
            height=768,
            width=1344,
            generator=torch.Generator("cuda").manual_seed(100 + idx)
        ).images[0]
        
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.png")
        image.save(out_path)
        generated_files.append(out_path)
        print(f"✨ レンダリング完了: {out_path} (所要時間: {elapsed:.2f}秒)", flush=True)

    print("\n🎉 [4/4] 全画像の最高画質レンダリングが完了しました！", flush=True)
    print(f"出力ファイル一覧: {generated_files}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_generation()
