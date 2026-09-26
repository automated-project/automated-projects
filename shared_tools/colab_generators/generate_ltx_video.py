#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する 真の世界最高峰 Image-to-Video 動画生成スクリプト
モデル: Lightricks/LTX-Video (DiT Architecture / 高解像度 / 121 Frames / 25 FPS)
"""
import os
import time
import subprocess
import sys

HF_TOKEN = os.getenv("HF_TOKEN", "")

def setup_environment():
    print("📦 [1/4] 必要な最新ライブラリのインストール...", flush=True)
    pkgs = [
        "torch",
        "diffusers>=0.31.0",
        "transformers>=4.46.0",
        "accelerate>=0.34.0",
        "sentencepiece",
        "imageio",
        "imageio-ffmpeg",
        "pillow"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + pkgs)

def run_ltx_generation():
    import torch
    from diffusers import LTXImageToVideoPipeline
    from diffusers.utils import load_image, export_to_video
    from PIL import Image

    print("🚀 [2/4] 世界最高峰動画モデル Lightricks/LTX-Video のロード (A100 GPU / bfloat16)...", flush=True)
    t0 = time.time()
    
    pipe = LTXImageToVideoPipeline.from_pretrained(
        "Lightricks/LTX-Video",
        torch_dtype=torch.bfloat16,
        token=HF_TOKEN
    )
    pipe.to("cuda")
    print(f"✅ LTX-Video ロード完了 ({time.time() - t0:.2f}秒)", flush=True)

    output_dir = "/content/ltx_video_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # 入力タスク (Ch3: カフェテラスと波打ち際 / Ch1: 深夜書斎と月)
    tasks = [
        {
            "id": "ch3_auramelody_ltx_ocean",
            "image_path": "/content/input_images/ch3_auramelody_flux_dev.png",
            "prompt": "Cinematic 8k video. Crystal clear turquoise ocean waves realistically breaking and washing onto the powdery white sand next to the cafe terrace. Bright pink bougainvillea flowers gently swaying in the soft morning breeze. Sun glistening on the water surface, photorealistic, ultra-smooth motion.",
            "title": "Ch3: カフェテラス × リアルな波の流体物理モーション"
        },
        {
            "id": "ch1_haven_chill_ltx_room",
            "image_path": "/content/input_images/ch1_haven_chill_flux_dev.png",
            "prompt": "Cinematic 8k video. Soft moody night atmosphere. Gentle steam rising and swirling realistically from the ceramic coffee mug on the wooden desk. Warm amber light glowing from the brass banker lamp. Outside the window, a colossal glowing moon in the starry night sky. Ultra-detailed, soothing ambient movement.",
            "title": "Ch1: 深夜書斎 × 立ちのぼる湯気と温かい光のゆらめき"
        }
    ]

    print("\n🎬 [3/4] LTX-Video 究極動画レンダリング開始 (768x512 / 121 Frames / 25 FPS)...", flush=True)
    generated_videos = []

    for idx, item in enumerate(tasks, 1):
        if not os.path.exists(item["image_path"]):
            print(f"⚠️ 画像が見つかりません: {item['image_path']}")
            continue
            
        print(f"\n--- [{idx}/{len(tasks)}] レンダリング中: {item['title']} ---", flush=True)
        start_gen = time.time()
        
        # LTX-Video 最適サイズ (768x512 / 32の倍数)
        input_image = load_image(item["image_path"]).resize((768, 512), Image.Resampling.LANCZOS)
        
        # 121フレーム（約5秒間）の超滑らか動画
        video = pipe(
            image=input_image,
            prompt=item["prompt"],
            width=768,
            height=512,
            num_frames=121,
            num_inference_steps=35,
            guidance_scale=3.0,
            generator=torch.Generator("cuda").manual_seed(100 + idx)
        ).frames[0]
        
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.mp4")
        export_to_video(video, out_path, fps=25)
        generated_videos.append(out_path)
        print(f"✨ 最高峰動画完成: {out_path} (所要時間: {elapsed:.2f}秒 / 25fps)", flush=True)

    print("\n🎉 [4/4] 全LTX-Video最高峰動画のレンダリングが完了しました！", flush=True)
    print(f"出力ファイル一覧: {generated_videos}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_ltx_generation()
