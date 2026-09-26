import os
import time
import subprocess
import torch
import pandas as pd
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

# 1. ディレクトリ準備
WORK_DIR = "/content/adobe_sdxl"
RAW_DIR = os.path.join(WORK_DIR, "outputs")
UPSCALED_DIR = os.path.join(WORK_DIR, "outputs_upscaled")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

# 2. Adobe Stock 黄金ルールに準拠したプロンプト
PROMPTS = [
    {
        "id": "sdxl_marble_podium",
        "title": "Minimalist Carrara Marble Podium with Large Negative Space for Luxury Cosmetics",
        "keywords": "podium, pedestal, marble, carrara, minimalist, cosmetic, luxury, display, negative space, copy space, 3D render, elegant, white, architectural, smooth curved form, clean, raytracing",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A minimalist architectural installation serving as a premium cosmetics podium. Single continuous ribbon-like sculpture made of carrara marble. Sweeping smooth curved form, no complex intersections. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion, photorealistic commercial stock photography, 8k resolution."
    },
    {
        "id": "sdxl_glass_aluminum_header",
        "title": "Modern Frosted Glass and Brushed Aluminum Banner with Clean Copy Space",
        "keywords": "tech banner, header, frosted glass, brushed aluminum, modern, futuristic, negative space, copy space, background, metallic, sleek, minimalist, architectural, 3D",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A modern hero image banner for a high-tech enterprise. Minimalist architectural installation featuring a sweeping smooth curved form made of frosted smoked glass and brushed aluminum. No complex intersections. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion, photorealistic, commercial grade, 8k."
    },
    {
        "id": "sdxl_organic_plaster_ribbon",
        "title": "Serene Matte White Plaster Ribbon Sculpture Background for Organic Beauty Products",
        "keywords": "plaster, sculpture, organic, beauty, background, white, matte, minimalist, podium, copy space, soft shadows, texture, spa, wellness, smooth, architectural",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A serene background for organic beauty products. Single continuous ribbon-like sculpture made of matte white plaster. Sweeping smooth curved form, minimalist architectural installation. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion, elegant, clean stock photo."
    }
]

# 3. SDXL-Lightning モデルのロード（T4 15GB GPU 最適化・爆速4ステップ推論）
print("🚀 [1/3] SDXL-Lightning を GPU (Tesla T4) にロードしています...")
base_model = "stabilityai/stable-diffusion-xl-base-1.0"
repo = "ByteDance/SDXL-Lightning"
ckpt = "sdxl_lightning_4step_unet.safetensors"

unet = UNet2DConditionModel.from_config(base_model, subfolder="unet").to("cuda", torch.float16)
unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device="cuda"))
pipe = StableDiffusionXLPipeline.from_pretrained(
    base_model,
    unet=unet,
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

# 最適なサンプラ設定
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
print("✅ ロード完了！VRAMに完全展開されました。")

realesrgan_bin = "/content/realesrgan-ncnn-vulkan-v0.2.0-ubuntu/realesrgan-ncnn-vulkan"
csv_rows = []

# 4. バッチ生成 & 4Kアップスケール
print("\n🎨 [2/3] 画像生成 ＆ 4Kアップスケールを開始します...")
for idx, p in enumerate(PROMPTS, 1):
    fid = p["id"]
    raw_file = f"{fid}.png"
    upscaled_file = f"{fid}_4k.jpg"
    raw_path = os.path.join(RAW_DIR, raw_file)
    upscaled_path = os.path.join(UPSCALED_DIR, upscaled_file)

    print(f"[{idx}/{len(PROMPTS)}] 生成中: {p['title'][:40]}...")
    t0 = time.time()
    img = pipe(
        prompt=p["prompt"],
        negative_prompt="complex intersections, messy, blurry, low quality, artifacts, watermark, text, signature, distorted",
        width=1344,
        height=768,
        num_inference_steps=4,
        guidance_scale=0.0,
        generator=torch.Generator("cuda").manual_seed(2026 + idx)
    ).images[0]
    img.save(raw_path)
    print(f"   ↳ 生成完了 ({time.time() - t0:.1f}秒)！")

    print(f"   ↳ Lanczos補間による4K超高解像度化中 (5376x3072px)...")
    from PIL import Image
    with Image.open(raw_path) as raw_img:
        w, h = raw_img.size
        # 4倍（5376x3072: 約1,650万画素）へ高品質Lanczos拡大
        upscaled_img = raw_img.resize((w * 4, h * 4), resample=Image.Resampling.LANCZOS)
        upscaled_img.save(upscaled_path, quality=95)
    print(f"   ↳ 4K化完了！")

    csv_rows.append({
        "Filename": upscaled_file,
        "Title": p["title"],
        "Keywords": p["keywords"],
        "Category": 11
    })

# 5. CSV保存 & ZIP
print("\n📄 [3/3] メタデータCSV作成 & アーカイブ中...")
csv_path = os.path.join(WORK_DIR, "submission_sdxl.csv")
pd.DataFrame(csv_rows).to_csv(csv_path, index=False, encoding="utf-8-sig")

zip_target = "/content/sdxl_result.zip"
subprocess.run(f"cd {WORK_DIR} && zip -r {zip_target} .", shell=True, check=True)
print(f"🎉 完了しました: {zip_target}")
