"""
Google Colab用 ゲームアセット画像一括生成パイプライン
(Game Assets Generator for Google Colab)

【特徴】
1. Colab GPUを活用したローカル生成 (Diffusers / SDXL / PixelArt)
2. または Google Imagen 3 / Gemini API を使った高解像度アセット生成
3. 自動背景透過（rembg）＆ マルチ解像度リサイズ（512x512, 256x256, 128x128）
4. itch.io / Gumroad 納品用 ZIP自動パッケージング
"""

# ==========================================
# 1. Google Colab 依存パッケージのインストール
# ==========================================
# !pip install -q diffusers transformers accelerate torch torchvision rembg pillow google-genai

import os
import zipfile
from PIL import Image
import torch

# 出力ディレクトリ作成
OUTPUT_DIR = "generated_game_assets"
PACK_DIR = os.path.join(OUTPUT_DIR, "icons_and_textures")
os.makedirs(PACK_DIR, exist_ok=True)

# ==========================================
# 2. 生成アセットのプロンプトリスト定義
# ==========================================
ASSET_PROMPTS = [
    {
        "filename": "potion_health_red",
        "prompt": "pixel art, 2d game item icon, glowing red healing potion in a glass bottle, cork stopper, clean white background, isolated, sharp edges",
    },
    {
        "filename": "potion_mana_blue",
        "prompt": "pixel art, 2d game item icon, mystical glowing blue mana potion in an ornate glass flask, clean white background, isolated",
    },
    {
        "filename": "sword_legendary_fire",
        "prompt": "pixel art, 2d game weapon icon, flaming legendary broadsword with golden hilt, fire aura, clean white background, isolated",
    },
    {
        "filename": "shield_iron_emblem",
        "prompt": "pixel art, 2d game armor icon, sturdy medieval iron shield with engraved lion emblem, clean white background, isolated",
    },
    {
        "filename": "crystal_gem_emerald",
        "prompt": "pixel art, 2d game item icon, shiny glowing emerald green gemstone, faceted cut, clean white background, isolated",
    },
    {
        "filename": "magic_spellbook_dark",
        "prompt": "pixel art, 2d game item icon, ancient spellbook with glowing purple runes, leather cover, clean white background, isolated",
    }
]

# ==========================================
# 3. ローカルAI (Stable Diffusion / Diffusers) による生成
# ==========================================
def generate_with_local_diffusion():
    """Google ColabのGPUを使用してローカルで画像を生成"""
    from diffusers import StableDiffusionPipeline

    print("🚀 ローカルAIモデルをロード中...")
    model_id = "runwayml/stable-diffusion-v1-5"  # または "nerogar/pixel-art-diffusion" 等
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16
    ).to("cuda" if torch.cuda.is_available() else "cpu")

    pipe.safety_checker = None  # パフォーマンス向上

    for item in ASSET_PROMPTS:
        print(f"🎨 生成中: {item['filename']}...")
        image = pipe(
            prompt=item["prompt"],
            negative_prompt="blurry, realistic photo, watermark, text, messy, dark background, complex scene",
            num_inference_steps=30,
            guidance_scale=7.5,
            height=512,
            width=512
        ).images[0]

        save_path = os.path.join(PACK_DIR, f"{item['filename']}_raw.png")
        image.save(save_path)
        print(f"   ✓ 保存完了: {save_path}")

# ==========================================
# 4. 背景自動透過 & マルチ解像度リサイズ
# ==========================================
def process_and_package_assets():
    """背景除去、複数解像度書き出し、ZIPアーカイブ化"""
    try:
        from rembg import remove
        has_rembg = True
    except ImportError:
        print("⚠️ rembgがインストールされていないため、透過処理をスキップします。")
        has_rembg = False

    sizes = [512, 256, 128, 64]
    
    for item in ASSET_PROMPTS:
        raw_path = os.path.join(PACK_DIR, f"{item['filename']}_raw.png")
        if not os.path.exists(raw_path):
            continue

        with Image.open(raw_path) as img:
            # 透過処理
            if has_rembg:
                img_transparent = remove(img)
            else:
                img_transparent = img.convert("RGBA")

            # 各解像度で出力
            for size in sizes:
                resized = img_transparent.resize((size, size), Image.NEAREST if "pixel" in item["prompt"] else Image.LANCZOS)
                size_dir = os.path.join(OUTPUT_DIR, f"{size}x{size}")
                os.makedirs(size_dir, exist_ok=True)
                out_path = os.path.join(size_dir, f"{item['filename']}_{size}.png")
                resized.save(out_path)

    # ZIPパッケージング
    zip_path = "Game_Assets_Icons_Pack.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(OUTPUT_DIR):
            for file in files:
                if not file.endswith("_raw.png"):  # 完成版のみ同梱
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, OUTPUT_DIR)
                    zipf.write(full_path, arcname)

    print(f"\n📦 【納品ZIPパッケージ完成】: {zip_path}")

if __name__ == "__main__":
    generate_with_local_diffusion()
    process_and_package_assets()
