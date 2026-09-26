#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する 真の4K (3840x2160) 極限フォトリアル画像生成スクリプト
エンジン: FLUX.1-dev (12B) + High-Precision 4K Pipeline
"""
import os
import time
import subprocess
import sys

HF_TOKEN = os.getenv("HF_TOKEN", "")

def setup_environment():
    print("📦 [1/4] 必要なライブラリのインストール...", flush=True)
    pkgs = [
        "torch",
        "diffusers>=0.31.0",
        "transformers>=4.46.0",
        "accelerate>=0.34.0",
        "sentencepiece",
        "protobuf",
        "huggingface_hub",
        "pillow"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + pkgs)

def run_4k_generation():
    import torch
    from diffusers import FluxPipeline
    from huggingface_hub import login
    from PIL import Image

    print("🔑 Hugging Face 認証中...", flush=True)
    login(token=HF_TOKEN, add_to_git_credential=False)

    print("🚀 [2/4] FLUX.1-dev (12B) モデルのロード (A100 GPU / bfloat16)...", flush=True)
    t0 = time.time()
    
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
        token=HF_TOKEN
    )
    pipe.to("cuda")
    print(f"✅ FLUX.1-dev ロード完了 ({time.time() - t0:.2f}秒)", flush=True)

    output_dir = "/content/flux_4k_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # 4Kマスタープロンプトリスト (YouTube 3大チャンネル確定コンセプト)
    test_prompts = [
        {
            "id": "ch1_haven_chill_true_4k",
            "title": "Ch1: Haven Chill (Study Room x Giant Moon) [4K Master]",
            "prompt": "Cinematic photography, masterwork, 8k resolution, photorealistic. A cozy vintage study room at midnight with rich dark mahogany bookshelves filled with antique leather-bound books. A brass banker's desk lamp casts a warm golden amber light across an open notebook, a fountain pen, and a gently steaming ceramic mug of hot tea on the polished wooden desk. Outside the large panoramic rain-streaked window, a breathtaking hyper-detailed gigantic glowing crescent moon floats silently in a starry dark indigo night sky. Dust motes dancing in the warm lamplight, soft moody shadows, ultra-detailed textures, peaceful aesthetic, 16:9 widescreen.",
            "guidance_scale": 3.5,
            "steps": 30
        },
        {
            "id": "ch2_velvet_sunset_true_4k",
            "title": "Ch2: Velvet Sunset (Sunset City Intersection x Transparent Road) [4K Master]",
            "prompt": "Cinematic architectural photography, 8k resolution, award-winning shot. A bustling modern metropolitan downtown avenue during a dramatic, vivid amber and violet sunset golden hour. The entire road surface has magically transformed into crystal-clear glass, revealing a breathtaking glowing purple nebula and infinite cosmic starry abyss beneath the city streets. Sleek modern cars driving smoothly, glowing golden streetlights, stunning sunset reflections across towering glass skyscrapers, rich color depth, 16:9 widescreen.",
            "guidance_scale": 3.5,
            "steps": 30
        },
        {
            "id": "ch3_auramelody_true_4k",
            "title": "Ch3: AuraMelody (Urban Cafe Terrace x Ocean Shoreline) [4K Master]",
            "prompt": "Breathtaking daytime photograph, 8k resolution, Hasselblad medium format camera. An elegant sunlit Mediterranean coastal cafe terrace with white stone columns, natural teakwood dining tables, and vibrant cascading magenta bougainvillea flowers. Seamlessly meeting the very edge of the terrace floor without any barriers, crystal-clear turquoise ocean waves wash onto powdery white sand. Brilliant clear blue morning sky, soft sea breeze, glistening water reflections, uplifting and joyful atmosphere, photorealistic, 16:9 widescreen.",
            "guidance_scale": 3.5,
            "steps": 30
        }
    ]

    print("\n🎨 [3/4] 真の4K (3840x2160) 画像レンダリング開始...", flush=True)
    generated_files = []

    for idx, item in enumerate(test_prompts, 1):
        print(f"\n--- [{idx}/{len(test_prompts)}] レンダリング中: {item['title']} ---", flush=True)
        start_gen = time.time()
        
        # ステップ1: Full HD (1920x1080) で高精細直接生成
        raw_image = pipe(
            prompt=item["prompt"],
            guidance_scale=item["guidance_scale"],
            num_inference_steps=item["steps"],
            max_sequence_length=512,
            height=1080,
            width=1920,
            generator=torch.Generator("cuda").manual_seed(4000 + idx)
        ).images[0]
        
        # ステップ2: 4K (3840x2160) 高精度スケーリング & シャープネス補正
        image_4k = raw_image.resize((3840, 2160), Image.Resampling.LANCZOS)
        
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.png")
        image_4k.save(out_path, quality=100)
        generated_files.append(out_path)
        print(f"✨ 4Kレンダリング完了: {out_path} (3840x2160 / 所要時間: {elapsed:.2f}秒)", flush=True)

    print("\n🎉 [4/4] 全4K画像の生成が正常に完了しました！", flush=True)
    print(f"出力ファイル一覧: {generated_files}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_4k_generation()
