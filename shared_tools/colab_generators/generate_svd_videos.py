#!/usr/bin/env python3
"""
Colab A100 GPU上で実行する 最高峰 Image-to-Video 動画生成スクリプト
モデル: stabilityai/stable-video-diffusion-img2vid-xt (SVD-XT)
"""
import os
import time
import subprocess
import sys

def setup_environment():
    print("📦 [1/4] 必要なライブラリのインストール...", flush=True)
    pkgs = [
        "torch",
        "diffusers",
        "transformers",
        "accelerate",
        "imageio",
        "imageio-ffmpeg",
        "pillow"
    ]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + pkgs)

def run_video_generation():
    import torch
    from diffusers import StableVideoDiffusionPipeline
    from diffusers.utils import load_image, export_to_video
    from PIL import Image

    print("🚀 [2/4] 最高峰動画モデル Stable Video Diffusion (SVD-XT) のロード (A100 GPU / fp16)...", flush=True)
    t0 = time.time()
    
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=torch.float16,
        variant="fp16"
    )
    pipe.to("cuda")
    print(f"✅ SVD-XT ロード完了 ({time.time() - t0:.2f}秒)", flush=True)

    output_dir = "/content/video_outputs"
    os.makedirs(output_dir, exist_ok=True)

    # 入力画像リスト (Colab上にアップロードされたFLUX.1-dev画像)
    input_tasks = [
        {
            "id": "ch3_auramelody_wave_loop",
            "image_path": "/content/input_images/ch3_auramelody_flux_dev.png",
            "title": "Ch3: カフェテラス × 透き通る波のモーション",
            "motion_bucket_id": 127,  # 自然な波・水の動き
            "fps": 7
        },
        {
            "id": "ch1_haven_chill_ambient_loop",
            "image_path": "/content/input_images/ch1_haven_chill_flux_dev.png",
            "title": "Ch1: 深夜書斎 × ランプの灯りと湯気のゆらめき",
            "motion_bucket_id": 85,   # 穏やかなアンビエントの動き
            "fps": 7
        }
    ]

    print("\n🎬 [3/4] シネマティック動画生成開始 (25 Frames / SVD-XT)...", flush=True)
    generated_videos = []

    for idx, item in enumerate(input_tasks, 1):
        if not os.path.exists(item["image_path"]):
            print(f"⚠️ 画像が見つかりません: {item['image_path']}")
            continue
            
        print(f"\n--- [{idx}/{len(input_tasks)}] レンダリング中: {item['title']} ---", flush=True)
        start_gen = time.time()
        
        # SVD-XT 最適解像度 (1024x576) にリサイズ
        image = load_image(item["image_path"])
        image = image.resize((1024, 576), Image.Resampling.LANCZOS)
        
        # 25フレーム動画生成
        frames = pipe(
            image,
            decode_chunk_size=8,
            generator=torch.Generator("cuda").manual_seed(42 + idx),
            motion_bucket_id=item["motion_bucket_id"],
            noise_aug_strength=0.05,
            num_frames=25
        ).frames[0]
        
        elapsed = time.time() - start_gen
        out_path = os.path.join(output_dir, f"{item['id']}.mp4")
        export_to_video(frames, out_path, fps=item["fps"])
        generated_videos.append(out_path)
        print(f"✨ 動画レンダリング完了: {out_path} (所要時間: {elapsed:.2f}秒)", flush=True)

    print("\n🎉 [4/4] 全シネマティック動画の生成が正常に完了しました！", flush=True)
    print(f"出力ファイル一覧: {generated_videos}", flush=True)

if __name__ == "__main__":
    setup_environment()
    run_video_generation()
