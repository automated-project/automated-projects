#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する ゲームアセット画像（サイバーパンク路地裏背景）生成スクリプト
"""
import os
import time
import subprocess
import sys

HF_TOKEN = os.getenv("HF_TOKEN", "")

def setup_environment():
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

def run_asset():
    import torch
    from diffusers import FluxPipeline
    from huggingface_hub import login

    login(token=HF_TOKEN, add_to_git_credential=False)

    print("🚀 FLUX.1-dev ロード中...", flush=True)
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
        token=HF_TOKEN
    )
    pipe.to("cuda")

    prompt = "2d game background art, high resolution, cyberpunk alleyway at night, glowing japanese and english neon signs, wet reflective asphalt streets, dark moody atmosphere, side-scroller parallax layered background, ultra-detailed pixel-perfect digital painting, 8k resolution, no characters."
    
    print("🎨 ゲームアセット画像生成中...", flush=True)
    t0 = time.time()
    img = pipe(
        prompt=prompt,
        guidance_scale=3.5,
        num_inference_steps=28,
        max_sequence_length=512,
        height=1080,
        width=1920,
        generator=torch.Generator("cuda").manual_seed(2024)
    ).images[0]

    out_path = "/content/cyberpunk_game_asset_bg.png"
    img.save(out_path, quality=100)
    print(f"✅ 生成成功: {out_path} (所要時間: {time.time() - t0:.2f}秒)", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_asset()
