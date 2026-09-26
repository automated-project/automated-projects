import os
import time
import subprocess
import torch
import pandas as pd
from huggingface_hub import login
from diffusers import FluxPipeline

# 1. 認証
HF_TOKEN = os.getenv("HF_TOKEN", "")
if HF_TOKEN:
    login(token=HF_TOKEN)

# 2. ディレクトリ準備
WORK_DIR = "/content/adobe_flux"
RAW_DIR = os.path.join(WORK_DIR, "outputs")
UPSCALED_DIR = os.path.join(WORK_DIR, "outputs_upscaled")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)

# 3. Adobe Stock 黄金ルールに準拠したプロンプト
PROMPTS = [
    {
        "id": "flux_marble_podium",
        "title": "Minimalist Carrara Marble Podium with Copy Space for Luxury Cosmetics",
        "keywords": "podium, pedestal, marble, carrara, minimalist, cosmetic, luxury, display, negative space, copy space, 3D render, elegant, white, clean, architectural",
        "prompt": "Asymmetrical composition, large empty negative space on the left, copy space for text. A minimalist architectural installation serving as a premium cosmetics podium. Single continuous ribbon-like sculpture made of carrara marble. Sweeping smooth curved form, no complex intersections. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion. 8k resolution, highly detailed, photorealistic commercial stock photography."
    },
    {
        "id": "flux_glass_aluminum_header",
        "title": "Modern Frosted Glass and Brushed Aluminum Banner with Clean Copy Space",
        "keywords": "tech banner, header, frosted glass, brushed aluminum, modern, futuristic, negative space, copy space, background, metallic, sleek, minimalist, architectural, 3D",
        "prompt": "Asymmetrical composition, large empty negative space on the right, copy space for text. A modern hero image banner for a high-tech enterprise. Minimalist architectural installation featuring a sweeping smooth curved form made of frosted smoked glass and brushed aluminum. No complex intersections. Dramatic directional lighting from a single light source, deep soft shadows, ambient occlusion. 8k resolution, photorealistic, commercial grade."
    }
]

# 4. モデルロード（T4 15GB VRAM 用に最適化）
print("🚀 [1/3] FLUX.1-schnell をロードしています（キャッシュ確認中）...")
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.float16
)
pipe.enable_sequential_cpu_offload()
print("✅ ロード完了！")

# 5. 生成 & 4K拡大ループ
realesrgan_bin = "/content/realesrgan-ncnn-vulkan-v0.2.0-ubuntu/realesrgan-ncnn-vulkan"
csv_rows = []

print("\n🎨 [2/3] FLUX.1 による画像生成を開始します...")
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
        width=1360,
        height=768,
        num_inference_steps=4,
        guidance_scale=0.0,
        generator=torch.Generator("cuda").manual_seed(100 + idx)
    ).images[0]
    img.save(raw_path)
    print(f"   ↳ 生成完了 ({time.time() - t0:.1f}秒)")

    print(f"   ↳ 4Kアップスケール中 (5440x3072px)...")
    cmd = f"{realesrgan_bin} -i {raw_path} -o {upscaled_path} -s 4"
    subprocess.run(cmd, shell=True, check=True)

    csv_rows.append({
        "Filename": upscaled_file,
        "Title": p["title"],
        "Keywords": p["keywords"],
        "Category": 11
    })

# 6. CSV保存 & ZIP
print("\n📄 [3/3] メタデータCSV作成 & アーカイブ中...")
csv_path = os.path.join(WORK_DIR, "submission_flux.csv")
pd.DataFrame(csv_rows).to_csv(csv_path, index=False, encoding="utf-8-sig")

zip_target = "/content/flux_result.zip"
subprocess.run(f"cd {WORK_DIR} && zip -r {zip_target} .", shell=True, check=True)
print(f"🎉 完了しました: {zip_target}")
