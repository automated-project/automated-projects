#!/usr/bin/env python3
"""
Colab A100 (40GB VRAM) 上で実行する 世界最高峰 FLUX.1-dev (12Bパラメータ) 画像生成スクリプト
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
        "diffusers",
        "transformers",
        "accelerate",
        "sentencepiece",
        "protobuf",
        "huggingface_hub"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + pkgs)

def run_generation():
    import torch
    from diffusers import FluxPipeline
    from huggingface_hub import login
    from PIL import Image

    print("🔑 Hugging Face 認証中...", flush=True)
    login(token=HF_TOKEN, add_to_git_credential=False)

    print("🚀 [2/4] 世界最高峰モデル FLUX.1-dev (12B) のロード (A100 GPU / bfloat16)...", flush=True)
    t0 = time.time()
    
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
        token=HF_TOKEN
    )
    pipe.to("cuda")
    print(f"✅ FLUX.1-dev ロード完了 ({time.time() - t0:.2f}秒)", flush=True)

    # 出力ディレクトリ
    output_dir = "/content/flux_dev_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # 究極の超高精細プロンプトリスト (YouTube 3大チャンネル確定コンセプト)
    test_prompts = [
        {
            "id": "ch1_haven_chill_flux_dev",
            "title": "Ch1: Haven Chill (Study Room x Giant Moon)",
            "prompt": "Cinematic photography, masterwork, 8k resolution. A cozy and atmospheric vintage study room at midnight. Rich dark mahogany wood bookshelves filled with antique books, a brass banker's desk lamp casting a warm golden amber light across an open notebook, a fountain pen, and a gently steaming ceramic mug. Through a huge panoramic window, a breathtaking, hyper-realistic, colossal glowing crescent moon with visible craters hangs close in the starry deep indigo night sky. Dust motes dancing in the warm lamplight, soft moody shadows, ultra-detailed textures, peaceful aesthetic, 16:9 widescreen.",
            "guidance_scale": 3.5,
            "steps": 28
        },
        {
            "id": "ch2_velvet_sunset_flux_dev",
            "title": "Ch2: Velvet Sunset (Sunset City Intersection x Transparent Road)",
            "prompt": "Cinematic architectural photography, 8k resolution, award-winning shot. A bustling metropolitan downtown avenue during a dramatic, vivid amber and violet sunset golden hour. The entire road surface has magically transformed into crystal-clear glass, revealing a breathtaking glowing purple nebula and infinite cosmic starry abyss beneath the city streets. Sleek modern cars driving over the glass road, glowing golden streetlights, stunning sunset reflections across towering glass skyscrapers, rich color depth, 16:9 widescreen.",
            "guidance_scale": 3.5,
            "steps": 28
        },
        {
            "id": "ch3_auramelody_flux_dev",
            "title": "Ch3: AuraMelody (Urban Cafe Terrace x Ocean Shoreline)",
            "prompt": "Breathtaking daytime photograph, 8k resolution, Hasselblad medium format camera. An elegant sunlit Mediterranean coastal cafe terrace with white stone columns, natural teakwood dining tables, and vibrant cascading magenta bougainvillea flowers. Seamlessly meeting the very edge of the terrace floor without any barriers, crystal-clear turquoise ocean waves wash onto powdery white sand. Brilliant clear blue morning sky, soft sea breeze, glistening water reflections, uplifting and joyful atmosphere, photorealistic, 16:9 widescreen.",
            "guidance_scale": 3.5,
            "steps": 28
        }
    ]

    print("\n🎨 [3/4] FLUX.1-dev 究極レンダリング開始 (28 Steps / Guidance 3.5 / 1360x768)...", flush=True)
    generated_files = []

    for idx, item in enumerate(test_prompts, 1):
        print(f"\n--- [{idx}/{len(test_prompts)}] FLUX.1-dev レンダリング中: {item['title']} ---", flush=True)
        start_gen = time.time()
        
        # 16:9 (1360x768)
        image = pipe(
            prompt=item["prompt"],
            guidance_scale=item["guidance_scale"],
            num_inference_steps=item["steps"],
            max_sequence_length=512,
            height=768,
            width=1360,
            generator=torch.Generator("cuda").manual_seed(2026 + idx)
        ).images[0]
        
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.png")
        image.save(out_path)
        generated_files.append(out_path)
        print(f"✨ レンダリング完了: {out_path} (所要時間: {elapsed:.2f}秒)", flush=True)

    print("\n🎉 [4/4] FLUX.1-dev 全画像の最高峰レンダリングが完了しました！", flush=True)
    print(f"出力ファイル一覧: {generated_files}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_generation()
