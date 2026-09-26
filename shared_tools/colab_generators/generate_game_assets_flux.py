#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する ゲームアセット2D画像（背景・テクスチャ・UI・アイコン）完全自動生成スクリプト
モデル: FLUX.1-dev (12B) / 高解像度＆アルファ最適化
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

def run_game_asset_generation():
    import torch
    from diffusers import FluxPipeline
    from huggingface_hub import login
    from PIL import Image

    print("🔑 Hugging Face 認証中...", flush=True)
    login(token=HF_TOKEN, add_to_git_credential=False)

    print("🚀 [2/4] FLUX.1-dev (12B) モデルロード中 (A100 GPU / bfloat16)...", flush=True)
    t0 = time.time()
    
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
        token=HF_TOKEN
    )
    pipe.to("cuda")
    print(f"✅ FLUX.1-dev ロード完了 ({time.time() - t0:.2f}秒)", flush=True)

    output_dir = "/content/game_assets_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # ゲーム開発用特化プロンプト（itch.io / Gumroad 販売用アセット）
    asset_prompts = [
        {
            "id": "game_bg_cyberpunk_street",
            "title": "2D Game Background: Cyberpunk Alley",
            "width": 1920, "height": 1080,
            "prompt": "2d game background art, high resolution, cyberpunk alleyway at night, glowing neon signs in japanese and english, wet reflective asphalt streets, dark moody atmosphere, side-scroller parallax layered background, ultra-detailed pixel-perfect digital painting, 8k resolution, no characters.",
            "steps": 28
        },
        {
            "id": "game_bg_fantasy_dungeon",
            "title": "2D Game Background: Dark Fantasy Crystal Cave",
            "width": 1920, "height": 1080,
            "prompt": "2d game background art, dark fantasy underground crystal cave dungeon, glowing cyan and violet magical crystals embedded in ancient stone walls, underground waterfall, dramatic lighting, side-scrolling platformer background, high quality concept art, 8k resolution, clean composition.",
            "steps": 28
        },
        {
            "id": "game_ui_icons_rpg_potions",
            "title": "Game UI Asset: RPG Magic Potions Icon Sheet",
            "width": 1024, "height": 1024,
            "prompt": "game ui asset sheet, set of 4 different glowing magical potion bottles, Health Potion, Mana Potion, Poison Potion, Elixir of Strength, isometric view, isolated on pure solid black background, vibrant colors, glossy glass reflection, 2d game icon art, highly detailed.",
            "steps": 28
        },
        {
            "id": "game_texture_seamless_sci_fi_metal",
            "title": "Game Texture: Seamless Sci-Fi Metal Floor",
            "width": 1024, "height": 1024,
            "prompt": "top-down game texture, seamless tileable sci-fi metal floor panel, dark steel plating with glowing blue neon LED stripes, heavy industrial rust and scratches, high-resolution texture map for 3d games and 2d games, PBR material style.",
            "steps": 28
        }
    ]

    print("\n🎨 [3/4] ゲームアセット画像生成開始...", flush=True)
    generated_files = []

    for idx, item in enumerate(asset_prompts, 1):
        print(f"\n--- [{idx}/{len(asset_prompts)}] 生成中: {item['title']} ({item['width']}x{item['height']}) ---", flush=True)
        start_gen = time.time()
        
        image = pipe(
            prompt=item["prompt"],
            guidance_scale=3.5,
            num_inference_steps=item["steps"],
            max_sequence_length=512,
            height=item["height"],
            width=item["width"],
            generator=torch.Generator("cuda").manual_seed(1000 + idx)
        ).images[0]
        
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.png")
        image.save(out_path, quality=100)
        generated_files.append(out_path)
        print(f"✨ アセット生成完了: {out_path} (所要時間: {elapsed:.2f}秒)", flush=True)

    # ZIP化して保存
    print("\n📦 [4/4] ゲームアセットZIPパッケージを作成中...", flush=True)
    zip_path = "/content/game_assets_pack_colab.zip"
    subprocess.check_call(["zip", "-q", "-j", zip_path] + generated_files)
    print(f"🎉 全アセット生成＆パッケージング完了！ 出力ZIP: {zip_path}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_game_asset_generation()
