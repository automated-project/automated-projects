#!/usr/bin/env python3
"""
Colab A100 / L4 GPU上で実行する Flux.1-schnell 超高速画像生成テストスクリプト
"""
import os
import time
import subprocess
import sys

def setup_environment():
    print("📦 [1/4] 必要なライブラリのインストール...")
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
    from diffusers import AutoPipelineForText2Image
    from PIL import Image

    print("🚀 [2/4] SDXL-Turbo / SDXL モデルのロード (A100 GPU / fp16)...")
    t0 = time.time()
    
    # 認証不要のオープン最高峰モデル: stabilityai/sdxl-turbo
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    pipe.to("cuda")
    print(f"✅ モデルロード完了 ({time.time() - t0:.2f}秒)", flush=True)

    # 出力ディレクトリ
    output_dir = "/content/flux_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # テストプロンプトリスト (YouTube 3大チャンネル確定コンセプト)
    test_prompts = [
        {
            "id": "ch1_haven_chill",
            "title": "Ch1: Haven Chill (Study Room x Giant Moon)",
            "prompt": "Masterpiece, ultra-detailed 8k, cinematic lighting. A warm cozy dark wooden study room with glowing vintage lamps and open books on a polished mahogany desk. Outside the large panoramic rain-streaked window, a breathtaking hyper-detailed gigantic glowing crescent moon floats silently in a starry dark indigo night sky. Atmospheric, soothing lofi aesthetic, peaceful solitude, high realism, 16:9."
        },
        {
            "id": "ch2_velvet_sunset",
            "title": "Ch2: Velvet Sunset (Sunset City Intersection x Transparent Road)",
            "prompt": "Masterpiece, ultra-detailed 8k, golden hour sunset lighting. A modern metropolitan downtown intersection during a brilliant purple and amber sunset. The road beneath is made of completely transparent crystal glass, revealing a breathtaking deep starry abyss beneath the city streets. Warm orange streetlights glowing, cinematic R&B mood, hyper-realistic architectural detail, 16:9."
        },
        {
            "id": "ch3_auramelody",
            "title": "Ch3: AuraMelody (Urban Cafe Terrace x Ocean Shoreline)",
            "prompt": "Masterpiece, ultra-detailed 8k, crisp morning sunshine lighting. A chic modern urban cafe terrace with wooden tables and blooming pastel flowers. Directly next to the terrace edge, crystal-clear turquoise ocean waves gently lap against pristine white sand under a brilliant clear blue sky. Refreshing breeze, uplifting atmosphere, vibrant colors, photorealistic, 16:9."
        }
    ]

    print("\n🎨 [3/4] 画像生成の開始 (SDXL Engine)...", flush=True)
    generated_files = []

    for idx, item in enumerate(test_prompts, 1):
        print(f"\n--- [{idx}/{len(test_prompts)}] 生成中: {item['title']} ---", flush=True)
        start_gen = time.time()
        
        # 16:9 (1024x576)
        image = pipe(
            prompt=item["prompt"],
            guidance_scale=0.0,
            num_inference_steps=4,
            height=576,
            width=1024,
            generator=torch.Generator("cuda").manual_seed(42 + idx)
        ).images[0]
        
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.png")
        image.save(out_path)
        generated_files.append(out_path)
        print(f"✨ 生成完了: {out_path} (所要時間: {elapsed:.2f}秒)", flush=True)

    print("\n🎉 [4/4] 全画像の生成が正常に完了しました！")
    print(f"出力ファイル一覧: {generated_files}")

if __name__ == "__main__":
    setup_environment()
    run_generation()
