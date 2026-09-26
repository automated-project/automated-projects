import os
import time
import subprocess
import torch
import pandas as pd
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from PIL import Image

# 1. ディレクトリ準備
WORK_DIR = "/content/adobe_sdxl_batch2"
RAW_DIR = os.path.join(WORK_DIR, "outputs")
UPSCALED_DIR = os.path.join(WORK_DIR, "outputs_upscaled")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

# 2. 新しい3パターンのプロンプト（実需・商用価値の高い異なるマテリアル）
PROMPTS = [
    {
        "id": "sdxl_dark_stone_gold_jewelry",
        "title": "Minimalist Dark Slate Stone and Brushed Gold Pedestal for Luxury Jewelry",
        "keywords": "pedestal, podium, jewelry display, dark slate, brushed gold, brass, luxury, minimalist, negative space, copy space, 3D render, dramatic lighting, ambient occlusion, black stone, architectural",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A luxury jewelry display pedestal. Sweeping smooth curved form and minimalist architectural installation made of dark polished stone and brushed gold metal. Single continuous shape, no complex overlapping. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion. Photorealistic commercial stock photography, 8k resolution."
    },
    {
        "id": "sdxl_liquid_acrylic_cosmetic",
        "title": "Clear Translucent Fluid Acrylic Sculpture Podium for Premium Perfume Display",
        "keywords": "acrylic, resin, translucent, liquid wave, clear, podium, cosmetic display, perfume, negative space, copy space, pastel gradient, refraction, smooth curve, minimalist, elegant, 3D render",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A premium cosmetics and perfume podium made of a single continuous flowing wave of clear translucent acrylic and frosted glass. Smooth curved liquid form, no complex intersections. Gentle soft studio lighting from a single light source, subtle caustic reflections, deep soft shadows, ambient occlusion. Clean, photorealistic commercial stock quality, 8k."
    },
    {
        "id": "sdxl_concrete_plant_shadow_wall",
        "title": "Minimalist Cool Grey Raw Concrete Wall with Cinematic Palm Leaf Shadows and Copy Space",
        "keywords": "concrete wall, backdrop, architectural, minimal, shadows, palm leaves, sunlight, window shadow, negative space, copy space, textured, clean, interior background, neutral grey, 3D",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. Subtle textured cool grey raw concrete wall surface backdrop. Dramatic cinematic lighting, soft blurred shadows of palm leaves and window blinds casting shadow play across the wall from the left. Deep ambient occlusion, clean empty space, minimalist architectural aesthetic, photorealistic, 8k resolution stock photo."
    }
]

# 3. SDXL-Lightning ロード（キャッシュ済みなので一瞬）
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

pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
print("✅ ロード完了！")

csv_rows = []

# 4. バッチ生成 & Lanczos 4K拡大
print("\n🎨 [2/3] 画像生成 ＆ 4Kアップスケールを開始します...")
for idx, p in enumerate(PROMPTS, 1):
    fid = p["id"]
    raw_file = f"{fid}.png"
    upscaled_file = f"{fid}_4k.jpg"
    raw_path = os.path.join(RAW_DIR, raw_file)
    upscaled_path = os.path.join(UPSCALED_DIR, upscaled_file)

    print(f"[{idx}/{len(PROMPTS)}] 生成中: {p['title'][:40]}...", flush=True)
    t0 = time.time()
    img = pipe(
        prompt=p["prompt"],
        negative_prompt="complex intersections, messy, blurry, low quality, artifacts, watermark, text, signature, distorted",
        width=1344,
        height=768,
        num_inference_steps=4,
        guidance_scale=0.0,
        generator=torch.Generator("cuda").manual_seed(3000 + idx)
    ).images[0]
    img.save(raw_path)
    print(f"   ↳ 生成完了 ({time.time() - t0:.1f}秒)！", flush=True)

    print(f"   ↳ Lanczos補間による4K超高解像度化中 (5376x3072px)...", flush=True)
    with Image.open(raw_path) as raw_img:
        w, h = raw_img.size
        upscaled_img = raw_img.resize((w * 4, h * 4), resample=Image.Resampling.LANCZOS)
        upscaled_img.save(upscaled_path, quality=95)
    print(f"   ↳ 4K化完了！", flush=True)

    csv_rows.append({
        "Filename": upscaled_file,
        "Title": p["title"],
        "Keywords": p["keywords"],
        "Category": 11
    })

# 5. CSV保存 & ZIP
print("\n📄 [3/3] メタデータCSV作成 & アーカイブ中...", flush=True)
csv_path = os.path.join(WORK_DIR, "submission_sdxl_batch2.csv")
pd.DataFrame(csv_rows).to_csv(csv_path, index=False, encoding="utf-8-sig")

zip_target = "/content/sdxl_batch2_result.zip"
subprocess.run(f"cd {WORK_DIR} && zip -r {zip_target} .", shell=True, check=True)
print(f"🎉 完了しました: {zip_target}", flush=True)
