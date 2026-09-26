#!/usr/bin/env python3
"""
【SSD-1B 高品位生成 × Real-ESRGAN × シネマティック動画化パイプライン】
1. SSD-1B（ステップ数を12→28に大幅増量してディテール破綻を排除）
2. Real-ESRGAN x4plus で超高解像度4Kマスター画像（4096x2304）を生成
3. 超高解像度画像から滑らかなカメラワーク（Ken Burns / 緩やかなスライド＆ズーム）を施した
   10秒・フルHD（1080p / 24fps）の高品質ストック動画（.mp4）を自動生成
4. Adobe Stock提出用メタデータCSVに登録
"""

import os
import sys
import time
import subprocess
import csv
import math
import torch
from PIL import Image
from diffusers import StableDiffusionXLPipeline, EulerDiscreteScheduler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
UPSCALED_DIR = os.path.join(BASE_DIR, "outputs_upscaled")
VIDEOS_DIR = os.path.join(BASE_DIR, "outputs_videos")
MAIN_CSV = os.path.join(BASE_DIR, "adobe_stock_submission.csv")
REALESRGAN_BIN = os.path.join(BASE_DIR, "tools", "realesrgan", "realesrgan-ncnn-vulkan")
REALESRGAN_MODELS = os.path.join(BASE_DIR, "tools", "realesrgan", "models")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(UPSCALED_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

# 建築・ラグジュアリー空間のプロンプト（破綻が少なくストック需要の高い題材）
PROMPT_DATA = {
    "id": "arch_minimal_luxury_lounge",
    "title": "Minimalist Modern Architectural Lounge with Warm Sunlight and Polished Concrete",
    "keywords": [
        "modern architecture", "minimalist interior", "concrete wall", "wooden louvers",
        "sunlight shadows", "luxury lounge", "empty room", "spacious", "high ceiling",
        "clean lines", "contemporary", "commercial interior", "b roll", "4k", "1080p",
        "slow motion", "cinematic", "peaceful", "geometric design", "living room"
    ],
    "category": "Buildings and Architecture",
    "prompt": (
        "Minimalist modern architectural lounge interior. Exposed smooth raw concrete walls, "
        "warm natural oak wood vertical acoustic louvers, expansive floor-to-ceiling glass windows. "
        "Soft diffused morning golden hour sunlight casting sharp geometric shadows across polished limestone floor. "
        "Architectural digest photography style, razor sharp straight lines, clean craftsmanship, "
        "no crooked geometry, perfect perspective, 8k resolution, elegant serene atmosphere."
    ),
    "negative_prompt": (
        "worst quality, low quality, artifacts, distorted walls, crooked lines, blurry, "
        "noise, grainy, morphing, watermark, text, logos, ugly furniture, messy details"
    )
}

def load_pipeline():
    print("🚀 [1/4] SSD-1B モデルをメモリにロードしています...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"   ↳ 実行デバイス: {device.upper()} (Apple Silicon GPU)")
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "segmind/SSD-1B",
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        use_safetensors=True,
        variant="fp16" if device == "mps" else None
    )
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
    pipe.to(device)
    pipe.enable_attention_slicing()
    print("✅ ロード完了（ステップ数28でノイズ徹底除去設定）\n")
    return pipe

def run_ai_upscale(input_path, output_path):
    print(f"🔍 [2/4] Real-ESRGAN x4plus で超高解像度化 (4096px)...")
    cmd = [
        REALESRGAN_BIN,
        "-i", input_path,
        "-o", output_path,
        "-s", "4",
        "-n", "realesrgan-x4plus",
        "-m", REALESRGAN_MODELS
    ]
    t0 = time.time()
    subprocess.run(cmd, check=True)
    print(f"✅ アップスケール完了 ({time.time() - t0:.1f}秒): {os.path.basename(output_path)}\n")

def create_cinematic_video(image_path, output_video_path, duration_sec=10, fps=24, target_w=1920, target_h=1080):
    """
    超高解像度マスター画像から、滑らかなシネマティックカメラワーク（緩やかなズーム＆パン）を適用して
    Adobe Stock規格の10秒フルHD動画（H.264 mp4）を出力する
    """
    print(f"🎬 [3/4] シネマティック動画を生成中 ({duration_sec}秒, {fps}fps, {target_w}x{target_h})...")
    t0 = time.time()
    
    img = Image.open(image_path).convert("RGB")
    orig_w, orig_h = img.size
    total_frames = duration_sec * fps  # 240フレーム
    
    # カメラワーク設定:
    # 開始時: 画面中央やや左から、ズーム倍率 1.00 (最大視野)
    # 終了時: 画面中央やや右へスライドしつつ、ズーム倍率 1.10 (緩やかな寄り)
    # クロップ枠のアスペクト比は常に target_w : target_h (16:9)
    aspect = target_w / target_h
    
    # 基本の最大切り出し幅・高さ
    if orig_w / orig_h > aspect:
        base_h = orig_h
        base_w = int(orig_h * aspect)
    else:
        base_w = orig_w
        base_h = int(orig_w / aspect)
        
    start_zoom = 1.00
    end_zoom = 1.12
    
    # ffmpegのstdinパイプを開いて直接エンコード（ディスクに連番画像を保存しないため超高速・エコ）
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{target_w}x{target_h}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-crf", "17",
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_video_path
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    for i in range(total_frames):
        # スムーズなイージング (Sine Ease In-Out)
        progress = (1.0 - math.cos(math.pi * (i / (total_frames - 1)))) / 2.0
        
        # ズーム率
        current_zoom = start_zoom + (end_zoom - start_zoom) * progress
        cur_w = base_w / current_zoom
        cur_h = base_h / current_zoom
        
        # カメラスライド（左から右へ微細にパン）
        max_dx = orig_w - cur_w
        max_dy = orig_h - cur_h
        
        # X座標: 左寄り(15%)から右寄り(85%)へ移動
        cx = max_dx * (0.15 + 0.70 * progress)
        # Y座標: 中央付近を微細に安定維持
        cy = max_dy * 0.50
        
        crop_box = (int(cx), int(cy), int(cx + cur_w), int(cy + cur_h))
        frame = img.crop(crop_box).resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    
    print(f"✅ 動画生成完了 ({time.time() - t0:.1f}秒): {os.path.basename(output_video_path)}\n")

def record_to_csv(video_name, pdata):
    print("📝 [4/4] Adobe Stock提出用CSVにメタデータを登録中...")
    file_exists = os.path.exists(MAIN_CSV)
    
    with open(MAIN_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize(MAIN_CSV) == 0:
            writer.writerow(["Filename", "Title", "Keywords", "Category", "Releases", "Generative AI"])
        
        writer.writerow([
            video_name,
            pdata["title"],
            ", ".join(pdata["keywords"]),
            pdata["category"],
            "",
            "Yes"
        ])
    print(f"✅ メタデータ登録完了: {MAIN_CSV}\n")

def main():
    print("==========================================================")
    print("🏛️ SSD-1B(高ステップ) × Real-ESRGAN × シネマティック動画化")
    print("==========================================================")
    
    pipe = load_pipeline()
    timestamp = int(time.time())
    fid = PROMPT_DATA["id"]
    
    raw_img_name = f"{fid}_step28_{timestamp}.png"
    upscaled_img_name = f"{fid}_step28_{timestamp}_4k.jpg"
    final_video_name = f"{fid}_cinematic_1080p_{timestamp}.mp4"
    
    raw_img_path = os.path.join(OUTPUTS_DIR, raw_img_name)
    upscaled_img_path = os.path.join(UPSCALED_DIR, upscaled_img_name)
    final_video_path = os.path.join(VIDEOS_DIR, final_video_name)
    
    # 1. 画像生成（ステップ数28で破綻のない高品位生成）
    print(f"🎨 画像生成中 (ステップ数: 28, 解像度: 1024x576 16:9)...")
    t0 = time.time()
    result = pipe(
        prompt=PROMPT_DATA["prompt"],
        negative_prompt=PROMPT_DATA["negative_prompt"],
        num_inference_steps=28,
        guidance_scale=7.5,
        width=1024,
        height=576,
        generator=torch.Generator("cpu").manual_seed(12345)
    ).images[0]
    
    result.save(raw_img_path)
    print(f"✅ 原画生成完了 ({time.time() - t0:.1f}秒): {raw_img_name}\n")
    
    # メモリ解放
    del pipe
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
    
    # 2. AI超解像（4096px 4Kマスター化）
    run_ai_upscale(raw_img_path, upscaled_img_path)
    
    # 3. 10秒シネマティック動画化（240フレーム, フルHD, 24fps）
    create_cinematic_video(upscaled_img_path, final_video_path, duration_sec=10, fps=24)
    
    # 4. CSV登録
    record_to_csv(final_video_name, PROMPT_DATA)
    
    print("==========================================================")
    print("🎉 全工程が完了しました！")
    print(f"・原画(SSD-1B Step28) : {raw_img_path}")
    print(f"・4K超解像マスター     : {upscaled_img_path}")
    print(f"・完成動画(10秒 1080p): {final_video_path}")
    print(f"・登録CSV              : {MAIN_CSV}")
    print("==========================================================")

if __name__ == "__main__":
    main()
